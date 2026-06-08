from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import chromadb
from chromadb.api.models.Collection import Collection
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer

try:
    import pdfplumber
except ImportError:  # pragma: no cover
    pdfplumber = None


SUPPORTED_EXTENSIONS = {".txt", ".md", ".pdf"}
DEFAULT_DOCUMENTS_DIR = Path("documents")
DEFAULT_DB_DIR = Path("chroma_db")
DEFAULT_COLLECTION_NAME = "unofficial_guide"
DEFAULT_EMBED_MODEL = "all-MiniLM-L6-v2"
DEFAULT_CHUNK_SIZE = 700
DEFAULT_OVERLAP = 120
DEFAULT_TOP_K = 5


@dataclass
class DocumentRecord:
    source: str
    text: str


@dataclass
class ChunkRecord:
    chunk_id: str
    source: str
    chunk_index: int
    text: str


def _normalize_whitespace(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\t+", " ", text)
    text = re.sub(r"\u00a0", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ ]{2,}", " ", text)
    return text.strip()


def clean_text(raw_text: str) -> str:
    # Remove obvious HTML tags/entities if users pasted from web pages.
    text = re.sub(r"<[^>]+>", " ", raw_text)
    text = text.replace("&nbsp;", " ").replace("&amp;", "&")
    text = text.replace("&#39;", "'").replace("&quot;", '"')
    return _normalize_whitespace(text)


def _extract_pdf_text(path: Path) -> str:
    if pdfplumber is None:
        raise RuntimeError(
            "pdfplumber is required for PDF ingestion. Install dependencies with pip install -r requirements.txt"
        )

    pages: list[str] = []
    with pdfplumber.open(str(path)) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pages.append(text)
    return "\n\n".join(pages)


def load_documents(documents_dir: Path = DEFAULT_DOCUMENTS_DIR) -> list[DocumentRecord]:
    if not documents_dir.exists():
        raise FileNotFoundError(
            f"Documents directory not found: {documents_dir}. Create it and add source files first."
        )

    records: list[DocumentRecord] = []
    for path in sorted(documents_dir.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        if path.suffix.lower() == ".pdf":
            raw_text = _extract_pdf_text(path)
        else:
            raw_text = path.read_text(encoding="utf-8", errors="ignore")
        cleaned = clean_text(raw_text)
        if not cleaned:
            continue

        records.append(DocumentRecord(source=str(path), text=cleaned))

    if not records:
        raise ValueError(
            "No non-empty .txt/.md documents found in documents/. Add at least 10 files before indexing."
        )

    return records


def chunk_text(text: str, chunk_size: int = DEFAULT_CHUNK_SIZE, overlap: int = DEFAULT_OVERLAP) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be >= 0 and < chunk_size")

    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    current = ""

    for para in paragraphs:
        candidate = f"{current}\n\n{para}".strip() if current else para
        if len(candidate) <= chunk_size:
            current = candidate
            continue

        if current:
            chunks.append(current)

        # Long paragraph fallback: split by sentence-ish boundaries then by hard chars.
        if len(para) > chunk_size:
            sentence_parts = re.split(r"(?<=[.!?])\s+", para)
            temp = ""
            for part in sentence_parts:
                merged = f"{temp} {part}".strip() if temp else part
                if len(merged) <= chunk_size:
                    temp = merged
                else:
                    if temp:
                        chunks.append(temp)
                    if len(part) <= chunk_size:
                        temp = part
                    else:
                        start = 0
                        while start < len(part):
                            end = min(start + chunk_size, len(part))
                            piece = part[start:end].strip()
                            if piece:
                                chunks.append(piece)
                            if end >= len(part):
                                break
                            start = max(end - overlap, start + 1)
                        temp = ""
            current = temp
        else:
            current = para

    if current:
        chunks.append(current)

    # Apply overlap between adjacent chunks to preserve boundary context.
    if overlap == 0 or len(chunks) < 2:
        return [c for c in chunks if c.strip()]

    overlapped: list[str] = [chunks[0]]
    for idx in range(1, len(chunks)):
        prev = overlapped[-1]
        prefix = prev[-overlap:] if len(prev) > overlap else prev
        merged = f"{prefix}\n{chunks[idx]}".strip()
        overlapped.append(merged)

    return [c for c in overlapped if c.strip()]


def build_chunk_records(
    docs: list[DocumentRecord],
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_OVERLAP,
) -> list[ChunkRecord]:
    records: list[ChunkRecord] = []
    for doc in docs:
        chunks = chunk_text(doc.text, chunk_size=chunk_size, overlap=overlap)
        for i, chunk in enumerate(chunks):
            records.append(
                ChunkRecord(
                    chunk_id=f"{doc.source}::chunk_{i}",
                    source=doc.source,
                    chunk_index=i,
                    text=chunk,
                )
            )
    return records


def _get_collection(db_dir: Path = DEFAULT_DB_DIR, name: str = DEFAULT_COLLECTION_NAME) -> Collection:
    client = chromadb.PersistentClient(path=str(db_dir))
    return client.get_or_create_collection(name=name)


def build_index(
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_OVERLAP,
    db_dir: Path = DEFAULT_DB_DIR,
    collection_name: str = DEFAULT_COLLECTION_NAME,
    embedding_model: str = DEFAULT_EMBED_MODEL,
) -> dict[str, Any]:
    docs = load_documents(DEFAULT_DOCUMENTS_DIR)
    chunk_records = build_chunk_records(docs, chunk_size=chunk_size, overlap=overlap)

    if not chunk_records:
        raise ValueError("No chunks were produced. Check document loading and chunking settings.")

    embedder = SentenceTransformer(embedding_model)
    embeddings = embedder.encode([c.text for c in chunk_records], show_progress_bar=True)

    collection = _get_collection(db_dir=db_dir, name=collection_name)
    collection.upsert(
        ids=[c.chunk_id for c in chunk_records],
        documents=[c.text for c in chunk_records],
        embeddings=embeddings.tolist(),
        metadatas=[
            {
                "source": c.source,
                "chunk_index": c.chunk_index,
            }
            for c in chunk_records
        ],
    )

    return {
        "document_count": len(docs),
        "chunk_count": len(chunk_records),
        "collection": collection_name,
        "db_dir": str(db_dir),
        "chunk_size": chunk_size,
        "overlap": overlap,
        "embedding_model": embedding_model,
    }


def retrieve(
    question: str,
    top_k: int = DEFAULT_TOP_K,
    db_dir: Path = DEFAULT_DB_DIR,
    collection_name: str = DEFAULT_COLLECTION_NAME,
    embedding_model: str = DEFAULT_EMBED_MODEL,
) -> list[dict[str, Any]]:
    if not question.strip():
        return []

    collection = _get_collection(db_dir=db_dir, name=collection_name)
    embedder = SentenceTransformer(embedding_model)
    question_embedding = embedder.encode(question).tolist()

    result = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    docs = result.get("documents", [[]])[0]
    metas = result.get("metadatas", [[]])[0]
    distances = result.get("distances", [[]])[0]

    output: list[dict[str, Any]] = []
    for d, m, dist in zip(docs, metas, distances):
        output.append(
            {
                "text": d,
                "source": m.get("source", "unknown") if isinstance(m, dict) else "unknown",
                "chunk_index": m.get("chunk_index", -1) if isinstance(m, dict) else -1,
                "distance": float(dist),
            }
        )
    return output


def generate_answer(
    question: str,
    retrieved_chunks: list[dict[str, Any]],
    model: str = "llama-3.3-70b-versatile",
) -> str:
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        raise ValueError("GROQ_API_KEY is missing. Add it to .env first.")

    if not retrieved_chunks:
        return "I don't have enough information in the indexed documents to answer that."

    context_blocks: list[str] = []
    for idx, item in enumerate(retrieved_chunks, start=1):
        context_blocks.append(
            "\n".join(
                [
                    f"[Chunk {idx}]",
                    f"Source: {item['source']}",
                    f"Chunk index: {item['chunk_index']}",
                    f"Distance: {item['distance']:.4f}",
                    item["text"],
                ]
            )
        )

    prompt = (
        "You are a retrieval-grounded assistant for student knowledge. "
        "Answer ONLY using the provided context chunks. "
        "If the context is insufficient, say exactly: \"I don't have enough information on that.\" "
        "Do not use outside knowledge.\n\n"
        f"Question: {question}\n\n"
        "Context:\n"
        + "\n\n---\n\n".join(context_blocks)
        + "\n\nReturn a concise answer with no fabricated details."
    )

    client = Groq(api_key=api_key)
    completion = client.chat.completions.create(
        model=model,
        temperature=0,
        messages=[
            {"role": "system", "content": "You must be strictly grounded in retrieved context."},
            {"role": "user", "content": prompt},
        ],
    )

    answer = completion.choices[0].message.content or ""
    return answer.strip() or "I don't have enough information on that."


def ask(question: str, top_k: int = DEFAULT_TOP_K) -> dict[str, Any]:
    retrieved = retrieve(question, top_k=top_k)
    answer = generate_answer(question, retrieved)

    unique_sources = []
    seen = set()
    for item in retrieved:
        src = item["source"]
        if src not in seen:
            seen.add(src)
            unique_sources.append(src)

    return {
        "answer": answer,
        "sources": unique_sources,
        "retrieved_chunks": retrieved,
    }

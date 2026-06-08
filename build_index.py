from __future__ import annotations

import argparse

from src.rag_pipeline import build_index


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Chroma index from local documents.")
    parser.add_argument("--chunk-size", type=int, default=700)
    parser.add_argument("--overlap", type=int, default=120)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    stats = build_index(chunk_size=args.chunk_size, overlap=args.overlap)

    print("Index build complete")
    print(f"Documents indexed: {stats['document_count']}")
    print(f"Chunks indexed: {stats['chunk_count']}")
    print(f"Embedding model: {stats['embedding_model']}")
    print(f"Collection: {stats['collection']}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import random

from src.rag_pipeline import build_chunk_records, load_documents


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect random chunks for quality checks.")
    parser.add_argument("--chunk-size", type=int, default=700)
    parser.add_argument("--overlap", type=int, default=120)
    parser.add_argument("--samples", type=int, default=5)
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    docs = load_documents()
    chunks = build_chunk_records(docs, chunk_size=args.chunk_size, overlap=args.overlap)

    print(f"Documents loaded: {len(docs)}")
    print(f"Total chunks: {len(chunks)}")

    if not chunks:
        print("No chunks were produced.")
        return

    sample_count = min(args.samples, len(chunks))
    picks = random.sample(chunks, sample_count)

    for i, chunk in enumerate(picks, start=1):
        print("=" * 80)
        print(f"Sample {i}")
        print(f"Source: {chunk.source}")
        print(f"Chunk index: {chunk.chunk_index}")
        print(f"Length: {len(chunk.text)}")
        print("-" * 80)
        print(chunk.text)
        print()


if __name__ == "__main__":
    main()

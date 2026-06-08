from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.rag_pipeline import retrieve


DEFAULT_QUERIES_PATH = Path("retrieval_queries.json")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run retrieval-only quality checks.")
    parser.add_argument("--queries-path", type=str, default=str(DEFAULT_QUERIES_PATH))
    parser.add_argument("--top-k", type=int, default=5)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    queries_path = Path(args.queries_path)

    if not queries_path.exists():
        raise FileNotFoundError(
            f"{queries_path} not found. Create it with at least 3 queries under a 'queries' array."
        )

    payload = json.loads(queries_path.read_text(encoding="utf-8"))
    queries = [str(q).strip() for q in payload.get("queries", []) if str(q).strip()]
    if len(queries) < 3:
        raise ValueError("Add at least 3 queries to retrieval_queries.json")

    for query in queries:
        print("=" * 100)
        print(f"Query: {query}")
        results = retrieve(query, top_k=args.top_k)
        if not results:
            print("No results returned")
            continue

        for idx, item in enumerate(results, start=1):
            print("-" * 100)
            print(f"Rank: {idx}")
            print(f"Source: {item['source']}")
            print(f"Chunk index: {item['chunk_index']}")
            print(f"Distance: {item['distance']:.4f}")
            preview = item["text"][:300].replace("\n", " ")
            print(f"Preview: {preview}")
        print()


if __name__ == "__main__":
    main()

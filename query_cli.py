from __future__ import annotations

import argparse
import json

from src.rag_pipeline import ask


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Query the Unofficial Guide RAG system from CLI.")
    parser.add_argument("question", type=str, help="Question to ask")
    parser.add_argument("--top-k", type=int, default=5)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = ask(args.question, top_k=args.top_k)
    print(json.dumps(result, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()

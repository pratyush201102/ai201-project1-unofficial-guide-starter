from __future__ import annotations

import json
from pathlib import Path

from src.rag_pipeline import ask


QUESTIONS_PATH = Path("evaluation_questions.json")
OUTPUT_PATH = Path("evaluation_results.json")


def main() -> None:
    if not QUESTIONS_PATH.exists():
        raise FileNotFoundError(
            "evaluation_questions.json not found. Create it with 5 test questions first."
        )

    payload = json.loads(QUESTIONS_PATH.read_text(encoding="utf-8"))
    questions = payload.get("questions", [])
    if not questions:
        raise ValueError("No questions found in evaluation_questions.json")

    results = []
    for item in questions:
        question = str(item.get("question", "")).strip()
        expected = str(item.get("expected_answer", "")).strip()
        if not question:
            continue

        output = ask(question)
        results.append(
            {
                "question": question,
                "expected_answer": expected,
                "system_answer": output["answer"],
                "sources": output["sources"],
                "retrieved_chunks": output["retrieved_chunks"],
                "retrieval_quality": "",
                "response_accuracy": "",
                "notes": "",
            }
        )

    OUTPUT_PATH.write_text(json.dumps({"results": results}, indent=2, ensure_ascii=True), encoding="utf-8")
    print(f"Saved {len(results)} evaluation entries to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

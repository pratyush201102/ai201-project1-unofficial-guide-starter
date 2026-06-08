from __future__ import annotations

import csv
from pathlib import Path

SOURCE_LOG = Path("source_log.csv")
OUTPUT = Path("generated/source_tables.md")


def to_planning_table(rows: list[dict[str, str]]) -> str:
    lines = [
        "| # | Source | Description | URL or location |",
        "|---|--------|-------------|-----------------|",
    ]
    for r in rows:
        lines.append(
            f"| {r['id']} | {r['source_name']} | {r['notes']} | {r['url_or_path']} |"
        )
    return "\n".join(lines)


def to_readme_table(rows: list[dict[str, str]]) -> str:
    lines = [
        "| # | Source | Type | URL or file path |",
        "|---|--------|------|-----------------|",
    ]
    for r in rows:
        lines.append(
            f"| {r['id']} | {r['source_name']} | {r['source_type']} | {r['url_or_path']} |"
        )
    return "\n".join(lines)


def main() -> None:
    if not SOURCE_LOG.exists():
        raise FileNotFoundError("source_log.csv not found")

    with SOURCE_LOG.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    rows = [r for r in rows if (r.get("source_name", "").strip() or r.get("url_or_path", "").strip())]
    if not rows:
        raise ValueError("No filled source rows found in source_log.csv")

    planning = to_planning_table(rows)
    readme = to_readme_table(rows)

    OUTPUT.write_text(
        "# Generated Source Tables\n\n"
        "## planning.md Documents Table\n\n"
        f"{planning}\n\n"
        "## README.md Document Sources Table\n\n"
        f"{readme}\n",
        encoding="utf-8",
    )

    print(f"Wrote source table snippets to {OUTPUT}")


if __name__ == "__main__":
    main()

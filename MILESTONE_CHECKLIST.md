# Project 1 Milestone Checklist

## Milestone 1: Domain + Documents

- [ ] Choose one domain and write a 2–3 sentence summary.
- [ ] Collect at least 10 source documents.
- [ ] Record all sources in `source_log.csv`.
- [ ] Run: `python sync_sources.py` and paste generated tables into planning/README.
- [ ] Copy source list into `planning.md` and `README.md` tables.
- [ ] Commit milestone progress.

## Milestone 2: Spec

- [ ] Fill all sections in `planning.md` with real project values.
- [ ] Finalize chunk size + overlap and rationale.
- [ ] Finalize embedding model + top-k.
- [ ] Define 5 evaluation questions with expected answers.
- [ ] Commit milestone progress.

## Milestone 3: Ingestion + Chunking

- [ ] Add document files to `documents/`.
- [ ] Run: `python inspect_chunks.py --chunk-size 700 --overlap 120 --samples 5`
- [ ] Verify chunk quality (self-contained and clean).
- [ ] Run: `python build_index.py --chunk-size 700 --overlap 120`
- [ ] Commit milestone progress.

## Milestone 4: Embedding + Retrieval

- [ ] Fill `retrieval_queries.json` with 3 evaluation-style queries.
- [ ] Run: `python retrieval_check.py --top-k 5`
- [ ] Verify top chunk distances and relevance.
- [ ] Tune chunking or top-k if needed.
- [ ] Commit milestone progress.

## Milestone 5: Generation + Interface

- [ ] Run: `python app.py`
- [ ] Test 2 in-scope questions and 1 out-of-scope question.
- [ ] Verify source attribution is always shown.
- [ ] Save sample outputs for README.
- [ ] Commit milestone progress.

## Milestone 6: Evaluation + Documentation

- [ ] Fill `evaluation_questions.json`.
- [ ] Run: `python evaluate.py`
- [ ] Copy outputs into README evaluation table.
- [ ] Document one honest failure case with root cause.
- [ ] Record 3–5 minute demo video.
- [ ] Final commit for submission.

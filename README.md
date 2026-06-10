# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

## Local Runbook

1. Add your source documents into `documents/` as `.txt`, `.md`, or `.pdf` files.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Build embeddings index:

```bash
python build_index.py --chunk-size 700 --overlap 120
```

Optional milestone checks before generation:

```bash
python inspect_chunks.py --chunk-size 700 --overlap 120 --samples 5
```

Fill `retrieval_queries.json` with at least 3 test queries, then run:

```bash
python retrieval_check.py --top-k 5
```

4. Test from CLI:

```bash
python query_cli.py "What do students say about professor feedback quality?" --top-k 5
```

5. Run interface:

```bash
python app.py
```

6. Run evaluation helper after filling `evaluation_questions.json`:

```bash
python evaluate.py
```

The script writes `evaluation_results.json`; copy the results into the Evaluation Report table below and add your qualitative judgments.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | RMP Intro Programming reviews set 1 | manual_export_txt | documents/rmp_intro_programming_reviews_01.txt |
| 2 | RMP Data Structures reviews set 1 | manual_export_txt | documents/rmp_data_structures_reviews_01.txt |
| 3 | RMP Algorithms reviews set 1 | manual_export_txt | documents/rmp_algorithms_reviews_01.txt |
| 4 | Reddit CSMajors thread set 1 | manual_export_txt | documents/reddit_csmajors_professor_advice_01.txt |
| 5 | Reddit University subreddit thread set 1 | manual_export_txt | documents/reddit_university_course_selection_01.txt |
| 6 | Department unofficial FAQ copy | manual_export_md | documents/unofficial_department_faq.md |
| 7 | Discord senior advice transcript 1 | manual_export_txt | documents/discord_senior_advice_01.txt |
| 8 | Campus tutoring feedback notes | manual_export_txt | documents/tutoring_center_feedback_01.txt |
| 9 | Assignment turnaround discussion set 1 | manual_export_txt | documents/assignment_turnaround_discussion_01.txt |
| 10 | Course workload comparison notes | manual_export_txt | documents/course_workload_comparison_01.txt |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**
Initial: 700 characters; tuned to 500 characters during implementation.

**Overlap:**
Initial: 120 characters; tuned to 150 characters to reduce split-context failures.
**Why these choices fit your documents:**

**Final chunk count:**

30 chunks across all documents (after tuning and re-indexing).
---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

`all-MiniLM-L6-v2` via `sentence-transformers` (local inference)
**Production tradeoff reflection:**

For production I'd evaluate larger, higher-fidelity embedding models (or model ensembles) to improve semantic matching on noisy, short-form review text. Tradeoffs include increased latency and cost vs. better retrieval precision; I'd also consider API-hosted models for maintenance simplicity or private on-prem models for privacy-sensitive data.
---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

The generation step constructs a grounded prompt that includes the user query followed by the top-k retrieved chunks (each prefixed by its source filename). The instruction explicitly tells the LLM to: (1) answer using only the provided retrieved text; (2) include inline source attributions for factual claims; and (3) respond with "I don't know" or a short insufficient-information reply when the retrieved context doesn't contain an answer.
**How source attribution is surfaced in the response:**

Responses are returned as JSON with the `system_answer` string and a `sources` array listing the filenames of the top retrieved documents. The UI also displays retrieved chunk previews and distances so users can inspect grounding.
---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What do students say about how difficult Professor X exams are? | Summary of reported exam difficulty with citations (trick questions, emphasis on lecture examples, cumulative final) | System returns that exams focus on lecture examples, include "trick" questions, and the final is cumulative; cites multiple RMP and forum files. | Partially relevant (top 1–2 chunks relevant; some noisy results) | Partially accurate |
| 2 | Do students mention whether attendance matters for Course Y? | Grounded yes/no with nuance and sources | System answers yes — recommends attending lectures and copying examples; cites forum and review excerpts. | Relevant | Accurate |
| 3 | What feedback do students give about assignment turnaround time? | Typical wait times and consistency issues (3–5 days vs 2+ weeks) | System reports mixed turnaround: some courses 3–5 days, others 2+ week delays; cites assignment turnaround and FAQ files. | Relevant | Accurate |
| 4 | Which course is described as having the heaviest weekly workload? | Comparative answer referencing project-heavy courses and Data Structures hours | System identifies project-heavy courses as peaking at 20+ hours and Data Structures ~10–15 hours; cites workload comparison and DS reviews. | Relevant | Accurate |
| 5 | Are there contradictory opinions about Professor Z's grading fairness? | Balanced answer that acknowledges disagreement with citations | System acknowledges mixed opinions and cites RMP and discussion threads showing disagreement. | Partially relevant (some chunks marginal) | Partially accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

Question 1 (exam difficulty summary) — partial failures in completeness.
**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

Some relevant facts were split across adjacent chunks and the retrieval ranking returned only one of the two complementary chunks. This caused the generator to miss a qualifying detail. The root cause is chunking + retrieval ranking, not the generation step.
**What you would change to fix it:**

- Increase overlap or use a paragraph-aware splitter that preserves logical paragraphs.
- Add lightweight metadata (course/professor normalized tokens) to improve targeting.
- Consider re-ranking retrieved chunks with a cross-encoder or using a denser top-10 then re-rank top-5 approach.
---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

The `planning.md` chunking and retrieval sections gave clear constraints that made it straightforward to implement the `chunk_text()` and indexing steps without iterating on format decisions.
**One way your implementation diverged from the spec, and why:**

I initially used the specified 700/120 chunking but tuned to 500/150 after inspection because the short-review corpus benefited from smaller chunks with larger overlap; this change improved top-k relevance in testing.
---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 1 — Code scaffolding (Copilot / GitHub Copilot):**

- *What I gave the AI:* The `Chunking Strategy` and `Retrieval Approach` sections from `planning.md` and examples of document files.
- *What it produced:* Initial implementations of `load_documents()`, `clean_text()`, and `chunk_text()` helper functions.
- *What I changed or overrode:* Tuned the chunk size and overlap and added paragraph-cleaning logic to remove navigation artifacts.

**Instance 2 — Generation and testing (Groq + local model calls):**

- *What I gave the AI:* Grounded prompt template and retrieved context for each query; asked for concise, source-attributed answers.
- *What it produced:* `generate_answer()` outputs used in `evaluate.py` and `app.py` which include `system_answer` and `sources` fields.
- *What I changed or overrode:* Added explicit insistence in the prompt to answer "I don't know" if evidence is insufficient, and formatted the output as JSON for evaluation.

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

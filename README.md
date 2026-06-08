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

**Overlap:**

**Why these choices fit your documents:**

**Final chunk count:**

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

**Production tradeoff reflection:**

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

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

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

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

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

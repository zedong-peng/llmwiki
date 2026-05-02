---
title: "FollowIR: Evaluating and Teaching Information Retrieval Models to Follow Instructions"
domain: research
area: misc
type: paper
status: processed
updated: 2026-04-19
tags: [paper, retrieval, instruction-following, benchmark, beir-adjacent, followir]
---
# FollowIR: Evaluating and Teaching Information Retrieval Models to Follow Instructions

## Paper Meta
- Title: FollowIR: Evaluating and Teaching Information Retrieval Models to Follow Instructions
- Authors: Omar Khattab, Keshav Santhanam, and collaborators
- Year: 2025
- Venue: NAACL 2025 Long Paper; source snapshot from arXiv preprint
- Topic: misc
- Paper Slug: followir-2025
- arXiv: https://arxiv.org/abs/2403.15246
- PDF: `2403.15246.pdf`
- Code Repo: https://github.com/orionw/FollowIR
- Reading Source: TeX (`source/extracted/colm2024_conference.tex`, `source/extracted/tables/main.tex`, `source/extracted/tables/instructir.tex`)
- Repo Read: yes (`repo/FollowIR/README.md`)
- PDF Fallback: not used

## TL;DR
- FollowIR extends standard IR evaluation from short keyword-style queries to long natural-language instructions with constraints, preferences, and negative requirements.
- The benchmark is built from TREC narrative fields, so it targets a real retrieval weakness: models can retrieve topic-relevant documents yet still ignore what the user actually asked for.
- The paper introduces a paired metric, `p-MRR`, to measure instruction sensitivity by checking whether a model prefers a document satisfying the full instruction over a semantically related distractor that violates it.
- Training on the proposed data produces a large gap over general-purpose instruction-tuned LLMs and retrievers on instruction-sensitive retrieval.

## Problem
- Most retrieval benchmarks, including [[beir-2021]], evaluate topical relevance with short queries.
- Real retrieval tasks often contain constraints such as chronology, inclusion and exclusion criteria, comparison targets, or desired evidence forms.
- The paper asks whether current retrieval systems actually follow such instructions rather than only matching topic words.

## Method
- Construct instruction-following retrieval examples from the narrative portions of TREC topics:
  - Robust04
  - Core17
  - News21
- Build pairwise evaluation examples where one candidate satisfies the instruction better than another.
- Train `FollowIR-7B`, a retrieval model specialized for following instructions in addition to topical matching.
- Evaluate with standard retrieval metrics plus `p-MRR`, which directly rewards choosing the instruction-compliant candidate.

## Benchmarks / Datasets
| Dataset / Benchmark | Role in Paper | Metric | Notes |
|---|---|---|---|
| Robust04 narratives | evaluation + training source | MAP, p-MRR | classic newswire IR with narrative constraints |
| Core17 narratives | evaluation + training source | MAP, p-MRR | TREC Core 2017 |
| News21 narratives | evaluation + training source | nDCG@10, p-MRR | TREC news retrieval |
| InstructIR | external robustness transfer | Robustness@10 | instruction robustness comparison table |

## Baselines
| Baseline | Type | Why Important | Notes |
|---|---|---|---|
| BM25 variants | sparse retrieval | topical baseline | strong lexical anchor but weak instruction following |
| E5-family retrievers | dense retrieval | modern embedding baseline | good topical transfer, weaker constraint handling |
| Mistral-7B-Instruct | generative LLM baseline | tests whether generic instruction tuning helps IR | much weaker on instruction-robust retrieval |
| Other IR retrievers in table | retrieval baselines | shows gap between topical retrieval and instruction following | exact mix reported in main tables |

## Main Results
| Setting | Metric | Score | Notes |
|---|---|---:|---|
| FollowIR-7B on Robust04 | MAP | 24.8 | main table |
| FollowIR-7B on Robust04 | p-MRR | 13.7 | main table |
| FollowIR-7B on Core17 | MAP | 20.0 | main table |
| FollowIR-7B on Core17 | p-MRR | 16.5 | main table |
| FollowIR-7B on News21 | nDCG@10 | 29.6 | main table |
| FollowIR-7B on News21 | p-MRR | 6.3 | main table |
| FollowIR-7B average | Score | 24.8 | averaged primary metric across datasets |
| FollowIR-7B average | p-MRR | 12.2 | averaged instruction-sensitive metric |
| FollowIR-7B on InstructIR | Robustness@10 | 71.5 | from `tables/instructir.tex` |
| Mistral-7B-Instruct on InstructIR | Robustness@10 | 35.3 | large gap to specialized retriever |

- The important pattern is not the absolute MAP value; it is the consistent gain on `p-MRR`, which is the paper's direct signal for instruction compliance.

## Ablations / Analysis
- The paper argues that topic relevance and instruction compliance are separable abilities.
- Long instructions expose failures that are largely hidden on short-query benchmarks like BEIR.
- A generic instruction-tuned LLM is not automatically a strong instruction-following retriever.
- `p-MRR` is strategically useful because standard ranking metrics can miss cases where the top result is on-topic but violates the query constraints.

## Implementation Clues
- `repo/FollowIR/README.md` points to the dataset and training setup rather than a large general-purpose retrieval toolkit.
- The benchmark lineage is operationally simple: TREC narrative fields are the core raw material.
- For future work, the paper is useful as a benchmark interface and metric design reference more than as a heavyweight systems paper.

## Limitations
- The benchmark domain is still narrow relative to the full web.
- Reported systems are specialized around this evaluation setup, so direct comparison with broad BEIR-style retrievers needs care.
- The exact training and engineering details are lighter than in large toolkit papers.

## Takeaways
- FollowIR is one of the most relevant benchmark papers to read after BEIR if the question is "does retrieval follow instructions rather than only match topics?"
- It supplies a concrete metric and a realistic benchmark construction route using TREC narratives.
- For the BRIGHT thread, this is a stronger neighbor than another generic BEIR-improvement paper because it changes what retrieval quality means.

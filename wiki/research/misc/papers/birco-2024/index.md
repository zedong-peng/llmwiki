---
title: "BIRCO: A Benchmark of Information Retrieval Tasks with Complex Objectives"
domain: research
area: misc
type: paper
status: processed
updated: 2026-04-19
tags: [paper, retrieval, benchmark, complex-objectives, beir-adjacent, birco]
---
# BIRCO: A Benchmark of Information Retrieval Tasks with Complex Objectives

## Paper Meta
- Title: BIRCO: A Benchmark of Information Retrieval Tasks with Complex Objectives
- Authors: Lilli Kiesel, Katsiaryna Mararskaya, and collaborators
- Year: 2024
- Venue: arXiv preprint
- Topic: misc
- Paper Slug: birco-2024
- arXiv: https://arxiv.org/abs/2402.14151
- PDF: `2402.14151.pdf`
- Code Repo: https://github.com/BIRCO-benchmark/BIRCO_dataset
- Reading Source: TeX (`source/extracted/main.tex`)
- Repo Read: yes (`repo/BIRCO_dataset/README.md`)
- PDF Fallback: not used

## TL;DR
- BIRCO is a benchmark for retrieval tasks where the objective is not a simple topical query but a constrained or multi-criteria request.
- It is deliberately hard in a different way from BEIR: candidate pools are relatively small, yet the query semantics are much richer and more compositional.
- Strong BEIR models degrade sharply on BIRCO, which is the paper's main point.
- This benchmark is one of the cleanest bridges from classical IR evaluation toward reasoning-like or instruction-heavy retrieval.

## Problem
- Standard retrieval benchmarks mostly reward topical similarity.
- Many realistic retrieval tasks ask for documents satisfying multiple properties at once, such as a specific argumentative stance, a matching clinical condition, or a specific book identity from indirect clues.
- The paper asks whether retrievers that look strong on BEIR still perform well when the retrieval objective itself becomes structurally complex.

## Method
- Assemble five retrieval tasks with complex objectives:
  - DORIS-MAE
  - ArguAna
  - WhatsThatBook
  - Clinical-Trial
  - RELIC
- Normalize them into a common retrieval benchmark format.
- Measure complexity statistics such as query length, document length, relevant documents per query, and lexical overlap.
- Filter likely contamination using LLM-assisted checks before final evaluation.

## Benchmarks / Datasets
| Dataset / Benchmark | Role in Paper | Metric | Notes |
|---|---|---|---|
| DORIS-MAE | benchmark task | nDCG@10 | complex archival retrieval |
| ArguAna | benchmark task | nDCG@10 | argumentative stance retrieval |
| WhatsThatBook | benchmark task | nDCG@10 | clue-based book retrieval |
| Clinical-Trial | benchmark task | nDCG@10 | condition/intervention matching |
| RELIC | benchmark task | nDCG@10 | citation / reference-style retrieval |
| BEIR average | external comparison | avg. nDCG@10 | used to contrast with BIRCO transfer |

## Benchmark Statistics
| Statistic | Average | Notes |
|---|---:|---|
| Queries per task | 51.3 | across the five tasks |
| Documents per task | 66.0 | small pools, semantically demanding |
| Relevant docs per query | 8.4 | multiple acceptable answers common |
| Query length | 168.3 | much longer than typical BEIR queries |
| Document length | 185.1 | moderate |
| Lexical overlap | 0.083 | low direct term overlap |

## Baselines
| Baseline | Type | Why Important | Notes |
|---|---|---|---|
| E5-large-v2 | dense retriever | strong general embedding baseline | large BEIR to BIRCO gap |
| RankLLaMA | reranker / retrieval model | stronger modern ranking baseline | still drops notably |
| TART | instruction-aware retriever | relevant because tasks are instruction-like | transfer remains limited |

## Main Results
| Setting | Metric | Score | Notes |
|---|---|---:|---|
| E5-large-v2 on BEIR | avg. nDCG@10 | 50.0 | comparison anchor |
| E5-large-v2 on BIRCO | avg. nDCG@10 | 38.5 | substantial drop |
| RankLLaMA on BEIR | avg. nDCG@10 | 56.6 | comparison anchor |
| RankLLaMA on BIRCO | avg. nDCG@10 | 47.4 | still materially lower |
| TART on BEIR | avg. nDCG@10 | 44.8 | instruction-aware baseline |
| TART on BIRCO | avg. nDCG@10 | 39.5 | limited transfer advantage |

- The paper's core result is that retrieval quality on BEIR does not carry over cleanly to complex-objective tasks.

## Ablations / Analysis
- BIRCO has much longer queries and lower lexical overlap than standard BEIR-style datasets.
- The contamination analysis is unusually important:
  - 7% removed from Clinical-Trial
  - 8% removed from RELIC
  - 56% removed from WhatsThatBook
  - none removed from DORIS-MAE and ArguAna
- This strengthens the claim that the remaining performance gap is not just memorization.
- The benchmark is intentionally compact in corpus size, which means the challenge is semantic objective matching rather than web-scale search.

## Implementation Clues
- `repo/BIRCO_dataset/README.md` is primarily a data-release repository rather than a training codebase.
- The repo is most useful for understanding task packaging and downloading the benchmark.
- The paper is therefore better treated as an evaluation benchmark note than a systems implementation note.

## Limitations
- Small candidate pools make BIRCO less representative of first-stage industrial retrieval.
- Some tasks are heterogeneous enough that average scores hide per-task behavior.
- Because the repo is dataset-centric, exact reproduction of every baseline may require external codebases.

## Takeaways
- BIRCO is a high-value benchmark paper because it exposes a real blind spot in BEIR-era evaluation.
- It is especially useful when the retrieval question includes multiple constraints or latent objectives.
- Relative to BRIGHT, BIRCO is the nearest benchmark if the goal is to study "complex retrieval objectives" rather than general zero-shot transfer.

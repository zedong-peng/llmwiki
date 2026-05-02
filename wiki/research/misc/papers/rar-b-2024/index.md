---
title: "RAR-b: Reasoning as Retrieval Benchmark"
domain: research
area: misc
type: paper
status: processed
updated: 2026-04-19
tags: [paper, retrieval, reasoning, benchmark, beir-adjacent, rar-b]
---
# RAR-b: Reasoning as Retrieval Benchmark

## Paper Meta
- Title: RAR-b: Reasoning as Retrieval Benchmark
- Authors: Akari Asai, Omar Khattab, and collaborators
- Year: 2024
- Venue: arXiv preprint
- Topic: misc
- Paper Slug: rar-b-2024
- arXiv: https://arxiv.org/abs/2404.06347
- PDF: `2404.06347.pdf`
- Code Repo: https://github.com/gowitheflow-1998/RAR-b
- Reading Source: TeX (`source/extracted/paper.tex`)
- Repo Read: yes (`repo/RAR-b/README.md`)
- PDF Fallback: not used

## TL;DR
- RAR-b converts reasoning tasks into retrieval tasks so that reasoning ability can be probed with retrievers and rerankers rather than only generators.
- The benchmark includes both multiple-choice retrieval and full-corpus retrieval settings, which is useful because it separates "pick the right option" from "find the right evidence in a larger pool."
- A striking result is that instruction-aware retrievers can do worse when the task instructions are included.
- Fine-tuned rerankers dominate the benchmark, suggesting current dual-encoder retrieval is still weak as a reasoning substrate.

## Problem
- Many papers talk about retrieval helping reasoning, but few isolate whether retrievers themselves can perform reasoning-like discrimination.
- The authors ask whether retrieval models can solve tasks that require commonsense, temporal, spatial, mathematical, or code reasoning when phrased as retrieval.

## Method
- Transform reasoning benchmarks into retrieval benchmarks.
- Evaluate two settings:
  - Multiple-choice retrieval, scored by accuracy
  - Full-dataset retrieval, scored by ranking metrics such as nDCG@10 and Recall@10
- Cover 12 tasks derived from 17 source datasets across:
  - commonsense reasoning
  - temporal reasoning
  - spatial reasoning
  - mathematics
  - code
- Compare sparse, dense, instruction-aware, and reranking systems under the same framing.

## Benchmarks / Datasets
| Dataset / Benchmark | Role in Paper | Metric | Notes |
|---|---|---|---|
| 12 RAR-b tasks | main benchmark | Accuracy, nDCG@10, Recall@10 | transformed from 17 reasoning datasets |
| Multiple-choice retrieval | evaluation setting | Accuracy | easier controlled setting |
| Full-dataset retrieval | evaluation setting | nDCG@10, Recall@10 | more realistic retrieval setup |
| MTEB integration | tooling | not a paper metric | repo exposes benchmark wrapper |

## Baselines
| Baseline | Type | Why Important | Notes |
|---|---|---|---|
| Instruction-aware retrievers | dense retrieval | tests whether verbal instructions help | surprising degradation in some tasks |
| Dual-dense retrievers | dense retrieval | standard retrieval backbone | weak on reasoning-heavy tasks |
| Rerankers | ranking models | strongest performers | best overall benchmark behavior |
| Sparse baselines | lexical retrieval | calibration | useful lower-bound reference |

## Main Results
- The paper's most important findings are qualitative and benchmark-wide:
  - instruction-aware retrievers often perform better **without** the natural-language task instruction
  - current dense retrievers are poor late-interaction reasoners
  - a fine-tuned reranker is state of the art across all reported task categories
- The main contribution is therefore the benchmark and the failure mode it reveals, not a single new architecture.

## Ablations / Analysis
- Including instructions can inject noise instead of useful task guidance for retrievers.
- RAR-b argues that current retrieval encoders still over-index on superficial similarity rather than task-conditional reasoning.
- The multiple-choice setting is useful diagnostically, but the full-dataset setting is closer to actual retrieval use.
- Relative to BRIGHT, this benchmark is more synthetic in construction: it repackages reasoning datasets as retrieval problems rather than starting from realistic long-form document search.

## Implementation Clues
- `repo/RAR-b/README.md` documents the benchmark usage and dataset loading.
- The repo includes `HFDataLoader`, task-specific instruction mapping, and MTEB-compatible wrappers.
- That makes RAR-b operationally useful if I want to benchmark retrieval models on reasoning-heavy tasks without rebuilding datasets by hand.

## Limitations
- The benchmark is powerful diagnostically but still somewhat synthetic relative to open-domain search.
- Because tasks are transformed from reasoning datasets, success may not transfer directly to real document retrieval.
- The paper emphasizes evaluation more than deployable retrieval-system design.

## Takeaways
- RAR-b is important because it cleanly isolates a question many retrieval papers blur: can a retriever itself behave like a reasoner?
- The answer from this paper is mostly no for dense retrievers, and only partially yes for rerankers.
- For the current misc library, RAR-b is best filed next to BRIGHT and BIRCO as a benchmark that changes the target capability, not just the score.

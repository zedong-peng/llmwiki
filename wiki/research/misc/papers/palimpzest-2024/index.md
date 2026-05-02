---
title: "Palimpzest: A Declarative System for Optimizing AI Workloads"
domain: research
area: misc
type: paper
status: processed
updated: 2026-04-19
tags: [paper, misc, ai-systems, database-optimization, declarative-programming]
---
# Palimpzest: A Declarative System for Optimizing AI Workloads

## Paper Meta
- Title: Palimpzest: A Declarative System for Optimizing AI Workloads
- Authors: Chunwei Liu, Matthew Russo, Michael Cafarella, Lei Cao, Peter Baille Chen, Zui Chen, Michael Franklin, Tim Kraska, Samuel Madden, Gerardo Vitagliano
- Year: 2024
- Venue: arXiv preprint
- Topic: misc
- Paper Slug: palimpzest-2024
- arXiv: https://arxiv.org/abs/2405.14696
- PDF: palimpzest-2405.14696.pdf
- Code Repo: https://github.com/mitdbg/palimpzest
- Reading Source: TeX/source
- Legacy Note: [[llm-grep-retrieval/papers/liu-2024-palimpzest]]

## TL;DR
- Palimpzest is a declarative system for semantic analytics applications, meaning AI workloads that mix conventional data processing with model-backed extraction, filtering, and multimodal reasoning over large corpora.
- The main abstraction is a `convert` operator that turns one schema into another, while the optimizer chooses among models, synthesized code, prompt marshaling strategies, and token-reduction tactics.
- The prototype is about 9,200 lines of Python and shows that the same logical program can produce very different runtime, cost, and quality trade-offs depending on the selected physical plan.

## Problem
- Modern AI analytics pipelines require many choices that are expensive to tune by hand: model selection, prompting strategy, batching, inference hardware, and the order in which conventional and semantic operators run.
- The paper argues that these workloads should be handled more like database queries, where users declare intent and the system searches for a good execution plan.
- The target workload class, SAPPs, is defined by three properties: they mix AI and non-AI operators, they are data-intensive, and they can be represented as an execution tree over sets of objects.

## Method
- Users write Python programs in a thin declarative library built around typed `Schema` classes, `Dataset`, `filter`, `convert`, `policy`, and `Execute`.
- `convert` is the key AI operator: it fills missing fields in a target schema from a source schema, usually through LLM inference, but sometimes through built-in conversions or synthesized code.
- Logical optimization currently includes filter reordering and convert reordering, with explicit `depends_on` annotations used to preserve correctness when operators move.
- Physical optimization includes model selection, code synthesis, multi-data prompt marshaling, input token reduction, and output token reduction; the prototype implements the first four and describes the others as future directions or related ideas.
- The optimizer generates logical candidates, runs sentinel physical plans on a small sample, estimates runtime/cost/quality, prunes to the Pareto frontier, and then selects the plan that best fits the user policy.

## Benchmarks / Datasets
| Dataset / Benchmark | Task | Metric | Notes |
|---|---|---|---|
| Legal Discovery | Identify emails about fraudulent investment vehicles while excluding quoted news text | F1 | 1,000 Enron emails; 50 positive fraud examples and 30 fraud-related but non-fraud examples were hand-labeled. |
| Real Estate Search | Find homes that are modern, attractive, near MIT, and in budget | F1 | 100 Boston/Cambridge listings; 23 satisfied all criteria. The workload is multimodal because it uses text plus images. |
| Medical Schema Matching | Filter patient-related tables and harmonize them into a target schema | micro-average F1 | 11 spreadsheet files, 49 tables, and 15 target attributes derived from the proteogenomics pipeline in Li et al. |

## Baselines
| Baseline | Type | Why Important | Notes |
|---|---|---|---|
| GPT-4 naive plan | Single-model baseline | The paper compares optimized plans against a strong direct prompting baseline for each operator | Uses GPT-4 for every convert and filter step. |
| GPT-3.5 naive plan | Cheaper single-model baseline | Shows whether Palimpzest can beat a fast-but-cheap model when the workload is easy | Used as a sentinel plan and as a baseline candidate. |
| Mixtral-8x7B naive plan | Alternative open-model baseline | Checks whether different model families change the trade-off landscape | Used as a sentinel plan and as a baseline candidate. |
| Single-threaded GPT-4 baseline | End-to-end baseline for the parallel section | Establishes the speedup and cost reduction achievable when parallel execution is enabled | Reported separately from the main Pareto-frontier comparisons. |

## Main Results
| Dataset / Benchmark | Metric | Baseline | Ours | Gain / Delta | Notes |
|---|---|---|---|---|---|
| Legal Discovery | Frontier plan quality trade-off | GPT-4 baseline | PLAN 1-style plan | 4.7x faster, 9.1x cheaper, up to 85.7% of GPT-4 F1 | The best non-parallel plan keeps some quality loss but substantially lowers runtime and cost. |
| Real Estate Search | Frontier plan quality trade-off | GPT-4 baseline | PLAN 2-style plan | 3.3x faster, 2.9x cheaper, up to 1.1x better F1 | Reordering text operations before image operations is a major win. |
| Medical Schema Matching | Frontier plan quality trade-off | GPT-4 baseline | PLAN 3-style plan | 2.4x faster, 4.6x cheaper, up to 1.2x better F1 | Mixtral plus modest token reduction beats the GPT-4 baseline on this workload. |
| All workloads | Policy satisfaction | 9 policy cases | 7 satisfied | 7/9 met | The misses were Medical under Policy A and Real Estate under Policy C. |
| Legal Discovery | Parallel execution | GPT-4 single-threaded baseline | Palimpzest | 90.3x speedup, 9.1x lower cost, 83.5% F1 of baseline | 16,712 s and $51.0 versus 185 s and $5.60. |
| Real Estate Search | Parallel execution | GPT-4 single-threaded baseline | Palimpzest | 20.0x speedup, 2.9x lower cost, 107% F1 of baseline | 1,626 s and $5.46 versus 80.9 s and $1.86. |
| Medical Schema Matching | Parallel execution | GPT-4 single-threaded baseline | Palimpzest | 5.6x speedup, 1.5x lower cost, 102% F1 of baseline | 1,195 s and $4.96 versus 215 s and $3.36. |

## Ablations / Analysis
- The paper reports that the optimizer generated 234, 10,140, and 1,950 physical plans for Legal Discovery, Real Estate Search, and Medical Schema Matching, respectively.
- Sample-based statistics were collected from 5% of the workload input for the first two workloads, while Medical Schema Matching used 1 of its 11 inputs for sampling.
- The optimizer currently uses three sentinel plans: GPT-3.5, Mixtral-8x7B, and GPT-4.
- The paper’s implemented logical optimizations are filter reordering and convert reordering; the physical optimizations it evaluates in the prototype are model selection, code synthesis, multi-data prompt marshaling, and input token reduction.
- For the parallel evaluation, each convert and filter operator used 32 workers, and the system did not pipeline operators across stages.

## Implementation Clues
- The prototype is implemented in roughly 9,200 lines of Python and uses an iterator execution model, so each operator processes records one at a time.
- The paper says the system was tested with `gpt-3.5-turbo-0125`, `gpt-4-0125-preview`, `gpt-4-vision-preview`, and `Mixtral-8x7B-Instruct-v0.1`, with Modal used for bulk non-AI execution tasks.
- `depends_on` is an important programming hook because it tells the optimizer which fields a filter or conversion really needs, which in turn enables safe logical reordering.
- The paper explicitly says the current optimizer is still naive: sampling has no rigorous termination criterion, sentinel plans are chosen heuristically, and quality estimation still leans on a champion-model style proxy.
- The source archive is complete and readable, so this note was written from extracted TeX rather than from the PDF fallback.

## Limitations
- The current prototype does not implement every optimization discussed in the paper; several ideas are described as future work, including model cascades, knowledge distillation, and workload-aware execution management beyond the basic prototype.
- Quality estimation remains brittle because it depends on a champion model rather than on broad human labels or guaranteed correctness.
- `depends_on` is still a manual annotation, so safe reordering depends on the user being explicit about operator dependencies.
- The system is positioned as a best-effort optimizer; it does not provide correctness guarantees for semantic outputs.

## Takeaways
- Palimpzest is essentially a query optimizer for AI pipelines: users specify intent once, and the system searches over semantically equivalent execution plans.
- The main win is not any single trick, but the combination of declarative structure, cost/quality estimation, and multiple physical implementations per operator.
- The paper’s experiments show that even a relatively small prototype can produce plans that beat naïve GPT-4 pipelines on runtime and cost, and sometimes on quality too.

## Open Questions
- Can the system infer `depends_on`-style dependencies automatically instead of asking users to annotate them?
- How stable are the cost and quality estimates as model prices, latency, and behavior change over time?
- How much of the gain comes from reordering versus model choice versus token reduction?
- Would the same design remain effective for workloads that are more multimodal or less neatly representable as relational execution trees?

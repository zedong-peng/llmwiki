---
title: "HopRAG: Multi-Hop Reasoning for Logic-Aware Retrieval-Augmented Generation"
domain: research
area: misc
type: paper
status: processed
updated: 2026-04-18
tags: [paper, misc, hoprag, rag, multi-hop-qa]
---
# HopRAG: Multi-Hop Reasoning for Logic-Aware Retrieval-Augmented Generation

## Paper Meta
- Title: HopRAG: Multi-Hop Reasoning for Logic-Aware Retrieval-Augmented Generation
- Authors: Hao Liu, Zhengren Wang, Xi Chen, Zhiyu Li, Feiyu Xiong, Qinhan Yu, Wentao Zhang
- Year: 2025 (inferred from arXiv ID 2502.12442)
- Venue: not reported; ACL preprint manuscript
- Topic: logic-aware RAG for multi-hop QA
- Paper Slug: hoprag-2025
- arXiv: https://arxiv.org/abs/2502.12442
- PDF: 2502.12442.pdf
- Code Repo: local `repo/` directory is empty; no implementation files were available
- Reading Source: TeX

## TL;DR
- HopRAG treats retrieval as a logic-aware graph traversal problem rather than a one-shot similarity search.
- It builds a passage graph whose directed edges are induced by LLM-generated pseudo-queries.
- Retrieval uses a retrieve-reason-prune pipeline to hop from indirectly relevant passages toward supporting facts.
- The paper reports strong gains on MuSiQue, 2WikiMultiHopQA, and HotpotQA, especially against similarity-only retrievers.
- The main tradeoff is better retrieval quality at the cost of more LLM calls during traversal.

## Problem
- Standard sparse and dense retrievers optimize lexical or semantic similarity, not logical relevance.
- In multi-hop QA, many retrieved passages are only indirectly relevant, so the final answer context is incomplete.
- This hurts both precision and recall, especially when the answer requires several supporting passages.
- The paper argues that retrieval itself should reason over passage relationships, not just rank similarity.

## Method
- HopRAG first chunks documents into passages, then generates two pseudo-query sets per passage: in-coming questions whose answers are inside the passage and out-going questions that point to other passages.
- Edge merging matches out-going and in-coming pseudo-queries with a hybrid lexical-plus-dense similarity score, creating directed edges between passages.
- At retrieval time, the system starts from top-k similar edges, then uses LLM reasoning to choose which neighbor to hop to next, while counting repeated visits as an importance signal.
- Final pruning uses a helpfulness score that averages textual similarity and visit importance, keeping the top-k passages for the reader model.
- Implementation details extracted from the source: BGE embeddings at 768 dimensions, PaddleNLP-based keyword extraction, Neo4j for graph storage, GPT-4o-mini for question generation and traversal, and GPT-4o / GPT-3.5-turbo as readers.
- Compared with GraphRAG, HopRAG keeps original chunks as vertices rather than summary nodes; compared with HippoRAG, it combines similarity and logic more explicitly during edge construction and traversal.

## Benchmarks / Datasets
| Dataset / Benchmark | Task | Metric | Notes |
|---|---|---|---|
| MuSiQue | Multi-hop QA | EM, F1; retrieval F1 in ablations | 1,000 validation questions; appendix reports 19,990 docs, 2,800 supporting facts, 13,086 vertices, 81,348 edges |
| 2WikiMultiHopQA | Multi-hop QA | EM, F1; retrieval F1 in ablations | 1,000 validation questions; appendix reports 10,000 docs, 2,388 supporting facts, 23,360 vertices, 167,068 edges |
| HotpotQA | Multi-hop QA | EM, F1; retrieval F1 in ablations | 1,000 validation questions; appendix reports 9,942 docs, 2,458 supporting facts, 40,534 vertices, 171,946 edges |

## Baselines
| Baseline | Type | Why Important | Notes |
|---|---|---|---|
| BM25 | Sparse retriever | Canonical lexical baseline | Used as a conventional IR reference |
| BGE | Dense retriever | Main semantic retrieval baseline | Also used as the starting point for query decomposition and reranking |
| Query decomposition | Dense retriever + decomposition | Tests whether breaking the question into sub-queries helps | GPT-4o-mini decomposes queries into single-hop sub-queries |
| Reranking | Dense retriever + reranker | Tests whether ranking alone can recover logical relevance | Uses bge-reranker-base on top of BGE candidates |
| RAPTOR | Tree-structured RAG | Represents hierarchical summarization-based retrieval | Included as a structured RAG baseline |
| SiReRAG | Tree-structured RAG | Strong structured baseline for similar + related retrieval | Often the strongest baseline in the answer tables |
| GraphRAG | Graph-structured RAG | Important graph baseline with entity-centric indexing | Used with local search in the paper |
| HippoRAG | Graph-structured RAG | Important graph baseline for logical relevance | Strong on 2WikiMultiHopQA in one table |
| HopRAG (non-LLM) | Internal ablation | Measures the value of reasoning during traversal | Replaces LLM reasoning with similarity matching |
| HopRAG (Qwen2.5-1.5B-Instruct) | Internal ablation | Measures lower-cost traversal reasoning | Shows a cheaper reasoning option |

## Main Results
| Setting | Metric | Best baseline | HopRAG | Gain / Delta | Notes |
|---|---|---|---|---|---|
| GPT-3.5-turbo, average over datasets | EM / F1 | SiReRAG 53.93 / 65.88 | 54.00 / 66.76 | +0.07 EM, +0.88 F1 | HopRAG is best overall in this table |
| GPT-4o, average over datasets | EM / F1 | SiReRAG 53.93 / 65.83 | 55.10 / 66.40 | +1.17 EM, +0.57 F1 | HopRAG is best overall in this table |
| GPT-3.5-turbo, retrieval at top 20 | Retrieval F1 | BGE 9.16 | 14.96 | +5.80 F1 | Internal traversal ablation; non-LLM is 9.36 and Qwen2.5 is 13.98 |
| Paper-level claim | Answer metric | Conventional IR approaches | not reported in a single table row | 36.25% higher | Stated in the conclusion relative to reranking-style IR |
| Paper-level claim | Retrieval F1 | Conventional IR approaches | not reported in a single table row | 20.97% higher | Stated in the conclusion |

Additional extracted scores worth keeping:
- GPT-3.5-turbo average answer scores: BM25 22.07 / 28.95, BGE 26.03 / 33.32, query decomposition 31.10 / 40.01, reranking 34.67 / 43.60, HippoRAG 52.97 / 64.03, RAPTOR 49.43 / 60.38, SiReRAG 53.93 / 65.88, HopRAG 54.00 / 66.76.
- GPT-4o average answer scores: BM25 31.77 / 39.85, BGE 36.17 / 45.14, query decomposition 47.46 / 55.91, reranking 48.61 / 56.25, GraphRAG 22.10 / 30.15, RAPTOR 49.40 / 61.21, SiReRAG 53.93 / 65.83, HopRAG 55.10 / 66.40.
- The paper notes two exceptions in the main tables: HotpotQA can favor SiReRAG on F1, and 2WikiMultiHopQA can favor HippoRAG on one metric.

## Ablations / Analysis
- `top_k` sweep: answer quality improves as more candidates are kept, but retrieval F1 drops as redundancy increases; the paper notes that top 12 can already be competitive with HippoRAG or RAPTOR at top 20.
- `n_hop` sweep: average retrieval F1 rises from 8.08 at 1 hop to 14.96 at 4 hops, while the average LLM-call cost rises from 19.92 to 38.53.
- Traversal-model ablation: BM25 22.07 / 28.95 EM/F1 average and 7.93 retrieval F1, BGE 26.03 / 33.32 and 9.16 retrieval F1, HopRAG non-LLM 36.04 / 45.19 and 9.36 retrieval F1, Qwen2.5-1.5B-Instruct 51.53 / 62.08 and 13.98 retrieval F1, GPT-4o-mini 54.00 / 66.76 and 14.96 retrieval F1.
- The case study shows a three-hop path from a first retrieved sentence about Donnie Smith to the final answer "Major League Soccer" via logically linked passages.
- The appendix also reports average edge counts per vertex of 6.22 on MuSiQue, 7.15 on 2Wiki, 4.24 on HotpotQA, and 5.87 overall.

## Implementation Clues
- Entry file: `source/extracted/acl_latex.tex`
- Main sections read: `source/extracted/latex/sections/introduction.tex`, `realted_work.tex`, `method.tex`, `experiment.tex`, `conclusion.tex`, `appendix.tex`
- Core indexing pipeline: query simulation, edge merging, retrieve-reason-prune traversal, helpfulness-based pruning
- Storage and tooling: Neo4j graph database, BGE embeddings, PaddleNLP keyword extraction, GPT-4o-mini traversal/modeling, GPT-4o and GPT-3.5-turbo readers
- No implementation files were present in `repo/`, so repo-vs-paper consistency could not be checked beyond confirming the local checkout is empty

## Limitations
- Evaluation is limited to multi-hop or multi-document QA tasks.
- The paper does not establish strong evidence for broader transfer to other domains.
- Query simulation and edge merging are still heuristic and may need better strategies.
- The authors explicitly note that the passage graph does not follow a power-law degree distribution, so the six-degrees / small-world analogy is only motivational.
- Retrieval quality improves with more hops, but cost and latency rise with the number of LLM calls.

## Takeaways
- HopRAG reframes retrieval as logic-guided traversal over original passages rather than summarization-heavy graph construction.
- Pseudo-queries are the key design move: they turn latent logical relationships into searchable directed edges.
- The strongest gains come from recovering indirectly relevant passages and then pruning them with a combined similarity-plus-importance score.
- The method is practical enough to show competitive results with a smaller context budget, but traversal cost is still a real constraint.

## Open Questions
- Can query simulation and edge merging be learned or simplified without losing logical coverage?
- Can traversal be made cheaper without sacrificing the benefits of multi-hop reasoning?
- How well does HopRAG transfer to non-QA tasks or much larger corpora?
- Would a learned helpfulness scorer outperform the current heuristic pruning rule?

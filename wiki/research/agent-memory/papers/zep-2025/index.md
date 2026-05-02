---
title: "Zep: A Temporal Knowledge Graph Architecture for Agent Memory"
domain: research
area: misc
type: paper
status: processed
updated: 2026-04-19
tags: [paper, misc, agent-memory, knowledge-graph, rag, temporal-memory]
---
# Zep: A Temporal Knowledge Graph Architecture for Agent Memory

## Paper Meta
- Title: Zep: A Temporal Knowledge Graph Architecture for Agent Memory
- Authors: Preston Rasmussen, Pavlo Paliychuk, Travis Beauvais, Jack Ryan, Daniel Chalef
- Venue: arXiv preprint
- Year: not reported in source
- arXiv: https://arxiv.org/abs/2501.13956
- PDF: `zep-2501.13956.pdf`
- Source read: TeX source
- Code repo: not available in this ingest
- Legacy note: [[agent-memory/papers/zep-2025]]

## TL;DR
- Zep is a production memory layer for AI agents built on Graphiti, a temporally aware knowledge graph that stores episodes, entities, and communities as a non-lossy memory substrate.
- The retrieval pipeline is three-stage: search candidate facts/entities/communities, rerank them, then construct a text context for the LLM.
- On the paper's benchmarks, Zep beats MemGPT on DMR and materially improves both accuracy and latency on LongMemEval, but the authors also argue that DMR is too weak to be a realistic memory benchmark.

## Problem
- Standard RAG systems assume static corpora, while agent memory needs to handle continuously changing conversational history plus structured business data.
- LLM context windows are still too small for long multi-session histories, so memory systems need indexing, temporal validity, and retrieval over evolving facts.
- The paper frames agent memory as a production systems problem: accuracy matters, but latency and token cost matter too.

## Method
- Zep stores memory in a temporally aware knowledge graph `G = (N, E, phi)` with three tiers: episode subgraph, semantic entity subgraph, and community subgraph.
- Episodes are the raw inputs and can be messages, text, or JSON; this paper focuses on messages because the experiments are conversation-memory evaluations.
- The graph is bi-temporal: `T` tracks event time and `T'` tracks ingestion time, with fields such as `t_valid`, `t_invalid`, `t'_created`, and `t'_expired`.
- Retrieval is a three-step pipeline: search, rerank, and construct. Search includes cosine similarity, BM25, and breadth-first traversal; reranking includes RRF, MMR, mention-frequency reranking, node-distance reranking, and cross-encoders.
- The constructor formats facts with validity windows plus entity and community summaries into a prompt-ready context string.

## Benchmarks / Datasets
| Dataset / Benchmark | Task | Metric | Notes |
|---|---|---|---|
| DMR (Deep Memory Retrieval) | 500 multi-session conversations with QA memory retrieval | Accuracy | 5 sessions per conversation, up to 12 messages per session |
| LongMemEval_s | Long-term interactive memory on longer, enterprise-like conversations | Accuracy, latency, latency IQR, avg context tokens | Average context length is about 115,000 tokens |

## Baselines
| Baseline | Type | Why Important | Notes |
|---|---|---|---|
| Recursive summarization | Memory baseline | Reported MemGPT comparator in DMR | Prior reported score is 35.3% |
| Conversation summaries | Memory baseline | Common compressed-memory strategy | Stronger than recursive summarization but weaker than full context |
| Full-conversation context | Direct-context baseline | Tests whether retrieval is actually needed | Surpassed MemGPT on DMR in this paper |
| MemGPT | Prior state of the art | The main memory-system comparison target | Reported DMR score is 93.4% |

## Main Results
| Dataset / Benchmark | Metric | Baseline | Ours | Gain / Delta | Notes |
|---|---|---|---|---|---|
| DMR | Accuracy | MemGPT 93.4% | Zep 94.8% | +1.4 pts | Evaluated with gpt-4-turbo |
| DMR | Accuracy | Full-conversation 94.4% | Zep 94.8% | +0.4 pts | Full context already nearly matches Zep |
| DMR | Accuracy | Full-conversation 98.0% | Zep 98.2% | +0.2 pts | Evaluated with gpt-4o-mini |
| LongMemEval_s | Accuracy | Full-context 55.4% | Zep 63.8% | +8.4 pts | gpt-4o-mini; context shrinks from 115k to 1.6k tokens |
| LongMemEval_s | Accuracy | Full-context 60.2% | Zep 71.2% | +11.0 pts | gpt-4o; larger gain with stronger model |
| LongMemEval_s | Latency | Full-context 31.3 s | Zep 3.20 s | about 90% lower | gpt-4o-mini |
| LongMemEval_s | Latency | Full-context 28.9 s | Zep 2.58 s | about 90% lower | gpt-4o |

## Ablations / Analysis
| Question type | Model | Full-context | Zep | Delta |
|---|---|---|---|---|
| single-session-preference | gpt-4o-mini | 30.0% | 53.3% | +77.7% |
| single-session-assistant | gpt-4o-mini | 81.8% | 75.0% | -9.06% |
| temporal-reasoning | gpt-4o-mini | 36.5% | 54.1% | +48.2% |
| multi-session | gpt-4o-mini | 40.6% | 47.4% | +16.7% |
| knowledge-update | gpt-4o-mini | 76.9% | 74.4% | -3.36% |
| single-session-user | gpt-4o-mini | 81.4% | 92.9% | +14.1% |
| single-session-preference | gpt-4o | 20.0% | 56.7% | +184% |
| single-session-assistant | gpt-4o | 94.6% | 80.4% | -17.7% |
| temporal-reasoning | gpt-4o | 45.1% | 62.4% | +38.4% |
| multi-session | gpt-4o | 44.3% | 57.9% | +30.7% |
| knowledge-update | gpt-4o | 78.2% | 83.3% | +6.52% |
| single-session-user | gpt-4o | 81.4% | 92.9% | +14.1% |

- The strongest gains are on temporal, preference, and multi-session questions, which aligns with the claim that Zep is better at multi-hop memory over evolving histories.
- DMR is a weak discriminator because the conversations are short enough to fit current context windows, and simple full-conversation baselines already do very well.
- The only consistent regression is `single-session-assistant`, which the paper treats as a reason for further work rather than a solved problem.

## Implementation Clues
- Embedding and reranking use BGE-m3.
- Graph construction uses `gpt-4o-mini-2024-07-18`.
- Response generation uses `gpt-4o-mini-2024-07-18` and `gpt-4o-2024-11-20`.
- DMR comparability uses `gpt-4-turbo-2024-04-09`.
- The paper says experiments ran between December 2024 and January 2025, from a consumer laptop in Boston against Zep hosted in AWS `us-west-2`.
- The paper says notebooks will be published through the GitHub repository, but no repo content was present in this ingest.

## Limitations
- DMR is small, single-turn, and largely fact-retrieval oriented; it does not test richer memory behavior well.
- Some DMR questions are ambiguously phrased, which weakens the benchmark as a memory evaluation.
- The LongMemEval MemGPT comparison could not be reproduced because the framework did not support direct ingestion of existing message histories.
- The reported latency includes the distributed setup used in the authors' evaluation, so absolute numbers are deployment-specific.

## Takeaways
- Zep is best read as a production memory architecture, not just another RAG wrapper.
- Its main technical contribution is the combination of temporal graph storage, multi-stage retrieval, and prompt construction over a memory graph.
- The benchmark story matters as much as the architecture story: the paper argues that memory evaluation still lags behind the systems people are trying to build.

## Open Questions
- Can the retrieval pipeline be improved with learned extraction or domain-specific ontologies, as the authors suggest?
- How much of Zep's gain comes from graph structure versus model choice and prompt construction?
- What benchmark would better capture enterprise memory across conversation plus structured business data?

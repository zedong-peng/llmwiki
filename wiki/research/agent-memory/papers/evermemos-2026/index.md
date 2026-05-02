---
title: "EverMemOS: A Self-Organizing Memory Operating System for Structured Long-Horizon Reasoning"
domain: research
area: agent-memory
type: paper
status: processed
updated: 2026-04-26
tags: [paper, agent-memory, long-term-memory, memory-operating-system, episodic-memory, semantic-consolidation, reconstructive-recollection, evermemos, everos]
---

# EverMemOS: A Self-Organizing Memory Operating System for Structured Long-Horizon Reasoning

## Paper Meta
- Title: EverMemOS: A Self-Organizing Memory Operating System for Structured Long-Horizon Reasoning
- Authors: Chuanrui Hu, Xingze Gao, Zuyi Zhou, Dannong Xu, Yi Bai, Xintong Li, Hui Zhang, Tong Li, Chong Zhang, Lidong Bing, Yafeng Deng
- Affiliation: EverMind; Shanda Group
- Year: 2026 (arXiv January 2026)
- Venue: arXiv preprint
- Topic: agent-memory
- Paper Slug: evermemos-2026
- arXiv: https://arxiv.org/abs/2601.02163
- PDF: `2601.02163.pdf`
- Code Repo: https://github.com/EverMind-AI/EverOS.git
- Repo Path: `repo/`
- Reading Source: arXiv PDF + TeX source under `source/extracted/`; repo docs under `repo/methods/evermemos/docs/`

## TL;DR
- EverMemOS frames long-term agent memory as an engram-inspired lifecycle rather than a flat store of isolated facts.
- The atomic memory unit is a **MemCell**, containing an episode narrative, atomic facts, time-bounded foresight, and grounding metadata.
- **Semantic Consolidation** clusters MemCells into thematic **MemScenes**, which become the unit for coherent aggregation and user-profile evolution.
- **Reconstructive Recollection** performs MemScene-guided agentic retrieval, using sufficiency checks and query rewriting to compose necessary and sufficient context.
- On GPT-4.1-mini, the paper reports 93.05% LoCoMo overall accuracy and 83.00% LongMemEval overall accuracy, outperforming reported memory-system baselines.

## Problem
- Long-context prompting alone remains expensive and unreliable because important evidence can be lost or underused across long interaction histories.
- Many memory systems improve storage and retrieval but keep memory as flat fragments, so agents can retrieve relevant pieces without integrating them into stable semantic structures.
- The key failure mode is not just missing evidence; it is poor consolidation across evolving user states, temporary constraints, conflicts, and multi-session narratives.
- EverMemOS targets this gap by turning episodic interactions into coherent structures before retrieval.

## Memory Primitives

### MemCell
A MemCell is the atomic unit bridging raw dialogue and higher-level semantics:

| Field | Role |
|---|---|
| Episode | Concise third-person narrative of an event; the semantic anchor |
| Atomic Facts | Discrete, verifiable statements used for precise matching |
| Foresight | Forward-looking inferences, plans, or temporary states with validity intervals |
| Metadata | Timestamps, source pointers, and grounding information |

The important design move is adding time-bounded foresight to ordinary episodic/factual memory, allowing temporary states such as medication, travel plans, or deadlines to affect later answers only while valid.

### MemScene
- MemScenes are thematic clusters of related MemCells.
- They serve as stable scene-level structures for aggregation, conflict handling, and retrieval.
- Scene summaries update compact user profiles from grouped evidence rather than individual turns.

## Method

### Phase I: Episodic Trace Formation
- A Semantic Boundary Detector segments dialogue streams using a sliding window and detects topic shifts.
- Narrative Synthesis rewrites each raw episode history into a concise third-person episode with resolved coreferences.
- Structural Derivation extracts atomic facts and time-bounded foresight from the episode.
- The result is a grounded MemCell that can be indexed and consolidated.

### Phase II: Semantic Consolidation
- Each new MemCell is embedded and compared against MemScene centroids.
- If similarity exceeds threshold `tau`, the MemCell is assimilated into an existing scene; otherwise a new MemScene is created.
- Scene summaries and user profiles are updated online.
- The profile distinguishes explicit facts, time-varying measurements, implicit traits, and conflicting evidence.

### Phase III: Reconstructive Recollection
- Query retrieval first fuses dense retrieval and BM25 over MemCell atomic facts via Reciprocal Rank Fusion.
- MemScenes are scored by the strongest relevant MemCell and a small number of top scenes are selected.
- Episodes inside selected scenes are reranked; valid foresight is filtered by the current time.
- An LLM sufficiency checker decides whether the retrieved context can answer the query.
- If context is insufficient, the system rewrites the query into complementary search variants and retrieves again.

## Architecture / Repo Notes
- The open-source EverOS repository now groups methods, benchmarks, and use cases under one repo.
- The EverMemOS implementation is under `methods/evermemos/`.
- Repo docs describe six layers: Agentic, Memory, Retrieval, Business, Infrastructure, and Core Framework.
- The implementation stack includes FastAPI, Python 3.10+, MongoDB, Elasticsearch/BM25, Milvus/vector search, Redis, LLM APIs, embedding models, and rerankers.
- The repo distinguishes lightweight retrieval mode (BM25/vector/RRF without extra LLM calls) from agentic multi-round recall.

## Evaluation

### Benchmarks
| Benchmark | Scope | Reported size |
|---|---|---|
| LoCoMo | Long-term multi-session dialogue QA: single-hop, multi-hop, temporal, open-domain | 1,540 questions over 10 ultra-long dialogues |
| LongMemEval | Long-horizon memory QA with user/asst/pref, multi-session, knowledge update, temporal reasoning | 500 questions |
| PersonaMem-v2 | User profile and personalization | 2,447 questions across 9 scenarios in appendix |

### Baselines
- Zep
- Mem0
- MemOS
- MemoryOS
- MemU

The paper standardizes the final answer-generation backbone for LoCoMo and reports LongMemEval baselines from the official MemOS leaderboard.

### Main Results
| Benchmark | EverMemOS result | Strongest baseline | Key gain |
|---|---:|---:|---|
| LoCoMo, GPT-4.1-mini | 93.05 overall | 85.22 Zep | +9.2% relative |
| LoCoMo, GPT-4o-mini | 86.76 overall | 81.06 Zep | +7.0% relative |
| LongMemEval | 83.00 overall | 77.80 MemOS | +6.7% relative |
| PersonaMem-v2 | 53.25 overall | 50.72 MemOS | +2.53 points |

### LoCoMo Detail
| Backbone | Method | Avg. Tokens | Single Hop | Multi Hop | Temporal | Open Domain | Overall |
|---|---|---:|---:|---:|---:|---:|---:|
| GPT-4.1-mini | Zep | 1.4k | 90.84 | 81.91 | 77.26 | 75.00 | 85.22 |
| GPT-4.1-mini | EverMemOS | 2.3k | 96.67 | 91.84 | 89.72 | 76.04 | 93.05 |
| GPT-4o-mini | Zep | 1.4k | 88.11 | 71.99 | 74.45 | 66.67 | 81.06 |
| GPT-4o-mini | EverMemOS | 2.5k | 91.08 | 86.17 | 81.93 | 66.67 | 86.76 |

### LongMemEval Detail
| Method | Token | SS-User | SS-Asst | SS-Pref | Multi-S | Know. Upd | Temp. Reas | Overall |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| MemOS | 1.4k | 95.71 | 67.86 | 96.67 | 70.67 | 74.26 | 77.44 | 77.80 |
| EverMemOS | 2.8k | 97.14 | 85.71 | 93.33 | 73.68 | 89.74 | 77.44 | 83.00 |

## Ablations
- Removing MemScenes lowers LoCoMo overall from 93.05 to 89.16 and LongMemEval overall from 83.00 to 79.60.
- Removing MemCells lowers LoCoMo to 81.82 and LongMemEval to 71.20.
- Removing external memory collapses performance to near zero on these long-horizon tasks.
- The biggest reported gains from structure are LoCoMo multi-hop, LoCoMo temporal, and LongMemEval knowledge update.

## Implementation Clues
- Default retrieval uses top-10 MemScenes and 10 Episodes for inference.
- Dense retrieval uses Qwen3-Embedding-4B; reranking uses Qwen3-Reranker-4B.
- LoCoMo clustering threshold `tau` is 0.70 with max time gap 7 days.
- LongMemEval clustering threshold `tau` is 0.50 with max time gap 30 days.
- On LoCoMo, the sufficiency checker triggers second-round query rewriting for 31.0% of questions.
- Phase I memory construction is LLM-token intensive; Phase II clustering/embedding updates add no LLM tokens in the reported Episodes-only LoCoMo setting.

## Takeaways
- EverMemOS is best understood as a consolidation-first memory OS: retrieval is downstream of structured memory formation, not the whole system.
- MemCell and MemScene provide a useful split between high-precision local facts and broader thematic context.
- Time-bounded foresight is a practical mechanism for temporary constraints, but current benchmarks only partially test it.
- The system trades higher memory-construction and retrieval cost for stronger multi-hop, temporal, and knowledge-update reasoning.

## Limitations
- Experiments are text-only; multimodal and embodied settings are left for future work.
- LLM-mediated extraction, sufficiency checking, and query rewriting introduce cost and latency.
- Benchmark evidence annotations can be redundant or non-unique, making recall measurements imperfect.
- LongMemEval comparisons rely on reported leaderboard baselines rather than fully rerun baseline APIs due to extreme input length.

## Open Questions
- How robust is MemScene consolidation when many user states conflict or decay at different rates?
- Can time-bounded foresight be evaluated systematically beyond qualitative examples?
- How much of the gain comes from better memory construction versus agentic retrieval and reranking?
- What governance model should apply when profiles and foresight contain sensitive inferred user states?

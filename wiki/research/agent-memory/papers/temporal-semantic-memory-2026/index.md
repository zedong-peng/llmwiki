---
title: "Beyond Dialogue Time: Temporal Semantic Memory for Personalized LLM Agents"
domain: research
area: misc
type: paper
status: processed
updated: 2026-04-19
tags: [paper, misc, temporal-memory, agent-memory, processed]
---
# Beyond Dialogue Time: Temporal Semantic Memory for Personalized LLM Agents

## Paper Meta
- Title: Beyond Dialogue Time: Temporal Semantic Memory for Personalized LLM Agents
- Authors: Miao Su, Yucan Guo, Zhongni Hou, Long Bai, Zixuan Li, Yufei Zhang, Guojun Yin, Wei Lin, Xiaolong Jin, Jiafeng Guo, Xueqi Cheng
- Year: 2026
- Venue: not reported in the source
- arXiv: https://arxiv.org/abs/2601.07468
- PDF: `2601.07468.pdf`
- Paper Slug: `temporal-semantic-memory-2026`
- Reading Source: TeX/source only
- Repo: not reported / not available locally

## TL;DR
- Temporal Semantic Memory (TSM) fixes two failures in agent memory: dialogue-time mismatch and fragmentation of point-wise memories.
- It builds a semantic timeline over a temporal knowledge graph, consolidates monthly durative summaries, and retrieves with query-time constraints.
- On `LongMemEval_S`, TSM reaches 74.80% accuracy on both GPT-4o-mini and Qwen3-30B-A3B-Instruct-2507; on `LoCoMo`, it is the best memory-based method, while full text still wins on Qwen3 because the dialogues are short enough to fit.

## Problem
- Existing memory systems often index by dialogue time, not event time. That breaks cases where the user talks about past trips, future plans, or ongoing states that do not align with the current chat turn.
- Existing systems also store memories as isolated point facts. That fragments continuous experiences and makes it hard to recover persistent states, durations, and evolving user preferences.

## Method
### 1) Duration-aware memory construction
- TSM builds an episodic temporal knowledge graph with facts of the form `(e_s, r, e_o, t)` and compact entity summaries.
- It slices the graph into monthly intervals by default, clusters entities inside each slice with a Gaussian Mixture Model, and summarizes each cluster into topic and persona memories.
- The resulting durative memories are time-anchored summaries, not raw facts; they capture stable themes and user traits across a period.

### 2) Semantic-time guided retrieval
- For each query, TSM parses a semantic time constraint with spaCy and treats that as the retrieval target, not just the dialogue timestamp.
- It retrieves over topics, personas, and raw dialogue chunks with dense similarity, then filters or reranks summaries so time-aligned memories come first.
- It also queries the temporal knowledge graph for facts valid in the query interval and uses those linked turns as supporting evidence.

### 3) Hierarchical update
- Online updates are lightweight: add new entities, merge mentions into existing nodes, and handle fact changes through duplicate, add, invalidate, and update operations.
- Summaries are refreshed periodically, roughly monthly or after a threshold of new turns, so the expensive consolidation step does not block online use.

## Benchmarks / Datasets
| Dataset | Scope | Size / Shape | Metric | Notes |
|---|---|---:|---|---|
| `LongMemEval_S` | long-term memory and temporal reasoning | 500 questions, about 115k tokens of history, 30-40 sessions | Accuracy | Includes temporal, multi-session, knowledge-update, single-user, single-assistant, single-preference |
| `LoCoMo` | long-range conversational memory | 1,986 questions, about 9k tokens average, about 300 turns | Accuracy | Includes temporal, multi-hop, open-domain, single-hop |

## Baselines
| Baseline | Type | Why it matters |
|---|---|---|
| Full Text | upper bound when context fits | Shows how far retrieval-based memory is from simply giving the model everything |
| Naive RAG | dense retrieval | Strong semantic retrieval baseline without temporal structure |
| LangMem | long-term memory module | Representative LangChain-style memory layer |
| A-MEM | note-based memory graph | Strong structured memory baseline with dynamic note linking |
| MemoryOS | hierarchical memory | Tests an OS-inspired layered memory design |
| Mem0 / Mem0$^g$ | memory graph / graph variant | Important graph-based conversational memory baseline |
| Zep | temporal KG memory | Closest conceptual baseline on temporal graph memory |

## Main Results
### LongMemEval_S
| Backbone | Method | Overall | Temporal | Multi-Session | Knowledge-Update |
|---|---|---:|---:|---:|---:|
| GPT-4o-mini | A-MEM | 62.60 | 47.36 | 48.87 | 64.11 |
| GPT-4o-mini | TSM | 74.80 | 69.92 | 69.17 | 80.77 |
| Qwen3-30B-A3B-Instruct-2507 | A-MEM | 65.20 | 51.88 | 51.12 | 76.93 |
| Qwen3-30B-A3B-Instruct-2507 | TSM | 74.80 | 63.91 | 63.91 | 82.05 |

TSM is the top overall method on `LongMemEval_S` for both backbones. The biggest gains are on temporal and multi-session questions, which match the paper's claim that semantic time and durative summaries matter most.

### LoCoMo
| Backbone | Method | Overall | Temporal | Multi-Hop | Open-Domain | Single-Hop |
|---|---|---:|---:|---:|---:|---:|
| GPT-4o-mini | Mem0$^g$ | 68.44 | 58.13 | 47.19 | 75.71 | 65.71 |
| GPT-4o-mini | TSM | 76.69 | 71.03 | 66.67 | 58.33 | 84.30 |
| Qwen3-30B-A3B-Instruct-2507 | Full Text | 74.87 | 76.92 | 82.86 | 87.50 | 50.00 |
| Qwen3-30B-A3B-Instruct-2507 | TSM | 71.23 | 65.42 | 64.54 | 56.25 | 77.41 |

TSM is the best memory-based method on `LoCoMo`. The paper explicitly notes that full text still wins on Qwen3 because those conversations are short enough that feeding the entire history can outperform retrieval.

## Ablations / Analysis
- Removing temporal reranking and filtering drops `LongMemEval_S` overall accuracy from 74.80% to 72.80%, with the largest hit on temporal questions, from 69.92% to 63.91%.
- Removing durative summaries drops overall accuracy to 73.40% and hurts single-session preference the most, from 40.00% to 23.33%.
- The paper's interpretation is that temporal modeling is the more consistently important component, while summaries help most on preference-centric and long-horizon tasks.

## Implementation Clues
- Backbone models used throughout: GPT-4o-mini and Qwen3-30B-A3B-Instruct-2507.
- Generation settings: temperature 0.0, max tokens 8192.
- Default embedding model: `text-embedding-3-small`; the appendix also compares `text-embedding-v4`.
- Retrieval top-k: 25.
- Durative memory granularity: one month by default.
- Update cadence: monthly or when accumulated turns exceed a preset threshold.
- LoCoMo has no explicit query timestamps, so the session start time is used as the reference time.
- Hardware: 8 NVIDIA A100 GPUs with 80 GB each, plus 256 GB system memory.

## Limitations
- The temporal granularity is fixed at monthly intervals, which may not fit every domain.
- The method is framed around personalization. The paper leaves procedural memory and shared multi-agent memory for future work.

## Takeaways
- The core contribution is not just storing more memory, but aligning memory with the time the user actually meant.
- Durative summaries help when a question depends on a stable state or evolving pattern instead of a single fact.
- The strongest improvements appear where temporal reasoning and multi-session continuity are required.

## Open Questions
- How should the system choose temporal granularity adaptively instead of defaulting to monthly slices?
- Can the same semantic-time machinery extend to procedural memory or shared memory without losing efficiency?
- Inference from the reported results: when the full dialogue fits into context, retrieval-heavy memory may be less useful than direct full-text prompting on some benchmarks.

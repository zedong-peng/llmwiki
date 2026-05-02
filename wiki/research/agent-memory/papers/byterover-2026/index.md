---
title: ByteRover: Agent-Native Memory Through LLM-Curated Hierarchical Context
domain: research
area: misc
type: paper
status: processed
updated: 2026-04-18
tags: [paper, misc, memory, retrieval, agent-native, byterover]
---

# ByteRover: Agent-Native Memory Through LLM-Curated Hierarchical Context

## Paper Meta
- Title: ByteRover: Agent-Native Memory Through LLM-Curated Hierarchical Context
- Authors: Andy Nguyen, Danh Doan, Hoang Pham, Bao Ha, Dat Pham, Linh Nguyen, Hieu Nguyen, Thien Nguyen, Cuong Do, Phat Nguyen, Toan Nguyen
- Year: 2026
- Venue: not reported in source
- Topic: misc
- Paper Slug: byterover-2026
- ArXiv: https://arxiv.org/abs/2604.01599
- PDF: 2604.01599.pdf
- Source Read: yes, from `source/extracted/main.tex`
- Repo Read: no local repo content was available in `repo/`
- PDF Fallback: not used
- Legacy Note: [[agent-memory/papers/byterover-2026]]

## TL;DR
- ByteRover inverts the usual memory-augmented generation setup: the same LLM that reasons about a task also curates, structures, and retrieves memory.
- The memory substrate is a hierarchical `Context Tree` of markdown entries, plus a local MiniSearch index and cache, with no external vector database or graph database.
- The paper reports 96.1% overall accuracy on LoCoMo and 92.8% overall accuracy on LongMemEval-S.
- Its main empirical strengths are multi-hop and temporal retrieval; its main tradeoff is that write-path curation is slower than mechanical chunk-and-embed pipelines.

## Problem
- Existing MAG systems generally treat memory as an external service.
- That separation creates semantic drift: the agent intends one thing, while the memory pipeline chunking, embedding, or graph extraction captures something slightly different.
- Shared memory services also lose coordination context, because later agents can see stored facts but not the reasoning or provenance behind them.
- Crash recovery is fragile when state lives in a separate service rather than in inspectable files.

## Method

### Architecture
| Layer | What it does | Source details |
|---|---|---|
| Agent Layer | Runs the LLM reasoning loop and exposes memory tools | `curate`, `search_knowledge`, and other tools are first-class |
| Execution Layer | Serializes curate/query operations | Sequential task queue, sandboxed curation, per-operation feedback |
| Knowledge Layer | Stores the actual memory | Hierarchical markdown `Context Tree`, MiniSearch full-text index, cache |

### Core data model
- The `Context Tree` is organized as `Domain > Topic > Subtopic > Entry`.
- Each entry is a standalone markdown file with relation annotations, provenance, narrative structure, snippets, and lifecycle metadata.
- Explicit relations are stored as author-stated links, not inferred similarities.
- A bidirectional reference index supports forward links and backlinks.

### Adaptive Knowledge Lifecycle
- Each entry has an importance score in `[0, 100]`.
- Access events add `+3`; update events add `+5`; daily decay is `0.995^delta_t`.
- Maturity tiers are `draft`, `validated`, and `core`, with thresholds at 65/85 for promotion and 35/60 for demotion.
- Recency is modeled as `exp(-delta_t / 30)`.
- Retrieval combines BM25 relevance with importance and recency signals.

### Curate operations
| Operation | Behavior |
|---|---|
| ADD | Create a new entry and auto-generate `context.md` at each hierarchy level |
| UPDATE | Replace an existing entry |
| UPSERT | Add if missing, update if present |
| MERGE | Combine two entries and delete the source |
| DELETE | Remove a single entry or a subtree |

### Retrieval
- Retrieval is a 5-tier progressive pipeline.
- Tier 0 returns an exact cache hit.
- Tier 1 uses fuzzy cache matching.
- Tier 2 serves high-confidence MiniSearch results directly.
- Tier 3 makes a single optimized LLM call with pre-fetched context.
- Tier 4 escalates to the full agentic loop.
- The system explicitly rejects out-of-domain queries when matches are weak and significant query terms remain unmatched.

## Benchmarks / Datasets
| Benchmark | Scope | Size / shape | Notes |
|---|---|---|---|
| LoCoMo | Long-term conversational memory | 1,982 questions across 35 sessions; average length about 20K tokens | 4 categories: single-hop, multi-hop, open-domain, temporal |
| LongMemEval-S | Long-horizon memory retention | 500 questions; average context length above 100K tokens across about 48 sessions per question | 6 categories: KU, SSU, SSA, SSP, TR, MS |

## Baselines
| Benchmark | Baselines reported | Notes |
|---|---|---|
| LoCoMo | Mem0, Zep, Hindsight, HonCho, Memobase, OpenAI Memory | All evaluated under the same judge setup in the paper's harness |
| LongMemEval-S | Chronos, SmartSearch, Memora, TiMem, Zep, Full-context, plus Hindsight and HonCho in the authors' own runs | Daggered results use different backbones and judges |

## Main Results
| Benchmark | Ours | Best baseline in source | Key takeaway |
|---|---|---|---|
| LoCoMo | 96.1 overall | 89.9 overall (HonCho) | +6.2 points overall; strongest on temporal (97.8) and multi-hop (93.3) |
| LongMemEval-S | 92.8 overall | 92.6 overall (Chronos in table) | The text says this beats Chronos-Low (92.6) but remains below Chronos-High (95.6) |

### LoCoMo detail
| Method | Single-Hop | Multi-Hop | Open-Domain | Temporal | Overall |
|---|---:|---:|---:|---:|---:|
| HonCho | 93.2 | 84.0 | 77.1 | 88.2 | 89.9 |
| Hindsight | 86.2 | 70.8 | 95.1 | 83.8 | 89.6 |
| Memobase | 70.9 | 46.9 | 77.2 | 85.1 | 75.8 |
| Zep | 74.1 | 66.0 | 67.7 | 79.8 | 75.1 |
| Mem0 | 67.1 | 51.2 | 72.9 | 55.5 | 66.9 |
| OpenAI Memory | 63.8 | 42.9 | 62.3 | 21.7 | 52.9 |
| ByteRover | 97.5 | 93.3 | 85.9 | 97.8 | 96.1 |

### LongMemEval-S detail
| Method | KU | SSU | SSA | SSP | TR | MS | Overall |
|---|---:|---:|---:|---:|---:|---:|---:|
| Chronos | 96.2 | 94.3 | 100.0 | 80.0 | 90.2 | 91.7 | 92.6 |
| Hindsight | 94.9 | 97.1 | 96.4 | 80.0 | 91.0 | 87.2 | 91.4 |
| HonCho | 94.9 | 94.3 | 96.4 | 90.0 | 88.7 | 85.0 | 90.4 |
| SmartSearch | 93.6 | 100.0 | 85.7 | 96.7 | 82.7 | 84.2 | 88.4 |
| Memora | 97.4 | 98.6 | 78.6 | 83.3 | 89.5 | 78.2 | 87.4 |
| TiMem | 87.7 | 96.3 | 85.7 | 55.3 | 73.4 | 72.8 | 79.0 |
| Zep | 83.3 | 92.9 | 80.4 | 56.7 | 62.4 | 57.9 | 71.2 |
| Full-context | 78.2 | 81.4 | 94.6 | 20.0 | 45.1 | 44.3 | 60.2 |
| ByteRover | 98.7 | 98.6 | 98.2 | 96.7 | 91.7 | 84.2 | 92.8 |

## Ablations / Analysis
- Removing tiered retrieval drops LongMemEval-S overall from 92.8 to 63.4, a 29.4 point loss.
- The biggest category damage from removing tiered retrieval is multi-session, which falls from 84.2 to 47.4.
- Removing OOD detection lowers overall score only slightly, from 92.8 to 92.4, with the main hit on temporal reasoning.
- Removing the relation graph gives the same overall score as removing OOD detection on LongMemEval-S, suggesting overlapping failure modes for that benchmark.
- AKL, the curation feedback loop, and escalated compression were not isolated by query-time ablation because the curated tree stayed fixed.

## Implementation Clues
- Storage is local filesystem only; the paper explicitly says there is no vector database, graph database, or embedding service.
- The search stack is MiniSearch v7 with fields weighted as title 5x, path 1.5x, content 1x.
- Key retrieval thresholds are `0.93` for high confidence, `0.85` for minimum score, and `0.08` for the top-vs-second gap.
- OOD detection uses a minimum relevance score of `0.6` and an unmatched-term threshold of `0.85`.
- Curation limits are 5 files per operation and 40,000 characters per file; code files are truncated to 2,000 lines.
- The system uses Gemini 3 Flash for curate/query and judging, with Gemini 3.1 Pro as the justifier.
- The runtime includes a per-project daemon, a sequential task queue, a sandboxed curation path, and atomic temp-then-rename writes.
- The paper also exposes `brv-query` and `brv-curate` as MCP tools.

## Limitations
- Write-path curation is expensive because the LLM must reason on each curation event.
- Novel queries can still be slower than vector search when they miss the cache and index.
- Quality depends on backbone model capability, so weaker models can degrade curation.
- The in-memory MiniSearch index and sequential queue may become bottlenecks at larger scales.
- The paper estimates the file-based design for knowledge bases up to about 10K entries before sharding may be needed.

## Takeaways
- ByteRover is best understood as an auditable local-memory system, not just a retrieval stack.
- Its main idea is alignment: the same agent that reasons also decides how knowledge is stored and linked.
- The strongest empirical gains are on multi-hop and temporal memory, which fit the explicit relation graph and timestamped entries.
- The design is attractive when you want inspectable markdown memory and zero external infrastructure.

## Open Questions
- How much better would the relation graph perform on benchmarks with stronger multi-hop dependence?
- How far can the local-file design scale before the sequential queue and in-memory index become the dominant bottlenecks?
- How sensitive is the system to weaker backbone models that produce noisier structured outputs?
- Would the write-path costs still be acceptable in high-frequency agent workloads?

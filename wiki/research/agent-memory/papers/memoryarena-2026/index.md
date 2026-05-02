---
title: "Benchmarking Agent Memory in Interdependent Multi-Session Agentic Tasks"
domain: research
area: misc
type: paper
status: processed
updated: 2026-04-18
tags: [paper, misc, memory, agents, benchmark, multi-session]
---

# Benchmarking Agent Memory in Interdependent Multi-Session Agentic Tasks

## Paper Meta
- Benchmark name: MemoryArena (`\ours` in the source)
- arXiv: [2602.16313](https://arxiv.org/abs/2602.16313)
- Reading source: TeX/source from `source/extracted/`
- Source read: yes
- Repo read: no local repo present in `repo/`
- PDF fallback used: no
- Ingest state: processed
- Source naming note: the draft TeX uses `MemoryArena`, `MemArena`, and `MemAct Arena` inconsistently, but the canonical benchmark name in the macro is `MemoryArena`

## TL;DR
MemoryArena benchmarks whether an agent can carry useful state across multiple sessions, not just recall facts from a long prompt. It turns memory into a memory-agent-environment loop and tests four interdependent settings: bundled shopping, group travel planning, progressive web search, and formal reasoning. The key finding is that strong long-context and memory systems still fail badly once later subtasks depend on earlier decisions.

## Problem
- Existing memory benchmarks mostly test recall from static long-context dialogue, so they measure memorization but not whether memory actually helps an agent choose better actions in a changing environment.
- Existing agent benchmarks mostly test single-session execution, so the history often behaves like short working memory rather than persistent long-term memory.
- The paper argues that realistic memory evaluation must cover multi-session tasks where early decisions create latent constraints that must be reused later.

## Method
- The benchmark is framed as a Memory-Agent-Environment loop: an agent acts, the environment responds, memory is updated, and later sessions retrieve that memory to guide the next action.
- Four task families are included: bundled web shopping, preference-constrained group travel, progressive information search, and sequential formal reasoning over math and physics.
- Each task family is manually curated so later subtasks are causally dependent on earlier ones; the paper filters out cases that can be solved without cross-session dependence.
- Evaluation uses Task Success Rate (SR) for full completion and Task Progress Score (PS) for partial progress. Group travel also reports soft PS (sPS) because SR and PS are near zero.

## Benchmarks / Datasets
| Environment | Construction | Tasks | Sessions / subtasks | Avg trace length | Notes |
|---|---|---:|---:|---:|---|
| Bundled Web Shopping | Extended from WebShop with compatibility chains and distractors | 150 | 6 sessions per task | 41.5k tokens | Products are constrained by compatibility plus a unique selection rule |
| Group Travel Planning | Extended from TravelPlanner with incremental travelers and JOIN / RELATION constraints | 270 | 5 to 9 sessions per task | 40.6k tokens | Hardest setting; dependency chains go up to depth 4 |
| Progressive Web Search | Filtered and decomposed from BrowseComp-Plus into dependent subqueries | 256 | 2 to 16 sessions per task | 122.4k tokens | Each later query adds a new constraint that depends on earlier search state |
| Math Formal Reasoning | Expert-curated derivations from research papers | 40 | 2 to 16 sessions per task | 18.1k tokens | Covers pure math, optimization, and learning theory |
| Physics Formal Reasoning | Expert-curated derivations from research papers | 20 | 2 to 12 sessions per task | 14.1k tokens | Covers high-energy theory, phenomenology, lattice, and condensed matter |

## Baselines
| Family | Methods | Memory form | What the paper varies |
|---|---|---|---|
| Long-context agents | GPT-5.1-mini, GPT-4.1-mini, Gemini-3-Flash, Claude-Sonnet-4.5 | 0D verbatim history | Appends the full interaction trace as prompt context |
| External memory systems | Letta, Mem0, Mem0-g, Reasoning Bank | 1D or 2D memory | Tests curated or learned memory with abstraction, consolidation, or graph structure |
| RAG systems | BM25, Text-Embedding-3-Small, MemoRAG, GraphRAG | 0D / 1D / 2D retrieval | Retrieves prior information from an indexed store instead of replaying all history |

## Main Results
| Environment | Best reported result | What it means |
|---|---|---|
| Bundled Web Shopping | SR 0.12, PS 0.79, both reported by Claude-Sonnet-4.5 | Long-context can do some bundle reasoning, but full task success stays low |
| Group Travel Planning | SR 0.00 and PS 0.00 for all methods; best sPS 0.62 by Gemini-3-Flash | This is the hardest environment in the benchmark |
| Progressive Web Search | Best SR 0.28 by BM25; best PS 0.32 by Text-Embedding-3-Small | Retrieval helps when search traces become very long |
| Math Formal Reasoning | Best SR 0.32 by Text-Embedding-3-Small; best PS 0.39 tied by BM25, MemoRAG, and GraphRAG | Memory and retrieval help more than raw long-context in this setting |
| Physics Formal Reasoning | Best SR 0.60 and best PS 0.70 by Text-Embedding-3-Small | This is the strongest single-environment result in the paper |

| Family / observation | Source-backed takeaway |
|---|---|
| All methods | Full success is rare even when partial progress is common |
| Long-context agents | Stronger than many memory systems in some settings, but still fail on cross-session dependency tracking |
| External memory systems | Not universally beneficial; the paper calls out representation mismatch and training mismatch |
| RAG systems | More helpful in progressive search and formal reasoning than in shopping or travel |

## Ablations / Analysis
- Success falls as subtask depth increases in every environment; no method keeps a flat SR-at-depth curve across tasks.
- Progressive web search is the clearest long-context failure case because traces exceed 122.4k tokens, which pushes attention and context handling beyond practical limits.
- External memory and RAG help most when the trace becomes too long or reasoning is domain-specific, but they do not reliably beat simply keeping the full history in context.
- The paper explains the gap using two mismatches: long-context agents reason over a coherent trace, while memory systems may return compressed or reordered fragments; memory systems also are not jointly trained with the task agent.
- The authors also interpret the benchmark as a POMDP-style testbed, where memory approximates belief-state tracking across sessions.

## Implementation Clues
- The extracted source is complete enough to reconstruct the benchmark design, metrics, and results without opening the PDF.
- The paper reports results with GPT-5.1-mini as the task agent for the memory and RAG families.
- The paper uses a simple memory taxonomy: 0D for raw context, 1D for flat learned or curated memory, and 2D for structured memory.
- Latency is reported as another diagnostic. Average per-task latency is lowest for long-context agents and highest for external memory systems.

| Method | Avg latency, sec. | Source note |
|---|---:|---|
| GPT-5.1-mini | 74.2 | Long-context family |
| GPT-4.1-mini | 33.6 | Long-context family |
| Claude-Sonnet-4.5 | 81.8 | Long-context family |
| Gemini-3-Flash | 52.2 | Long-context family |
| Letta | 132.8 | External memory |
| Mem0 | 114.8 | External memory |
| Mem0-g | 125.2 | External memory |
| Reasoning Bank | 115.4 | External memory |
| BM25 | 107.4 | RAG |
| Text-Embedding-3-Small | 107.0 | RAG |
| MemoRAG | 102.8 | RAG |
| GraphRAG | 90.2 | RAG |

## Limitations
- Group Travel Planning is extremely hard, with SR and PS at zero for all methods, so the benchmark gives limited gradient there.
- The source does not include a standalone limitations section, so the paper’s own caveats are inferred from the experiments and discussion.
- The source does not show any local official repo, so I could not verify code entry points, training scripts, or implementation defaults beyond the TeX source.
- Results are reported primarily on one task-agent backbone for the memory and RAG families, so broader backbone transfer is not established in the source.

## Takeaways
- Memory should be evaluated as a functional part of agent behavior, not as a separate recall benchmark.
- Multi-session causal dependence exposes failures that long-context QA benchmarks miss.
- Current memory systems and RAG pipelines still do not solve state tracking across sessions.
- Benchmarking only on single-session tasks overstates how well memory supports actual agentic work.

## Open Questions
- Which memory representation best preserves task-relevant state without adding noise or latency?
- How should task agents be trained to query and consume memory outputs more reliably?
- Can memory systems be designed to support belief-state tracking instead of generic recall?
- What benchmark variants would isolate retrieval failure, reasoning failure, and planning failure more cleanly?

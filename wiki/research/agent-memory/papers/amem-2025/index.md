---
title: "A-MEM: Agentic Memory System"
domain: research
area: misc
type: paper
status: processed
updated: 2026-04-18
tags: [paper, misc, memory, zettelkasten, locomo, neurips]
---
# A-MEM: Agentic Memory System

## Paper Meta
- Title: A-MEM: Agentic Memory System
- Authors: Wujiang Xu, Zujie Liang, Kai Mei, Hang Gao, Juntao Tan, Yongfeng Zhang
- Year: 2025
- Venue: NeurIPS 2025
- Topic: misc
- Paper Slug: amem-2025
- arXiv: https://arxiv.org/abs/2502.12110
- PDF: 2502.12110.pdf
- Code Repo: https://github.com/WujiangXu/A-mem
- Reading Source: TeX / source, then repo
- Legacy Note: [[agent-memory/papers/amem-2025]]

## TL;DR
- A-MEM is a Zettelkasten-inspired memory system for LLM agents that turns each interaction into a structured note, links it to semantically related notes, and can evolve older notes when new evidence arrives.
- The paper argues that static memory schemas and fixed write/retrieve workflows are too rigid for long-horizon agent settings.
- On LoCoMo and DialSim, A-MEM reports strong category-level gains over LoCoMo, ReadAgent, MemoryBank, and MemGPT, while using far fewer tokens per memory operation.

## Problem
- Existing agent memory systems usually require predefined storage structures, fixed write points, and preset retrieval timing.
- Graph-backed memory improves organization, but preset schemas and relationships still limit adaptability when the agent encounters new tasks or new kinds of evidence.
- The paper frames the core challenge as building a flexible, universal memory system that supports long-term interaction without hard-coded memory workflows.

## Method
- Each new memory is converted into an atomic note with original content, timestamp, LLM-generated keywords, tags, and a contextual summary.
- The note is embedded with a text encoder, and the new embedding is used to retrieve the top-k nearest historical memories as candidates for linking.
- The LLM then decides whether to create links and whether any nearby memories should be evolved, which can update context, tags, and relationships.
- Retrieval reuses the same embedding space; when a related note is returned, other notes in the same linked neighborhood can also be surfaced.
- The repository code implements this as `MemoryNote` plus `AgenticMemorySystem`, with a `SimpleEmbeddingRetriever` built on `all-MiniLM-L6-v2`.
- The robust repo variant replaces JSON-schema-dependent calls with plain-text prompts and parsing, and adds retry logic plus graceful degradation when evolution fails.

## Benchmarks / Datasets
| Dataset / Benchmark | Task | Metric | Notes |
|---|---|---|---|
| LoCoMo | Long-term conversational QA across multiple sessions | F1, BLEU-1, token length | Main evaluation set in the paper; 7,512 QA pairs across single-hop, multi-hop, temporal, open-domain, and adversarial questions. |
| DialSim | Long-term dialogue QA from TV-show conversations | F1, BLEU-1, ROUGE-L, ROUGE-2, METEOR, SBERT similarity | Paper reports this as an additional evaluation set; the paper states 1,300 sessions, about 350,000 tokens, and more than 1,000 questions per session. |

## Baselines
| Baseline | Type | Why Important | Notes |
|---|---|---|---|
| LoCoMo | Direct long-context baseline | Strong reference point for long conversation QA without the A-MEM memory pipeline | Uses the full preceding conversation and questions in the prompt. |
| ReadAgent | Episodic pagination + memory gisting | Tests a structured long-context memory approach | Much shorter output token length than direct prompting. |
| MemoryBank | Memory management with historical weighting | Compares against a classical memory system with dynamic update logic | Uses Ebbinghaus-style forgetting and user portrait building. |
| MemGPT | Virtual context management | Tests a memory hierarchy approach with explicit context management | Strong on some factual categories, but still uses a static memory structure. |

## Main Results
| Dataset / Benchmark | Metric | Baseline | Ours | Gain / Delta | Notes |
|---|---|---|---|---|---|
| LoCoMo, GPT-4o-mini | Multi-hop F1 | MemGPT 26.65 | 27.02 | +0.37 | Category-level win in the hardest reasoning setting. |
| LoCoMo, GPT-4o-mini | Temporal F1 | MemGPT 25.52 | 45.85 | +20.33 | Largest GPT-4o-mini gain in the main table. |
| LoCoMo, GPT-4o-mini | Single-hop F1 | MemGPT 41.04 | 44.65 | +3.61 | Clear improvement on direct recall questions. |
| LoCoMo, GPT-4o-mini | Adversarial F1 | LoCoMo 69.23 | 50.03 | -19.20 | The direct-prompt baseline still leads on this slice. |
| LoCoMo, GPT-4o-mini | Token length | MemGPT 16,977 | 2,520 | -14,457 | Much shorter answers and memory traces than MemGPT. |
| LoCoMo, Qwen2.5-1.5B | Multi-hop F1 | MemoryBank 11.14 | 18.23 | +7.09 | A-MEM leads the Qwen2.5-1.5B block on multi-hop. |
| LoCoMo, Llama 3.2-1B | Multi-hop F1 | MemoryBank 13.18 | 19.06 | +5.88 | A-MEM also leads on the small Llama block. |
| DialSim | F1 | LoCoMo 2.55 | 3.45 | +0.90 | Paper also reports improvements on BLEU-1, ROUGE-L, ROUGE-2, METEOR, and SBERT similarity. |
| DialSim | SBERT similarity | MemGPT 8.54 | 19.51 | +10.97 | Largest reported gap in the DialSim summary table. |

## Ablations / Analysis
- Removing both link generation and memory evolution causes a substantial drop, with the GPT-4o-mini ablation row falling to 9.65 F1 on multi-hop and 24.55 F1 on temporal questions.
- Keeping link generation but removing memory evolution still helps, which the paper treats as evidence that link generation is the structural foundation and evolution is a refinement layer.
- The hyperparameter study varies retrieval `k` across 10, 20, 30, 40, and 50 on GPT-4o-mini, and the paper says performance generally improves then plateaus or slightly declines.
- Scaling analysis reports retrieval time from 0.31 microseconds at 1,000 memories to 3.70 microseconds at 1,000,000 memories, with linear memory growth.
- The t-SNE analysis shows tighter clustering for A-MEM embeddings than the base memory variant without link generation and evolution.

## Implementation Clues
- The repo organizes the memory system around `memory_layer.py`, where `MemoryNote` stores content, keywords, links, timestamps, context, category, and tags.
- The core retrieval path uses `SimpleEmbeddingRetriever` with `all-MiniLM-L6-v2`, and memory documents are indexed with both content and metadata text.
- `process_memory` retrieves the top-5 neighbors, sends them to the LLM for an evolution decision, and can update links, tags, and neighbor context in place.
- `test_advanced.py` and `test_advanced_robust.py` evaluate the memory system on the LoCoMo dataset and cache memory/retriever state for reuse.
- `run_all_experiments.sh` runs the robust evaluation across GPT-4o-mini, GPT-4o, GPT-4, Llama 3.2 3B/1B, and Qwen2.5 3B/1.5B.
- `run_k_sweep.sh` varies retrieval `k` across 10 to 50 for the same family of models, which matches the paper’s hyperparameter discussion.

## Limitations
- The paper says memory quality is still bounded by the base LLM because the model generates contextual descriptions and link decisions.
- The current implementation is text-only; the paper explicitly lists multimodal memory as future work.
- The repository README in this workspace is only a placeholder, so the code notes are derived from the Python and shell files rather than a maintained project README.

## Takeaways
- A-MEM’s main design move is to shift memory from a fixed store-and-retrieve abstraction to a note graph that can be reorganized by the model itself.
- The strongest practical claim is not raw context length, but better long-horizon organization under a relatively cheap retrieval budget.
- The implementation is simple enough to be reproducible: embedding retrieval, structured note construction, LLM-driven linking, and optional memory evolution.

## Open Questions
- How stable are the learned links across different base LLMs and prompt templates?
- How much of the reported gain comes from structured note construction versus the evolution step?
- Would a multimodal extension preserve the same link-generation and evolution behavior, or require a different note schema?
- The paper reports several metrics, but some category-specific comparisons are not summarized in prose; those need the table for exact values.

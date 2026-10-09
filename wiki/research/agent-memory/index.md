---
title: Agent Memory
domain: research
area: agent-memory
type: overview
status: active
updated: 2026-09-22
tags: [research, agent-memory, papers, index]
---

# Agent Memory

Agent memory 领域的论文库与研究线程。

从 `misc` 剥离，覆盖：记忆架构、评测 benchmark、产品实现。

## Thread Directory

- [Mem0 New Algorithm Benchmark Decision](threads/2026-04-23-mem0-new-algorithm-benchmark-decision.md)
- [Benchmark Comparison Thread](threads/2026-04-25-benchmark-comparison-thread.md) — 各论文 baseline / benchmark / judge model 对比矩阵
- locomo leadboard: https://www.wizwand.com/sota/long-term-memory-evaluation-on-locomo

## Paper Directory

- [Mem0 2026 software / technical release](assets/mem0-2026/note.md) — SDK 2.1.0, evaluation code and saved results; platform boundary, changed judge, headline/artifact discrepancies, and shared 2025 protocol decision updated on 2026-09-20.

### Corpora & Syntheses

- [Jev 相关工作通俗对照](threads/jev-related-work.md)：[LOTUS](../misc/assets/lotus-2025/note.md)、[UtilityQwen](assets/utilityqwen-2025/note.md)、[SCARLet](assets/scarlet-2025/note.md)、[OptiSet](assets/optiset-2026/note.md)。语义算子、证据效用与集合选择。

- [MemAgent](assets/memagent-2025/note.md) — existing paper reading and source archive.

### Agent Memory Architectures

| Paper                                                                                     | Year | Venue   | Importance                                 | Wiki Status |                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ----------------------------------------------------------------------------------------- | ---: | ------- | ------------------------------------------ | ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [A-MEM](assets/amem-2025/note.md)                                                        | 2025 | NeurIPS | Zettelkasten-style agent memory graph      | `processed` |                                                                                                                                                                                                                                                                                                                                                                                                                         |
| [Agentic Memory](assets/agemem-2026/note.md)                                             | 2026 | Arxiv   | Tool-driven memory control policy          | `processed` |                                                                                                                                                                                                                                                                                                                                                                                                                         |
| [ByteRover](assets/byterover-2026/note.md)                                               | 2026 | Arxiv   | LLM-curated hierarchical memory            | `processed` |                                                                                                                                                                                                                                                                                                                                                                                                                         |
| [Claude-Mem](assets/claude-mem-2026/note.md)                                             | 2026 | Repo    | Persistent coding-memory sidecar           | `processed` |                                                                                                                                                                                                                                                                                                                                                                                                                         |
| [ENGRAM](threads/unread-engram-2025.md)                                                     | 2025 | Arxiv   | Lightweight typed episodic/semantic/procedural memory | `stub` |  |
| [EverMemOS](assets/evermemos-2026/note.md)                                               | 2026 | Arxiv   | Self-organizing MemCell/MemScene memory OS | `processed` | https://github.com/EverMind-AI/EverOS/issues/56 paper里的token不是消耗token而是记忆有多少token<br>多个issure提到无法复现 https://github.com/EverMind-AI/EverOS/issues/41, https://github.com/EverMind-AI/EverOS/issues/73<br>                                                                                                                                                                                                                |
| [GRAVITY](threads/unread-gravity-2026.md)                                                   | 2026 | Arxiv   | Generation-time relational/temporal/topical anchoring | `stub` |  |
| [Hindsight](assets/hindsight-2025/note.md)                                               | 2025 | Arxiv   | Retain-recall-reflect memory pipeline      | `processed` |                                                                                                                                                                                                                                                                                                                                                                                                                         |
| [HingeMem](threads/unread-hingemem-2026.md)                                                 | 2026 | Arxiv   | Event boundaries + query-adaptive routing/depth | `stub` |  |
| [Mem0 2025 paper + experiment code](assets/mem0-2025/note.md)                                                         | 2025 | Arxiv   | Production dialogue memory operations      | `processed` | Official historical evaluation/src/rag.py, 256-token k=2 RAG, and paper/code citations; newer memory-benchmarks prompts belong to the separate [Mem0 2026 reference](assets/mem0-2026/note.md)                                                                                                                                                                                                                                                               |
| [MemGPT](assets/memgpt-letta-2023/note.md)                                               | 2023 | Arxiv   | Virtual-context memory hierarchy           | `processed` |                                                                                                                                                                                                                                                                                                                                                                                                                         |
| Memory for Autonomous LLM Agents (原归档已移除) | 2026 | Arxiv   | Mechanisms and evaluation survey           | `processed` |                                                                                                                                                                                                                                                                                                                                                                                                                         |
| [Memobase](assets/memobase-2025/note.md)                                                 | 2025 | Repo    | Personalized agent memory platform         | `processed` | https://github.com/memodb-io/memobase/tree/main/docs/experiments/locomo-benchmark 结果对比表格引用的mem0的结果                                                                                                                                                                                                                                                                                                                      |
| [MemOS](assets/memos-2026/note.md)                                                       | 2026 | Arxiv   | Unified agent-memory system framework      | `processed` |                                                                                                                                                                                                                                                                                                                                                                                                                         |
| [PRISM (Pareto-Efficient)](threads/unread-prism-memory-2026.md)                             | 2026 | Arxiv   | Intent-aware structured retrieval on a cost frontier | `stub` | 与 prism-2025 (Precision-Recall Iterative Selection) 同名不同文 |
| [REMem](assets/remem-2026/note.md)                                                       | 2026 | Arxiv   | Episodic-memory reasoning for agents       | `processed` |                                                                                                                                                                                                                                                                                                                                                                                                                         |
| SALM Survey (原归档已移除)                                           | 2025 | Arxiv   | Human-inspired memory systems survey       | `processed` |                                                                                                                                                                                                                                                                                                                                                                                                                         |
| [Temporal Semantic Memory](assets/temporal-semantic-memory-2026/note.md)                 | 2026 | Arxiv   | Time-aware semantic memory layer           | `processed` |                                                                                                                                                                                                                                                                                                                                                                                                                         |
| [Zep](assets/zep-2025/note.md)                                                           | 2025 | Arxiv   | Temporal knowledge-graph memory layer      | `processed` | 有俩repo 一个项目的，一个paper的有eval.  发文说mem0搞错了 https://blog.getzep.com/lies-damn-lies-statistics-is-mem0-really-sota-in-agent-memory/<br><br>mem0 cto在zep paper repo发issure说zep结果错了 https://github.com/getzep/zep-papers/issues/5<br><br>旧记录中的 answer prompt 文件为 `zep-papers/kg_architecture_agent_memory/locomo_eval/zep_locomo_responses.py`；当前归档未缓存该仓库或文件，`citation.bib` 历史 metadata 快照中的 repositories 为空，无法从本地复核 prompt |
| memU                                                                                      |      |         |                                            |             | https://github.com/NevaMind-AI/memU                                                                                                                                                                                                                                                                                                                                                                                     |

### Agent Memory Evaluation And Reasoning

| Paper | Year | Venue | Importance | Wiki Status |
|---|---:|---|---|---|
| [Episodic Memories Benchmark](assets/episodic-memory-evaluation-benchmark-2025/note.md) | 2025 | Arxiv | Synthetic episodic-memory benchmark | `processed` |
| [LongMemEval](assets/longmemeval-2025/note.md) | 2025 | Arxiv | Long-term chat memory benchmark | `processed` |
| [LoCoMo](assets/locomo-2024/note.md) | 2024 | Arxiv | Multi-session conversational memory benchmark | `processed` |
| [Memory-T1](assets/memory-t1-2025/note.md) | 2025 | Arxiv | Temporal-reasoning memory retriever | `processed` |
| [MemoryArena](assets/memoryarena-2026/note.md) | 2026 | Arxiv | Functional agent-memory benchmark | `processed` |
| [Toward Conversational Agents with Context and Time Sensitive Long-term Memory](assets/toward-conversational-agents-context-time-sensitive-long-term-memory-2024/note.md) | 2024 | Arxiv | Time-sensitive conversational memory retrieval | `processed` |
| [TReMu](assets/tremu-2025/note.md) | 2025 | Arxiv | Neuro-symbolic temporal memory reasoning | `processed` |
| [Memory in the LLM Era](assets/memory-llm-era-2026/note.md) | 2026 | PVLDB | Unified framework + benchmark comparison of 10 memory methods | `processed` |
| [User Memory via Recollection-Familiarity Retrieval](assets/recollection-familiarity-retrieval-2026/note.md) | 2026 | Arxiv | Dual-path personalized memory retrieval | `processed` |
| [MemTrace](threads/unread-memtrace-2026.md) | 2026 | Arxiv | Knowledge-point diagnostics: retrieval vs evidence-use failure | `stub` |
| [MemOps](threads/unread-memops-2026.md) | 2026 | Arxiv | Lifecycle-operation benchmark (remember/update/forget/reflect) | `stub` |
| [RUMBA](threads/unread-rumba-2026.md) | 2026 | Arxiv | Multilingual (Russian) memory benchmark; temporal/session factors | `stub` |
| [Beyond Memory Leaderboards](threads/unread-budgeted-context-restoration-2026.md) | 2026 | Arxiv | Budgeted context restoration; sparse-dense hybrid > architecture labels | `stub` |
| [MEMAUDIT](threads/unread-memaudit-2026.md) | 2026 | Arxiv | Package-oracle protocol isolating memory writing quality | `stub` |

### Product Memory Notes

- [Jev / System One](assets/jev-system-one-2026/note.md) — 2026-09-15 发布的结构化决策模型；概率检索/重排模块，非完整持久记忆系统；blog/docs 已读（2026-09-22）。

| Paper | Year | Venue | Importance | Wiki Status |
|---|---:|---|---|---|
| [Honcho](assets/honcho-2025/note.md) | 2025 | Repo | User-centric social-cognition memory platform with peers, sessions, context, search, and representations | `processed` |
| [OpenAI Memory](assets/openai-memory-2024/note.md) | 2024 | Blog | ChatGPT memory product baseline | `processed` |

### Retrieval Methods (Query Expansion & Multi-Query)

| Paper | Year | Venue | Importance | Wiki Status |
|---|---:|---|---|---|
| [HyDE](threads/unread-hyde-2023.md) | 2023 | SIGIR | Hypothetical document embeddings for zero-shot dense retrieval | `stub` |
| [Query2doc](threads/unread-query2doc-2023.md) | 2023 | EMNLP | LLM query expansion with pseudo-documents | `stub` |
| RAG-Fusion（原归档已移除） | 2023 | Blog | Multi-query generation + Reciprocal Rank Fusion | `stub` |
| [MemoRAG](../misc/assets/memorag-2025/note.md) | 2025 | WWW | Global memory model generates clue drafts as retrieval queries | `stub` |
| [AutoBool](../misc/assets/autobool-2026/note.md) | 2026 | Arxiv | RL-trained LLM for Boolean query generation (literature retrieval) | `stub` |
| [PRISM](../misc/assets/prism-2025/note.md) | 2025 | Arxiv (withdrawn ICLR 2026) | Precision-recall iterative selection; Prune-and-Recover loop | `stub` |
| [Collab-RAG](threads/unread-collab-rag-2025.md) | 2025 | Arxiv | Fine-tuned 3B SLM decomposer outperforms frozen 32B LLM | `stub` |
| [Query Decomposition as Bandit](threads/unread-query-decomp-bandit-2025.md) | 2025 | Arxiv | Multi-armed bandit for sub-query selection; 35% precision gain | `stub` |
| [Query Optimization Survey](threads/unread-query-optim-survey-2024.md) | 2024 | Arxiv | Taxonomy: Foundation→Expansion→Sophistication→Agentic | `stub` |
| [Multi-Turn Conversational RAG](threads/unread-multi-turn-conv-rag-2026.md) | 2026 | Arxiv | Retrieval stability in multi-turn settings; RRF improves stability | `stub` |

### Iterative / Active Retrieval

| Paper | Year | Venue | Importance | Wiki Status |
|---|---:|---|---|---|
| [IRCoT](threads/unread-irco-2023.md) | 2023 | ACL | Interleave CoT reasoning with retrieval; key multi-hop baseline | `stub` |
| [Self-RAG](../misc/assets/self-rag-2024/note.md) | 2024 | ICLR | Fine-tuned adaptive retrieve-generate-critique cycle | `stub` |
| [FLARE](threads/unread-flare-2023.md) | 2023 | EMNLP | Generation-uncertainty-triggered active retrieval | `stub` |
| FAIR-RAG（原归档已移除） | 2025 | Arxiv | Multi-model pipeline with LLM-as-Judge ablations | `stub` |
| [ReAct](threads/unread-react-2023.md) | 2023 | ICLR | Interleave reasoning traces with actions (search); framework inspiration | `stub` |

### Search as Planning / LLM as Heuristic

| Paper | Year | Venue | Importance | Wiki Status |
|---|---:|---|---|---|
| [LLM-A*](threads/unread-llm-astar-2024.md) | 2024 | EMNLP Findings | LLM provides heuristic h(n) in A*; proof-of-concept for LLM-as-heuristic | `stub` |
| [Think-on-Graph 2.0](threads/unread-tog2-2025.md) | 2025 | ICLR | KG + unstructured text retrieval; graph traversal as beam search | `stub` |
| [HopRAG](../misc/assets/hoprag-2025/note.md) | 2025 | ACL Findings | Passage graph with logical connections; multi-hop via LLM reasoning | `stub` |
| ERL（原归档已移除） | 2026 | Arxiv | LLM-based retrieval 56.1% vs embedding baseline; quality > quantity | `stub` |
| [Reranking Survey](threads/unread-reranking-survey-2025.md) | 2025 | Arxiv | LLMs as zero-shot listwise rankers outperform supervised methods | `stub` |

### Memory Retrieval Granularity & Personalization

| Paper | Year | Venue | Importance | Wiki Status |
|---|---:|---|---|---|
| [Segment-Level Memory](threads/unread-segment-level-memory-2025.md) | 2025 | ICLR | Turn-level too fine, session-level too coarse; topically coherent units | `stub` |
| [Entropy-Based Adaptive Memory](threads/unread-entropy-adaptive-memory-2026.md) | 2026 | ICLR | Entropy router selects retrieval granularity per query | `stub` |
| [Memoria](threads/unread-memoria-2025.md) | 2025 | Arxiv | Session summarization + weighted KG; 115k→400 tokens, 87.1% accuracy | `stub` |
| [Personalize Before Retrieve](../misc/assets/personalize-before-retrieve-2025/note.md) | 2025 | Arxiv | User-specific query expansion injecting history/preferences/persona | `stub` |
| [Mintlify ChromaFs](../misc/assets/mintlify-chromafs-2026/note.md) | 2026 | Blog | Virtual filesystem for LLM retrieval; 460x speedup | `stub` |

### Raw-History Retrieval & Adaptive Routing

以下均为未读 `stub`。

| Paper | Year | Venue | Importance | Wiki Status |
|---|---:|---|---|---|
| [SmartSearch](threads/unread-smartsearch-2026.md) | 2026 | Arxiv | Raw deterministic recall + learned rank fusion; ranking beats structure | `stub` |
| [AgentIR](threads/unread-agentir-2026.md) | 2026 | Arxiv | BM25-margin cascade skipping dense retrieval | `stub` |
| [Lexical-Dense Fusion](threads/unread-lexical-dense-fusion-2026.md) | 2026 | Arxiv | Controlled BM25 + max-turn dense fusion; +11.2 Hit@1 on LoCoMo | `stub` |
| [Back to Basics (Nano-Memory)](threads/unread-back-to-basics-2026.md) | 2026 | Arxiv | Turn Isolation Retrieval + Query-Driven Pruning | `stub` |
| [SelRoute](threads/unread-selroute-2026.md) | 2026 | Arxiv | Query-type routing among lexical/semantic/hybrid/enriched pipelines | `stub` |
| [EviMem](threads/unread-evimem-2026.md) | 2026 | Arxiv | Evidence-gap diagnosis, query refinement, abstention | `stub` |
| [TierMem](threads/unread-tiermem-2026.md) | 2026 | Arxiv | Cheapest-sufficient-tier answering with raw-log escalation | `stub` |
| [Fidelity Before Structure](threads/unread-fidelity-before-structure-2026.md) | 2026 | Arxiv | Verbatim chunks beat lossy typed artifacts (+15.9 LoCoMo, +22.0 LongMemEval-S) | `stub` |
| [Event-Memory Baseline](threads/unread-event-memory-baseline-2025.md) | 2025 | Arxiv | Non-compressive event memory + simple dense retrieval | `stub` |
| [DeferMem](threads/unread-defermem-2026.md) | 2026 | Arxiv | High-recall retrieval + RL evidence distillation | `stub` |
| [MGRetrieval](threads/unread-mgretrieval-2026.md) | 2026 | Arxiv | Memory-guided reflective retrieval with sufficiency stopping | `stub` |
| [Eywa](threads/unread-eywa-2026.md) | 2026 | Arxiv | Immutable evidence + derived facts with provenance | `stub` |
| [ConvMemory](threads/unread-convmemory-2026.md) | 2026 | Arxiv | Lightweight lexical-dense reranker; negative attribution result | `stub` |
| [EAR](threads/unread-ear-2026.md) | 2026 | Arxiv | Reflective recall cycle + experience-based reranker adaptation | `stub` |
| [Training-Free Control](threads/unread-training-free-control-2026.md) | 2026 | Arxiv | Whether to apply retrieved memory at all: acceptance/rollback/retirement | `stub` |
| [Recursive Language Models](threads/unread-recursive-language-models-2025.md) | 2025 | Arxiv | Programmatic query-time inspection of long contexts | `stub` |

### IR Foundations

| Paper | Year | Venue | Importance | Wiki Status |
|---|---:|---|---|---|
| [DPR](threads/unread-dpr-2020.md) | 2020 | EMNLP | Canonical dense dual-encoder retrieval baseline | `stub` |
| [ColBERT](threads/unread-colbert-2020.md) | 2020 | SIGIR | Token-level late interaction; strong reranking primitive | `stub` |
| [SPLADE v2](threads/unread-splade-v2-2021.md) | 2021 | Arxiv | Learned sparse lexical expansion beyond BM25 | `stub` |
| [BEIR](../misc/assets/beir-2021/note.md) | 2021 | NeurIPS D&B | Heterogeneous zero-shot retrieval evaluation | `stub` |

## Archive Migration Caveats

- Memory for Autonomous LLM Agents (原归档已移除) and SALM Survey (原归档已移除): their notes, metadata, and source files were already deleted before this migration; historical directory entries above are retained as unavailable records.
- Unread summaries now live in `threads/unread-*.md`; their historical `stub` labels do not establish reading. Bibliographic fields were migrated from existing records without external reverification.

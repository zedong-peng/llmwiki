---
title: Agent Memory
domain: research
area: agent-memory
type: overview
status: active
updated: 2026-07-27
tags: [research, agent-memory, papers, index]
---

# Agent Memory

Agent memory 领域的论文库与研究线程。

从 `misc` 剥离，覆盖：记忆架构、评测 benchmark、产品实现。

## Thread Directory

- [Threads Guide](threads/index.md)
- [Mem0 New Algorithm Benchmark Decision](threads/2026-04-23-mem0-new-algorithm-benchmark-decision.md)
- [Benchmark Comparison Thread](threads/2026-04-25-benchmark-comparison-thread.md) — 各论文 baseline / benchmark / judge model 对比矩阵
- locomo leadboard: https://www.wizwand.com/sota/long-term-memory-evaluation-on-locomo

## Paper Directory

- [Papers Directory Guide](papers/index.md)

### Corpora & Syntheses

- [LazyMem Related-Work Corpus](papers/lazymem-related-work/index.md) — 45 篇冻结 arXiv 语料 + 新颖性审计 + ResearchStudio 复核;结论:BM25-window 是当前最强默认,compiler 为被拒 ablation

### Agent Memory Architectures

| Paper                                                                                     | Year | Venue   | Importance                                 | Wiki Status |                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ----------------------------------------------------------------------------------------- | ---: | ------- | ------------------------------------------ | ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [A-MEM](papers/amem-2025/index.md)                                                        | 2025 | NeurIPS | Zettelkasten-style agent memory graph      | `processed` |                                                                                                                                                                                                                                                                                                                                                                                                                         |
| [Agentic Memory](papers/agemem-2026/index.md)                                             | 2026 | Arxiv   | Tool-driven memory control policy          | `processed` |                                                                                                                                                                                                                                                                                                                                                                                                                         |
| [ByteRover](papers/byterover-2026/index.md)                                               | 2026 | Arxiv   | LLM-curated hierarchical memory            | `processed` |                                                                                                                                                                                                                                                                                                                                                                                                                         |
| [Claude-Mem](papers/claude-mem-2026/index.md)                                             | 2026 | Repo    | Persistent coding-memory sidecar           | `processed` |                                                                                                                                                                                                                                                                                                                                                                                                                         |
| [ENGRAM](papers/engram-2025/index.md)                                                     | 2025 | Arxiv   | Lightweight typed episodic/semantic/procedural memory | `stub` | LazyMem corpus |
| [EverMemOS](papers/evermemos-2026/index.md)                                               | 2026 | Arxiv   | Self-organizing MemCell/MemScene memory OS | `processed` | https://github.com/EverMind-AI/EverOS/issues/56 paper里的token不是消耗token而是记忆有多少token<br>多个issure提到无法复现 https://github.com/EverMind-AI/EverOS/issues/41, https://github.com/EverMind-AI/EverOS/issues/73<br>                                                                                                                                                                                                                |
| [GRAVITY](papers/gravity-2026/index.md)                                                   | 2026 | Arxiv   | Generation-time relational/temporal/topical anchoring | `stub` | LazyMem corpus |
| [Hindsight](papers/hindsight-2025/index.md)                                               | 2025 | Arxiv   | Retain-recall-reflect memory pipeline      | `processed` |                                                                                                                                                                                                                                                                                                                                                                                                                         |
| [HingeMem](papers/hingemem-2026/index.md)                                                 | 2026 | Arxiv   | Event boundaries + query-adaptive routing/depth | `stub` | LazyMem corpus |
| [Mem0](papers/mem0-2025/index.md)                                                         | 2025 | Arxiv   | Production dialogue memory operations      | `processed` | answer prompt在 /Users/pengzedong/Documents/GitHub/llmwiki/wiki/research/agent-memory/papers/mem0-2025/repo/memory-benchmarks/benchmarks/locomo/prompts.py                                                                                                                                                                                                                                                               |
| [MemGPT](papers/memgpt-letta-2023/index.md)                                               | 2023 | Arxiv   | Virtual-context memory hierarchy           | `processed` |                                                                                                                                                                                                                                                                                                                                                                                                                         |
| [Memory for Autonomous LLM Agents](papers/memory-for-autonomous-llm-agents-2026/index.md) | 2026 | Arxiv   | Mechanisms and evaluation survey           | `processed` |                                                                                                                                                                                                                                                                                                                                                                                                                         |
| [Memobase](papers/memobase-2025/index.md)                                                 | 2025 | Repo    | Personalized agent memory platform         | `processed` | https://github.com/memodb-io/memobase/tree/main/docs/experiments/locomo-benchmark 结果对比表格引用的mem0的结果                                                                                                                                                                                                                                                                                                                      |
| [MemOS](papers/memos-2026/index.md)                                                       | 2026 | Arxiv   | Unified agent-memory system framework      | `processed` |                                                                                                                                                                                                                                                                                                                                                                                                                         |
| [PRISM (Pareto-Efficient)](papers/prism-memory-2026/index.md)                             | 2026 | Arxiv   | Intent-aware structured retrieval on a cost frontier | `stub` | LazyMem corpus;与 prism-2025 (Precision-Recall Iterative Selection) 同名不同文 |
| [REMem](papers/remem-2026/index.md)                                                       | 2026 | Arxiv   | Episodic-memory reasoning for agents       | `processed` |                                                                                                                                                                                                                                                                                                                                                                                                                         |
| [SALM Survey](papers/salm-survey-2025/index.md)                                           | 2025 | Arxiv   | Human-inspired memory systems survey       | `processed` |                                                                                                                                                                                                                                                                                                                                                                                                                         |
| [Temporal Semantic Memory](papers/temporal-semantic-memory-2026/index.md)                 | 2026 | Arxiv   | Time-aware semantic memory layer           | `processed` |                                                                                                                                                                                                                                                                                                                                                                                                                         |
| [Zep](papers/zep-2025/index.md)                                                           | 2025 | Arxiv   | Temporal knowledge-graph memory layer      | `processed` | 有俩repo 一个项目的，一个paper的有eval.  发文说mem0搞错了 https://blog.getzep.com/lies-damn-lies-statistics-is-mem0-really-sota-in-agent-memory/<br><br>mem0 cto在zep paper repo发issure说zep结果错了 https://github.com/getzep/zep-papers/issues/5<br><br>answer prompt在 /Users/pengzedong/Documents/GitHub/llmwiki/wiki/research/agent-memory/papers/zep-2025/repo/zep-papers/kg_architecture_agent_memory/locomo_eval/zep_locomo_responses.py |
| memU                                                                                      |      |         |                                            |             | https://github.com/NevaMind-AI/memU                                                                                                                                                                                                                                                                                                                                                                                     |

### Agent Memory Evaluation And Reasoning

| Paper | Year | Venue | Importance | Wiki Status |
|---|---:|---|---|---|
| [Episodic Memories Benchmark](papers/episodic-memory-evaluation-benchmark-2025/index.md) | 2025 | Arxiv | Synthetic episodic-memory benchmark | `processed` |
| [LongMemEval](papers/longmemeval-2025/index.md) | 2025 | Arxiv | Long-term chat memory benchmark | `processed` |
| [LoCoMo](papers/locomo-2024/index.md) | 2024 | Arxiv | Multi-session conversational memory benchmark | `processed` |
| [Memory-T1](papers/memory-t1-2025/index.md) | 2025 | Arxiv | Temporal-reasoning memory retriever | `processed` |
| [MemoryArena](papers/memoryarena-2026/index.md) | 2026 | Arxiv | Functional agent-memory benchmark | `processed` |
| [Toward Conversational Agents with Context and Time Sensitive Long-term Memory](papers/toward-conversational-agents-context-time-sensitive-long-term-memory-2024/index.md) | 2024 | Arxiv | Time-sensitive conversational memory retrieval | `processed` |
| [TReMu](papers/tremu-2025/index.md) | 2025 | Arxiv | Neuro-symbolic temporal memory reasoning | `processed` |
| [Memory in the LLM Era](papers/memory-llm-era-2026/index.md) | 2026 | PVLDB | Unified framework + benchmark comparison of 10 memory methods | `processed` |
| [User Memory via Recollection-Familiarity Retrieval](papers/recollection-familiarity-retrieval-2026/index.md) | 2026 | Arxiv | Dual-path personalized memory retrieval | `processed` |
| [MemTrace](papers/memtrace-2026/index.md) | 2026 | Arxiv | Knowledge-point diagnostics: retrieval vs evidence-use failure | `stub` |
| [MemOps](papers/memops-2026/index.md) | 2026 | Arxiv | Lifecycle-operation benchmark (remember/update/forget/reflect) | `stub` |
| [RUMBA](papers/rumba-2026/index.md) | 2026 | Arxiv | Multilingual (Russian) memory benchmark; temporal/session factors | `stub` |
| [Beyond Memory Leaderboards](papers/budgeted-context-restoration-2026/index.md) | 2026 | Arxiv | Budgeted context restoration; sparse-dense hybrid > architecture labels | `stub` |
| [MEMAUDIT](papers/memaudit-2026/index.md) | 2026 | Arxiv | Package-oracle protocol isolating memory writing quality | `stub` |

### Product Memory Notes

| Paper | Year | Venue | Importance | Wiki Status |
|---|---:|---|---|---|
| [Honcho](papers/honcho-2025/index.md) | 2025 | Repo | User-centric social-cognition memory platform with peers, sessions, context, search, and representations | `processed` |
| [OpenAI Memory](papers/openai-memory-2024/index.md) | 2024 | Blog | ChatGPT memory product baseline | `processed` |

### Retrieval Methods (Query Expansion & Multi-Query)

| Paper | Year | Venue | Importance | Wiki Status |
|---|---:|---|---|---|
| [HyDE](papers/hyde-2023/index.md) | 2023 | SIGIR | Hypothetical document embeddings for zero-shot dense retrieval | `stub` |
| [Query2doc](papers/query2doc-2023/index.md) | 2023 | EMNLP | LLM query expansion with pseudo-documents; adjacent to LazyMem predicate compilation | `stub` |
| [RAG-Fusion](papers/rag-fusion-2023/index.md) | 2023 | Blog | Multi-query generation + Reciprocal Rank Fusion — closest prior to LAzyMem | `stub` |
| [MemoRAG](papers/memorag-2025/index.md) | 2025 | WWW | Global memory model generates clue drafts as retrieval queries — closest published work to LAzyMem | `stub` |
| [AutoBool](papers/autobool-2026/index.md) | 2026 | Arxiv | RL-trained LLM for Boolean query generation (literature retrieval) | `stub` |
| [PRISM](papers/prism-2025/index.md) | 2025 | Arxiv (withdrawn ICLR 2026) | Precision-recall iterative selection; Prune-and-Recover loop | `stub` |
| [Collab-RAG](papers/collab-rag-2025/index.md) | 2025 | Arxiv | Fine-tuned 3B SLM decomposer outperforms frozen 32B LLM | `stub` |
| [Query Decomposition as Bandit](papers/query-decomp-bandit-2025/index.md) | 2025 | Arxiv | Multi-armed bandit for sub-query selection; 35% precision gain | `stub` |
| [Query Optimization Survey](papers/query-optim-survey-2024/index.md) | 2024 | Arxiv | Taxonomy: Foundation→Expansion→Sophistication→Agentic | `stub` |
| [Multi-Turn Conversational RAG](papers/multi-turn-conv-rag-2026/index.md) | 2026 | Arxiv | Retrieval stability in multi-turn settings; RRF improves stability | `stub` |

### Iterative / Active Retrieval

| Paper | Year | Venue | Importance | Wiki Status |
|---|---:|---|---|---|
| [IRCoT](papers/irco-2023/index.md) | 2023 | ACL | Interleave CoT reasoning with retrieval; key multi-hop baseline | `stub` |
| [Self-RAG](papers/self-rag-2024/index.md) | 2024 | ICLR | Fine-tuned adaptive retrieve-generate-critique cycle | `stub` |
| [FLARE](papers/flare-2023/index.md) | 2023 | EMNLP | Generation-uncertainty-triggered active retrieval | `stub` |
| [FAIR-RAG](papers/fair-rag-2025/index.md) | 2025 | Arxiv | Multi-model pipeline with LLM-as-Judge ablations | `stub` |
| [ReAct](papers/react-2023/index.md) | 2023 | ICLR | Interleave reasoning traces with actions (search); framework inspiration | `stub` |

### Search as Planning / LLM as Heuristic

| Paper | Year | Venue | Importance | Wiki Status |
|---|---:|---|---|---|
| [LLM-A*](papers/llm-astar-2024/index.md) | 2024 | EMNLP Findings | LLM provides heuristic h(n) in A*; proof-of-concept for LLM-as-heuristic | `stub` |
| [Think-on-Graph 2.0](papers/tog2-2025/index.md) | 2025 | ICLR | KG + unstructured text retrieval; graph traversal as beam search | `stub` |
| [HopRAG](papers/hoprag-2025/index.md) | 2025 | ACL Findings | Passage graph with logical connections; multi-hop via LLM reasoning | `stub` |
| [ERL](papers/erl-2026/index.md) | 2026 | Arxiv | LLM-based retrieval 56.1% vs embedding baseline; quality > quantity | `stub` |
| [Reranking Survey](papers/reranking-survey-2025/index.md) | 2025 | Arxiv | LLMs as zero-shot listwise rankers outperform supervised methods | `stub` |

### Memory Retrieval Granularity & Personalization

| Paper | Year | Venue | Importance | Wiki Status |
|---|---:|---|---|---|
| [Segment-Level Memory](papers/segment-level-memory-2025/index.md) | 2025 | ICLR | Turn-level too fine, session-level too coarse; topically coherent units | `stub` |
| [Entropy-Based Adaptive Memory](papers/entropy-adaptive-memory-2026/index.md) | 2026 | ICLR | Entropy router selects retrieval granularity per query | `stub` |
| [Memoria](papers/memoria-2025/index.md) | 2025 | Arxiv | Session summarization + weighted KG; 115k→400 tokens, 87.1% accuracy | `stub` |
| [Personalize Before Retrieve](papers/personalize-before-retrieve-2025/index.md) | 2025 | Arxiv | User-specific query expansion injecting history/preferences/persona | `stub` |
| [Mintlify ChromaFs](papers/mintlify-chromafs-2026/index.md) | 2026 | Blog | Virtual filesystem for LLM retrieval; 460x speedup; direct LAzyMem inspiration | `stub` |

### Raw-History Retrieval & Adaptive Routing (LazyMem Corpus)

来自 [LazyMem Related-Work Corpus](papers/lazymem-related-work/index.md) 的 raw-retrieval 类论文,均为 `stub`。

| Paper | Year | Venue | Importance | Wiki Status |
|---|---:|---|---|---|
| [SmartSearch](papers/smartsearch-2026/index.md) | 2026 | Arxiv | Raw deterministic recall + learned rank fusion; ranking beats structure | `stub` |
| [AgentIR](papers/agentir-2026/index.md) | 2026 | Arxiv | BM25-margin cascade skipping dense retrieval — Level 1 collision with LazyMem | `stub` |
| [Lexical-Dense Fusion](papers/lexical-dense-fusion-2026/index.md) | 2026 | Arxiv | Controlled BM25 + max-turn dense fusion; +11.2 Hit@1 on LoCoMo | `stub` |
| [Back to Basics (Nano-Memory)](papers/back-to-basics-2026/index.md) | 2026 | Arxiv | Turn Isolation Retrieval + Query-Driven Pruning | `stub` |
| [SelRoute](papers/selroute-2026/index.md) | 2026 | Arxiv | Query-type routing among lexical/semantic/hybrid/enriched pipelines | `stub` |
| [EviMem](papers/evimem-2026/index.md) | 2026 | Arxiv | Evidence-gap diagnosis, query refinement, abstention | `stub` |
| [TierMem](papers/tiermem-2026/index.md) | 2026 | Arxiv | Cheapest-sufficient-tier answering with raw-log escalation | `stub` |
| [Fidelity Before Structure](papers/fidelity-before-structure-2026/index.md) | 2026 | Arxiv | Verbatim chunks beat lossy typed artifacts (+15.9 LoCoMo, +22.0 LongMemEval-S) | `stub` |
| [Event-Memory Baseline](papers/event-memory-baseline-2025/index.md) | 2025 | Arxiv | Non-compressive event memory + simple dense retrieval | `stub` |
| [DeferMem](papers/defermem-2026/index.md) | 2026 | Arxiv | High-recall retrieval + RL evidence distillation | `stub` |
| [MGRetrieval](papers/mgretrieval-2026/index.md) | 2026 | Arxiv | Memory-guided reflective retrieval with sufficiency stopping | `stub` |
| [Eywa](papers/eywa-2026/index.md) | 2026 | Arxiv | Immutable evidence + derived facts with provenance | `stub` |
| [ConvMemory](papers/convmemory-2026/index.md) | 2026 | Arxiv | Lightweight lexical-dense reranker; negative attribution result | `stub` |
| [EAR](papers/ear-2026/index.md) | 2026 | Arxiv | Reflective recall cycle + experience-based reranker adaptation | `stub` |
| [Training-Free Control](papers/training-free-control-2026/index.md) | 2026 | Arxiv | Whether to apply retrieved memory at all: acceptance/rollback/retirement | `stub` |
| [Recursive Language Models](papers/recursive-language-models-2025/index.md) | 2025 | Arxiv | Programmatic query-time inspection of long contexts | `stub` |

### IR Foundations

| Paper | Year | Venue | Importance | Wiki Status |
|---|---:|---|---|---|
| [DPR](papers/dpr-2020/index.md) | 2020 | EMNLP | Canonical dense dual-encoder retrieval baseline | `stub` |
| [ColBERT](papers/colbert-2020/index.md) | 2020 | SIGIR | Token-level late interaction; strong reranking primitive | `stub` |
| [SPLADE v2](papers/splade-v2-2021/index.md) | 2021 | Arxiv | Learned sparse lexical expansion beyond BM25 | `stub` |
| [BEIR](papers/beir-2021/index.md) | 2021 | NeurIPS D&B | Heterogeneous zero-shot retrieval evaluation | `stub` |


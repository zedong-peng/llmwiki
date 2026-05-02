---
title: Agent Memory
domain: research
area: agent-memory
type: overview
status: active
updated: 2026-04-26
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

### Agent Memory Architectures

| Paper                                                                                     | Year | Venue   | Importance                                 | Wiki Status |                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ----------------------------------------------------------------------------------------- | ---: | ------- | ------------------------------------------ | ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [A-MEM](papers/amem-2025/index.md)                                                        | 2025 | NeurIPS | Zettelkasten-style agent memory graph      | `processed` |                                                                                                                                                                                                                                                                                                                                                                                                                         |
| [Agentic Memory](papers/agemem-2026/index.md)                                             | 2026 | Arxiv   | Tool-driven memory control policy          | `processed` |                                                                                                                                                                                                                                                                                                                                                                                                                         |
| [ByteRover](papers/byterover-2026/index.md)                                               | 2026 | Arxiv   | LLM-curated hierarchical memory            | `processed` |                                                                                                                                                                                                                                                                                                                                                                                                                         |
| [Claude-Mem](papers/claude-mem-2026/index.md)                                             | 2026 | Repo    | Persistent coding-memory sidecar           | `processed` |                                                                                                                                                                                                                                                                                                                                                                                                                         |
| [EverMemOS](papers/evermemos-2026/index.md)                                               | 2026 | Arxiv   | Self-organizing MemCell/MemScene memory OS | `processed` | https://github.com/EverMind-AI/EverOS/issues/56 paper里的token不是消耗token而是记忆有多少token<br>多个issure提到无法复现 https://github.com/EverMind-AI/EverOS/issues/41, https://github.com/EverMind-AI/EverOS/issues/73<br>                                                                                                                                                                                                                |
| [Hindsight](papers/hindsight-2025/index.md)                                               | 2025 | Arxiv   | Retain-recall-reflect memory pipeline      | `processed` |                                                                                                                                                                                                                                                                                                                                                                                                                         |
| [Mem0](papers/mem0-2025/index.md)                                                         | 2025 | Arxiv   | Production dialogue memory operations      | `processed` | answer prompt在 /Users/pengzedong/Documents/GitHub/llmwiki/wiki/research/agent-memory/papers/mem0-2025/repo/memory-benchmarks/benchmarks/locomo/prompts.py                                                                                                                                                                                                                                                               |
| [MemGPT](papers/memgpt-letta-2023/index.md)                                               | 2023 | Arxiv   | Virtual-context memory hierarchy           | `processed` |                                                                                                                                                                                                                                                                                                                                                                                                                         |
| [Memory for Autonomous LLM Agents](papers/memory-for-autonomous-llm-agents-2026/index.md) | 2026 | Arxiv   | Mechanisms and evaluation survey           | `processed` |                                                                                                                                                                                                                                                                                                                                                                                                                         |
| [Memobase](papers/memobase-2025/index.md)                                                 | 2025 | Repo    | Personalized agent memory platform         | `processed` | https://github.com/memodb-io/memobase/tree/main/docs/experiments/locomo-benchmark 结果对比表格引用的mem0的结果                                                                                                                                                                                                                                                                                                                      |
| [MemOS](papers/memos-2026/index.md)                                                       | 2026 | Arxiv   | Unified agent-memory system framework      | `processed` |                                                                                                                                                                                                                                                                                                                                                                                                                         |
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

### Product Memory Notes

| Paper | Year | Venue | Importance | Wiki Status |
|---|---:|---|---|---|
| [Honcho](papers/honcho-2025/index.md) | 2025 | Repo | User-centric social-cognition memory platform with peers, sessions, context, search, and representations | `processed` |
| [OpenAI Memory](papers/openai-memory-2024/index.md) | 2024 | Blog | ChatGPT memory product baseline | `processed` |

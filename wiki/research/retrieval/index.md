---
title: Retrieval
domain: research
area: retrieval
type: overview
status: active
updated: 2026-10-09
tags: [research, retrieval, rag, index]
---

# Retrieval

检索、RAG 与长上下文：benchmark、检索优化、检索推理与 AI 数据系统。由 `misc` 拆出（2026-10-09）。

## Threads

- [BEIR Related Paper Search](threads/2026-04-19-beir-related-paper-search.md)
- [BEIR Current SOTA Snapshot](threads/2026-04-19-beir-current-sota-snapshot.md)

## Retrieval-Augmented Generation And Retrieval Reasoning

| Paper | Year | Venue | Importance | Wiki Status |
|---|---:|---|---|---|
| [CORAL](assets/coral-2024/note.md) | 2024 | Arxiv | Multi-turn conversational RAG benchmark | `processed` |
| [Demonstrate-Search-Predict](assets/dsp-2022/note.md) | 2022 | ICML | Programmatic retrieval-augmented prompting | `processed` |
| FAIR-RAG | 2025 | Arxiv | Gap-driven iterative RAG refinement | `processed` |
| [HippoRAG](assets/hipporag-2024/note.md) | 2024 | NeurIPS | Graph-based multi-hop retrieval | `processed` |
| [HopRAG](assets/hoprag-2025/note.md) | 2025 | Arxiv | Logic-aware graph RAG | `processed` |
| [IRCoT](assets/ircot-2023/note.md) | 2023 | Arxiv | Reasoning-guided iterative retrieval | `processed` |
| [Iterative Retrieval-Generation Synergy](assets/iter-retgen-2023/note.md) | 2023 | EMNLP | Alternating retrieval-generation feedback loop | `processed` |
| [MemoRAG](assets/memorag-2025/note.md) | 2024 | Arxiv | Global-memory retrieval augmentation | `processed` |
| [Multi-Turn Conversational RAG Comparison](assets/multi-turn-conversational-rag-2026/note.md) | 2026 | Arxiv | Controlled multi-turn RAG comparison | `processed` |
| [PRISM](assets/prism-2025/note.md) | 2025 | Arxiv | Three-agent multi-hop retriever | `processed` |
| RAG-Fusion | 2024 | Arxiv | Multi-query retrieval fusion | `processed` |
| [Self-RAG](assets/self-rag-2024/note.md) | 2024 | ICLR | Self-reflective retrieval generation | `processed` |
| [Think-on-Graph 2.0](assets/think-on-graph-2-2025/note.md) | 2025 | ICLR | Training-free graph-guided RAG | `processed` |

## Retrieval Optimization And Search Systems

| Paper | Year | Venue | Importance | Wiki Status |
|---|---:|---|---|---|
| [BEIR](assets/beir-2021/note.md) | 2021 | NeurIPS | Zero-shot retrieval benchmark suite | `processed` |
| [AutoBool](assets/autobool-2026/note.md) | 2026 | EACL | RL-trained Boolean query generation | `processed` |
| [BIRCO](assets/birco-2024/note.md) | 2024 | Arxiv | Complex-objective retrieval benchmark | `processed` |
| [BRIGHT](assets/bright-2025/note.md) | 2025 | ICLR | Reasoning-intensive retrieval benchmark | `processed` |
| [FollowIR](assets/followir-2025/note.md) | 2025 | NAACL | Instruction-following retrieval benchmark | `processed` |
| [InPars](assets/inpars-2022/note.md) | 2022 | SIGIR | Synthetic-query IR augmentation | `processed` |
| [InPars-v2](assets/inpars-v2-2023/note.md) | 2023 | Arxiv | Open-source BEIR query generation | `processed` |
| [How We Built a Virtual Filesystem for Our Assistant](assets/mintlify-chromafs-2026/note.md) | 2026 | Blog | Virtual filesystem retrieval layer | `processed` |
| [LLM Reranking Survey](assets/llm-reranking-survey-2025/note.md) | 2025 | Arxiv | Reranking evolution survey | `processed` |
| [Personalize Before Retrieve](assets/personalize-before-retrieve-2025/note.md) | 2025 | AAAI | Personalized pre-retrieval query expansion | `processed` |
| [Query Decomposition for RAG](assets/query-decomposition-as-bandit-2025/note.md) | 2025 | Arxiv | Bandit-based query decomposition | `processed` |
| Query Optimization Survey | 2024 | Arxiv | Query optimization survey | `processed` |
| [RAGChecker](assets/ragchecker-2024/note.md) | 2024 | Arxiv | Fine-grained RAG diagnosis framework | `processed` |
| [RAR-b](assets/rar-b-2024/note.md) | 2024 | Arxiv | Reasoning-as-retrieval benchmark | `processed` |
| [TART](assets/tart-2023/note.md) | 2023 | ACL Findings | Instruction-conditioned retrieval baseline | `processed` |

## Code Retrieval Benchmarks

| Paper | Year | Venue | Importance | Wiki Status |
|---|---:|---|---|---|
| [CodeSearchNet](threads/unread/codesearchnet-2019.md) | 2019 | Arxiv | Multilingual code search benchmark | `queued` |
| [CoIR](threads/unread/coir-2024.md) | 2024 | Arxiv | Comprehensive code retrieval benchmark | `queued` |

## AI Data Systems

| Paper | Year | Venue | Importance | Wiki Status |
|---|---:|---|---|---|
| [LOTUS](assets/lotus-2025/note.md) | 2024 | Arxiv | Declarative semantic operator system | `processed` |
| [Palimpzest](assets/palimpzest-2024/note.md) | 2024 | Arxiv | Declarative AI workload optimizer | `processed` |

- 2026-09-22：LOTUS 补充官方代码静态核查及 [[research/agent-memory/threads/jev-related-work|与 UtilityQwen / SCARLet / OptiSet 的对照]]。

## Long Context

| Paper | Year | Venue | Importance | Wiki Status |
|---|---:|---|---|---|
| [RULER](assets/ruler-2024/note.md) | 2024 | Arxiv | Effective context length benchmark | `processed` |
| [In-Place TTT](assets/in-place-ttt-2026/note.md) | 2026 | ICLR | Fast-weight long-context adaptation | `processed` |

## Tools

| Tool | Year | Type | Importance | Wiki Status |
|---|---:|---|---|---|
| [zvec-grep (zg)](assets/zvec-grep-2026/note.md) | 2026 | Repo | Local ripgrep + BM25 + vector search with RRF, CLI/MCP for coding agents | `processed` |

## Migration Archive Gaps

FAIR-RAG、RAG-Fusion 与 Query Optimization Survey 的原归档在迁移前已删除，表中保留为纯文本。

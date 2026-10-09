---
title: Misc Paper Library
domain: research
area: misc
type: overview
status: active
updated: 2026-09-17
tags: [research, misc, papers, index]
---

# Misc Paper Library

`misc` 是论文缓冲区。

> Agent memory 相关论文（架构、评测、产品）已剥离至 [[../agent-memory/index]]。

## Thread Directory

- [BEIR Related Paper Search](threads/2026-04-19-beir-related-paper-search.md)
- [BEIR Current SOTA Snapshot](threads/2026-04-19-beir-current-sota-snapshot.md)
- [Cursor Blog Reading Notes](threads/2026-04-19-cursor-blog-reading-notes.md)
- [LLM Leaderboard Resources](threads/2026-04-25-llm-leaderboard-resources.md)
- [Dream-RSI Search](threads/2026-09-17-dream-rsi-search.md)

> Agent memory 相关线程已迁移至 `agent-memory/threads/`

### Thread Guidelines

`threads/` 记录对话形成的研究判断、benchmark 选择、实验路线、概念澄清、paper positioning / novelty 风险，以及暂时不值得升级为独立 area 的想法。单篇参考资料的正式笔记存入 `assets/<slug>/note.md`；只有一句待办或没有后续研究价值的聊天不单建线程。

文件名采用 `YYYY-MM-DD-topic-slug.md`，slug 使用稳定小写短语并聚焦一个线程；同一主题继续推进时优先更新原页。推荐内容包括 `Context`、`Key Judgments`、`Definitions / Clarifications`、`References / Evidence`、`Benchmarks / Papers Mentioned` 和 `Next Steps`。

关键判断需尽量带本地文献锚点，优先链接 `assets/<slug>/note.md` 或相关线程。尤其是已有工作、benchmark 有效性或局限、venue framing 等判断，应说明对应参考。论文尚未归档时，先标记“待 ingest”，再按 llmwiki skill 的 `scaffold-template.md` 补齐正式笔记；线程虽非正式 survey，也应避免大段无出处的 literature claims。

## Paper Directory

### Retrieval-Augmented Generation And Retrieval Reasoning

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

### Retrieval Optimization And Search Systems

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
| [LLM Test-Time Compute via Search Survey](assets/llm-inference-via-search-survey-2025/note.md) | 2025 | TMLR | Test-time search systems survey | `processed` |
| [Personalize Before Retrieve](assets/personalize-before-retrieve-2025/note.md) | 2025 | AAAI | Personalized pre-retrieval query expansion | `processed` |
| [Query Decomposition for RAG](assets/query-decomposition-as-bandit-2025/note.md) | 2025 | Arxiv | Bandit-based query decomposition | `processed` |
| Query Optimization Survey | 2024 | Arxiv | Query optimization survey | `processed` |
| [RAGChecker](assets/ragchecker-2024/note.md) | 2024 | Arxiv | Fine-grained RAG diagnosis framework | `processed` |
| [RAR-b](assets/rar-b-2024/note.md) | 2024 | Arxiv | Reasoning-as-retrieval benchmark | `processed` |
| [TART](assets/tart-2023/note.md) | 2023 | ACL Findings | Instruction-conditioned retrieval baseline | `processed` |

### Agent Architectures And Behaviors

| Paper | Year | Venue | Importance | Wiki Status |
|---|---:|---|---|---|
| [CoALA](assets/coala-2024/note.md) | 2024 | TMLR | Language-agent cognitive architecture | `processed` |
| Experiential Reflective Learning | 2026 | Arxiv | Experience-driven agent heuristics | `processed` |
| [Generative Agents](assets/generative-agents-2023/note.md) | 2023 | UIST | Believable social-agent simulation | `processed` |
| [ReAct](assets/react-2022/note.md) | 2022 | ICLR | Reasoning-and-acting agent prompting | `processed` |

### AI Data Systems

| Paper | Year | Venue | Importance | Wiki Status |
|---|---:|---|---|---|
| [LOTUS](assets/lotus-2025/note.md) | 2024 | Arxiv | Declarative semantic operator system | `processed` |
| [Palimpzest](assets/palimpzest-2024/note.md) | 2024 | Arxiv | Declarative AI workload optimizer | `processed` |

### Code Retrieval And Search Benchmarks

| Paper | Year | Venue | Importance | Wiki Status |
|---|---:|---|---|---|
| [Agentless](threads/unread/agentless-2024.md) | 2024 | Arxiv | Hierarchical code localization pipeline | `queued` |
| [CodeSearchNet](threads/unread/codesearchnet-2019.md) | 2019 | Arxiv | Multilingual code search benchmark | `queued` |
| [CoIR](threads/unread/coir-2024.md) | 2024 | Arxiv | Comprehensive code retrieval benchmark | `queued` |
| [SWE-bench](threads/unread/swebench-2024.md) | 2024 | ICLR | Real-world code issue benchmark | `queued` |

### Coding Agent Systems And Evaluation

| Paper | Year | Venue | Importance | Wiki Status |
|---|---:|---|---|---|
| [Claude Code Lead Source Collection](assets/claude-code-lead-source-2026/note.md) | 2026 | Repo | Claude Code source meta-collection | `stable` |
| [CursorBench](assets/cursorbench-2026/note.md) | 2026 | Blog | Real-session coding benchmark design | `processed` |

### Long-Context Adaptation And Test-Time Training

| Paper                                             | Year | Venue | Importance                          | Wiki Status |
| ------------------------------------------------- | ---: | ----- | ----------------------------------- | ----------- |
| [In-Place TTT](assets/in-place-ttt-2026/note.md) | 2026 | ICLR  | Fast-weight long-context adaptation | `processed` |

### Self-Improving Agents and Harness Optimization

探索策略、agent harness 与经验学习形成一个小型关联组，暂保留在 misc；已有历史资产不迁移。

| Paper | Year | 改进对象 | Wiki Status |
|---|---:|---|---|
| [[assets/dream-rsi-2026/note|Dream-RSI]] | 2026 | 历史树回放优化 exploration-policy code；Google / DeepMind 等，arXiv v1 2026-09-14 | `processed` |
| [[assets/meta-harness/note|Meta-Harness]] | 2026 | 完整执行历史驱动 harness 代码搜索 | existing note |
| Experiential Reflective Learning | 2026 | 经验提炼与检索 heuristics | `processed` |

检索记录：[[threads/2026-09-17-dream-rsi-search]]。

- 2026-09-22：LOTUS 补充官方代码静态核查及 [[research/agent-memory/threads/jev-related-work|与 UtilityQwen / SCARLet / OptiSet 的对照]]。

## Migration Archive Gaps

The following historical targets are absent in the current working tree (including previously deleted archives). Their labels and research discussion are retained as plain text; migration did not restore deleted material:

- `assets/erl-2026/index`
- `assets/erl-2026/index.md`
- `assets/fair-rag-2025/index.md`
- `assets/query-optimization-survey-2024/index.md`
- `assets/rag-fusion-2023/index.md`

## Reference Archive Catalog

Each citation is reachable here. `note.md` preserves actual historical reading; the four unread seeds are held in `threads/unread/`. Metadata snapshots in citations are historical provenance, not current asset availability.

- `agentless-2024`: [citation](assets/agentless-2024/citation.bib) · [unread seed](threads/unread/agentless-2024.md)
- `autobool-2026`: [citation](assets/autobool-2026/citation.bib) · [note](assets/autobool-2026/note.md)
- `beir-2021`: [citation](assets/beir-2021/citation.bib) · [note](assets/beir-2021/note.md)
- `birco-2024`: [citation](assets/birco-2024/citation.bib) · [note](assets/birco-2024/note.md)
- `bright-2025`: [citation](assets/bright-2025/citation.bib) · [note](assets/bright-2025/note.md)
- `claude-code-lead-source-2026`: [citation](assets/claude-code-lead-source-2026/citation.bib) · [note](assets/claude-code-lead-source-2026/note.md)
- `coala-2024`: [citation](assets/coala-2024/citation.bib) · [note](assets/coala-2024/note.md)
- `codesearchnet-2019`: [citation](assets/codesearchnet-2019/citation.bib) · [unread seed](threads/unread/codesearchnet-2019.md)
- `coir-2024`: [citation](assets/coir-2024/citation.bib) · [unread seed](threads/unread/coir-2024.md)
- `coral-2024`: [citation](assets/coral-2024/citation.bib) · [note](assets/coral-2024/note.md)
- `cursorbench-2026`: [citation](assets/cursorbench-2026/citation.bib) · [note](assets/cursorbench-2026/note.md)
- `dream-rsi-2026`: [citation](assets/dream-rsi-2026/citation.bib) · [note](assets/dream-rsi-2026/note.md)
- `dsp-2022`: [citation](assets/dsp-2022/citation.bib) · [note](assets/dsp-2022/note.md)
- `evomaster-2025`: [citation](assets/evomaster-2025/citation.bib) · [note](assets/evomaster-2025/note.md)
- `followir-2025`: [citation](assets/followir-2025/citation.bib) · [note](assets/followir-2025/note.md)
- `generative-agents-2023`: [citation](assets/generative-agents-2023/citation.bib) · [note](assets/generative-agents-2023/note.md)
- `hipporag-2024`: [citation](assets/hipporag-2024/citation.bib) · [note](assets/hipporag-2024/note.md)
- `hoprag-2025`: [citation](assets/hoprag-2025/citation.bib) · [note](assets/hoprag-2025/note.md)
- `in-place-ttt-2026`: [citation](assets/in-place-ttt-2026/citation.bib) · [note](assets/in-place-ttt-2026/note.md)
- `inpars-2022`: [citation](assets/inpars-2022/citation.bib) · [note](assets/inpars-2022/note.md)
- `inpars-v2-2023`: [citation](assets/inpars-v2-2023/citation.bib) · [note](assets/inpars-v2-2023/note.md)
- `ircot-2023`: [citation](assets/ircot-2023/citation.bib) · [note](assets/ircot-2023/note.md)
- `iter-retgen-2023`: [citation](assets/iter-retgen-2023/citation.bib) · [note](assets/iter-retgen-2023/note.md)
- `llm-inference-via-search-survey-2025`: [citation](assets/llm-inference-via-search-survey-2025/citation.bib) · [note](assets/llm-inference-via-search-survey-2025/note.md)
- `llm-reranking-survey-2025`: [citation](assets/llm-reranking-survey-2025/citation.bib) · [note](assets/llm-reranking-survey-2025/note.md)
- `lotus-2025`: [citation](assets/lotus-2025/citation.bib) · [note](assets/lotus-2025/note.md)
- `memorag-2025`: [citation](assets/memorag-2025/citation.bib) · [note](assets/memorag-2025/note.md)
- `memrl-2025`: [citation](assets/memrl-2025/citation.bib) · [note](assets/memrl-2025/note.md)
- `meta-harness`: [citation](assets/meta-harness/citation.bib) · [note](assets/meta-harness/note.md)
- `mintlify-chromafs-2026`: [citation](assets/mintlify-chromafs-2026/citation.bib) · [note](assets/mintlify-chromafs-2026/note.md)
- `multi-turn-conversational-rag-2026`: [citation](assets/multi-turn-conversational-rag-2026/citation.bib) · [note](assets/multi-turn-conversational-rag-2026/note.md)
- `palimpzest-2024`: [citation](assets/palimpzest-2024/citation.bib) · [note](assets/palimpzest-2024/note.md)
- `personalize-before-retrieve-2025`: [citation](assets/personalize-before-retrieve-2025/citation.bib) · [note](assets/personalize-before-retrieve-2025/note.md)
- `prism-2025`: [citation](assets/prism-2025/citation.bib) · [note](assets/prism-2025/note.md)
- `query-decomposition-as-bandit-2025`: [citation](assets/query-decomposition-as-bandit-2025/citation.bib) · [note](assets/query-decomposition-as-bandit-2025/note.md)
- `ragchecker-2024`: [citation](assets/ragchecker-2024/citation.bib) · [note](assets/ragchecker-2024/note.md)
- `rar-b-2024`: [citation](assets/rar-b-2024/citation.bib) · [note](assets/rar-b-2024/note.md)
- `react-2022`: [citation](assets/react-2022/citation.bib) · [note](assets/react-2022/note.md)
- `rlm-2026`: [citation](assets/rlm-2026/citation.bib) · [note](assets/rlm-2026/note.md)
- `ruler-2024`: [citation](assets/ruler-2024/citation.bib) · [note](assets/ruler-2024/note.md)
- `scimaster-xmaster-2025`: [citation](assets/scimaster-xmaster-2025/citation.bib) · [note](assets/scimaster-xmaster-2025/note.md)
- `self-rag-2024`: [citation](assets/self-rag-2024/citation.bib) · [note](assets/self-rag-2024/note.md)
- `swebench-2024`: [citation](assets/swebench-2024/citation.bib) · [unread seed](threads/unread/swebench-2024.md)
- `tart-2023`: [citation](assets/tart-2023/citation.bib) · [note](assets/tart-2023/note.md)
- `think-on-graph-2-2025`: [citation](assets/think-on-graph-2-2025/citation.bib) · [note](assets/think-on-graph-2-2025/note.md)

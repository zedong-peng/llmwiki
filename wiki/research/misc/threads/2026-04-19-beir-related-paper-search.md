---
title: BEIR Related Paper Search
domain: research
area: misc
type: note
status: active
updated: 2026-04-19
tags: [beir, retrieval, benchmark, literature-search]
---

# BEIR Related Paper Search

## Context

快速整理一组和 [[../papers/beir-2021/index|BEIR]] 强相关、值得优先阅读的论文，面向“想看 benchmark 本体、后续提升路线、以及 embedding 方向代表作”的需求。

## Key Judgments

- 如果只读一篇，先读原始 benchmark 论文：BEIR 定义了 zero-shot heterogeneous IR evaluation 的基本讨论框架。
- 如果关心 “BEIR 上怎么继续提分”，最直接的后续线索是两类：
  - 用 LLM 生成训练数据或 query-document pairs，比如 InPars / InPars-v2。
  - 改进 embedding / first-stage retrieval / reranking，比如 E5、SPLADE、RankT5。
- 如果按 [[../papers/bright-2025/index|BRIGHT]] 的 TeX `related work` 来重新收窄范围，那么比起继续堆更多 embedding 模型，更值得补的是几类 “benchmark 扩展” 论文：
  - complex-objective retrieval：BIRCO
  - reasoning-as-retrieval：RAR-b
  - instruction-following retrieval：TART / FollowIR / INSTRUCTIR
  - long-context retrieval：LoCo / LongEmbed
- 需要区分三类论文：
  - benchmark paper：定义问题和评测协议。
  - method paper：在 BEIR 上报告改进。
  - leaderboard / model-card claim：给出分数，但不一定是统一可复现的 benchmark paper。

## BRIGHT TeX Re-read

- 我重新读了 `bright-2025/source/extracted/texts/related_works.tex` 和 appendix 里的 `Comparison to RAR-b`。
- 按 BRIGHT 作者自己的 framing：
  - **BEIR** 是“广覆盖 heterogeneous benchmark”，但相关文档与 query 往往仍有较高 semantic overlap。
  - **BIRCO** 是最接近 BRIGHT 的 complex-objective benchmark，但作者认为它更偏 LLM reranking，且候选池较小。
  - **RAR-b** 也是 reasoning-intensive retrieval，但更像“把选择题答案改造成 retrieval”，不是现实文档检索。
  - instruction-following retrieval 和 long-context retrieval 被作者视为相邻扩展方向，而不是和 BRIGHT 同一问题。
- 因此，如果问题是“除了 BEIR 之外，还该读哪些 benchmark paper”，最应该补的是 **BIRCO + RAR-b + instruction retrieval + long-context retrieval** 这四组。

## Papers Mentioned

### 1. BEIR benchmark 本体

- **BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models** (2021)
  - 作用：benchmark 定义论文。
  - 为什么读：理解 18 个数据集、zero-shot 设定、BM25 强基线、late interaction / reranking 的总体结论。
  - 链接：
    - OpenReview: https://openreview.net/forum?id=wCu6T5xFjeJ
    - arXiv: https://arxiv.org/abs/2104.08663

### 2. 用 LLM 造检索训练数据

- **InPars: Data Augmentation for Information Retrieval using Large Language Models** (2022)
  - 作用：较早把 LLM 用到 IR 数据生成里的代表作。
  - 为什么读：核心思路是给文档生成合成 query，再训练 retriever / reranker；它是后面 InPars-v2 的直接前身。
  - 链接：
    - arXiv: https://arxiv.org/abs/2202.05144

- **InPars-v2: Large Language Models as Efficient Dataset Generators for Information Retrieval** (2023)
  - 作用：BEIR 提分路线里很关键的一篇。
  - 为什么读：论文明确把 open-source LLM + reranker selection 结合起来，并报告了新的 BEIR SOTA。
  - 链接：
    - arXiv: https://arxiv.org/abs/2301.01820

### 3. Embedding / retrieval 代表方向

- **Text Embeddings by Weakly-Supervised Contrastive Pre-training** (E5, 2022)
  - 作用：通用 embedding 方向的代表作。
  - 为什么读：论文直接把自己放到 BEIR 上评估，并强调 zero-shot 下首次稳定超过强 BM25 baseline 的 embedding 路线之一。
  - 链接：
    - arXiv: https://arxiv.org/abs/2212.03533

- **Improving Text Embeddings with Large Language Models** (2024)
  - 作用：更新一代 embedding 论文。
  - 为什么读：论文直接声称在 BEIR 和 MTEB 上做到更强结果，代表 synthetic data + LLM supervision 的新路线。
  - 链接：
    - arXiv: https://arxiv.org/abs/2401.00368

### 4. Sparse retrieval / reranking 代表模块

- **SPLADE: Sparse Lexical and Expansion Model for First Stage Ranking** (2021)
  - 作用：稀疏检索代表作。
  - 为什么读：BEIR 相关公开榜和后续系统里，SPLADE 经常作为 BM25 的更强 sparse 替代或 hybrid 组件出现。
  - 链接：
    - arXiv: https://arxiv.org/abs/2107.05720

- **RankT5: Fine-Tuning T5 for Text Ranking with Ranking Losses** (2022)
  - 作用：reranking 代表模块。
  - 为什么读：当前官方公开 BEIR 榜顶端系统里出现了 `RANKT5`，如果你想理解“为什么是 hybrid retrieve + strong reranker”，这篇值得读。
  - 链接：
    - arXiv: https://arxiv.org/abs/2210.10634

### 5. BRIGHT 视角下最该补的 benchmark 扩展

- **BIRCO: A Benchmark of Information Retrieval Tasks with Complex Objectives** (2024)
  - 作用：BRIGHT 在 related work 里点名的最近邻 benchmark。
  - 为什么读：如果你关心“query 目标本身就很复杂”而不是普通 relevance，这篇比继续读 embedding paper 更接近 BRIGHT 想解决的问题。
  - BRIGHT 的区分：BIRCO 更偏 LLM reranking setting，且每个 query 只有较小候选池。
  - 链接：
    - arXiv: https://arxiv.org/abs/2402.14151

- **RAR-b: Reasoning as Retrieval Benchmark** (2024)
  - 作用：另一篇 reasoning-intensive retrieval benchmark。
  - 为什么读：它测试的是“retriever 能否直接检索出 reasoning problem 的答案”。
  - BRIGHT appendix 的区分：RAR-b 更像把多选题答案集合改成 corpus，文档通常极短，更偏抽象 reasoning 测试，不是现实文档检索。
  - 链接：
    - arXiv: https://arxiv.org/abs/2404.06347

- **Task-aware Retrieval with Instructions** (TART / BERRI, 2023)
  - 作用：instruction-following retrieval 的代表作。
  - 为什么读：它不是 reasoning benchmark，但它是把 “query 之外再给 retrieval system 一个 intent/instruction” 做成系统路线的关键论文，而且论文直接报告了 BEIR / LOTTE zero-shot 提升。
  - 链接：
    - ACL Anthology: https://aclanthology.org/2023.findings-acl.225/

- **FollowIR: Evaluating and Teaching Information Retrieval Models to Follow Instructions** (2024/2025)
  - 作用：instruction-following retrieval benchmark。
  - 为什么读：如果你关心“retriever 是否真正理解长 instruction / narrative”，这篇比只看 BEIR 更贴近真实复杂检索需求。
  - 链接：
    - arXiv: https://arxiv.org/abs/2403.15246

- **INSTRUCTIR: A Benchmark for Instruction Following of Information Retrieval Models** (2024)
  - 作用：另一条 instruction retrieval benchmark 线。
  - 为什么读：可以和 FollowIR 对照看，理解 instruction retrieval 的 benchmark 构造差异。
  - 链接：
    - arXiv: https://arxiv.org/abs/2402.14334

- **Benchmarking and Building Long-Context Retrieval Models with LoCo and M2-BERT** (2024)
  - 作用：long-context retrieval benchmark + model。
  - 为什么读：BRIGHT 把它列为相邻 benchmark 扩展方向；如果你的 retrieval 场景中文档很长，这条线会比 BEIR 更 relevant。
  - 链接：
    - arXiv: https://arxiv.org/abs/2402.07440

- **LongEmbed: Extending Embedding Models for Long Context Retrieval** (2024)
  - 作用：long-context embedding retrieval 代表作。
  - 为什么读：和 LoCo 一起看，可以把 “benchmark” 和 “embedding window extension” 两件事分开。
  - 链接：
    - arXiv: https://arxiv.org/abs/2404.12096

## Reading Order

1. [[../papers/beir-2021/index|BEIR]]
2. BIRCO
3. RAR-b
4. Task-aware Retrieval with Instructions
5. FollowIR
6. InPars-v2
7. E5

## Definitions / Clarifications

- “BEIR 相关论文” 不等于 “BEIR 官方 leaderboard 上有提交的论文”。
- “在 BEIR 上表现好” 也不一定代表是同一种任务设定：
  - 有的是 zero-shot；
  - 有的是 synthetic-data-assisted training；
  - 有的是 reranking；
  - 有的是 first-stage embedding retrieval。
- 一个更清楚的分法是：
  - **BEIR 主线**：heterogeneous zero-shot retrieval benchmark
  - **BIRCO / FollowIR / INSTRUCTIR 主线**：复杂目标或 instruction-aware retrieval
  - **RAR-b / BRIGHT 主线**：reasoning-intensive retrieval
  - **LoCo / LongEmbed 主线**：long-context retrieval

## Next Steps

- 如果后续要补正式文献笔记，优先 ingest：
  - `birco-2024`
  - `rar-b-2024`
  - `followir-2025`
  - `inpars-v2`
  - `text-embeddings-by-weakly-supervised-contrastive-pre-training`
  - `improving-text-embeddings-with-large-language-models`

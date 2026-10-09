---
title: "Beyond Memory Leaderboards: Evaluating Scientific Memory as Budgeted Context Restoration"
updated: 2026-10-09
---

# Beyond Memory Leaderboards: Evaluating Scientific Memory as Budgeted Context Restoration

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文、参考文献、附录 A 均已读）。图 3–6 只有文字坐标残片，数值以正文和表格为准；表 4 的列标题（chars/score）在提取文本中错位，按正文数字对应。

## Summary

问题：现有 agent memory 基准（LongMemEval、LoCoMo、BEAM）面向对话，而科研 agent 需要从整篇论文中还原证据。作者把任务称为 context restoration，并构造两个全文科研记忆基准：Paim（81 篇，66 道审计后问题，主题为 agent memory）和 PTr（252 篇，98 题，主题为近期 Transformer 架构）。问题按 8 种题型 × 3 个难度层（L1 单段、L2 机制/比较、L3 跨论文综合）组织，rubric 逐条对到原文（§4）。

协议：8 个系统加无检索 base model，共用 gpt-4.1-mini（T=0）做外部合成，主 judge 为 Gemini 3.1 Pro。分两条轨道：native（各系统默认、不限量）和 budget-targeted（B ≈ 10K/30K/50K 字符，只改检索参数不重新 ingest）。三个系统加了 BM25 + RRF（k=60）的混合检索（§3、§6.1）。

主要结果：
- Paim native 上 Graphiti 以 8.04 居首（Simple RAG 7.22），但每个 query 返回约 2.55M 字符，因为它返回整篇论文的 episode 原文。去掉 episode 后（KG-only），30K 下降到 5.27，排在最后（Table 4）。
- Paim 30K：Simple RAG 7.25、Theoria 7.19、Mem0 6.97 差距在噪声内；Simple RAG 对 Hindsight、Cognee、Graphiti(KG) 的优势显著（Table 7）。
- PTr 上专有名词密集，BM25 提升最大：50K 时 Simple RAG +0.50、Mem0 +0.29、Theoria +0.20，三个混合方案为 9.22/9.24/9.21，两两差异的 bootstrap 区间均含 0（Table 5、7）。三者 ingest 成本悬殊（Simple RAG 约 1.5 分钟 embedding，Theoria 约 \$30 LLM 抽取加约 10 小时）。
- Judge 校准（§6.5）：Paim 上三个 judge 在 6 题子集上的排名 Spearman 为 0.90–0.97；PTr 上 DeepSeek V4 Pro 与 Gemini 逐 cell Pearson 0.93（n=946），前者系统性更严。112 对盲评人工 SxS 中，judge 与人类在 gap≥4 时 29/29 一致，0–2 分时 11/22；允许 1 分平局容差后整体一致率 77%。结论是 judge 分辨率约 1 分。
- 事后路由上界：PTr 50K 上逐题 oracle 路由 9.68（比最佳单一混合方案高 0.40），按难度层路由的方案没有收益（§8.1）。

另提出 Theoria（evidence + Leiden community + theory 三层，含 RAPTOR 树和类型化跨文档链接）及其消融 Prism，并给出基准、harness、原始输出已公开。

## Evidence and Limits

论点与证据的对应：
- "native 榜单被检索量主导"证据充分：Graphiti 的 episode 通道在 native 与 KG-only 之间的落差直接可见，且 Table 2 显示各系统检索量跨两个数量级。
- "Paim 上结构化记忆相对 chunk RAG 无优势"：只对顶部集群成立，30K 的差异区间全含 0；作者自己也限定为顶部集群。
- "BM25 是最大单一干预"：只在能干净接入 BM25 的三个系统、PTr 一个语料上测得；Theoria 的提升区间略含 0。"收敛到 0.03 内"是点估计，作者也说不能当排名。PTr 上的 BM25 机制解释（词汇独特）是推测，没有对照实验。
- Theoria 的结论比较克制：不赢混合榜单，且 /theories、/observe 两个最特别的接口完全没评。但"Theoria 在 PTr dense 下领先 Simple RAG 0.24"没有给 CI，且 80 篇子集（Table 6）上 Mem0 在 50K 反超 Theoria（8.72 vs 8.45）。作者是自己系统的评测方，需留意。
- 写 Table 6 与全库对比时，题目集合不同（48 题 vs 98 题），作者已说明混有难度因素。

设置与局限（多数为作者自述）：
- 题量小（66/98），簇内小于约 0.3 的差异视为噪声；每个 (系统, 预算) 只跑一次；PTr 问题只覆盖约 48% 的论文。
- 预算控制不精确：Hindsight 忽略 n（固定约 19K），Cognee 的 chunk 约 19K 导致只有 top_k=1/2/3，Graphiti 的 top_k 按通道计。
- 合成模型固定为 gpt-4.1-mini；公开 arXiv 论文使 base model 不是零信息基线（base 在 Paim 2.64、PTr 1.78）。
- 多个系统不是在其预期粒度下使用（Hindsight 喂整篇论文且拒收 3 篇，Mem0 6K 窗口，Graphiti 整篇一个 episode）。
- 人工 SxS 样本较小，rubric 审计由 agent 完成：Paim 初版 76 题中 37 题有缺陷并重写（Table 3），说明基准质量依赖审计，审计本身未经独立验证。
- 8.3 节记录了三个静默失效的工程坑（空 symlink、BM25 未启用、Qdrant 本地模式 OOM），可作为跑实验的检查清单。

## Open Questions

1. 一次性 QA 之外，持续更新的 research-agent 场景（论文自述的 /observe、/theories）下，结构化记忆是否有 RAG 没有的优势？文中未测。
2. BM25 带来的收敛是否只来自 PTr 的词汇特征？缺少第三个领域或词汇特征不同的语料来验证。
3. 逐题 oracle 路由的 0.4–0.8 分上界能否被真实信号实现？tier 路由已证明不行，是否有可用的逐题信号仍未知。

---
title: "Query Decomposition for RAG: Balancing Exploration-Exploitation"
updated: 2026-10-09
---

# Query Decomposition for RAG: Balancing Exploration-Exploitation

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文、参考文献、附录 A.1–A.4）。图 4、8–13 只有图注，曲线数值未提取；Table 2/4 的文本版式有错位，个别单元格（如 0.2512）可能是排版问题。BibTeX 中的标题（"Query Decomposition as Multi-Armed Bandit"）与论文实际标题不一致，以论文为准。

## Summary

- 问题：RAG 把复杂请求拆成 sub-queries 后，每个子查询各取固定数量文档，文档多、噪声大、占上下文。作者问：哪些子查询值得继续取，每个取多深（§1）。
- 方法：把每个 sub-query 当作 multi-armed bandit 的一个 arm，每次"拉臂"就是取该子查询排序列表里的下一篇文档，观察其相关性（人工或 LLM 判断）后更新 posterior，总预算 b 篇文档（§3.1–3.2）。核心是 Thompson sampling：离散情形用 Bernoulli + Beta 先验（Alg. 1），连续情形用 Gaussian（Alg. 2，奖励为检索得分）。
- 奖励设计（§3.3，Eq. 1，Table 1）：rank 信息（当前位置起 k 篇文档的平均相关性，k=3/4/5）、多样性（1 − 与已观察文档的最大余弦相似度归一化）、UCB 探索项（c→0）。最终为 "Bernoulli top-k UCB diversity"。
- 层级扩展（§3.4）：后验均值超过阈值 τ 且观察次数不少于 n 的子查询被展开，子节点继承父节点后验 Beta(λα, λβ)（"correlated MAB"）。
- 数据：NeuCLIR24（19 个请求，文档翻译成英文；每请求由 LLM 生成 16 个子查询，每个取 10 篇；检索器为 PLAID-X + LSR + Qwen retriever 的组合）与 ResearchyQuestions（BM25，过滤后 140 条，两级人工拆分）（§4）。每个设置重复 1000 次，拆分重复 10 次。
- 结果：
  - 文档选择（§5.1，Fig. 4，Table 3）：纯 exploit / 纯 explore 的 precision 在 NeuCLIR 分别为 0.57 / 0.55，Researchy 均为 0.14。Bernoulli top-k 类奖励在各预算下整体最好；ε-greedy 在 10–20% 预算最强；预算到 100% 时所有策略收敛。Table 3 中 α-nDCG@K=5 在 NeuCLIR24 上 Random 0.411、ε-greedy 0.500、Top-k UCB Div. 0.469。
  - 报告生成（§5.2，Table 2，Auto-ARGUE）：b=20%/30% 时，选出的子集在 citation support / nugget coverage / sentence support 上都略高于全量文档（0.788 / 0.461 / 0.780），如 Bernoulli k=4 在 b=20% 为 0.866 / 0.463 / 0.855。
  - 层级（§5.3，Table 4）：b=10% 时层级比串行高，如 Bernoulli top-5 由 0.303 升到 0.401。
  - Rank 信息检验（§5.4，Fig. 5）：用平均倒数排名做线性回归，少数请求斜率为负，即排序并不总与相关性一致。
  - Gaussian 奖励明显较差（Table 5，A.2），作者归因于排序得分噪声大。

## Evidence and Limits

- 摘要和引言的数字与正文对不上：摘要称 precision +35%、α-nDCG +15%；引言称 Bernoulli 比"顺着排序列表往下取"相对相关性估计高 17%，层级比单层 precision 高 30%；§5.3 给出 21.6% / 32.3% / 20.4%，Table 4 图注说 24%。这些百分比的基准和计算方式文中没交代，从表里也难复原。
- 奖励用的是真实相关性标注（人工或 LLM 判断），即 oracle 反馈，实际系统里每取一篇就要判断一次，这部分成本没有计入"效率"。结论里作者也只说"有二元相关性标签时"成立。
- 报告生成：Table 2 的差异很小，置信区间大面积重叠（如 nugget coverage 0.446–0.500 对 0.461），且随机选子集在 citation/sentence support 上与 bandit 策略相近（b=30% 时 Random 0.827 / 0.837）。图注称提升 6.0–9.9% 等，是相对"全量文档"的增益，并不能说明 bandit 优于随机。生成模型、提示和 Auto-ARGUE 所用评判模型文中未说明。
- 层级结果：Table 4 在 b=20% 时，top-k 策略层级反而略低（k=3：0.260 → 0.250；k=4：0.261 → 0.251），与结论"在所有奖励上一致提升"不符；增益只出现在 b=10%。τ、n、λ 通过 Bayesian 搜索在同一数据（Researchy）、同一 top-k=5 目标上选出，存在调参即评测的风险。
- 规模：NeuCLIR 只有 19 个请求，子查询由 LLM 重复生成 10 次，噪声由重复实验平均，但未给出显著性检验。Researchy 语料由所有相关文档拼成，并过滤掉相关文档不足 10% 的实例，会偏向较易的情形。
- 文中表述有笔误（"exploitation and exploitation-only"）；Bernoulli UCB 项在 c→0 下实际作用不明确；Eq. 1 把奖励用于 Alg. 1 的更新，而多样性乘积使奖励不再是 0/1，与 Beta-Bernoulli 更新的假设不完全一致。
- 作者自述的局限：奖励依赖检索器；预算效果依赖真实相关性分布；动态场景下子查询不预先给定，LLM 每次重生成会带来噪声。代码为匿名仓库链接（脚注 1）。

## Open Questions

- 在没有 oracle 相关性标签、只能用 LLM 判断或检索得分时，Bernoulli 优势还剩多少？判断本身的开销如何计入预算？
- 层级相关 bandit 的收益是否只在极小预算下成立，且是否来自调参（τ=0.77、λ=0.91、n=4）而非结构本身？
- 选出的文档子集带来的生成质量提升，相对随机子集是否显著？

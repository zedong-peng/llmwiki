---
title: "LLM-A*: Large Language Model Enhanced Incremental Heuristic Search on Path Planning"
updated: 2026-10-09
---

# LLM-A*: Large Language Model Enhanced Incremental Heuristic Search on Path Planning

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文、参考文献、附录 A–D）。Figure 1–4 只有图注和零散文字，图本身未见；Table 2–4 的 prompt 示例中 demonstrations 被省略。

## Summary

问题：A* 及其变体在地图变大时，扩展节点数和内存开销增长很快；LLM 能做全局的环境理解，但直接输出路径常常无效或不优（§1）。

方法：LLM-A*（§3.2，Algorithm 1）让 LLM 先根据起点、终点和障碍物生成一串 waypoint（TARGET list T）。T 必须包含起点和终点（缺则由算法补上），且 waypoint 不能落在障碍内（落入则被删除）。搜索过程与 A* 相同，不同之处有两点：f(s) = g(s) + h(s) + cost(t, s)，其中 t 是当前目标 waypoint；当扩展到的邻居等于 t 时，t 切换到 T 中的下一个，并重新计算 OPEN 表中所有状态的 f 值。LLM 只提供搜索方向，路径由 A* 的搜索产生，所以路径始终有效。论文测试了三种 prompt：5-shot、CoT（3-shot）、RePE（Recursive Path Evaluation，3-shot，逐点生成并评估）（§3.3）。

实验（§4）：100 张 50×30 的随机连续空间地图（横/纵障碍线段），每张 10 组起终点，共 1000 个样本；实际搜索在离散点和动作上进行。模型为 GPT-3.5-turbo 和 LLaMA3-8B（16bit）。指标是相对 A* 的操作数比、存储比、相对路径长度（均为几何平均），以及有效路径率。

主要结果（Table 1）：
- LLM-only 的有效路径率只有 7.8%–16.4%，路径长度为最优的 111%–184%。
- LLM-A* + LLaMA3 few-shot：操作 44.59%、存储 64.02%、路径长度 102.47%、有效率 100%。
- LLM-A* + GPT-3.5 few-shot：操作 57.39%、存储 74.96%、路径长度 102.44%。
- RePE 的资源节省最少（GPT-3.5 操作 85.47%，LLaMA3 64.08%），CoT 居中。
- Dynamic WA*（w=2，衰减 0.99）：操作 60.91%、存储 78.53%、路径长度 100.24%。作者称 LLM-A*（LLaMA3）在资源上优于它，但 GPT-3.5 的 CoT/RePE 并不优于它。
- 规模实验（Figure 3，环境放大 1–10 倍，LLaMA3 few-shot，10 次随机采样均值）：A* 的操作数和存储增长因子随规模快速上升，LLM-A* 接近线性。具体数值只在图中，文本里没有。

## Evidence and Limits

- 效率结论局限于一个自建的小型 benchmark：地图只有一种尺寸（50×30）、只由矩形/线段障碍构成，没有与已有 benchmark 对比，也没有报告方差、置信区间或随机种子数。
- 基线较弱：只有 A* 和一个 Dynamic WA*。没有与 JPS、Theta*、HPA* 等论文自己在 §2 列出的变体比较，也没有"随机/几何方法生成 waypoint"的对照，因此无法区分收益来自 LLM 的语义理解还是仅来自带 waypoint 的偏置搜索。
- "near linear"、"A* 指数增长"的说法只由 Figure 3 支持，没有拟合或数值表。A* 在网格上的增长本来就是多项式量级，"exponential" 的说法没有分析支撑。
- 最优性：附录 A 承认 f 中加入 cost(t, s) 使启发式不可采纳，不保证最优。Limitations 称"约 90% 的路径最优"，但正文没有给出对应的实验。Table 1 的路径长度比为 102%–103%。
- 开销缺失：效率只统计搜索的操作数和存储，LLM 调用的延迟、token 成本和 waypoint 被丢弃/修补的比例均未报告，也没有 LLM 调用后总耗时与 A* 的对比。
- 测试的 LLM 只有 GPT-3.5-turbo 和 LLaMA3-8B，作者自己指出没有试更多模型和更强的 prompt。LLaMA3-8B 的结果好于 GPT-3.5，原因没有分析。
- 论文标题带 "Incremental"，但方法本身并没有用到增量式启发搜索（如 LPA*）；文中仅在重新计算 OPEN 表 f 值处体现。
- 附录 D 的"几何平均大于 1 表示更好"与正文"比值越低越好"不一致。
- 未复现；代码仓库 https://github.com/SilinMeng0510/llm-astar 在论文文本中没有写出。

## Open Questions

1. 收益有多少来自 LLM 的语义判断，有多少只来自"任何合理的中间目标"？需要随机/规则 waypoint 的对照。
2. 在障碍更复杂、非线段形、不同尺寸或真正连续的环境中，waypoint 质量和有效率会怎样变化？考虑 LLM 调用开销后，总体收益是否仍成立？
3. 为什么 RePE 这类更细致的 prompt 反而节省更少？论文只给出了"LLM 空间推理有限"的猜测。

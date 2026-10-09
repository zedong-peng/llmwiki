---
title: "MemTrace: Probing What Final Accuracy Misses in Long-Term Memory"
updated: 2026-10-09
---

# MemTrace: Probing What Final Accuracy Misses in Long-Term Memory

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文、参考文献、附录 A–E，含 Table 1–20）。图为文本抽取，Figure 3/4/6/8/9 只能看到标签与少量数字；Table 12 之后个别引用（"??"）缺失；附录 E 部分段落与表格说明较零碎。

## Summary

- 问题：长期记忆基准通常按问题行或整段 episode 汇总准确率，同一事实的多个问题被当作独立样本，无法固定一个事实、观察它在条件变化下的表现（§1）。
- 方法：以 knowledge point（KP，关于用户的一条带类型事实）为测量单位。数据改造自 HaluMem-Medium，共 20 个用户、835 个 KP（静态 348、动态 213、偏好 74、conflict 干扰项 100、boundary 干扰项 100），展开为 5,677 个 base probe、15,422 个问题行、200,453 条打分回答（§3.1, Table 2, Table 6）。
- 三个受控维度（§3.2）：
  - memory age：每个用户 8 个按时间递增的 checkpoint（W1–W8），历史前缀逐步变长。
  - question type：Current / Historical / Trajectory（变化轨迹）。
  - evidence condition：证据存在 / 缺失（boundary，问未提及的事实）/ 被错误前提反驳（conflict）。
- 指标：Gist 准确率（二值）、Verbatim 完整度、Response type（正确 / 弃答 / 幻觉）。主评审 GPT-4o，Gemini-3-Flash 对 200 个 probe 复核（Gist κ=0.772，Response type κ=0.703，Table 13）。
- 评测 13 个配置、4 类范式（§4.1, Table 8）：长上下文 3 个（Qwen3.5-35B、Gemini-3-Flash、GPT-5-nano）；RAG 4 个（BM25、text-emb-3-small、Qwen3-Emb、HippoRAG-v2）；外部记忆 4 个（Mem0、SimpleMem、REMem、AMem）；agentic 记忆 2 个（MIRIX、Mem-T）。除长上下文外，统一用 gpt-4o-mini 作答。
- 主要结果：
  - Fresh（W1–W2）到 Saturated（W7–W8）的 Gist 下降随类型而异（Table 3）。整体 Saturated 最高的是 HippoRAG-v2（36.5%）。Current/Historical 也是它领先（45.4% / 50.9%），Trajectory 则是 Mem-T 领先（19.8%）。
  - 长上下文模型 Trajectory 老化后崩塌：Qwen3.5-35B 从 49.0 降到 6.7，GPT-5-nano 从 38.4 降到 6.5。
  - 弃答不等于纠错（Table 4）：Mem0 / AMem / REMem 的 boundary 弃答为 99.3 / 97.4 / 94.0%，conflict Gist 只有 14.6 / 20.1 / 35.1%，失败多为弃答而非幻觉。
  - 失败归因（§4.4）：对 120 个难 probe 直接给 gold 证据（oracle），Gist 升到 80–85%，生产基线为 0–33.8%。用 text-emb-3-small 做 300-probe 回放：reach 缺失 7.0%，reached 但未解 73.3%，成功 19.7%（Table 12）。对 13 个系统，P(U=0|R=1) 为 69.2%–88.2%，oracle 后恢复到 80.4%–83.9%（Table 5）。作者据此得出结论：瓶颈是"证据使用"，不是存储或检索（约 10 倍）。

## Evidence and Limits

- 论点与证据的对应：
  - "相近的汇总准确率掩盖不同失败模式"有 Table 3/4 支撑，各系统在三种 question type 上排名不同。
  - Table 11 给出 Current/Historical 与 Trajectory 排名的 Spearman 相关：中位数 0.39–0.52，bootstrap 中 78–91% 低于 0.6。CI 较宽（如 [0.247, 0.747]），只能说排名相关性中等偏低。
  - 附录 Table 10/11 给出 bootstrap 95% CI，部分 boundary 单元格 CI 很宽（如 Qwen3.5-35B [2.3, 21.3]）。
- "证据使用 ≫ 检索"的约 10 倍结论证据较弱：
  - reach 只用单个 text-emb-3-small 检索器，且只判断是否命中 gold 所在的 session，不判断是否命中具体片段。
  - 样本 300 个 probe，来自作者选取的难例，不是全基准的随机抽样。
  - oracle 是开卷设定，直接给 gold 证据，不等同于现实中可检索到的证据形态。"reached 但未解"里混有证据片段不全、检索排序差、生成端不会用等多种原因，没有进一步拆分。
  - 作者在 Limitations 中承认该比例只是方向性结论，幅度依赖检索器。
- 比较的混杂因素：
  - 比较对象是整套端到端配置，不是孤立机制：长上下文用各自原生模型，其余共用 gpt-4o-mini，但 embedding 等组件各异。
  - 换答案模型影响很大：Gemini 作答时 conflict Gist，AMem 20.1→72.9，Mem0 14.6→59.8，HippoRAG-v2 反而 80.2→69.9（Table 18）；统一 prompt 下 HippoRAG-v2 conflict Gist 80.2→33.8（Table 16）。因此"弃答不等于纠错"在一定程度上取决于答案生成器和 prompt，跨范式排名只在配置层面成立。
  - MIRIX 换 gpt-4.1-mini 后总体 Gist 22.5→37.4（Table 15）；Mem-T 的训练语料 LoCoMo 与评测数据有 session 谱系重叠。
- 数据与评分：
  - 数据只来自 HaluMem-Medium 单一分布，20 个用户。
  - Table 7 显示改造草稿的时间锚点缺陷率为 38.74%、语义一致性缺陷为 10.24%，经人工修复后降到 1.42% 和 0.00%。
  - 评分依赖 LLM 判官，Response type 的 κ 为 0.703；Table 14 中 Trajectory/Dynamic 的判官分歧达 45.8%，而 Trajectory 正是核心结论所依赖的类型。
- Table 17 的 oracle 路由干预（tr+cr+ac）使 saturated trajectory 的 Gist 20.0→31.2，仅作"可行动性"示意，不是可部署方法。

## Open Questions

- 把"reached 但未解"进一步拆开：证据片段是否包含全部所需状态、排序是否合理、生成器是否忽略，各占多少？换更强的检索器后 10 倍的比例还成立吗？
- Trajectory 的低分有多少来自问题本身的评分难度（判官分歧最高）而非记忆系统的缺陷？在人工标注的子集上结论是否一致？
- 结论在 HaluMem 之外的数据分布和更长的真实对话上是否成立？生成器和 prompt 的敏感性（Table 16/18）使得"安全弃答 vs 纠正错误前提"的区分有多少属于系统本身的性质？

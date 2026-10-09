---
title: "A Simple Yet Strong Baseline for Long-Term Conversational Memory of LLM Agents"
updated: 2026-10-09
---

# A Simple Yet Strong Baseline for Long-Term Conversational Memory of LLM Agents

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文、参考文献、附录 A，共 12 页）。图 2–4 只有坐标轴数值标注，曲线本身无法读取；表格基本完整可读。

## Summary

问题：固定上下文窗口下，多 session 对话的长期记忆要么按大块检索而丢细节，要么压缩成摘要/事实而有损，要么拆成三元组而碎片化（§1）。

方法：受 neo-Davidsonian 事件语义启发，用 LLM 把每个 session 改写成 enriched EDU（自包含的短事件陈述，实体归一化、带时间，附源 turn 编号和时间戳）。再对每个 EDU 抽取事件类型与 role-argument，建异构图：session 节点、EDU 节点、argument 节点；边为 session-EDU、EDU-arg，以及余弦相似度 ≥ 0.9 的 argument 同义边（§3.2）。

两个检索变体（§3.3、§3.4）：
- EMem：dense 检索 top-30 EDU，再由偏召回的 LLM filter 选出相关项，直接交给 QA 模型。
- EMem-G：另对 query 做 LLM mention 检测，检索 argument 节点并同样过滤，以相似度作种子权重跑 Personalized PageRank（沿用 HippoRAG 2 默认参数），取 top-10 EDU。

结果（LLM judge 为 gpt-4o-mini，跑三次；baseline 数字取自 Nemori 论文）：
- LoCoMo（Table 2）：gpt-4o-mini 下总体 LLM score，Nemori 0.744，EMem 与 EMem-G 均为 0.780，full-context 0.723。gpt-4.1-mini 下 EMem-G 0.853，EMem 0.842，Nemori 0.794，full-context 0.806。F1 上 Nemori 更高（0.495 对 0.487/0.483）。
- LongMemEvalS（Table 3）：gpt-4o-mini 平均 EMem-G 77.9%，EMem 76.0%，Nemori 64.2%，full-context 55.0%；gpt-4.1-mini 分别为 84.9%、83.0%、74.6%、65.6%。
- QA 上下文很短：LoCoMo 上 EMem 平均约 738 token，EMem-G 约 988，Nemori 2,745，full-context 23,653。LongMemEvalS 上 EMem 为 0.6K–2.5K，full-context 为 101K。
- Ablation（Table 5、6）：去掉 EDU filter，LoCoMo 总体由 0.780 降到 0.733（EMem-G）、0.748（EMem）；LongMemEvalS 由 77.9% 降到 73.1%。去掉 QA 的 zero-shot CoT，LongMemEvalS 降到 73.4%（EMem-G）和 70.6%（EMem）。去掉图与 PPR（即 EMem）降 1.9 点。

## Evidence and Limits

- 设置：embedding 为 text-embedding-3-small，骨干为 gpt-4o-mini 和 gpt-4.1-mini；LoCoMo 共 1,520 题（去掉 adversarial 类），LongMemEvalS 共 470 题。评测框架与 baseline（FullContext、LangMem、Mem0、RAG-4096、Zep、Nemori）沿用 Nemori。文中未写硬件和 EDU 抽取的成本。
- 文中的论断大体有表支撑，但有几处过强。"EDU 表示 + 召回型 filter 是主要增益来源"：ablation 只拆了 filter、CoT、图，没有把 EDU 与 chunk、triple 或摘要在相同检索与 filter 条件下对比，因此"事件语义优于三元组"没有被直接检验。
- 表 2 中 baseline 数字来自他人论文，EMem 系统另用相同 judge 复测，未说明 judge prompt 与 baseline 原始运行是否完全一致。LoCoMo 只有 10 段对话；±值只反映 judge 的三次重复，不含数据或抽取的方差，EMem 与 EMem-G 在 gpt-4o-mini 下总体相同。
- LongMemEvalS 需要数据集专用处理（附录 A）：对助手长回复额外抽"结构化 chunk"加 2–3 句摘要，需多一次 LLM 调用，并只在 QA 时展开原文。因此"非压缩"之说在此处并不完全成立。
- 作者承认的局限：single-session-preference 明显弱（EMem-G 32.2%，Nemori 46.7%；gpt-4.1-mini 下 50% 对 86.7%），因 EDU 抽取偏向事实性事件，风格与态度信息被丢；argument 抽取不够归一化，图较稀疏（argument 度约 1–2）；LongMemEvalS 中同 session 的相似 EDU 较多，需要更强的 embedding、reranker 或 filter。
- 超参图（图 2–4）显示 Ke 在 20–40 间较平，QA top-K 约 10–15 饱和。Ablation 只用 gpt-4o-mini。

## Open Questions

- 增益里有多少来自 EDU 的信息改写本身，多少来自召回型 filter 与 CoT？缺少同条件下对 triple、摘要、原始 turn 的对照。
- 图传播只带来 1–2 点提升，且在 multi-session 上 EMem 反而更好；argument 抽取更规整后图是否会明显有用，文中仅作推测。
- 离线 EDU 抽取（每 session 多次 LLM 调用）的成本与建图延迟未报告，而结论强调的是 QA 阶段的上下文长度；信息被"改写"后的幻觉或推断错误率也没有评估。

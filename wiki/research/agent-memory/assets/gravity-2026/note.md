---
title: "GRAVITY: Architecture-Agnostic Structured Anchoring for Long-Horizon Conversational Memory"
updated: 2026-10-09
---

# GRAVITY: Architecture-Agnostic Structured Anchoring for Long-Horizon Conversational Memory

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文、参考文献、附录 A.1–A.6，含 prompt 模板）。图 2–4 只有文本提取的残片，主要靠正文和表格数字；表格均可读。

## Summary

问题：现有 memory 系统（Mem0、ZEP、A-Mem、LightMem 等）即使内部有结构，送给生成器的仍是平铺的检索片段，关系、时间、主题联系要模型自己重建。作者称检索与生成之间存在 "reasoning gap"。oracle 实验里，ground-truth 证据全在时准确率 84.9%，证据被干扰项稀释到 60 条里随机分布时降到 75.6%（§5.1, Table 10）。

方法：GRAVITY 是外挂模块，不改 host，只改 generation prompt。
- 构建阶段（§3.2）：直接对原始 utterance 用 GPT-4o-mini 抽取三类 anchor。Entity（属性带置信度、关系、时间线、共现，离线整合）；Event（Who/What/When/Where/Outcome 元组，When 含绝对/相对/时长/周期，按参与者或关键词启发式连成 trace，相似度 >0.6 去重）；Topic（跨 session 话题归并，每个话题生成摘要）。
- 推理阶段（§3.3）：各模块先原生匹配，再按 query 与条目文本的 embedding 余弦重排，每模块取 top-5。含时间表达的 query 为 Event 预留名额（temporal preservation）。另由 anchor 生成最多 9 条扩展 query，替换 host 检索结果中相似度最低的 9 条。anchor 作为三个文本块追加到 prompt，并要求以 host 检索的记忆为主。

结果（Table 1，GPT-4o-mini 作生成器与评判）：五个 host 在 LongMemEval 和 LoCoMo 上都提升，平均 LME-Micro 56.2→65.4，LME-Macro 55.9→66.0，LoCoMo 59.3→66.8。最强 host LightMem 提升最小（+3.8/+3.8/+5.7），最弱的 ZEP、Mem0 在 LME 上提升 11–13 点。
- 消融（Table 2, 7, 8，host 为 LightMem）：同位置注入无结构摘要仅 LoCoMo +1.3，三 anchor 全开 +5.7。去掉 rerank 掉得最多（LoCoMo −3.4，LME-Micro 回到基线），去掉扩展 query 影响小（LME-Micro 反而 73.0 > 72.6）。
- 成本（Table 3, 4, 9）：每段对话构建约 193K token / 557 s（LoCoMo），anchor 一次构建各 host 共用；推理每 query 多约 0.3–0.9 s、约 2K token（ZEP、LiCoMemory 更高，LME 上 LiCoMemory +4.22 s）。并行抽取构建时间减半；三合一单次调用 token 降约 75%，平均准确率降约 1.6 点；Qwen-3-8B 本地抽取 token 更多（286K）但准确率接近。
- 误差分析（§5.2, Table 11–12）：LoCoMo 上 gain/loss 约 2.2:1；各 host 被修正的题集重合很低（Jaccard 0.09–0.17）。50 个 loss 的人工归类：过度摘要约 38%、时间槽错误约 32%、实体混淆约 20%、话题过度概括约 10%。

## Evidence and Limits

- 设置：5 个 host 用默认配置；LoCoMo 1,540 题（去掉对抗类），LME 500 题；检索条数固定 60/20；所有 LLM 与评判均为 GPT-4o-mini；每个配置仅一次结果，未报方差、种子或置信区间。
- 公平性：host 检索条数固定，但 anchor 上下文额外多约 2K token（LoCoMo），而 +Sum 对照没有扩展 query，且注入量是否真的等同只由作者声明（§4.3），未给出具体 token 数。"结构而非文本量" 的结论依赖这一个对照，且 +Sum 只在 LightMem 一个 host 上做。
- 回归分析（§5.1, A.3.1）：15 个点来自 5 个 host x 3 个指标，LME-Micro 与 Macro 高度相关，并非独立样本；p<0.0001 偏乐观。LoCoMo 单独拟合 R²=0.48, p=0.19，不显著。Poisson CDF 模型是事后假设；"K 与 host 无关" 由 F 检验 p=0.62 支持，但这是未拒绝而非证明，样本仅 15 点。文中把小增益归为 "天花板效应" 而非方法局限，这个解释同样无法与"重叠覆盖"解释区分开。
- Oracle 实验（Table 10）只用 A-Mem 一个 host。有 oracle 证据时 anchor 略降（84.9→83.9），Oracle Front +2.0，Random +2.9；时间类题 Random 下反降（50.0→47.9）。Intro 把 80.9 称为 oracle 准确率、同时又称 84.9，表述不一致（80.9 对应 Oracle Front）。
- 数字小不一致：Table 1 与 Table 6/11 中个别 delta 差 0.1–0.2；摘要的 "7.5–10.1%" 实为绝对百分点而非相对提升。
- 自述局限：build 阶段 LLM 抽取会丢细节或混淆（loss 分析），anchor 被生成器优先于原文证据；有 65 题在至少一个 baseline 对、加 anchor 后五个 host 全错；附录 A.6 提到隐私和错误固化风险。
- 数据集偏小：LoCoMo 仅 10 段对话，多数 anchor 数量和 batch 超参（B=60/150）只在 conv-42 一段上做敏感性分析（A.3.3）。未在 LoCoMo/LME 之外验证，也没有与直接复用 Mem0/ZEP 图结构作为 prompt 的对比。
- 论文称 "first fully portable" 模块，未与同类 prompt 层结构注入（如把 host 自带图结构序列化进 prompt）直接比较。

## Open Questions

- 增益是否来自 anchor 抽取用了对全量对话的一次完整扫描（等于 host 之外多一遍全局信息），而不单是 "结构"？缺少把同一信息以半结构化或检索版本注入的对照。
- 扩展 query 在 LME 上无益甚至略负，在 LoCoMo 上略正，其作用是否依赖检索窗口大小？
- 换更强的生成/抽取模型（GPT-4o-mini 之外）后，增益是否因模型自身能整合碎片而缩小？论文只报告了单一骨干。

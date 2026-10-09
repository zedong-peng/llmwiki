---
title: "MEMAUDIT: An Exact Package-Oracle Evaluation Protocol for Budgeted Long-Term LLM Memory Writing"
updated: 2026-10-09
---

# MEMAUDIT: An Exact Package-Oracle Evaluation Protocol for Budgeted Long-Term LLM Memory Writing

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文 §1–8、参考文献、附录 A–E）。图以文字提取形式出现，数值多可读；Figure 6/7 的柱状数值残缺，未采用。arXiv:2605.02199v1，Purdue。

## Summary

问题：长期记忆 agent 要在未知未来查询之前把经验流压缩成持久记忆。现有评测只看最终 QA 准确率，写入、检索、reader 三层混在一起，无法定位错误出在哪（§1）。

方法：提出 MemAudit "package"，固定经验流、每条经验的候选表示（raw、fact、summary、graph edge、tombstone、compound update 等）、存储成本、语义证据单元、未来查询需求和预算 B（§2）。可行集为一个 knapsack 约束加一个 partition matroid（每条经验至多选一种表示）。目标函数是 concave-over-modular 覆盖 F(X)=Σ w_r h_r(Σ a_ur)，默认 h=min(1,z)，Theorem 1 证明其单调次模。"过期事实"用正向的 validity-state 证据单元（失效、取代、删除、弃答）表示，而非负效用。用 branch-and-bound 求精确 OPT，并用 MILP 交叉验证（Table 1：1,200 个实例目标值全部一致）。外部系统（Mem0、A-Mem、Letta）的导出记忆并入 union package 计算 ρ_union，另给"upper-pruned"上界以区分抽取质量与预算内选择质量。另有一个有精确边际的参考写入器 GVT，给出 1/4 级别的 insertion-only 保证（Theorem 5，需 c_u ≤ B/2）。

结果：
- 精确小规模包（500 seeds，B=2,4,8,16，§4，Fig. 2）：density-only 在 B=2,4,8 不覆盖任何 invalidation 单元，仅达 OPT 的 0.264–0.361；去掉 tombstone/compound-update 后的精确 OPT 为全 OPT 的 0.523/0.654/0.689/0.815。
- 压力测试（B=6，§5，Fig. 3）：no-tombstone OPT 在 update_chain 为 0.513、temporal_interval 为 0.700；density-only 在 base/update/temporal 为 0.398/0.730/0.662。
- 自然包：Natural-200 由 Gemini Flash-Lite 构造（约 $0.907），严格裁决后保留 87 例（13 例因歧义剔除，Table 2）。两位人工标注者在 1,975 个单元格上 κ=0.831；人工–Gemini κ=0.863；用人工标签重打分平均比值变化 0.035，排序不变（Table 3）。
- 外部系统（B=100，Table 4）：union 比值 Letta salience 0.734、Mem0 salience 0.427、Mem0 upper 0.886、A-Mem metadata 0.180、A-Mem 完整笔记 0（完整笔记平均最小成本 1768 词，装不进预算）。解读为 Mem0 的瓶颈在预算内选择，不在抽取。非 oracle 的 Estimated-GVT 在 B=30/60/100 达 OPT 的 0.53/0.68/0.83。

## Evidence and Limits

论文声称的是"写入层诊断"，而非替代端到端 QA；这个定位与证据基本相称。分数完全是 package 条件下的：候选表、成本模型、证据单元 schema 都由 benchmark 作者定义，OPT 只是该候选集内的最优，不是"所有可能记忆"的最优（§1, §8）。

设置细节：
- 小规模包为合成数据，由隐藏事件图生成，候选类型和 tombstone 的价值是设计者给定的，"去掉 tombstone 后 OPT 下降"在一定程度上由构造决定，不是经验发现。
- 自然包是 LongMemEval 风格的 support slice，候选记忆、证据单元和覆盖标签都由 Gemini Flash-Lite/Flash 生成并裁决，仅 87 例；人工审核覆盖所有模型正例单元格加 20% 抽样的模型零例单元格，标注者为熟悉 schema 的项目成员（附录 B.3）。
- Sonnet 4.5 交叉审计的单元格一致性较低（κ 约 0.48–0.65），排序保持，作者仅作为 prompt/模型敏感性压力测试。
- 外部系统分数是事后按预算剪枝的诊断，三个系统并非按该预算和目标原生运行；salience 剪枝的启发式也由作者定义；upper-pruned 使用隐藏覆盖，仅为分析上界。
- 成本用词数等价；字节开销规则（8+⌈bytes/24⌉）和 k=2 放宽下排序稳定，OPT 变化 1.3–6.0%（Table 5, 6）。
- 附录 D 的 LongMemEval-S 迁移实验没有精确 OPT，论文自己说只是证据使用和检索紧凑性的诊断，不主张准确率提升；文本中无具体数值可核对。
- Mem0 的 upper-pruned package ratio 超过 1（1.041），说明 package 分母不含其导出，需靠 union 分母才可比，也说明比值随被评系统改变分母。
- Theorem 5 需要精确边际和 c_u ≤ B/2，只是校准结果。证明里把定理称作 "Theorem 4"（实为 Proposition 4），属小的排版瑕疵。

## Open Questions

- 覆盖矩阵 a_ur 和证据单元由模型生成，F 与下游 QA 是否单调相关，文中没有直接证据（作者明确承认 F 只是 surrogate）。
- 87 例的 support slice 去掉了检索干扰，写入层分数在完整长历史、更大规模下是否仍能区分系统，论文未验证。
- 因分母含被评系统自己的导出，union 比值能否在不同系统之间公平比较，尤其当某系统生成大量冗余候选时，文中未讨论。

（论文正文未给出官方代码地址，只说 artifact 随论文发布。）

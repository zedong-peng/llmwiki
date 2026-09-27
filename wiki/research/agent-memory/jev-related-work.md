---
title: Jev 相关工作：LOTUS、UtilityQwen、SCARLet、OptiSet
domain: research
area: agent-memory
type: comparison
status: active
updated: '2026-09-22'
tags:
- rag
- evidence-utility
- related-work
---

# Jev 相关工作：LOTUS、UtilityQwen、SCARLet、OptiSet

这四项并不是同一种产品。它们分别对应数据处理接口、在线证据选择、离线检索器训练，以及证据集合选择。

## 用一个例子理解

假设你问：“Melanie 今年去了几次海滩？”资料里有“喜欢海滩”、实际出游记录、重复转述、去年记录。下面只是帮助理解的应用例子，不是这四篇已验证的记忆实验。

| 工作 | 通俗理解 | 在流程里的位置 | 需要训练吗 |
| --- | --- | --- | --- |
| [[research/misc/papers/lotus-2025/index|LOTUS]] | 给数据表加上“能理解文字”的筛选、关联、汇总操作 | 数据处理层；可组织整个筛选/聚合流程 | 使用模型，用户不必先训练专用模型 |
| [[research/agent-memory/assets/utilityqwen-2025/index|UtilityQwen]] | 搜到资料后，挑能帮助回答的片段，排除只有主题相关的内容 | 召回之后、回答之前 | 论文训练了专用小模型；使用其权重无需重训 |
| [[research/agent-memory/assets/scarlet-2025/index|SCARLet]] | 训练时遮住资料观察答案支持变化，教搜索器找有用证据 | 离线标注/训练检索器 | 需要训练；不是每次问题都重新做归因 |
| [[research/agent-memory/assets/optiset-2026/index|OptiSet]] | 挑一组互补证据，避免前三条全在重复同一次出游 | 召回之后、回答之前 | 有免训练版，也有训练版 |

LOTUS 可以表达“挑出今年实际出游的记录，再汇总”；但正确计数还依赖事件去重和事实覆盖，语义聚合不保证精确计数。UtilityQwen 强調“喜欢海滩”未必有助于回答次数。SCARLet 把这类有用/无用差异变成训练信号。OptiSet 强调“同一次旅行的三篇记录”可能不如“三次不同旅行的三条记录”。这些解释均不代表方法在该例上一定成功。

## 为什么感觉以前有人做过

你的直觉有依据：语义过滤、证据效用、扩展后精选都是已有研究方向。Jev / System One 更接近一个通用的、带类型输出及概率的决策模型接口；上述工作则规定怎样组织数据、构造监督或选择证据。可以用某个决策模型去实现系统中的一步，但“换成 Jev”本身不自动形成新的科研贡献。

从可实施性看，UtilityQwen 与 OptiSet 的思路最接近 RAG 的“检索结果进入回答上下文之前”；LOTUS 可组织过滤/聚合的数据处理；SCARLet 是训练方法，应放在离线流程里。映射到 Pi agent 时，这只是架构建议，尚未验证具体 extension hook：先在记忆检索工具返回后、最终上下文组装前考察选择器。

## 共同边界

- 只筛已有候选，无法自动找回候选池之外的事实。UtilityQwen 实验 top-100，OptiSet top-20；OptiSet 的 Expand 是问题视角/集合扩展，不应描述为全库主动补搜。
- “有用”取决于问题、其他证据及最终回答模型；相关性与效用不等价，但效用估计也会错。
- 这些论文不足以证明长期记忆、时间冲突、精确计数已经解决，也不足以否定该领域所有新方法。
- 代码与论文分开记录：OptiSet 只有占位仓库；SCARLet 缺归因模块且训练脚本与 dense 部署理解有差距。无本地复现结果。

## 来源与维护

2026-09-22：按上述四篇原文及官方代码缓存整理；版本、commit、实验设置及已知差异见各正式笔记。关联 [[research/agent-memory/assets/jev-system-one-2026/index|Jev / System One]]。

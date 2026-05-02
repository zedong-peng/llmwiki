---
title: "Construct Validity in AI Benchmarks"
domain: research
area: research-taste
type: paper
status: stable
updated: 2026-04-08
tags: [construct-validity, benchmark-design, psychometrics, evaluation]
---
# Construct Validity in AI Benchmarks (Salaudeen et al., 2025)

## 核心主张

大多数 AI benchmark **缺乏 construct validity**——它们测量的是某个操作化指标，但从未验证这个指标真正反映了目标构念（construct）。

## Construct Validity 的三个层次

| 层次 | 问题 | 验证方法 |
|------|------|----------|
| **Content validity** | 题目是否覆盖了构念的所有方面？ | 专家评审，覆盖率分析 |
| **Convergent validity** | 同一构念的不同测量是否相关？ | 相关系数，因子分析 |
| **Predictive validity** | benchmark 分数是否能预测真实世界表现？ | 下游任务相关性 |

## 对 ResearchTaste-Bench 的含义

1. **Karpathy 四维度缺乏验证**：问题选择、Hamming awareness、简洁性、时机感——这四个维度来自直觉，从未被数据验证。如果它们高度相关（测的是同一件事），分开报告是冗余的；如果完全不相关，"taste"作为统一构念就不存在。

2. **IRT 是解决方案**：用 Multidimensional IRT（MIRT）在 20+ 个不同能力水平的模型上，跑 200 个 taste 判断题，探索真实的因子结构。让数据告诉我们 taste 是几维的。

3. **Predictive validity 是护城河**：一个能声明并验证 construct validity 的 benchmark 本身就是对领域的贡献，这是被社区接受的必要条件。

## 论文对应信号

- 本条目基于 txt 中提到的 Salaudeen et al. 2025 框架
- 与 [[papers/chen-2025-irt-llm]] 联合使用：IRT 工具 + construct validity 框架

## 关键引用
> "大多数 AI benchmark 缺乏 construct validity" — Salaudeen et al. 2025

## 关联页面
- [[concepts/researchTaste-bench-design]] — 如何在设计中满足 construct validity
- [[papers/chen-2025-irt-llm]] — IRT 工具实现

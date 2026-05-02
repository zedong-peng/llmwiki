---
title: "SWE-bench-Live: Living Benchmark Design"
domain: research
area: research-taste
type: paper
status: stable
updated: 2026-04-08
tags: [living-benchmark, contamination, data-freshness, benchmark-design]
---
# SWE-bench-Live: Living Benchmark Design

## 核心创新

**Living Benchmark**：持续自动更新的 benchmark，新数据永远比模型训练数据新，从根本上解决数据污染问题。

## 设计原理

```
传统 benchmark:
数据（2020）→ 发布 → 模型训练（2023）包含了数据 → 污染

Living benchmark:
新数据（T）→ 冻结模型判断 → 等待 18 个月 → 计算GT → 更新 leaderboard
                              （T + 18 months > 模型训练截止）
```

## 关键机制

```
每季度自动更新：
1. 拉最新论文（发布后 < 30 天）
2. 冻结模型对这批论文的判断（在 GT 计算前）
3. 18 个月后计算实际影响力
4. 更新 leaderboard
```

**效果**：新数据永远比模型训练数据新，污染问题随时间自动解决。

## 对 ResearchTaste-Bench 的应用

ResearchTaste-Bench 是**"Research Taste 的 SWE-bench-Live"**：

- 历史数据（2019-2022）：已知 GT，用于初始版本
- 每季度新数据：发布后 30 天内的新论文，18 个月后 GT 成熟
- 跨 venue 覆盖：ICLR、NeurIPS、ICML、ICLR

**这是最重要的设计选择**：不是一次性 paper，而是持续运行的基础设施。

## 与 CCV 的协同

| 机制 | 解决的问题 | 时间维度 |
|------|-----------|----------|
| Living benchmark | 训练数据污染 | 长期（每季度） |
| CCV 3-session probe | 单次评估中的记忆检索 | 即时（每次评估） |

两者互补：CCV 检测当前污染，Living benchmark 通过时间隔离根本性解决污染。

## 关联页面
- [[concepts/researchTaste-bench-design]] — Living benchmark 在方案中的位置
- [[papers/ccv-contamination]] — CCV 污染检测（互补机制）

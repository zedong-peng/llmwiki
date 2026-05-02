---
title: "Ke et al. 2015: Sleeping Beauty Index"
domain: research
area: research-taste
type: paper
status: stable
updated: 2026-04-08
tags: [sleeping-beauty, citation-dynamics, scientometrics, ground-truth]
---
# Ke et al. 2015: Sleeping Beauty Index (SB Index)

## 什么是 Sleeping Beauty 论文

一篇发表后长期被忽视、但在某一时刻突然被大量引用的论文。

**经典例子**：Mendel 的遗传学论文发表后几十年无人引用，直到 DNA 结构被发现后爆发。

## SB 指数的定义

Ke et al. (2015) 提出的量化公式，测量一篇论文从"沉睡"到"觉醒"的程度：

```
SB = (c_awakening - c_sleep) / (t_awakening - t_sleep)
```

其中：
- `c_sleep`：沉睡期平均年引用数
- `c_awakening`：觉醒后年引用数
- `t_sleep`、`t_awakening`：对应时间段

**高 SB 指数** = 长期低引用后突然爆发 = 典型的 Sleeping Beauty

## 在 ResearchTaste-Bench 中的应用

SB 论文是 **Ground Truth 金字塔的最高层（层级3，权重5x）**：

```python
def compute_sb_index(early_cites, late_cites):
    """
    简化版 SB 指数计算
    early_cites: 发表后6个月引用数
    late_cites: 发表后24个月引用数
    """
    if early_cites < 5 and late_cites > 50:
        tier = 3  # Sleeping Beauty，权重5x
    elif early_cites < 10 and late_cites > 30:
        tier = 2  # Early Underrated，权重2x
    else:
        tier = 1  # Standard，权重1x
    return tier
```

**为什么 SB 是最好的 taste ground truth**：
- SB 论文代表了"事后看明显重要，但当时无人识别"的极端案例
- 识别 SB 潜力 = 真正的 taste，而不是跟风引用
- 客观、可计算，不依赖任何人的主观判断

## D3: Sleeping Beauty Detection 子任务

```
给定一篇发表后6个月引用<5的论文
判断它是否会在2年后"觉醒"（引用>50）
这是最难的子任务，最能区分taste高低
```

**SB Detection Rate（SBDR）**：在此子任务上的准确率，最有区分度的诊断指标。

## 关联页面
- [[concepts/researchTaste-bench-design]] — 三层 Ground Truth 金字塔设计
- [[papers/gong-2025-economics-taste]] — 人类在 SB 论文上的表现基线

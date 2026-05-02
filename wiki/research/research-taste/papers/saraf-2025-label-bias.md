---
title: "Saraf et al. 2025: Label Bias in LLM Evaluation"
domain: research
area: research-taste
type: paper
status: stable
updated: 2026-04-08
tags: [label-bias, LLM-judge, blind-evaluation, evaluation-methodology]
---
# Saraf et al. 2025: Label Bias in LLM Evaluation

## 核心发现

在 LLM-as-judge 评估中，**标签（label）本身**会影响评分：

- **False attribution**：给 LLM 生成的内容贴上错误的作者标签，可以让偏好排名**偏移 50 个百分点**
- "Claude" 标签 vs. 无标签，分数显著不同
- 去掉标签可以消除 label bias

## Label Bias vs. Preference Leakage

| 问题 | 来源 | 解决方案 |
|------|------|----------|
| **Label bias** (Saraf) | 标签本身影响判断（品牌效应） | 匿名评估（去掉所有标签） |
| **Preference leakage** (Li) | 用同一模型生成+评估 | 跨 family 评估 |

两者都是 circular evaluation 的表现，但机制不同。

## Blind Evaluation Protocol

Saraf et al. 建议的标准盲评协议，直接用于 ResearchTaste-Bench：

```
严格去掉所有可识别信息：
✗ 标题（最强污染信号）
✗ 作者名（机构偏见）
✗ 引用数（直接泄漏结果）
✗ 发表年份（时间线索）
✗ Venue 名称（质量信号）
✗ 方法名中的专有名词（BERT → "双向预训练模型"）
✓ 只保留：摘要正文 + 领域背景
```

**效果**：消除可偏移 50pp 的 label bias。

## 关联页面
- [[papers/li-2026-preference-leakage]] — preference leakage（相关问题）
- [[concepts/researchTaste-bench-design]] — 盲评协议在 benchmark 中的实现

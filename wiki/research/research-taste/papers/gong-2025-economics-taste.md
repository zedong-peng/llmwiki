---
title: "Gong et al. 2025: LLM Research Taste in Economics"
domain: research
area: research-taste
type: paper
status: stable
updated: 2026-04-08
tags: [research-taste, citation-prediction, economics, human-baseline, cross-domain]
---
# Gong et al. 2025: LLM Research Taste in Economics

## 核心结果

| 条件 | 准确率 |
|------|--------|
| Zero-shot taste 判断 | **31%**（低于随机？或 31% = 正确率偏低） |
| Fine-tuned（economics 数据）| **59-70%** |
| Human reviewer | **42-63%** |
| 跨域迁移（economics→management science）| **70%** |

## 关键发现

### 1. Zero-shot 区分度空间
Zero-shot 只有 31% 意味着 frontier 模型在 taste 判断上有**真实的提升空间**。这不是天花板测试，而是真正难的任务。

### 2. Fine-tuning 有效
Fine-tuned 模型可以达到 59-70%，说明 taste 是**可学习的**，不完全是智商测试。这支持了 Karpathy 的"taste 可以被培养"的观点。

### 3. Human reviewer 只有 42-63%
这是最重要的数字：**人类 reviewer 本身的 taste 判断也不准**。这给了 AI 系统超越人类的空间，也说明"人类基线"远没有想象中高。

### 4. 跨域迁移（70%）
Economics 训练的模型迁移到 management science 达到 70%，说明 taste 有**跨领域的通用成分**。这是 ResearchTaste-Bench 需要测跨领域的理论基础。

## 对 ResearchTaste-Bench 的含义

- 人类基线设为 **0.61**（42-63% 的中位数）
- 目标：frontier LLM zero-shot 在 WTA 上超过 0.61
- 跨域一致性：在 NLP 和 CV 的 WTA 相关 = taste 通用性的度量

## 与 HindSight 的关系

Gong et al. 测的是引用预测准确率（citation prediction），而 HindSight 发现 LLM 在 novelty 判断上有 ρ=-0.29 的负相关。两者合起来说明：**LLM 既不能准确预测影响力，又系统性高估 novelty**——两种错误都指向 taste 缺失。

## 关联页面
- [[concepts/researchTaste-bench-design]] — 基线设计
- [[papers/hindsight-novelty-bias]] — novelty bias 补充
- [[papers/hicke-2025-tastybench]] — TastyBench 同类工作

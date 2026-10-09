---
title: "LiveMathematicianBench: Substitution-Resistant Evaluation"
domain: research
area: research-taste
type: note
status: active
updated: 2026-04-08
tags: [benchmark-design, pattern-matching, substitution-test, genuine-capability]
---


> 未读资料：原页面来自网页检索摘要、会话引用或方案推演，未阅读论文原文，也没有代码核验记录。以下内容完整保留历史研究素材，数字、引文、方法归属和新颖性主张尚未核实；本次迁移不构成重新阅读或事实复核。
> 引用记录：[citation.bib](../assets/livemathematicianBench/citation.bib)。
# LiveMathematicianBench: Substitution-Resistant Evaluation

## 核心发现

在 **substitution-resistant** 测试下，模型准确率从 **43.5% 暴跌到 17.6%**（低于随机基线 25%）。

这说明：**模型的"能力"很大程度上是模式匹配，不是真实理解。**

## Substitution 测试是什么

通过改变题目中的具体实例（方法名、数据集名、数字），保留核心推理结构，测试模型是否真正理解原理。

```
原题：BERT 和 ELMo 哪个更适合 NER 任务？[原始准确率 43.5%]
   ↓ substitution（改变所有具体名称）
新题：双向预训练模型 X 和 浅层双向模型 Y 哪个更适合序列标注？[准确率 17.6%]
```

暴跌说明：模型在背"BERT 比 ELMo 好"这个事实，而不是理解背后的推理。

## 对 ResearchTaste-Bench 的含义

**最基本假设的攻击**：

LLM 的 pairwise taste judgment 是否真的反映了判断能力，还是只是"哪篇论文更有名"的记忆检索？

如果我们把两篇论文摘要做 substitution（改变具体方法名），模型的判断会改变吗？

- **改变** → 模型在用表面特征（方法名知名度）做判断，不是 taste
- **不改变** → 模型有某种对 idea 结构的真实判断

## 为什么不直接做 Substitution

**致命缺陷**：改变方法名可能同时改变了 idea 的语义，导致 ground truth 也变了。

**改进**：
1. 不做 substitution，改用**统计方法**验证：同一模型在 NLP 和 CV 领域的 WTA 高度相关 → 有通用 taste
2. 用**D4 合成 idea 子任务**：完全合成的 idea 无法被记忆检索，测 taste vs. knowledge 分离

## Knowledge Independence 指标 (KI)

```python
KI = WTA_synthetic - WTA_real
# 接近 0 = taste 能力不依赖知识检索（好）
# > 0.1 打 ⚠️ = 分数部分来自知识，不是纯 taste
```

这是 LiveMathematicianBench 启发的直接应用。

## 关联页面
- [[research/research-taste/threads/researchTaste-bench-design]] — KI 指标设计、D4 合成 idea 子任务

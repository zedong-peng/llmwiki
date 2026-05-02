---
title: "Why LLMs Aren't Scientists Yet"
domain: research
area: research-taste
type: paper
status: stable
updated: 2026-04-08
tags: [AI-scientist, research-taste, failure-modes, motivation]
---
# Why LLMs Aren't Scientists Yet

## 核心贡献

系统梳理 LLM 在科学研究中的**六大失败模式**，其中第六条是：

> **"Weak scientific taste in experimental design"**

这是 ResearchTaste-Bench **最强的工作动机**：领域已有论文明确指出 taste 是 LLM 的关键失败模式，而我们的工作是**第一个系统测量这个失败模式的 benchmark**。

## 六大失败模式

（基于 txt 中的引用，具体编号可能与原文有出入）

1. 无法提出真正新颖的研究假设
2. 实验设计缺乏系统性
3. 对异常结果解释不足
4. 过度依赖已知模式（知识检索 vs. 推理）
5. 跨领域迁移能力弱
6. **Weak scientific taste in experimental design** ← 直接动机

## 对 ResearchTaste-Bench 定位的意义

```
AI Scientist 能力 = Taste × Execution
                    ↑              ↑
            ResearchTaste-Bench  Scientist-Bench
```

- **Why LLMs Aren't Scientists Yet** 明确了 taste 是失败维度
- **Scientist-Bench / PaperBench** 测 execution
- **ResearchTaste-Bench** 测 taste

Taste 是乘数：execution 再强，taste 为零，结果也是零。

## 与 Scientist-Bench 的差异化定位

| 维度 | Scientist-Bench | ResearchTaste-Bench |
|------|----------------|---------------------|
| 测什么 | 能否执行研究（execution） | 能否判断什么值得执行（taste） |
| GT 来源 | implementation success rate | 客观影响力信号（SB index） |
| 评估方式 | human-level quality comparison | pairwise judgment + 客观GT |
| 关系 | 互补 | 互补 |

## 引用价值

这篇论文在 paper 中的作用：**工作动机的直接支撑**。

> "We are the first to systematically measure the failure mode identified by [Why LLMs Aren't Scientists Yet]: weak scientific taste."

## 关联页面
- [[concepts/researchTaste-bench-design]] — 方案如何回应这一动机
- [[papers/scientist-bench]] — execution 测量的对比工作

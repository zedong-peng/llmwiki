---
title: "Scientist-Bench: Autonomous Research Capability Evaluation"
domain: research
area: research-taste
type: paper
status: stable
updated: 2026-04-08
tags: [AI-scientist, execution-benchmark, autonomous-research, benchmark]
---
# Scientist-Bench: Autonomous Research Capability Evaluation

## 核心设计

测量 LLM 的**自主研究执行能力**：

- **任务类型**：guided innovation + open-ended exploration
- **评估指标**：implementation success rate、human-level quality comparison
- **本质**：测执行能力，而非 taste

## 与 ResearchTaste-Bench 的关键区别

| 维度 | Scientist-Bench | ResearchTaste-Bench |
|------|----------------|---------------------|
| 核心问题 | 能否执行研究？ | 能否判断什么值得执行？ |
| 能力类型 | Execution | Taste |
| 互补性 | ✓ 互补，非竞争 | ✓ 互补，非竞争 |

**完整的 AI Scientist 评估需要两者：**
```
AI Scientist = Taste × Execution
```

## 重要提醒：不要与 PaperBench 混淆

| Benchmark | 组织 | 侧重 |
|-----------|------|------|
| PaperBench | OpenAI | 复现论文实验 |
| Scientist-Bench | 学术 | 自主研究执行 |
| MLR-Bench | 学术 | 模块化研究流程 |

三者都在 execution 侧，与 ResearchTaste-Bench（taste 侧）互补。

## 潜在协同实验

在 paper 中直接测试 taste 和 execution 的相关性：
- 用同一批模型跑 ResearchTaste-Bench 和 Scientist-Bench
- 报告相关系数
- **如果相关低** → 证明两者是独立能力，两个 benchmark 都有独立价值
- **如果相关高** → 说明 taste 是 execution 的前提条件，更支持 taste 研究的重要性

## 关联页面
- [[papers/why-llms-arent-scientists.md]] — taste 是失败模式的动机
- [[papers/starace-2025-paperbench]] — PaperBench（execution 侧）
- [[concepts/researchTaste-bench-design]] — Taste × Execution 框架

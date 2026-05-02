---
title: "HindSight: LLM Novelty Bias in Research Evaluation"
domain: research
area: research-taste
type: paper
status: stable
updated: 2026-04-08
tags: [novelty-bias, LLM-evaluation, research-taste, hindsight]
---
# HindSight: LLM Novelty Bias (HindSight paper)

## 核心发现

LLM 在评估研究 idea 时，**系统性高估 novelty**：

> **ρ = −0.29**（novelty 评分与实际影响力的斯皮尔曼相关）

即：LLM 认为新颖的 idea，实际影响力反而更低。

## Novelty Bias 的机制

LLM 倾向于给"听起来新颖"的 idea 打高分，但：
- High novelty ≠ High impact
- 真正重要的工作往往是"用更简单的方式做到同样的事"（符合 Karpathy 的简洁性直觉）
- "新颖"容易被 LLM 识别，"重要"需要更深层的判断

## 四象限框架

```
              High Impact
                  ↑
   Taste Signal   │   Easy Case
   （low novelty  │  （high novelty
    high impact） │   high impact）
─────────────────┼──────────────→ High Novelty
   Hard Case     │  Novelty Trap
   （low novelty  │  （high novelty
    low impact）  │   low impact）
                  │
              Low Impact
```

**Novelty Trap**（右下象限）：模型最容易被迷惑的区域

## 对 ResearchTaste-Bench 的应用

**D1: Novelty Trap Test 子任务**

```python
def build_novelty_trap_pairs(papers, judge_llm):
    """
    用LLM打novelty分，交叉实际影响力
    找四象限极端样本
    """
    for paper in papers:
        paper.novelty_score = judge_llm.score_novelty(paper.abstract)

    # Novelty Trap：高novelty评分 + 低实际影响力
    high_novelty_low_impact = [
        p for p in papers
        if p.novelty_score > 0.7 and p.composite_score < 0.3
    ]

    # Taste Signal：低novelty评分 + 高实际影响力
    low_novelty_high_impact = [
        p for p in papers
        if p.novelty_score < 0.3 and p.composite_score > 0.7
    ]

    # 构造对：taste signal vs. novelty trap
    trap_pairs = []
    for signal in low_novelty_high_impact:
        trap = random.choice(high_novelty_low_impact)
        trap_pairs.append(TastePair(
            high=signal,  # 正确答案：选这个
            low=trap,
            pair_type="novelty_trap"
        ))
    return trap_pairs
```

**Novelty Bias 指标（NB）**：
```
NB = accuracy_on_novelty_trap - 0.5
# 负数越大 = 越容易被 novelty 迷惑
```

## Sakana AI Scientist 的印证

Sakana AI Scientist 评估发现"misclassifying established concepts as novel"——这正是 novelty bias 在生成端的表现。我们的 benchmark 测判断端的 novelty bias，与之互补。

## 关联页面
- [[concepts/researchTaste-bench-design]] — Novelty Trap Test 设计
- [[papers/gong-2025-economics-taste]] — taste 的人类基线

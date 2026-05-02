---
title: "IRT for LLM Capability Evaluation"
domain: research
area: research-taste
type: paper
status: stable
updated: 2026-04-08
tags: [IRT, psychometrics, construct-validation, LLM-evaluation, factor-analysis]
---
# IRT for LLM Capability Evaluation (Chen et al., 2025)

## 核心贡献

将 **Item Response Theory（IRT）** 引入 LLM 评估：用 IRT 学习模型的多维能力向量，发现

> "Learned parameters encode meaningful, interpretable information"

## 什么是 IRT

经典心理测量工具，原用于人类能力测试（SAT、GRE）。核心思想：
- **Item difficulty**：每道题的难度参数
- **Item discrimination**：每道题对能力的区分度
- **Ability parameter**：被试（模型）的潜在能力向量

**MIRT（Multidimensional IRT）**：允许多维能力结构，可以探索 k 维因子解。

## 对 ResearchTaste-Bench 的直接应用

```python
from mirt import MultidimensionalIRT

def validate_taste_construct(response_matrix):
    """
    验证taste的因子结构
    response_matrix: shape (n_models, n_items)
    n_models >= 20（从GPT-2到Claude Opus，覆盖能力范围）
    n_items = 200（四个维度各50题）
    """
    # 探索性因子分析
    for n_factors in [1, 2, 3, 4]:
        model = MultidimensionalIRT(n_factors=n_factors)
        model.fit(response_matrix)
        fit_stats = model.get_fit_statistics()
        print(f"{n_factors}因子模型: BIC={fit_stats['BIC']:.1f}, "
              f"RMSEA={fit_stats['RMSEA']:.3f}")

    # 最优因子数 + 各维度的因子载荷
    # 回答：Karpathy的四维度是否真的是独立的？
```

## 关键约束

- 需要 **≥20 个不同能力水平的模型**作为"被试"（从 7B 到 frontier，人为制造方差）
- Frontier 模型的 taste 能力集中在 31-70%（Gong et al.），方差可能不足
- 解决方案：加入 7B、13B、70B 规模模型

## 预期发现

| 因子数 | 含义 | 行动 |
|--------|------|------|
| 1因子最优 | taste 是单一能力 | 简化为单一分数 |
| 2-3因子最优 | 相关维度可合并 | 简化 profile |
| 4因子最优 | Karpathy 的直觉被数据验证 | 分开报告 |

## 关联页面
- [[papers/salaudeen-2025-construct-validity]] — construct validity 框架
- [[concepts/researchTaste-bench-design]] — IRT 在 benchmark 设计中的应用

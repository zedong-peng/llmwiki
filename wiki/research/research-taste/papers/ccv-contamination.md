---
title: "CCV: Contamination Check via Cross-session Variance"
domain: research
area: research-taste
type: paper
status: stable
updated: 2026-04-08
tags: [contamination, benchmark-design, data-leakage, evaluation-methodology]
---
# CCV: Contamination Check via Cross-session Variance

## 核心思想

**污染检测**：如果模型"背"了答案，它在多个独立 session 中会给出**一致的具体答案**（低多样性）；如果模型在真正"思考"，答案会有合理的多样性（高多样性）。

## 操作化

```python
def ccv_contamination_check(model, abstract, n_sessions=3):
    """
    同一问题跑3个独立session，测diversity
    低diversity = 高污染（模型在背答案）
    """
    responses = []
    for _ in range(n_sessions):
        # 每次新建独立session，无历史context
        r = model.fresh_session().ask(
            f"Abstract: {abstract}\n"
            f"What is the title of this paper? "
            f"How many citations does it have?"
        )
        responses.append(r)

    diversity = compute_semantic_diversity(responses)
    # 低diversity = 模型给出一致的具体答案 = 记住了
    return 1 - diversity  # contamination score
```

## 污染分数的使用

```python
# 对每个评估对计算污染分数
contamination_score = ccv_check(model, abstract_a) + ccv_check(model, abstract_b)

# 高污染 = contamination_score > threshold
# 处理方式：
# 1. 排除（最保守）
# 2. 降权（推荐：污染越高，这对的权重越低）
# 3. 报告 Contamination Gap (CG)
```

## Contamination Gap (CG) 指标

```python
CG = WTA_high_contamination - WTA_low_contamination
# > 0.1 打 ⚠️，说明分数部分来自记忆
```

**解读**：
- CG 接近 0 → 模型的 taste 能力不依赖记忆
- CG > 0.1 → 模型在高污染样本上表现更好，说明在"作弊"

## 局限性

CCV 只能检测**二进制污染**（背了 vs. 没背），无法区分：
1. 真实 taste 能力
2. 基于知识的正确判断（"我知道这篇论文后来很有影响力"）
3. 真正的模式匹配 taste

→ 需要 D4 Knowledge Independence Test 作为补充

## 关联页面
- [[papers/swe-bench-live]] — 互补机制（时间隔离）
- [[concepts/researchTaste-bench-design]] — 四层防泄漏体系

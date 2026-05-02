---
title: "Preference Leakage in LLM-as-Judge (Li et al., ICLR 2026)"
domain: research
area: research-taste
type: paper
status: stable
updated: 2026-04-08
tags: [preference-leakage, LLM-judge, evaluation-bias, circular-evaluation]
---
# Preference Leakage in LLM-as-Judge (Li et al., ICLR 2026)

## 核心发现

当用同一个 LLM 既生成内容又评估内容时，存在**系统性的自我偏好**（self-preference bias）：

- 模型倾向于给自己生成的内容打高分
- "Claude" 标签本身就会提升分数，与内容质量无关
- Steering vectors 可以降低 97% 的 self-preference，但仍不稳定

## Preference Leakage 的机制

```
Generator LLM ─── 生成 idea A ──→ ┐
                                    ├─→ Judge LLM ─── 偏向 A ⚠️
Judge LLM ─────────────────────────┘
（同一个模型）
```

**关键问题**：如果用 Claude 评估 Claude Code 生成的 idea，self-preference bias 会**系统性地高估质量**。

## 解决方案：跨 Family 评估

| 生成模型 | Judge 模型 | 有效？ |
|---------|-----------|--------|
| Claude | Claude | ❌ Self-preference |
| Claude | GPT-4o | ✓ Cross-family |
| GPT-4o | Gemini | ✓ Cross-family |
| GPT-4o | GPT-4o | ❌ Self-preference |

**强制规则**：Judge 必须来自不同 LLM family。

## 对 ResearchTaste-Bench 的含义

ResearchTaste-Bench 的主要评估任务是让 LLM 做 pairwise judgment，但 **ground truth 不依赖 LLM judge**（用客观信号：SB 指数、引用数），所以 preference leakage 的影响主要在：

1. **Novelty Trap 子任务**：novelty 评分用 LLM——必须跨 family
2. **合成 idea 子任务（D4）**：GT 用 5 个跨 family 模型的高一致性判断
3. **Human-LLM agreement 验证**：用人类专家验证 LLM judge 的可靠性

## 关联页面
- [[papers/saraf-2025-label-bias]] — label bias（同类问题的不同维度）
- [[concepts/researchTaste-bench-design]] — 四层防泄漏设计

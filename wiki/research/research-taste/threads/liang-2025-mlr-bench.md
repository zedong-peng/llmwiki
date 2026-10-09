---
title: "MLR-Bench: Evaluating AI Agents on Open-Ended Machine Learning Research"
domain: research
area: research-taste
type: note
status: active
updated: 2026-04-07
tags: [benchmark, ml-research, idea-generation, open-ended, modular]
arxiv: "2505.19955"
authors: [Liang et al.]
venue: arXiv
year: 2025
---


> 未读资料：原页面来自网页检索摘要、会话引用或方案推演，未阅读论文原文，也没有代码核验记录。以下内容完整保留历史研究素材，数字、引文、方法归属和新颖性主张尚未核实；本次迁移不构成重新阅读或事实复核。
> 引用记录：[citation.bib](../assets/liang-2025-mlr-bench/citation.bib)。
# MLR-Bench: Evaluating AI Agents on Open-Ended Machine Learning Research

**arXiv:** https://arxiv.org/abs/2505.19955

## Abstract
MLR-Bench is a comprehensive benchmark for evaluating AI agents through open-ended machine learning research tasks. It uses a modular research agent scaffold and an LLM-based evaluator (MLR-Judge) that mimics human peer review.

## Key Contributions
- 201 research tasks sourced from NeurIPS, ICLR, ICML
- Multi-stage evaluation: Idea Generation → Proposal Formulation → Experimentation → Paper Writing
- MLR-Judge: automated evaluator mimicking peer review
- Modular design allows evaluating individual research stages

## Key Findings
- LLMs perform **well in ideation and writing** stages
- Coding agents often produce **unreliable experimental results**
- Significant gap between writing quality and experimental validity
- The bottleneck is execution/experimentation, not idea generation

## What This Reveals About Research Taste
Interesting implication: if LLMs are good at ideation but bad at execution, then:
- We can't yet tell if their "ideas" are actually good (can't verify experimentally)
- The taste problem may be masked by the execution problem
- Need to decouple idea quality evaluation from execution

## Connections
- [[research/research-taste/threads/mlrc-bench-2025]] — similar benchmark, different focus (competition tasks)
- [[research/research-taste/threads/research-ability-dimensions]] — maps to the modular stages
- [[research/research-taste/threads/benchmark-landscape]]

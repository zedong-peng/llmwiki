---
title: "ERL: Experiential Reflective Learning"
domain: research
area: agent-memory
type: paper
status: stub
updated: 2026-05-28
tags: [paper, retrieval, llm-as-heuristic, reflective-learning, heuristic-selection]
---

# ERL: Experiential Reflective Learning

## Paper Meta
- Title: Experiential Reflective Learning for LLM-Based Heuristic Retrieval
- Authors: —
- Year: 2026
- Venue: arXiv
- arXiv: https://arxiv.org/abs/2603.24639

## TL;DR
- LLM-based retrieval (k=20 heuristics) achieves 56.1% vs embedding-based baseline.
- "Retrieval quality matters more than heuristic quantity."
- **Direct empirical evidence**: LLM-based retrieval > embedding-based retrieval for heuristic selection.

## Method
- LLM generates k=20 heuristics for retrieval.
- Experiential reflection: LLM learns from past retrieval successes/failures.
- Key finding: quality of each heuristic matters more than generating many heuristics.

## Relevance to LAzyMem
**Direct empirical evidence** that LLM-based retrieval outperforms embedding-based retrieval. Supports LAzyMem's core design: LLM-compiled boolean predicates over raw dialogue beats dense RAG by 3.4pp (F1 0.495 vs 0.461) on LoCoMo-10. The "quality > quantity" finding aligns with LAzyMem's focused predicate compilation.

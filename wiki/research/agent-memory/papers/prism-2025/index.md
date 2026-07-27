---
title: "PRISM: Precision-Recall Iterative Selection for Multi-Hop QA"
domain: research
area: agent-memory
type: paper
status: stub
updated: 2026-05-28
tags: [paper, retrieval, iterative, multi-hop, precision-recall]
---

# PRISM: Precision-Recall Iterative Selection for Multi-Hop QA

## Paper Meta
- Title: PRISM: Precision-Recall Iterative Selection for Multi-Hop QA
- Authors: Nahid & Rafiei, University of Alberta
- Year: 2025
- Venue: Withdrawn from ICLR 2026 (Jan 6, 2026); still on arXiv
- arXiv: https://arxiv.org/abs/2510.14278

## TL;DR
- Three agents: Question Analyzer (decomposition), Selector (precision-filtering), Adder (recall-addition) — "Prune-and-Recover" loop ≤3 rounds.
- Withdrawn from ICLR 2026 after reviewers questioned novelty ("variant of ReAct/IRCoT") and missing fine-tuned baselines.
- Safe to cite as "concurrent unpublished work."

## Method
1. **Question Analyzer**: Decomposes the question into sub-questions.
2. **Selector**: Precision-filtering — prunes irrelevant retrieved passages.
3. **Adder**: Recall-addition — adds back passages that may have been incorrectly pruned.
4. Loop runs ≤3 rounds.

## Results
| Benchmark | Metric | PRISM | IRCoT | OneR |
|-----------|--------|-------|-------|------|
| MuSiQue | Recall | 83.2% | 57.1% | 44.6% |
| HotpotQA | Recall | 90.9% | — | — |
| HotpotQA | F1 | 66.96 | — | — (CoRAG 56.3) |
| Latency | — | 8.6s | 16s | — |
| Context reduction | — | 73.3% | — | — |

## Relevance to LAzyMem
- Precision-recall split maps onto LoCoMo categories: Cat 1/2 = precision, Cat 3 = recall.
- Not a published competitor — safe to cite as concurrent unpublished work.
- Ablation methodology (FAIR-RAG style) directly usable for LoCoMo experiments with LAzyMem.

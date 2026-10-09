---
title: "AgentIR: A Workload-Adaptive Cascade Retrieval Substrate for Long-Term Conversational Memory"
domain: research
area: agent-memory
type: paper
status: seed
updated: 2026-07-27
tags: [paper, agent-memory, raw-retrieval, cascade, bm25, adaptive-retrieval]
---

## Unread Archive Record

- Reading status: not_started in the historical metadata. This page preserves a legacy summary or research artifact; it does not establish paper reading or verify the claims below.
- Source provenance: [citation.bib](../assets/agentir-2026/citation.bib); the complete historical metadata is retained there.

# AgentIR: A Workload-Adaptive Cascade Retrieval Substrate for Long-Term Conversational Memory

## Paper Meta
- Title: AgentIR: A Workload-Adaptive Cascade Retrieval Substrate for Long-Term Conversational Memory
- Year: 2026
- Venue: Arxiv
- arXiv: https://arxiv.org/abs/2605.25092

## TL;DR
- BM25-first confidence cascade: uses only the BM25 top-k score margin to decide whether to pay the ~52 ms dense-channel cost.
- LongMemEval (500-question): skips dense retrieval for 63% of queries at parity LLM-judged accuracy, 2.67x speedup; per-question-type thresholds reach 5.76x.
- LoCoMo: trigger chooses 100% skip rate, +0.089 Hit@5 over the dense path at a 132x latency ratio.


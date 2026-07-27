---
title: "AgentIR: A Workload-Adaptive Cascade Retrieval Substrate for Long-Term Conversational Memory"
domain: research
area: agent-memory
type: paper
status: stub
updated: 2026-07-27
tags: [paper, agent-memory, raw-retrieval, cascade, bm25, adaptive-retrieval]
---

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

## Local Files
- PDF: [2605.25092-agentir.pdf](../lazymem-related-work/pdfs/2605.25092-agentir.pdf)
- Text: [2605.25092-agentir.txt](../lazymem-related-work/text/2605.25092-agentir.txt)
- Corpus: [lazymem-related-work](../lazymem-related-work/index.md) (category: raw-retrieval)

## Relevance to LazyMem
- **Level 1 direct collision** (ResearchStudio scoop audit): a confidence-triggered BM25-to-dense cascade with workload retuning already exists in the same domain.
- The generic "BM25 first, semantic retrieval only when useful" claim is not available to LazyMem; any gate must beat AgentIR-style retrieval-margin gating.

---
title: "SelRoute: Query-Type-Aware Routing for Long-Term Conversational Memory Retrieval"
domain: research
area: agent-memory
type: paper
status: stub
updated: 2026-07-27
tags: [paper, agent-memory, raw-retrieval, routing, query-type]
---

# SelRoute: Query-Type-Aware Routing for Long-Term Conversational Memory Retrieval

## Paper Meta
- Title: SelRoute: Query-Type-Aware Routing for Long-Term Conversational Memory Retrieval
- Year: 2026
- Venue: Arxiv
- arXiv: https://arxiv.org/abs/2604.02431

## TL;DR
- Routes queries among lexical, semantic, hybrid, and vocabulary-enriched pipelines by question type; routing can be deterministic from metadata; an 83%-effective regex classifier suffices.
- Predicted-type Recall@5 0.689; type-aware routing works without a query-time LLM or GPU.
- Demonstrated heterogeneity: near-verbatim single-session questions favor full-text search; other types benefit from semantic/enriched routes. Also documents large FTS5-vs-BM25 and granularity-dependent discrepancies across LongMemEval reports.

## Local Files
- PDF: [2604.02431-selroute.pdf](../lazymem-related-work/pdfs/2604.02431-selroute.pdf)
- Text: [2604.02431-selroute.txt](../lazymem-related-work/text/2604.02431-selroute.txt)
- Corpus: [lazymem-related-work](../lazymem-related-work/index.md) (category: raw-retrieval)

## Relevance to LazyMem
- Direct collision at the routing-principle level; any LazyMem gate must be compared with query-type routing, not only always-on dense baselines.

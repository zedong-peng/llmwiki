---
title: "SmartSearch: How Ranking Beats Structure for Conversational Memory Retrieval"
domain: research
area: agent-memory
type: paper
status: stub
updated: 2026-07-27
tags: [paper, agent-memory, raw-retrieval, ranking, reranking]
---

# SmartSearch: How Ranking Beats Structure for Conversational Memory Retrieval

## Paper Meta
- Title: SmartSearch: How Ranking Beats Structure for Conversational Memory Retrieval
- Year: 2026
- Venue: Arxiv
- arXiv: https://arxiv.org/abs/2603.15599

## TL;DR
- Raw-history retrieval with no LLM ingestion: NER/POS-weighted substring matching for high-recall candidates, then CrossEncoder + ColBERT fused via RRF.
- Oracle analysis: substring matching resolves 98.9% of queries, raw recall 98.6% — but without strong ranking only 22.5% of gold evidence survives the effective context position. Ranking/truncation, not initial search, is the bottleneck.
- Reports 93.5% LoCoMo accuracy (EverMemOS protocol), 91.9% (MemOS protocol), 88.4% LongMemEval-S — protocol-bound numbers; explicitly reports two incompatible LoCoMo protocols separately.

## Local Files
- PDF: [2603.15599-smartsearch.pdf](../lazymem-related-work/pdfs/2603.15599-smartsearch.pdf)
- Text: [2603.15599-smartsearch.txt](../lazymem-related-work/text/2603.15599-smartsearch.txt)
- Corpus: [lazymem-related-work](../lazymem-related-work/index.md) (category: raw-retrieval)

## Relevance to LazyMem
- Closest raw-history deterministic-retrieval + learned-reranking system; consumes the "no LLM at ingestion" novelty claim.
- Implies LazyMem's compiler attacks the wrong stage: candidate generation is saturated, ranking is where value remains.

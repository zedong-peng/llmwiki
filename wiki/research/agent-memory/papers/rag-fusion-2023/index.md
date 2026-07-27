---
title: "RAG-Fusion: Multi-Query Retrieval with Reciprocal Rank Fusion"
domain: research
area: agent-memory
type: paper
status: stub
updated: 2026-05-28
tags: [paper, retrieval, rag, multi-query, rrf, query-expansion]
---

# RAG-Fusion: Multi-Query Retrieval with Reciprocal Rank Fusion

## Paper Meta
- Title: RAG-Fusion
- Authors: Zackary Raudaschl
- Year: 2023
- Venue: Blog post (widely adopted in LangChain)
- arXiv: —
- Source: https://towardsdatascience.com/forget-rag-the-future-is-rag-fusion-1147298d8ad1

## TL;DR
- Generate N query variations from the original question → retrieve for each → merge results with Reciprocal Rank Fusion (RRF).
- Not evaluated on LoCoMo; no category-awareness or conversational context.

## Method
1. LLM generates N paraphrase/variation queries from the original question.
2. Each query is used independently for retrieval.
3. Results are merged via RRF: `score(d) = sum(1 / (rank_i(d) + 60))` across all query retrievals.
4. Top-k by RRF score are returned.

## Relevance to LAzyMem
LAzyMem uses a different approach: instead of multiple NL query variations, it compiles questions into boolean predicates (must/should keywords) executed via exact string matching. The RRF aggregation idea is related but LAzyMem uses max-merge across predicates rather than rank fusion.

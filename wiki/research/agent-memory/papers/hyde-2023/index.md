---
title: "HyDE: Hypothetical Document Embeddings"
domain: research
area: agent-memory
type: paper
status: stub
updated: 2026-05-28
tags: [paper, retrieval, query-expansion, hyde, embedding]
---

# HyDE: Hypothetical Document Embeddings

## Paper Meta
- Title: Precise Zero-Shot Dense Retrieval without Relevance Labels
- Authors: Luyu Gao, Xueguang Ma, Jimmy Lin, Jamie Callan
- Year: 2023
- Venue: SIGIR 2023
- arXiv: —

## TL;DR
- Generate a hypothetical answer to the query, embed it, retrieve by embedding similarity to the hypothetical answer rather than the original question.
- Strong single-query baseline; no multi-angle coverage.
- Relevant for LoCoMo Cat 4 (open-domain/adversarial).

## Method
1. LLM generates a hypothetical document/answer for the query.
2. Embed the hypothetical document.
3. Retrieve real documents by similarity to the hypothetical embedding.

## Relevance to LAzyMem
Baseline for query expansion via hypothetical documents. LAzyMem takes a different approach: instead of embedding a hypothetical answer, it compiles the question into boolean predicates (must/should keywords + optional speaker filter) for exact string matching. No embedding required.

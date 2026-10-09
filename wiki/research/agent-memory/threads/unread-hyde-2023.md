---
title: "HyDE: Hypothetical Document Embeddings"
domain: research
area: agent-memory
type: paper
status: seed
updated: 2026-05-28
tags: [paper, retrieval, query-expansion, hyde, embedding]
---

## Unread Archive Record

- Reading status: not_started in the historical metadata. This page preserves a legacy summary or research artifact; it does not establish paper reading or verify the claims below.
- Source provenance: [citation.bib](../assets/hyde-2023/citation.bib); the complete historical metadata is retained there.

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

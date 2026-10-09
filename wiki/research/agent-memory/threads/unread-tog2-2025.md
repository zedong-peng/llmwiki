---
title: "Think-on-Graph 2.0: KG + Unstructured Text Retrieval"
domain: research
area: agent-memory
type: paper
status: seed
updated: 2026-05-28
tags: [paper, retrieval, knowledge-graph, beam-search, multi-source]
---

## Unread Archive Record

- Reading status: not_started in the historical metadata. This page preserves a legacy summary or research artifact; it does not establish paper reading or verify the claims below.
- Source provenance: [citation.bib](../assets/tog2-2025/citation.bib); the complete historical metadata is retained there.

# Think-on-Graph 2.0: KG + Unstructured Text Retrieval

## Paper Meta
- Title: Think-on-Graph 2.0: Deep and Faithful Large Language Model Reasoning with Knowledge-Guided Retrieval
- Authors: —
- Year: 2025
- Venue: ICLR 2025
- arXiv: https://arxiv.org/abs/2410.10813

## TL;DR
- Couples KG retrieval with unstructured text retrieval.
- Graph traversal as beam search guided by LLM scoring.
- Multi-source iterative retrieval guided by LLM reasoning.

## Method
1. Start from entities in the question.
2. Traverse KG edges guided by LLM relevance scoring (beam search).
3. At each node, also retrieve unstructured text passages.
4. LLM scores and prunes the beam.
5. Aggregate evidence from both KG and text.

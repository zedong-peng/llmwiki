---
title: "Think-on-Graph 2.0: KG + Unstructured Text Retrieval"
domain: research
area: agent-memory
type: paper
status: stub
updated: 2026-05-28
tags: [paper, retrieval, knowledge-graph, beam-search, multi-source]
---

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

## Relevance to LAzyMem
Formal vocabulary: graph traversal as beam search = LLM-guided heuristic search. LAzyMem takes a simpler approach — compiling questions into boolean predicates for exact string matching — but the LLM-as-planner framing is shared. Multi-source retrieval (KG + text) contrasts with LAzyMem's raw-dialogue-only storage.

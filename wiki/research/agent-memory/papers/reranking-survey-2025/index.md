---
title: "Reranking Survey: LLMs as Zero-Shot Listwise Rankers"
domain: research
area: agent-memory
type: paper
status: stub
updated: 2026-05-28
tags: [paper, survey, reranking, llm-as-ranker, zero-shot]
---

# Reranking Survey: LLMs as Zero-Shot Listwise Rankers

## Paper Meta
- Title: A Survey on LLM-based Reranking
- Authors: —
- Year: 2025
- Venue: arXiv
- arXiv: https://arxiv.org/abs/2512.16236

## TL;DR
- LLMs as zero-shot listwise rankers outperform prior supervised methods.
- LLM-as-ranker = heuristic-search view of retrieval.

## Relevance to LAzyMem
Supports the LLM-as-heuristic framing: if LLMs can outperform supervised rankers zero-shot, they can also compile better boolean predicates zero-shot. Relevant as a potential post-processing step for LAzyMem: reranking exact-match results before passing to the answer LLM.

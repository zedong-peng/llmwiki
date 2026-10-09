---
title: "LLM-A*: LLM as Heuristic Function for A* Search"
domain: research
area: agent-memory
type: paper
status: seed
updated: 2026-05-28
tags: [paper, search, heuristic, astar, planning, llm-as-heuristic]
---

## Unread Archive Record

- Reading status: not_started in the historical metadata. This page preserves a legacy summary or research artifact; it does not establish paper reading or verify the claims below.
- Source provenance: [citation.bib](../assets/llm-astar-2024/citation.bib); the complete historical metadata is retained there.

# LLM-A*: LLM as Heuristic Function for A* Search

## Paper Meta
- Title: LLM-A*: Large Language Model Enhanced Incremental Heuristic Search on Path Planning
- Authors: —
- Year: 2024
- Venue: EMNLP Findings 2024
- arXiv: —

## TL;DR
- LLM provides the heuristic function h(n) in A*, estimating cost-to-goal.
- LLM world knowledge substitutes for hand-crafted heuristics.
- **Proof-of-concept**: LLMs are valid heuristic functions for structured search.

## Method
- Standard A* search framework.
- Replace hand-crafted h(n) with LLM-generated estimate of cost-to-goal.
- LLM uses world knowledge to estimate remaining path cost.

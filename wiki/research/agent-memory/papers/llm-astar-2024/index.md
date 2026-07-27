---
title: "LLM-A*: LLM as Heuristic Function for A* Search"
domain: research
area: agent-memory
type: paper
status: stub
updated: 2026-05-28
tags: [paper, search, heuristic, astar, planning, llm-as-heuristic]
---

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

## Relevance to LAzyMem
Formal justification for the "LLM as heuristic" framing. In LAzyMem, the LLM acts as a heuristic by compiling questions into boolean predicates — estimating which keywords and speaker filters will locate the relevant conversation turns. See also: LLM Inference via Search Survey (TMLR 2025).

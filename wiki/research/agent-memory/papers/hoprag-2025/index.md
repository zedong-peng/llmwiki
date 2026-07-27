---
title: "HopRAG: Multi-Hop Retrieval via Passage Graph and LLM Reasoning"
domain: research
area: agent-memory
type: paper
status: stub
updated: 2026-05-28
tags: [paper, retrieval, multi-hop, graph, reasoning]
---

# HopRAG: Multi-Hop Retrieval via Passage Graph and LLM Reasoning

## Paper Meta
- Title: HopRAG: Multi-Hop Retrieval Augmented Generation for the Web
- Authors: —
- Year: 2025
- Venue: ACL Findings 2025
- arXiv: https://arxiv.org/abs/2502.12442

## TL;DR
- Passage graph with logical connections. Retrieval: retrieve-reason-prune exploring multi-hop neighbors via LLM reasoning.
- Relevant for LoCoMo Cat 3 (multi-hop), which requires logical relevance, not just semantic similarity.

## Method
1. Build a passage graph where edges represent logical connections between passages.
2. Start from initial retrieved passages.
3. LLM reasons about which neighboring passages are logically relevant.
4. Prune irrelevant neighbors, expand to relevant ones.
5. Repeat for multi-hop traversal.

## Relevance to LAzyMem
LoCoMo Cat 3 (multi-hop) requires logical relevance beyond semantic similarity. HopRAG's graph traversal approach contrasts with LAzyMem's boolean predicate strategy: LAzyMem handles multi-hop by decomposing questions into must/should keyword predicates rather than graph traversal.

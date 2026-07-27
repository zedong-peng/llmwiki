---
title: "Entropy-Based Adaptive Memory Retrieval"
domain: research
area: agent-memory
type: paper
status: stub
updated: 2026-05-28
tags: [paper, retrieval, adaptive, granularity, entropy, memory]
---

# Entropy-Based Adaptive Memory Retrieval

## Paper Meta
- Title: Entropy-Based Adaptive Memory Retrieval
- Authors: —
- Year: 2026
- Venue: ICLR 2026
- arXiv: https://openreview.net/pdf?id=i2yIvZARnG

## TL;DR
- Entropy-based router selects retrieval granularity level (session/turn/summary/keyword) per query.
- High-entropy queries → coarser granularity; low-entropy queries → finer granularity.
- Adaptive granularity = learned meta-heuristic for memory retrieval.

## Method
- Compute entropy of the query representation.
- Route to different granularity levels based on entropy:
  - High entropy (uncertain/broad) → session-level or summary retrieval
  - Low entropy (specific/precise) → turn-level or keyword retrieval
- Combines multiple granularity levels in a unified retrieval framework.

## Relevance to LAzyMem
Adaptive granularity is a potential extension for LAzyMem's predicate compilation:
- High-entropy queries → broader must/should keyword sets
- Low-entropy queries → tighter, more specific predicates
- Entropy-based routing as a meta-heuristic for predicate complexity selection

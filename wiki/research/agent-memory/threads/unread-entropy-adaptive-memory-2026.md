---
title: "Entropy-Based Adaptive Memory Retrieval"
domain: research
area: agent-memory
type: paper
status: seed
updated: 2026-05-28
tags: [paper, retrieval, adaptive, granularity, entropy, memory]
---

## Unread Archive Record

- Reading status: not_started in the historical metadata. This page preserves a legacy summary or research artifact; it does not establish paper reading or verify the claims below.
- Source provenance: [citation.bib](../assets/entropy-adaptive-memory-2026/citation.bib); the complete historical metadata is retained there.

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

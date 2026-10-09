---
title: "Segment-Level Memory: Topically Coherent Retrieval Units"
domain: research
area: agent-memory
type: paper
status: seed
updated: 2026-05-28
tags: [paper, memory, segmentation, granularity, retrieval-unit]
---

## Unread Archive Record

- Reading status: not_started in the historical metadata. This page preserves a legacy summary or research artifact; it does not establish paper reading or verify the claims below.
- Source provenance: [citation.bib](../assets/segment-level-memory-2025/citation.bib); the complete historical metadata is retained there.

# Segment-Level Memory: Topically Coherent Retrieval Units

## Paper Meta
- Title: Segment-Level Memory for Long-Context Dialogue
- Authors: —
- Year: 2025
- Venue: ICLR 2025
- arXiv: —

## TL;DR
- Turn-level = too fine; session-level = too coarse.
- Conversation segmentation for topically coherent units.
- Retrieval unit granularity should match conversation structure.

## Method
- Segment conversations into topically coherent units (neither turn-level nor session-level).
- Use segments as retrieval units.
- Segmentation can be done by topic shift detection or LLM-based segmentation.

## Relevance to LAzyMem
Retrieval unit granularity is a key design decision. LAzyMem uses individual conversation turns as retrieval units, which this paper suggests may be too fine. Segment-level units could improve LAzyMem's recall by matching boolean predicates against topically coherent chunks rather than single turns.

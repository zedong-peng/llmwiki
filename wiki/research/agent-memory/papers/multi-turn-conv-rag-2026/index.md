---
title: "Multi-Turn Conversational RAG: Retrieval Stability"
domain: research
area: agent-memory
type: paper
status: stub
updated: 2026-05-28
tags: [paper, retrieval, rag, multi-turn, conversational, stability]
---

# Multi-Turn Conversational RAG: Retrieval Stability

## Paper Meta
- Title: Multi-Turn Conversational RAG as a Retrieval Stability Problem
- Authors: —
- Year: 2026
- Venue: arXiv
- arXiv: https://arxiv.org/abs/2602.09552

## TL;DR
- Multi-turn RAG as retrieval stability problem.
- Small reformulation errors accumulate across turns.
- Multi-query expansion + RRF naturally improves retrieval stability.

## Relevance to LAzyMem
Directly relevant to LAzyMem's setting: LoCoMo is inherently multi-turn. LAzyMem addresses retrieval stability differently — boolean predicate execution over raw turns is deterministic and not subject to embedding drift across reformulations.

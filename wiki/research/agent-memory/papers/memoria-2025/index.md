---
title: "Memoria: Session Summarization + Weighted Knowledge Graph"
domain: research
area: agent-memory
type: paper
status: stub
updated: 2026-05-28
tags: [paper, memory, summarization, knowledge-graph, compression]
---

# Memoria: Session Summarization + Weighted Knowledge Graph

## Paper Meta
- Title: Memoria: Resolving Fateful Forgetting Problem through Human-Inspired Memory Architecture
- Authors: —
- Year: 2025
- Venue: arXiv
- arXiv: https://arxiv.org/abs/2512.12686

## TL;DR
- Session summarization + weighted KG.
- Compresses 115,000 tokens → under 400 with 87.1% accuracy.
- Extreme compression ratio while maintaining high accuracy.

## Method
- Session-level summarization to compress conversation history.
- Weighted knowledge graph to represent key facts and relationships.
- Retrieval from both summaries and KG nodes.

## Relevance to LAzyMem
Demonstrates extreme compression is possible (115k → 400 tokens). LAzyMem takes the opposite design choice: store raw dialogue unchanged and rely on boolean predicate execution rather than compression. The tradeoff is storage vs. retrieval precision.

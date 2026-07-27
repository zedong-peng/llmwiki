---
title: "MemoRAG: Global Memory + Clue Drafts for Long-Context RAG"
domain: research
area: agent-memory
type: paper
status: stub
updated: 2026-05-28
tags: [paper, retrieval, rag, memory, query-expansion, clue-drafts]
---

# MemoRAG: Global Memory + Clue Drafts for Long-Context RAG

## Paper Meta
- Title: MemoRAG: Moving towards Next-Gen RAG Via Memory-Inspired Knowledge Discovery
- Authors: Hongjin Qian et al.
- Year: 2025
- Venue: WWW 2025
- arXiv: https://arxiv.org/abs/2409.05591

## TL;DR
- Lightweight global memory model reads the full long context, generates "clue drafts" (partial hypothetical answers) used as retrieval queries.
- Outperforms HyDE, RQ-RAG, GraphRAG.
- **Closest published work to LAzyMem**: MemoRAG trains a dedicated clue model; LAzyMem uses zero-shot prompting only (zero training).
- Not evaluated on LoCoMo.

## Method
1. A lightweight "memory model" reads the full document/context and builds a global memory.
2. At query time, the memory model generates "clue drafts" — partial hypothetical answers that hint at where the answer might be.
3. Clue drafts are used as retrieval queries (similar to HyDE but with a trained model).
4. Retrieved passages are passed to the main LLM for final answer generation.

## Relevance to LAzyMem
**Closest published work** in spirit. Both use LLM-generated intermediate representations as retrieval queries. Key differentiators: LAzyMem uses zero-shot prompting (no training), targets exact string matching over raw dialogue (not embedding similarity), and is evaluated on LoCoMo-10 (F1 0.495, beating Mem0 by 9.5pp and dense RAG by 3.4pp).

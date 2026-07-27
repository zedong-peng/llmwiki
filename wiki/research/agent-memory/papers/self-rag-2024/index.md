---
title: "Self-RAG: Self-Reflective Retrieval-Augmented Generation"
domain: research
area: agent-memory
type: paper
status: stub
updated: 2026-05-28
tags: [paper, retrieval, rag, self-reflection, adaptive, fine-tuning]
---

# Self-RAG: Self-Reflective Retrieval-Augmented Generation

## Paper Meta
- Title: Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection
- Authors: Akari Asai, Zeqiu Wu, Yizhong Wang, Avirup Sil, Hannaneh Hajishirzi
- Year: 2024
- Venue: ICLR 2024
- arXiv: —

## TL;DR
- Fine-tune LLM with special tokens for adaptive retrieve-generate-critique cycle.
- Training-required; LAzyMem is training-free.

## Method
- Special tokens: `[Retrieve]`, `[IsRel]`, `[IsSup]`, `[IsUse]`.
- LLM decides when to retrieve, whether retrieved passages are relevant, whether they support the generation, and whether the output is useful.
- Fine-tuned end-to-end on this adaptive retrieve-generate-critique loop.

## Relevance to LAzyMem
Key baseline for adaptive retrieval. Training-required approach vs LAzyMem's zero-shot prompting. Demonstrates that adaptive retrieval decisions can be learned; LAzyMem achieves retrieval selectivity through boolean predicate compilation rather than fine-tuned special tokens.

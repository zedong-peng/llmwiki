---
title: "Collab-RAG: Fine-Tuned SLM Decomposer"
domain: research
area: agent-memory
type: paper
status: stub
updated: 2026-05-28
tags: [paper, retrieval, query-decomposition, fine-tuning, slm]
---

# Collab-RAG: Fine-Tuned SLM Decomposer

## Paper Meta
- Title: Collab-RAG: Boosting Retrieval-Augmented Generation for Complex Question Answering via White-Box and Black-Box LLM Collaboration
- Authors: —
- Year: 2025
- Venue: arXiv
- arXiv: https://arxiv.org/abs/2504.04915

## TL;DR
- Fine-tune 3B SLM as decomposer via iterative preference optimization.
- 3B SLM outperforms frozen 32B LLM on decomposition.
- Query decomposition is a learnable, specialized skill.

## Relevance to LAzyMem
Potential future direction: fine-tune a small model specifically for LoCoMo predicate compilation. The 3B SLM > 32B LLM result suggests that task-specific fine-tuning for boolean predicate generation could improve LAzyMem's predicate quality beyond its current zero-shot prompting approach.

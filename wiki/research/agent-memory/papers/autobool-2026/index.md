---
title: "AutoBool: RL-Trained LLM for Boolean Query Generation"
domain: research
area: agent-memory
type: paper
status: stub
updated: 2026-05-28
tags: [paper, retrieval, boolean-query, rl, query-generation]
---

# AutoBool: RL-Trained LLM for Boolean Query Generation

## Paper Meta
- Title: AutoBool: An Reinforcement-Learning trained LLM for Effective Automated Boolean Query Generation for Systematic Reviews
- Authors: Wang et al.
- Year: 2026
- Venue: arXiv
- arXiv: https://arxiv.org/abs/2602.00005

## TL;DR
- Train an LLM to generate Boolean retrieval queries directly, optimizing retrieval metrics rather than just next-token likelihood.
- Domain: literature retrieval (systematic reviews), not long-conversation memory QA.
- **Closest evidence that executable query generation is a real retrieval direction**, not just natural-language query rewriting.

## Method
- RL training: reward = retrieval metric (recall/precision on systematic review queries).
- LLM learns to generate Boolean expressions (`AND`, `OR`, `NOT`) that maximize retrieval quality.
- Evaluated on systematic review literature search benchmarks.

## Relevance to LAzyMem
Key prior art for LAzyMem's boolean predicate approach. Demonstrates that LLM-generated executable Boolean queries are a viable retrieval direction. LAzyMem extends this to long-conversation memory QA (LoCoMo-10, F1 0.495) using zero-shot prompting rather than RL training, and targets exact string matching over raw dialogue rather than literature retrieval.

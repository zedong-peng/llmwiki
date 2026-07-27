---
title: "Query Decomposition as Multi-Armed Bandit"
domain: research
area: agent-memory
type: paper
status: stub
updated: 2026-05-28
tags: [paper, retrieval, query-decomposition, bandit, exploration-exploitation]
---

# Query Decomposition as Multi-Armed Bandit

## Paper Meta
- Title: Query Decomposition as Multi-Armed Bandit for Retrieval
- Authors: Petcu et al.
- Year: 2025
- Venue: arXiv
- arXiv: https://arxiv.org/abs/2510.18633

## TL;DR
- Multi-query decomposition as multi-armed bandit.
- Rank information + human judgment: 35% gain in document-level precision over naive decomposition.
- Exploration-exploitation trade-off directly applicable to iterative LoCoMo retrieval.

## Method
- Each sub-query is an "arm" in a multi-armed bandit.
- Reward = retrieval precision for that sub-query.
- Bandit algorithm selects which sub-queries to execute based on past performance.
- Balances exploration (new query types) vs exploitation (known good queries).

## Relevance to LAzyMem
Bandit-based sub-query selection is a potential extension for LAzyMem: iteratively select the most informative boolean predicates from a candidate set rather than executing all in parallel. Could reduce the 2,334 tokens/query cost while maintaining the F1 0.495 quality.

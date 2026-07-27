---
title: "From Lossy to Verified: A Provenance-Aware Tiered Memory for Agents (TierMem)"
domain: research
area: agent-memory
type: paper
status: stub
updated: 2026-07-27
tags: [paper, agent-memory, raw-retrieval, tiered-memory, escalation, provenance]
---

# From Lossy to Verified: A Provenance-Aware Tiered Memory for Agents (TierMem)

## Paper Meta
- Title: From Lossy to Verified: A Provenance-Aware Tiered Memory for Agents
- Year: 2026
- Venue: Arxiv
- arXiv: https://arxiv.org/abs/2602.17913

## TL;DR
- Makes the lazy principle explicit: query a summary index first, judge sufficiency with a router, escalate through provenance pointers to immutable raw pages, write back verified information.
- LoCoMo: accuracy 0.851 vs 0.873 raw-only, with 54.1% fewer input tokens and 60.7% lower latency (3,396 vs 7,398 tokens; 6.76 vs 17.18 s).

## Local Files
- PDF: [2602.17913-tiermem.pdf](../lazymem-related-work/pdfs/2602.17913-tiermem.pdf)
- Text: [2602.17913-tiermem.txt](../lazymem-related-work/text/2602.17913-tiermem.txt)
- Corpus: [lazymem-related-work](../lazymem-related-work/index.md) (category: raw-retrieval)

## Relevance to LazyMem
- Owns the claim "answer with the cheapest sufficient evidence and escalate when needed"; LazyMem can only test whether an even cheaper lexical tier has a better lifecycle Pareto point — empirical, not conceptual, novelty.

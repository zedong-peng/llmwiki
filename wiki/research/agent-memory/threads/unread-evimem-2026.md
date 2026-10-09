---
title: "EviMem: Evidence-Gap-Driven Iterative Retrieval for Long-Term Conversational Memory"
domain: research
area: agent-memory
type: paper
status: seed
updated: 2026-07-27
tags: [paper, agent-memory, raw-retrieval, iterative, sufficiency]
---

## Unread Archive Record

- Reading status: not_started in the historical metadata. This page preserves a legacy summary or research artifact; it does not establish paper reading or verify the claims below.
- Source provenance: [citation.bib](../assets/evimem-2026/citation.bib); the complete historical metadata is retained there.

# EviMem: Evidence-Gap-Driven Iterative Retrieval for Long-Term Conversational Memory

## Paper Meta
- Title: EviMem: Evidence-Gap-Driven Iterative Retrieval for Long-Term Conversational Memory
- Year: 2026
- Venue: Arxiv
- arXiv: https://arxiv.org/abs/2604.27695

## TL;DR
- Evaluates the accumulated evidence set, labels sufficiency, diagnoses what is missing, refines the query, and abstains when the loop cannot close the gap.
- Particularly large gains on multi-hop questions; lower latency than a multi-agent comparator.

## Local Files
- PDF: [2604.27695-evimem.pdf](../assets/lazymem-related-work/pdfs/2604.27695-evimem.pdf)
- Text: [2604.27695-evimem.txt](../assets/lazymem-related-work/text/2604.27695-evimem.txt)
- Corpus: [lazymem-related-work](lazymem-related-work.md) (category: raw-retrieval)

## Relevance to LazyMem
- Direct collision on evidence-sufficiency escalation; LazyMem cannot claim novelty for "test intermediate result, retrieve again". A cheaper/calibrated deterministic gap certificate would be the only remaining distinction.

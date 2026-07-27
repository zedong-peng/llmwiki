---
title: "ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT"
domain: research
area: agent-memory
type: paper
status: stub
updated: 2026-07-27
tags: [paper, ir-foundation, late-interaction, reranking]
---

# ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT

## Paper Meta
- Title: ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT
- Year: 2020
- Venue: SIGIR
- arXiv: https://arxiv.org/abs/2004.12832

## TL;DR
- Retains token-level representations and uses late interaction, reducing the information bottleneck of a single pooled vector.
- Strong reranking primitive used by raw-history systems (e.g. SmartSearch).

## Local Files
- PDF: [2004.12832-colbert.pdf](../lazymem-related-work/pdfs/2004.12832-colbert.pdf)
- Text: [2004.12832-colbert.txt](../lazymem-related-work/text/2004.12832-colbert.txt)
- Corpus: [lazymem-related-work](../lazymem-related-work/index.md) (category: ir-foundation)

## Relevance to LazyMem
- Conversational memory adds a second late-interaction level: scoring a session by its best-matching turn (max-turn) rather than pooling the whole session.

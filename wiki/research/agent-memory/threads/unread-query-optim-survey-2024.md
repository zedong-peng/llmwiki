---
title: "Survey on Query Optimization in LLMs"
domain: research
area: agent-memory
type: paper
status: seed
updated: 2026-05-28
tags: [paper, survey, query-optimization, query-expansion, taxonomy]
---

## Unread Archive Record

- Reading status: not_started in the historical metadata. This page preserves a legacy summary or research artifact; it does not establish paper reading or verify the claims below.
- Source provenance: [citation.bib](../assets/query-optim-survey-2024/citation.bib); the complete historical metadata is retained there.

# Survey on Query Optimization in LLMs

## Paper Meta
- Title: A Survey on Query Optimization in Large Language Models
- Authors: —
- Year: 2024
- Venue: arXiv
- arXiv: https://arxiv.org/abs/2412.17558

## TL;DR
- Taxonomy: Foundation → Expansion → Sophistication → Agentic (2025-2026).
- Positions LAzyMem in the "Agentic Era" of query optimization.

## Taxonomy
| Era | Approach | Examples |
|-----|----------|---------|
| Foundation | Basic query rewriting | Paraphrase, synonym expansion |
| Expansion | Multi-query, HyDE | RAG-Fusion, Query2Doc |
| Sophistication | Structured decomposition | IRCoT, PRISM |
| Agentic (2025-2026) | LLM-driven adaptive retrieval planning | LAzyMem, ByteRover |

## Relevance to LAzyMem
Provides formal positioning for LAzyMem in the query optimization literature. LAzyMem fits the "Agentic Era" framing: LLM compiles questions into executable boolean predicates, going beyond multi-query expansion to symbolic retrieval planning. Achieves F1 0.495 on LoCoMo-10 at 2,334 tokens/query.

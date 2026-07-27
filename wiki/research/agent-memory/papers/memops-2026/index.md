---
title: "MemOps: Benchmarking Lifecycle Memory Operations in Long-Horizon Conversations"
domain: research
area: agent-memory
type: paper
status: stub
updated: 2026-07-27
tags: [paper, agent-memory, benchmark, lifecycle-operations]
---

# MemOps: Benchmarking Lifecycle Memory Operations in Long-Horizon Conversations

## Paper Meta
- Title: MemOps: Benchmarking Lifecycle Memory Operations in Long-Horizon Conversations
- Year: 2026
- Venue: Arxiv
- arXiv: https://arxiv.org/abs/2607.12893

## TL;DR
- Operation-level benchmark for remember, update, forget, and reflect behavior — broadens evaluation beyond recall QA.
- A raw append-only design is naturally strong on preservation but weak on explicit deletion, conflict resolution, and consolidation unless defined separately.

## Local Files
- PDF: [2607.12893-memops.pdf](../lazymem-related-work/pdfs/2607.12893-memops.pdf)
- Text: [2607.12893-memops.txt](../lazymem-related-work/text/2607.12893-memops.txt)
- Corpus: [lazymem-related-work](../lazymem-related-work/index.md) (category: benchmark)

## Relevance to LazyMem
- Exposes lifecycle operations where raw-history systems like LazyMem are weakest; update/forget semantics need explicit design.

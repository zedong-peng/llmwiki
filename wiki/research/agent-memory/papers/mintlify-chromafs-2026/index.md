---
title: "Mintlify ChromaFs: Virtual Filesystem for LLM Retrieval"
domain: research
area: agent-memory
type: blog
status: stub
updated: 2026-05-28
tags: [blog, retrieval, filesystem, symbolic, grep, production, inspiration]
---

# Mintlify ChromaFs: Virtual Filesystem for LLM Retrieval

## Source Meta
- Title: How We Built a Virtual Filesystem for Our Assistant
- Author: Mintlify team
- Year: 2026
- Type: Engineering blog post
- URL: https://www.mintlify.com/blog/how-we-built-a-virtual-filesystem-for-our-assistant
- Date: March 24, 2026

## TL;DR
- ChromaFs: virtual filesystem on top of Chroma vector DB. LLM uses `ls`, `grep`, `cat` as retrieval primitives.
- Directory trees stored in gzipped JSON; `cat file.mdx` = fetch all chunks from Chroma.
- Session creation: 46s → 100ms (460x speedup). Cost: $0.0137 → $0. 30k+ conversations/day.
- Conceptual inspiration for LAzyMem's compiled boolean predicate retrieval.

## Architecture
- Virtual filesystem layer on Chroma vector DB.
- LLM navigates using familiar filesystem commands: `ls` (list), `cd` (navigate), `grep` (search), `cat` (fetch content).
- Directory structure mirrors the information structure of the codebase/docs.
- `cat file.mdx` triggers a Chroma query to fetch all chunks associated with that file.

## Core Insight
**Retrieval interface should match information structure.**
- For code/docs: filesystem hierarchy is the natural structure → `ls`/`grep`/`cat` beats semantic search.
- For LoCoMo conversations: sessions, turns, speakers, timestamps are the natural structure → structured navigation may outperform embedding similarity for many query types.

## Results
| Metric | Before | After | Gain |
|--------|--------|-------|------|
| Session creation time | 46s | 100ms | 460x |
| Cost per conversation | $0.0137 | $0 | 100% |
| Scale | — | 30k+ conversations/day | — |

## Relevance to LAzyMem
Conceptual precedent: LLM-generated executable search programs over structured data beat semantic search when the information has natural structure. LAzyMem applies the same principle to raw conversation turns via boolean predicates (must/should keywords + speaker filter), achieving F1 0.495 on LoCoMo-10 at 2,334 tokens/query.

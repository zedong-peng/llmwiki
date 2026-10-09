---
title: "Training-Free Lexical-Dense Fusion for Conversational-Memory Retrieval"
domain: research
area: agent-memory
type: paper
status: seed
updated: 2026-07-27
tags: [paper, agent-memory, raw-retrieval, bm25, dense, fusion]
---

## Unread Archive Record

- Reading status: not_started in the historical metadata. This page preserves a legacy summary or research artifact; it does not establish paper reading or verify the claims below.
- Source provenance: [citation.bib](../assets/lexical-dense-fusion-2026/citation.bib); the complete historical metadata is retained there.

# Training-Free Lexical-Dense Fusion for Conversational-Memory Retrieval

## Paper Meta
- Title: Training-Free Lexical-Dense Fusion for Conversational-Memory Retrieval
- Year: 2026
- Venue: Arxiv
- arXiv: https://arxiv.org/abs/2606.04194

## TL;DR
- Controlled BM25 + max-turn dense late-interaction fusion study with leave-one-conversation-out fusion weight.
- LoCoMo: BM25 Hit@1 0.640; dense max-turn 0.664; BM25+dense max-turn fusion 0.752 (+11.2 points). Dense helps multi-hop/temporal; BM25 stronger on adversarial; fusion captures complementary errors.
- LongMemEval-S: BM25 saturates the lexical regime; net fusion gain small and non-significant — the conditional-value pattern a lazy system must model.
- Negative result: adding an off-the-shelf MS MARCO cross-encoder to fused top-10 drops Hit@1 0.701 → 0.633.


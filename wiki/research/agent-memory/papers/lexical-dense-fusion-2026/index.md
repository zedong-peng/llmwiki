---
title: "Training-Free Lexical-Dense Fusion for Conversational-Memory Retrieval"
domain: research
area: agent-memory
type: paper
status: stub
updated: 2026-07-27
tags: [paper, agent-memory, raw-retrieval, bm25, dense, fusion]
---

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

## Local Files
- PDF: [2606.04194-lexical-dense-fusion.pdf](../lazymem-related-work/pdfs/2606.04194-lexical-dense-fusion.pdf)
- Text: [2606.04194-lexical-dense-fusion.txt](../lazymem-related-work/text/2606.04194-lexical-dense-fusion.txt)
- Corpus: [lazymem-related-work](../lazymem-related-work/index.md) (category: raw-retrieval)

## Relevance to LazyMem
- Strongest direct control for a simple LazyMem redesign; defines the B4 hybrid baseline any new mechanism must survive.

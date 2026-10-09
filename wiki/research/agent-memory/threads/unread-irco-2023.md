---
title: "IRCoT: Interleaving Retrieval with Chain-of-Thought Reasoning"
domain: research
area: agent-memory
type: paper
status: seed
updated: 2026-05-28
tags: [paper, retrieval, iterative, chain-of-thought, multi-hop]
---

## Unread Archive Record

- Reading status: not_started in the historical metadata. This page preserves a legacy summary or research artifact; it does not establish paper reading or verify the claims below.
- Source provenance: [citation.bib](../assets/irco-2023/citation.bib); the complete historical metadata is retained there.

# IRCoT: Interleaving Retrieval with Chain-of-Thought Reasoning

## Paper Meta
- Title: Interleaving Retrieval with Chain-of-Thought Reasoning for Knowledge-Intensive Multi-Step Questions
- Authors: Harsh Trivedi, Niranjan Balasubramanian, Tushar Khot, Ashish Sabharwal
- Year: 2023
- Venue: ACL 2023
- arXiv: —

## TL;DR
- Alternate CoT reasoning steps with retrieval; each reasoning step generates a new retrieval query.
- Designed for Wikipedia KB, not personal conversation memory.
- Key baseline for multi-hop iterative retrieval.

## Method
1. Generate a CoT reasoning step.
2. Use the reasoning step as a retrieval query.
3. Retrieve relevant passages.
4. Continue CoT with retrieved context.
5. Repeat until answer is generated.

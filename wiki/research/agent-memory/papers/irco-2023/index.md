---
title: "IRCoT: Interleaving Retrieval with Chain-of-Thought Reasoning"
domain: research
area: agent-memory
type: paper
status: stub
updated: 2026-05-28
tags: [paper, retrieval, iterative, chain-of-thought, multi-hop]
---

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

## Relevance to LAzyMem
Key baseline for iterative retrieval. PRISM (arXiv 2510.14278) extends IRCoT with precision-recall split. LAzyMem takes a different approach: instead of sequential CoT-driven retrieval, it compiles questions into boolean predicates executed via exact string matching over raw conversation turns.

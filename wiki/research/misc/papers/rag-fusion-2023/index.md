---
title: "RAG-Fusion: a New Take on Retrieval-Augmented Generation"
domain: research
area: misc
type: paper
status: processed
updated: 2026-04-19
tags: [paper, misc, rag, retrieval-augmented-generation, reciprocal-rank-fusion, chatbot, infineon]
---
# RAG-Fusion: a New Take on Retrieval-Augmented Generation

## Paper Meta
- Title: RAG-Fusion: a New Take on Retrieval-Augmented Generation
- Author: Zackary Rackauckas, Infineon Technologies, San Jose, CA
- Year: 2024 (inferred from arXiv 2402.03367)
- Venue: not reported in source; arXiv preprint
- Topic: misc
- Paper Slug: rag-fusion-2023
- arXiv: https://arxiv.org/abs/2402.03367
- PDF: 2402.03367.pdf
- Code Repo: not found locally; `repo/` is empty
- Reading Source: TeX / source

## TL;DR
- This is an application report on an Infineon product-information chatbot, not a broad benchmark paper.
- RAG-Fusion improved answer richness over traditional RAG in manual evaluations, especially for engineer, sales, and customer questions.
- The main trade-off was latency: the paper measured RAG-Fusion as 1.77x slower than the RAG baseline on repeated runs.

## Problem
- Engineers, account managers, and customers needed fast answers from long product selection guides, datasheets, and forum-like support material.
- Traditional RAG could retrieve relevant product text, but it often stayed too narrow for multi-part questions and missed broader context.
- The paper asks whether query expansion plus reciprocal rank fusion can produce more useful product Q&A without losing accuracy.

## Method
- Start with a user query, then ask an LLM to generate multiple related search queries from that prompt.
- Retrieve documents for the original and generated queries, then fuse the ranked lists with reciprocal rank fusion using the score form `1 / (rank + k)`.
- Send the original query, the generated queries, and the fused documents to the LLM to produce the final answer.
- Before testing, the author normalized prompts by fixing spelling and grammar, converting statements into questions, and splitting multi-part questions into single queries.
- The paper frames the chatbot around Infineon product documentation, especially MEMS microphones and MOSFETs.

## Benchmarks / Datasets
| Source / Task | Metric | Notes |
|---|---|---|
| Infineon developer community questions | manual answer quality | Used for engineer-facing technical questions and troubleshooting examples |
| Sales and customer prompts over product docs | manual answer quality | Used to test account-manager and customer-facing use cases |
| Repeated runtime runs on one query | seconds | Ten back-to-back runs compared RAG-Fusion against traditional RAG |

## Baselines
| Baseline | Type | Why Important | Notes |
|---|---|---|---|
| Traditional RAG chatbot | Retrieval-augmented chatbot | Primary comparison point for quality and latency | Uses the same product-document setting but without query expansion and RRF |

## Main Results
| Finding | Evidence |
|---|---|
| Engineer-facing answers improved in breadth | The IM72D128 IP-rating example returned the correct IP57 answer and added explanatory context about sealing and durability. |
| Sales-facing answers were especially strong | The bot handled a 100V OptiMOS Linear FET for Power over Ethernet prompt by combining product facts with sales-oriented framing. |
| Customer-facing answers were useful for product fit | The outdoor surveillance camera example concluded the IM72D128 microphone was a good fit based on product properties. |
| RAG-Fusion was slower than RAG | Average runtime was 34.62 s for RAG-Fusion versus 19.52 s for RAG, about 1.77x slower. |

## Ablations / Analysis
- The paper attributes most of the latency to the second LLM call, not to retrieval or reciprocal rank fusion itself.
- Even long prompts of 70+ words reportedly generated multiple queries in under 5 seconds, while the final answer call took much longer.
- The author argues that query quality strongly affects relevance: when the generated queries drift, the final answer can drift too.
- Human evaluation on accuracy, relevance, and comprehensiveness was preferred because generic text metrics do not match open-ended product support tasks well.
- The paper mentions RAGElo and Ragas as candidate evaluation toolkits, but treats them as still needing adaptation to this setting.

## Implementation Clues
- The implementation pattern is query expansion plus reciprocal rank fusion over a product-document store.
- The paper implies the retrieval corpus contains datasheets, product selection guides, and forum solutions.
- Query preprocessing is part of the workflow and mattered for the examples that worked well.
- The local `repo/` directory is empty, so there are no code files here to map the paper into an implementation.

## Limitations
- RAG-Fusion was measurably slower than the simpler RAG baseline.
- The system can go off topic when generated queries do not match the original intent closely enough.
- It does not reliably produce firm negative answers when the documents do not contain the answer.
- Manual evaluation is practical for this paper, but not scalable as a general benchmark protocol.
- The paper notes that translating user questions from other languages into English can lose context.

## Takeaways
- RAG-Fusion is a better fit when breadth and completeness matter more than raw response time.
- For product support, the method is useful because one user question often contains multiple implicit sub-questions.
- The best results came from questions where prompt wording, retrieval, and answer intent stayed aligned.
- The approach is strongest as a support assistant for engineers, sales teams, and customers rather than as a pure factual lookup tool.

## Open Questions
- How many generated queries is the best trade-off between relevance and latency?
- Can prompt engineering be moved from the user side into the system side?
- Can the chatbot be extended to Japanese and Mandarin without losing intent?
- Can multimodal datasheets be represented more faithfully for retrieval?
- Can the system give clearer negative answers when the evidence is absent?

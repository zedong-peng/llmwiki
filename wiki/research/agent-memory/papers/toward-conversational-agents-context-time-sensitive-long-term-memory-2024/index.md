---
title: "Toward Conversational Agents with Context and Time Sensitive Long-term Memory"
domain: research
area: misc
type: paper
status: processed
updated: 2026-04-19
tags: [paper, misc, conversational-agents, long-term-memory, retrieval, temporal-reasoning]
---
# Toward Conversational Agents with Context and Time Sensitive Long-term Memory

## Paper Meta
- Authors: Nick Alonso, Tomás Figliolia, Anthony Ndirango, Beren Millidge
- Year: 2024
- Venue: not reported in source
- Topic: misc
- Paper Slug: `toward-conversational-agents-context-time-sensitive-long-term-memory-2024`
- arXiv: https://arxiv.org/abs/2406.00057
- PDF: `2406.00057.pdf`
- Reading source: TeX in `source/extracted/main.tex`
- Code repo: not available locally

## TL;DR
- The paper argues that conversational memory retrieval is harder than standard RAG because chat history needs both time-aware lookup and disambiguation of pronouns/demonstratives.
- It builds a benchmark on LoCoMo dialogues by adding explicit time stamps per response, selecting the 12 longest dialogues, and generating three query families: time-only, ambiguous time-only, and time+content.
- The proposed retrieval pipeline combines query rewriting, a meta-data classifier, chain-of-table style table lookup, and semantic retrieval; this is the strongest system in the paper.

## Problem
- Standard RAG benchmarks mostly assume static corpora such as Wikipedia, so they do not test retrieval from long conversational logs where the user asks for "that thing we discussed yesterday" or "the third conversation on Tuesday."
- Two failure modes matter here: time/event metadata queries that require ordering or date lookup, and ambiguous questions whose meaning depends on preceding context.
- The paper positions these as core retrieval problems for future conversational agents with persistent memory.

## Dataset / Benchmark
| Component | Value | Notes |
|---|---:|---|
| Source dataset | LoCoMo dialogues | Built on the released long-form dialogue set |
| Dialogues used | 12 | The 12 longest dialogues were kept |
| Added padding session | ~4,000 tokens | Appended to each selected dialogue, but never queried |
| Extra timestamps | per response | Estimated from speech-rate assumptions |
| Time-based question families | 11 | Earlier today, date span, dates, day span, last day, month, relative day, relative month, relative session, session span, session |
| Unambiguous time questions | 2,134 | Total across the appendix table |
| Ambiguous time questions | 1,944 | Total across the appendix table |
| Time+content questions | 177 | Multi-hop questions using speaker, date/session, and topic cues |

## Method
- The memory store is represented as a table with response-level meta-data such as speaker, day, week, date, time, session index, and response index, plus a content pointer into the semantic vector store.
- A classifier first decides whether the query needs meta-data retrieval, semantic retrieval, or both, which avoids wasting semantic search on purely temporal questions.
- If meta-data is needed, the system uses a chain-of-table style function sequence with `f_value(column_name, values)` and `f_between(column_name, [start, end])` to narrow the table.
- If semantic retrieval is needed, the system runs vector search on the reduced table; if the query is ambiguous, it first rewrites the query using few-shot prompting.

## Main Results
### Unambiguous time-based and time+content queries
| Method | Time Recall | Time F2 | Time+Content Recall | Time+Content F2 | Average Recall | Average F2 |
|---|---:|---:|---:|---:|---:|---:|
| Semantic (k=10) | 2.01 | 2.32 | 15.43 | 5.62 | 8.72 | 3.97 |
| Semantic (k=20) | 3.91 | 4.21 | 24.29 | 5.19 | 14.10 | 4.70 |
| Semantic (k=30) | 5.82 | 5.89 | 29.43 | 4.43 | 17.62 | 5.16 |
| Semantic w/ meta-data (k=10) | 2.51 | 2.90 | 37.83 | 13.68 | 20.17 | 8.29 |
| Semantic w/ meta-data (k=20) | 5.02 | 5.43 | 51.26 | 10.85 | 28.14 | 8.14 |
| Semantic w/ meta-data (k=30) | 7.47 | 7.55 | 56.40 | 8.43 | 31.93 | 7.99 |
| CoTable+Semantic (hMistral7b) | 93.95 | 87.67 | 65.30 | 22.69 | 79.62 | 55.18 |
| CoTable+Semantic (GPT-3.5) | 90.47 | 78.34 | 90.17 | 32.19 | 90.32 | 55.27 |

- Pure semantic retrieval is extremely weak on time-only queries because embeddings do not encode the relevant metadata.
- Adding metadata into the text helps somewhat, but it still does not solve temporal lookup.
- The combined CoTable+Semantic system is the clear winner on both recall and F2.

### Ambiguous time-based queries
| Query handling | hMistral Recall | hMistral F2 | GPT-3.5 Recall | GPT-3.5 F2 |
|---|---:|---:|---:|---:|
| Original query | 2.93 | 2.35 | 10.62 | 3.12 |
| Context + query | 73.51 | 61.59 | 77.27 | 65.47 |
| Query rewrite | 89.43 | 81.05 | 83.90 | 72.56 |

- The original ambiguous query fails because the memory system cannot infer the referent.
- Concatenating a short context window helps a lot, but explicit query rewriting performs best overall.
- For this task, query rewriting beats naive context stuffing even when the latter already provides the missing antecedents.

### Meta-semantic classifier ablation
| Method | Time Recall | Time F2 | Time+Content Recall | Time+Content F2 | Average Recall | Average F2 |
|---|---:|---:|---:|---:|---:|---:|
| CoTable+Semantic hMistral7b w/ classification | 93.95 | 87.67 | 65.30 | 22.69 | 79.62 | 55.18 |
| CoTable+Semantic hMistral7b w/o classification | 42.26 | 33.11 | 69.07 | 28.29 | 18.82 | 8.01 |
| CoTable+Semantic GPT-3.5 w/ classification | 90.47 | 78.34 | 90.17 | 32.19 | 90.32 | 55.27 |
| CoTable+Semantic GPT-3.5 w/o classification | 89.78 | 75.25 | 63.10 | 24.52 | 76.44 | 49.88 |

- The classifier mainly matters because the model otherwise overuses content search on questions that only need metadata.
- The paper reports the biggest gain for hMistral on time-only questions and for GPT-3.5 on time+content questions.

## Implementation Clues
- The system is designed around low-cost retrieval rather than long-context generation, so it tries to reduce the search space before semantic lookup.
- The appendix says experiments run locally on one L40 per run, except when using GPT-3.5.
- Semantic retrieval uses one vector per response and flat cosine search with Faiss.
- The authors use greedy sampling for both chain-of-table generation and meta-semantic classification.

## Limitations
- Only two LLMs were tested: Mistral-Hermes-7b and GPT-3.5-turbo.
- The embedding model is small, so better embeddings might improve absolute performance even if the ranking of methods stays similar.
- The benchmark focuses mainly on single-hop time questions, with time+content questions serving as the multi-hop case.
- The paper does not create ambiguous versions of the time+content questions.

## Takeaways
- Conversational memory retrieval is not just "RAG on chat logs"; time and ambiguity create distinct retrieval problems.
- A table-first retrieval stack is effective when the query is metadata-heavy, and query rewriting is useful when the referent is underspecified.
- The most important design pattern here is hybrid memory: metadata filtering, semantic retrieval, and disambiguation should be separate stages.

## Open Questions
- Would stronger open-source LLMs reduce the gap between GPT-3.5 and hMistral on the ambiguous-query task?
- How much of the gain comes from the classifier versus the chain-of-table functions themselves?
- Would the same approach work as well on real user chat logs instead of synthetic dialogues?

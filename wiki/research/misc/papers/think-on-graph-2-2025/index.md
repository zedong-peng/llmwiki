---
title: "Think-on-Graph 2.0: Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation"
domain: research
area: misc
type: paper
status: processed
updated: 2026-04-19
tags: [paper, misc, rag, knowledge-graph, reasoning]
---
# Think-on-Graph 2.0: Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation

## Paper Meta
- Title: Think-on-Graph 2.0: Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation
- Authors: Shengjie Ma, Chengjin Xu, Xuhui Jiang, Muzhi Li, Huaren Qu, Cehao Yang, Jiaxin Mao, Jian Guo
- Venue: ICLR 2025
- Year: 2025
- Paper Slug: think-on-graph-2-2025
- arXiv: https://arxiv.org/abs/2407.10805
- PDF: 2407.10805.pdf
- Code Repo: https://github.com/IDEA-FinAI/ToG-2
- Reading Source: TeX / source

## TL;DR
- ToG-2 is a training-free KG x text RAG framework that alternates graph search and document retrieval.
- The key idea is tight coupling: KG traversal narrows candidate entities, while entity contexts from documents refine graph search.
- On GPT-3.5-turbo, it is best on 6 of 7 reported knowledge-intensive benchmarks, with especially strong gains on multi-hop QA.
- It also improves smaller LLMs substantially, which suggests the retrieval loop compensates for knowledge and reasoning bottlenecks.

## Problem
- Text-only RAG often finds semantically similar passages but misses structured relations between entities.
- KG-only RAG captures relations but usually lacks the detail needed for complex reasoning.
- Prior hybrid systems combine text and KGs loosely, but do not let one source improve retrieval in the other source.

## Method
- The pipeline starts with entity linking and a topic-prune step to select initial topic entities from the question.
- Each iteration first does knowledge-guided graph search: relation discovery, relation prune, and entity discovery on the KG.
- Retrieved candidate entities then drive context retrieval from associated documents; chunks are scored with a DRM using the question plus a triple sentence derived from the current candidate relation.
- Context-based entity prune uses the top scored chunks to choose the next topic entities, so document evidence reshapes the next graph step.
- After each round, the LLM either answers from the current triple paths and contexts or emits clues and continues until depth limit `D`.

## Datasets / Benchmarks
| Dataset | Task | Metric | Notes |
|---|---|---|---|
| WebQSP | multi-hop KBQA | EM | full Wikipedia + Wikidata setting |
| AdvHotpotQA | multi-hop document QA | EM | challenging HotpotQA subset |
| QALD-10-en | multi-hop KBQA | EM | linked data question answering |
| FEVER | fact verification | Acc. | Wikipedia + Wikidata setting |
| Creak | commonsense fact verification | Acc. | Wikidata-based verification |
| Zero-Shot RE | slot filling | EM | knowledge-intensive relation extraction |
| ToG-FinQA | domain QA over Chinese financial statements | EM | 17,013 docs, 671,806 entities, 565,994 edges, 97 QA pairs |

## Main Results
| Dataset | ToG-2 | Best baseline in paper | Notes |
|---|---:|---:|---|
| WebQSP | 81.1 EM | 77.6 CoK | +4.93 over ToG, strong multi-hop gain |
| AdvHotpotQA | 42.9 EM | 35.4 CoK | +16.6 over ToG |
| QALD-10-en | 54.1 EM | 50.2 ToG | +3.85 over ToG |
| FEVER | 63.1 acc (3-shot), 59.7 acc (6-shot) | 63.5 CoK (3-shot) | competitive but not top overall |
| Creak | 93.5 acc | 93.8 ToG | essentially tied with ToG |
| Zero-Shot RE | 91.0 EM | 88.0 ToG | +3.0 over ToG |
| ToG-FinQA | 34.0 EM | 14.0 ToG, 6.2 GraphRAG, 0 Vanilla RAG | domain-specific gap is large |

## Ablations / Analysis
- Backbone scaling: ToG-2 lifts Llama-3-8B, Qwen2-7B, GPT-3.5-turbo, and GPT-4o on AdvHotpotQA, FEVER, and ToG-FinQA; weaker models benefit the most.
- Entity-pruning tools: BGE-Reranker is best among the tested pruning choices, with Minilm and BM25 also reasonably strong; the paper favors reranking for the best cost-quality balance.
- Width and depth: performance improves up to width 3 and depth 3, then saturates; broader search is not always better.
- Runtime: with combined relation pruning, ToG-2 needs at most `2D + (D-1) + 1` LLM calls, versus `2WD + D + 1` for ToG.
- Runtime comparison: on FEVER and AdvHotpotQA, relation pruning time drops to 45% of ToG and entity pruning time averages 68.7% of ToG.
- HotpotQA runtime: ToG-2 averages 27.3 s and 5.4 API calls, compared with ToG at 69.3 s and 16.3 calls.
- Threshold study: relation-prune thresholds 0.2 and 0.5 behave similarly, while 0.8 hurts performance.
- KG completeness: at 30% graph completeness, EM falls to 23 under default settings but can recover to 29 with a wider, shallower search (`W = 8`, `D = 2`).
- Manual analysis: on 50 AdvHotpotQA cases, doc-enhanced answers are most common at 41.94%, both-enhanced at 32.26%, triple-enhanced at 9.68%, and direct answers at 16.13%.
- Error analysis: the method reduces hallucinations, but false negatives and overcautious refusals remain a recurring issue.

## Implementation Clues
- Backbone LLMs used in the paper: GPT-3.5-turbo for main comparisons, plus GPT-4o, Llama3-8B, and Qwen2-7B in ablations.
- Default settings: `W = 3`, `D = 3`, relation-prune threshold `0.2`, and `K = 10` top chunks for entity scoring.
- Context retrieval uses BGE-embedding without fine-tuning.
- For most datasets, reasoning uses a 2-shot demonstration; FEVER uses 3-shot and 6-shot settings plus an initial self-consistency check.
- The paper says ToG-2 is training-free and plug-and-play across LLMs, KGs, and document corpora.
- No local repo files were present in `repo/`, so I did not read implementation code from a checked-out repository.

## Limitations
- The method still depends on incomplete KGs and noisy retrieval; the paper explicitly notes gaps, contradictions, and missing entity details.
- EM is an imperfect metric for these tasks, especially when aliases or answer granularity differ.
- The system can be too cautious and return false negatives on ambiguous questions.
- Some gains are limited by dataset quality, especially on Creak and on questions where the labels are not perfectly aligned with natural reasoning.

## Takeaways
- The main contribution is the tight coupling loop between KG traversal and document retrieval.
- The practical win is better deep retrieval without training a new retriever.
- The most consistent gains appear on multi-hop and domain-specific tasks where pure text RAG or pure KG RAG is weak.
- The method is most convincing when knowledge must be both structurally guided and textually grounded.

## Open Questions
- How well does the method scale if the KG is much less complete than the paper’s benchmark settings?
- Can the retrieval loop be made less cautious without reintroducing hallucinations?
- Would a stronger or domain-adapted retriever change the balance between graph search and context retrieval?
- How much of the gain comes from the coupling itself versus the specific pruning and reranking choices?

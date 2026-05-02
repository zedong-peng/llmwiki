---
title: "Comprehensive Comparison of RAG Methods Across Multi-Domain Conversational QA"
domain: research
area: misc
type: paper
status: processed
updated: 2026-04-19
tags: [paper, misc, conversational-qa, rag, retrieval]
---
# Comprehensive Comparison of RAG Methods Across Multi-Domain Conversational QA

## Paper Meta
- Title: Comprehensive Comparison of RAG Methods Across Multi-Domain Conversational QA
- Authors: Klejda Alushi, Jan Strich, Chris Biemann, Martin Semmann
- Year: 2026
- Venue: arXiv preprint; final venue not reported in the source
- Topic: misc
- Paper Slug: multi-turn-conversational-rag-2026
- arXiv: https://arxiv.org/abs/2602.09552
- PDF: 2602.09552.pdf
- Code Repo: https://github.com/Klejda-A/exp-rag
- Reading Source: TeX source (`source/extracted/main.tex` and `source/extracted/clean.bib`)
- Repo Read: `repo/README.md` only; local repo content is a placeholder in this folder
- PDF Fallback: not used

## TL;DR
- This paper is a controlled comparison of vanilla and advanced RAG methods for multi-turn conversational QA across eight datasets.
- HyDE is the strongest retriever overall, while Reranker is the most reliable answer-quality method in several datasets.
- Hybrid BM25 and Reranker consistently beat Vanilla RAG, but several advanced methods still fall back to or below the No-RAG baseline.
- Dataset structure and dialogue depth matter as much as method choice.

## Problem
- Most conversational QA studies evaluate one RAG method at a time and usually focus on single-turn settings.
- Multi-turn QA adds dialogue history, coreference, ellipsis, and topic shifts, which can break naive retrieval.
- The paper asks whether more complex RAG methods are actually better than straightforward sparse, dense, and reranking baselines.
- It also asks how retrieval quality changes as conversations get longer.

## Method
- The study compares two reference points: `No RAG` and `Oracle Context`.
- Basic methods are `Base RAG`, `Standard BM25`, `Hybrid BM25`, and `Reranker`.
- Advanced methods are `Query Rewriting`, `HyDE`, `HyDE + Reranker`, `Summarization`, and `SumContext`.
- Retrieval uses Chroma with `all-MiniLM-L6-v2` embeddings and cosine similarity.
- Experiments use EncouRAGe, Llama 3 8B Instruct, temperature `0`, max output `1000`, and context length `40,000`.
- Generator quality is measured with F1; retriever quality is measured with MRR@5 and Recall@k.

## Benchmarks / Datasets
| Dataset | Source | Contexts | QA pairs | Notable structure |
|---|---:|---:|---:|---|
| QuAC | Wikipedia | 26,315 | 7,350 | Teacher/student Wikipedia dialogue |
| SQA | Wikipedia | 185 | 3,010 | Table-based sequential questions |
| QReCC | Wikipedia | 19,275 | 2,790 | Rewritten conversational queries |
| TopiOCQA | Wikipedia | 169,231 | 2,510 | Topic switching every few turns |
| Doc2Dial | Social Welfare | 1,238 | 3,940 | User/agent dialogues grounded in public docs |
| DoQA | StackExchange | 395 | 1,790 | Domain forum conversations over cooking/travel/movies |
| CoQA | Mixed | 499 | 7,980 | Short answers from heterogeneous sources |
| INSCIT | Mixed | 29,497 | 502 | Mixed-initiative Wikipedia information seeking |

- The benchmark comes from ChatRAG-Bench and the paper uses eight of its ten subsets.
- HybridDial is excluded because it lacks annotated ground-truth contexts.
- ConvFinQA is excluded because numeric arithmetic makes F1 unreliable.
- Total scale: 246,635 contexts and 29,872 QA pairs.

## Baselines
| Baseline | Role | Key point |
|---|---|---|
| No RAG | Lower bound | Tests the model without external evidence |
| Oracle Context | Upper bound | Uses gold context to estimate ceiling performance |
| Vanilla RAG | Main baseline | Original retrieve-then-generate pipeline |
| Standard BM25 | Lexical baseline | Checks pure term-overlap retrieval |
| Hybrid BM25 | Sparse+dense | Combines lexical and semantic retrieval |
| Reranker | Cross-encoder rerank | Reorders candidates after initial retrieval |

## Main Results
| Dataset | Best F1 | Best MRR@5 |
|---|---:|---:|
| QuAC | Reranker 29.2 | Hybrid BM25 44.6 |
| SQA | Reranker 51.3 | Reranker 71.0 |
| QReCC | HyDE 42.2 | HyDE 49.0 |
| TopiOCQA | HyDE 43.5 | HyDE 25.1 |
| Doc2Dial | Reranker 28.7 | HyDE 57.5 |
| DoQA | Hybrid BM25 36.9 | Reranker 93.1 |
| CoQA | Reranker 36.7 | HyDE 86.6 |
| INSCIT | HyDE 25.9 | HyDE 25.2 |

- `Hybrid BM25` improves F1 slightly over `Vanilla RAG` on every dataset in the reported table.
- `HyDE` is the strongest retrieval method overall, winning MRR@5 on 5 of 8 datasets.
- `Reranker` is the most consistent final-answer method across the easier and medium-complexity datasets.
- `Query Rewriting` is unstable and can fall below `No RAG` on INSCIT, QReCC, and TopiOCQA.
- `Summarization` and `SumContext` often reduce retrieval quality, suggesting that compression can remove useful context.
- `No RAG` ranges from F1 19.0 to 35.9, while `Oracle Context` ranges from 37.0 to 83.9.

## Ablations / Analysis
- Conversation-turn analysis is mixed rather than monotonic.
- INSCIT and TopiOCQA degrade as turn count increases, which matches their high context-to-question ratios and topic-switching behavior.
- CoQA and SQA improve with more context, suggesting that stable conversational history helps when the topic stays aligned.
- QReCC, QuAC, DoQA, and Doc2Dial are comparatively flatter through early turns, but QReCC and QuAC weaken later.
- F1 and MRR are positively correlated overall, but the correlation is weak or negative for SQA and DoQA.
- Spearman rho ranges from `0.874` on TopiOCQA to `-0.157` on DoQA.

## Implementation Clues
- Local execution uses EncouRAGe plus `vLLM` and MLflow.
- The embedding store is Chroma with Sentence Transformers `all-MiniLM-L6-v2`.
- Inference is reported on an NVIDIA RTX A6000 with 48 GB memory.
- The paper reports one run per method/dataset because repeated runs produced negligible differences.
- The appendix adds Gemma 3 27B results and says the trends align with the main table.
- The local repo directory here is not a real code checkout; it contains only a placeholder README, so no implementation details were recoverable from code.

## Limitations
- The method and dataset space is heterogeneous, so preprocessing and prompt formatting are dataset-specific.
- Very large context pools make it harder to retrieve the gold passage, especially for TopiOCQA, QuAC, and INSCIT.
- Summarization can erase key evidence instead of filtering noise.
- The paper does not claim a single universally best RAG strategy.

## Takeaways
- In conversational QA, retrieval strategy matters more than architectural complexity.
- Simple combinations such as Hybrid BM25 and reranking are often the safest improvements over Vanilla RAG.
- HyDE is strong when semantic reformulation helps retrieval, but it does not always translate into the best answer F1.
- Dataset structure should drive method choice; topic switching and long histories need different retrieval behavior than stable dialogues.

## Open Questions
- Would history truncation or metadata-aware grouping help the hardest datasets more than additional RAG complexity?
- How much of the error comes from retrieval failure versus answer-format mismatch?
- Do these trends hold for other generators beyond Llama 3 8B Instruct and Gemma 3 27B?

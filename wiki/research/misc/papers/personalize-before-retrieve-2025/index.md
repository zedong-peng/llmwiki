---
title: "Personalize Before Retrieve: LLM-based Personalized Query Expansion for User-Centric Retrieval"
domain: research
area: misc
type: paper
status: processed
updated: 2026-04-19
tags: [paper, misc, query-expansion, personalized-retrieval]
---
# Personalize Before Retrieve: LLM-based Personalized Query Expansion for User-Centric Retrieval

## Paper Meta
- Title: Personalize Before Retrieve: LLM-based Personalized Query Expansion for User-Centric Retrieval
- Authors: Yingyi Zhang, Pengyue Jia, Derong Xu, Yi Wen, Xianneng Li, Yichao Wang, Wenlin Zhang, Xiaopeng Li, Weinan Gan, Huifeng Guo, Yong Liu, Xiangyu Zhao
- Year: 2025
- Venue: not reported; source uses an AAAI 2026 template
- Topic: misc
- Paper Slug: personalize-before-retrieve-2025
- arXiv: https://arxiv.org/abs/2510.08935
- PDF: 2510.08935.pdf
- Code Repo: https://github.com/Applied-Machine-Learning-Lab/PBR-code
- Reading Source: TeX / source
- Local repo snapshot: not found in `repo/`

## TL;DR
- PBR personalizes query expansion before retrieval by combining style-aware pseudo feedback with a graph-based semantic anchor over each user's corpus.
- On PersonaBench, the method reaches 0.4527 R@5 and 0.3819 N@5 averaged over three retrievers, beating ThinkQE's 0.4098 / 0.3484.
- On LongMemEval, PBR improves top-1 retrieval on both sparse and dense memory settings and remains statistically significant over the best baseline.

## Problem
- Standard query expansion methods treat all users the same, even though identical queries can reflect different preferences, background knowledge, and expression styles.
- Personalized retrieval needs two things at once: a query expansion that preserves user-specific style, and an anchor that grounds the query in the structure of the user's own corpus.
- The paper frames this as personalized query expansion before retrieval, rather than trying to fix personalization after the retriever has already ranked documents.

## Method
- PBR has three pieces: P-PRF, P-Anchor, and a fusion module that combines them into the final personalized query vector.
- P-PRF first selects the top-$k_1$ history items similar to the query, then asks an LLM to generate pseudo utterances and pseudo reasoning that imitate the user's expression pattern.
- P-Anchor builds a semantic graph over the user's history, keeps edges above a similarity threshold $\theta$ with top-$k_2$ neighbors, and applies PageRank to get a corpus anchor vector.
- Fusion weights the pseudo utterance and pseudo reasoning by their similarity to the mean of the query and anchor vectors, then adds the resulting personalization shift to the original query embedding.
- Final retrieval is FAISS-based nearest-neighbor search over the user corpus with the fused query vector.

## Benchmarks / Datasets
| Dataset / Benchmark | Task | Metric | Notes |
|---|---|---|---|
| PersonaBench | Personalized retrieval over heterogeneous private corpora | R@5, N@5 | 6 users; 263 queries total; 527 corpus items total |
| LongMemEval-s | Long-term memory retrieval in sparse histories | R@1, N@1, R@3, N@3, R@5, N@5 | 500 questions; 25,112 memories total; about 50 memories per question |
| LongMemEval-m | Long-term memory retrieval in dense histories | R@1, N@1, R@3, N@3, R@5, N@5 | 500 questions; 250,948 memories total; about 502 memories per question |

## Baselines
| Baseline | Type | Why Important | Notes |
|---|---|---|---|
| Base | No expansion | Lower bound | Static query retriever |
| HyDE | Hypothetical document generation | Strong zero-shot QE baseline | LLM-generated answer-style expansion |
| Query2Term | Keyphrase expansion | Lightweight lexical reformulation | Uses rationale before answer |
| MILL | Multi-level logical expansion | Reasoning-heavy QE baseline | Generates sub-queries and passages |
| CoT | Chain-of-thought expansion | Tests whether reasoning helps retrieval | Step-by-step expansion prompt |
| ThinkQE | Reasoning-based QE | Strongest non-personalized baseline in the paper | Best baseline on PersonaBench average |

## Main Results
| Dataset / Benchmark | Metric | Baseline | Ours | Gain / Delta | Notes |
|---|---|---|---|---|---|
| PersonaBench overall average | R@5 / N@5 | 0.4098 / 0.3484 | 0.4527 / 0.3819 | +0.0429 / +0.0335 | Best baseline is ThinkQE; two-sided t-test p<0.05 |
| PersonaBench, multi-qa-MiniLM-L6-cos-v1 | R@5 / N@5 | 0.4791 / 0.3902 | 0.5035 / 0.4201 | +0.0244 / +0.0299 | Best scores on the three-backbone comparison table |
| LongMemEval-s, bge-base-en-v1.5 | R@1 / N@1 | 0.2267 / 0.8807 | 0.2315 / 0.8902 | +0.0048 / +0.0095 | Best baseline in the table is Base for R@1 and ThinkQE for N@1 |
| LongMemEval-m, bge-base-en-v1.5 | R@1 / N@1 | 0.1384 / 0.6072 | 0.1408 / 0.6205 | +0.0024 / +0.0133 | PBR is statistically significant over the best baseline |

## Ablations / Analysis
- Removing P-PRF hurts the most. On PersonaBench with all-MiniLM-L6-v2, overall R@5 drops from 0.4516 to 0.2860 and N@5 from 0.3855 to 0.2449.
- Removing P-Anchor is milder but still consistent. On the same setting, overall R@5 drops from 0.4516 to 0.4382 and N@5 from 0.3855 to 0.3729.
- The strongest configuration uses both style and structure: removing both modules falls back to the Base row in the ablation table.
- Hyperparameter sensitivity on LongMemEval-s shows that k1 = 5 is a good default, while k1 = 10 gives the best recall/ndcg in the appendix table.
- P-Anchor is most stable around theta in [0.65, 0.75] and k2 = 5; overly large propagation starts to flatten or slightly hurt performance.
- The appendix reports generation EM of 42.6% for PBR on LongMemEval-s, above CoT at 41.0% and ThinkQE at 41.8%.
- The visualization section reports stronger user separation for PBR than HyDE or the original query.

## Implementation Clues
- The paper evaluates three retrieval backbones: multi-qa-MiniLM-L6-cos-v1, all-MiniLM-L6-v2, and bge-base-en-v1.5.
- It uses an advanced LLM for query expansion, with temperature 0, and repeats experiments 5 times.
- Default PBR settings are k1 = 5, m = 5, theta = 0.75, and k2 = 10 for PersonaBench and LongMemEval-s; LongMemEval-m uses k2 = 50.
- Retrieval is done with FAISS and Euclidean distance over embeddings.
- Appendix timing shows the extra graph-building step is negligible, and PBR adds about 0.18 s over ThinkQE mainly from generation.
- The source only was read locally; no usable repository snapshot was present in `repo/`, so repo-level implementation details are not available from this ingest.

## Limitations
- The paper evaluates on two personalized retrieval benchmarks; broader task coverage is left to future work.
- The main gain depends on LLM-generated pseudo utterances and pseudo reasoning, so quality and cost are tied to the generator.
- P-Anchor can over-propagate; the paper reports small drops when graph expansion becomes too broad.
- The paper does not report a locally available code snapshot in this workspace, so implementation-level verification is limited to the TeX source.

## Takeaways
- Personalized query expansion is the core lever here, not a post-retrieval reranker.
- Style imitation and structural anchoring contribute different signal types and are both needed for the strongest results.
- The gains are largest on ambiguous, personal queries, but the method also helps long-term factual memory retrieval.
- The method is simple enough to be practical: the added graph step is tiny, and the main extra cost is the LLM generation step.

## Open Questions
- How well does PBR transfer to domains where user histories are short, noisy, or not semantically coherent?
- Would a learned retriever or reranker reduce the need for manual threshold tuning in P-Anchor?
- Can the pseudo utterance and pseudo reasoning generators be trained to reduce generation latency without losing personalized signal?

---
title: "Query Decomposition for RAG: Balancing Exploration-Exploitation"
domain: research
area: misc
type: paper
status: processed
updated: 2026-04-19
tags: [paper, misc, bandit, rag, query-decomposition]
---
# Query Decomposition for RAG: Balancing Exploration-Exploitation

## Paper Meta
- Title: Query Decomposition for RAG: Balancing Exploration-Exploitation
- Authors: Roxana Petcu, Kenton Murray, Daniel Khashabi, Evangelos Kanoulas, Maarten de Rijke, Dawn Lawrie, Kevin Duh
- Year: 2025
- Venue: not reported; arXiv preprint
- Topic: misc
- Paper Slug: query-decomposition-as-bandit-2025
- arXiv: https://arxiv.org/abs/2510.18633
- PDF: 2510.18633.pdf
- Code Repo: not reported
- Reading Source: TeX / source
- Source Read: yes
- Repo Read: no
- PDF Fallback: no

## TL;DR
- The paper reframes query decomposition and document retrieval for RAG as a multi-armed bandit problem, where each sub-query is an arm and each retrieved document updates a posterior over sub-query utility.
- The strongest recurring signal is rank-aware Bernoulli reward modeling: using binary relevance plus top-k rank information improves document precision, alpha-nDCG, and downstream report generation.
- Hierarchical correlated bandits help when sub-queries are decomposed in multiple levels, especially under small budgets.

## Problem
- Standard RAG query decomposition often retrieves a fixed number of documents per sub-query, which can waste budget on irrelevant evidence and still miss useful material.
- The paper targets the trade-off between exploration across sub-queries and exploitation within promising sub-queries.
- The concrete question is how to allocate a limited retrieval budget across decomposed queries so that relevance, diversity, and downstream generation quality improve.

## Method
- The core formulation treats each sub-query as a bandit arm and each retrieved document as the next observation from that arm's ranked list.
- The paper uses Thompson sampling in both discrete and continuous forms, with Beta-Bernoulli posteriors for binary relevance and Gaussian posteriors for continuous scores.
- The main reward variants are rank-aware and diversity-aware: top-k Bernoulli averaging, rank discounting, diversity weighting with cosine similarity, and a small UCB-style exploration term.
- For hierarchical decomposition, informative parent sub-queries are expanded into correlated child arms by inheriting the parent's posterior with factor `lambda`.

## Benchmarks / Datasets
| Dataset / Benchmark | Task | Metric | Notes |
|---|---|---|---|
| NeuCLIR24 | One-level query decomposition and document selection for RAG | precision, alpha-nDCG, report-generation metrics | Complex multilingual user requests; translated English docs; entire human-annotated nugget partition; average query length `51.95 ± 19.46` words; `k=16` sub-queries and `n=10` docs per sub-query |
| ResearchyQuestions | Hierarchical sub-query selection with correlated bandits | precision, alpha-nDCG | `100k` complex Bing questions; two-level decomposition; corpus built from all relevant docs; BM25 top-10 retrieval; final eval set filtered to `140` instances |

## Baselines
| Baseline | Type | Why Important | Notes |
|---|---|---|---|
| Random | retrieval baseline | Lower bound for budgeted selection | Samples arms and documents uniformly |
| Random rank-aware | retrieval baseline | Tests whether rank alone helps | Uniform arm choice, document chosen from rank |
| `epsilon`-greedy | bandit baseline | Simple exploitation-first policy | Exploits after positive observations |
| Bernoulli | bandit baseline | Binary relevance without extra shaping | Beta-Bernoulli posterior |
| Bernoulli UCB | bandit baseline | Adds exploration pressure | UCB bonus on Bernoulli reward |
| Bernoulli top-k | bandit baseline | Tests rank-window information | Reported for `k=4` and `k=5` |
| Bernoulli rank-aware | bandit baseline | Uses discounted rank signal | Reward divided by `log2(n + 2)` |
| Gaussian | continuous-score baseline | Compares against embedding/ranking scores | Uses RFF or ColBERT-style scores |
| Diversity / Diversity Concave | retrieval baseline | Tests novelty-aware selection | Cosine-similarity novelty shaping |
| Bernoulli top-k UCB diversity | combined policy | Best mixed heuristic in the paper | Combines top-k, diversity, and UCB |

## Main Results
| Dataset / Benchmark | Metric | Baseline | Ours | Gain / Delta | Notes |
|---|---|---|---|---|---|
| Overall claim | document-level precision | not reported | not reported | `35%` gain | Abstract-level summary using rank information and human judgments |
| Overall claim | alpha-nDCG | not reported | not reported | `15%` increase | Abstract-level summary |
| NeuCLIR24 | precision | exploitation-only: `0.57`; exploration-only: `0.55` | bandit rewards | better than both extremes | Precision improves with reward policies; rank information helps noticeably |
| NeuCLIR24 | alpha-nDCG | random: `0.411-0.479` depending on `k` | Bernoulli top-k / UCB variants | best values around `0.555` | Bernoulli `k=5` reaches `0.555` at `K=20`; `epsilon`-greedy is strong at smaller budgets |
| NeuCLIR24 report generation | citation support / nugget coverage / sentence support | full set: `0.788 / 0.461 / 0.780` | Bernoulli top-k, top-k UCB div. | `6.0%-9.9%`, `6.7%-8.5%`, `7.3%-9.6%` gains | Best downstream report-quality results come from rank-aware Bernoulli policies |
| ResearchyQuestions | precision at `b=10%` | serialized Bernoulli: `0.305`; serialized top-k `k=5`: `0.303` | hierarchical Bernoulli: `0.371`; hierarchical top-k `k=5`: `0.401` | up to `24%` boost over serialized | Hierarchy-aware bandits help most under small budgets |

## Ablations / Analysis
- Rank information is consistently useful: the paper reports that Bernoulli models using top-k documents outperform plain Bernoulli and most alternatives on both datasets.
- UCB helps in some settings, but the strongest gains come from combining rank information with binary relevance rather than from exploration bonuses alone.
- Diversity-aware rewards are present but do not consistently beat rank-aware Bernoulli variants.
- Hierarchical correlated bandits improve early-budget behavior by focusing effort on promising branches of the sub-query tree.

## Implementation Clues
- NeuCLIR uses LLM-generated decompositions with `k=16` sub-queries, then retrieves `n=10` documents per sub-query with a retriever stack combining PLAID-X, learned sparse retrieval, and a Qwen retriever.
- The paper repeats each experiment `1000` times and runs query decomposition `10` times per user request, averaging over `19 x 10 x 1000` experiments per budget.
- For the hierarchical setting, Bayesian search selected `n=4`, informativeness threshold `tau=0.77`, and inheritance factor `lambda=0.91`.
- The abstract says code is available on GitHub via an anonymous `4open.science` link, but no local repo was ingested here.

## Limitations
- The method depends on retriever quality, because bandit rewards are computed from retrieved documents.
- Performance depends on the true relevance distribution and the retrieval budget.
- The paper notes that sub-query regeneration can add noise, and that some settings may not have a predefined, bounded set of sub-queries.

## Takeaways
- Treating query decomposition as bandit allocation is a practical fit for sequential, budgeted retrieval.
- Binary relevance plus rank information is the most reliable pattern in the reported experiments.
- Correlated hierarchical bandits are most valuable when the query tree is sparse and the budget is tight.

## Open Questions
- How well would the same policies transfer to domains where relevance labels are weaker or much noisier?
- Would a learned retriever optimized jointly with the bandit policy reduce the dependence on the base search engine?
- How stable are the reported gains when the sub-query decomposition itself is generated by a different model or prompt?

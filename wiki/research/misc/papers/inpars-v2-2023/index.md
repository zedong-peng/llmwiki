---
title: "InPars-v2: Large Language Models as Efficient Dataset Generators for Information Retrieval"
domain: research
area: misc
type: paper
status: processed
updated: 2026-04-19
tags: [paper, retrieval, synthetic-data, beir, reranking, llm, inpars-v2]
---
# InPars-v2: Large Language Models as Efficient Dataset Generators for Information Retrieval

## Paper Meta
- Title: InPars-v2: Large Language Models as Efficient Dataset Generators for Information Retrieval
- Authors: Vitor Jeronymo, Luiz Bonifacio, Hugo Abonizio, Marzieh Fadaee, Roberto Lotufo, Jakub Zavrel, Rodrigo Nogueira
- Year: 2023
- Venue: arXiv preprint
- Topic: misc
- Paper Slug: inpars-v2-2023
- arXiv: https://arxiv.org/abs/2301.01820
- PDF: `2301.01820.pdf`
- Code Repo: https://github.com/zetaalphavector/InPars
- Reading Source: TeX (`source/extracted/main.tex`, `source/extracted/main.bbl`)
- Repo Read: yes (`repo/InPars/README.md`, `repo/InPars/legacy/inpars-v2/README.md`, `repo/InPars/legacy/inpars-v2/train_inpars.py`, `repo/InPars/legacy/inpars-v2/run_t5_3B_inpars.py`, `repo/InPars/inpars/filter.py`)
- PDF Fallback: not used

## TL;DR
- InPars-v2 is the BEIR-oriented refinement of [[inpars-2022]]: it replaces the proprietary generator with open-source GPT-J and replaces score-only filtering with monoT5-based reranker filtering.
- The core result is simple and important: a BM25 retrieval pipeline followed by monoT5-3B finetuned on InPars-v2 synthetic data reaches a new BEIR SOTA at the time of publication.
- The paper is short, but strategically important. It is one of the cleanest demonstrations that synthetic data quality, not just synthetic data quantity, is the bottleneck.
- For the current retrieval thread, this is the direct paper behind the "InPars-v2 was on the BEIR SOTA path" statement.

## Problem
- [[inpars-2022]] already showed that synthetic query generation can help retrieval, but it still relied on proprietary GPT-3 and a relatively weak filtering signal based on generation probabilities.
- The authors ask whether they can get similar or better BEIR gains with a reproducible open model and a stronger quality filter over generated query-document pairs.

## Method
- Query generation:
  - Use GPT-J 6B instead of GPT-3 Curie
  - For each BEIR dataset, sample up to 100k documents
  - Prompt GPT-J with 3 MS MARCO examples and the GBQ prompt from InPars-v1
  - Generate one synthetic query per sampled document
- Positive filtering:
  - Score all 100k synthetic query-document pairs with a monoT5-3B reranker already finetuned on MS MARCO
  - Keep only the top 10k pairs as positives
- Negative construction:
  - Use BM25 on the synthetic query
  - Randomly sample one document from the top 1000 retrieved results
- Training and evaluation:
  - Finetune monoT5-3B on MS MARCO for one epoch
  - Further finetune one reranker per BEIR dataset on the synthetic data
  - Retrieve with BM25 and rerank the top 1000 documents with the dataset-specific monoT5-3B model

## Benchmarks / Datasets
| Dataset / Benchmark | Role in Paper | Metric | Notes |
|---|---|---|---|
| BEIR | main benchmark | nDCG@10 | 18 datasets reported in the table |
| Promptagator subset average | comparison subset | avg. nDCG@10 | "Avg PrGator" aligns with datasets Promptagator reported |
| MS MARCO | initialization source | not primary target | monoT5 starts from MS MARCO-finetuned checkpoint |

## Baselines
| Baseline | Type | Why Important | Notes |
|---|---|---|---|
| BM25 | sparse retrieval | base retrieval stage | first anchor on all datasets |
| monoT5-3B (MS MARCO) | reranker | strong transfer baseline | before synthetic adaptation |
| InPars-v1 | synthetic-data reranker | direct predecessor | isolates value of reranker filtering |
| Promptagator | synthetic-data retriever | contemporaneous competitor | uses FLAN and task-specific prompts |
| RankT5 | reranker | strong ranking baseline | competitive but not fully open at the time |

## Main Results
| Setting | Metric | Score | Notes |
|---|---|---:|---|
| BM25 average on BEIR | avg. nDCG@10 | 0.424 | sparse baseline |
| monoT5-3B from MS MARCO | avg. nDCG@10 | 0.533 | strong generic reranker |
| monoT5-3B + InPars-v1 | avg. nDCG@10 | 0.539 | modest gain over v1 |
| monoT5-3B + InPars-v2 | avg. nDCG@10 | 0.545 | new SOTA claimed by paper |
| TREC-News | nDCG@10 | 0.490 | much higher than 0.458 from InPars-v1 |
| Climate-FEVER | nDCG@10 | 0.323 | much higher than 0.287 from InPars-v1 |
| Robust04 | nDCG@10 | 0.632 | higher than 0.610 from InPars-v1 |
| FEVER | nDCG@10 | 0.872 | strongest single-dataset gain in the table |

- The paper also reports:
  - `Avg PrGator`: BM25 0.417, monoT5 0.520, InPars-v1 0.523, InPars-v2 0.533, Promptagator 0.531, RankT5 0.536
- This matters because it shows InPars-v2 is stronger than Promptagator on the overlapping subset, but still roughly tied with RankT5 there.

## Ablations / Analysis
- The only method change versus v1 is strategically important:
  - better query generator
  - better filtering criterion
- The paper attributes its gains mainly to reranker-based filtering of synthetic pairs rather than to a radical architecture change.
- InPars-v2 improves most on datasets where generic transfer is weaker, such as TREC-News, Climate-FEVER, and Robust.
- Argument retrieval remains a weakness. Promptagator and RankT5 stay stronger on ArguAna and Touché because they use more tailored prompts or training designs.
- The authors explicitly note that a dataset-specific prompt can improve ArguAna by more than 10 nDCG@10 points in preliminary experiments, but they do not include the full follow-up here.

## Implementation Clues
- `repo/InPars/legacy/inpars-v2/README.md` is the most faithful implementation map for the paper, not the toolkit root README.
- `legacy/inpars-v2/train_inpars.py` loops over BEIR datasets, filters synthetic queries, builds triples, converts them into monoT5 input format, pushes files to GCS, and launches TPU training jobs dataset by dataset.
- `legacy/inpars-v2/run_t5_3B_inpars.py` prepares BM25 run pairs, shards large reranking inputs, uploads them to cloud storage, and dispatches TPU inference over the BEIR datasets.
- `repo/InPars/inpars/filter.py` exposes the method's core conceptual change in reusable form: `filter_strategy="reranker"` swaps out the original score-only selection for reranker-based filtering.
- The modern repo has two layers:
  - a historical `legacy/inpars-v2/` reproduction path close to the paper
  - a generalized `inpars/` toolkit that unifies v1 and v2 under one interface
- The repo README also points to released generated datasets and finetuned models, which makes this paper much more reproducible than many neighboring BEIR-SOTA claims.

## Limitations
- The paper is an arXiv note rather than a long archival conference paper, so many ablations and implementation details are compressed.
- The main system is still a BM25-plus-reranker pipeline, not an efficient first-stage dense retriever.
- Training one reranker per BEIR dataset is effective but less elegant than learning one truly universal retriever.
- Argument retrieval remains a hole in the approach.

## Takeaways
- InPars-v2 is important because it shows that better synthetic data curation can move BEIR more than swapping retriever architectures in isolation.
- It is one of the cleanest examples where "LLM-generated training data" became an actual benchmark-winning retrieval recipe rather than a speculative idea.
- If I need a compact citation for open-source synthetic-data generation improving BEIR, this is the paper.


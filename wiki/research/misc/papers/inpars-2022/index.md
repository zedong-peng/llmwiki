---
title: "InPars: Data Augmentation for Information Retrieval using Large Language Models"
domain: research
area: misc
type: paper
status: processed
updated: 2026-04-19
tags: [paper, retrieval, synthetic-data, beir, reranking, llm, inpars]
---
# InPars: Data Augmentation for Information Retrieval using Large Language Models

## Paper Meta
- Title: InPars: Data Augmentation for Information Retrieval using Large Language Models
- Proceedings Title Variant: InPars: Unsupervised Dataset Generation for Information Retrieval
- Authors: Luiz Bonifacio, Hugo Abonizio, Marzieh Fadaee, Rodrigo Nogueira
- Year: 2022
- Venue: SIGIR 2022 per repo citation; arXiv TeX snapshot uses the longer "Data Augmentation..." title
- Topic: misc
- Paper Slug: inpars-2022
- arXiv: https://arxiv.org/abs/2202.05144
- PDF: `2202.05144.pdf`
- Code Repo: https://github.com/zetaalphavector/InPars
- Reading Source: TeX (`source/extracted/main.tex`, `source/extracted/main.bbl`)
- Repo Read: yes (`repo/InPars/README.md`, `repo/InPars/inpars/generate.py`, `repo/InPars/inpars/filter.py`, `repo/InPars/inpars/generate_triples.py`)
- PDF Fallback: not used

## TL;DR
- InPars is one of the earliest strong papers on using large language models as synthetic query generators for IR instead of using them directly at inference time.
- The pipeline is simple: sample documents from the target corpus, few-shot prompt GPT-3 to generate likely relevant queries, keep the highest-confidence pairs, mine BM25 negatives, then finetune a reranker.
- In the unsupervised setting, the resulting monoT5 rerankers beat BM25, Contriever, and OpenAI Search baselines on several datasets; in the supervised transfer setting they also improve zero-shot results on Robust04 and TREC-COVID.
- For the current BEIR thread, this is a foundational paper because it establishes the "synthetic in-domain data beats pure zero-shot transfer" line that later systems such as [[inpars-v2-2023]] continue.

## Problem
- Neural IR systems benefit heavily from large supervised datasets such as MS MARCO, but many target domains do not have enough user queries and relevance labels.
- Using billion-parameter LLMs directly as retrievers or rerankers is too expensive for realistic retrieval workloads.
- The paper asks whether large LLMs can instead be used once, offline, to synthesize in-domain query-document supervision that is cheap to reuse during retrieval.

## Method
- InPars generates synthetic positive pairs `(q, d)` by prompting a large autoregressive LM with a document and a small few-shot prefix of query-document examples.
- The paper uses only 3 in-context examples and generates one query per sampled document.
- It scores each generated query by the average log-probability assigned during generation and keeps the top 10k query-document pairs out of 100k generated examples.
- Negatives are mined by issuing each synthetic query to BM25 and randomly sampling one document from the top 1000 retrieved documents.
- The final retriever is not a bi-encoder but a BM25-plus-reranking stack: BM25 retrieves 1000 candidates and monoT5 reranks them.
- Two prompt families are studied:
  - `Vanilla`: standard MS MARCO few-shot examples
  - `GBQ`: "Guided by Bad Questions", which explicitly contrasts weak and stronger questions to encourage more contextual synthetic queries

## Benchmarks / Datasets
| Dataset / Benchmark | Role in Paper | Metric | Notes |
|---|---|---|---|
| MS MARCO | in-domain supervised source and eval | MRR@10 | large web search training source |
| TREC-DL 2020 | reranking eval on MS MARCO corpus | MAP / nDCG@10 | deeper judgments than MS MARCO |
| Robust04 | zero-shot transfer eval | MAP / nDCG@20 | long-document news retrieval |
| NQ (BEIR version) | zero-shot transfer eval | nDCG@10 | Wikipedia QA retrieval |
| TREC-COVID (BEIR version) | zero-shot transfer eval | nDCG@10 | biomedical retrieval |
| FiQA (BEIR version) | zero-shot transfer eval | nDCG@10 | finance retrieval |

## Baselines
| Baseline | Type | Why Important | Notes |
|---|---|---|---|
| BM25 | lexical first-stage | default sparse baseline | strong zero-shot anchor |
| Contriever | unsupervised dense retrieval | dense pretraining baseline | compared in unsupervised setting |
| cpt-text | OpenAI embedding-style retriever | large-model dense baseline | another unsupervised point of comparison |
| OpenAI Search API | proprietary reranker | direct use of large LMs at inference | cost-heavy comparison |
| monoT5-220M / 3B on MS MARCO | supervised reranker | strong transfer baseline | measures added value of synthetic data |
| GPL / ColBERT-v2 / miniLM reranker | transfer baselines | context for zero-shot performance | only reported on some datasets |

## Main Results
| Setting | Metric | Baseline | InPars | Delta | Notes |
|---|---|---:|---:|---:|---|
| MS MARCO unsupervised | MRR@10 | BM25 0.1874 | monoT5-3B 0.2967 | +0.1093 | strong gain without manual labels |
| TREC-DL 2020 unsupervised | nDCG@10 | Curie Search 0.5422 | monoT5-3B 0.6612 | +0.1190 | smaller reranker beats larger API model |
| NQ unsupervised | nDCG@10 | Contriever 0.2580 | monoT5-3B 0.5133 | +0.2553 | large zero-shot gain |
| TREC-COVID unsupervised | nDCG@10 | BM25 0.6880 | monoT5-3B 0.7835 | +0.0955 | in-domain synthetic data matters |
| FiQA unsupervised | nDCG@10 | cpt-text 0.3970 | monoT5-3B 0.4103 | +0.0133 | smaller but positive gain |
| Robust04 supervised transfer | MAP | monoT5-3B 0.3876 | InPars 0.3967 | +0.0091 | best reported transfer result |
| TREC-COVID supervised transfer | nDCG@10 | monoT5-3B 0.7948 | InPars 0.8471 | +0.0523 | strongest reported zero-shot transfer |

## Ablations / Analysis
- Prompt choice matters. Vanilla prompts work best on MS MARCO-style retrieval, while GBQ prompts help more on out-of-domain collections.
- In-domain generation helps more for harder transfer datasets such as NQ and TREC-COVID than for MS MARCO itself.
- Larger rerankers benefit most from the synthetic data: monoT5-3B consistently beats the 220M version.
- Filtering is not a detail. The method explicitly relies on selecting high-confidence generated queries rather than training on all raw generations.
- The paper argues that cross-encoders benefit both from query-document interaction and from the diversity of the newly generated synthetic supervision.

## Implementation Clues
- `repo/InPars/inpars/generate.py` is the main query-generation entry point. It samples documents from a BEIR dataset or local corpus and calls the `InPars` generator with a selected prompt template and base model.
- `repo/InPars/inpars/filter.py` implements the key filtering step. It supports both score-based filtering from generation log-probabilities and reranker-based filtering, the latter becoming the default idea behind [[inpars-v2-2023]].
- `repo/InPars/inpars/generate_triples.py` mines negatives from BM25 results to build training triples after the positive synthetic pairs are selected.
- `repo/InPars/inpars/train.py`, `rerank.py`, and `evaluate.py` turn the paper into a reusable pipeline rather than a one-off script: generate synthetic queries, filter, build triples, finetune monoT5, rerank, then evaluate.
- The current repo is more of a post-paper toolkit than a frozen SIGIR artifact. It exposes both InPars-v1 and InPars-v2 style filtering under one interface.

## Limitations
- The original paper depends on proprietary OpenAI GPT-3 models for query generation, which hurts reproducibility and cost.
- The work is reranker-centric rather than first-stage retrieval-centric, so latency and throughput still depend on a reranking stage.
- The paper only evaluates a small subset of BEIR-style datasets, not the full 18-dataset BEIR benchmark.
- Synthetic queries can drift away from the target distribution, which the authors explicitly suspect for the slight MS MARCO degradation after extra synthetic finetuning.

## Takeaways
- InPars is an important paper because it turned "use LLMs for IR" into a practical offline data-generation recipe instead of an expensive online inference story.
- It is one of the clearest early examples where LLM-generated supervision improves zero-shot transfer in retrieval.
- If I need a historical root for BEIR-era synthetic query generation, this is the paper to cite before [[inpars-v2-2023]], Promptagator, or later synthetic-data retriever work.


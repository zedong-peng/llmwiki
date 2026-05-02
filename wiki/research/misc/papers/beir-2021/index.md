---
title: "BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models"
domain: research
area: misc
type: paper
status: processed
updated: 2026-04-21
tags: [paper, retrieval, benchmark, beir, zero-shot, bm25, dense-retrieval, reranking]
---
# BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models

## Paper Meta
- Title: BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models
- Authors: Nandan Thakur, Nils Reimers, Andreas Rücklé, Abhishek Srivastava, Iryna Gurevych
- Year: 2021
- Venue: NeurIPS 2021 Datasets and Benchmarks Track
- Topic: misc
- Paper Slug: beir-2021
- arXiv: https://arxiv.org/abs/2104.08663
- PDF: `2104.08663-beir.pdf`
- Code Repo: https://github.com/beir-cellar/beir
- Repo Lineage: paper-linked `https://github.com/UKPLab/beir`, now redirects to `beir-cellar/beir`
- Reading Source: TeX (`source/extracted/neurips2021.tex` + `source/extracted/neurips2021.bbl`)
- Repo Read: yes (`repo/beir/README.md`, `repo/beir/beir/datasets/data_loader.py`, `repo/beir/beir/retrieval/evaluation.py`, `repo/beir/beir/retrieval/search/lexical/bm25_search.py`, `repo/beir/beir/retrieval/search/dense/exact_search.py`)
- Important Later Source: AILog update `https://app.ailog.fr/en/blog/news/beir-benchmark-update`
- PDF Fallback: not used

## TL;DR
- BEIR is a benchmark and evaluation framework, not a new retriever. Its core contribution is 18 zero-shot retrieval datasets across 9 tasks plus a unified software stack and metric protocol.
- The paper's main empirical message is that strong in-domain MS MARCO performance does not predict zero-shot transfer. BM25 stays surprisingly competitive, while many dense retrievers degrade badly out of domain.
- The best average zero-shot performer is a BM25 plus cross-encoder reranker, followed by ColBERT and docT5query. Plain dense bi-encoders often lose to BM25 despite much stronger in-domain numbers.
- The paper also argues that benchmark construction matters: existing relevance pools are lexically biased, and this can systematically under-credit dense or semantic retrievers.

## Problem
- Retrieval papers were largely being evaluated in narrow, homogeneous settings, often on one task and one domain, especially MS MARCO-style passage retrieval.
- That makes it hard to answer the question that matters for real deployment: if a retriever is trained on one setup, how well does it transfer to different domains, query styles, and document types without retraining?
- Prior benchmarks such as MultiReQA and KILT were useful but still too narrow for broad zero-shot IR evaluation, either because they focused on one task family or because they stayed inside Wikipedia.
- The paper therefore targets a benchmark that is simultaneously diverse in task, domain, query/document form, and annotation process, while still exposing a common evaluation interface.

## Method
- The core "method" is benchmark design rather than a retrieval architecture. BEIR curates 18 English zero-shot evaluation datasets from 9 retrieval tasks, spanning Wikipedia, science, biomedical, finance, news, social media, and online communities.
- Dataset selection is driven by four criteria: diverse tasks, diverse domains, sufficient difficulty, and diverse annotation strategies to reduce benchmark-specific bias.
- The software contribution standardizes all datasets into a common IR format: `corpus.jsonl`, `queries.jsonl`, and `qrels/*.tsv`. This allows different retrieval systems to be swapped into the same evaluation pipeline.
- Evaluation is unified around nDCG@10 because the benchmark mixes binary and graded relevance judgments; the code also exposes MAP, Recall, Precision, MRR, recall-cap, and Hole@k.
- The paper compares 10 retrieval systems from five architecture families: lexical, sparse, dense, late interaction, and reranking.

## Benchmarks / Datasets
| Dataset / Benchmark | Task | Domain | Test Queries | Corpus | Notes |
|---|---|---|---:|---:|---|
| TREC-COVID | Bio-Medical IR | Bio-Medical | 50 | 171,332 | 3-level relevance; CORD-19 search |
| NFCorpus | Bio-Medical IR | Bio-Medical | 323 | 3,633 | 3-level relevance; medical QA retrieval |
| BioASQ | Bio-Medical IR | Bio-Medical | 500 | 14,914,602 | Large biomedical article retrieval |
| NQ | QA | Wikipedia | 3,452 | 2,681,468 | Google-style question retrieval |
| HotpotQA | QA | Wikipedia | 7,405 | 5,233,329 | Multi-hop QA retrieval |
| FiQA-2018 | QA | Finance | 648 | 57,638 | Financial QA retrieval |
| Signal-1M (RT) | Tweet Retrieval | Twitter | 97 | 2,866,316 | Retrieve tweets for news articles |
| TREC-NEWS | News Retrieval | News | 57 | 594,977 | 5-level relevance |
| Robust04 | News Retrieval | News | 249 | 528,155 | Classic robust ad hoc retrieval |
| ArguAna | Argument Retrieval | Misc. | 1,406 | 8,674 | Long argumentative queries |
| Touché-2020 | Argument Retrieval | Misc. | 49 | 382,545 | Argument search with graded relevance |
| CQADupStack | Duplicate Question | StackExchange | 13,145 | 457,199 | Mean over 12 subforums |
| Quora | Duplicate Question | Quora | 10,000 | 522,931 | Duplicate question retrieval |
| DBPedia-Entity-v2 | Entity Retrieval | Wikipedia | 400 | 4,635,922 | Entity-centric retrieval |
| SCIDOCS | Citation Prediction | Scientific | 1,000 | 25,657 | Citation recommendation style retrieval |
| FEVER | Fact Checking | Wikipedia | 6,666 | 5,416,568 | Evidence retrieval for claims |
| Climate-FEVER | Fact Checking | Wikipedia | 1,535 | 5,416,593 | Climate claim verification |
| SciFact | Fact Checking | Scientific | 300 | 5,183 | Scientific claim verification |

## Baselines
| Baseline | Type | Why Important | Notes |
|---|---|---|---|
| BM25 | Lexical | Classical sparse baseline and industrial default | Strong zero-shot anchor throughout the paper |
| DeepCT | Sparse term weighting | Tests learned term weighting on top of lexical retrieval | Good in-domain, poor transfer |
| SPARTA | Sparse neural retrieval | Tests token-level sparse semantic retrieval | Re-implemented by authors |
| docT5query | Sparse document expansion | Adds synthetic lexical coverage to documents | One of the strongest zero-shot methods |
| DPR | Dense bi-encoder | Canonical QA dense retriever | Worst transfer among compared dense models |
| ANCE | Dense bi-encoder | Strong MS MARCO hard-negative baseline | Better than DPR but still unstable out of domain |
| TAS-B | Dense bi-encoder | Stronger dense training objective with KD | Best dense model on average |
| GenQ | Synthetic domain adaptation | Tests target-domain synthetic query generation | Helps on some specialized domains |
| ColBERT | Late interaction | Token-level interaction without full cross-encoder cost | Good transfer, but large index |
| BM25+CE | Reranking | Strong cross-attention reranker on top of BM25 | Best average zero-shot result |

## Main Results
| Dataset / Benchmark | Metric | Baseline | Ours | Gain / Delta | Notes |
|---|---|---:|---:|---:|---|
| BEIR average vs BM25 | Relative avg. nDCG@10 | BM25 | docT5query | +1.6% | Document expansion is the strongest cheap alternative to BM25 |
| BEIR average vs BM25 | Relative avg. nDCG@10 | BM25 | ColBERT | +2.5% | Late interaction transfers better than dense bi-encoders |
| BEIR average vs BM25 | Relative avg. nDCG@10 | BM25 | BM25+CE | +11.0% | Best overall zero-shot performer |
| BEIR average vs BM25 | Relative avg. nDCG@10 | BM25 | ANCE | -7.4% | Dense retrieval does not reliably generalize |
| BEIR average vs BM25 | Relative avg. nDCG@10 | BM25 | DPR | -47.7% | In-domain success does not transfer |
| TREC-COVID | nDCG@10 | BM25 0.656 | BM25+CE 0.757 | +0.101 | Best reported result in the main table |
| HotpotQA | nDCG@10 | BM25 0.603 | BM25+CE 0.707 | +0.104 | Cross-attention helps on multi-hop QA retrieval |
| ArguAna | nDCG@10 | BM25 0.315 | GenQ 0.493 | +0.178 | One of the clearest wins for synthetic adaptation |
| Touché-2020 | nDCG@10 | BM25 0.367 | BM25 0.367 | +0.000 | BM25 itself is best; rerankers do not dominate everywhere |
| Quora | nDCG@10 | BM25 0.789 | ColBERT 0.854 | +0.065 | Late interaction is strongest on this duplicate-question task |
| FEVER | nDCG@10 | BM25 0.753 | BM25+CE 0.819 | +0.066 | Reranking remains strongest on claim retrieval |

## Ablations / Analysis
- In-domain performance is misleading. BM25 is far behind neural methods on MS MARCO, but becomes a strong zero-shot baseline once evaluation expands across domains.
- Learned term weighting does not transfer well. DeepCT and SPARTA both underperform BM25 on most datasets, while docT5query works better because it expands lexical coverage rather than only reweighting terms.
- Dense bi-encoders are brittle under domain and task shift. BioASQ and Touché-2020 are the paper's clearest examples where dense retrieval degrades sharply.
- Cross-attention and late interaction generalize better. BM25+CE wins 16/18 datasets against BM25; ColBERT beats BM25 on 9/18.
- TAS-B is the best dense model, which the authors attribute to stronger training losses and knowledge-distilled supervision.
- The paper identifies a document-length effect: TAS-B tends to retrieve shorter documents than ANCE, which hurts it especially on TREC-COVID and Touché-2020.
- Domain adaptation via GenQ is mixed: it helps on specialized domains such as finance, scientific literature, and StackExchange, but hurts on broader Wikipedia-style tasks.
- Annotation bias is a major result, not a side note. On TREC-COVID, Hole@10 is 6.4% for BM25 and 31.8% for TAS-B; after manual completion of missing judgments, ANCE improves from 0.654 to 0.735 nDCG@10 and ColBERT from 0.677 to 0.735.
- Efficiency results show the classic trade-off: BM25+CE and ColBERT are strongest but slow; dense models are much faster; BM25 remains tiny and cheap. On a 1M-document DBPedia slice, BM25 latency is 20ms CPU, TAS-B 14ms GPU / 125ms CPU, BM25+CE 450ms GPU / 6100ms CPU, and ColBERT needs a 20GB index.

## Implementation Clues
- `repo/beir/beir/datasets/data_loader.py` defines the benchmark's canonical file contract: `corpus.jsonl`, `queries.jsonl`, and `qrels/<split>.tsv`, loaded through `GenericDataLoader`.
- `repo/beir/beir/retrieval/evaluation.py` is the main evaluator wrapper. It standardizes retrieval and computes nDCG, MAP, Recall, Precision, and custom metrics such as MRR, recall-cap, and Hole@k via `pytrec_eval`.
- `repo/beir/beir/retrieval/search/lexical/bm25_search.py` wraps Elasticsearch BM25. It indexes `{title, body}` fields, bulk-loads the corpus, then batch-runs lexical multisearch.
- `repo/beir/beir/retrieval/search/dense/exact_search.py` is the core dense retrieval path. It sorts the corpus by text length, encodes in chunks, supports `cos_sim` and `dot`, keeps top-k results in per-query heaps, and can also search from saved embedding shards via Faiss.
- `repo/beir/beir/util.py` provides the dataset download/unzip helper plus `save_runfile` and `save_results`, which reflects the benchmark's emphasis on reusable evaluation artifacts.
- Benchmarking entry scripts in `repo/beir/examples/benchmarking/` make the paper's efficiency study concrete: `benchmark_bm25.py`, `benchmark_bm25_ce_reranking.py`, and `benchmark_sbert.py` benchmark BM25, reranking, and dense retrieval on a 1M-document DBPedia slice.
- 推断：the current `beir-cellar/beir` repository is a maintained continuation of the original 2021 codebase rather than a frozen paper artifact. Evidence: `UKPLab/beir` redirects to `beir-cellar/beir`, the README still cites the 2021 paper, and the repo now includes post-2021 evaluation backends such as HuggingFace APIs, LoRA/vLLM, and additional sparse/dense examples.

## Limitations
- The benchmark is English-only, which the paper explicitly lists as an open limitation.
- Most compared neural systems are trained on MS MARCO, so BEIR is zero-shot with respect to target tasks, not training-free in the stronger sense.
- BEIR is still constrained by the biases of its source datasets. The paper's TREC-COVID study shows that even "strong" pooled evaluations can still systematically prefer lexical systems.
- The benchmark is broad but not exhaustive. Multi-field retrieval, multilingual retrieval, and more task families are left for future extensions.
- The maintained repo is broader than the paper snapshot, so reproducing the exact 2021 comparison from today's code may require version pinning or historical commits.

## Later Ecosystem Position
- Separate the **2021 benchmark artifact** from the **2026 benchmark ecosystem framing**.
- As a 2021 paper artifact, BEIR is still the original 18-dataset zero-shot retrieval benchmark introduced at NeurIPS 2021.
- As a 2026 ecosystem object, BEIR is increasingly consumed through **MTEB's retrieval slice** rather than through a single standalone leaderboard.
- Evidence:
  - a 2026 AILog BEIR update explicitly says the 18 BEIR retrieval datasets are now a subset of the larger MTEB benchmark
  - the official MTEB project presents retrieval as one task family inside a much broader benchmark suite, with a dedicated retrieval task page and benchmark tooling
- Inference: for current model comparison, it is more precise to say "BEIR-style retrieval performance is often surfaced through MTEB" than to treat BEIR as the only live benchmark surface.

## Why This Blog Matters
- The AILog post is important because it makes an ecosystem transition explicit that is easy to miss if I only read the original 2021 paper and the old EvalAI board.
- It gives a clean practical statement for 2026 use: **BEIR's 18 retrieval datasets are now a subset of the larger MTEB benchmark**.
- That statement is exactly the bridge between two otherwise separate observations already present in the wiki:
  - the original BEIR paper defines the canonical retrieval benchmark
  - the current public BEIR leaderboard looks frozen and no longer captures the full embedding-model discussion
- So this blog is not important as a new primary benchmark source; it is important as a durable **interpretation source** for how practitioners now navigate BEIR versus MTEB.
- Wiki usage rule: when explaining current retrieval benchmarking practice, cite this blog together with the official MTEB project rather than citing the blog alone.

## Takeaways
- BEIR is the canonical reference for the claim that BM25 remains a serious zero-shot baseline even in the neural retrieval era.
- The paper is most useful as a benchmark-design paper: it explains why retrieval evaluation must be heterogeneous, not just how to score models.
- If a new retriever only beats BM25 on a narrow in-domain setup, BEIR is the obvious stress test.
- For current retrieval engineering, the main architectural lesson is still intact: full reranking and late interaction transfer better than plain bi-encoder dense retrieval, but they cost more in latency and memory.
- For 2026 benchmark navigation, BEIR is best understood as the canonical retrieval core that now sits inside a broader MTEB evaluation stack.
- For my own retrieval and grep-style benchmark work, the most reusable insight is the lexical-bias warning: benchmark construction can make semantic models look worse than they really are, or make lexical baselines look stronger than expected.

## Open Questions
- The maintained repo README now describes "17 benchmark datasets", while the 2021 paper evaluates 18 zero-shot datasets plus MS MARCO in-domain. Which dataset was removed, merged, or re-scoped in the modern codebase?
- How much of BM25's strength on BEIR is true lexical robustness versus artifact from dataset creation pipelines that already favored lexical candidate generation?
- Can modern embedding models and rerankers close the transfer gap without inheriting the latency and memory penalties that made BM25+CE and ColBERT expensive here?
- Should future retrieval benchmarks report only macro-averaged scores, or should they more explicitly group by task family, domain shift, and annotation bias profile?

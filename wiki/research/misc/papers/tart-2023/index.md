---
title: "Task-aware Retrieval with Instructions"
domain: research
area: misc
type: paper
status: processed
updated: 2026-04-19
tags: [paper, retrieval, instruction-following, beir, lotte, tart, berri]
---
# Task-aware Retrieval with Instructions

## Paper Meta
- Title: Task-aware Retrieval with Instructions
- Authors: Akari Asai, Timo Schick, Patrick Lewis, Xilun Chen, Gautier Izacard, Sebastian Riedel, Hannaneh Hajishirzi, Wen-tau Yih
- Year: 2023
- Venue: Findings of ACL 2023
- Topic: misc
- Paper Slug: tart-2023
- arXiv: https://arxiv.org/abs/2211.09260
- PDF: `2211.09260.pdf`
- Code Repo: https://github.com/facebookresearch/tart
- Reading Source: TeX (`source/extracted/acl_latex.tex`, `source/extracted/sections/*.tex`, `source/extracted/acl_latex.bbl`)
- Repo Read: yes (`repo/tart/README.md`, `repo/tart/TART/eval_beir.py`, `repo/tart/TART/eval_cross_task.py`, `repo/tart/TART/generate_passage_embeddings.py`, `repo/tart/TART/finetuning_tart_full.py`, `repo/tart/TART/finetuning.py`)
- PDF Fallback: not used

## TL;DR
- TART introduces "retrieval with instructions": the retrieval model receives not just a query, but an explicit natural-language description of the user's intent.
- The paper builds BERRI, a large multi-task collection of retrieval tasks with human-written instructions, and trains TART on top of it.
- TART-full improves over strong zero-shot baselines on BEIR and LOTTE while also introducing a harder cross-task cross-domain retrieval setup that is closer to real open-world retrieval.
- For the current BRIGHT/BEIR line, this is one of the most important adjacent papers because it expands the retrieval input space itself rather than only changing retriever architecture.

## Problem
- Standard retrieval assumes that the query alone defines relevance, but many real retrieval needs also depend on task intent, domain, or desired output unit.
- Existing IR systems rarely consume long-form instructions, even though instruction-following is central in modern LLM use.
- The paper asks whether a single multi-task retriever can adapt zero-shot to new tasks when the user provides an explicit instruction.

## Method
- Task formulation:
  - input = instruction `t` + query `q`
  - output = documents relevant to `q` under the relevance notion described by `t`
- Data:
  - build **BERRI** (Bank of Explicit Retrieval Instructions)
  - about 40 retrieval tasks with expert-written instructions
  - covers both standard retrieval datasets and non-retrieval datasets recast as retrieval tasks
- Instruction schema:
  - intent
  - domain
  - unit
- Models:
  - **TART-dual**: efficient bi-encoder retriever
  - **TART-full**: cross-encoder reranker initialized from T0-3B or FLAN-T5-XL
- Training:
  - multi-task instruction tuning across BERRI
  - combine random negatives, hard negatives, and instruction-unfollowing negatives
- Evaluation:
  - zero-shot transfer on BEIR and LOTTE-pooled
  - new `X^2-Retrieval` cross-task cross-domain evaluation with pooled corpora and heterogeneous intents

## Benchmarks / Datasets
| Dataset / Benchmark | Role in Paper | Metric | Notes |
|---|---|---|---|
| BERRI | training collection | not a single metric | around 40 instruction-annotated retrieval tasks |
| BEIR | zero-shot eval | nDCG@10 | 9 datasets used for fair comparison after exclusions |
| LOTTE-Search pooled | zero-shot eval | Success@5 | instructions specify target forum domain |
| X^2-Retrieval | new eval setup | nDCG@10 | pooled corpora across tasks/domains |

## Baselines
| Baseline | Type | Why Important | Notes |
|---|---|---|---|
| BM25 | sparse lexical | classic baseline | strong on BEIR, weak on LOTTE intent control |
| Contriever / Contriever-MS | dense retriever | strong generic bi-encoder baseline | both unsupervised and MS MARCO-tuned variants |
| UPR | retriever + reranker | LLM-style reranking baseline | cross-encoder over Contriever results |
| ColBERT-v2 | late interaction | strong zero-shot retriever | efficient versus full cross-encoder |
| MonoT5 3B | reranker | heavy reranking baseline | strongest non-instruction MS MARCO-style system |
| GPL / Promptagator | synthetic-data per-task training | customized target-dataset baselines | not universal models |

## Main Results
| Setting | Metric | Result | Notes |
|---|---|---:|---|
| TART-full (FLAN-T5) on BEIR | avg. nDCG@10 | 44.8 | best average in the paper's BEIR table |
| TART-full (T0-3B) on LOTTE-pooled | Success@5 | 75.7 | best LOTTE result in the table |
| TART-full (FLAN-T5) on Climate-FEVER | nDCG@10 | 35.4 | strongest number on that column |
| TART-full (FLAN-T5) on SciFact | nDCG@10 | 77.7 | tied best in the table |
| TART-full (T0-3B) on Touché | nDCG@10 | 31.2 | beats many strong baselines there |
| TART-dual on BEIR | avg. nDCG@10 | 37.4 | weaker than full reranker but still instruction-aware |

- Comparison points that matter:
  - BM25 + MonoT5 3B gets 43.4 BEIR average, but it is a heavyweight reranker without instruction following.
  - TART-full (FLAN-T5) gets 44.8 average while also handling instructions and new tasks.
  - Promptagator (rank) gets 43.9 average but requires training separate models for each target dataset.

## Ablations / Analysis
- Instructions matter at both train and test time. Removing them during either phase causes a clear drop.
- Dataset scale matters. More training datasets improve average BEIR performance.
- Task diversity matters. QA-only training struggles on tasks such as ArguAna.
- Domain diversity matters. Wikipedia-only training degrades on domains like argument search or scientific retrieval.
- Model scale matters. Larger reranking models improve average performance.
- Instruction-unfollowing negatives are especially important for the new cross-task setup; ablating them hurts `X^2-Retrieval` more than BEIR.
- The paper also shows robustness trade-offs: different valid instructions lead to small variation, but inaccurate instructions do meaningfully hurt performance.

## Implementation Clues
- The repo is split into:
  - `BERRI/` for the instruction-annotated dataset resources
  - `TART/` for training and evaluation code
- `repo/tart/TART/eval_beir.py` is the BEIR evaluation entry. It loads a retriever, optionally a finetuned checkpoint, and calls BEIR evaluation utilities with an explicit `--prompt`.
- `repo/tart/TART/eval_cross_task.py` and `generate_passage_embeddings.py` implement the paper's more realistic pooled-corpus evaluation path, where embeddings are precomputed and reused.
- `repo/tart/TART/finetuning_tart_full.py` is the cross-encoder training path built on custom T5 encoder classification heads (`src/modeling_enc_t5.py`, `src/tokenization_enc_t5.py`).
- `repo/tart/TART/finetuning.py` is the dual-encoder training path. It uses hard negatives and supports instruction-aware training through custom data loaders.
- The README is concrete about the deployment shape of the system:
  - `TART-full` as an instruction-aware reranker
  - `TART-dual` as an efficient instruction-aware retriever
  - optional pre-encoded embeddings for large corpora

## Limitations
- TART-full still depends on reranking top candidates, so full-corpus inference cost remains high.
- The paper excludes several datasets from BEIR comparison for fairness because they overlap with training resources, so its BEIR result is not directly the same as full-benchmark BEIR reporting.
- The dual-encoder version lags behind the full reranker, showing that efficient instruction-following retrieval is still harder than expensive reranking.
- The method depends on hand-authored or curated instructions, which is a new annotation burden.

## Takeaways
- TART is important because it changes the retrieval problem definition, not just the scoring model.
- It is one of the strongest papers for arguing that future retrieval benchmarks should include explicit intent or instruction channels.
- In the current literature map, TART sits between BEIR-style heterogeneous retrieval and BRIGHT-style harder retrieval: it asks not "can you transfer?" but "can you transfer when relevance itself is explicitly conditioned by instructions?"


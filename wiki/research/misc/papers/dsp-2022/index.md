---
title: "Demonstrate-Search-Predict: Composing retrieval and language models for knowledge-intensive NLP"
domain: research
area: misc
type: paper
status: processed
updated: 2026-04-18
tags: [paper, misc, dspy, retrieval-augmented-icl, open-domain-qa, hotpotqa, qrecc]
---
# Demonstrate-Search-Predict: Composing retrieval and language models for knowledge-intensive NLP

## Paper Meta
- Title: Demonstrate-Search-Predict: Composing retrieval and language models for knowledge-intensive NLP
- Authors: Omar Khattab, Keshav Santhanam, Xiang Lisa Li, David Hall, Percy Liang, Christopher Potts, Matei Zaharia
- Year: 2022
- Venue: ICML template used in source; exact final venue not explicitly reported in extracted text (inference)
- Topic: retrieval-augmented in-context learning for knowledge-intensive NLP
- Paper Slug: dsp-2022
- arXiv: https://arxiv.org/abs/2212.14024
- PDF: 2212.14024.pdf
- Code Repo: https://github.com/stanfordnlp/dsp
- Reading Source: TeX + repo
- PDF Fallback: not used

## TL;DR
- DSP turns retrieval-augmented in-context learning into a program over `Example` objects, with three composable stages: `demonstrate`, `search`, and `predict`.
- `demonstrate` bootstraps intermediate hops and passages from end-task labels, so the pipeline can learn without hand-labeling every query rewrite or retrieval step.
- `search` can rewrite or decompose questions, retrieve over multiple hops, and fuse multiple queries; `predict` can aggregate evidence with self-consistency.
- The paper reports strong development-set gains on Open-SQuAD, HotPotQA, and QReCC using frozen GPT-3.5 plus ColBERTv2, without fine-tuning.
- The authors explicitly frame the results as preliminary and note that some comparisons are not apples-to-apples.

## Problem
- Standard retrieve-then-read pipelines treat retrieval as a single context-gathering step, which leaves a lot of structure on the table for knowledge-intensive tasks.
- For open-domain QA, multi-hop QA, and conversational QA, a good system often needs query rewriting, hop-by-hop planning, and evidence aggregation, not just one retrieval call.
- Prior approaches often rely on hand-written rewrites, decompositions, or target-hop labels, which makes them brittle and expensive to extend.

## Method
- DSP treats natural-language text as the interface between a frozen language model and a frozen retrieval model.
- The core abstraction is a program over `Example` objects. A transformation takes an `Example` in and returns an updated `Example` with new fields such as demonstrations, queries, passages, summaries, or predictions.
- `demonstrate` selects training examples and programmatically bootstraps intermediate annotations by running the pipeline on examples that it can solve correctly.
- `search` uses the LM to generate search queries, retrieve passages with the RM, and optionally iterate across hops or fuse multiple rewritten queries.
- `predict` conditions on demonstrations and retrieved passages to produce the final answer, sometimes with self-consistency over multiple generated reasoning chains.
- In the evaluation setup, the paper uses GPT-3.5 (`text-davinci-002`) and ColBERTv2. The reported programs use 16-shot training examples, greedy decoding in some stages, and self-consistency or multiple query generations where useful.
- The source text also gives concrete patterns: open-domain QA retrieves 7 passages and uses 20 prediction samples; HotPotQA uses two hops; QReCC uses rewritten queries and autoregressive conversation rollout.

## Benchmarks / Datasets
| Dataset / Benchmark | Task | Metric | Notes |
|---|---|---|---|
| Open-SQuAD | Open-domain QA | EM / F1 | Wikipedia 2016 corpus; same splits as prior DPR/ColBERT work |
| HotPotQA fullwiki | Multi-hop QA | EM / F1 | Official Wikipedia 2017 abstracts; paper uses validation because the test set is hidden |
| QReCC | Conversational QA | F1 / nF1 | Wikipedia 2018; train split is subdivided 90/10, and low-quality conversations are filtered |

## Baselines
| Baseline | Type | Why Important | Notes |
|---|---|---|---|
| Vanilla LM | Few-shot in-context learning | Establishes the no-retrieval reference point | Uses sampled demonstrations only; no search |
| Retrieve-then-Read | Standard RAG pipeline | The main retrieval-augmented baseline | Retrieves passages once and then reads them |
| Self-ask w/ ColBERTv2 search | Hand-crafted multi-hop pipeline | Contemporary control-flow baseline | Modified to search the same ColBERTv2 index used by DSP |
| Self-ask + refined prompt | Prompt-engineered variant | Tests whether prompt tweaks close the gap | Paper reports it remains below DSP on HotPotQA |
| Retrieval-augmented LM SoTA | Related-work reference point | Qualitative comparison with concurrent systems | Numbers are not apples-to-apples across settings |

## Main Results
| Dataset / Benchmark | Metric | Baseline | Ours | Gain / Delta | Notes |
|---|---|---|---|---|---|
| Open-SQuAD | EM / F1 | 33.8 / 46.1 retrieve-then-read | 36.6 / 49.0 | +2.8 EM, +2.9 F1 | 16-shot, GPT-3.5 + ColBERTv2 |
| HotPotQA fullwiki | EM / F1 | 36.9 / 46.1 retrieve-then-read | 51.4 / 62.9 | +14.5 EM, +16.8 F1 | Largest reported gain in the table |
| QReCC | F1 / nF1 | 31.6 / 22.2 retrieve-then-read | 35.0 / 25.3 | +3.4 F1, +3.1 nF1 | Conversational QA with autoregressive rollout |

## Ablations / Analysis
- There is no standalone ablation table in the extracted source section; the paper relies mostly on baseline comparisons plus qualitative discussion of the stages.
- The text highlights several useful variants: direct-question retrieval for open-domain QA, multi-hop query generation with fusion, and conversational query rewriting.
- The paper explicitly discusses self-ask failure modes, especially "self-distraction", where the model follows a tangential subquestion instead of the target information need.
- The source says future versions will add more test tasks and LM choices, which is a sign that the reported evaluation is still a first pass.

## Implementation Clues
- The local repo snapshot is a current `dspy` package, not a frozen paper reproduction. `repo/README.md` points to the live DSPy docs rather than an experiment harness.
- `repo/dspy/__init__.py` re-exports the main API surface: predict primitives, retrievers, signatures, teleprompting, evaluation, adapters, utilities, `ColBERTv2`, and the global settings helpers.
- `repo/pyproject.toml` identifies the package as `dspy` version `3.1.3`, requires Python `>=3.10, <3.15`, and depends on packages such as `openai`, `litellm`, `pydantic`, `diskcache`, `json-repair`, and `numpy`.
- `repo/docs/README.md` says the docs site is built with MkDocs Material and is maintained separately from the paper.
- The repo state available here is useful for understanding the implementation surface, but it does not appear to contain the paper-era experimental scripts described in the manuscript.

## Limitations
- The authors say the report is preliminary and that future versions will include additional test tasks and LM choices.
- Several comparisons are not apples-to-apples because the cited systems use different settings, prompts, or corpora.
- The paper reports development-set results, not a complete held-out benchmark suite for every task it mentions.
- The method is demonstrated with GPT-3.5 and ColBERTv2; the paper does not claim these are the only or final choices.

## Takeaways
- DSP is best read as a programming model for retrieval-augmented in-context learning, not just a new prompt template.
- The most important design move is to make intermediate reasoning and retrieval steps first-class and bootstrappable from end-task labels.
- Multi-hop and conversational QA benefit from structured query generation and evidence aggregation rather than a single retrieval call.
- The paper’s strongest practical message is that short, composable programs can outperform much more rigid prompt pipelines.

## Open Questions
- How much of the gain comes from the DSP control flow itself versus self-consistency and better retrieval?
- How would the same programs behave with newer LMs, newer retrievers, or more retrieval budget?
- Can the pipeline be simplified without losing most of the reported improvement?
- Which of these ideas transfer cleanly to tasks outside QA?

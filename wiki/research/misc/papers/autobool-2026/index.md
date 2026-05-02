---
title: "AutoBool: An Reinforcement-Learning trained LLM for Effective Automated Boolean Query Generation for Systematic Reviews"
domain: research
area: misc
type: paper
status: processed
updated: 2026-04-21
tags: [paper, misc, reinforcement-learning, boolean-query-generation, systematic-reviews, pubmed]
---
# AutoBool: An Reinforcement-Learning trained LLM for Effective Automated Boolean Query Generation for Systematic Reviews

## Paper Meta
- Title: AutoBool: An Reinforcement-Learning trained LLM for Effective Automated Boolean Query Generation for Systematic Reviews
- Authors: Shuai Wang, Harrisen Scells, Bevan Koopman, Guido Zuccon
- Year: 2026
- Venue: EACL 2026
- Topic: misc
- Paper Slug: autobool-2026
- arXiv: https://arxiv.org/abs/2602.00005
- PDF: 2602.00005.pdf
- Code Repo: https://github.com/ielab/AutoBool
- Reading Source: TeX source and repo scripts
- Publication note: user reported acceptance/publication at EACL 2026; arXiv record remains the public preprint artifact.

## TL;DR
- AutoBool uses GRPO to train an LLM to generate PubMed Boolean queries for systematic reviews, with retrieval reward instead of gold-query supervision.
- The paper builds a 65,588-topic dataset from PMC OA, then shows that RL-trained Qwen3 models substantially outperform zero-shot prompting and few-shot ICL on recall-heavy retrieval.
- On external benchmarks, the trained models can nearly match expert queries on CLEF TAR while retrieving far fewer documents.

## Problem
- Boolean query generation for systematic reviews needs very high recall, but zero-shot prompting usually misses too many relevant studies.
- Supervised fine-tuning is awkward because there is no single gold Boolean query per topic, and existing datasets are tiny.
- The task also has a real screening-cost tradeoff: higher recall should not explode the number of retrieved documents.

## Method
- AutoBool trains a causal LLM with GRPO, using topic text as input and a Boolean query as the output.
- The reward has three parts: format correctness, syntactic/exec validity, and retrieval effectiveness.
- Format reward is `+10` for proper `<answer>...</answer>` output and `-10` otherwise; validity reward is `+10` for a syntactically valid, executable query and `-10` otherwise.
- Retrieval reward is recall-first: it combines a recall term with a recall-weighted log precision term, controlled by `alpha`, `M`, and smoothing constant `s`.
- The main prompt family is four-way: No Reasoning (`N.R`), Free-text Reasoning (`R`), Conceptual Reasoning (`R-con`), and Objective Reasoning (`R-obj`).

## Datasets / Benchmarks
| Dataset / Benchmark | Size | Role | Notes |
|---|---:|---|---|
| PMC OA systematic reviews | 75,676 identified; 65,600 usable; 65,588 final | Training and evaluation source | Derived from PMC OA reviews by extracting PMIDs cited in the results section |
| PubTemp | 1,000 topics | Main out-of-distribution test set | Topics published after 2024-11-01; sampled to avoid leakage and keep evaluation feasible |
| CLEF TAR | 72 topics | External benchmark | Uses CLEF TAR 2017 and 2018 subsets |
| Seed Collection | 40 topics | External benchmark | Standard Boolean-query-generation benchmark |

## Baselines
| Baseline | Type | Why it matters | Notes |
|---|---|---|---|
| Qwen3-4B zero-shot | Prompt baseline | Main in-family comparison | Evaluated under N.R, R, R-con, and R-obj |
| GPT-4o | Commercial LLM baseline | Strong general-purpose benchmark | Better than Qwen3 zero-shot, but still below AutoBool recall |
| O3 | Commercial LLM baseline | Stronger commercial comparison | Often competitive, but AutoBool still wins on recall/high-recall coverage |
| ICL 1/3/5-shot | Few-shot baseline | Tests whether examples can replace RL | Improves over zero-shot, but does not scale to AutoBool performance |
| Expert-crafted queries | Upper-bound reference | Domain expert baseline | Available on CLEF TAR and Seed Collection only |

## Main Results
| Dataset | Best AutoBool setting | Headline result | Strongest comparison point | Notes |
|---|---|---|---|---|
| PubTemp | Qwen3-4B, N.R, `alpha=1` | Recall `0.7036`, F3 `0.1195`, recall>80 `47.10`, recall>90 `32.30` | Qwen3-4B zero-shot N.R recall `0.0098`; best ICL recall `0.1011` | Also achieves 98.4% success and retrieves `732.49` docs on average |
| CLEF TAR | Qwen3-4B, N.R, `alpha=1` | Recall `0.8387`, F3 `0.2401`, recall>80 `70.83`, recall>90 `51.39` | Expert-crafted recall `0.8458`, retrieved `14,327.07` docs | Nearly matches expert recall while retrieving about 17x fewer documents |
| Seed Collection | Qwen3-4B, N.R, `alpha=1` | Recall `0.6828`, F3 `0.0943`, recall>80 `47.50`, recall>90 `35.00` | Expert-crafted recall `0.7241`, F3 `0.1869` | Beats zero-shot and the cited O1 baseline, but trails expert precision/F3 |

- Across PubTemp, AutoBool beats the best in-context learning result by about 7x in recall for the N.R prompt.
- Compared with GPT-4o and O3, AutoBool uses a much smaller backbone but is still stronger on recall and high-recall thresholds.
- The trained models keep the retrieved set size practical, usually well under 1,000 documents on PubTemp/CLEF/Seed except expert queries.

## Ablations / Analysis
- Model size: Qwen3 models at 1.7B, 4B, 8B, and 14B show a tradeoff where larger models improve F3 but slightly reduce recall and high-recall coverage.
- Temperature: the paper evaluates 0.6, 0.9, and 1.2; higher temperature consistently improves primary metrics by encouraging more diverse generations.
- Backbone: on the same RL setup, LLaMA3.1-8B beats Qwen3-8B on recall and recall-threshold metrics, while Qwen3-8B is better on F3 and easier to train stably.
- Reward ablations: removing scaling hurts F3 sharply in N.R, removing recall dependency destroys recall, and removing precision weighting reduces both recall coverage and F3.
- Direct F3 optimization is not a substitute for the paper's reward: it increases F3 but collapses recall and high-recall coverage.
- After training, N.R usually becomes the strongest prompt for recall, while reasoning prompts remain more stable and often need fewer regenerations.

## Implementation Clues
- The repo README is a placeholder, so the useful implementation evidence is in `train_autobool/`.
- `train_grpo.py` uses `trl.GRPOTrainer` with LoRA, bf16, flash-attention-2, DeepSpeed, vLLM colocate mode, and four completions per prompt.
- `reward.py` computes format, validity, and retrieval rewards, and sends retrieval requests to a local Entrez service at `http://localhost:8000/entrez/query`.
- `create_unified_dataset.py` defines the four prompt templates and the dataset-building pipeline; `run_generation.py` and `run_generation_chatgpt.py` handle evaluation and regeneration.
- The source and appendix disagree on training temperature: the main text says `1.2`, while the appendix hyperparameter table lists `0.6`.

## Limitations
- The authors only fine-tuned open-source backbones up to 14B parameters, so they could not test whether much larger models would improve recall further.
- LLaMA3.1 training was less stable than Qwen3, with abrupt reward collapses that made replication difficult.
- The training process is stochastic, so query-level outputs can vary across runs even when overall trends are stable.

## Takeaways
- Retrieval-aware RL is the core contribution: it solves the supervision problem and directly optimizes the metric that matters for systematic reviews.
- The best default operating point in the paper is Qwen3-4B with the N.R prompt and `alpha=1`.
- AutoBool is most compelling when recall is the hard constraint and a modest screening load is acceptable.

## Open Questions
- How far does the approach transfer beyond PubMed-style biomedical systematic reviews?
- Can the recall advantage survive training on larger backbones without the stability issues seen in LLaMA3.1?
- Which reward variant would be preferred if downstream screening cost were explicitly priced into the objective?

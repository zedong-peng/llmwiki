---
title: "Memory-T1: Reinforcement Learning for Temporal Reasoning in Multi-session Agents"
domain: research
area: misc
type: paper
status: processed
updated: 2026-04-18
tags: [paper, misc, processed, temporal-reasoning, reinforcement-learning, memory]
---
# Memory-T1: Reinforcement Learning for Temporal Reasoning in Multi-session Agents

## Paper Meta
- Title: Memory-T1: Reinforcement Learning for Temporal Reasoning in Multi-session Agents
- Authors: Yiming Du, Baojun Wang, Yifan Xiang, Zhaowei Wang, Wenyu Huang, Boyang Xue, Bin Liang, Xingshan Zeng, Fei Mi, Haoli Bai, Lifeng Shang, Jeff Z. Pan, Yuxin Jiang, Kam-Fai Wong
- Year: not reported
- Venue: not reported
- Topic: misc
- Paper Slug: memory-t1-2025
- arXiv: https://arxiv.org/abs/2512.20092
- PDF: 2512.20092.pdf
- Code Repo: https://github.com/Elvin-Yiming-Du/Memory-T1
- Reading Source: TeX; repo README only; PDF fallback not used

## TL;DR
- Memory-T1 is a coarse-to-fine memory retrieval framework for temporal reasoning in long, multi-session dialogues.
- It predicts a query time window, filters dialogue sessions temporally, ranks the survivors by relevance, and then uses RL to select evidence sessions and answer.
- Training uses GRPO with a multi-level reward: answer accuracy, evidence grounding, and temporal consistency at both session and utterance level.
- On Time-Dialog, Memory-T1 reaches 66.9% with a 3B backbone and 67.0% with a 7B backbone, beating Time-R1, MemAgent, and larger vanilla baselines.
- The method stays robust on LoCoMo, long contexts up to 128k tokens, and moderate label noise, with negligible retrieval latency.

## Problem
- The paper targets temporal reasoning over long, noisy, multi-session dialogues.
- The key failure mode is that long-context models treat history as flat text, so they miss the right session, mis-handle relative time expressions, or attend to plausible but temporally wrong evidence.
- Prior temporal or memory methods are presented as either too dependent on explicit metadata/summaries or too sparse in supervision, which makes them brittle for unstructured conversational memory.

## Method
- Memory-T1 uses a coarse-to-fine retrieval pipeline before the final answer is generated.
- First, the model predicts a query time window and removes sessions outside that range.
- Second, BM25 ranks the remaining temporally valid sessions to form a candidate pool.
- Third, an RL policy trained with GRPO selects evidence sessions and emits a structured output that includes `selected_memory` plus the answer.
- The reward is multi-level: `R_a` checks answer correctness, `R_g` checks overlap between cited session IDs and gold evidence, and `R_t` enforces temporal consistency through session-level proximity `R_s` and utterance/event-level fidelity `R_f`.
- The source uses Qwen2.5-3B-Instruct and Qwen2.5-7B-Instruct backbones, BM25 retrieval, VERL, batch size 32, learning rate `1e-6`, `K=8` rollouts, KL coefficient `0.1`, and max sequence length `16k`.

## Benchmarks / Datasets
| Dataset / Benchmark | Task | Metric | Notes |
|---|---|---|---|
| Time-Dialog | Multi-session temporal QA | Overall score and subtask percentages | 4,716 QA examples; split into 4,065 train / 451 val / 200 test; annotations include query time ranges, utterance-level event spans, and gold evidence session IDs |
| LoCoMo | OOD multi-session conversational memory | Overall and subtask percentages | Five subtasks; used for out-of-domain temporal reasoning and RAG / non-RAG comparison |

## Baselines
| Baseline | Type | Why Important | Notes |
|---|---|---|---|
| Qwen2.5-3B / 7B / 14B Instruct | Open-source LLM baselines | Shows whether scale alone solves the task | Used as full-context baselines and as the base family for Memory-T1 |
| Gemma-4B-it and Llama-3.1-8B-Instruct | Open-source LLM baselines | Cross-family scaling comparison | Help show the gain is not model-family specific |
| GPT-4 Full Prompt / ReAct / Oracle Evidence | Closed-source strong baselines | Upper bound and agent-style comparison | Oracle uses gold evidence; Full Prompt and ReAct are non-oracle settings |
| RAG | Retrieval baseline | Tests standard retrieval augmentation | Useful for separating retrieval from learned policy improvements |
| SFT | Supervised fine-tuning baseline | Tests whether RL is needed | Fine-tuned from Qwen2.5-3B |
| MemAgent and Time-R1 | Specialized memory / temporal agents | Most relevant prior methods | Zero-shot public checkpoints are compared directly |
| RL (Task Reward Only) | Ablation baseline | Tests the value of the new reward terms | Same architecture as Memory-T1 but only answer accuracy reward |

## Main Results
| Dataset / Benchmark | Metric | Baseline | Ours | Gain / Delta | Notes |
|---|---|---|---|---|---|
| Time-Dialog | Overall score (%) | Time-R1 49.4; MemAgent 49.9; Qwen2.5-14B 60.7; GPT-4 Full Prompt 64.8 | 66.9 (3B), 67.0 (7B) | +17.5 to +17.6 vs specialized baselines; +6.3 vs Qwen2.5-14B; +2.2 vs GPT-4 Full Prompt | Best non-GPT result in the table |
| LoCoMo | Overall score (%) | Qwen2.5-3B 33.5 non-RAG / 31.9 RAG | 37.7 non-RAG / 36.7 RAG | +4.2 non-RAG; +4.8 vs Qwen2.5-3B RAG | Better OOD temporal reasoning |
| Long-context test | F1 by context length | Qwen2.5-7B drops by over 30 points as context grows | Stable, with a +25.0 point lead in the 64k-128k bracket | Large robustness gap at long lengths | Shows the value of coarse-to-fine filtering |
| Efficiency | Avg latency (s) | Time-R1 1.24; MemAgent 1.56; Qwen2.5-3B 1.36 | 1.26 | Competitive with baselines | Retrieval overhead is reported as 0.01 s |

## Ablations / Analysis
- Reward ablation shows that answer-only RL is not enough: `R_a` only drops overall performance to 51.9, which is 22.4 points below the full 3B model.
- Removing evidence grounding hurts more than a pure temporal tweak: `w/o R_g` falls to 60.8 overall, a 9.1 point drop.
- Removing temporal consistency as a whole drops to 63.5 overall, while removing only `R_s` creates a sharp trade-off: Category A improves, but Category B collapses hard.
- Removing only `R_f` still hurts overall performance to 64.8, so both the session-level and utterance-level terms matter.
- Candidate-generation analysis says top-k around 10 is needed for high evidence recall, and the temporal filter removes distractors without losing key evidence.
- Noise robustness is decent: overall score stays 67.0 at 5% noise, then drops to 63.4 at 10% and 60.0 at 20%.
- LoCoMo analysis suggests the learned policy generalizes better than the raw backbone, and that RAG can help adversarial answerability detection while slightly shifting standard-task behavior.

## Implementation Clues
- The local repo snapshot is only a placeholder: `repo/README.md` says cloning was skipped and contains no runnable code.
- The readable source is `source/extracted/iclr2025_conference.tex`; `00README.json` marks this as the toplevel source.
- The paper's concrete training setup is documented in the TeX: Qwen2.5-3B/7B-Instruct backbones, BM25 retrieval, GRPO in VERL, `batch size 32`, `lr 1e-6`, `K=8`, `KL=0.1`, and `max seq len 16k`.
- No local training script, evaluation script, or config file is available in this paper directory, so paper-vs-repo consistency cannot be checked beyond the placeholder README.

## Limitations
- The strongest supervision depends on extra annotations for query time ranges, utterance-level events, and evidence sessions.
- The output format must be parseable for the reward to work, so the method is sensitive to generation-format failures.
- The local repository snapshot does not include executable code, so reproducibility cannot be verified from this directory alone.
- The paper still leaves a sizable gap to GPT-4 Oracle Evidence, which indicates that perfect evidence access remains substantially easier than learned retrieval.

## Takeaways
- Temporal retrieval policy matters more than base-model scale alone on this benchmark.
- Dense reward design is the main technical contribution, especially the combination of evidence grounding with temporal consistency.
- A coarse temporal filter before relevance ranking is a practical way to reduce long-context distraction.
- The method is strongest on temporally demanding subtasks and on very long contexts, which is exactly where ordinary long-context prompting degrades.

## Open Questions
- How much of the gain comes from the query time-window predictor versus the RL evidence selector?
- Would the same reward design work on other memory tasks that do not have clean time annotations?
- How sensitive are the results to annotation quality, since the paper relies on GPT-4-assisted labels plus human verification?
- Will the eventual public code release match the paper's claims closely, given that the local repo snapshot here is only a placeholder?

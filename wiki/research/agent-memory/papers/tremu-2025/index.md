---
title: "TReMu: Towards Neuro-Symbolic Temporal Reasoning for LLM-Agents with Memory in Multi-Session Dialogues"
domain: research
area: misc
type: paper
status: processed
updated: 2026-04-19
tags: [paper, temporal-reasoning, multi-session-dialogues, llm-agents, memory, benchmark]
---
# TReMu: Towards Neuro-Symbolic Temporal Reasoning for LLM-Agents with Memory in Multi-Session Dialogues

## Paper Meta
- Authors: Yubin Ge, Salvatore Romeo, Jason Cai, Raphael Shu, Yassine Benajiba, Monica Sunkara, Yi Zhang
- Year: 2025
- Venue: not reported
- Topic: misc
- Paper Slug: tremu-2025
- arXiv: https://arxiv.org/abs/2502.01630
- PDF: `2502.01630.pdf`
- Source read: TeX source (`source/extracted/acl_latex.tex`, `sections/*`, `acl_latex.bib`)
- Code repo: not available locally

## TL;DR
- TReMu targets temporal reasoning in multi-session dialogues, where relative time and cross-session dependencies make long-horizon memory harder than in standard temporal QA.
- The paper adds a benchmark by augmenting LoCoMo and creates 600 multiple-choice temporal questions, including 112 unanswerable items.
- The framework combines time-aware memorization with neuro-symbolic reasoning through generated Python code, and it reports a GPT-4o overall accuracy jump from 29.83 with standard prompting to 77.67.

## Problem
- Existing temporal reasoning benchmarks mostly focus on short texts with explicit timestamps, not long dialogue histories with fragmented timing cues.
- Multi-session dialogue introduces two hard cases: relative time expressions and cross-session dependencies, where later sessions refer back to earlier events and changed states.
- Memory-augmented agents can still miss relevant temporal facts because long histories create retrieval noise and context truncation.

## Method
- Time-aware memorization replaces coarse session summaries with timeline-style memory pieces tied to inferred event dates, so the model can separate when an event happened from when it was mentioned.
- Memory organization groups events by inferred timestep and keeps them retrievable for later questions.
- Neuro-symbolic temporal reasoning retrieves relevant memory, asks the LLM to emit Python code, executes that code with temporal libraries, and then uses the result to select the final answer.
- The implementation explicitly leans on Python tools such as `datetime`, `dateutil.relativedelta`, and custom helpers like `weekRange(t)`.

## Benchmarks / Datasets

### Source Dataset Choice
| Dataset | Avg. turns / conv. | Avg. sessions / conv. | Avg. tokens / conv. | Time interval | Collection |
|---|---:|---:|---:|---|---|
| MSC | 53.3 | 4 | 1,225.9 | few days | Crowdsourcing |
| Conversation Chronicles | 58.5 | 5 | 1,054.7 | few hours - years | LLM-generated |
| LoCoMo | 304.9 | 19.3 | 9,209.2 | few months | LLM-gen. + crowdsourcing |

### Constructed Temporal QA Benchmark
| Question type | Count | Options | Events | Event type |
|---|---:|---:|---:|---|
| Temporal Anchoring | 264 | 5 | 1 | relative time |
| Temporal Precedence | 102 | 3 | 2 | cross-session dependency (+ relative time) |
| Temporal Interval | 234 | 5 | 2 | cross-session dependency (+ relative time) |
| Total | 600 | not reported | not reported | not reported |
| Unanswerable | 112 | not reported | not reported | not reported |
| LoCoMo source dialogues | 321 | not reported | not reported | not reported |

### Construction Pipeline
- Step 1: prompt GPT-4o to extract temporal events from each dialogue session and annotate relative time expressions.
- Step 2: link events across sessions when they refer to the same or related entities, especially when attributes change over time.
- Step 3: generate multiple-choice questions for anchoring, precedence, interval, and unanswerable cases.
- Step 4: manually review each question to fix bad inferences, remove unreasonable items, and keep the answers grounded in the dialogues.

## Baselines
| Baseline | Type | Why Important | Notes |
|---|---|---|---|
| SP | standard prompting | Minimal temporal reasoning baseline | No explicit chain-of-thought or memory tools |
| CoT | reasoning baseline | Tests whether verbal reasoning alone is enough | Helps but still misses temporal calculation |
| MemoChat | memory baseline | Prior memory-augmented conversational agent | Uses memory but no explicit symbolic reasoning |
| MemoChat + CoT | memory + reasoning baseline | Stronger MemoChat variant | Shows effect of reasoning on top of memory |
| Timeline + CoT | time-aware memory baseline | Isolates the value of timeline memorization | Strongest non-symbolic baseline |

## Main Results

### GPT-4o
| Method | TA | TP | TI | Overall | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|---:|
| SP | 18.18 | 58.82 | 30.34 | 29.83 | 46.88 | 13.39 | 20.84 |
| CoT | 67.80 | 74.51 | 49.15 | 61.67 | 42.61 | 43.75 | 43.18 |
| MemoChat | 35.23 | 43.14 | 25.21 | 32.67 | 24.30 | 77.68 | 37.02 |
| MemoChat + CoT | 51.14 | 49.02 | 26.50 | 41.67 | 24.80 | 81.25 | 38.00 |
| Timeline + CoT | 83.33 | 78.41 | 58.55 | 71.50 | 48.51 | 58.04 | 52.84 |
| TReMu | 84.47 | 81.37 | 68.38 | 77.67 | 55.48 | 76.79 | 64.42 |

### GPT-4o-mini
| Method | TA | TP | TI | Overall | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|---:|
| SP | 20.08 | 50.00 | 29.91 | 29.00 | 40.00 | 26.79 | 32.08 |
| CoT | 46.59 | 62.75 | 37.18 | 45.67 | 33.96 | 48.21 | 39.86 |
| MemoChat | 21.21 | 39.22 | 23.50 | 25.17 | 21.11 | 74.11 | 32.88 |
| MemoChat + CoT | 24.62 | 45.10 | 24.36 | 28.00 | 21.11 | 75.00 | 32.94 |
| Timeline + CoT | 55.68 | 59.80 | 38.46 | 49.67 | 30.73 | 59.82 | 40.60 |
| TReMu | 64.02 | 46.08 | 38.89 | 51.17 | 29.21 | 92.86 | 44.44 |

### GPT-3.5-Turbo
| Method | TA | TP | TI | Overall | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|---:|
| SP | 21.59 | 31.37 | 23.08 | 23.83 | 22.91 | 46.43 | 30.68 |
| CoT | 23.86 | 38.24 | 22.65 | 25.83 | 20.97 | 50.00 | 29.56 |
| MemoChat | 17.42 | 45.10 | 23.50 | 24.50 | 21.93 | 66.96 | 33.04 |
| MemoChat + CoT | 20.45 | 53.92 | 26.50 | 28.50 | 21.79 | 50.00 | 30.36 |
| Timeline + CoT | 32.58 | 44.12 | 22.65 | 30.67 | 22.57 | 51.79 | 31.44 |
| TReMu | 42.42 | 37.25 | 22.22 | 33.67 | 23.33 | 75.00 | 35.60 |

## Ablations / Analysis
- `MemoChat + CoT` vs `Timeline + CoT` isolates the value of time-aware memorization; the timeline variant improves temporal grounding, especially for relative-time cases.
- `Timeline + CoT` vs `TReMu` isolates the value of symbolic reasoning; generating and executing Python code gives another step up in accuracy and F1.
- The paper notes that memory augmentation does not always help GPT-4o or GPT-4o-mini, likely because those models can already fit more of LoCoMo into context.
- For GPT-3.5-Turbo, memory helps more because truncation is a real constraint.
- Execution failures are said to be generally low, with GPT-4o lowest and GPT-3.5-Turbo highest, but exact failure percentages are not reported in the text.

## Implementation Clues
- Built on the memory-augmented LLM-agent pipeline from MemoChat.
- Time-aware memorization is implemented as timeline summarization rather than a single holistic session summary.
- Retrieval happens before code generation, so the code only sees the most relevant memory pieces.
- The symbolic step uses Python as the reasoning language because the authors found current frontier models handle Python generation better than alternative symbolic formalisms.
- The paper specifically says open-source models were hard to adapt; only about 10% of LoCoMo dialogues fit into Llama-3-70B, and even then instruction following degraded.

## Limitations
- Evaluation is multiple-choice QA, not generative dialogue, because free-form temporal answers are harder to score reliably.
- The experiments focus mainly on closed-source LLMs.
- The authors leave adaptation to open-source models as future work.
- The benchmark still depends on manual quality control over GPT-generated questions.

## Takeaways
- The main gain is not just better prompting; it is the combination of memory representation that preserves time and a symbolic step that does explicit temporal calculation.
- The benchmark is materially harder than older temporal QA sets because it tests relative time and cross-session dependency in long dialogue histories.
- The strongest reported result is GPT-4o TReMu at 77.67 overall accuracy, compared with 29.83 for standard prompting on the same benchmark.

## Open Questions
- How well does the approach transfer to fully generative dialogue evaluation rather than multiple-choice QA?
- Can open-source models close the gap once context handling and instruction following improve?
- How brittle is the Python-code reasoning step under noisier temporal language than the benchmark examples?

---
title: "ReAct: Synergizing Reasoning and Acting in Language Models"
domain: research
area: misc
type: paper
status: processed
updated: 2026-04-19
tags: [paper, misc, react, reasoning, acting, prompting]
---
# ReAct: Synergizing Reasoning and Acting in Language Models

## Paper Meta
- Title: ReAct: Synergizing Reasoning and Acting in Language Models
- Authors: Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan Cao
- Year: 2022
- Venue: ICLR 2023
- Topic: misc
- Paper Slug: react-2022
- arXiv: https://arxiv.org/abs/2210.03629
- PDF: 2210.03629.pdf
- Code Repo: https://github.com/ysymyth/ReAct
- Reading Source: TeX source plus local repo snapshot
- PDF Fallback: not used

## TL;DR
- ReAct interleaves free-form reasoning traces with environment actions so one LLM can both reason and gather evidence.
- The paper shows that this coupling improves groundedness and interpretability on HotpotQA and FEVER, and boosts success on ALFWorld and WebShop.
- The strongest prompting results come from combining ReAct with self-consistency or from finetuning on generated trajectories.

## Problem
- Chain-of-thought reasoning and action-based decision making were usually studied separately.
- Pure reasoning can hallucinate or propagate errors because it is not grounded in external evidence.
- Pure acting can lose track of high-level goals, subgoals, and exceptions when the trajectory is long.
- The paper asks whether language models can use reasoning and acting in one closed loop.

## Method
- ReAct expands the action space to include language "thoughts" alongside environment actions.
- A thought updates the context without changing the external environment, which lets the model plan, track progress, recover from mistakes, and decide what to retrieve next.
- For knowledge tasks, the action space is a simple Wikipedia API with `search[entity]`, `lookup[string]`, and `finish[answer]`.
- For reasoning tasks, prompts use dense thought-action-observation trajectories; for decision-making tasks, thoughts are sparse and placed only where they help most.
- The paper also evaluates two combination heuristics: `ReAct -> CoT-SC` when ReAct fails to finish, and `CoT-SC -> ReAct` when self-consistency is not decisive.
- Finetuning experiments use 3,000 generated trajectories for HotpotQA and compare PaLM-8B and PaLM-62B against prompt-only baselines.

## Benchmarks / Datasets
| Dataset / Benchmark | Task | Metric | Notes |
|---|---|---|---|
| HotpotQA | Multi-hop QA | Exact Match | Question-only setting; Wikipedia search/lookup available |
| FEVER | Fact verification | Accuracy | Question-only setting; label space SUPPORTS / REFUTES / NOT ENOUGH INFO |
| ALFWorld | Text-based household game | Success rate | 134 unseen evaluation games, task-specific setup |
| WebShop | Web navigation / shopping | Score, success rate | 500 test instructions; 1.18M products and 12k human instructions |

## Baselines
| Baseline | Type | Why Important | Notes |
|---|---|---|---|
| Standard prompting | Prompt-only | No reasoning traces or actions | Removes thoughts, actions, and observations from ReAct trajectories |
| Chain-of-thought | Reasoning-only | Tests internal reasoning without tools | Uses `CoT` and `CoT-SC` self-consistency |
| Act-only | Acting-only | Tests tool use without explicit reasoning | Removes thoughts from ReAct trajectories |
| IM-style prompting | External-feedback reasoning | Tests a narrower thought style | Used as an ALFWorld ablation against ReAct |
| BUTLER | Imitation learning | Strong RL-era ALFWorld baseline | Trained on 100k expert trajectories per task type |
| IL / IL+RL | Learned WebShop policies | Strong shopping baselines | Taken from the WebShop paper |

## Main Results
| Dataset / Benchmark | Metric | Key Numbers |
|---|---|---|
| HotpotQA | EM | Standard 28.7; CoT 29.4; CoT-SC 33.4; Act-only 25.7; ReAct 27.4; CoT-SC -> ReAct 34.2; ReAct -> CoT-SC 35.1 |
| FEVER | Accuracy | Standard 57.1; CoT 56.3; CoT-SC 60.4; Act-only 58.9; ReAct 60.9; CoT-SC -> ReAct 64.6; ReAct -> CoT-SC 62.0 |
| ALFWorld | Success rate | Act-only best of 6: 45; ReAct avg: 57; ReAct best of 6: 71; IM avg: 48; IM best of 6: 53; BUTLER: 37 |
| WebShop | Score / SR | Act-only 62.3 / 30.1; ReAct 66.6 / 40.0; IL 59.9 / 29.1; IL+RL 62.4 / 28.7; Human expert 82.1 / 59.6 |
| GPT-3 ReAct prompt transfer | EM / success rate | HotpotQA 30.8 vs PaLM-540B 29.4; ALFWorld 78.4 vs PaLM-540B 70.9 |

## Ablations / Analysis
- The human study on HotpotQA found ReAct trajectories were more grounded than CoT: true positives 94% vs 86%, false positives 6% vs 14%.
- ReAct failure modes were dominated by reasoning error (47%) and search-result error (23%); CoT failure modes were dominated by hallucination (56%).
- The paper reports that ReAct can get stuck in repetitive loops, which they suspect is partly due to greedy decoding.
- The best combined prompting methods were task-dependent: `ReAct -> CoT-SC` on HotpotQA and `CoT-SC -> ReAct` on FEVER.
- Finetuning with 3,000 trajectories improves ReAct substantially; PaLM-8B/62B finetuned ReAct beats the corresponding prompt-only variants and outperforms all 540B prompting methods in the reported HotpotQA comparison.

## Implementation Clues
- The local repo snapshot is only partially populated, but the important code files are readable.
- `wikienv.py` implements the Wikipedia environment with `search[]`, `lookup[]`, `finish[]`, and `think[]` actions plus simple page parsing.
- `wrappers.py` contains the HotpotQA and FEVER wrappers, answer normalization, EM/F1 logic, and trajectory logging.
- `base_config.yaml` shows an ALFWorld training setup based on oracle / DAgger-style control, with task types 1 through 6 and greedy or beam-search options.
- The repo README is a placeholder, so the local code should be treated as a partial implementation snapshot rather than a complete release.

## Limitations
- ReAct still depends on enough in-context examples, and long-horizon tasks can run into context-length limits.
- Prompting alone remains below supervised state of the art on HotpotQA and FEVER.
- On WebShop, ReAct is still far below the human expert score and success rate.
- Some HotpotQA labels are outdated relative to current Wikipedia, which can make evaluation look harsher than the retrieved evidence.

## Takeaways
- The core contribution is not a new retriever or a new planner; it is a simple prompt format that lets one LM alternate between thinking and acting.
- External tools improve factual grounding, while verbal reasoning improves planning and recovery.
- The strongest pattern is not "reason or act" but "reason to act, act to reason."
- Combining ReAct with self-consistency or finetuning is where the paper gets its best results.

## Open Questions
- How much better would ReAct scale with higher-quality human trajectories instead of bootstrapped ones?
- Could better decoding or search reduce the looping failures seen in greedy trajectories?
- How well does the pattern transfer to richer tool suites than Wikipedia, text games, and shopping websites?
- What is the best way to combine ReAct with RL or multi-task finetuning without losing interpretability?

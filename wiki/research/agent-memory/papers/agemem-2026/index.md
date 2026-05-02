---
title: "Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management for Large Language Model Agents"
domain: research
area: misc
type: paper
status: processed
updated: 2026-04-18
tags: [paper, misc, memory, reinforcement-learning, llm-agents]
---
# Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management for Large Language Model Agents

## Paper Meta
- Title: Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management for Large Language Model Agents
- Authors: Yi Yu, Liuyi Yao, Yuexiang Xie, Qingquan Tan, Jiaqi Feng, Yaliang Li, and Libing Wu
- Year: 2026
- Venue: not reported
- Topic: misc
- Paper Slug: agemem-2026
- arXiv: https://arxiv.org/abs/2601.01885
- PDF: `2601.01885.pdf`
- Code Repo: not reported
- Reading Source: TeX source (`source/extracted/acl_latex.tex` and `source/extracted/sections/*.tex`)
- Legacy Note: [[agent-memory/papers/agemem-2026]]

## TL;DR
- AgeMem turns memory management into part of the agent policy: the model can add, update, delete, retrieve, summarize, and filter memory through tools instead of relying on heuristic controllers.
- The paper trains this unified behavior with a three-stage progressive RL setup and a step-wise GRPO objective that broadcasts the terminal reward back across all memory decisions.
- On five benchmarks, AgeMem is the strongest method in both backbone settings, reaching 41.96 average on Qwen2.5-7B-Instruct and 54.31 average on Qwen3-4B-Instruct.

## Problem
- Existing agent memory systems usually split long-term memory and short-term context into separate modules.
- Long-term memory methods often depend on static memory structures or heuristic update rules, while short-term memory methods often rely on fixed retrieval or summarization schedules.
- That separation makes it hard to learn end-to-end memory policies, and many systems still need auxiliary controllers or external expert LLMs.

## Method
- AgeMem formulates memory management as a reinforcement learning problem where the state includes the current context, the long-term memory store, and the task specification.
- The action space mixes normal language generation with explicit memory tools.
- Long-term memory tools are `Add`, `Update`, and `Delete`.
- Short-term memory tools are `Retrieve`, `Summary`, and `Filter`.
- Training is staged: Stage 1 builds long-term memory, Stage 2 stresses short-term control with distractors, and Stage 3 requires coordinated use of both memories to solve the final task.
- LTM persists across stages, but the short-term context is reset before Stage 2 so the agent cannot solve the task by leaking information through context alone.
- The reward combines task performance, context management, and memory quality, with penalties for overflow, excessive tool use, and redundant storage.
- Step-wise GRPO assigns the final trajectory reward to all earlier actions so memory decisions in earlier stages receive credit from the end task outcome.

## Benchmarks / Datasets
| Dataset / Benchmark | Task | Metric | Notes |
|---|---|---|---|
| ALFWorld | embodied action / household tasks | Success Rate (SR) | Part of the five-benchmark evaluation suite |
| SciWorld | science-based reasoning and action | Success Rate (SR) | Used to test long-horizon agent control |
| PDDL | planning | Progress Rate (PR) | Measures progress toward task completion |
| BabyAI | gridworld / instruction following | Success Rate (SR) | Tests navigation and action sequencing |
| HotpotQA | multi-hop question answering | LLM-as-a-Judge (J) | Also used for memory-quality evaluation and RL fine-tuning |

## Baselines
| Baseline | Type | Why Important | Notes |
|---|---|---|---|
| No-Memory | null memory baseline | Shows how much the backbone can do without any memory system | Used in the main comparison table |
| LangMem | modular LTM framework | Representative long-term memory system | Supports multiple memory types |
| A-Mem | agentic LTM system | Strong memory baseline with learned memory organization | Zettelkasten-inspired design |
| Mem0 | scalable LTM system | Strong production-style memory baseline | Best baseline on some settings |
| Mem0^g | graph-based memory variant | Tests whether graph structure improves memory use | Provided as a Mem0 variant |
| AgeMem-noRL | ablation | Separates architecture gains from RL gains | Same system without RL fine-tuning |

## Main Results
| Backbone | Method | ALFWorld | SciWorld | PDDL | BabyAI | HotpotQA | Average |
|---|---|---:|---:|---:|---:|---:|---:|
| Qwen2.5-7B-Instruct | No-Memory | 27.16 | 13.80 | 10.15 | 50.80 | 38.36 | 28.05 |
| Qwen2.5-7B-Instruct | Best baseline (per dataset) | 38.27 | 30.50 | 18.39 | 60.58 | 46.66 | 37.14 |
| Qwen2.5-7B-Instruct | AgeMem-noRL | 37.90 | 28.67 | 8.87 | 46.34 | 45.36 | 33.43 |
| Qwen2.5-7B-Instruct | AgeMem | 41.07 | 35.55 | 17.31 | 61.42 | 54.44 | 41.96 |
| Qwen3-4B-Instruct | No-Memory | 38.51 | 47.89 | 30.14 | 55.83 | 47.48 | 43.97 |
| Qwen3-4B-Instruct | Best baseline (per dataset) | 41.17 | 51.38 | 34.41 | 61.35 | 48.48 | 45.74 |
| Qwen3-4B-Instruct | AgeMem-noRL | 38.02 | 50.42 | 27.52 | 57.48 | 54.49 | 45.59 |
| Qwen3-4B-Instruct | AgeMem | 48.97 | 59.48 | 35.07 | 72.56 | 55.49 | 54.31 |

## Ablations / Analysis
- RL matters. AgeMem improves over AgeMem-noRL by 8.53 average points on Qwen2.5-7B-Instruct and 8.72 on Qwen3-4B-Instruct.
- HotpotQA memory quality is highest for AgeMem on both backbones, with MQ of 0.533 for Qwen2.5 and 0.605 for Qwen3.
- Learned STM management reduces prompt tokens versus replacing STM tools with RAG. The paper reports a 3.1% token reduction on Qwen2.5-7B-Instruct and a 5.1% reduction on Qwen3-4B-Instruct.
- Tool usage shifts after RL. On Qwen2.5, `Add` rises from 0.92 to 1.64 calls per episode, `Update` appears from 0.00 to 0.13, `Delete` rises from 0.00 to 0.08, and `Filter` rises from 0.02 to 0.31.
- The full reward signal is better than answer-only training. On HotpotQA with Qwen2.5, All-Returns improves J from 0.509 to 0.544 and MQ from 0.479 to 0.533, while using more tool calls.

## Implementation Clues
- The source is a single ACL-style TeX project with `acl_latex.tex` as the top-level entry and chapter files under `source/extracted/sections/`.
- The appendix gives the concrete tool behavior: retrieval uses cosine similarity over embeddings, `Summary` compresses spans of context, and `Filter` removes messages by a similarity threshold.
- The paper says reward weights are set uniformly to 1.0, and the system is built with Agentscope and fine-tuned with Trinity.
- The local `repo/` directory exists but is empty, so there is no code repository content to read here.
- The paper fine-tunes on the HotpotQA training set and then evaluates on all five benchmarks.

## Limitations
- The paper uses a fixed set of memory tools, so finer-grained control is not explored.
- Evaluation covers five representative benchmarks, but broader task coverage would strengthen the claim of generality.
- RL fine-tuning is performed on HotpotQA training data, so the cross-benchmark results still depend on transfer from a single training source.

## Takeaways
- Treating memory as part of the policy is the main contribution, not a post-hoc memory module.
- Joint LTM + STM management is better than optimizing only one side of the memory stack.
- Staged RL with step-wise credit assignment is important because memory actions are fragmented and rewards are delayed.

## Open Questions
- How well does the unified tool policy transfer to more open-ended or less structured agent environments?
- Can the fixed tool set be expanded without making training unstable?
- Would a richer reward model further improve memory quality without increasing token usage?

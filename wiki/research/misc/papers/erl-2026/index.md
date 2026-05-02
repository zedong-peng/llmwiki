---
title: "Experiential Reflective Learning for Self-Improving LLM Agents"
domain: research
area: misc
type: paper
status: processed
updated: 2026-04-18
tags: [paper, misc, erl, agent-memory, self-improvement]
---
# Experiential Reflective Learning for Self-Improving LLM Agents

## Paper Meta
- Title: Experiential Reflective Learning for Self-Improving LLM Agents
- Authors: Marc-Antoine Allard, Arnaud Teinturier, Victor Xing, Gautier Viaud
- Affiliation: Illuin Technology
- Venue: not explicitly reported in the paper body; source uses an ICLR 2026 template
- Year: 2026
- Topic: misc
- Paper Slug: erl-2026
- arXiv: https://arxiv.org/abs/2603.24639
- PDF: 2603.24639.pdf
- Code Repo: not found locally
- Reading Source: TeX / source

## TL;DR
- ERL turns past agent experience into reusable heuristics, then retrieves only the most relevant heuristics at test time.
- On Gaia2 Search + Execution, it reaches 56.1% overall success, up from 48.3% for the ReAct baseline.
- The strongest gains come from selective retrieval, not from dumping more trajectories into context.

## Problem
- General-purpose LLM agents often restart from scratch on every task and do not accumulate reusable experience.
- Prior experiential methods either require multiple retries, use all extracted lessons regardless of relevance, or depend on heavy retrieval at every turn.
- The paper asks whether a lightweight memory of transferable heuristics can improve agent performance without parameter updates.

## Method
- ERL stores experience as structured heuristics built from a single task trajectory and its outcome.
- Each heuristic contains two parts: an analysis of what caused success or failure, and a learned guideline with explicit trigger conditions and recommended actions.
- At test time, the agent decomposes the new task, scores stored heuristics for relevance with an LLM ranker, and injects the top-$k$ heuristics into the system prompt.
- The default setup uses $k=20$ heuristics, GPT-5-mini as the agent backbone, and GPT-5.2 as the retrieval ranker.

## Benchmarks / Datasets
| Dataset / Benchmark | Task | Metric | Notes |
|---|---|---|---|
| Gaia2 Search / Execution | Long-horizon agent tasks in a simulated mobile environment | success rate, pass@3, pass^3 | 12 applications, 101 tools; heuristics accumulated on 8 universes and evaluated on 2 held-out universes |
| Gaia2 train universes | Source task pool for heuristic accumulation | success rate | 112 execution tasks and 132 search tasks |
| Gaia2 test universes | Held-out evaluation pool | success rate | 48 execution tasks and 28 search tasks |
| $\tau^2$-bench | Conversational agent tasks | success rate, pass@3, pass^3 | Appendix-only evaluation on Airline, Retail, and Telecom |

## Baselines
| Baseline | Type | Why Important | Notes |
|---|---|---|---|
| ReAct baseline | direct agent scaffold | Main reference point for success-rate gains | Gaia2 default agent loop |
| Few-shot trajectories | in-context raw experience | Tests whether raw trajectories are enough | Underperforms baseline at 46.4% overall |
| ExpeL | experiential memory method | Prior method that extracts reusable insights | 50.9% overall success |
| AutoGuide | guideline generation and retrieval | Prior method with context-aware guidelines | Strong Search, weak Execution |
| Embedding retrieval | retrieval ablation | Measures whether lexical/semantic similarity is enough | Uses Qwen3-Embedding-0.6B |
| Random retrieval | retrieval ablation | Tests whether quantity alone helps | Best random configuration reaches 53.8% overall |
| Iterative ERL | variant | Checks whether growing guidance during accumulation helps | Better source performance, worse test generalization |

## Main Results
| Dataset / Benchmark | Metric | Baseline | Ours | Gain / Delta | Notes |
|---|---|---|---|---|---|
| Gaia2 overall | success rate | 48.3% | 56.1% | +7.8% | Main reported result |
| Gaia2 Execution | success rate | 43.1% | 51.4% | +8.3% | Stronger than baseline and most ablations |
| Gaia2 Search | success rate | 53.6% | 60.7% | +7.1% | Largest split-level gain in the paper |
| Gaia2 overall | pass^3 | not reported | improved | +8.3% Execution, +10.6% Search | Reliability improves more than pass@3 |
| Gaia2 overall | pass@3 | not reported | not reported | not reported | The paper says gains are smaller than pass^3 gains |
| $\tau^2$-bench overall | success rate | 36.7% | 38.0% | +1.3% | Appendix result across Airline, Retail, Telecom |

## Ablations / Analysis
- `No retrieval` drops overall success to 53.8%, showing that simply having heuristics is not enough without selection.
- `Embedding retrieval` reaches 53.3% overall, below LLM-based retrieval at 56.1%.
- `Only failures` is best overall among outcome-specific variants at 58.9%, driven by Search at 67.9%, while `only successes` is weaker at 49.9%.
- Randomly adding more heuristics is non-monotonic; performance peaks around 40-60 random heuristics and then degrades.
- When reward signals are unavailable during heuristic generation, the agent identifies success/failure correctly about 70% of the time and ERL falls to 51.2%, still above baseline.
- Iterative ERL improves the source pool itself but generalizes worse to held-out universes, ending at 50.7% overall on test tasks.

## Implementation Clues
- The paper is implemented on the Agents Research Environments (ARE) platform for Gaia2.
- The baseline agent is the default ReAct scaffold, with ERL added only through prompt injection of retrieved heuristics.
- Heuristic generation and retrieval use GPT-5-mini and GPT-5.2 respectively; embedding retrieval uses Qwen3-Embedding-0.6B.
- Prompt caching matters: ERL roughly doubles input tokens during rollout, but cache hit rates remain high enough that scenario cost rises more moderately than raw token counts suggest.
- The source describes an approximate practical upper bound of $k=20$ heuristics because LLM-based retrieval becomes inefficient above that range.

## Limitations
- ERL depends on a useful outcome signal; performance degrades when the reward signal is missing or inferred imperfectly.
- Heuristics can be task-specific, and iterative accumulation may reduce diversity by narrowing the failure modes seen later.
- Telecommunication tasks in $\tau^2$-bench show weaker generalization, suggesting limits in dual-control settings and combinatorial task spaces.
- The method adds retrieval overhead and increases total API cost by about 40% in the reported evaluation setup.

## Takeaways
- Distilling experience into concise heuristics is more transferable than appending raw trajectories.
- Relevance filtering is the key ingredient; more memory is not automatically better.
- Failure-derived heuristics are especially useful for search-heavy tasks, while success-derived heuristics help execution-heavy tasks more.
- ERL is a practical self-improvement loop for closed-model or no-finetuning settings because it only changes context, not parameters.

## Open Questions
- How small can heuristics become before retrieval quality starts to collapse?
- Can a two-stage retrieval pipeline combine broad embedding recall with LLM reranking without losing too much efficiency?
- How should the system resolve conflicting heuristics as the pool grows?
- Can the approach be extended to settings with weaker feedback or richer human collaboration than Gaia2?

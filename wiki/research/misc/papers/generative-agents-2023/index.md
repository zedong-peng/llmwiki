---
title: "Generative Agents: Interactive Simulacra of Human Behavior"
domain: research
area: misc
type: paper
status: processed
updated: 2026-04-18
tags: [paper, misc, llm-agents, memory, reflection, simulation]
---
# Generative Agents: Interactive Simulacra of Human Behavior

## Paper Meta
- Title: Generative Agents: Interactive Simulacra of Human Behavior
- Authors: Joon Sung Park, Joseph C. O'Brien, Carrie J. Cai, Meredith Ringel Morris, Percy Liang, Michael S. Bernstein
- Year: 2023
- Venue: UIST '23
- Topic: misc
- Paper Slug: generative-agents-2023
- arXiv: https://arxiv.org/abs/2304.03442
- PDF: `2304.03442.pdf`
- Code Repo: official repo is linked in the source, but no local repo contents were present here
- Reading Source: TeX
- Legacy Note: [[agent-memory/papers/generative-agents-2023]]

## TL;DR
Generative Agents turns a language model into a long-horizon social simulator by adding natural-language memory, reflection, and planning. In Smallville, a 25-agent sandbox inspired by The Sims, the full architecture produced the strongest believability scores in interview-based evaluation and also showed emergent information diffusion, relationship formation, and coordinated party attendance over two simulated days.

## Problem
The paper starts from a gap in LLM-based agents: they can sound plausible at a single time point, but they do not naturally maintain long-term coherence as memories accumulate, social relationships evolve, and plans need to change. The authors want agents that act believably over time, not just answer one prompt well.

## Method
### Memory, Reflection, Planning
Generative agents use a memory stream that stores every observation as a natural-language record with a creation timestamp and a last-access timestamp. Retrieval combines three signals: recency, importance, and relevance. In the implementation, recency uses exponential decay with a factor of `0.995`, importance is scored by asking the model to rate poignancy on a `1-10` scale, and relevance is computed from embedding similarity.

Reflection is the mechanism for turning many memories into higher-level inferences. The paper triggers reflection when the sum of recent importance scores exceeds `150`, then asks the model to generate salient questions and synthesize answers from retrieved memories. Planning works top-down: the agent first makes a broad daily plan, then recursively decomposes that plan into hour-scale and 5-15 minute actions.

### Acting and Dialogue
At each step, the agent either continues its plan or reacts to new observations. If the reaction involves another agent, the system generates dialogue conditioned on a memory summary plus the current conversation history. Reflections and plans are written back into the memory stream so future retrieval can use them.

### Smallville
The simulation world, Smallville, is a Phaser-based sandbox with manually authored locations, collision maps, and object states. It contains 25 agents, each initialized from a natural-language paragraph that is split into seed memories. The user can observe agents, change object states in natural language, and even command an agent by speaking as its inner voice. The paper notes that the implementation used `gpt3.5-turbo`; GPT-4 was not yet generally available through the API at the time.

## Benchmarks / Datasets
| Dataset / Benchmark | Task | Metric | Notes |
|---|---|---|---|
| Controlled interview protocol | Probe self-knowledge, memory, planning, reactions, reflections | Human believability rankings and TrueSkill | 25 questions total; 100 US Prolific evaluators ranked five conditions |
| Smallville end-to-end simulation | Observe emergent social behavior over time | Information spread, network density, attendance, hallucination rate | 25 agents over two game days |

## Baselines
| Baseline | Type | Why Important | Notes |
|---|---|---|---|
| Full generative-agent architecture | System under test | Uses memory, reflection, and planning together | Best-performing condition in the paper |
| No reflection | Ablation | Tests whether higher-level synthesis matters | Keeps observations and plans |
| No reflection, no planning | Ablation | Tests whether planning adds coherence | Keeps only observations |
| No observation, no reflection, no planning | Ablation | Approximates prior LLM-agent style behavior | Worst ablation in the study |
| Crowdworker-authored responses | Human baseline | Checks whether the agent reaches a basic human-like level | Manual quality screening was applied |

## Main Results
### Controlled Interview Study
| Condition | TrueSkill mean | TrueSkill std | Notes |
|---|---|---|---|
| Full architecture | 29.89 | 0.72 | Highest believability |
| No reflection | 26.88 | 0.69 | Second best |
| No reflection, no planning | 25.64 | 0.68 | Lower than no-reflection |
| Crowdworker-authored | 22.95 | 0.69 | Human baseline, but below the full system |
| No observation, no reflection, no planning | 21.21 | 0.70 | Worst condition |

The paper reports that the full architecture beat the prior-work-style condition by a very large margin, with an effect size of `d = 8.16`. The overall rank differences were significant by Kruskal-Wallis test (`H(4)=150.29`, `p < 0.001`), and Dunn post-hoc tests found all pairwise differences significant except between the crowdworker condition and the fully ablated baseline.

### End-to-End Simulation
| Phenomenon | Reported value | Notes |
|---|---|---|
| Knowledge of Sam's candidacy | 1 agent (4%) to 8 agents (32%) | Spread without user intervention |
| Knowledge of Isabella's party | 1 agent (4%) to 13 agents (52%) | Spread without user intervention |
| Relationship network density | 0.167 to 0.74 | Mutual-knowledge graph density |
| Party attendance | 0 of 12 invited to 5 of 12 attended | Attendance on Valentine's Day |
| Hallucinated awareness responses | 6 of 453 responses (1.3%) | Checked against memory stream |

## Ablations / Analysis
The controlled evaluation makes the causal role of the architecture components fairly clear. Without planning, agents lose long-horizon coherence and can repeat obviously bad behavior. Without reflection, they struggle to synthesize deeper judgments from experience, such as choosing a person to spend time with based on accumulated interactions rather than raw frequency. Without memory retrieval, they lose self-consistency and often answer with generic or incorrect statements.

The paper also surfaces realistic failure modes. Agents can miss the right memory fragment, produce embellished claims that go beyond their actual experiences, or inherit overly formal and overly cooperative behavior from the underlying instruction-tuned model. The end-to-end simulation also showed that agents sometimes chose odd locations or violated local norms when those rules were not explicitly grounded in the environment description.

## Implementation Clues
- Source was read from `source/extracted/` (`main.tex`, section files, `main.bbl`); no PDF fallback was needed.
- No local official repo was present in `repo/`, so the repo was not read.
- The paper’s public demo URL is given in the source as `https://reverie.herokuapp.com/UIST_Demo/`.
- The architecture uses a cached agent summary built from core characteristics, current occupation, and recent progress.
- Runtime is described as roughly real-time game time, with `1` second of real time corresponding to `1` minute of game time.
- The key implementation knobs called out in the source are recency decay `0.995`, reflection threshold `150`, and top-k retrieval after min-max scaling.

## Limitations
The authors say the simulation was expensive: running 25 agents for two days cost thousands of dollars in token credits and took multiple days. They also flag vulnerability to prompt hacking, memory hacking, hallucination, and the usual language-model bias issues. More broadly, the paper warns that these agents should complement human stakeholders rather than replace them.

## Takeaways
Generative Agents is one of the clearest early demonstrations that adding structured memory and reflection to an LLM can create a believable long-horizon social system. The main technical lesson is that agent behavior becomes much more stable when the model can retrieve the right memories, generalize from them, and plan ahead instead of generating each step in isolation.

## Open Questions
- How far can the architecture scale before sequential memory and dialogue generation become too expensive?
- Which retrieval and reflection heuristics matter most once the base model improves?
- How can the environment model capture local physical norms more reliably?
- What is the right human baseline for believability in longer simulations?

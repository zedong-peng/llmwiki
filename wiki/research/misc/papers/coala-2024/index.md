---
title: Cognitive Architectures for Language Agents (CoALA)
domain: research
area: misc
type: paper
status: processed
updated: 2026-04-18
tags: [paper, misc, language-agents, cognitive-architecture, framework]
---
# Cognitive Architectures for Language Agents (CoALA)

## Paper Meta
- Title: Cognitive Architectures for Language Agents (CoALA)
- Authors: Theodore R. Sumers, Shunyu Yao, Karthik Narasimhan, Thomas L. Griffiths
- Year: 2024
- Venue: TMLR
- Topic: misc
- Paper Slug: coala-2024
- arXiv: https://arxiv.org/abs/2309.02427
- PDF: `2309.02427.pdf`
- Code Repo: not reported in this directory
- Reading Source: TeX source
- Legacy Note: [[agent-memory/papers/coala-2024]]

## TL;DR
CoALA is a conceptual framework for language agents. It organizes agents around memory, action space, and decision-making, then uses those concepts to reinterpret recent work such as SayCan, ReAct, Voyager, Generative Agents, and Tree of Thoughts.

## Problem
Recent language-agent papers used inconsistent terminology for similar mechanisms. The paper argues that this makes it hard to compare agents, reason about their evolution, or design new systems with clean abstractions.

## Method
CoALA adapts ideas from cognitive science and symbolic AI to language agents.
- Language models are treated as probabilistic production systems that sample completions conditioned on prompts.
- Prompt engineering becomes a form of control flow: the prompt sequence constrains which productions happen next.
- A full language agent is then described by memory modules, a structured action space, and a decision procedure.

## Framework Details
### Memory
CoALA separates memory into working memory and long-term memory.
- Working memory stores active state for the current decision cycle, including perceptual inputs, goals, and intermediate reasoning.
- Episodic memory stores experiences from prior cycles, such as trajectories or event traces.
- Semantic memory stores knowledge about the world or the agent.
- Procedural memory stores code and implicit model behavior; the paper emphasizes that procedural updates are the riskiest form of learning.

### Action Space
The paper divides actions into external grounding actions and internal actions.
- Grounding actions interact with physical, human, or digital environments and turn observations back into text.
- Retrieval actions read long-term memory into working memory.
- Reasoning actions transform working-memory contents into new intermediate knowledge.
- Learning actions write to long-term memory, including episodic updates, semantic updates, and procedural updates.

### Decision Making
Decision-making is a repeated cycle that uses reasoning and retrieval to propose and evaluate candidate actions, then selects a grounding or learning action to execute.
- This is presented as a more explicit alternative to simple prompt chains.
- The paper frames Tree of Thoughts as a stronger example of propose-evaluate-select behavior.
- CoALA treats learning as an action that can be chosen during the loop, not only as a fixed offline training step.

## Benchmarks / Datasets
| Dataset / Benchmark | Task | Metric | Notes |
|---|---|---|---|
| not reported | not reported | not reported | Conceptual framework paper; no new benchmark section with quantitative evaluation |

## Baselines
| Baseline | Type | Why Important | Notes |
|---|---|---|---|
| SayCan | robot grounding agent | Shows external grounding with a fixed skill library | No internal reasoning/retrieval/learning actions |
| ReAct | reasoning + acting agent | Minimal example of internal reasoning plus external action | Single reasoning step before acting |
| Voyager | embodied code agent | Shows procedural memory, retrieval, and learning | Uses code-based skills in Minecraft |
| Generative Agents | social simulation agent | Shows episodic/semantic memory plus learning | Uses reflections written back into memory |
| Tree of Thoughts | deliberative reasoning system | Shows explicit propose-evaluate-select planning | No long-term memory; mainly reasoning actions |

## Main Results
| Dataset / Benchmark | Metric | Baseline | Ours | Gain / Delta | Notes |
|---|---|---|---|---|---|
| not reported | not reported | not reported | CoALA framework | not reported | The paper is a synthesis and taxonomy, not an empirical benchmark paper |

## Case Studies
The paper maps several agents into the CoALA framework.

| Method | Long-term memory | External grounding | Internal actions | Decision style |
|---|---|---|---|---|
| SayCan | none beyond procedural code/value function | physical | none | evaluate |
| ReAct | none | digital | reason | propose |
| Voyager | procedural | digital | reason, retrieve, learn | propose |
| Generative Agents | episodic, semantic | digital/agent | reason, retrieve, learn | propose |
| Tree of Thoughts | none | digital final answer | reason | propose, evaluate, select |

## Ablations / Analysis
- No quantitative ablation table is reported in the paper.
- The analysis is structural: it compares what each agent stores, what actions it can take, and how it chooses actions.
- A key qualitative conclusion is that larger action spaces tend to require more customized decision procedures.

## Implementation Clues
- Source read from `source/extracted/main.tex`; no official code repository was present in this paper directory.
- The paper’s useful implementation abstraction is `Memory`, `Action`, and `Agent` classes, with explicit separation between working memory, long-term memories, grounding, retrieval, reasoning, and learning.
- The authors suggest using code sparingly for generic algorithms such as tree search, while relying on LLMs for flexible reasoning.

## Limitations
- The framework is conceptual, so it does not provide new experimental metrics or standardized task coverage.
- The paper acknowledges that many boundaries in agent design are ambiguous, especially internal vs external and single-agent vs multi-agent framing.
- Safety remains open, especially for risky grounding actions and procedural-memory modification.

## Takeaways
- CoALA gives a shared vocabulary for language-agent design.
- The most important design axes are memory, action space, and decision procedure.
- The paper’s strongest practical message is that modular, structured agents will be easier to compare, reuse, and extend than monolithic prompt chains.

## Open Questions
- Should future agents reason with language-only models or multimodal models?
- Where exactly is the boundary between an agent and its environment?
- How should agents balance learning against acting in an always-on loop?
- How much of CoALA will still matter as LLMs become more capable?

---
title: "Human-inspired Perspectives: A Survey on AI Long-term Memory (SALM)"
domain: research
area: misc
type: paper
status: processed
updated: 2026-04-19
tags: [paper, misc, survey, long-term-memory, salm]
---

# Human-inspired Perspectives: A Survey on AI Long-term Memory (SALM)

## Paper Meta
- Title: Human-inspired Perspectives: A Survey on AI Long-term Memory
- Authors: Zihong He, Weizhe Lin, Hao Zheng, Fan Zhang, Matt W. Jones, Laurence Aitchison, Xuhai Xu, Miao Liu, Per Ola Kristensson, Junxiao Shen
- arXiv: https://arxiv.org/abs/2411.00489
- Paper slug: `salm-survey-2025`
- Reading source: TeX (`main.tex` + `main.bbl`)
- Repo: not reported
- Year / venue: not reported in the extracted TeX
- PDF fallback: not used
- Legacy note: [[agent-memory/papers/salm-survey-2025]]

## TL;DR
- This is a narrative survey that links human long-term memory theory to AI long-term memory systems.
- The paper splits AI long-term memory by storage format into parametric and non-parametric memory, then maps both to human episodic, semantic, and procedural memory.
- It proposes SALM, a self-adaptive cognitive architecture with storage, retrieval, and forgetting adapters.
- The paper is conceptual and taxonomy-driven; it does not report new benchmark results.

## Problem
- Existing AI memory surveys are too narrow: some focus on computer memory or RNN/LSTM-style sequence storage, while others focus on LLM agents without grounding the discussion in human memory theory.
- The authors argue that current surveys do not provide a unified framework that explains AI memory through human memory hierarchy and processing.
- They also identify a gap in system design: existing cognitive architectures do not cover all memory types or provide a systematic adaptive mechanism for choosing storage, retrieval, and forgetting operations.

## Method
- The survey reviews literature from 2015 onward and states that the search was conducted on October 7, 2024.
- The search terms combine review/survey/taxonomy with memory and AI-related terms such as AI, agent(s), deep learning, machine learning, and neural network(s).
- The authors read human memory theory first, then use it to structure the AI memory review around storage format, memory type, and processing stage.
- They synthesize 37 papers related to AI memory survey work and organize them by research subject, publisher, and preprint server.

## Benchmarks / Datasets

| Item | Status | Notes |
|---|---|---|
| Benchmark results | not reported | Survey paper; no new experimental benchmark table. |
| Evaluation protocol | not reported | The paper proposes target-task-driven evaluation, but does not run experiments. |
| Datasets used for experiments | not reported | No original experiment section was reported in the extracted TeX. |
| Application datasets mentioned | reported | Ego4D, Ego-Exo4D, Replica, Project Aria appear in the video-understanding discussion. |

## Baselines

| Baseline / comparator | What the paper says | Gap relative to SALM |
|---|---|---|
| ACT / ACT-R | Early cognitive architectures with long-term memory and retrieval mechanisms | Do not cover all memory types or adaptive processing. |
| Soar | Strong on procedural memory, weaker on broader memory coverage | Missing broader episodic and semantic coverage. |
| Sigma | Broader coverage, including semantic memory | Still lacks a systematic adaptive mechanism. |
| SMoM | Separate declarative and procedural long-term memory modules | Limited coverage of the full parametric / non-parametric split. |
| CoALA | LLM-based architecture with episodic and semantic memory from external data | No full six-way coverage and no systematic adaptive loop. |
| SALM | Proposed framework | Covers all six forms of memory and adds adaptive storage, retrieval, and forgetting. |

## Main Results
- The paper’s main result is a two-axis taxonomy of AI long-term memory: storage format (`parametric` vs `non-parametric`) and human-memory analogy (`episodic`, `semantic`, `procedural`).
- It argues that non-parametric memory is better for externally stored, timely, and long-tail knowledge, while parametric memory is better for implicit generalization inside model weights.
- It gives a concrete mapping between AI memory mechanisms and human memory processes, including storage, retrieval, and forgetting.
- It proposes SALM as the first step toward an adaptive long-term memory architecture that can choose storage format, retrieval mode, and forgetting strategy based on feedback.

## Ablations / Analysis
- No empirical ablation study is reported.
- The paper explicitly suggests future ablations for SALM: isolate each memory module, compare individual adapters, and compare multi-stage pipeline assembly versus end-to-end integration.
- It also suggests comparing retrieval and storage choices under target-task-driven metrics rather than only task-local retrieval metrics.

## Implementation Clues
- The `storage adapter` should filter corrupted, poisoned, and privacy-sensitive inputs before deciding whether to store them.
- The `storage adapter` should also choose between parametric and non-parametric storage based on capacity, time-sensitivity, and long-tail information.
- The `retrieval adapter` should decide when retrieval is needed, choose sparse or dense retrieval, augment queries, and resolve conflicts or hallucinations.
- The `forgetting adapter` should support active forgetting for non-parametric memory and catastrophic-forgetting mitigation for parametric memory.
- The paper’s concrete method families include rehearsal, distance-based methods, sub-networks, dynamic networks, and curriculum learning for parametric forgetting.

## Limitations
- The paper is a survey and architecture proposal, not an implementation or benchmark paper.
- Existing cognitive architectures discussed in the paper do not cover all memory types and do not include a systematic adaptive mechanism.
- Human memory is still limited by interference and forgetting; the paper uses that limitation as motivation for making AI memory more adaptive.
- SALM is presented as a theoretical framework, so its effectiveness still needs empirical validation.

## Takeaways
- Human memory theory is used as the organizing principle for the AI memory literature, not just as inspiration.
- The cleanest practical split is storage format: external non-parametric memory versus internal parametric memory.
- Dense retrieval, vector databases, and query augmentation are central to modern non-parametric memory systems.
- SALM is most useful as a design target for future memory-heavy AI systems, especially in video understanding and cognition simulation.

## Open Questions
- What target-task metrics should be used to evaluate memory storage, retrieval, and forgetting?
- How should a system decide when to store information parametrically versus non-parametrically?
- Can the proposed adaptive adapters be trained reliably without causing new retrieval conflicts or hallucinations?
- Is a multi-stage pipeline or an end-to-end integrated SALM implementation more effective in practice?
- How should privacy-sensitive or poisoned inputs be filtered without losing useful long-tail information?

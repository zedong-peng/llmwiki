---
title: Research Taste
domain: research
area: research-taste
type: concept
status: stable
updated: 2026-04-08
tags: [core-concept, research-quality, judgment, impact]
---
# Research Taste

## Definition
"Research taste" refers to the judgment that guides a researcher toward important, attackable, well-timed, elegant, and fertile problems — and away from incremental or dead-end work. It includes the ability to:
- Identify which problems are worth working on
- Recognize which approaches are promising vs. dead ends
- Predict which ideas will be influential before they are proven
- Know when a result is surprising vs. expected

The term is borrowed from aesthetic taste, but here it means judgment about *what matters* in research.

## Why It Matters for AI Research Agents
As AI systems become capable of executing research tasks (writing code, running experiments, writing papers), the bottleneck shifts to **direction-setting**. An AI that can execute perfectly but has no taste will:
- Work on unimportant problems
- Pursue incremental improvements
- Miss the surprising connections that define great research

This is why taste benchmarks are emerging as a distinct category from execution benchmarks.

## Working Decomposition
The most useful decomposition in this area now comes from [[karpathy-perspective]]:
- **Importance**
- **Attackability**
- **Timing**
- **Elegance**
- **Fertility**

These are still hypotheses about the construct. A serious benchmark should validate whether they form one latent ability or several related ones.

## How It's Currently Operationalized

### Citation Velocity (TastyBench)
- Proxy: papers with high citation velocity = high impact
- Task: rank pairs of papers by predicted citation count
- Limitation: citations are lagging and popularity-sensitive

### Novelty Score (InnoGym)
- Proxy: methodological distance from prior work
- Task: generate solutions that are both effective and novel
- Limitation: novelty is not the same as taste

### Peer Review Simulation (MLR-Bench, AI Scientist)
- Proxy: LLM judge mimicking human peer review
- Task: generate research that passes automated review
- Limitation: LLM judges may have the same blind spots as LLM generators

## The Core Tension
**Taste is hard to measure because it's prospective.** We only know a paper was important after the fact. Any benchmark using historical data is measuring "taste in hindsight" — which may not correlate with "taste in foresight."

Possible approaches to this problem:
1. **Temporal holdout**: train on papers up to year X, test on predicting impact of papers from year X+1 to X+3
2. **Expert elicitation**: ask domain experts to rate idea quality before results are known
3. **Diversity of proxies**: combine citation, novelty, expert rating, and downstream influence
4. **Contamination checks**: quantify whether the model is recognizing papers rather than judging ideas
5. **Psychometric validation**: validate the latent structure instead of assuming it

## Related Concepts
- [[concepts/research-ability-dimensions]] — taste is one dimension among many
- [[concepts/evaluation-approaches]] — how to measure taste
- [[researchTaste-bench-design]] — current benchmark proposal

## Key Papers
- [[papers/hicke-2025-tastybench]] — first direct taste benchmark attempt
- [[papers/zhang-2024-innogym]] — novelty as one component of the story

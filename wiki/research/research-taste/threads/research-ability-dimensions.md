---
title: Research Ability Dimensions
domain: research
area: research-taste
type: concept
status: stable
updated: 2026-04-08
tags: [taxonomy, research-pipeline, dimensions, evaluation]
---
# Research Ability Dimensions

## Overview
AI research capability is not monolithic. Different benchmarks measure different stages of the research pipeline.

The strongest simplification is:

> **Research ability = Taste × Execution**, with ideation, planning, writing, and evaluation around that core loop.

## The Research Pipeline

```
Taste/Direction -> Idea Generation -> Proposal -> Execution -> Writing -> Evaluation
     ^                                                                      |
     +-------------------- feedback loop -----------------------------------+
```

### 1. Research Taste / Direction Setting
**What**: Identifying which problems and approaches are worth pursuing
**Measured by**: [[papers/hicke-2025-tastybench]], [[researchTaste-bench-design]]
**Key challenge**: Prospective judgment under uncertainty, disentangled from fame recall

### 2. Idea Generation / Novelty
**What**: Generating new hypotheses, methods, or approaches
**Measured by**: [[papers/zhang-2024-innogym]] (novelty + performance), [[papers/liang-2025-mlr-bench]] (ideation stage)
**Key challenge**: Distinguishing genuine novelty from recombination

### 3. Proposal Formulation
**What**: Turning an idea into a concrete, testable research plan
**Measured by**: [[papers/liang-2025-mlr-bench]] (proposal stage)
**Key challenge**: Feasibility and scope control

### 4. Execution / Experimentation
**What**: Implementing the plan, running experiments, getting results
**Measured by**: [[papers/starace-2025-paperbench]] (replication), [[papers/mlrc-bench-2025]] (competition tasks), [[papers/scientist-bench]]
**Key challenge**: Long-horizon coding, debugging, reproducibility

### 5. Scientific Writing
**What**: Communicating results clearly and persuasively
**Measured by**: [[papers/liang-2025-mlr-bench]] (writing stage), [[papers/lu-2024-ai-scientist]] (full paper)
**Key challenge**: Narrative coherence and honest limitations

### 6. Peer Review / Evaluation
**What**: Judging the quality of others' (or one's own) research
**Measured by**: [[papers/lu-2024-ai-scientist]] (automated reviewer), [[papers/liang-2025-mlr-bench]] (MLR-Judge)
**Key challenge**: Avoiding self-serving bias and circular evaluation

## Key Insight: The Decoupling Problem
MLR-Bench found that LLMs are **good at ideation and writing** but **bad at execution**. This creates one measurement problem:
- We can't verify if ideas are good without executing them
- Execution failures may mask taste failures
- Need benchmarks that decouple these dimensions

The complementary problem also matters:
- execution benchmarks cannot tell whether the model chose a worthwhile project

## What's Missing
Current benchmarks mostly cover execution and generation. The least-covered dimension is still **taste**, especially:
- timing/ripeness
- underrated-future-impact detection
- contamination-aware judgment
- construct-valid measurement

## Related Concepts
- [[concepts/research-taste]] — the hardest dimension to measure
- [[concepts/evaluation-approaches]] — how each dimension is evaluated
- [[researchTaste-bench-design]] — proposed taste-specific benchmark

---
title: Evaluation Approaches
domain: research
area: research-taste
type: concept
status: stable
updated: 2026-04-08
tags: [evaluation, methodology, proxies, metrics]
---
# Evaluation Approaches for Research Ability

## The Core Challenge
Research quality is subjective, prospective, and domain-dependent. Unlike coding or math benchmarks, it requires judgment about:
- Importance
- Novelty
- Correctness
- Impact
- Timing

## Current Approaches

### 1. Citation-Based (Retrospective Impact)
**Used by**: TastyBench
**Metric**: Citation count / citation velocity
**Pros**: Objective, measurable, community-validated
**Cons**:
- Lagging indicator (takes years to accumulate)
- Popularity bias (famous labs get more citations)
- Field-size effects (ML papers get more citations than niche fields)
- Gaming potential

### 2. Performance-Based (Objective Metrics)
**Used by**: MLRC-Bench, PaperBench
**Metric**: Does the code run? Does it reproduce the results? Does it beat the baseline?
**Pros**: Objective, unambiguous, automatable
**Cons**: Measures execution, not taste; a perfect executor with no taste would score 100%

### 3. Novelty-Based (Methodological Distance)
**Used by**: InnoGym
**Metric**: How different is the approach from prior work?
**Pros**: Captures originality
**Cons**: Novelty ≠ quality; being different isn't the same as being better or more insightful

### 4. LLM-as-Judge (Simulated Peer Review)
**Used by**: MLR-Bench (MLR-Judge), AI Scientist (automated reviewer)
**Metric**: LLM rates the quality of generated research
**Pros**: Scalable, flexible, can assess multiple dimensions
**Cons**:
- LLM judges may share blind spots with LLM generators
- Calibration against human experts is unclear
- Self-serving bias risk
- Circular-evaluation risk

### 5. Human Expert Evaluation
**Used by**: PaperBench (human baseline), various
**Metric**: Domain experts rate quality
**Pros**: Gold standard
**Cons**: Expensive, slow, hard to scale, inter-rater disagreement

## The Proxy Problem
Every current approach uses a **proxy** for research taste:
- Citations → impact
- Performance → execution quality
- Novelty → originality
- LLM judge → peer review

None directly measures "would a great researcher have chosen to work on this?" — the core of taste.

## Emerging Hybrid Strategy
The direction taken in this wiki is a hybrid:

1. Use **objective downstream signals** for the main answer key.
2. Use **LLM judgment only for diagnostic or auxiliary tasks**.
3. Use **blind protocols** to reduce label and family bias.
4. Add **contamination probes** so the benchmark reports memory effects directly.
5. Run **construct-validation analysis** so dimensions are tested, not assumed.

This is the logic behind [[researchTaste-bench-design]].

## Promising Directions
1. **Temporal holdout with expert annotation**
2. **Downstream influence** beyond raw citations
3. **Sleeping-beauty-sensitive metrics**
4. **Blind cross-family evaluation**
5. **Synthetic idea diagnostics**

## Related Concepts
- [[concepts/research-taste]] — what we're trying to measure
- [[concepts/research-ability-dimensions]] — what dimensions need evaluation
- [[researchTaste-bench-design]] — current synthesis of these approaches

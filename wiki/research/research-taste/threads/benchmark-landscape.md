---
title: Benchmark Landscape Comparison
domain: research
area: research-taste
type: comparison
status: stable
updated: 2026-04-08
tags: [benchmark, comparison, landscape]
---
# Research Ability Benchmark Landscape

## Overview Table

| Benchmark | Year | What It Measures | Proxy Used | Scale | Key Finding |
|-----------|------|-----------------|------------|-------|-------------|
| **TastyBench** | 2025 | Research taste (impact prediction) | Citation velocity | 1000 papers | Frontier LLMs have poor research taste |
| **ResearchTaste-Bench** | 2026 | Research taste (judgment under uncertainty) | Weighted downstream impact + SB signals | living | Separates taste from execution and reports contamination |
| **InnoGym** | 2024 | Innovation potential | Novelty + performance gain | 18 tasks | AI can improve but struggles with genuine novelty |
| **PaperBench** | 2025 | Research replication | Reproduction score | 20 ICML papers | Best AI: 21% vs human: 41.4% |
| **AI Scientist** | 2024 | End-to-end research generation | Automated peer review | Open-ended | Can produce workshop-level papers |
| **MLR-Bench** | 2025 | Full research pipeline | LLM judge (MLR-Judge) | 201 tasks | Good at ideation/writing, bad at execution |
| **MLRC-Bench** | 2025 | ML research challenges | Objective performance | Dynamic | Significant gaps remain |

## Dimension Coverage

| Benchmark | Taste | Ideation | Proposal | Execution | Writing | Evaluation |
|-----------|-------|----------|----------|-----------|---------|------------|
| TastyBench | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| ResearchTaste-Bench | ✅✅ | ❌ | ❌ | ❌ | ❌ | partial |
| InnoGym | partial | ✅ | ✅ | ✅ | ❌ | ❌ |
| PaperBench | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| AI Scientist | partial | ✅ | ✅ | ✅ | ✅ | ✅ |
| MLR-Bench | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| MLRC-Bench | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |

**Gap**: The field still lacks a mature benchmark for **taste** that is objective, contamination-aware, and theory-backed.

## Key Tensions

### Taste vs. Execution
Most benchmarks measure execution (can you do the research?) not taste (should you do this research?). This is the core separation behind the `Taste × Execution` framing.

### Objective vs. Subjective
- Objective metrics (PaperBench, MLRC-Bench): unambiguous but miss qualitative dimensions
- Subjective metrics (MLR-Judge, human review): richer but harder to scale and calibrate
- Mixed metrics (ResearchTaste-Bench): objective downstream ground truth with diagnostic judge-based probes

### Retrospective vs. Prospective
- Citation-based (TastyBench): measures impact after the fact
- Novelty-based (InnoGym): measures originality at generation time
- ResearchTaste-Bench: uses retrospective signals to evaluate prospective judgment
- True taste is prospective, so all historical benchmarks still face a benchmark-reality gap

### Validity vs. Convenience
- Most benchmarks choose a proxy and stop there
- ResearchTaste-Bench explicitly adds construct validation and predictive validity checks

## What ResearchTaste-Bench Tries to Add
1. **Three-tier ground truth**: not just citation count, but underrated and sleeping-beauty cases
2. **Contamination reporting**: score cards should expose contamination gap directly
3. **Living updates**: benchmark freshness as a design property
4. **Construct validation**: factor analysis rather than assumed dimensions
5. **Taste-specific diagnostics**: novelty bias, timing, and SB detection

## Research Opportunity
The strongest opportunity is not "another benchmark," but a benchmark with a stronger measurement story:
- clearer construct definition
- more faithful objective ground truth
- explicit leakage defenses
- psychometric validation
- direct comparison against execution benchmarks such as Scientist-Bench

## Related Pages
- [[concepts/research-taste]]
- [[concepts/research-ability-dimensions]]
- [[concepts/evaluation-approaches]]
- [[../concepts/researchTaste-bench-design]]

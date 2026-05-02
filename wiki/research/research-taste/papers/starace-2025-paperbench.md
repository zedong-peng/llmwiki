---
title: "PaperBench: Evaluating AI's Ability to Replicate AI Research"
domain: research
area: research-taste
type: paper
status: stable
updated: 2026-04-07
tags: [replication, benchmark, research-execution, code-generation]
arxiv: "2504.01848"
authors: [OpenAI / Starace et al.]
venue: arXiv
year: 2025
---
# PaperBench: Evaluating AI's Ability to Replicate AI Research

**arXiv:** https://arxiv.org/abs/2504.01848

## Abstract
PaperBench evaluates AI agents' ability to autonomously replicate complete machine learning research papers from scratch. Released April 2025 by OpenAI. Agents must replicate code, experiments, and results — not just summarize.

## Key Contributions
- 20 ICML 2024 Spotlight and Oral papers as tasks
- Author-approved hierarchically structured rubrics: **8,316 atomic grading tasks**
- Both LLM-based and human judges for assessment
- Measures end-to-end research execution capability

## Results
| Agent | Replication Score |
|-------|------------------|
| Claude 3.5 Sonnet (best) | 21.0% |
| GPT-4o | significantly lower |
| Gemini 2.0 Flash | significantly lower |
| Human researchers | **41.4%** |

Key gap: best AI at 21% vs. human baseline at 41.4%.

## What This Measures
Research **execution** — can you take a paper and reproduce it? This is distinct from:
- Research taste (identifying good ideas)
- Research generation (coming up with new ideas)
- Research evaluation (judging quality)

## Open Questions
- Replication ≠ innovation. A perfect replicator has zero taste.
- Is 41.4% human baseline surprisingly low? (Suggests replication is genuinely hard)
- What's the ceiling? Would a 100% replication score indicate research mastery?

## Connections
- [[concepts/research-ability-dimensions]] — replication is the "execution" dimension
- [[papers/lu-2024-ai-scientist]] — AI Scientist goes further: generates *new* papers
- [[comparisons/benchmark-landscape]]

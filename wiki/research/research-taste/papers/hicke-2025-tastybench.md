---
title: "TastyBench: Benchmarking LLM Research Taste"
domain: research
area: research-taste
type: paper
status: stable
updated: 2026-04-07
tags: [research-taste, citation-prediction, benchmark, impact-prediction]
arxiv: "2506.07738"
authors: [Yann Hicke, Shashank Shet, Aditya Bhatt, Dhruv Agarwal, Chloe Loughridge, Piero Molino]
venue: arXiv
year: 2025
---
# TastyBench: Benchmarking LLM Research Taste

**arXiv:** https://arxiv.org/abs/2506.07738
**Project:** https://tastybench.github.io/

## Abstract
TastyBench is a benchmark for evaluating the ability of LLMs to predict the impact of research papers, as measured by citation count. The authors curate a dataset of 1000 papers from top ML venues (NeurIPS, ICML, ICLR) and evaluate LLMs on their ability to rank papers by citation count.

## Key Contributions
- Operationalizes "research taste" as **citation velocity** — the rate at which a paper receives citations
- Pairwise ranking task: given two paper summaries, which will be more cited?
- Dataset of 1000 papers from NeurIPS, ICML, ICLR
- Evaluates frontier LLMs on this ranking task

## Methodology
- Papers are summarized (to avoid data contamination from memorized abstracts)
- LLMs are asked to rank pairs of papers by predicted citation count
- Citation velocity used as ground truth proxy for "impact"

## Key Findings
- **Frontier models are quite bad at predicting research impact** — they do not have superhuman research taste
- Current LLMs cannot reliably identify which research directions will be influential
- Suggests a significant gap between LLM capabilities and human expert judgment on research quality

## Open Questions
- Is citation count the right proxy for "research taste"? (Citations ≠ quality; popular ≠ important)
- Does this measure taste or just familiarity with citation patterns?
- How does this relate to the ability to *generate* high-impact ideas vs. *recognize* them?
- Would a model trained specifically on citation data do better, and would that constitute "taste"?

## Connections
- [[concepts/research-taste]] — defines what this benchmark is trying to measure
- [[papers/zhang-2024-innogym]] — complementary: measures innovation/novelty rather than impact prediction
- [[comparisons/benchmark-landscape]] — how this fits in the broader landscape

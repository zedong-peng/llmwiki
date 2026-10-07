---
title: "The AI Scientist: Fully Automated Scientific Discovery"
domain: research
area: research-taste
type: paper
status: active
updated: 2026-04-07
tags: [autonomous-research, paper-generation, scientific-discovery, end-to-end]
arxiv: "2408.06292"
authors: [Chris Lu et al., Sakana AI]
venue: arXiv
year: 2024
---
# The AI Scientist: Fully Automated Scientific Discovery

**arXiv:** https://arxiv.org/abs/2408.06292
**Blog:** https://sakana.ai/ai-scientist/

## Abstract
The AI Scientist is a fully automated system for open-ended scientific discovery. It generates novel research ideas, writes code to implement them, executes experiments, visualizes results, writes full scientific papers in LaTeX, and runs a simulated peer review process.

## Key Contributions
- End-to-end pipeline: idea → code → experiments → paper → review
- Automated reviewer achieving near-human performance in evaluating paper scores
- Open-ended: iteratively develops ideas and adds them to a growing knowledge base
- Papers produced exceed workshop acceptance thresholds

## AI Scientist v2 (2025)
- **arXiv:** https://arxiv.org/abs/2504.08066
- Submitted 3 fully autonomous manuscripts to a peer-reviewed ICLR workshop
- One manuscript achieved scores exceeding the average human acceptance threshold
- Uses agentic tree search for idea exploration

## What This Measures / Demonstrates
This is less a benchmark and more a **system demonstration**. It shows:
- AI can complete the full research loop autonomously
- But quality is still below top human researchers
- The bottleneck may be taste (idea selection) more than execution

## Open Questions
- The system generates many ideas — which ones does it pursue? This is the taste problem.
- Automated reviewer: can an LLM judge its own output reliably?
- Does producing workshop-level papers constitute "research taste" or just "research execution"?

## Connections
- [[research/research-taste/assets/starace-2025-paperbench/index]] — PaperBench tests replication; AI Scientist tests generation
- [[research/research-taste/threads/research-ability-dimensions]] — covers the full pipeline
- [[research/research-taste/assets/hicke-2025-tastybench/index]] — TastyBench asks: can LLMs identify which AI Scientist outputs are good?

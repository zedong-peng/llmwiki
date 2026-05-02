---
title: "Agentless: Demystifying LLM-based Software Engineering Agents"
domain: research
area: misc
type: paper
status: queued
updated: 2026-04-20
tags: [paper, misc, code-retrieval, agentless, software-engineering, file-localization, swe-bench]
---
# Agentless: Demystifying LLM-based Software Engineering Agents

## Paper Meta
- Title: Agentless: Demystifying LLM-based Software Engineering Agents
- Authors: Chunqiu Steven Xia, Yinlin Deng, Soren Dunn, Lingming Zhang
- Year: 2024
- Venue: arXiv preprint
- Topic: misc
- Paper Slug: agentless-2024
- arXiv: https://arxiv.org/abs/2407.01489
- Code Repo: https://github.com/OpenAutoCoder/Agentless
- Reading Source: secondary sources (abstract, related work mentions, SWE-bench leaderboard)
- PDF Fallback: not yet downloaded
- Ingest Status: queued — needs full TeX/PDF read

## TL;DR
- Agentless proposes a simple, non-agentic approach to software engineering tasks that achieves competitive results on SWE-bench.
- The key insight: instead of giving an LLM agent free-form tool access, use a **hierarchical localization** pipeline followed by direct patch generation.
- The localization step is the most relevant part for compiled retrieval: it uses LLM reasoning to narrow down from repo structure → files → classes/functions, without any embedding or vector search.

## Problem
- Agentic approaches (SWE-agent, AutoCodeRover) give LLMs tool access and let them explore freely, but this leads to long trajectories, high cost, and unpredictable behavior.
- Agentless argues that a simpler, structured pipeline can match or beat agentic approaches.

## Method

### Hierarchical Localization (most relevant to compiled retrieval)
The localization pipeline has three stages:

1. **File-level localization**
   - Input: issue description + repo file tree (just file paths)
   - LLM identifies suspicious files based on file names and issue keywords
   - This is essentially LLM-compiled file-path grep

2. **Class/Function-level localization**
   - Input: issue description + skeleton of suspicious files (class/function signatures)
   - LLM identifies specific classes/functions to edit

3. **Line-level localization**
   - Input: issue description + full content of identified functions
   - LLM identifies specific lines to edit

### Key Insight for Compiled Retrieval
- Agentless's localization is a form of **compiled retrieval without explicit keyword predicates**
- Instead of generating keywords and grepping, it uses the LLM to directly reason about file paths and code structure
- The question for our paper: can explicit keyword predicates (GrepQA-style) match or beat this hierarchical reasoning approach?

## Relevance to Compiled Retrieval Project

### Comparison Dimensions
| Dimension | Agentless | GrepQA-Code |
|---|---|---|
| Query formulation | LLM reasons over file tree | LLM generates keyword predicates |
| Retrieval engine | LLM selection (no search) | Exact keyword matching |
| Granularity | Hierarchical (file → class → line) | Flat (keyword match over all files) |
| LLM calls | 3+ (one per level) | 1 (predicate generation) + 1 (answer) |
| Cost | Higher (multiple LLM calls with large context) | Lower (small predicate call + grep) |

### Potential Experiments
1. Compare GrepQA-Code vs Agentless localization on SWE-bench Verified
2. Test whether GrepQA-Code's flat keyword search can match hierarchical reasoning
3. Test hybrid: GrepQA-Code for initial file filtering, then Agentless-style refinement

## Main Results (from SWE-bench leaderboard)
- Agentless achieves ~27% resolve rate on SWE-bench Lite (as of mid-2024)
- Competitive with SWE-agent and other agentic approaches
- Much lower cost and fewer LLM calls than agentic approaches

## Open Questions
- What is Agentless's exact file localization accuracy (independent of patch generation)?
- How does the hierarchical approach scale with repo size?
- Can keyword predicates provide a cheaper first-stage filter before hierarchical refinement?

## Next Steps
- [ ] Download and read full paper
- [ ] Extract exact localization accuracy numbers
- [ ] Implement GrepQA-Code comparison on same SWE-bench instances

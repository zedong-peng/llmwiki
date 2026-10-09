---
title: "Agentless: Demystifying LLM-based Software Engineering Agents"
domain: research
area: misc
type: paper
status: seed
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
- The localization step uses LLM reasoning to narrow down from repo structure → files → classes/functions, without any embedding or vector search.

## Problem
- Agentic approaches (SWE-agent, AutoCodeRover) give LLMs tool access and let them explore freely, but this leads to long trajectories, high cost, and unpredictable behavior.
- Agentless argues that a simpler, structured pipeline can match or beat agentic approaches.

## Method

### Hierarchical Localization
The localization pipeline has three stages:

1. **File-level localization**
   - Input: issue description + repo file tree (just file paths)
   - LLM identifies suspicious files based on file names and issue keywords

2. **Class/Function-level localization**
   - Input: issue description + skeleton of suspicious files (class/function signatures)
   - LLM identifies specific classes/functions to edit

3. **Line-level localization**
   - Input: issue description + full content of identified functions
   - LLM identifies specific lines to edit

## Main Results (from SWE-bench leaderboard)
- Agentless achieves ~27% resolve rate on SWE-bench Lite (as of mid-2024)
- Competitive with SWE-agent and other agentic approaches
- Much lower cost and fewer LLM calls than agentic approaches

## Open Questions
- What is Agentless's exact file localization accuracy (independent of patch generation)?
- How does the hierarchical approach scale with repo size?

## Next Steps
- [ ] Download and read full paper
- [ ] Extract exact localization accuracy numbers

## Migration Reading Boundary

This is an unread reference seed based on the secondary sources listed above. No full-paper reading is recorded. Citation and historical provenance: [[research/misc/assets/agentless-2024/citation.bib]]. Migration did not read the archived paper or execute code.

---
title: "ReAct: Synergizing Reasoning and Acting in Language Models"
domain: research
area: agent-memory
type: paper
status: stub
updated: 2026-05-28
tags: [paper, reasoning, acting, agent, search, framework]
---

# ReAct: Synergizing Reasoning and Acting in Language Models

## Paper Meta
- Title: ReAct: Synergizing Reasoning and Acting in Language Models
- Authors: Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan Cao
- Year: 2023
- Venue: ICLR 2023
- arXiv: https://arxiv.org/abs/2210.03629

## TL;DR
- Interleave reasoning traces with actions (including search).
- Framework-level inspiration for agentic retrieval.
- Uses Wikipedia search API (semantic), not symbolic predicates.

## Relevance to LAzyMem
Framework-level inspiration for agentic retrieval. The "reason → act → observe" loop maps to LAzyMem's "compile predicate → execute exact match → aggregate." Key distinction: ReAct uses semantic Wikipedia search; LAzyMem uses symbolic boolean predicates over raw conversation turns.

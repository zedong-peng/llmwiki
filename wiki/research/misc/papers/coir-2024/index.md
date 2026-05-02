---
title: "CoIR: A Comprehensive Benchmark for Code Information Retrieval Models"
domain: research
area: misc
type: paper
status: queued
updated: 2026-04-20
tags: [paper, misc, code-retrieval, code-search, benchmark, coir, mteb]
---
# CoIR: A Comprehensive Benchmark for Code Information Retrieval Models

## Paper Meta
- Title: CoIR: A Comprehensive Benchmark for Code Information Retrieval Models
- Authors: Xiangyang Li, Kuicai Dong, Yi Quan Lee, Wei Xia, Yichun Yin, Hao Zhang, Yong Liu, Defu Lian, Yasheng Wang
- Year: 2024
- Venue: arXiv preprint
- Topic: misc
- Paper Slug: coir-2024
- arXiv: https://arxiv.org/abs/2407.02883
- Code Repo: https://github.com/CoIR-team/coir (likely)
- Reading Source: secondary sources (abstract, related work mentions)
- PDF Fallback: not yet downloaded
- Ingest Status: queued — needs full TeX/PDF read

## TL;DR
- CoIR is a comprehensive benchmark for evaluating retrieval/embedding models specifically on code-related tasks.
- It covers multiple programming languages and diverse code retrieval scenarios.
- Compatible with MTEB framework, making it easy to compare with general-purpose embedding models.
- Fills a gap where most IR benchmarks (BEIR, MTEB) focus on natural language, not code.

## Problem
- Most retrieval benchmarks evaluate on natural language documents.
- Code retrieval has unique characteristics: identifiers are precise, syntax matters, cross-file dependencies exist.
- No comprehensive benchmark existed that systematically evaluates retrieval models across diverse code retrieval tasks.

## Relevance to Compiled Retrieval Project

### Why CoIR Matters
- Code is the **most lexical-faithful** domain: function names, variable names, API calls are exact strings.
- If compiled retrieval (LLM-generated keyword predicates + exact matching) works anywhere, it should work on code.
- CoIR provides a standardized evaluation framework to test this hypothesis across multiple code retrieval sub-tasks.

### Expected Tasks (based on benchmark description)
| Task Type | Description | Lexical Faithfulness |
|---|---|---|
| NL → Code | Natural language query to code function | Medium-High |
| Code → Code | Code snippet to similar code | High |
| Bug → Fix | Bug description to fix | Medium |
| API → Usage | API name to usage examples | Very High |
| Doc → Code | Documentation to implementation | Medium |

### GrepQA-Code Applicability
- NL → Code: LLM generates keyword predicates from NL query (function names, API calls)
- Code → Code: extract identifiers from query code, search for matching identifiers
- API → Usage: direct keyword match on API names — GrepQA's strongest case

## Open Questions
- What are the exact tasks and datasets included in CoIR?
- What are the current SOTA results on CoIR?
- How do code-specific embedding models (Voyage Code, Jina Code) perform vs BM25 on CoIR?
- Can GrepQA-style predicates outperform both on the lexical-faithful subtasks?

## Next Steps
- [ ] Download and read full paper
- [ ] Understand exact task list and evaluation protocol
- [ ] Set up CoIR evaluation pipeline
- [ ] Run GrepQA-Code vs baselines

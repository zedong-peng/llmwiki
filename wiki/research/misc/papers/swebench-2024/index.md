---
title: "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?"
domain: research
area: misc
type: paper
status: queued
updated: 2026-04-20
tags: [paper, misc, code-retrieval, swe-bench, software-engineering, benchmark, file-localization]
---
# SWE-bench: Can Language Models Resolve Real-World GitHub Issues?

## Paper Meta
- Title: SWE-bench: Can Language Models Resolve Real-World GitHub Issues?
- Authors: Carlos E. Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, Karthik Narasimhan
- Year: 2024
- Venue: ICLR 2024
- Topic: misc
- Paper Slug: swebench-2024
- arXiv: https://arxiv.org/abs/2310.06770
- Code Repo: https://github.com/princeton-nlp/SWE-bench
- Reading Source: secondary sources (paper abstract, leaderboard, related work from other papers)
- PDF Fallback: not yet downloaded
- Ingest Status: queued — needs full TeX/PDF read

## TL;DR
- SWE-bench is a benchmark for evaluating LLMs on resolving real-world GitHub issues by generating code patches.
- The dataset contains 2,294 task instances from 12 popular Python repositories.
- **File localization** — identifying which files need to be modified — is a critical sub-task and the most relevant aspect for the compiled retrieval project.
- SWE-bench Lite (300 instances) and SWE-bench Verified (500 instances) are curated subsets.

## Problem
- Existing code generation benchmarks (HumanEval, MBPP) test isolated function generation, not real-world software engineering.
- Real software engineering requires understanding large codebases, finding relevant files, understanding context, and generating correct patches.
- The retrieval/localization step is often the bottleneck — if you can't find the right files, you can't fix the bug.

## Relevance to Compiled Retrieval Project

### File Localization as Code Retrieval
- Given an issue description, the agent must find which files (out of hundreds or thousands) need to be modified.
- Issue descriptions often contain: error messages, function names, file paths, stack traces — all **lexical-faithful** signals.
- This is a natural testbed for GrepQA-Code: LLM generates keyword predicates from the issue, grep over the codebase.

### Known Retrieval Approaches on SWE-bench
| Method | Approach | Notes |
|---|---|---|
| Agentless | Hierarchical: repo structure → file → class/function | No embedding, LLM-driven localization |
| SWE-agent | Interactive grep/find in terminal | Agent-driven lexical search |
| AutoCodeRover | AST-based search + spectrum-based fault localization | Structured search |
| Moatless Tools | Embedding-based retrieval with code-specific models | Dense retrieval |
| OpenHands | Hybrid BM25 + embedding | Hybrid approach |
| Aider | Tree-sitter AST + repo map | Structured + lexical |

### Evaluation Metrics for File Localization
- Recall@K: fraction of gold files found in top-K predictions
- Precision@K: fraction of top-K predictions that are gold files
- File-level accuracy: exact match of predicted file set

## Benchmarks / Datasets
| Dataset | Size | Notes |
|---|---|---|
| SWE-bench (full) | 2,294 instances | 12 Python repos |
| SWE-bench Lite | 300 instances | Curated subset, more tractable |
| SWE-bench Verified | 500 instances | Human-verified subset |

## Key Numbers (from leaderboard and related papers)
- Top systems resolve ~50% of SWE-bench Verified instances (as of early 2026)
- File localization accuracy varies widely: from ~30% (naive) to ~80% (best systems)
- Most top-performing systems use some form of lexical search (grep, find) as part of their pipeline

## Open Questions
- What is the exact file localization accuracy of pure GrepQA-style keyword search vs embedding-based retrieval?
- How does the number of files in the repo affect the relative performance of lexical vs dense retrieval?
- Can structured predicates (with file_pattern, language filters) outperform free-form LLM reasoning for localization?

## Next Steps
- [ ] Download and read full paper (TeX or PDF)
- [ ] Download SWE-bench Verified dataset
- [ ] Implement GrepQA-Code file localization pipeline
- [ ] Run comparison experiments

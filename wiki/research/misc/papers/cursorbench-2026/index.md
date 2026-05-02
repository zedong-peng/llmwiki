---
title: How We Compare Model Quality in Cursor
domain: research
area: misc
type: paper
status: processed
updated: 2026-04-19
tags: [paper, misc, benchmark, coding-agents, cursor, evaluation]
---

# How We Compare Model Quality in Cursor

## Paper Meta
- Title: How We Compare Model Quality in Cursor
- Author: Naman Jain
- Date: March 11, 2026
- Venue: Cursor Research blog
- Topic: misc
- Paper Slug: cursorbench-2026
- Canonical URL: https://cursor.com/blog/cursorbench
- Reading Source: official Cursor blog post
- TeX/source: unavailable
- PDF fallback: not used

## TL;DR
- CursorBench is Cursor's internal benchmark suite for coding agents, built from real developer-agent sessions rather than public GitHub issues or synthetic tasks.
- The central claim is that public coding benchmarks are increasingly misaligned, under-specified, and contaminated, so they no longer separate frontier models well.
- CursorBench-3 increases task scope substantially relative to earlier internal versions and public SWE-style benchmarks, with more files, larger edits, and shorter, more realistic task descriptions.
- Cursor uses CursorBench as only one half of a hybrid evaluation loop; offline benchmark rankings are checked against controlled online experiments to avoid optimizing to the wrong metric.

## Problem
- Public coding benchmarks are increasingly weak proxies for real agent usefulness in software development.
- The post argues that many public tasks are too narrow, over-focused on bug fixing, or shaped like puzzle problems rather than realistic engineering work.
- Grading is also fragile because many real developer requests are under-specified and admit several valid solutions, while benchmark graders often assume one narrow gold answer.
- The blog additionally claims contamination is severe for public repository benchmarks, making top-line scores less trustworthy at frontier model levels.

## Method
- Cursor sources tasks through `Cursor Blame`, a pipeline that traces committed code back to the original agent request that produced it.
- This yields a natural pair of developer query and ground-truth solution from actual internal use, rather than curated issues rewritten into benchmark tasks.
- Many tasks come from Cursor's internal codebase and controlled sources, which the post says reduces training-data contamination risk.
- Cursor refreshes the suite every few months so the task distribution tracks changes in how developers actually use coding agents.
- The benchmark is evaluated across multiple dimensions including solution correctness, code quality, efficiency, and interaction behavior, though the post only reports correctness-oriented results.
- Tasks are intentionally short and ambiguous in wording, closer to real prompts developers give agents than to fully specified issue descriptions.
- Grading uses agentic evaluators rather than strict exact-match or patch-match logic, which is important because many valid solutions differ from the reference implementation.

## Benchmark Design Notes
| Aspect | CursorBench claim | Why it matters |
|---|---|---|
| Task source | Real Cursor sessions | Better alignment with actual developer workflows |
| Gold solution | Committed developer outcome | Natural supervision instead of synthetic labels |
| Contamination control | Internal / controlled sources | Lower chance of memorized public patches |
| Prompt style | Short, ambiguous requests | Closer to real agent usage |
| Grading | Agentic graders | Better fit for under-specified tasks |
| Refresh cycle | Every few months | Keeps pace with changing agent work patterns |

## Baselines / Comparisons
| Baseline | Type | Why Cursor critiques it |
|---|---|---|
| SWE-bench Verified | public coding benchmark | May be contaminated and too issue-centric |
| SWE-bench Pro | public coding benchmark | Same public-repo exposure and grading limits |
| SWE-bench Multilingual | public coding benchmark | Also sourced from public repos |
| Terminal-Bench | agent benchmark | The post says its puzzle-like tasks are less aligned with coding work |

## Main Results
- CursorBench reportedly produces more separation between frontier models than the public benchmarks Cursor compares against.
- The benchmark rankings are said to align better with Cursor's online product metrics, meaning offline winners are more likely to match what developers experience in practice.
- CursorBench-3 roughly doubles problem scope relative to the initial internal version in terms of lines changed and mean number of files.
- The post highlights harder task patterns such as monorepo work, multi-workspace setups, production-log investigation, and long-running experiments.
- The semantic-search ablation in online evals is used as an example of why offline-only evaluation is insufficient: changes that look good under a grader may still fail developers in real workflows.

## Experimental Framing
- The post describes Cursor's process as a hybrid online-offline evaluation loop.
- Offline evals are used to compare model behavior under controlled conditions.
- Online evals aggregate higher-level interaction and output-quality proxies to check whether a change genuinely improves user outcomes.
- Controlled ablations are then used to attribute causality for specific system components such as semantic search and retrieval.

## Implementation Clues
- `Cursor Blame` is the key internal data-generation mechanism for deriving benchmark tasks from production usage.
- Agentic graders are central to the evaluation design because exact patch matching would over-penalize alternative valid solutions.
- Cursor is optimizing for task families that include broader codebase changes, repository-grounded question answering, and longer-horizon agent behavior rather than just bug-fix patches.
- CursorBench-3 is still fundamentally a single-session benchmark; the team expects the next generation to target long-running agents operating over longer timescales.

## Limitations
- CursorBench is not publicly released in this post, so the benchmark cannot currently be independently reproduced from the information provided.
- Most evidence in the article is comparative and figure-based; the text gives few precise numerical results in the accessible blog narrative.
- Because the task source is internal, external researchers cannot directly inspect task distribution, grader prompts, or contamination controls.
- The article is a product-research post, not a formal paper with exhaustive methodological detail.

## Takeaways
- CursorBench is best understood as a benchmark design argument: realistic task sourcing and evaluation methodology matter more than squeezing another point out of saturated public leaderboards.
- The most durable idea here is the online-offline loop, not just the offline benchmark itself.
- For the wiki, CursorBench is a useful reference point when comparing coding-agent evaluations against SWE-bench-style public benchmarks and longer-horizon agent benchmarks.

## Open Questions
- Can a partially public version of CursorBench be released without reintroducing contamination and overfitting?
- How reliable are agentic graders compared with human judgments on under-specified coding tasks?
- What should a benchmark for long-running coding agents look like once tasks span multiple sessions, external services, and asynchronous execution?

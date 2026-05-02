---
title: Research Log
domain: research
type: timeline
status: active
updated: 2026-04-23
tags: [research, log]
---

# Wiki Log

## [2026-04-23] note | Mem0 2026 algorithm as moving agent-memory baseline

Created a research thread for the 2026-04-16 Mem0 token-efficient memory algorithm blog and its impact on local agent-memory benchmark planning.

Page created:
- `wiki/research/misc/threads/2026-04-23-mem0-new-algorithm-benchmark-decision.md`

Key synthesis: The new Mem0 algorithm should not replace the citable 2025 paper baseline, but it is too close to ignore. Recommended strategy is to keep the paper result as the formal literature baseline and run a small controlled evaluation of the new SDK / blog-era algorithm on temporal, multi-hop, assistant-fact, and knowledge-update slices. Report the two baselines separately because vendor-reported managed-platform scores are not directly comparable to local micro-F1 results.

## [2026-04-21] update | AutoBool venue updated to EACL 2026

Updated the paper note at `wiki/research/misc/papers/autobool-2026/index.md` and the misc paper index so AutoBool is now tracked as an `EACL 2026` paper rather than `Arxiv`.

Metadata sync:
- `wiki/research/misc/papers/autobool-2026/metadata.yaml` now records `venue: EACL 2026`
- publication status set to `published`
- arXiv link retained as the preprint pointer

Reason:
- User reported that AutoBool has now appeared at EACL 2026, so the wiki should distinguish publication venue from artifact hosting.

## [2026-04-07] init | Wiki created — Research Taste Benchmark

Initial wiki setup. Ingested knowledge from web search on the following topics:
- TastyBench (arxiv 2506.07738) — LLM research taste via citation prediction
- InnoGym (arxiv 2512.01822) — AI innovation potential benchmark
- PaperBench (arxiv 2504.01848) — OpenAI research replication benchmark
- The AI Scientist (arxiv 2408.06292) — Sakana AI end-to-end research system
- MLR-Bench (arxiv 2505.19955) — open-ended ML research benchmark
- MLRC-Bench (arxiv 2504.09702) — ML research competition benchmark

Pages created:
- wiki/index.md
- wiki/research-taste/overview.md
- wiki/research-taste/papers/hicke-2025-tastybench.md
- wiki/research-taste/papers/zhang-2024-innogym.md
- wiki/research-taste/papers/starace-2025-paperbench.md
- wiki/research-taste/papers/lu-2024-ai-scientist.md
- wiki/research-taste/papers/liang-2025-mlr-bench.md
- wiki/research-taste/papers/mlrc-bench-2025.md
- wiki/research-taste/concepts/research-taste.md
- wiki/research-taste/concepts/research-ability-dimensions.md
- wiki/research-taste/concepts/evaluation-approaches.md
- wiki/research-taste/concepts/karpathy-perspective.md
- wiki/research-taste/comparisons/benchmark-landscape.md

Key synthesis: The field has good coverage of execution and generation benchmarks, but "taste" (prospective judgment about what's worth doing) remains the least-measured dimension. TastyBench is the first direct attempt but uses citation count as a proxy, which has significant limitations.

## [2026-04-07] init | Wiki created — Claude Code Memory System

Area 2 created. Source: leaked Claude Code source code at `raw/claude-code-source/src/`.

Pages created:
- wiki/claude-code-memory/overview.md
- wiki/claude-code-memory/concepts/memdir-long-term.md
- wiki/claude-code-memory/concepts/extract-memories.md
- wiki/claude-code-memory/concepts/find-relevant-memories.md
- wiki/claude-code-memory/concepts/agent-memory.md

Key synthesis: Claude Code's memory system is the industrial-grade instantiation of the Karpathy LLM wiki pattern — markdown files + LLM indexing, async background extraction, and a tiered recall strategy. No vector DB. The 200-line MEMORY.md cap and the security exclusion of projectSettings are the most notable design decisions.

## [2026-04-07] init | New area — LLM-Generated Executable Search for Conversation Memory

New research area created from exploration of `agent-memory-locomo` repo and related work survey.

Source material:
- `agent-memory-locomo/research/survey.md` — full prior art survey (38 papers)
- `agent-memory-locomo/experiments/locomo_memory.py` — current implementation
- `agent-memory-locomo/benchmark.md` — current numbers

Pages created:
- wiki/llm-grep-retrieval/overview.md
- wiki/llm-grep-retrieval/concepts/problem-definition.md
- wiki/llm-grep-retrieval/concepts/related-work.md
- wiki/llm-grep-retrieval/concepts/experiments.md

Key synthesis: The idea of LLM-generated *executable* search programs (grep/boolean/filter) for long-conversation memory retrieval appears untested on LoCoMo. Adjacent work (AutoBool for literature search, Mintlify ChromaFs in production) validates the direction. Current heuristic multi-query baseline shows +4.88% F1 on a pilot run (16.53% → 21.41%), validating the multi-query direction. The next step is replacing heuristic query generation with LLM-generated structured programs. Target: beat A-MEM (~35% F1) with GPT-4o-mini.

## [2026-04-08] update | venue reassessment + declarative query systems survey

Reassessed publication strategy after surveying LongMemEval SOTA (95%+ accuracy) and identifying the declarative query systems cluster as the right framing for our work.

Key findings:
- LongMemEval SOTA: Chronos 95.60%, MemMachine 93.0%, Mnemis 91.6% — memory benchmark space is saturated
- NeurIPS with current results (43.1% on LongMemEval, 29.76% F1 on LoCoMo) is not viable without a strong new angle
- Core contribution reframed: **zero-index symbolic retrieval** — LLM generates grep/boolean predicates, executes directly on raw text, no embedding required
- Closest prior work identified: SQUINT (ASPLOS 2024) — LLM-generated boolean queries for IR without embedding
- Recommended venues: VLDB/SIGMOD or CIDR, framing as "declarative/symbolic retrieval" not "memory benchmark"

Pages updated:
- wiki/llm-grep-retrieval/overview.md — added Venue Reassessment section with venue table and next steps
- wiki/llm-grep-retrieval/concepts/related-work.md — added Declarative Query Systems section (SQUINT, LOTUS, Palimpzest) + Venue Analysis table; updated Gap Summary with new prior work

Pages created:
- wiki/llm-grep-retrieval/papers/xu-2024-squint.md — SQUINT notes (⚠️ PDF not yet verified)
- wiki/llm-grep-retrieval/papers/patel-2025-lotus.md — LOTUS/Semantic Operators notes
- wiki/llm-grep-retrieval/papers/liu-2024-palimpzest.md — Palimpzest notes

PDFs downloaded:
- wiki/llm-grep-retrieval/papers/pdfs/lotus-2407.11418.pdf ✅
- wiki/llm-grep-retrieval/papers/pdfs/palimpzest-2405.14696.pdf ✅
- wiki/llm-grep-retrieval/papers/pdfs/squint-2411.07643.pdf ⚠️ wrong paper (xCG), need correct PDF

TODO:
- [ ] Find correct SQUINT PDF (ACM DL: 10.1145/3698038.3698548)
- [ ] Read SQUINT to determine exact differentiation
- [ ] Decide: memory domain vs general IR framing
- [ ] If VLDB/CIDR: add cost/latency analysis (embedding cost vs LLM grep token cost)



Full sweep of `agent-memory-locomo/research/survey.md` (39 papers, 16 sections). Synchronized all wiki pages with latest survey content.

Source: `agent-memory-locomo/research/survey.md` (April 7, 2026 version)

Pages updated:
- wiki/llm-grep-retrieval/overview.md — added ⚠️ metric warning (accuracy ≠ micro F1), ByteRover/Hindsight context, "Two Complementary Directions" structure (HeuristicRetriever + SymbolicRetriever), full leaderboard with Metric column, updated NeurIPS framing as *adaptive retrieval planning*
- wiki/llm-grep-retrieval/concepts/related-work.md — added Recollection-Familiarity Retrieval (arXiv:2603.09250) to Closest Prior Art; expanded Multi-Query section with FLARE, ITER-RETGEN, Self-RAG, FAIR-RAG, Query Decomposition as Bandit (arXiv:2510.18633), Query Optimization Survey (arXiv:2412.17558); new Search as Planning section (LLM Search Survey TMLR 2025, Think-on-Graph 2.0 ICLR 2025, LLM-A*); new Personalized and Episodic Memory section (Episodic Memory Benchmark, Personalize Before Retrieve, Recollection-Familiarity); Temporal Reasoning expanded with Temporal Semantic Memory (arXiv:2601.07468); LLM as Search Heuristic expanded with Reranking Survey (arXiv:2512.16236), Multi-Turn Conversational RAG (arXiv:2602.09552)
- wiki/llm-grep-retrieval/concepts/experiments.md — added HeuristicRetriever pseudocode with category-aware expansion strategy; restructured plan to 7-condition experimental design; updated ceiling target to MemOS 42.79% (from A-MEM 35%); added SymbolicRetriever ablation table
- wiki/index.md — added symbolic-retriever row to Area 3 table; updated related-work and experiments summaries

Pages created:
- wiki/llm-grep-retrieval/concepts/symbolic-retriever.md — new direction identified April 7, 2026; full §16 content: core idea with JSON pseudocode, Mintlify ChromaFs inspiration, prior art table showing zero direct matches, symbolic vs embedding comparison per LoCoMo category, HeuristicRetriever vs SymbolicRetriever comparison table, NeurIPS framing with title candidate, open questions, next steps

Key synthesis: Two major updates from this sweep: (1) **Metric clarification** — the accuracy-based SOTA systems (ByteRover 96.1%, Hindsight 89.6%, mem0 66.9%) are not comparable to our micro F1 results; the real F1 ceiling is MemOS 42.79% (72B), not the accuracy numbers. (2) **New research direction** — SymbolicRetriever: LLM generates structured symbolic predicates (keywords + filters + boolean) executed on memory fields with zero embedding; no paper has done this on LoCoMo. The two directions (HeuristicRetriever for Cat 3/4, SymbolicRetriever for Cat 1/2) are complementary and route by category.

## [2026-04-08] update | ResearchTaste-Bench synthesis completed

Finished the interrupted research-taste synthesis pass and converted the multi-round design notes into wiki pages.

Pages created:
- wiki/research-taste/concepts/researchTaste-bench-design.md

Pages updated:
- wiki/research-taste/overview.md
- wiki/research-taste/concepts/research-taste.md
- wiki/research-taste/concepts/research-ability-dimensions.md
- wiki/research-taste/concepts/evaluation-approaches.md
- wiki/research-taste/comparisons/benchmark-landscape.md
- wiki/index.md

Previously created in the interrupted session and now integrated into the index / concept graph:
- wiki/research-taste/papers/salaudeen-2025-construct-validity.md
- wiki/research-taste/papers/chen-2025-irt-llm.md
- wiki/research-taste/papers/hindsight-novelty-bias.md
- wiki/research-taste/papers/gong-2025-economics-taste.md
- wiki/research-taste/papers/ke-2015-sleeping-beauty.md
- wiki/research-taste/papers/li-2026-preference-leakage.md
- wiki/research-taste/papers/saraf-2025-label-bias.md
- wiki/research-taste/papers/swe-bench-live.md
- wiki/research-taste/papers/ccv-contamination.md
- wiki/research-taste/papers/scientist-bench.md
- wiki/research-taste/papers/livemathematicianBench.md
- wiki/research-taste/papers/why-llms-arent-scientists.md

Key synthesis:
- The field is best framed as **Taste × Execution**, with ResearchTaste-Bench covering the upstream judgment axis.
- The proposed benchmark combines four ingredients that current work rarely combines in one place: objective downstream ground truth, contamination reporting, living updates, and construct validation.
- The main task is pairwise taste judgment on blinded abstracts; the main score is weighted toward underrated and sleeping-beauty cases rather than raw citation popularity.
- Diagnostic slices matter: novelty bias, timing sense, sleeping-beauty detection, and synthetic-idea testing expose different failure modes.
- The benchmark should explicitly acknowledge the benchmark-reality gap: it measures compressed judgment, not the full real-world decision of what to work on for six months.

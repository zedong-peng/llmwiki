---
title: Super Personal Wiki Log
domain: root
type: timeline
status: active
updated: 2026-04-24
tags: [log]
---

# Super Personal Wiki Log

## [2026-04-24] ingest | Added Memory for Autonomous LLM Agents survey note

- Added `wiki/research/misc/papers/memory-for-autonomous-llm-agents-2026/` from arXiv `2603.07670`.
- Recorded the paper as a processed agent-memory survey focused on the write-manage-read loop, memory taxonomy, mechanism families, benchmark landscape, and engineering checklist.
- Updated `wiki/research/misc/index.md` so the note is reachable from the Agent Memory Architectures section.

## [2026-04-21] metadata | Updated AutoBool venue to EACL 2026

- Revised `wiki/research/misc/papers/autobool-2026/index.md` to record AutoBool as published at `EACL 2026` rather than only an arXiv preprint.
- Updated `wiki/research/misc/index.md` so the Retrieval Optimization and Search Systems table now shows `EACL` as the venue.
- Added `venue: EACL 2026` and `publication_status: published` to `wiki/research/misc/papers/autobool-2026/metadata.yaml` while keeping the arXiv preprint link as the public artifact.

## [2026-04-10] bootstrap | Created super personal wiki skeleton

- Established root index, domain overview pages, source catalog, inbox, and raw source policy.
- Chose a domain model that can later absorb the existing research wiki without mixing research and administrative material.
- Set privacy rule: sensitive documents are indexed by metadata only unless the user explicitly requests otherwise.

## [2026-04-14] migration | Imported research-map-wiki into wiki/research

- Copied the existing research areas into `wiki/research/`: `research-taste`, `claude-code-memory`, and `llm-grep-retrieval`.
- Preserved the original area structure, paper notes, concept pages, comparisons, PDFs, and chronological research log.
- Added `wiki/research/index.md` as the research-domain master index inside the super personal wiki.
- Updated the root index so research pages are reachable from the top-level wiki.
- Fixed one migrated cross-area link in `llm-grep-retrieval/concepts/symbolic-retriever.md`.

## [2026-04-18] reorg | Rebuilt paper intake under `wiki/research/misc`

- Added `wiki/research/misc/overview.md` and `wiki/research/misc/paper-registry.md` as the new normalized entry point for unclassified papers.
- Merged old standalone paper notes from `agent-memory` and `llm-grep-retrieval` into a single registry with canonical slugs and ingest status.
- Created `seed` protocol stubs under `wiki/research/misc/papers/<slug>/` for previously standalone paper pages.
- Recorded mention-only papers and industrial systems from `llm-grep-retrieval` as `name-only` entries without copying unverified summaries.
- Updated root and research overview pages so the new misc paper library is reachable from the main wiki navigation.

## [2026-04-18] index | Generated `misc/papers` directory index

- Added `wiki/research/misc/papers/index.md` as the catalog for all current paper directories under `wiki/research/misc/papers/`.
- Restored `wiki/research/misc/overview.md` and `wiki/research/misc/paper-registry.md` so existing navigation links resolve again.
- Summarized current ingest coverage: 46 directories total, 45 with `index.md`, 45 with `metadata.yaml`, 42 TeX-first entries, 2 PDF fallback entries, and 1 placeholder directory needing cleanup.

## [2026-04-18] repair | Extracted cached arXiv sources under `misc/papers`

- Identified that 42 papers marked `tex_available: true` only had raw source blobs in `source/` and had not been unpacked.
- Added `scripts/fix_paper_sources.py` to normalize cached source files into `source/archives/` and `source/extracted/`.
- Repaired all 42 TeX-backed papers locally without re-downloading; metadata now records `source_archive_path`, `source_extracted_path`, and `source_extracted: true`.
- Verified `agemem-2026` specifically: its `2601.01885-source` file is a valid gzip-compressed tarball containing `acl_latex.tex`, section files, figures, and `custom.bib`.

## [2026-04-19] simplify | Collapsed `misc` navigation into one page

- Added `wiki/research/misc/index.md` as the single entry page for the misc paper library.
- Removed `wiki/research/misc/overview.md`, `wiki/research/misc/paper-registry.md`, and `wiki/research/misc/papers/index.md` because they duplicated navigation without adding durable content.
- Updated root and research indexes to point to `[[research/misc/index]]` / `[[misc/index]]`.

## [2026-04-19] ingest | Added CursorBench note under `misc/papers`

- Added `wiki/research/misc/papers/cursorbench-2026/index.md` from the official Cursor research blog post `How We Compare Model Quality in Cursor`.
- Recorded CursorBench as an internal coding-agent benchmark note, emphasizing real-session task sourcing, agentic grading, and the online-offline evaluation loop.
- Updated `wiki/research/misc/index.md` to include the new paper entry and refreshed the library counts.

## [2026-04-19] prune | Removed low-value fallback entries from `misc/papers`

- Deleted `wiki/research/misc/papers/flare-2023/` and `wiki/research/misc/papers/llm-a-star-2024/` with all local files.
- Removed the stale `flarerag-placeholder` mention from `wiki/research/misc/index.md`.
- Refreshed the misc paper library counts and directory links so the index matches the remaining 44 paper entries.

## [2026-04-19] ingest | Added Claude Code source and In-Place TTT notes

- Added `wiki/research/misc/papers/claude-code-lead-source-2026/index.md` and `metadata.yaml` to normalize the previously unindexed local Claude Code source collection into a durable engineering note.
- Added `wiki/research/misc/papers/in-place-ttt-2026/`, downloaded the arXiv source for `2604.06169`, extracted it under `source/extracted/`, and wrote a TeX-first note from the main TeX sections.
- Connected both notes to existing context: Claude Code versus explicit persistent memory, In-Place TTT versus implicit fast-weight adaptation, and CursorBench versus the still-open evaluation gap for long-running coding agents.
- Refreshed `wiki/research/misc/index.md` and `wiki/research/claude-code-memory/overview.md` so the new pages are reachable from existing navigation.

## [2026-04-19] nav | Clarified `research/` entry-point roles

- Kept `wiki/research/overview.md` as the single recommended entry page for human browsing.
- Reframed `wiki/research/index.md` as a secondary detailed index that preserves the old research-map structure.
- Updated `wiki/index.md` so root navigation explicitly tells readers to open `[[research/overview]]` first.

## [2026-04-19] ingest | Added BRIGHT, CORAL, and RAGChecker under `misc/papers`

- Added `wiki/research/misc/papers/bright-2025/` from arXiv source `2407.12883`, the official BRIGHT repo, and the PDF; wrote a processed note focused on reasoning-intensive retrieval and the benchmark's reasoning-query setup.
- Added `wiki/research/misc/papers/coral-2024/` from arXiv source `2410.23090`, the official CORAL repo, and the PDF; summarized the dataset construction pipeline, retrieval baselines, and generation/citation tasks.
- Added `wiki/research/misc/papers/ragchecker-2024/` from arXiv source `2408.08067`, the official RAGChecker repo, and the PDF; recorded its diagnostic metric taxonomy, benchmark curation, and average system-level results.
- Updated `wiki/research/misc/index.md` to include the three new entries and refreshed the library snapshot counts.

## [2026-04-19] threads | Added `misc/threads` for durable session records

- Added `wiki/research/misc/threads/index.md` as the entry page for conversation-driven research threads that should be preserved separately from formal paper notes.
- Added `wiki/research/misc/threads/2026-04-19-compiled-lexical-retrieval-and-rag-benchmarks.md` to summarize the current discussion around `grepqa`, BM25 vs grep, CoT reasoning queries, dense retrieval, and benchmark choices such as BRIGHT / CORAL / RAGChecker.
- Updated `wiki/research/misc/index.md` so the Thread Directory now links to the new session-record area.

## [2026-04-19] docs | Restored a `papers/` structure guide under `misc`

- Added `wiki/research/misc/papers/index.md` to explain the `papers/` directory layout, ingest priority, per-paper file structure, and status semantics.
- Updated `wiki/research/misc/index.md` so the Paper Directory now links to the new structure guide before the categorized paper lists.

## [2026-04-19] ingest | Added `claude-mem` GitHub repo note under `misc`

- Reworked `wiki/research/misc/papers/claude-mem-2026/` to track the public repo `thedotmack/claude-mem` rather than Claude Code's built-in memory subsystem.
- Recorded the repo as an external persistent-memory plugin stack: lifecycle hooks, worker service on port `37777`, SQLite storage, Chroma-backed retrieval, MCP search tools, and `<private>` tag stripping.
- Updated `wiki/research/misc/index.md` library counts and clarified the backlink from `wiki/research/claude-code-memory/overview.md` so the built-in system and the external plugin are no longer conflated.

## [2026-04-19] thread | Added Cursor blog reading notes

- Added `wiki/research/misc/threads/2026-04-19-cursor-blog-reading-notes.md` to summarize why Cursor's recent blog archive feels unusually coherent and high-signal.
- Organized the notes around recurring stack bottlenecks: evals, long-horizon training, lexical search, cloud runtime, and agent-first interface design.
- Updated `wiki/research/misc/threads/index.md` and `wiki/research/misc/index.md` so the new thread is reachable from existing misc navigation.

## [2026-04-19] ingest | Added BEIR benchmark note under `misc/papers`

- Added `wiki/research/misc/papers/beir-2021/`, downloaded the arXiv source for `2104.08663`, extracted `neurips2021.tex` under `source/extracted/`, and stored the paper PDF.
- Cloned the current official BEIR codebase under `repo/beir/`; recorded the lineage from the paper-linked `UKPLab/beir` repo to the maintained `beir-cellar/beir` repository.
- Wrote a TeX-first note focused on benchmark design, the zero-shot retrieval findings, lexical annotation bias, and the software interfaces around `GenericDataLoader`, `EvaluateRetrieval`, BM25, and dense retrieval.
- Updated `wiki/research/misc/index.md` so the new note is reachable from the Retrieval Optimization and Search Systems section and refreshed the library snapshot counts.

## [2026-04-19] thread | Added BEIR current-SOTA snapshot

- Added `wiki/research/misc/threads/2026-04-19-beir-current-sota-snapshot.md` to distinguish the official public EvalAI BEIR leaderboard from newer model-card-reported BEIR scores.
- Queried the official EvalAI API directly and recorded the current public leaderboard leader as `nle / (BM25+SPLADE) RANKT5 top 50` with `0.5525` average nDCG@10, while also noting the challenge is currently inactive and frozen.
- Added the newer comparison evidence from MongoDB's `mdbr-leaf-ir` model card, which lists `text-embedding-3-large` at `55.43` and `mdbr-leaf-ir (asym.)` at `54.03`, so future discussions do not conflate official public submissions with recent reported model-card results.
- Updated `wiki/research/misc/threads/index.md` and `wiki/research/misc/index.md` so the snapshot is reachable from existing misc navigation.

## [2026-04-19] thread | Added BEIR related-paper search note

- Added `wiki/research/misc/threads/2026-04-19-beir-related-paper-search.md` as a short literature-search note for papers that are most directly relevant to BEIR.
- Grouped the results by role: the original benchmark paper, LLM-based synthetic-data methods such as InPars / InPars-v2, embedding work such as E5 and Microsoft's 2024 text-embedding paper, and key sparse / reranking components such as SPLADE and RankT5.
- Updated `wiki/research/misc/threads/index.md` and `wiki/research/misc/index.md` so the note is reachable from the misc research entry point.

## [2026-04-19] thread | Refined BEIR paper search using BRIGHT related work

- Re-read `wiki/research/misc/papers/bright-2025/source/extracted/texts/related_works.tex` and the appendix section comparing BRIGHT to RAR-b.
- Updated `wiki/research/misc/threads/2026-04-19-beir-related-paper-search.md` to distinguish the BEIR line from adjacent benchmark lines: BIRCO for complex objectives, RAR-b for reasoning-as-retrieval, FollowIR / INSTRUCTIR / TART for instruction-following retrieval, and LoCo / LongEmbed for long-context retrieval.
- Recorded the judgment that, from BRIGHT's own framing, these benchmark-extension papers are a better next reading set than simply adding more embedding-model papers.

## [2026-04-19] ingest | Added important BEIR-adjacent papers: InPars, InPars-v2, and TART

- Added `wiki/research/misc/papers/inpars-2022/` from arXiv source `2202.05144`, the official `zetaalphavector/InPars` repo, and the PDF; wrote a TeX-first note covering synthetic query generation, score-based filtering, BM25 negative mining, and the monoT5 reranking pipeline.
- Added `wiki/research/misc/papers/inpars-v2-2023/` from arXiv source `2301.01820`, the official `zetaalphavector/InPars` repo, and the PDF; summarized the GPT-J generator swap, reranker-based filtering, and the paper's BEIR SOTA claim.
- Added `wiki/research/misc/papers/tart-2023/` from arXiv source `2211.09260`, the official `facebookresearch/tart` repo, and the PDF; summarized BERRI, retrieval with instructions, BEIR / LOTTE zero-shot results, and the cross-task cross-domain evaluation setup.
- Updated `wiki/research/misc/index.md` so the three notes are reachable from the Retrieval Optimization and Search Systems section and refreshed the library snapshot counts.

## [2026-04-19] ingest | Added OpenAI Memory product note

- Added `wiki/research/misc/papers/openai-memory-2024/` as a source note rather than a paper note because the canonical sources are OpenAI's product blog and Help Center, not arXiv or TeX.
- Recorded the product timeline from the official OpenAI blog: public launch in February 2024, wider rollout in September 2024, a more comprehensive memory model in April 2025, and free-user memory improvements in June 2025.
- Updated `wiki/research/misc/index.md` with a dedicated `Product Memory Notes` subsection so the note is reachable from the misc entry point.

## [2026-04-21] ingest | Imported core linear-attention hardware papers under `misc/papers`

- Added `wiki/research/misc/papers/pimba-2025/`, `plena-2025/`, `flexla-forge-2025/`, `tiled-flash-linear-attn-2025/`, and `danmp-2026/` using the same per-paper directory layout as the rest of `misc/papers`.
- Downloaded local PDFs plus arXiv source archives for Pimba (`2507.10178`), PLENA (`2509.09505`), Tiled Flash Linear Attention (`2503.14376`), and DANMP (`2603.00959`), then extracted each source tree under `source/extracted/`.
- Cloned the official `NX-AI/mlstm_kernels` repository into `wiki/research/misc/papers/tiled-flash-linear-attn-2025/repo/` because the repo README directly maps it to the TFLA paper.
- Recorded FlexLA/Forge as a stable seed directory, but OpenReview blocked automated PDF download with HTTP 403 and no public arXiv source or official repo was found during this pass.
- Updated `wiki/research/misc/index.md` so the new hardware-focused paper set is reachable from the misc library entry page and refreshed the snapshot counts.

## [2026-04-21] thread | Summarized linear-attention baseline planning from unfinished transcript

- Added `wiki/research/misc/threads/2026-04-21-linear-attn-baselines-and-adoption.md` from the durable planning content in `2026-04-21-022157-linear-attention-gpu.txt`.
- Captured the transcript’s three-layer “golden baseline” framing: naive PyTorch for correctness, FLA for main performance comparison, and Forge/FlexLA as the upper-bound reference.
- Preserved the transcript’s working judgment that hybrid linear-attention models are already a real deployment pattern, while explicitly marking the model-adoption list as transcript-derived and pending official-source verification.
- Recorded the paper priority queue around FLA, GLA, Mamba-2, FlashAttention, and the already imported hardware/compiler papers so future ingest work has a stable checklist.

## [2026-04-21] index | Expanded misc linear-attention reading queue

- Updated `wiki/research/misc/index.md` with a tiered linear-attention bibliography spanning core method papers, kernel/compiler baselines, hardware papers, and production-adoption references.
- Marked current wiki state inline as `processed`, `seed`, `brief mention only`, or `not ingested` so the download queue now matches the actual repository state.
- Linked the queue back to `wiki/research/misc/threads/2026-04-21-linear-attn-baselines-and-adoption.md` and the existing `wiki/research/linear-attn/` area so future ingest work has one stable entry point.

## [2026-04-26] update | Enriched Honcho entry in agent-memory index

- Updated `wiki/research/agent-memory/index.md` so the Honcho product-memory row points at the existing processed note and summarizes its actual API-centered memory surface: peers, sessions, context, search, and representations.

## [2026-04-21] ingest | Downloaded first-pass linear-attention core bibliography under `misc/papers`

- Added seed entries plus `metadata.yaml` for `transformers-are-rnns-2020`, `retnet-2023`, `gla-2024`, `mamba-2023`, `mamba-2-2024`, `deltanet-2024`, `gated-deltanet-2025`, `griffin-2024`, `recurrentgemma-2024`, `jamba-2024`, `linear-attn-gpu-kernel-2025`, and the repo-first `fla-2024`.
- Downloaded local arXiv PDFs and source archives for the 11 arXiv-backed entries, and extracted each source tree under `source/extracted/`.
- Cloned the key public repos that anchor this thread: `idiap/fast-transformers`, `microsoft/torchscale`, `state-spaces/mamba`, `NVlabs/GatedDeltaNet`, `google-deepmind/recurrentgemma`, and `fla-org/flash-linear-attention`.
- Updated `wiki/research/misc/index.md` so the new paper directories are linked from the linear-attention section and refreshed the library snapshot counts from 70 to 82 directories.

## [2026-04-21] cleanup | Reframed misc linear-attention index and attached local FlexLA PDF

- Removed the ad hoc `Linear Attention Reading Queue` subsection from `wiki/research/misc/index.md`; the misc index now keeps only a compact paper table rather than thread-planning content.
- Expanded the linear-attention section from a bare link list into a normalized table with paper link, year, venue, importance, and wiki status.
- Copied the user-downloaded FlexLinearAttention PDF into `wiki/research/misc/papers/flexla-forge-2025/` and updated that entry from “blocked PDF fetch” to “local PDF available”.

## [2026-04-26] synth | Re-scored EverMemOS saved LoCoMo outputs

- Updated `wiki/research/agent-memory/threads/2026-04-25-benchmark-comparison-thread.md` with an inspection of `EverMemOS_Eval_Results`.
- Confirmed the saved answer files are enough for offline GrepQA-style F1/BLEU-1 post-processing, while saved judge files should be reported as EverMemOS-native LLM judge accuracy.
- Recorded that EverMemOS and GrepQA use effectively the same generous LoCoMo judge prompt, with only minor output-format and system-prompt differences.
- Added the post-hoc metric table showing that verbose native answers can have high LLM-judge accuracy but low token F1/BLEU-1, so these numbers should not replace a unified-answerer comparison.

## [2026-04-21] ingest | Parallelized processed notes for linear-attention bibliography

- Spawned one worker per non-processed linear-attention entry and upgraded the corresponding `index.md` files in parallel.
- Promoted these entries from `seed` to `processed`: `transformers-are-rnns-2020`, `retnet-2023`, `gla-2024`, `mamba-2023`, `mamba-2-2024`, `deltanet-2024`, `gated-deltanet-2025`, `griffin-2024`, `recurrentgemma-2024`, `jamba-2024`, `fla-2024`, `linear-attn-gpu-kernel-2025`, `flexla-forge-2025`, `tiled-flash-linear-attn-2025`, and `danmp-2026`.
- Kept `pimba-2025` and `plena-2025` unchanged because they were not assigned in this worker pass.
- Updated `wiki/research/misc/index.md` so the linear-attention table now reflects the actual per-paper page statuses after the parallel ingest.

## [2026-04-21] synth | Tightened linear-attention systems framing

- Extended `wiki/research/misc/threads/2026-04-21-linear-attn-baselines-and-adoption.md` with a stronger systems framing for future paper planning.
- Recorded a concrete recommendation to prioritize `GLA` before `Mamba-2` when only one target architecture can be carried in a first compiler/runtime paper.
- Added a minimal experiment matrix spanning correctness, `torch.compile`, `FLA`, and `FlexLA` / hand-tuned upper bounds, plus explicit warning against the “pure linear attention replaces softmax everywhere” thesis.

## [2026-04-21] thread | Added a minimal validation plan for the “linear attention is bad on GPU” claim

- Added `wiki/research/misc/threads/2026-04-21-validating-linear-attn-gpu-bottleneck.md` to turn the vague GPU-bottleneck intuition into a concrete, falsifiable systems hypothesis.
- Recorded a 4090-friendly first-pass benchmark plan centered on three experiments: latency sweep, peak-memory / OOM sweep, and minimal profiling.
- Linked the plan to the existing `FLA`, `GLA`, `Mamba-2`, `TFLA`, and `FlexLA` notes so future work can move from “intuition” to “measured evidence”.

## [2026-04-19] ingest | Added FollowIR, BIRCO, RAR-b, Hindsight, Honcho, and Memobase under `misc/papers`

- Added `wiki/research/misc/papers/followir-2025/` from arXiv source `2403.15246`, the official `orionw/FollowIR` repo, and the PDF; wrote a TeX-first note focused on TREC-narrative instruction following, the `p-MRR` metric, and the gap between generic instruction tuning and instruction-sensitive retrieval.
- Added `wiki/research/misc/papers/birco-2024/` from arXiv source `2402.14151`, the official `BIRCO-benchmark/BIRCO_dataset` repo, and the PDF; summarized the five complex-objective retrieval tasks, low-overlap long-query setting, and the drop from BEIR scores to BIRCO scores for models such as E5, RankLLaMA, and TART.
- Added `wiki/research/misc/papers/rar-b-2024/` from arXiv source `2404.06347`, the official `gowitheflow-1998/RAR-b` repo, and the PDF; recorded the benchmark's multiple-choice and full-retrieval settings, the "instructions can hurt retrievers" finding, and the dominance of fine-tuned rerankers.
- Added `wiki/research/misc/papers/hindsight-2025/` from arXiv source `2512.12818`, the official `vectorize-io/hindsight` repo, and the PDF; summarized the retain-recall-reflect architecture, the hybrid retrieval stack, and the strong LongMemEval / LoCoMo results.
- Added `wiki/research/misc/papers/honcho-2025/` and `wiki/research/misc/papers/memobase-2025/` as source notes rather than paper notes because the canonical sources are product repos and docs, not formal publications.
- Refreshed `wiki/research/misc/index.md` so the new retrieval and memory-system entries are reachable from the misc entry point and updated the library snapshot counts to match the current 61-paper directory state.

## [2026-04-21] update | Clarified BEIR's 2026 relation to MTEB

- Updated `wiki/research/misc/papers/beir-2021/index.md` to distinguish the original 2021 BEIR paper from its later 2026 ecosystem role.
- Recorded the durable judgment that BEIR remains the canonical 18-dataset zero-shot retrieval benchmark, but current embedding comparisons increasingly consume it through MTEB's retrieval slice.
- Updated `wiki/research/misc/threads/2026-04-19-beir-current-sota-snapshot.md` so future leaderboard discussions separate three notions: official EvalAI BEIR, newer reported BEIR averages, and the broader MTEB retrieval framing.
- Promoted the AILog BEIR update page to an explicit important later source on the BEIR paper page, because it cleanly states the transition from standalone BEIR discussion to MTEB retrieval-subset framing.
## [2026-04-24] cleanup | Split linear-attention material out of misc

- Created `wiki/research/linear-attention/` as a dedicated area for linear attention, recurrent sequence models, kernels, compiler baselines, and hardware co-design.
- Moved the linear-attention paper set from `wiki/research/misc/papers/` into `wiki/research/linear-attention/papers/`, preserving each paper directory's PDFs, source trees, metadata, and repos.
- Moved the two linear-attention research threads and their local benchmark figures into `wiki/research/linear-attention/threads/`.
- Updated root and research indexes so the new area is reachable, and removed the migrated entries from `misc` navigation.

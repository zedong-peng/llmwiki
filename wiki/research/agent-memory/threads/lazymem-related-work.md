---
title: "LazyMem Related-Work Corpus"
domain: research
area: agent-memory
type: synthesis
status: stable
updated: 2026-07-27
tags: [agent-memory, lazymem, related-work, corpus, novelty-audit, bm25, raw-retrieval]
---

## Corpus Provenance Record

- This is an existing research synthesis and frozen corpus directory. Its generic historical metadata says `not_started`; that does not invalidate the preserved audit work or establish reading of each individual paper. Per-paper stubs remain explicitly unread unless their own evidence records reading.
- Source provenance: [citation.bib](../assets/lazymem-related-work/citation.bib); the complete historical metadata is retained there.

# LazyMem Related-Work Corpus

Frozen literature corpus (assembled 2026-07-27) for evaluating the scientific position of LazyMem: 45 official arXiv PDFs covering long-term conversational memory, raw-history retrieval, lexical/dense retrieval, query transformation, adaptive retrieval, evidence sufficiency, and evaluation methodology.

> This directory is intentionally a frozen artifact — do not rename or modify files under `pdfs/`, `text/`, or `SHA256SUMS`. The legacy `papers/<slug>/` stub summaries now live under `threads/unread-<slug>.md` (linked below); read notes remain under `assets/<slug>/note.md`.

## Key Conclusions (from RELATED_WORK.md)

- The literature supports LazyMem's design pressure (preserve raw record, spend semantic computation lazily) but **not the current mechanism as a contribution**.
- The LLM query compiler loses to the repo's own BM25-window control on LoCoMo dev: F1 0.5019 vs 0.5526, judge acc 0.7422 vs 0.7864, 2,320 vs 1,974 tokens/question — a rejected ablation.
- ResearchStudio scoop audit verdict: **Level 1 full overlap** for the broad "BM25 first, semantic only when useful" claim (AgentIR).
- Surviving hypothesis: directly predict cost-adjusted intervention value for one fixed semantic operation, transferring across corpora — not yet cleared as novel (TARG blocks reader-uncertainty gating).

## Contents

- [RELATED_WORK.md](../assets/lazymem-related-work/RELATED_WORK.md) — 561-line synthesis: novelty audit, baseline ladder (B0-B10), metrics, kill criteria, recommended experimental program.
- [README.md](../assets/lazymem-related-work/README.md) — corpus provenance, selection rule, validation, and revalidation commands.
- [selection.tsv](../assets/lazymem-related-work/selection.tsv) — 45-paper inclusion ledger (category, arXiv id, title, rationale).
- [arxiv_metadata.xml](../assets/lazymem-related-work/arxiv_metadata.xml) — raw arXiv API metadata.
- `pdfs/` / `text/` — 45 official PDFs and `pdftotext -layout` extractions.
- [SHA256SUMS](../assets/lazymem-related-work/SHA256SUMS) — frozen-byte checksums.
- `researchstudio-rerun/` — independent Microsoft ResearchStudio rerun (paper-search, scoop-check, idea-spark), incl. S2G-RAG/TARG artifacts and the falsification plan in `step7.md`.
- `researchstudio-rerun/utility-gate-search/` — narrow follow-up on answer utility, cost-aware retrieval, and learning-to-defer.

## Corpus Papers → Wiki Pages

### Benchmarks and evaluation
- [LoCoMo](../assets/locomo-2024/note.md) · [LongMemEval](../assets/longmemeval-2025/note.md) — pre-existing pages
- [MemTrace](unread-memtrace-2026.md) · [MemOps](unread-memops-2026.md) · [RUMBA](unread-rumba-2026.md) · [Beyond Memory Leaderboards](unread-budgeted-context-restoration-2026.md) · [MEMAUDIT](unread-memaudit-2026.md)

### Memory architectures
- [MemGPT](../assets/memgpt-letta-2023/note.md) · [Mem0](../assets/mem0-2025/note.md) · [A-MEM](../assets/amem-2025/note.md) · [Zep](../assets/zep-2025/note.md) · [EverMemOS](../assets/evermemos-2026/note.md) · [Hindsight](../assets/hindsight-2025/note.md) — pre-existing pages
- [ENGRAM](unread-engram-2025.md) · [HingeMem](unread-hingemem-2026.md) · [PRISM (Pareto-Efficient)](unread-prism-memory-2026.md) · [GRAVITY](unread-gravity-2026.md)

### Raw-history and conversational retrieval
- [SmartSearch](unread-smartsearch-2026.md) · [AgentIR](unread-agentir-2026.md) · [Lexical-Dense Fusion](unread-lexical-dense-fusion-2026.md) · [Back to Basics](unread-back-to-basics-2026.md) · [SelRoute](unread-selroute-2026.md) · [EviMem](unread-evimem-2026.md) · [TierMem](unread-tiermem-2026.md) · [Fidelity Before Structure](unread-fidelity-before-structure-2026.md) · [Event-Memory Baseline](unread-event-memory-baseline-2025.md) · [DeferMem](unread-defermem-2026.md) · [MGRetrieval](unread-mgretrieval-2026.md) · [Eywa](unread-eywa-2026.md) · [ConvMemory](unread-convmemory-2026.md) · [EAR](unread-ear-2026.md) · [Training-Free Control](unread-training-free-control-2026.md) · [Recursive Language Models](unread-recursive-language-models-2025.md)
- [Memory-T1](../assets/memory-t1-2025/note.md) · [Recollection-Familiarity](../assets/recollection-familiarity-retrieval-2026/note.md) — pre-existing pages

### IR foundations
- [DPR](unread-dpr-2020.md) · [ColBERT](unread-colbert-2020.md) · [SPLADE v2](unread-splade-v2-2021.md) · [BEIR](../../misc/assets/beir-2021/note.md)

### Query transformation
- [Query2doc](unread-query2doc-2023.md)
- [HyDE](unread-hyde-2023.md) · RAG-Fusion（原归档已移除） — pre-existing pages

### Adaptive retrieval
- [FLARE](unread-flare-2023.md)
- [Self-RAG](../../misc/assets/self-rag-2024/note.md) · [IRCoT](unread-irco-2023.md) — pre-existing pages

## Notes

- The ResearchStudio rerun artifacts (S2G-RAG, TARG, PGR) are audit evidence, not members of `selection.tsv`; PGR remains abstract-only (official PDF endpoint returned HTTP 403).
- Corpus PRISM (2605.12260, Pareto-Efficient Retrieval) is a different paper from the existing [prism-2025](../../misc/assets/prism-2025/note.md) (2510.14278, Precision-Recall Iterative Selection).

---
title: "LazyMem Related-Work Corpus"
domain: research
area: agent-memory
type: synthesis
status: stable
updated: 2026-07-27
tags: [agent-memory, lazymem, related-work, corpus, novelty-audit, bm25, raw-retrieval]
---

# LazyMem Related-Work Corpus

Frozen literature corpus (assembled 2026-07-27) for evaluating the scientific position of LazyMem: 45 official arXiv PDFs covering long-term conversational memory, raw-history retrieval, lexical/dense retrieval, query transformation, adaptive retrieval, evidence sufficiency, and evaluation methodology.

> This directory is intentionally a frozen artifact — do not rename or modify files under `pdfs/`, `text/`, or `SHA256SUMS`. Per-paper wiki notes live as standard stub pages under `papers/<slug>/` (linked below).

## Key Conclusions (from RELATED_WORK.md)

- The literature supports LazyMem's design pressure (preserve raw record, spend semantic computation lazily) but **not the current mechanism as a contribution**.
- The LLM query compiler loses to the repo's own BM25-window control on LoCoMo dev: F1 0.5019 vs 0.5526, judge acc 0.7422 vs 0.7864, 2,320 vs 1,974 tokens/question — a rejected ablation.
- ResearchStudio scoop audit verdict: **Level 1 full overlap** for the broad "BM25 first, semantic only when useful" claim (AgentIR).
- Surviving hypothesis: directly predict cost-adjusted intervention value for one fixed semantic operation, transferring across corpora — not yet cleared as novel (TARG blocks reader-uncertainty gating).

## Contents

- [RELATED_WORK.md](RELATED_WORK.md) — 561-line synthesis: novelty audit, baseline ladder (B0-B10), metrics, kill criteria, recommended experimental program.
- [README.md](README.md) — corpus provenance, selection rule, validation, and revalidation commands.
- [selection.tsv](selection.tsv) — 45-paper inclusion ledger (category, arXiv id, title, rationale).
- [arxiv_metadata.xml](arxiv_metadata.xml) — raw arXiv API metadata.
- `pdfs/` / `text/` — 45 official PDFs and `pdftotext -layout` extractions.
- [SHA256SUMS](SHA256SUMS) — frozen-byte checksums.
- `researchstudio-rerun/` — independent Microsoft ResearchStudio rerun (paper-search, scoop-check, idea-spark), incl. S2G-RAG/TARG artifacts and the falsification plan in `step7.md`.
- `researchstudio-rerun/utility-gate-search/` — narrow follow-up on answer utility, cost-aware retrieval, and learning-to-defer.

## Corpus Papers → Wiki Pages

### Benchmarks and evaluation
- [LoCoMo](../locomo-2024/index.md) · [LongMemEval](../longmemeval-2025/index.md) — pre-existing pages
- [MemTrace](../memtrace-2026/index.md) · [MemOps](../memops-2026/index.md) · [RUMBA](../rumba-2026/index.md) · [Beyond Memory Leaderboards](../budgeted-context-restoration-2026/index.md) · [MEMAUDIT](../memaudit-2026/index.md)

### Memory architectures
- [MemGPT](../memgpt-letta-2023/index.md) · [Mem0](../mem0-2025/index.md) · [A-MEM](../amem-2025/index.md) · [Zep](../zep-2025/index.md) · [EverMemOS](../evermemos-2026/index.md) · [Hindsight](../hindsight-2025/index.md) — pre-existing pages
- [ENGRAM](../engram-2025/index.md) · [HingeMem](../hingemem-2026/index.md) · [PRISM (Pareto-Efficient)](../prism-memory-2026/index.md) · [GRAVITY](../gravity-2026/index.md)

### Raw-history and conversational retrieval
- [SmartSearch](../smartsearch-2026/index.md) · [AgentIR](../agentir-2026/index.md) · [Lexical-Dense Fusion](../lexical-dense-fusion-2026/index.md) · [Back to Basics](../back-to-basics-2026/index.md) · [SelRoute](../selroute-2026/index.md) · [EviMem](../evimem-2026/index.md) · [TierMem](../tiermem-2026/index.md) · [Fidelity Before Structure](../fidelity-before-structure-2026/index.md) · [Event-Memory Baseline](../event-memory-baseline-2025/index.md) · [DeferMem](../defermem-2026/index.md) · [MGRetrieval](../mgretrieval-2026/index.md) · [Eywa](../eywa-2026/index.md) · [ConvMemory](../convmemory-2026/index.md) · [EAR](../ear-2026/index.md) · [Training-Free Control](../training-free-control-2026/index.md) · [Recursive Language Models](../recursive-language-models-2025/index.md)
- [Memory-T1](../memory-t1-2025/index.md) · [Recollection-Familiarity](../recollection-familiarity-retrieval-2026/index.md) — pre-existing pages

### IR foundations
- [DPR](../dpr-2020/index.md) · [ColBERT](../colbert-2020/index.md) · [SPLADE v2](../splade-v2-2021/index.md) · [BEIR](../beir-2021/index.md)

### Query transformation
- [Query2doc](../query2doc-2023/index.md)
- [HyDE](../hyde-2023/index.md) · [RAG-Fusion](../rag-fusion-2023/index.md) — pre-existing pages

### Adaptive retrieval
- [FLARE](../flare-2023/index.md)
- [Self-RAG](../self-rag-2024/index.md) · [IRCoT](../irco-2023/index.md) — pre-existing pages

## Notes

- The ResearchStudio rerun artifacts (S2G-RAG, TARG, PGR) are audit evidence, not members of `selection.tsv`; PGR remains abstract-only (official PDF endpoint returned HTTP 403).
- Corpus PRISM (2605.12260, Pareto-Efficient Retrieval) is a different paper from the existing [prism-2025](../prism-2025/index.md) (2510.14278, Precision-Recall Iterative Selection).

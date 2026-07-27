# Step 7 - Delta and Falsification Boundary

Timestamp: 2026-07-27

## Provisional delta

Unlike Tian, Ganguly, and Macdonald (ECIR 2026), which define retrieval utility as the contextual performance gain over no-context generation and predict it with linear predictors on NQ, the proposed work would turn that paired gain into a calibrated, cost-adjusted one-sided deployment certificate for one fixed semantic memory intervention and test whether the resulting gate transfers to held-out conversational-memory data, yielding an answer-quality/cost frontier rather than another relevance or reader-uncertainty heuristic.

## What must be demonstrated before claiming the delta

- The gate must beat AgentIR-style BM25-margin, TARG-style prefix uncertainty, SelRoute-style query-type, random matched-rate, always-semantic, and never-semantic controls under identical reader/context/call/token/latency budgets.
- The utility certificate must be calibrated on a development corpus and evaluated frozen on LongMemEval-S; no distribution-free OOD guarantee may be claimed.
- The gain must be downstream answer utility, not only evidence recall or retrieval rank, and must include harmful-escalation rate, oracle regret, and paired confidence intervals.
- The ICTIR 2025 utility-maximization paper must be obtained and compared at method level. If it already performs cost-aware utility routing, the candidate should be abandoned or reframed as an empirical transfer study.

## Verdict consequence

This is a decision memo, not a paper novelty claim. The current candidate is worth one controlled implementation only if the user accepts a high-overlap, falsification-first project. The broad claim “BM25 first and semantic retrieval only when useful” is already occupied and must not be used as the contribution.

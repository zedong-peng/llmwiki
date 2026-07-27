# Step 1 - Decompose the Novelty

Timestamp: 2026-07-27 (Asia/Shanghai)

## Research problem

Restore sufficient evidence from a long, raw, multi-session dialogue under a fixed reader-context budget and explicit query-time call/token costs. A strong BM25-window retriever is the minimum lexical control, and LoCoMo is development-only rather than held-out evidence.

## Claimed novelty under audit

Use BM25-window as the default path, invoke an additional semantic retrieval operation only when a cheap-path evidence signal predicts that the intervention has positive marginal answer utility, and preserve a per-query trace of route, evidence, cost, and paired outcome.

## Four atomic axes

- **Problem framing:** Budgeted conversational-memory context restoration from an authoritative raw transcript, evaluated end to end with a frozen answer reader, frozen context budget, per-query costs, and held-out transfer.
- **Core mechanism:** A lexical-first cascade: BM25-window always runs; a cheap evidence/score signal gates one predeclared semantic fallback; the final context is packed under the same token cap, and cheap-only versus fallback intervention outcomes are logged pairwise.
- **Key insight:** Semantic retrieval has heterogeneous conditional value. It should be purchased only on queries where it repairs a lexical evidence gap, rather than being run unconditionally or justified by retrieval metrics alone.
- **Application domain:** Long-term conversational memory and multi-session question answering, primarily LoCoMo for development diagnosis and LongMemEval or another untouched suite for transfer.

## Audit interpretation

This is intentionally stronger than the current typed predicate compiler. The compiler itself is already a negative ablation against BM25-window. The audit asks whether the replacement principle and mechanism remain novel after considering adaptive IR, query-type routing, sufficiency loops, tiered raw escalation, and matched-budget evaluation.

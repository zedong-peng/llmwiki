# Step 6 - Four-Axis Novelty Comparison

Timestamp: 2026-07-27 (Asia/Shanghai)

## Proposed work under audit

> Start from BM25-window over raw multi-session dialogue, then invoke semantic computation only when a cheap evidence signal predicts that the extra operation will improve answer quality enough to justify its context, token, latency, and call cost. Record route, evidence, cost, and paired answer outcome.

This is the broad research statement inferred from the current LazyMem redesign discussion. It is not yet a validated implementation.

## Comparison matrix

Legend: **M** = material match, **P** = partial match, **D** = materially different, **?** = unavailable evidence.

| Work | Problem framing | Core mechanism | Key insight | Domain | Assessment |
|---|---:|---:|---:|---:|---|
| Proposed LazyMem | M | M | M | M | Audited target |
| AgentIR | M | M | M | M | Direct: BM25-margin early exit, dense+fusion escalation, answer-preserving threshold, conversational memory |
| TARG | M | P | M | D | Training-free reader-logit gate for one retrieval decision; general QA rather than conversational memory |
| SelRoute | M | M | M | M | Direct principle: cheap query-type routing among lexical/semantic/hybrid paths in conversational memory; signal differs |
| EviMem | M | P | M | M | Same evidence-gap escalation in memory, but LLM multi-cycle structured retrieval rather than BM25-first cascade |
| TierMem | M | P | M | M | Same cheapest-sufficient routing in memory, but generated summary-to-raw tiers and a trained router |
| Lexical--dense fusion | M | D | M | M | Same operation and domain, but dense retrieval is always on; provides the effect-size boundary a cascade must exploit |
| PGR | M | P | M | ? | Warrant/obligation gate is close, but only abstract-level evidence and domain/mechanism details are unverified |
| S2G-RAG | M | P | M | D | Structured sufficiency/gap loop with matched ablation, but general QA and a trained multi-call controller |

## Level assignment

The ResearchStudio scoop rubric assigns:

- **Level 1 - Full overlap:** the same problem, core mechanism, key insight, and domain are already present.
- **Level 2 - High overlap:** three axes match, or the central mechanism/insight is substantially present with a scope difference.
- **Level 3 - Partial overlap:** one or two axes match without the same core contribution.
- **Level 4 - Low overlap:** only broad motivation or terminology matches.

| Work | Match level | Reason |
|---|---|---|
| AgentIR | **Level 1** | All four axes, including the exact BM25-first conditional dense cascade in the same domain |
| TARG | **Level 2** | Same conditional-value problem and a simple uncertainty gate, but reader-prefix rather than BM25 evidence and outside the memory domain |
| SelRoute | **Level 1** | All four axes at the routing-principle level; query type replaces BM25 confidence as the signal |
| EviMem | **Level 2** | Same problem, insight, and domain; different structured-memory multi-call mechanism |
| TierMem | **Level 2** | Same problem, insight, and domain; different memory tiers and trained routing mechanism |
| Lexical--dense fusion | **Level 2** | Same problem, operation-value question, and domain; no conditional gate |
| PGR | **Level 2 (provisional)** | Problem and gate insight are close, but full text and memory-domain evidence are unavailable |
| S2G-RAG | **Level 2** | Direct sufficiency/gap mechanism and insight, but outside conversational memory and not lexical-first |

## What is and is not left

The broad novelty claim is exhausted. The only plausible remaining distinction is narrower:

- AgentIR predicts whether *retrieval rankings* warrant dense escalation from a BM25 score margin and tunes an answer-preserving threshold on labelled deployment queries.
- TARG predicts whether retrieval is needed from reader-prefix uncertainty, but it already defines paired with/without-retrieval correctness, states a conditional average calibration assumption linking uncertainty to that benefit, and empirically analyzes their disagreement.
- A future LazyMem controller could at most attempt to *directly predict cost-adjusted intervention value for one fixed semantic operation and transfer that predictor across conversational-memory corpora*, rather than threshold a retrieval- or reader-confidence proxy.

That difference is currently a research hypothesis, not a demonstrated delta, and direct utility-based policy learning has broader ancestors outside the capped conversational-memory search. It requires another collision check. It is only reviewer-defensible if experiments show that the outcome-aware policy outperforms AgentIR-style retrieval-margin gating, TARG-style reader-uncertainty gating, SelRoute-style type routing, and always-on fusion under the same reader, candidate budget, context budget, call budget, and held-out evaluation protocol.

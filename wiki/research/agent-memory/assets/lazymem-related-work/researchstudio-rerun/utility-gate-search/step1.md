# Step 1 - Decompose the Novelty

Timestamp: 2026-07-27

## Research problem

LazyMem has a strong lexical BM25-window path, but a semantic retrieval branch can add tokens, latency, and calls without changing the downstream answer. Retrieval confidence, query type, and reader uncertainty are not the same object as the causal answer change produced by an intervention. The research problem is to decide, per memory question, whether one fixed semantic operation has positive net downstream value under a matched reader/context/call budget and whether that decision transfers from a development conversation corpus to a held-out memory corpus.

## Proposed novelty under audit

Candidate: **Net-Value Certificates for Lazy Conversational Memory**. The candidate proposes to run a fixed BM25-window baseline, measure paired cheap-only versus one-semantic-operation answers during development, fit a one-sided lower prediction bound for the cost-adjusted answer difference, and invoke the semantic branch only when that lower bound is positive. The stated differentiator is a deployment action based on paired downstream answer utility, explicit costs, and cross-corpus transfer rather than retrieval score or reader uncertainty alone.

## Four axes

- **Problem framing:** query-conditional selective retrieval for long-term conversational memory, evaluated with the same reader, context packing, calls, tokens, latency, and downstream answer score on a held-out corpus.
- **Core mechanism:** cross-fitted paired intervention outcomes; a regularized lower prediction bound for net answer utility; a single semantic escalation action when the bound is above zero.
- **Key insight:** retrieval relevance/confidence is not intervention value; the only defensible reason to pay for the semantic branch is a calibrated positive lower bound on downstream answer improvement after all marginal costs.
- **Application domain:** persistent conversational memory, with LoCoMo as development diagnostics and LongMemEval-S as held-out transfer evaluation.

# Step 7 - Scoop Verdict and Surviving Delta

Timestamp: 2026-07-27 (Asia/Shanghai)

## Verdict

**Level 1 - Full overlap for the broad LazyMem redesign claim.**

AgentIR already implements and evaluates a BM25-first cascade for long-term conversational memory: BM25 confidence controls dense/fusion escalation, and thresholds are selected to preserve downstream answer accuracy while reducing cost. SelRoute independently establishes cheap lexical/semantic/hybrid routing in the same domain. EviMem, TierMem, and S2G-RAG further occupy the evidence-sufficiency, cheapest-sufficient-evidence, and structured-gap-controller neighborhoods.

Consequently, none of the following is defensible as LazyMem novelty:

1. raw dialogue as an authoritative memory layer;
2. BM25 as the cheap default path;
3. conditional dense or semantic fallback;
4. query-type routing among retrieval paths;
5. evidence sufficiency or missing-gap diagnosis;
6. summary-to-raw escalation through provenance;
7. the general principle that expensive memory computation should run only when useful.

## Nearest prior work

**Primary collision:** AgentIR (arXiv:2605.25092). It matches all four audited axes and reports both same-domain operating points and downstream answer-preservation evidence.

**Secondary collisions:** TARG for training-free reader-uncertainty gating; SelRoute for query-type routing; EviMem and S2G-RAG for insufficiency/gap-driven continuation; TierMem for cheapest-sufficient escalation; training-free lexical--dense fusion for the actual marginal retrieval value of running both channels.

## Surviving delta, stated honestly

There is no crisp implemented delta in the current LazyMem system. The present predicate compiler loses to BM25-window, so it cannot support a positive method claim.

A narrower, **unvalidated and not yet cleared** hypothesis survives:

> Unlike gates that threshold retrieval confidence or reader uncertainty, directly predict the paired, cost-adjusted intervention value of one fixed semantic operation and test whether that predictor transfers across conversational-memory corpora. Execute the operation only when a calibrated lower confidence bound on net utility is positive.

This is only a potential distinction because retrieval confidence and answer intervention value are not identical. A low BM25 margin may still yield answer-sufficient evidence; a high margin may confidently rank incomplete evidence; a dense result may improve retrieval metrics without changing the reader's answer. However, TARG already formalizes paired answer benefit, assumes average calibration with reader uncertainty, and measures their disagreement. Therefore paired answer-change analysis itself is not new. Direct cost-adjusted prediction plus cross-corpus transfer needs a separate collision search against utility learning, policy learning, and selective-RAG work before it can become a novelty claim.

## Reviewer-defensible falsification plan

1. **Frozen substrate.** Store immutable raw turns; use the same BM25-window candidates, semantic retriever, reader, prompts, maximum context, and answer judge for every controller.
2. **Paired intervention labels.** For each development query, run BM25-only and BM25-plus-one-semantic-operation. Measure paired answer change, evidence change, tokens, calls, and latency. Never use LoCoMo test outcomes to select the policy.
3. **Controllers.** Compare always-BM25, always-fusion, random escalation at matched rate, AgentIR-style BM25-margin threshold, TARG-style reader-prefix uncertainty, SelRoute-style cheap query features, retrieval-sufficiency classifier, and the proposed net-utility gate.
4. **Primary estimand.** Report average treatment effect of escalation and policy value under fixed cost constraints, not only Hit@k. Include confidence intervals and the fraction of queries for which escalation helps, is neutral, or hurts.
5. **Held-out transfer.** Develop on one partition/corpus and freeze the policy before evaluating on a genuinely held-out conversational-memory benchmark. LoCoMo remains development evidence only.
6. **Negative result rule.** Reject the new controller if its answer-quality/cost frontier does not dominate BM25-window and AgentIR-style margin gating, or if gains disappear under a matched reader/context/call budget.
7. **Simplicity rule.** The gate must be cheaper than the expected saved semantic work and must not require an additional online LLM call; otherwise it violates LazyMem's stated design objective.

## Paper-positioning consequence

The current paper should be positioned as a transparent negative result and experimental reset:

- BM25-window is the minimum baseline and currently outperforms the predicate compiler.
- The related-work section should explicitly acknowledge AgentIR, SelRoute, EviMem, TierMem, lexical--dense fusion, and S2G-RAG.
- The future contribution must be downstream intervention-value estimation, if it works, rather than generic lazy retrieval.
- No abstract, introduction, or conclusion should claim a new cascade or sufficiency controller before the held-out falsification experiment succeeds.

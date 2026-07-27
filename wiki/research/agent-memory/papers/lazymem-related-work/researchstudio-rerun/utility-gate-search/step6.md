# Step 6 - Comparison Against Proposed Novelty

Timestamp: 2026-07-27

## Proposed work

- **Title:** Net-Value Certificates for Lazy Conversational Memory
- **Date:** proposed
- **Source:** `ideaspark_run/lazymem-marginal-utility/phase2_coherence/refined_candidate.json`
- **Problem framing:** one fixed semantic escalation beyond BM25-window, with matched reader/context/call/token/latency budgets and held-out cross-corpus conversational-memory evaluation.
- **Core mechanism:** cross-fitted paired cheap-only/semantic intervention outcomes, a cost-adjusted one-sided lower prediction bound, and a gate that escalates only when the bound is positive.
- **Key insight:** relevance, query type, and reader uncertainty are imperfect proxies for downstream treatment value.
- **Application domain:** long-term conversational memory.

## Prior work A - Predicting Retrieval Utility and Answer Quality in RAG

- **Problem framing:** RAG performance prediction, with utility defined by contextual gain over no-context generation.
- **Core mechanism:** linear regression over retriever, reader, and document-quality predictors.
- **Key insight:** contextual performance gain and final answer quality can be predicted separately.
- **Application domain:** Natural Questions / general RAG.
- **Axes matching:** 2/4 (problem, insight); **Level 3 - Medium Overlap**. Full-text pending.

## Prior work B - TARG

- **Problem framing:** selective retrieve-vs-skip decision under answer-quality and latency tradeoffs.
- **Core mechanism:** threshold no-context reader uncertainty, with paired with/without-RAG outcomes used for calibration and analysis.
- **Key insight:** retrieval is useful conditionally and can be harmful when always applied.
- **Application domain:** open-domain QA over Wikipedia.
- **Axes matching:** 2/4 (problem, insight; mechanism partial); **Level 3 - Medium Overlap**.

## Prior work C - UtilityQwen passage selector

- **Problem framing:** select useful evidence from a large retrieved candidate list for downstream QA.
- **Core mechanism:** distill pseudo-answer utility judgments into a small sliding-window selector.
- **Key insight:** utility, not topical relevance, determines answer-supporting passages.
- **Application domain:** NQ/HotpotQA RAG.
- **Axes matching:** 2/4 (mechanism, insight; problem partial); **Level 3 - Medium Overlap**.

## Prior work D - SCARLet

- **Problem framing:** train retrievers aligned with downstream task utility across multiple RALM tasks.
- **Core mechanism:** shared-context synthesis plus perturbation-based generation attribution and contrastive retriever training.
- **Key insight:** passage utility depends on downstream output and inter-passage interactions.
- **Application domain:** ten open-domain RALM tasks.
- **Axes matching:** 2/4 (mechanism, insight; problem partial); **Level 3 - Medium Overlap**.

## Prior work E - Cost-Aware Adaptive Retrieval Depth

- **Problem framing:** dynamic retrieval depth and search interaction under token/latency cost.
- **Core mechanism:** RL-trained Dynamic Search-R1 with memory- and latency-bound cost penalties.
- **Key insight:** answer reward must be traded against retrieval/reasoning cost.
- **Application domain:** seven general and multi-hop QA datasets.
- **Axes matching:** 2/4 (problem, insight; mechanism partial); **Level 3 - Medium Overlap**.

## Prior work F - Learning to Rank for Multiple RAG Models through Iterative Utility Maximization

- **Problem framing:** choosing among multiple RAG models with utility as the optimization signal.
- **Core mechanism:** unresolved without full text; title and indexed metadata explicitly claim iterative utility maximization.
- **Key insight:** downstream utility can drive model selection rather than fixed relevance ranking.
- **Application domain:** multiple RAG models.
- **Axes matching:** provisional 3/4 (problem, mechanism, insight); **Level 2 - High Overlap**. This provisional collision prevents a Level 3-or-better novelty claim until the ACM paper is read.

## Prior work G - Consistent Estimators for Learning to Defer to an Expert

- **Problem framing:** predict or defer to a downstream expert under an explicit joint system loss.
- **Core mechanism:** reduction to cost-sensitive learning with a consistent surrogate over an augmented deferral action.
- **Key insight:** confidence-only rejection can fail because the downstream actor's strengths and weaknesses matter.
- **Application domain:** classification with human/synthetic experts, not RAG memory.
- **Axes matching:** 2/4 (core abstraction, insight; domain differs); **Level 3 - Medium Overlap**.

## Overall verdict

**Provisional Level 2 - High Overlap.** The strongest cap is the exact-title ICTIR 2025 paper, whose indexed title already places iterative utility maximization at the multiple-RAG-model decision layer; the ECIR 2026 paper independently defines the paired contextual performance gain; TARG makes paired outcome analysis and retrieve-or-skip gating operational; SCARLet and UtilityQwen make downstream utility a retrieval training/selection target; and cost-aware depth makes answer reward versus retrieval cost a learned objective. A narrower delta around a one-sided cost-adjusted certificate for one fixed memory intervention and cross-corpus transfer may survive, but it is not cleared as novel until the ICTIR paper's full method is obtained and the proposed gate beats these controls.

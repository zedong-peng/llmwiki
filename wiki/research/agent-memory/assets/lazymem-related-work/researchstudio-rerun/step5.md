# Step 5 - Full-Text Deep Dive

Timestamp: 2026-07-27 (Asia/Shanghai)

## Audit protocol

Each candidate is checked against four axes from Step 1:

1. **Problem framing:** restore sufficient evidence from long raw dialogue under a reader/context/call budget.
2. **Core mechanism:** begin with a cheap lexical path and invoke a semantic path only conditionally.
3. **Key insight:** the expensive operation should run only when its expected marginal downstream value is positive.
4. **Domain:** long-term or multi-session conversational memory.

"Full-text verified" means that the local PDF, rather than API metadata alone, was inspected. Reported numbers retain the paper's own protocol and are not treated as directly comparable LazyMem results.

## 1. AgentIR

**Paper:** *AgentIR: A Workload-Adaptive Cascade Retrieval Substrate for Long-Term Conversational Memory* (arXiv:2605.25092, 2026).  
**Evidence level:** full-text verified from the official arXiv PDF.

- **Problem and domain.** AgentIR explicitly targets long-term conversational-memory retrieval under latency and capacity constraints, with LongMemEval and LoCoMo as its principal memory workloads.
- **Mechanism.** BM25 always runs first. A classifier-free confidence trigger computes the normalized top-1/top-2 BM25 score margin. High-margin queries exit on BM25; low-margin queries escalate to dense retrieval, reciprocal-rank fusion, and a recency component. A second variant predicts question type and uses per-type thresholds.
- **Downstream criterion.** Thresholds are selected to maximize skip rate while preserving answer accuracy within a bootstrap/noise tolerance relative to always-hybrid retrieval. This is already an empirical value-of-escalation policy, although the online signal is retrieval confidence rather than a direct estimate of answer-utility gain.
- **Results.** On LongMemEval, the global threshold skips dense retrieval for 63% of queries with parity LLM-judged accuracy and a reported 2.67x speedup. Per-question-type thresholds reach 5.76x in five-fold cross-validation. On the paper's LoCoMo setting, BM25 wins outright, producing a 100% dense-skip rate, 132x speedup, and a +0.089 Hit@5 change relative to its always-hybrid reference.
- **Assumptions and limits.** The global operating point and the per-workload policy are selected using roughly 50 labeled deployment questions; the per-type version additionally needs a query-type classifier. Answer preservation depends on LLM judges and a finite tolerance. The result shows that a retrieval-margin proxy can work, not that it estimates causal answer gain for every query.
- **Closest evidence.** Figure 1 and Section 5.9 define the BM25-margin cascade; Tables 11--12 give LongMemEval/LoCoMo operating points; Appendix J reports threshold sweeps and cross-validation.
- **Overlap.** All four axes match. This paper is a direct collision with a broad "BM25 first, dense only when useful" LazyMem claim.

## 2. SelRoute

**Paper:** *SelRoute: Query-Type-Aware Routing for Long-Term Conversational Memory Retrieval* (arXiv:2604.02431, 2026).  
**Evidence level:** full-text verified from the official arXiv PDF.

- **Problem and domain.** SelRoute studies long-term conversational-memory retrieval and asks which retrieval path should serve each query type.
- **Mechanism.** A cheap regex classifier routes among FTS5/BM25-style lexical retrieval, dense semantic retrieval, hybrid fusion, and vocabulary-enriched retrieval. The route is based on predicted query type, not on the confidence or outcome of a first-stage result.
- **Key result.** The regex classifier has 72% exact type accuracy but 83% effective routing accuracy because some classification errors choose the same route. Predicted routing reaches Recall@5 0.689, above uniform FTS5 in the paper's setup.
- **Assumptions and limits.** The routing table was derived empirically on LongMemEval rather than transferred from an independent development domain. The authors flag an FTS5-versus-published-BM25 comparability gap. Generalization is uneven: RECOR Recall@5 is 0.149, exposing a failure on reasoning-heavy retrieval.
- **Closest evidence.** Sections 3 and 4 specify the four routes; Section 5.3 evaluates predicted types; Sections 6.3 and 6.5 discuss comparability and limitations.
- **Overlap.** The problem, conditional lexical/semantic routing idea, value insight, and memory domain match. The gate signal differs materially: pre-retrieval query type rather than post-BM25 evidence or downstream utility.

## 3. EviMem

**Paper:** *EviMem: Evidence-Gap-Driven Iterative Retrieval for Long-Term Conversational Memory* (arXiv:2604.27695, 2026).  
**Evidence level:** full-text verified from the official arXiv PDF.

- **Problem and domain.** EviMem targets missing, temporally scattered, and multi-hop evidence in long multi-session conversations.
- **Mechanism.** Its IRIS controller evaluates the accumulated evidence as EXACT, INFERRABLE, or PARTIAL, diagnoses the missing evidence, writes a targeted follow-up query, and repeats for at most three iterations. It runs over LaceMem, a write-time structure with tuple indexes, graph edges, and provenance-linked raw evidence. If evidence remains insufficient, it abstains.
- **Key result.** The paper reports LoCoMo judge accuracy of 81.6% on temporal questions and 85.2% on multi-hop questions, versus MIRIX values of 73.3% and 65.9%. Average latency is reported as 9.54 seconds versus 42.71 seconds for MIRIX. These are not a one-call lexical baseline comparison: IRIS uses several role-specific LLM calls per question and a structured memory substrate.
- **Assumptions and limits.** Sufficiency, diagnosis, refinement, and answer generation depend on LLM prompts and calibrated thresholds; the retrieval substrate is not raw-dialogue BM25. The iterative design can be substantially more expensive than a single-pass baseline even when faster than MIRIX.
- **Closest evidence.** Section 3.2 and Algorithms 1--2 define IRIS; Tables 1--3 give answer, latency, and component ablations; the limitations section bounds the evaluation.
- **Overlap.** The evidence-sufficiency framing, conditional escalation insight, and conversational-memory domain match strongly. The core mechanism is only partial overlap because it is a multi-call structured-memory loop, not a lexical-first cascade.

## 4. TierMem

**Paper:** *From Lossy to Verified: A Provenance-Aware Tiered Memory for Agents* (arXiv:2602.17913, 2026).  
**Evidence level:** full-text verified from the official arXiv PDF.

- **Problem and domain.** TierMem asks whether an agent can answer cheaply from summaries while retaining a path to faithful raw evidence when summaries are insufficient.
- **Mechanism.** Tier 1 stores concise summaries, embeddings, and provenance pointers; Tier 2 stores immutable raw pages. A learned Answer-versus-Escalate router either answers from summaries or follows provenance links and performs bounded raw retrieval. The router is trained with supervised fine-tuning and GRPO.
- **Key result.** On LoCoMo, the routed system scores 0.851 versus 0.873 for raw-only while reducing average input tokens by 54.1% and latency by 60.7% (3,396+584 versus 7,398 tokens; 6.76 versus 17.18 seconds). It escalates 39% of queries. For escalated cases, linked provenance improves accuracy from 77.5% to 81.7% compared with no-linked retrieval.
- **Assumptions and limits.** The cheap tier is lossy, generated at write time, and the router is trained. Thus the method does not preserve LazyMem's no-write-LLM simplicity. Its measured trade-off also accepts an accuracy loss relative to always-raw.
- **Closest evidence.** The architecture section defines the two tiers and router; Tables 1, 4, and 5 report end-to-end cost, escalation behavior, and provenance ablations.
- **Overlap.** The cheapest-sufficient-evidence framing, conditional value insight, and conversational-memory domain match. The mechanism differs: summary-to-raw escalation rather than BM25-to-semantic escalation.

## 5. Training-Free Lexical--Dense Fusion

**Paper:** *Training-Free Lexical-Dense Fusion for Conversational-Memory Retrieval* (arXiv:2606.04194, 2026).  
**Evidence level:** full-text verified from the official arXiv PDF.

- **Problem and domain.** The paper isolates lexical/dense complementarity in conversational-memory retrieval under controlled retrieval units and evaluation.
- **Mechanism.** It computes BM25 and max-turn dense scores for every query and combines normalized scores with a cross-validated weight. This is always-on fusion, not a cascade.
- **Results and boundary.** On LoCoMo, BM25 obtains Hit@1/Recall@5/NDCG@5 of 0.640/0.833/0.746, while the best fusion obtains 0.752/0.894/0.829. On LongMemEval-S, BM25 obtains 0.589/0.948/0.916 and fusion 0.594/0.959/0.930; the paper says the net fusion gain over BM25 is small and not significant there. A cross-encoder reranker lowers LoCoMo Hit@1 from 0.701 to 0.633 in its tested pipeline, a 6.88-point decrease.
- **Assumptions and limits.** Fusion weights are selected by leave-one-conversation-out cross-validation. The study establishes heterogeneous marginal value across corpora and categories, but it does not learn when to avoid the dense call.
- **Closest evidence.** Tables 3--5 report the LoCoMo comparison and reranker ablation; Table 6 and the accompanying significance analysis report LongMemEval-S.
- **Overlap.** The problem, semantic-operation value question, and conversational-memory domain match. The conditional mechanism does not: both channels always run.

## 6. Evidence-Obligation Pool-Gated Retrieval (PGR)

**Paper:** *Evidence-Obligation Pool-Gated Retrieval: Stable Multi-Cycle Retrieval via Evidence Ledger and Warrant Judge* (Myung Ho Kim, Preprints.org, DOI 10.20944/preprints202607.1060.v1, 2026).  
**Evidence level:** abstract and Crossref metadata only. The official PDF endpoint returned HTTP 403 after DOI resolution and user-agent retries; no independent full text was available. Claims below must therefore be treated as provisional.

- **Problem.** The abstract targets multi-cycle retrieval failures caused by unstable semantic warrant decisions and poor evidence-obligation lifecycle management.
- **Reported mechanism.** One additional LLM Warrant Judge is paired with a deterministic turn-scoped Evidence Ledger whose obligations transition among pending, found, gap, and reused-gap states.
- **Reported insight.** Retrieval should continue only while a semantic warrant remains unsupported and unresolved obligations justify another cycle. This is close to an explicit evidence-value gate.
- **Limits.** The application domain, benchmark protocol, matched-cost evidence, and implementation details could not be verified. It is a recent preprint rather than an accepted archival paper.
- **Overlap.** The evidence-obligation and conditional-computation ideas overlap, but the conversational-memory domain and lexical-first mechanism are unverified. This record cannot by itself establish a full scoop.

## 7. S2G-RAG

**Paper:** *S2G-RAG: Structured Sufficiency and Gap Judging for Iterative Retrieval-Augmented QA* (ACL 2026, pp. 25846--25862, DOI 10.18653/v1/2026.acl-long.1185).  
**Evidence level:** full-text verified from the ACL PDF.

- **Problem and domain.** S2G-RAG addresses premature stopping and unfocused repeated retrieval in open-domain single-hop and multi-hop QA (TriviaQA, HotpotQA, and 2WikiMultiHopQA), not persistent conversational memory.
- **Mechanism.** At each turn a fine-tuned S2G-Judge receives the question and accumulated compact evidence, outputs a binary sufficiency decision plus structured gap items, and converts gaps into the next query. BM25 or E5 retrieves documents, and an LLM sentence-pointer extractor retains gap-aligned evidence. The process stops when sufficient or at a fixed maximum turn count.
- **Matched evidence.** Under BM25 with the retrieval budget and answer reasoner held fixed, S2G-RAG reaches 43.3 EM / 56.5 F1 on HotpotQA. Removing the judge drops this to 27.5/37.6; removing the extractor yields 39.5/52.5. The sufficiency judge has a 6.44% false-positive rate but predicts insufficient for 31.60% of actually sufficient states, so it is conservative.
- **Cost boundary.** Evidence compression is reported as roughly 4.5x--6.4x. End-to-end latency is 1.6085 seconds per question versus 0.3787 for standard RAG and 1.9552 without the extractor. The extractor improves the iterative pipeline, but the full system is still more than four times slower than standard RAG in this table.
- **Assumptions and limits.** The controller is LoRA-fine-tuned from teacher-labelled process traces, and the sentence extractor uses an LLM. The authors identify conservative calibration and possible omission of surrounding or multi-sentence evidence as limitations.
- **Closest evidence.** Sections 3.1--3.3 define the judge/gap/extractor loop; Tables 1--3 provide matched answer and ablation results; Sections 4.5.2--4.5.3 analyze calibration, compression, and latency.
- **Overlap.** The evidence-sufficiency problem, structured gap gate, and marginal-computation intuition match. The domain and lexical-first simplicity do not. It nevertheless blocks any general novelty claim for a structured sufficiency/gap controller.

## Deep-dive conclusion

AgentIR is the decisive same-domain collision: it matches the problem, cascade mechanism, conditional-value rationale, and conversational-memory domain. SelRoute supplies a second same-domain routing formulation; EviMem and TierMem cover evidence-driven and cheapest-sufficient escalation; S2G-RAG independently establishes a structured sufficiency/gap loop with strong matched ablations outside the memory domain. Therefore LazyMem cannot defensibly claim the broad principle or any of these controller forms as novel.

## IdeaSpark collision addendum: TARG

The subsequent IdeaSpark map search retrieved *Retrieval as a Decision: Training-Free Adaptive Gating for Efficient RAG* (TARG; TMLR 2026, arXiv:2511.09803). This paper was outside the capped seven-paper Scoop deep dive, but its PDF-derived introduction and method summary were verified in the IdeaSpark full-text cache.

TARG produces a short no-context draft, computes reader-side uncertainty from mean entropy, a top-1/top-2 logit-margin transform, or small-sample stochastic-prefix variance, and makes a single training-free retrieve-or-skip decision. Its reported default uses a 20-token prefix with about 50 ms overhead and reduces retrieval by 70--90% over five general-QA datasets while matching or improving always-retrieve EM/F1. More importantly for novelty, Section 3.3 defines retrieval benefit as paired correctness under Never-RAG and Always-RAG, assumes conditional average alignment between that benefit and uncertainty, and Appendix A.7 reports development quadrants where retrieval helps or hurts. It is not conversational memory and its online gate uses uncertainty rather than directly predicting cost-adjusted treatment effect, but it blocks both generic reader-confidence gating and paired answer-change analysis. Any surviving LazyMem hypothesis must therefore be narrower than "measure downstream intervention value."

# Step 5 - Full-Paper Deep Dive

Timestamp: 2026-07-27

## 1. Predicting Retrieval Utility and Answer Quality in RAG

- **Venue / evidence:** ECIR 2026, *Advances in Information Retrieval*, pp. 368--385, DOI `10.1007/978-3-032-21289-4_24`; official Springer abstract/metadata only because the chapter is subscription-gated.
- **Verified problem:** predicts retrieval performance and generation performance for RAG; retrieval utility is explicitly the performance gain from generation with retrieved context over generation without context.
- **Verified mechanism:** linear regression over query-performance predictors, reader-centric perplexity of retrieved context conditioned on the query, and document quality/readability features.
- **Verified scope:** Natural Questions; no evidence in the available abstract of a cost-adjusted deployment action, lower confidence bound, persistent conversational memory, or cross-corpus transfer.
- **Evidence:** official Springer abstract saved in [`papers/predicting-retrieval-utility.abstract.txt`](papers/predicting-retrieval-utility.abstract.txt); HTML landing page retained as `papers/predicting-retrieval-utility.html`.
- **Refined overlap:** problem = match; mechanism = partial; insight = match; application = differ. Provisional 2/4 axes, Level 3, but this is the strongest unresolved risk because the full chapter was not accessible.

## 2. Distilling a Small Utility-Based Passage Selector

- **Venue / evidence:** SIGIR-AP 2025; official ACM PDF downloaded as `papers/utility-passage-selector.pdf` and extracted to `.txt`.
- **Verified problem:** RAG passage relevance is not enough; utility is usefulness for generating an accurate answer, and LLM utility judgments are too expensive for large candidate lists.
- **Verified mechanism:** Qwen3-32B generates pseudo-answers and utility selections on 100k MS MARCO queries; a Qwen3-1.7B student uses a front-to-back sliding window to select a variable number of useful passages from BM25/BGE top-100 candidates.
- **Verified results:** on HotpotQA, UtilityQwen selection reaches 60.58 evidence micro-F1 / 53.56 answer F1 with Llama-3.1 over BGE and 57.03 / 50.57 over BM25; the paper reports about 70% lower inference time than relevance ranking in its table-5 setup (3.4h vs 11.2h for the student). This is selection inside an always-retrieved RAG pipeline, not retrieve-vs-skip gating.
- **Evidence:** Sections 2.2, 3, 4, 5, and Table 1/Table 5 in the extracted text.
- **Refined overlap:** problem = partial; mechanism = partial; insight = match; application = differ. 2/4 axes, Level 3.

## 3. SCARLet utility retriever

- **Venue / evidence:** EMNLP 2025, ACL Anthology PDF `papers/utility-retriever-attribution.pdf` / `.txt`.
- **Verified problem:** semantic relevance can misalign retrievers with downstream generation utility, especially across tasks and multi-hop passage interactions.
- **Verified mechanism:** build shared context, synthesize multi-task data, perturb passages, measure generation-logit fluctuations, fit passage-level utility attribution, and train a contrastive retriever.
- **Verified results:** Table 2 reports SCARLetBGE improving over BGE across ten tasks; e.g. NQ 49.2 vs 47.5 and HotpotQA 47.0 vs 41.6 under one generator, with similar gains under another. The method trains a retriever; it does not deploy a paired cheap-only/semantic action gate.
- **Evidence:** Abstract, Sections 1, 3.2--3.4, and Tables 2--5; the method explicitly says utility attribution is based on perturbation-induced changes in the generated output.
- **Refined overlap:** problem = partial; mechanism = partial; insight = match; application = differ. 2/4 axes, Level 3.

## 4. TARG

- **Venue / evidence:** TMLR 2026, arXiv `2511.09803v2`; official PDF `papers/targ.pdf` / `.txt`.
- **Verified problem:** retrieval can hurt answer quality and inflate tokens/latency; decide whether to retrieve.
- **Verified mechanism:** a short no-context draft supplies entropy, top-1/top-2 margin, or stochastic-prefix variance; threshold once and retrieve only above the gate.
- **Verified theory/evaluation:** Section 3.3 defines `A^(0)(q)`, `A^(1)(q)`, and `Delta(q)=A^(1)-A^(0)` and assumes conditional usefulness calibration. Appendix A.7 reports the four uncertainty/benefit quadrants, including confident-but-retrieval-useful and uncertain-but-retrieval-harmful cases.
- **Verified results/scope:** five open-domain QA benchmarks, dense Wikipedia retriever, 70--90% fewer retrievals with matched/improved EM/F1; no conversational-memory transfer.
- **Refined overlap:** problem = match; mechanism = partial; insight = match; application = differ. 2/4 axes, Level 3. Paired outcome analysis is prior art, not an Idea escape hatch.

## 5. Cost-Aware Retrieval-Augmentation Reasoning with Adaptive Depth

- **Venue / evidence:** arXiv preprint `2510.15719v1`; official PDF `papers/cost-aware-depth.pdf` / `.txt`.
- **Verified problem:** fixed retrieval depth and reasoning tokens are costly and can be insufficient for complex questions.
- **Verified mechanism:** Dynamic Search-R1 lets the model request more documents and trains PPO/GRPO with a cost-aware advantage function; memory-bound cost counts tokens, latency-bound cost distinguishes generated-token latency from retrieved-token encoding latency.
- **Verified results/scope:** seven general/multi-hop QA datasets; the abstract reports 16--20% lower latency and about 5% higher EM on average. It is an end-to-end RL policy for interactive search, not a small supervised lower-bound gate over one fixed semantic operation.
- **Refined overlap:** problem = match; mechanism = partial; insight = match; application = differ. 2/4 axes, Level 3.

## 6. Learning to Rank for Multiple RAG Models through Iterative Utility Maximization

- **Venue / evidence:** ICTIR 2025, DOI `10.1145/3731120.3744584`; ACM PDF endpoint returned HTTP 403. Metadata and title are verified; mechanism remains abstract-only and is not treated as fully read.
- **Verified scope:** the title directly names multiple RAG models and iterative utility maximization. No defensible claim about its exact routing features, cost accounting, or memory domain is made without the paper body.
- **Refined overlap:** problem = likely match; mechanism = likely match; insight = likely match; application = differ. Provisional 3/4 axes, Level 2, and the most dangerous unresolved collision for a utility-based router.

## 7. Consistent Estimators for Learning to Defer to an Expert

- **Venue / evidence:** ICML 2020 / arXiv v3 `2006.01862`; official PDF `papers/consistent-defer-estimators.pdf` / `.txt`.
- **Verified problem:** a predictor chooses to answer or defer to a downstream expert with potentially different information and cost.
- **Verified mechanism:** formulate the joint system as cost-sensitive learning over an augmented action space and derive a convex consistent surrogate. Section 5.1 shows the failure mode of independently comparing classifier and expert confidence.
- **Verified scope:** CIFAR-10/100, hate speech, and chest X-ray synthetic-expert experiments; no RAG or memory.
- **Refined overlap:** problem = partial; mechanism = partial; insight = match; application = differ. 2/4 axes, Level 3. It supplies the formal deferral ancestor, not a direct LazyMem competitor.

## Evidence failures

The ACM PDFs for the utility selector, ICTIR iterative utility ranking, and Stochastic RAG were not uniformly accessible; the utility selector succeeded, while the latter two returned 403. The Springer chapter PDF returned an HTML paywall page; its official abstract was preserved separately. These limitations are reflected in the comparison instead of being silently upgraded to full-text evidence.

# LazyMem: Related Work, Novelty Audit, and Experimental Positioning

Literature cutoff: 2026-07-27

Corpus: 45 official arXiv PDFs, indexed in [`selection.tsv`](selection.tsv)

## Executive conclusion

The literature supports the design pressure behind LazyMem, but it does not support the current mechanism as a contribution.

The strong part of the LazyMem thesis is that a long-term memory system should preserve an authoritative raw record, avoid lossy write-time commitments unless their value is measured, and spend semantic computation only when a cheap path is inadequate. The weak part is novelty: raw-history retrieval, no or light ingestion, BM25-first search, query-dependent routing, dense fallback, evidence-sufficiency checks, and escalation to raw text are all represented in direct 2025-2026 work. The current query compiler also loses to the repository's own BM25-window control on LoCoMo development data: F1 0.5019 versus 0.5526, judge accuracy 0.7422 versus 0.7864, and 2,320 versus 1,974 recorded tokens per question. It is therefore a rejected ablation, not a validated improvement.

The closest direct collisions are:

- [AgentIR](pdfs/2605.25092-agentir.pdf), which uses the BM25 top-k score margin to decide whether the dense channel is worth running;
- [Training-Free Lexical-Dense Fusion](pdfs/2606.04194-lexical-dense-fusion.pdf), which directly measures when BM25 and turn-level dense late interaction are complementary;
- [Back to Basics / Nano-Memory](pdfs/2604.11628-back-to-basics.pdf), which argues for retrieval plus generation over unstructured history and introduces turn-isolated scoring and query-driven pruning;
- [SelRoute](pdfs/2604.02431-selroute.pdf), which deterministically routes query types among lexical, semantic, hybrid, and enriched retrieval;
- [EviMem](pdfs/2604.27695-evimem.pdf), which diagnoses evidence gaps and iteratively refines retrieval;
- [TierMem](pdfs/2602.17913-tiermem.pdf), which answers from the cheapest sufficient tier and escalates to immutable raw logs;
- [SmartSearch](pdfs/2603.15599-smartsearch.pdf), which makes raw substring/entity recall cheap and treats ranking and truncation as the actual bottleneck; and
- [Fidelity Before Structure](pdfs/2601.00821-fidelity-before-structure.pdf), which holds the retriever, reranker, and judge fixed and finds that verbatim chunks beat lossy typed artifacts.

The defensible next paper is consequently not "a simpler memory architecture beats complex memory." The evidence does not show that. A defensible paper could instead be one of two things:

1. a rigorously matched negative-result and baseline paper showing where BM25-window dominates added memory machinery and defining a lifecycle-cost evaluation contract; or
2. a new retrieval mechanism whose marginal value survives BM25-window, lexical-dense fusion, and an adaptive cascade under a frozen reader, frozen budget, and held-out evaluation.

Until the second condition is met, LazyMem should present BM25-window as its operational default and the LLM compiler as an unsuccessful intervention.

## 1. Problem definition

Let a conversation history be a sequence of raw turns

```text
D = (d_1, ..., d_n),
```

and let `q` be a later question whose correct answer is `a`. A memory system may transform the history at write time,

```text
M = f_write(D),
```

retrieve evidence at query time,

```text
R = f_retrieve(q, M; B, C),
```

and pass `R` to a reader under context budget `B` and compute/call budget `C`. This decomposition separates five objects that memory papers often conflate:

| Object | Scientific question | Typical failure |
|---|---|---|
| Source record | What remains recoverable? | A summary or extracted fact omits a future-critical detail. |
| Retrieval unit | What can be admitted atomically? | A session unit adds noise; a turn unit loses surrounding context. |
| Candidate generator | What evidence can enter consideration? | Vocabulary mismatch or missing bridge evidence creates false negatives. |
| Ranker/packer | What survives the reader budget? | Gold evidence is recalled but ranked below the context cutoff. |
| Reader/controller | Is retrieved evidence used correctly? | The answer model ignores, miscombines, or is harmed by memory. |

The relevant optimization target is not retrieval accuracy in isolation. A simplified objective is

```text
J(pi) = E[U_answer(pi)]
        - lambda_w C_write(pi)
        - lambda_r C_retrieve(pi)
        - lambda_t C_reader_tokens(pi)
        - lambda_l C_latency(pi),
```

subject to evidence provenance and correctness constraints. A system is scientifically interesting when it moves the Pareto frontier, not when it adds a mechanism that raises one intermediate metric while using a different reader, more tokens, more calls, or a more permissive judge.

This framing yields the first-principles version of "lazy" memory:

> Buy an additional operation only when its conditional expected answer utility exceeds its full marginal lifecycle cost.

That principle is stronger than "use a fallback for difficult queries." It requires paired evidence that the gate identifies positive-value interventions, that the fallback actually repairs them, and that the same policy transfers outside the development distribution.

## 2. Evaluation foundations

### 2.1 What the main benchmarks measure

[LoCoMo](pdfs/2402.17753-locomo.pdf) supplies long multi-session conversations, question categories, and evidence annotations. It is useful for turn-level retrieval diagnosis, but its small set of source conversations makes conversation-level leakage and development overfitting serious risks. A result tuned repeatedly on LoCoMo is development evidence, even if all 1,540 questions are eventually reported.

[LongMemEval](pdfs/2410.10813-longmemeval.pdf) separates question types such as information extraction, multi-session synthesis, temporal reasoning, knowledge updates, and abstention. Its much longer histories make context selection material, but reported results vary with the S/M split, retrieval granularity, and evaluation protocol.

[MemTrace](pdfs/2606.17328-memtrace.pdf) is important because final answer accuracy hides whether failure occurred in candidate retrieval, complete evidence collection, or evidence use. This is directly relevant to a pair or multi-hop mechanism: aggregate F1 cannot establish that pairwise co-support caused the gain.

[MemOps](pdfs/2607.12893-memops.pdf) broadens evaluation from recall QA to lifecycle operations such as remember, update, forget, and reflect. A raw append-only design is naturally strong on preservation and weak on explicit deletion, conflict resolution, and consolidation unless those operations are defined separately.

[MEMAUDIT](pdfs/2605.02199-memaudit.pdf) isolates memory writing from downstream retrieval and reader choices using a package-oracle protocol. Its methodological lesson is general: if the claim is about write-time representation, evaluate what the representation preserved before attributing a final QA score to it.

[Beyond Memory Leaderboards](pdfs/2607.16848-budgeted-context-restoration.pdf) frames scientific memory evaluation as budgeted context restoration and reports that sparse-dense hybridization can dominate architectural labels. This matches the central concern here: the right comparison is between budget-matched evidence-restoration policies, not between product names.

[RUMBA](pdfs/2607.21447-rumba.pdf) adds a multilingual setting and session/temporal factors. It highlights a likely weakness of exact lexical predicates: morphology, transliteration, and lexical variation can change the relative strength of BM25, character/subword retrieval, and dense models.

### 2.2 Why published headline scores are often incomparable

At minimum, a cross-system result depends on:

- the exact question set and exclusions;
- whether the full conversation, oracle conversation, or a global corpus is searched;
- session, chunk, round, or turn retrieval units;
- answer model and checkpoint;
- answer prompt and chain-of-thought policy;
- number of retrieved units and final token budget;
- judge model, rubric, and abstention treatment;
- access to gold timestamps, categories, or evidence during routing; and
- whether hyperparameters were selected on the reported conversations.

SmartSearch explicitly reports two incompatible LoCoMo protocols separately. SelRoute documents large FTS5-versus-BM25 and granularity-dependent discrepancies across LongMemEval reports. These are not editorial details. A five-point gain can be smaller than the effect of changing the reader or judge.

For LazyMem, the minimum credible reporting unit is a per-question paired ledger containing: query ID, retrieved IDs, gold evidence IDs, final context tokens, calls, latency, answer, answer score, and error status. Any router must additionally log the cheap-path confidence, selected route, fallback cost, and the paired counterfactual outcomes of cheap-only and fallback execution on a held-out audit subset.

## 3. Memory representation: raw fidelity versus write-time structure

### 3.1 Structured memory systems

[MemGPT](pdfs/2310.08560-memgpt.pdf) treats limited context as a memory hierarchy managed through explicit movement between tiers. [Mem0](pdfs/2504.19413-mem0.pdf) emphasizes production-oriented extraction, update, and retrieval. [A-MEM](pdfs/2502.12110-a-mem.pdf) constructs linked notes dynamically. [Zep](pdfs/2501.13956-zep.pdf) represents temporal facts in a knowledge graph. [EverMemOS](pdfs/2601.02163-evermemos.pdf), [Hindsight](pdfs/2512.12818-hindsight.pdf), [ENGRAM](pdfs/2511.12960-engram.pdf), [HingeMem](pdfs/2604.06845-hingemem.pdf), [PRISM](pdfs/2605.12260-prism.pdf), and [GRAVITY](pdfs/2605.01688-gravity.pdf) add combinations of memory tiers, typed objects, boundaries, graphs, routing, compression, and relational or temporal anchors.

These systems respond to real problems. Structure can normalize aliases, expose temporal relations, merge redundant evidence, improve update semantics, and reduce reader tokens. It can also make a long history navigable when raw retrieval is weak. The correct first-principles objection is not "structure is bad." It is that lossy structure should not become the only source of truth before future queries are known.

If `f_write` is non-invertible, information omitted by `f_write(D)` cannot be reconstructed from that representation alone. This is a preservation statement, not an accuracy theorem: a lossy summary may still make the relevant fact much easier to retrieve. The empirical question is whether its retrieval and compression gain exceeds its omission cost for the target workload.

### 3.2 Controlled evidence for verbatim storage

[Fidelity Before Structure](pdfs/2601.00821-fidelity-before-structure.pdf) is the cleanest direct evidence. It holds retriever, reranker, and judge constant while comparing typed extracted artifacts with verbatim conversation chunks. It reports verbatim advantages of 15.9 accuracy points on LoCoMo (43.9 versus 28.0) and 22.0 points on LongMemEval-S (67.4 versus 45.4). Taking the union of artifacts does not close the gap. The paper's appropriately narrow conclusion is that structure should augment verbatim evidence rather than replace it.

This supports LazyMem's preservation premise, but it also consumes much of its novelty. Raw storage is now an experimental baseline with direct positive evidence, not a new LazyMem contribution.

[Back to Basics](pdfs/2604.11628-back-to-basics.pdf) reaches a related conclusion from a retrieval perspective. Its Nano-Memory system keeps an unstructured memory and focuses on two sources of signal sparsity: averaging a long session dilutes the relevant turn, and feeding a whole retrieved session dilutes the evidence presented to the reader. Turn Isolation Retrieval scores a session by its best-matching turn; Query-Driven Pruning removes conversational padding before answering.

[A Simple Yet Strong Baseline](pdfs/2511.17208-event-memory-baseline.pdf) uses non-compressive event-oriented memory with straightforward dense retrieval. It demonstrates that a minimally abstractive unit can be competitive without a heavy memory operating system.

[SmartSearch](pdfs/2603.15599-smartsearch.pdf) operates on raw history with no LLM ingestion. Its oracle analysis reports very high raw candidate recall and identifies ranking, rather than initial search, as the main bottleneck. It therefore applies learned models surgically after deterministic retrieval.

[Eywa](pdfs/2605.30771-eywa.pdf) separates immutable evidence from derived facts and deterministic retrieval routes. This is a useful refinement of the raw-memory idea: preserve evidence, but permit derived views with provenance instead of forcing a false choice between raw and structured memory.

### 3.3 Consequence for LazyMem

The defensible representation contract is:

1. raw turns are the authoritative evidence layer;
2. every summary, fact, edge, or embedding is a derived index, not a replacement;
3. derived objects carry source-turn provenance;
4. update and deletion semantics apply consistently to raw and derived layers; and
5. final contexts retain enough source text for verification.

This is a good systems requirement. It is not, by itself, a sufficient research contribution after Fidelity Before Structure, TierMem, EviMem, and Eywa.

## 4. Retrieval: what level of baseline is BM25?

### 4.1 BM25 is the minimum lexical floor

BM25 is a bag-of-words probabilistic ranking function with term-frequency saturation, inverse-document-frequency weighting, and document-length normalization. In a common form,

```text
score(q, d) = sum_{t in q} IDF(t) * tf(t,d) * (k1 + 1)
              / (tf(t,d) + k1 * (1 - b + b * |d| / avgdl)).
```

It is substantially stronger than counting exact predicate matches because it:

- weights rare terms more than common terms;
- grades term frequency instead of enforcing brittle all-or-nothing conjunctions;
- normalizes for varying unit lengths; and
- ranks every partially matching candidate rather than discarding it at a hard Boolean boundary.

For conversational memory, BM25 alone is not a modern frontier. It is a minimum baseline. Stronger simple controls include BM25 over multiple retrieval units, BM25 plus local windows, BM25 plus query expansion, lexical-dense fusion, late-interaction scoring, reranking, and budget-aware truncation.

LazyMem's local result is decisive for the current method. Under the same recorded answer model and seed, turn-level BM25 with `k=8` and a `+/-2` local window obtains:

| Method | Answer F1 | BLEU-1 | Judge accuracy | Tokens/query | Evidence recall | Evidence hit rate |
|---|---:|---:|---:|---:|---:|---:|
| BM25-window | 0.5526 | 0.4556 | 0.7864 | 1,974 | 0.742 | 0.803 |
| Current LazyMem compiler | 0.5019 | 0.4110 | 0.7422 | 2,320 | 0.652 | 0.716 |

This table answers the baseline question: there is already an end-to-end BM25 result, and it is better and cheaper. The paper should report it prominently. The compiler should not remain the named core method unless a later frozen experiment reverses the result.

### 4.2 Sparse, dense, and late-interaction retrieval

[DPR](pdfs/2004.04906-dpr.pdf) establishes learned dual-encoder dense retrieval: query and passage vectors make semantic matching efficient but compress each unit into a single vector. [ColBERT](pdfs/2004.12832-colbert.pdf) retains token-level representations and uses late interaction, reducing the information bottleneck of a single pooled vector. [SPLADE v2](pdfs/2109.10086-splade-v2.pdf) learns sparse lexical expansion while retaining inverted-index execution. [BEIR](pdfs/2104.08663-beir.pdf) shows why zero-shot retrieval claims need heterogeneous datasets: retriever rankings change across domains.

Conversational memory introduces a second late-interaction level. A session can be scored by comparing the query against each turn and aggregating the turn scores, instead of embedding the entire session once. Nano-Memory's max-turn score is a simple instance. This distinction matters because "session retrieval" can mean either a session retrieval unit with early pooled representation or a session container scored by its strongest internal turn.

### 4.3 Direct fusion evidence

[Training-Free Lexical-Dense Fusion](pdfs/2606.04194-lexical-dense-fusion.pdf) is the strongest direct control for a simple LazyMem redesign. It fixes the session retrieval unit, separates pooling from retrieval granularity, and evaluates BM25 plus max-turn dense late interaction using a leave-one-conversation-out fusion weight.

On LoCoMo it reports:

| Retrieval method | Hit@1 | Recall@5 | NDCG@5 |
|---|---:|---:|---:|
| BM25 | 0.640 | 0.833 | 0.746 |
| Dense mean-pool | 0.427 | 0.713 | 0.573 |
| Dense max-turn | 0.664 | 0.863 | 0.769 |
| BM25 + dense mean-pool | 0.666 | 0.851 | 0.766 |
| BM25 + dense max-turn | 0.752 | 0.894 | 0.829 |

The best fusion is +11.2 Hit@1 points over BM25 in that protocol. Category analysis shows why: dense late interaction helps most on multi-hop and temporal questions, while BM25 is stronger on adversarial questions; fusion captures complementary errors. On LongMemEval-S, however, BM25 already saturates the lexical regime and the net fusion gain is small and statistically non-significant. This is exactly the conditional-value pattern a lazy system must model.

The paper also reports a useful negative result: adding one off-the-shelf MS MARCO cross-encoder to the fused top-10 reduces Hit@1 from 0.701 to 0.633 in the tested configuration. "Add a reranker" is therefore not an assumption; target-distribution validation is required.

### 4.4 Ranking and packing can dominate candidate generation

SmartSearch uses NER/POS-weighted substring matching for high-recall candidate collection, then fuses a CrossEncoder and ColBERT ranker using reciprocal rank fusion. Its oracle analysis reports that substring matching resolves 98.9% of queries and raw retrieval recall is 98.6%, but without strong ranking only 22.5% of gold evidence survives the effective context position. Its claim is not that lexical search is universally enough. It is that when recall is already saturated, ranking and truncation are the remaining bottlenecks.

This is important for LazyMem because its current compiler changes candidate generation while leaving the stronger alternatives in ranking underexplored. If BM25-window already recalls more gold evidence, spending an LLM call to produce harder lexical predicates attacks the wrong stage.

SmartSearch reports 93.5% LoCoMo accuracy under the EverMemOS protocol, 91.9% under a separate MemOS protocol, and 88.4% on LongMemEval-S. Those numbers must remain within their protocol groups. The more portable evidence is its within-system ablation: ranking accounts for most of its measured improvement, while the index-free and indexed variants are close on LongMemEval-S.

### 4.5 Local windows, turns, sessions, and events

A local window around a lexical anchor is a strong and cheap device because exact hits often occur in a short answer-adjacent turn while the entity, date, or discourse referent appears nearby. It does not imply that two adjacent turns form a semantic pair or one reasoning hop.

This distinction matters for the earlier D0/D1 pair idea. Dataset identifiers such as `D1:8` name a dialogue/session and turn position; they do not encode a reasoning depth. More generally, grouping every two turns into a pair is too coarse as a first-principles model:

- one fact may occupy half a turn or ten turns;
- adjacent turns may be acknowledgements with no independent evidence;
- two-hop evidence may be separated by many sessions;
- a single answer can require three or more supports; and
- annotated supports are not necessarily a minimal sufficient set.

An adjacent two-turn unit is defensible only as a cheap context-window baseline. A pairwise research claim must define pair utility semantically, show that both endpoints are jointly necessary, compare against the same total token budget, and report complete-chain recall rather than ordinary hit rate.

## 5. Query transformation and compiled retrieval

[HyDE](pdfs/2212.10496-hyde.pdf) transforms a query into a hypothetical relevant document for zero-shot dense retrieval. [Query2doc](pdfs/2303.07678-query2doc.pdf) expands queries with LLM-generated text. [RAG-Fusion](pdfs/2402.03367-rag-fusion.pdf) generates multiple queries and fuses their ranked lists. These works establish that LLM-side query transformation is prior art and that the generated representation must be judged by downstream retrieval, not by plausibility.

LazyMem's typed compiler is narrower: it produces must terms, should terms, and an optional speaker constraint for deterministic execution. The audit trail is useful, but the mechanism has three structural risks:

1. Hard conjunction creates catastrophic false negatives when one generated term is absent.
2. The compiler is restricted to question-side wording and therefore may not bridge the vocabulary gap it is paying an LLM to solve.
3. A single compile call is paid for every question even when BM25 is already confident.

The local LoCoMo result shows all three costs in aggregate. A typed trace does not compensate for lower evidence recall. The compiler should be retained as an ablation or debugging interface, not presumed to be the main retrieval path.

A credible compiler experiment must compare at least:

- raw BM25 query;
- deterministic token normalization and entity extraction;
- BM25 with LLM query expansion;
- current Boolean/typed compiler;
- union or score fusion of raw BM25 and compiled candidates; and
- the same choices behind a frozen confidence gate.

Every row must use the same candidate unit, window policy, final token budget, and answer reader. Reporting retrieval-only gains from a larger candidate set is insufficient.

## 6. Adaptivity: routing, escalation, and sufficiency

### 6.1 BM25-first cascades already exist

[AgentIR](pdfs/2605.25092-agentir.pdf) is the most direct collision with "use BM25 by default and run dense retrieval only for difficult queries." It considers BM25, dense retrieval, reciprocal-rank fusion, recency-aware fusion, and runtime selection. Its cascade uses only the BM25 top-k score margin to decide whether to pay the approximately 52 ms dense-channel cost.

AgentIR reports that on a 500-question LongMemEval setting the cascade skips dense retrieval for 63% of queries at parity LLM-judged accuracy, yielding a 2.67x speedup; per-question-type thresholds reach 5.76x under five-fold cross-validation. On LoCoMo, where BM25 is the strongest single system in its setup, the trigger chooses a 100% skip rate and reports +0.089 Hit@5 over the dense path with a 132x latency ratio. The exact engineering scale is not the main LazyMem lesson. The novelty collision is: a confidence-triggered BM25-to-dense cascade, including workload retuning, has already been built and evaluated.

### 6.2 Query-type routing already exists

[SelRoute](pdfs/2604.02431-selroute.pdf) routes queries among lexical, semantic, hybrid, and vocabulary-enriched pipelines based on question type. Its routing can be deterministic from metadata, and it also reports an 83% effective regex-based classifier. It reaches predicted-type Recall@5 of 0.689 and reports that type-aware routing remains useful without a query-time LLM or GPU.

The scientific value is not its absolute Recall@5, which is protocol-sensitive. The value is the demonstrated heterogeneity: near-verbatim single-session questions favor full-text search, while other types benefit from semantic or enriched routes. A LazyMem gate must therefore be compared with query-type routing, not only with an always-on dense baseline.

### 6.3 Evidence-gap control already exists

[EviMem](pdfs/2604.27695-evimem.pdf) evaluates the accumulated evidence set, labels it by sufficiency, diagnoses what is missing, refines the query, and explicitly abstains when the loop cannot close the gap. It reports particularly large gains on multi-hop questions and lower latency than a multi-agent comparator. [MGRetrieval](pdfs/2605.27437-mgretrieval.pdf) similarly uses memory-guided reflective retrieval with sufficiency stopping. [DeferMem](pdfs/2605.22411-defermem.pdf) retrieves broadly and then performs learned query-conditioned evidence distillation.

These works occupy the space of "test an intermediate result, then retrieve again." LazyMem cannot claim that testing a transition result is new. A possible difference would have to lie in the signal, cost, or guarantee: for example, a deterministic evidence-gap certificate that is cheaper and more calibrated than an LLM sufficiency call. That has not yet been demonstrated.

### 6.4 Cheapest-sufficient-evidence routing already exists

[TierMem](pdfs/2602.17913-tiermem.pdf) makes the lazy principle explicit. It queries a summary index first, invokes a router to judge sufficiency, escalates through provenance pointers to immutable raw pages when necessary, and writes back verified information. On LoCoMo it reports accuracy 0.851 versus 0.873 for raw-only while reducing input tokens by 54.1% and latency by 60.7% (3,396 versus 7,398 tokens; 6.76 versus 17.18 seconds).

TierMem differs from a BM25-first design in its cheap tier and write-time summarization, but it owns the broader claim "answer with the cheapest sufficient evidence and escalate when needed." LazyMem can still test whether an even cheaper lexical tier has a better lifecycle Pareto point, but that is an empirical comparison, not a conceptual novelty claim.

### 6.5 Retrieval is not the only control point

[A Control Architecture for Training-Free Memory Use](pdfs/2604.18206-training-free-control.pdf) asks whether retrieved memory should be applied at all. It separates routing, selective acceptance, bank choice, rollback, and retirement under compute-matched controls. Its main gains are on arithmetic rather than conversational memory, so it is not a direct benchmark competitor. Conceptually, however, it exposes a missing counterfactual in most memory studies: a retrieval can be relevant and still harm the answer.

[Self-RAG](pdfs/2310.11511-self-rag.pdf), [FLARE](pdfs/2305.06983-flare.pdf), and [IRCoT](pdfs/2212.10509-ircot.pdf) provide the broader adaptive-RAG lineage. Self-RAG learns retrieval and critique decisions; FLARE triggers retrieval from generation uncertainty; IRCoT interleaves reasoning and retrieval for multi-step questions. A LazyMem cascade belongs to this family and must cite it as such.

[Evoking User Memory](pdfs/2603.09250-recollection-familiarity.pdf) frames retrieval through recollection and familiarity, while [Recursive Language Models](pdfs/2512.24601-recursive-language-models.pdf) let a model programmatically inspect an external long context. Both show that query-time access policies can be richer than a one-shot top-k without modifying the stored record.

## 7. Multi-hop evidence and the pairwise proposal

The first-principles problem is real: under a tight candidate budget, a necessary bridge turn may have weak direct affinity to the query, and its value may become visible only together with another turn. Direct itemwise top-k can discard both before a downstream reasoner can combine them.

However, "score turn pairs" is not yet a complete solution. It raises four identification problems.

### 7.1 What is a positive pair?

LoCoMo gold evidence is a set of annotated turns, not necessarily a minimal proof. If a question has three supports, labeling every within-set pair positive asserts that every pair is sufficient; labeling only adjacent supports injects chronology; selecting one pair manually adds annotation judgment. Singleton questions contribute no positive pair. A pair loss is therefore undefined until minimal sufficiency is operationalized.

### 7.2 Does the pair score model complementarity?

A pair scorer can improve simply by learning two independent relevance scores and adding them. To establish interaction, the experiment needs affinity-matched negative pairs whose individual turn scores match the positive endpoints but whose union is insufficient. It also needs an ablation that removes the cross-turn interaction while preserving parameter count and training data.

### 7.3 Is all-pairs computation solving the actual bottleneck?

If BM25-window already retrieves one or more supports for most questions, iterative expansion from a visible first hop may be cheaper than global pair scoring. SmartSearch, EviMem, DeferMem, MGRetrieval, and IRCoT all exploit this route in different ways. The pair mechanism is justified only on a measured stratum where:

- no productive lexical, dense, entity, or temporal first hop enters the fixed candidate budget;
- at least two low-affinity supports jointly suffice;
- this stratum is large enough to affect end-to-end utility; and
- the proposed method recovers it without losing easier cases or exceeding the cost budget.

### 7.4 Pair-complete packing is separate from pair retrieval

Even a correct pair score can fail if the context packer admits one long endpoint and drops the other. Complete-chain recall under the final token cap, not pre-packing pair Recall@k, is the relevant retrieval metric. Chronological reordering after selection and duplicate local-window removal must also be held fixed.

The pairwise direction should therefore remain a hypothesis, not the next default architecture. The first experiment is a prevalence study: measure the irreducible low-affinity multi-support stratum after BM25-window and lexical-dense fusion. If that stratum is negligible, the pair model should be stopped regardless of synthetic success.

## 8. Novelty audit

The following table distinguishes a useful engineering property from a publishable method claim.

| Candidate LazyMem claim | Closest prior work | Assessment |
|---|---|---|
| Store raw dialogue without lossy write-time extraction | Fidelity Before Structure; Back to Basics; SmartSearch; Eywa; event-memory baseline | Strongly supported, but not novel. |
| No LLM work at ingestion | SmartSearch; Back to Basics; conventional IR baselines | Not novel. Useful lifecycle-cost choice. |
| Deterministic lexical retrieval over raw turns | BM25; SmartSearch; SelRoute | Standard baseline territory. |
| LLM compiles a query into retrieval terms | Query2doc; HyDE; RAG-Fusion; Boolean-query formulation literature | Adjacent prior art; typed trace is an implementation distinction, not yet a validated contribution. |
| BM25 first, semantic fallback on hard queries | AgentIR | Direct collision. |
| Route by question type | SelRoute; AgentIR | Direct collision. |
| Escalate only when evidence is insufficient | EviMem; TierMem; MGRetrieval; adaptive RAG | Direct collision at the conceptual level. |
| Preserve raw source behind cheap derived memory | TierMem; EviMem; Eywa | Direct collision. |
| Rank raw candidates and truncate to budget | SmartSearch; DeferMem; Nano-Memory | Crowded space. |
| Pair every two turns | Local windows and turn/session granularity baselines | Too arbitrary to support a reasoning claim. |
| Query-conditioned global co-support before candidate admission | Adjacent to multi-hop retrieval and pair/listwise ranking; not directly established by the 45-paper conversational-memory corpus | Potentially distinct, but only if interaction, prevalence, cost, and held-out gains are proven. |
| Auditable query compiler plus deterministic executor | SmartSearch, SelRoute, and Eywa are deterministic/auditable in different ways | Possible systems distinction, but current accuracy/cost result is negative. |
| Matched-budget negative result establishing BM25-window as default | Closely aligned with Beyond Memory Leaderboards and Fidelity Before Structure methodology | Potentially publishable as an evaluation/control contribution if broadened and independently validated. |

The honest position today is:

> LazyMem is a minimal experimental baseline for raw, auditable conversational-memory retrieval. Its current compiler does not outperform BM25-window, and its broader lazy-routing principle is shared with recent cascade, routing, and sufficiency-based systems.

That sentence is scientifically stronger than an unsupported novelty claim because it makes the rejected mechanism and remaining burden explicit.

## 9. Recommended experimental program

### 9.1 Freeze the scientific question

The next question should be:

> Under a fixed reader, final context budget, answer prompt, and per-query cost ledger, which additional retrieval operation has positive marginal answer utility beyond BM25-window, and on which query strata does that utility transfer?

Do not begin with an architecture. Begin with intervention value.

### 9.2 Baseline ladder

Use a cumulative ladder where each row changes one factor:

| ID | Candidate generation | Ranking | Control | Purpose |
|---|---|---|---|---|
| B0 | BM25 turn | BM25 | always | Minimum lexical floor. |
| B1 | BM25 turn | BM25 | always | Add fixed local window; current strongest local baseline. |
| B2 | BM25 session/max-turn variants | BM25 | always | Separate unit and interaction effects. |
| B3 | Dense max-turn | dense | always | Measure semantic-only complement. |
| B4 | BM25 union dense | calibrated score fusion or RRF | always | Strong training-free hybrid. |
| B5 | Raw BM25 union compiled terms | same as B1 | always | Test whether the compiler adds candidates without replacing good lexical evidence. |
| B6 | B4 | same | BM25-margin cascade | AgentIR-style cost control. |
| B7 | Best fixed retriever | same | query-type router | SelRoute-style heterogeneity control. |
| B8 | Best fixed retriever | same | evidence-sufficiency retry | EviMem/MGRetrieval-style iterative control. |
| B9 | Best fixed retriever | pair/listwise packer | frozen | Test evidence assembly without changing candidate recall. |
| B10 | Global co-support candidate model | pair-complete packer | frozen | Only after the low-affinity chain stratum is established. |

The current compiler-only system belongs below B5 because it replaces rather than safely augments the stronger lexical route.

### 9.3 Metrics

Report four metric families.

**Answer utility**

- exact or token F1 as appropriate;
- a locked LLM judge with a published rubric;
- abstention accuracy and calibration;
- per-category results with paired confidence intervals.

**Evidence restoration**

- any-evidence hit rate;
- micro and macro evidence recall;
- complete-support-set recall under the final token budget;
- first-hop and later-hop recall;
- gold rank before and after reranking;
- evidence density in the final context.

**Cost**

- write-time calls/tokens and amortization assumption;
- query-time calls/tokens;
- reader input tokens;
- CPU/GPU latency distributions, not only means;
- index bytes and update cost.

**Control quality**

- fallback invocation rate;
- fallback help, hurt, and no-change counts relative to cheap-only;
- selective risk versus coverage;
- oracle intervention value;
- routing regret relative to the per-query best route.

### 9.4 Data discipline

LoCoMo should remain development-only because the current project has already inspected and optimized against it. Hyperparameters, prompts, routing thresholds, and stopping rules must be frozen before LongMemEval or another held-out suite is opened. If LongMemEval has also influenced design, create a new untouched split or report the work explicitly as exploratory.

Use conversation-level, not question-level, cross-validation for any fusion weight or router threshold. Question-level folds leak conversation-specific vocabulary and entity distributions.

### 9.5 Kill criteria

Stop the compiler if its union with BM25 does not improve paired answer utility after its extra call and tokens are priced.

Stop the cascade if the confidence signal cannot separate helpful from harmful fallback interventions on held-out conversations.

Stop the pair mechanism if fewer than a pre-registered fraction of questions require low-affinity multi-support retrieval after the strong hybrid baseline, or if complete-chain recall improves without downstream answer utility.

Stop any complexity increase that is Pareto-dominated by BM25-window or lexical-dense fusion on answer quality, calls, tokens, and latency.

## 10. Paper-facing related-work structure

The paper should organize prior work by scientific decision rather than by product:

1. **Representation fidelity:** structured memory is useful, but controlled evidence favors retaining verbatim sources.
2. **Retrieval floor:** BM25-window is the minimum; dense late interaction and fusion define stronger simple controls.
3. **Query-time computation:** query expansion is established, and the current typed compiler is a negative result.
4. **Adaptive control:** cascades, type routing, sufficiency loops, and tier escalation already cover the broad lazy-computation claim.
5. **Evaluation:** matched readers, budgets, evidence metrics, and lifecycle costs are required before architectural attribution.

The Related Work section should explicitly state that LazyMem does not claim novelty for raw storage, BM25-first retrieval, or conditional escalation. If the paper remains centered on the compiler, it must say that the current experiment rejects the mechanism and frame the paper as a transparent negative result or work in progress.

## 11. Microsoft ResearchStudio rerun

The initial synthesis was re-audited on 2026-07-27 with the Microsoft ResearchStudio `paper-search`, `scoop-check`, and `idea-spark` workflows. The independent run artifacts are under [`researchstudio-rerun/`](researchstudio-rerun/). They preserve the raw multi-source output, all 53 API records without relevance filtering, a 58-record abstract triage after adding five verified core papers, and the seven-paper full-text novelty audit.

### 11.1 Search coverage and failure disclosure

Three searches covered budgeted conversational memory, BM25/dense routing, and evidence-sufficiency iteration across arXiv, DBLP, OpenAlex, OpenReview, Semantic Scholar, and Crossref. OpenAlex and Crossref returned 60 source records, yielding 53 unique records after merging seven duplicates. DBLP returned no records. arXiv and Semantic Scholar were rate-limited for all three queries; two OpenReview requests were rate-limited; OpenAlex recovered from intermittent 504 responses. These failures are retained in [`allinone.md`](researchstudio-rerun/allinone.md) and the raw error logs rather than silently replaced with model recall.

Five load-bearing papers missed by the API run were added only after their official arXiv PDFs were verified: AgentIR, SelRoute, EviMem, TierMem, and Training-Free Lexical--Dense Fusion. S2G-RAG was obtained from ACL and inspected in full. The official PGR preprint endpoint returned HTTP 403 after DOI resolution and user-agent retries, so its record remains explicitly abstract-only.

### 11.2 Four-axis scoop result

The audit used four axes: (1) budgeted evidence restoration, (2) a cheap lexical path with conditional semantic work, (3) positive marginal downstream value as the reason to spend that work, and (4) long-term conversational memory.

| Work | Problem | Core mechanism | Value insight | Domain | Verdict |
|---|---:|---:|---:|---:|---|
| AgentIR | match | match | match | match | Level 1, direct collision |
| TARG | match | partial | match | different | Level 2, reader-logit gate in general QA |
| SelRoute | match | match | match | match | Level 1 at routing-principle level |
| EviMem | match | partial | match | match | Level 2, structured multi-call gap loop |
| TierMem | match | partial | match | match | Level 2, summary-to-raw trained routing |
| Lexical--Dense Fusion | match | different | match | match | Level 2, always-on operation boundary |
| PGR | match | partial | match | unverified | Level 2 provisional, abstract only |
| S2G-RAG | match | partial | match | different | Level 2, general-QA sufficiency loop |

The overall verdict is **Level 1 full overlap** for the broad redesign claim. AgentIR already runs BM25 first, uses the top-score margin to gate dense/fusion escalation, and chooses answer-preserving operating points in the same domain. A generic “BM25 first, semantic retrieval only when useful” claim is therefore not available to LazyMem.

IdeaSpark's independent map search also surfaced TARG (*Retrieval as a Decision*, TMLR 2026), which was absent from the original frozen corpus. TARG makes one training-free retrieve-or-skip decision from a short no-context draft using reader-prefix entropy, top-logit margin, or stochastic-prefix variance. It reports roughly 50 ms overhead for a 20-token prefix and 70--90% fewer retrievals over five general-QA datasets while matching or improving always-retrieve EM/F1. Section 3.3 already defines paired with/without-RAG correctness difference and a usefulness-calibration assumption; Appendix A.7 measures uncertainty/benefit error quadrants. Its domain differs from LazyMem, but it blocks both generic reader-confidence gating and paired answer-change analysis as novelty escapes.

### 11.3 New evidence from S2G-RAG

S2G-RAG is important because it closes a different escape route: structured sufficiency and gap judging is already an accepted ACL 2026 mechanism. Its fine-tuned judge emits a binary sufficiency decision and structured missing-evidence items; BM25 or E5 retrieves another round; an LLM sentence-pointer extractor retains compact evidence. Under a matched BM25 retriever budget and answer reasoner on HotpotQA, the full method reports 43.3 EM / 56.5 F1. Removing the judge drops performance to 27.5/37.6; removing the extractor gives 39.5/52.5. The sufficiency false-positive rate is 6.44%, but 31.60% of actually sufficient states are classified insufficient, revealing conservative over-retrieval.

The cost evidence is equally important. S2G-RAG reports 1.6085 seconds per question versus 0.3787 for standard RAG; its extractor improves the iterative no-extractor variant at 1.9552 seconds but does not make the controller cheap. Its 4.5x--6.4x context compression therefore should not be confused with end-to-end savings. The method is also trained from teacher-labelled process traces and evaluates open-domain QA rather than persistent conversational memory.

### 11.4 Surviving hypothesis, not current novelty

The only plausible remaining distinction is narrower: directly predict **cost-adjusted intervention value for one fixed semantic operation** rather than threshold retrieval confidence or reader uncertainty, and demonstrate that the policy transfers across conversational-memory corpora. For a fixed BM25-window result, compare the answer obtained without and with one semantic operation, then price the attributable answer change against extra reader context, calls, tokens, and latency. A gate would run the operation only when a calibrated lower confidence bound on net utility is positive.

This distinction is scientifically meaningful because a low BM25 score margin can still produce answer-sufficient evidence, while a high margin can confidently rank an incomplete evidence chain; likewise, reader uncertainty need not equal the treatment effect of the proposed evidence. It is not yet a LazyMem contribution, and TARG plus broader utility/policy-learning ancestors mean it is not yet cleared as novel. It needs a focused collision search and must beat AgentIR-style retrieval-margin gating, TARG-style reader-uncertainty gating, SelRoute-style type routing, always-on fusion, and random matched-rate escalation under the same reader, retrieval candidates, context budget, call budget, and held-out protocol. The complete falsification design and kill criteria are in [`step7.md`](researchstudio-rerun/step7.md).

## 12. Corpus catalog

### Benchmarks and evaluation

| Work | Role in this review |
|---|---|
| [LoCoMo](pdfs/2402.17753-locomo.pdf) | Primary long-conversation QA benchmark with evidence annotations. |
| [LongMemEval](pdfs/2410.10813-longmemeval.pdf) | Multi-session capability taxonomy and longer-context transfer target. |
| [MemTrace](pdfs/2606.17328-memtrace.pdf) | Separates retrieval, evidence use, and final-answer failure. |
| [MemOps](pdfs/2607.12893-memops.pdf) | Evaluates memory lifecycle operations beyond recall QA. |
| [RUMBA](pdfs/2607.21447-rumba.pdf) | Tests multilingual, temporal, and session-scope behavior. |
| [Beyond Memory Leaderboards](pdfs/2607.16848-budgeted-context-restoration.pdf) | Centers matched-budget context restoration and architecture-independent controls. |
| [MEMAUDIT](pdfs/2605.02199-memaudit.pdf) | Isolates memory-writing quality from retriever and reader confounds. |

### Memory architectures

| Work | Role in this review |
|---|---|
| [MemGPT](pdfs/2310.08560-memgpt.pdf) | Canonical hierarchical context and external-memory architecture. |
| [Mem0](pdfs/2504.19413-mem0.pdf) | Production extraction, consolidation, update, and retrieval. |
| [A-MEM](pdfs/2502.12110-a-mem.pdf) | Dynamic linked-note construction and associative retrieval. |
| [Zep](pdfs/2501.13956-zep.pdf) | Temporal knowledge-graph memory. |
| [EverMemOS](pdfs/2601.02163-evermemos.pdf) | Multi-tier structured memory and long-horizon comparison point. |
| [Hindsight](pdfs/2512.12818-hindsight.pdf) | Evidence, experience, belief, and reflection organization. |
| [ENGRAM](pdfs/2511.12960-engram.pdf) | Lightweight typed episodic, semantic, and procedural memory. |
| [HingeMem](pdfs/2604.06845-hingemem.pdf) | Event boundaries plus query-adaptive route and retrieval depth. |
| [PRISM](pdfs/2605.12260-prism.pdf) | Intent-aware structured retrieval evaluated on a cost frontier. |
| [GRAVITY](pdfs/2605.01688-gravity.pdf) | Generation-time relational, temporal, and topical anchoring. |

### Raw-history and conversational retrieval

| Work | Role in this review |
|---|---|
| [SmartSearch](pdfs/2603.15599-smartsearch.pdf) | Raw deterministic recall, learned rank fusion, and budget truncation; closest ranking baseline. |
| [AgentIR](pdfs/2605.25092-agentir.pdf) | Direct BM25-confidence cascade and workload-adaptive fusion collision. |
| [Lexical-Dense Fusion](pdfs/2606.04194-lexical-dense-fusion.pdf) | Controlled BM25/max-turn dense fusion and cross-corpus boundary. |
| [Back to Basics](pdfs/2604.11628-back-to-basics.pdf) | Minimal retrieval-generation design with turn isolation and query-driven pruning. |
| [SelRoute](pdfs/2604.02431-selroute.pdf) | Query-type routing among lexical, semantic, hybrid, and enriched paths. |
| [EviMem](pdfs/2604.27695-evimem.pdf) | Evidence-gap diagnosis, query refinement, and abstention. |
| [TierMem](pdfs/2602.17913-tiermem.pdf) | Cheapest-sufficient tier selection with provenance-linked raw escalation. |
| [Fidelity Before Structure](pdfs/2601.00821-fidelity-before-structure.pdf) | Controlled evidence that verbatim chunks can beat lossy typed artifacts. |
| [Simple Event-Memory Baseline](pdfs/2511.17208-event-memory-baseline.pdf) | Minimally compressive event units and simple dense retrieval. |
| [DeferMem](pdfs/2605.22411-defermem.pdf) | High-recall raw retrieval followed by learned evidence distillation. |
| [MGRetrieval](pdfs/2605.27437-mgretrieval.pdf) | Reflective, memory-guided retrieval with sufficiency stopping. |
| [Eywa](pdfs/2605.30771-eywa.pdf) | Immutable evidence, derived facts, provenance, and deterministic multi-route retrieval. |
| [ConvMemory](pdfs/2605.28062-convmemory.pdf) | Lightweight lexical-dense reranking and attribution/conflict controls. |
| [EAR](pdfs/2607.17879-ear.pdf) | Iterative reflective recall and experience-driven reranker adaptation. |
| [Memory-T1](pdfs/2512.20092-memory-t1.pdf) | Reinforcement learning for temporal retrieval and reasoning. |
| [Training-Free Control](pdfs/2604.18206-training-free-control.pdf) | Routing, acceptance, rollback, bank selection, and governance as a control problem. |
| [Evoking User Memory](pdfs/2603.09250-recollection-familiarity.pdf) | Recollection/familiarity view of adaptive personal-memory retrieval. |
| [Recursive Language Models](pdfs/2512.24601-recursive-language-models.pdf) | Programmatic query-time inspection of long external contexts. |

### IR foundations

| Work | Role in this review |
|---|---|
| [DPR](pdfs/2004.04906-dpr.pdf) | Dense dual-encoder baseline. |
| [ColBERT](pdfs/2004.12832-colbert.pdf) | Token-level late interaction and a strong reranking primitive. |
| [SPLADE v2](pdfs/2109.10086-splade-v2.pdf) | Learned sparse expansion beyond exact lexical matching. |
| [BEIR](pdfs/2104.08663-beir.pdf) | Heterogeneous zero-shot retrieval evaluation. |

### Query transformation

| Work | Role in this review |
|---|---|
| [HyDE](pdfs/2212.10496-hyde.pdf) | LLM-generated hypothetical document for zero-shot retrieval. |
| [Query2doc](pdfs/2303.07678-query2doc.pdf) | LLM query expansion directly adjacent to compiled predicates. |
| [RAG-Fusion](pdfs/2402.03367-rag-fusion.pdf) | Multi-query generation and reciprocal-rank fusion. |

### Adaptive retrieval

| Work | Role in this review |
|---|---|
| [Self-RAG](pdfs/2310.11511-self-rag.pdf) | Learned retrieval, generation, and evidence critique. |
| [FLARE](pdfs/2305.06983-flare.pdf) | Generation-uncertainty-triggered retrieval. |
| [IRCoT](pdfs/2212.10509-ircot.pdf) | Interleaved reasoning and retrieval for multi-step evidence. |

## 13. Final position

The literature does not say "complex memory is unnecessary." It says something more precise:

- raw evidence is a strong and often undercontrolled baseline;
- write-time structure must justify its fidelity loss;
- BM25 is unusually strong on some conversational-memory regimes;
- dense retrieval is complementary on some query categories and redundant on others;
- candidate recall, ranking, packing, evidence sufficiency, and memory application are distinct bottlenecks; and
- any added mechanism must be evaluated as a conditional intervention under matched budgets.

That is the first-principles foundation LazyMem should adopt. The current name can still fit: "lazy" should mean measured deferral of cost until evidence shows it is useful, not simply moving an unconditional LLM call from write time to query time.

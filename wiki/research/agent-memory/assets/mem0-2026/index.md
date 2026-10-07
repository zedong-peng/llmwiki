---
title: Mem0 2026 — software release, algorithm article, and evaluation
domain: research
area: agent-memory
type: engineering
status: active
updated: 2026-09-20
tags: [mem0, agent-memory, retrieval, evaluation, locomo]
---

# Mem0 2026

**The new algorithm has public source code, but the headline results describe the managed platform.** The public SDK implements ADD-only extraction and hybrid retrieval; platform-only features remain. The public benchmark repository also contains prompts and saved judgments, although its committed result files do not match its latest headline table.

This reference covers the [April 16 release article](https://mem0.ai/blog/mem0-the-token-efficient-memory-algorithm), updated July 10, and the source snapshots checked on September 18, 2026. Keep it distinct from the [2025 Mem0 paper](../mem0-2025/index.md). Pipeline “v3” is the algorithm terminology; the selected Python package is **mem0ai 2.1.0**.

## Citation identity

This is the independent **Mem0 2026 software / technical release** entry, not a second paper entry or an update to the 2025 paper's reported scores. No corresponding new research paper has been established by the archived sources.

| Claim being cited | Source to cite |
|---|---|
| New algorithm description or vendor-reported platform results | Official article, *The Token-Efficient Memory Algorithm*, published 2026-04-16, updated 2026-07-10 |
| OSS implementation used in an experiment | `mem0ai/mem0`, SDK v2.1.0 and its pinned commit |
| New answer-generation or judge rules | `mem0ai/memory-benchmarks`, pinned commit and `benchmarks/locomo/prompts.py` |
| 2025 method, paper scores, or original RAG baseline | Separate [Mem0 2025 paper and experiment-code entry](../mem0-2025/index.md) |

Reusable, separately keyed entries are in [citations.bib](citations.bib). For a Mem0 2026 method row, cite the article plus the actual implementation version; the evaluation-repository citation alone supports evaluator behavior, not all algorithm claims.

The April 2026 `memory-benchmarks` snapshot physically retained under the [legacy 2025 directory](../../papers/mem0-2025/repo/memory-benchmarks/) belongs to this newer evaluator lineage. Its path is preserved, with metadata explicitly marking that attribution. It must not be used as the 2025 paper's prompt source.

## Public sources

| Artifact | Archived revision | Local source |
|---|---|---|
| [mem0ai/mem0](https://github.com/mem0ai/mem0) | `v2.1.0`, `19f713408273fb1d657daa38d7b82ccf496d36d5` | [SDK](github-repo/mem0/) |
| [mem0ai/memory-benchmarks](https://github.com/mem0ai/memory-benchmarks) | `4b61c5d31b9c668a12b4f5e78064248a02c82d2b` | [Evaluation source and results](github-repo/memory-benchmarks/) |

Both repositories use Apache-2.0. The SDK's `evaluation` submodule points to the same benchmark commit; that repository is cached separately above. These are independent local Git clones, excluded from the parent wiki Git. Revisions, asset hashes, inspection scope, and download provenance are in [metadata.yaml](metadata.yaml).

The [article HTML](supplementary/algorithm-blog.html), [readable article text](supplementary/algorithm-blog.txt), [migration page](supplementary/oss-v2-to-v3.html), [release feed](supplementary/mem0-releases-atom.xml), and [PyPI metadata](supplementary/pypi-mem0ai.json) are also archived. PyPI and the release feed identify Python SDK 2.1.0 as released on September 18. This is a software/blog reference, not an archive of a new 2026 paper.

## What the code implements

- **Single-pass ADD-only extraction.** The normal inferred-add path supplies recent messages and retrieved existing memories to one extraction call, embeds new facts, deduplicates exact text, and stores ADD events. The [extraction prompt](github-repo/mem0/mem0/configs/prompts.py) explicitly covers both user and assistant messages. ADD-only refers to this extraction path; it does not imply the entire API cannot delete or modify data.
- **Entity and keyword signals.** The [memory implementation](github-repo/mem0/mem0/memory/main.py) stores lemmatized text and embeds entities linked to memories. Search retrieves a semantic candidate pool and ranks those candidates using semantic similarity, normalized keyword/BM25 scores, and entity boosts; see [scoring.py](github-repo/mem0/mem0/utils/scoring.py). Keyword-only candidates are not independently unioned into the final pool in this inspected path.
- **Platform boundary.** The [migration guide](github-repo/mem0/docs/migration/oss-v2-to-v3.mdx) says graph memory has moved to the platform. The SDK explicitly rejects the platform temporal parameters `timestamp` on add and `reference_date` on search. Retaining dates and accumulating facts in OSS should not be confused with having the platform's full temporal-reasoning implementation.

For our research, ADD-only storage supports the motivation to preserve changing facts, but **preserving extracted facts is still different from preserving the original conversation**: extraction can omit information. That is a useful design distinction, not evidence that either system is more accurate.

## Results and evaluator

The article reports single-call retrieval at top-200 and explicitly attributes the following scores to the managed platform, including proprietary optimizations. The context-token numbers below also come from that article, not from a local run.

| Benchmark | Current headline score | Reported context tokens/query | Committed top-200 judgments, counted locally |
|---|---:|---:|---:|
| LoCoMo | 92.5% | 6,956 | 1,410 / 1,540 = **91.56%** |
| LongMemEval | 94.4% | 6,787 | 467 / 500 = **93.4%** |

Evidence: [benchmark README](github-repo/memory-benchmarks/README.md), [LoCoMo result file](github-repo/memory-benchmarks/results/platform/locomo_results.json), and [LongMemEval result file](github-repo/memory-benchmarks/results/platform/longmemeval_results.json). Recounting saved labels is an artifact check, not a new evaluation. The earlier wiki's 91.6 / 93.4 values match these older result files and remain in the migration guide. The latest README instead lists 1,425 / 1,540 and 472 / 500. Its top-50 claims also differ: LoCoMo 91.8% versus 82.66% in the saved file; LongMemEval 94.8% versus 90.4%. The inspected files therefore do not substantiate the newer headline table.

The article additionally reports BEAM 1M / 10M scores of 64.1 / 48.6; the repository identifies these as scaled average scores, separate from its binary pass rates.

The current [LoCoMo runner](github-repo/memory-benchmarks/benchmarks/locomo/run.py) and [prompts](github-repo/memory-benchmarks/benchmarks/locomo/prompts.py) differ materially from the 2025 paper protocol:

| Component | Observed 2026 behavior |
|---|---|
| Population | All 10 conversations; categories 1–4; 1,540 saved questions. README prose saying “~300” is stale. |
| Models | CLI defaults to GPT-5 for answerer and judge; saved LoCoMo metadata also says GPT-5 for both. README flag documentation still says GPT-4o. |
| List answers | At least one correct item receives a binary CORRECT verdict, even if other requested items are absent. |
| Time answers | Dates within 14 days and durations within 50% are accepted. |
| Identity/detail | Same referent and extra detail receive broad allowances. |
| Optional evidence | `--with-evidence` supplies gold-linked conversation evidence to the judge and says to use it only to accept additional answers. Both saved LoCoMo files record `with_evidence: false`. |

The judge receives no method name, so these rules are not evidence of explicit architecture favoritism. They do favor certain answer properties, including incomplete lists and approximate time estimates. Their effect on rankings requires a comparison; a newer release alone does not justify adopting the rubric. The repository does not establish that today's exact prompt produced every archived judgment. For a matched comparison, hold the question set, answer model, judge model, rubric, evidence setting, and token accounting fixed across methods. Keep 2026 vendor-reported scores separately labeled until then; the shared protocol selected on September 20 is recorded below.

## Reproduction status

Source and artifacts were downloaded and inspected. No dependencies were installed, no downloaded code was executed, and no inference was run.

The benchmark Docker requirements still install `mem0` from `feat/v3-pipeline`; an exact remote-ref lookup returned no such public branch on September 18. Its wrapper also passes older `limit` and top-level `user_id` search arguments, while SDK 2.1.0 expects `top_k` and IDs inside `filters`. A reproduction must resolve that dependency/API mismatch. Hybrid search also requires its optional NLP/backend dependencies: spaCy for entity extraction/lemmatization and `fastembed` for Qdrant BM25. Downloaded source should not be described as a verified runnable reproduction.

Earlier context: [April benchmark decision](../../threads/2026-04-23-mem0-new-algorithm-benchmark-decision.md).

## Shared experiment protocol decision (2026-09-20)

**Identity:** use the distinct `Mem0 2026` reference label for this software/blog release and its standalone `mem0ai/memory-benchmarks` repository; do not attribute these evaluator rules to the 2025 paper. Existing archived clones already contain the inspected commit, so no duplicate archive was created.

**Code observations:** the answer formatter consumes `memory` / `created_at` records, sorts up to 200 memories chronologically, and can prepend a user profile. The answer prompt mandates seven reasoning steps and fixes event years to 2022–2024. The judge allows one correct list item, ±14 days for dates, and ±50% for durations; optional evidence can only broaden acceptance. See [the pinned prompt source](https://github.com/mem0ai/memory-benchmarks/blob/4b61c5d31b9c668a12b4f5e78064248a02c82d2b/benchmarks/locomo/prompts.py) and [local source](github-repo/memory-benchmarks/benchmarks/locomo/prompts.py).

**Decision for Evolving Memory:** use official LoCoMo data, Mem0 2025 answer/judge prompts, and `gpt-5.6-luna` (non-reasoning) for experiment model calls, answering and judging. Keep Mem0 2025 and Mem0 2026 as separate method rows under that same evaluator. Table 1 is a blank ten-method experiment template; all measurements remain pending.

**Interpretation:** the 2026 pipeline is tailored to retrieved memories and this benchmark. Its changed acceptance criteria are a concrete reason to keep the shared protocol fixed. This does not demonstrate architecture favoritism: method identity is absent from the judge input, the judge can be reused independently, and the 2025 rubric is also generous. No new inference, ranking comparison, or reproduction was performed.

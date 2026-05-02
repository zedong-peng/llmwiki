---
title: BEIR Current SOTA Snapshot
domain: research
area: misc
type: note
status: active
updated: 2026-04-21
tags: [research-thread, beir, retrieval, leaderboard, sota, bm25, splade, reranking, embeddings]
---
# BEIR Current SOTA Snapshot

## Context

This note answers a practical question: what counts as the "current SOTA" on BEIR right now?

That question turns out to be ambiguous because there are at least two different notions in circulation:
- the **official public BEIR leaderboard** on EvalAI
- more recent **model-card or paper claims** that report stronger BEIR averages but are not visible as current public EvalAI submissions
- the newer **MTEB retrieval framing**, where BEIR is treated as part of a broader embedding benchmark family

This page records the current official snapshot and the discrepancy.

## Key Judgments

1. If "SOTA" means the **current public official BEIR leaderboard on EvalAI**, the top public entry I could verify on **2026-04-19** is:
   - team: `nle`
   - method: `(BM25+SPLADE) RANKT5 top 50`
   - Avg nDCG@10: **0.5525**
   - submission date: **2023-01-28**

2. The top two public entries on the official leaderboard are both **hybrid / reranking-heavy** systems, not plain dense embedding retrievers:
   - `nle` — `(BM25+SPLADE) RANKT5 top 50` — **0.5525**
   - `ZA+NM+Unicamp` — `InParsv2` — **0.5457**

3. The official public leaderboard appears **stale** relative to 2024-2025 embedding-model discussion.
   Evidence:
   - the best public submissions visible today are from **January-February 2023**
   - the challenge metadata fetched on **2026-04-19** shows the challenge as **inactive** and **frozen**

4. If "SOTA" means the **best recent BEIR average reported in current model cards**, the strongest number I could verify from primary-source model cards is:
   - `OpenAI text-embedding-3-large` — **55.43** average nDCG@10
   from the comparison table in MongoDB's `mdbr-leaf-ir` model card.

5. For **compact open models**, MongoDB's September 2025 model card claims the current best ≤100M-parameter result is:
   - `mdbr-leaf-ir (asym.)` — **54.03**
   - `mdbr-leaf-ir` — **53.55**
   and explicitly says it is `#1` on the public BEIR leaderboard **for models with ≤100M parameters**.

6. Therefore the safest answer is:
   - **official public BEIR leaderboard leader**: `(BM25+SPLADE) RANKT5 top 50` at **55.25 nDCG@10**
   - **strongest newer model-card-reported BEIR average I could verify**: `text-embedding-3-large` at **55.43**
   - these are close numerically, but they come from **different evidence channels**

7. There is now a third practical framing:
   - BEIR remains the canonical 18-dataset retrieval benchmark
   - but current embedding comparisons increasingly surface those datasets through **MTEB retrieval**
   - so "current BEIR leaderboard" and "current retrieval leaderboard in practice" are no longer the same question

## Definitions / Clarifications

### Official leaderboard SOTA

This means: the highest public score returned by the current official EvalAI leaderboard API for BEIR.

That is the most conservative definition because it is directly tied to the official benchmark host.

### Reported model-card SOTA

This means: a recent model card or paper reports a BEIR average score and positions the model as state-of-the-art.

This can be useful for current practice, but it is weaker evidence than a visible official leaderboard row unless the underlying run is also publicly inspectable on the benchmark host.

### MTEB retrieval framing

This means: use MTEB as the broader benchmark surface, and interpret BEIR as one important retrieval subset inside it.

This is not a claim made by the 2021 BEIR paper itself. It is a later ecosystem framing supported by:
- the 2026 AILog BEIR update page
- the official MTEB project and task documentation

## Official Leaderboard Snapshot

Official source:
- EvalAI challenge metadata for `BEIR - Benchmarking IR`: `https://eval.ai/api/challenges/challenge/1897`
- phase list: `https://eval.ai/api/challenges/challenge/1897/challenge_phase`
- phase split list: `https://eval.ai/api/challenges/1897/challenge_phase_split`
- leaderboard JSON: `https://eval.ai/api/jobs/challenge_phase_split/4475/leaderboard/`

Relevant challenge facts verified on **2026-04-19**:
- challenge id: `1897`
- title: `BEIR - Benchmarking IR`
- official metric: **nDCG@10**
- challenge phase id: `3783`
- leaderboard split id: `4475`
- challenge status: `is_active: false`
- challenge status: `is_frozen: true`

### Top Public Official Entries

| Rank | Team | Method | Avg nDCG@10 | Submission Date |
|---|---|---|---:|---|
| 1 | `nle` | `(BM25+SPLADE) RANKT5 top 50` | **0.5525** | 2023-01-28 |
| 2 | `ZA+NM+Unicamp` | `InParsv2` | **0.5457** | 2023-01-12 |
| 3 | `MetaAI+UW*2` | `DRAGON+` | **0.4740** | 2023-02-13 |
| 4 | `BEIR` | `SPLADE` | **0.4740** | 2022-12-22 |
| 5 | `BEIR` | `BM25 multifield` | **0.4288** | 2022-12-22 |

### What This Means

- The official public leaderboard is still topped by a **hybrid lexical+sparse+rereanking** setup rather than a single modern dense embedding model.
- The margin between rank 1 and rank 2 is modest: **0.5525 vs 0.5457**.
- The leaderboard is not currently showing the wave of newer API embedding models discussed in 2024-2025.

## Newer Model-Card Evidence

Primary source:
- MongoDB `mdbr-leaf-ir` model card: `https://huggingface.co/MongoDB/mdbr-leaf-ir`

Verified on **2026-04-19**, the model card lists the following BEIR average nDCG@10 comparison:

| Model | Size | BEIR Avg. (nDCG@10) |
|---|---|---:|
| `OpenAI text-embedding-3-large` | Unknown | **55.43** |
| `mdbr-leaf-ir (asym.)` | 23M | **54.03** |
| `mdbr-leaf-ir` | 23M | **53.55** |
| `snowflake-arctic-embed-s` | 32M | 51.98 |
| `bge-small-en-v1.5` | 33M | 51.65 |
| `OpenAI text-embedding-3-small` | Unknown | 51.08 |
| `granite-embedding-small-english-r2` | 47M | 50.87 |
| `SPLADE++` | 110M | 48.88 |
| `BM25` | – | 41.14 |

The same model card explicitly states:
- `mdbr-leaf-ir` is `#1 on the public BEIR benchmark leaderboard for models with ≤100M parameters`

## Why The Two Views Differ

The discrepancy is most likely due to one or more of the following:
- the official public EvalAI leaderboard is no longer actively receiving or displaying newer public runs
- some newer model comparisons are reproduced locally against BEIR rather than submitted as public EvalAI leaderboard entries
- some claims refer to a restricted slice such as **compact models**, not the unrestricted overall leaderboard
- some current retrieval discussions have implicitly shifted from standalone BEIR governance to MTEB retrieval model comparison

This is an inference from the sources, not something the benchmark maintainers explicitly state.

## Practical Answer

If I need one short answer for conversation, I should say:

- **Official public BEIR leaderboard leader as of 2026-04-19**: `(BM25+SPLADE) RANKT5 top 50` with **55.25 nDCG@10** on the EvalAI BEIR leaderboard.
- **Best newer BEIR average I could verify from a primary-source model card**: `OpenAI text-embedding-3-large` with **55.43 nDCG@10**.
- **Best compact open model claim I could verify**: `mdbr-leaf-ir (asym.)` with **54.03 nDCG@10**, claimed #1 for models ≤100M.
- **Best 2026 framing**: use BEIR when discussing the original retrieval benchmark and frozen EvalAI board; use MTEB when discussing the broader current embedding leaderboard landscape.

## References / Evidence

- Official BEIR paper note: [[../papers/beir-2021]]
- AILog BEIR update page: `https://app.ailog.fr/en/blog/news/beir-benchmark-update`
- Official MTEB project: `https://github.com/embeddings-benchmark/mteb`
- Official MTEB retrieval task page: `https://embeddings-benchmark.github.io/mteb/overview/available_tasks/retrieval/`
- BEIR EvalAI challenge metadata: `https://eval.ai/api/challenges/challenge/1897`
- BEIR phase list: `https://eval.ai/api/challenges/challenge/1897/challenge_phase`
- BEIR phase split list: `https://eval.ai/api/challenges/1897/challenge_phase_split`
- BEIR leaderboard JSON: `https://eval.ai/api/jobs/challenge_phase_split/4475/leaderboard/`
- MongoDB model card: `https://huggingface.co/MongoDB/mdbr-leaf-ir`

## Next Steps

1. If I care about **official benchmark governance**, use the EvalAI leaderboard result and explicitly note that the public board looks frozen.
2. If I care about **current practical embedding quality**, compare recent dense models separately from the old public board.
3. For future local notes, maintain two labels instead of one:
   - `official-public-leaderboard`
   - `recent-reported-best`

---
title: "LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory"
domain: research
area: misc
type: paper
status: processed
updated: 2026-04-29
tags: [paper, benchmark, long-term-memory, chat-assistants, rag, retrieval, iclr-2025]
---

# LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory

## Paper Meta
- Authors: Di Wu, Hongwei Wang, Wenhao Yu, Yuwei Zhang, Kai-Wei Chang, Dong Yu
- Year: 2025
- Venue: not explicitly reported in the extracted text; the source uses an `iclr2025_conference` template
- arXiv: https://arxiv.org/abs/2410.10813
- PDF: `longmemeval-2410.10813.pdf`
- Code repo: https://github.com/xiaowu0162/LongMemEval
- Reading source: TeX/source
- Repo read: yes, but the local checkout is only a placeholder README plus requirements files
- PDF fallback: not used
- Legacy note: [[agent-memory/papers/longmemeval-2025]]

## TL;DR
- LongMemEval is a 500-question benchmark for long-term interactive memory in chat assistants.
- It covers five memory abilities: information extraction, multi-session reasoning, knowledge updates, temporal reasoning, and abstention.
- The benchmark scales histories to 50k sessions overall, with standard settings of about 115k tokens/question and 1.5M tokens/question.
- The paper argues that memory systems need better indexing, retrieval, and reading, not just longer context windows.

## Problem
- Existing long-term memory benchmarks covered only part of the problem space, especially for sustained personal chat.
- The paper targets realistic assistant memory: recording, recalling, updating, and reasoning over user information that evolves across sessions.
- The benchmark is designed to make simple retrieval insufficient by embedding evidence across multiple sessions and long histories.

## Evaluation Settings

**LongMemEval-S**: ~115k tokens/question, ~50 sessions. Standard shorter setting used for long-context LLM comparisons.

**LongMemEval-M**: 500 sessions, ~1.5M tokens/question. Stress-test setting; history length is freely configurable.

**Oracle retrieval**: Not a history-size setting but an evaluation condition. The model is given only the ground-truth evidence sessions directly (no retrieval step), bypassing retrieval entirely. Used to isolate reading/reasoning failure from retrieval failure, and to measure the upper bound of reading performance.

## Method
- The benchmark instance is a 4-tuple `(S, q, t_q, a)`, where `S` is an ordered history of sessions, `q` is the question, `t_q` is its time, and `a` is the answer or answer rubric.
- LongMemEval defines five core abilities and seven question types: single-session-user, single-session-assistant, single-session-preference, multi-session, knowledge-update, temporal-reasoning, and abstention.
- The curation pipeline uses a 164-attribute ontology, Llama 3 70B Instruct to generate user backgrounds and seed QA pairs, and human filtering plus rewriting to reach the final benchmark.
- Evidence statements are embedded into self-chatted evidence sessions, then mixed with unrelated sessions from ShareGPT, UltraChat, and simulated chats to build configurable long histories.

## Unified Memory Framework (Section 4)

The paper formulates long-term memory as a key-value datastore and identifies three stages and four control points (CPs):

**Three stages**: (1) Indexing — convert each session into (k, v) pairs; (2) Retrieval — query the datastore for top-k items; (3) Reading — LLM reads retrieved items and generates an answer.

**CP1 — Value**: granularity/format of stored memory units. Options: whole session, round-level decomposition (one user turn + one assistant response), summary, or extracted facts. Round-level is recommended; compression causes information loss.

**CP2 — Key**: what is used as the retrieval index. `K = V` (use value itself as key) is the common baseline. The paper proposes **key expansion**: `K = V + fact`, concatenating extracted user facts to the value to form a richer key. This improves Recall@k by 9.4% and final accuracy by 5.4% on average.

**CP3 — Query**: how the retrieval query is formulated. For temporal queries (e.g., "what did you recommend last weekend?"), plain similarity search fails. The paper proposes **time-aware query expansion**: index values with timestamped events; at retrieval time, use a strong LLM to extract a time range from the query and filter candidates.

**CP4 — Reading Strategy**: how the LLM processes retrieved items to produce an answer. Two orthogonal choices:
- **Format**: natural language (NL) vs. structured JSON — JSON helps the model recognize memory items as data.
- **Chain-of-Note (CoN)**: instruct the LLM to first extract notes from each memory item, then reason from the notes. Decomposes long-context reading into copy + reason.
- Best combination: **CoN + JSON**. Under oracle retrieval, this beats the worst combination by up to 10 absolute points for GPT-4o.

## Benchmarks / Datasets
| Asset | Size / Scale | Purpose | Notes |
|---|---:|---|---|
| Questions | 500 | Main evaluation set | Human-curated and manually edited |
| Sessions | 50k total | History pool scale | Used to build long interactive histories |
| LongMemEval-S | ~115k tokens/question | Standard shorter setting | About 50 sessions |
| LongMemEval-M | 500 sessions, ~1.5M tokens/question | Stress-test setting | Freely scalable history |
| Attribute ontology | 164 attributes | Question and background generation | 5 categories |

## Baselines
| Baseline | Role | Why it matters | Notes |
|---|---|---|---|
| ChatGPT | Commercial memory chatbot | Tests real deployed memory behavior | Evaluated through web UI |
| Coze | Commercial memory chatbot | Tests another deployed memory stack | Also web-UI based |
| GPT-4o | Long-context reader / judge | Strong reader and evaluator | Used in several setups |
| Llama 3.1 70B Instruct | Reader model | Strong open model baseline | Good but below GPT-4o in many settings |
| Llama 3.1 8B Instruct | Reader / extractor | Lower-capacity baseline | Used heavily in ablations |
| BM25 | Retriever | Sparse retrieval baseline | Weak compared to dense retrievers |
| Contriever | Retriever | Dense retrieval baseline | Compared in appendix |
| Stella V5 1.5B | Retriever | Main retriever in experiments | Chosen for strong MTEB performance |

## Main Results
| Finding | Concrete result |
|---|---|
| Benchmark difficulty | Commercial systems and long-context LLMs show about a 30% accuracy drop on sustained-memory settings, per the abstract and pilot study. |
| Best key design | `K = V + fact` is the strongest general indexing choice in Table 3. On LongMemEval-M with round values, it reaches Recall@10 = 0.784 and GPT-4o top-10 QA = 0.720. |
| Best session setting | With session values, `K = V + fact` reaches Recall@10 = 0.862 and GPT-4o top-5 QA = 0.714. |
| Time-aware retrieval | On the temporal subset, GPT-4o-based query expansion improves session Recall@10 from 0.721 to 0.797 with `K = V + fact`, and round Recall@10 from 0.550 to 0.722. |
| Reading strategy | Chain-of-Note plus JSON format is the strongest reading setup; the paper reports up to a 10-point absolute gain over weaker reading prompts. |
| More LLMs | Direct long-context reading on LongMemEval-S can collapse sharply: Llama-3.2-3B gets 0.008 and Llama-3.2-1B gets 0.010 in the oracle-less direct setting. |

## Experiments (Section 5)

Four experiment groups, all on LongMemEval-M unless noted:

**Exp 1 — Value granularity** (`fig:main-fig-value-design`): Compare session / round / summary / facts as value. Round-level decomposition significantly improves GPT-4o reading; fact values help only for multi-session reasoning. Optimal token budget differs by reader capability (Llama 8B peaks at ~3k tokens, GPT-4o keeps improving past 20k).

**Exp 2 — Key design** (`tab:main-results-key`): Compare K=V, K=summary, K=keyphrases, K=facts, K=V+fact, etc. Using compressed forms alone as K does not improve retrieval. `K = V + fact` (document expansion) is the best: average +9.4% Recall@k, +5.4% final accuracy.

**Exp 3 — Time-aware query expansion** (`tab:main-results-temporal_query`): On temporal-reasoning questions, adding LLM-extracted time range filtering improves recall by 11.3% (rounds) and 6.8% (sessions) on average. Requires a strong LLM (GPT-4o); Llama 8B hallucinates time ranges.

**Exp 4 — Reading strategy** (`fig:main-fig-reading-design`, oracle retrieval): 2×2 grid of NL/JSON × no-CoN/CoN. CoN+JSON is consistently best; CoN alone is always helpful; JSON alone is inconsistent without CoN. Up to 10-point absolute gap between best and worst for GPT-4o.



## Implementation Clues
- The unified memory view decomposes a memory assistant into indexing, retrieval, and reading.
- The recommended design is round-level value decomposition, `K = V + fact` key expansion, question-plus-time query formulation, flat retrieval, and Chain-of-Note reading.
- The main experimental reader models are GPT-4o, Llama 3.1 70B Instruct, and Llama 3.1 8B Instruct.
- The retriever is Stella V5 1.5B by default; appendix comparisons include BM25 and Contriever.
- The memory pipeline uses Llama 3.1 8B Instruct for summarization, keyphrase extraction, fact extraction, timestamped event extraction, and time-range parsing experiments.
- Retrieved items are sorted by timestamp before reading, and the reading prompt uses greedy search with a maximum generation length of 800 tokens.

## Limitations
- The benchmark is partially synthetic and depends on LLM-generated backgrounds, simulated sessions, and human filtering.
- Evaluation quality depends on a prompt-engineered GPT-4o judge rather than purely exact matching for open-ended answers.
- Time-aware retrieval depends on a strong query parser; weaker models can hallucinate irrelevant time ranges and prune the search space incorrectly.
- The paper's error analysis still finds a sizeable share of cases where retrieval is correct but generation fails.
- The ethics section notes privacy and misuse risks for memory systems, including the lack of a deletion operator.

## Takeaways
- Long-term memory for chat assistants is not just a longer context window problem.
- Session granularity matters, but so does preserving facts through key expansion rather than over-compressing values.
- Temporal memory needs explicit time-aware retrieval, not only semantic similarity search.
- Reading strategy still matters even with perfect retrieval, so retrieval and generation should be optimized together.

## Open Questions
- How should memory systems support safe deletion and correction of stale facts?
- Can long-term memory remain accurate without relying on a strong external LLM for judging and query-time time parsing?
- What retrieval and reading design generalizes best beyond personal-chat settings to broader assistant workloads?
- How much of the benchmark gap is due to retrieval failure versus reasoning failure after retrieval?

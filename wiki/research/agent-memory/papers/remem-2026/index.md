---
title: "REMem: Reasoning with Episodic Memory in Language Agents"
domain: research
area: misc
type: paper
status: processed
updated: 2026-04-19
tags: [paper, episodic-memory, memory-systems, rag, agents]
---
# REMem: Reasoning with Episodic Memory in Language Agents

## Paper Meta
- Authors: Yiheng Shu, Saisri Padmaja Jonnalagedda, Xiang Gao, Bernal Jiménez Gutiérrez, Weijian Qi, Kamalika Das, Huan Sun, Yu Su
- Year: 2026
- arXiv: 2602.13530
- Venue: not reported in the extracted text; the source uses the ICLR 2026 conference template
- Code/data link reported in the paper: https://github.com/intuit-ai-research/REMem
- Reading source: TeX only; no local repo checkout was present in this ingest

## TL;DR
- REMem targets the gap between semantic memory and episodic memory in language agents by explicitly modeling time-aware events, situational context, and multi-step reasoning over interaction history.
- The method builds a hybrid memory graph with gist nodes, phrase nodes, relation edges, context edges, and synonymy edges, then uses a ReAct-style agent for iterative retrieval over that graph.
- On four episodic memory benchmarks, it outperforms prior memory systems such as Mem0 and HippoRAG 2, with the paper reporting absolute gains of 3.4% on episodic recollection and 13.4% on episodic reasoning.

## Problem
- Existing agent memory systems are mostly semantic: they retrieve facts or summaries, but they do not preserve a coherent episode structure with time, place, participants, and event order.
- The paper formalizes two progressive challenges.
- Episodic recollection means reconstructing the situational details of past events.
- Episodic reasoning means composing multiple recalled events to answer order, duration, counting, and relation questions.

## Method

### Indexing
- For each event statement or chat session, the system extracts one or more natural-language gists with absolute timestamps when available.
- It also extracts fact triples `(subject, predicate, object)` with temporal qualifiers such as `point_in_time`, `start_time`, and `end_time`.
- Gists and facts are stored together in a hybrid memory graph so that context-level episodes and concept-level relations remain linked.
- The graph adds synonymy edges between similar gist nodes using embedding similarity, with the paper setting the threshold to 0.8.

### Agentic Inference
- REMem uses a ReAct-style agent with four tools: `semantic_retrieve`, `lexical_retrieve`, `find_gist_contexts`, and `find_entity_contexts`, plus `output_answer`.
- Retrieval is iterative, so the system can decompose complex queries, follow temporal constraints, and explore neighboring memory before answering.
- This is the main distinction from one-shot retrieval pipelines that only match a single text span.

## Benchmarks / Metrics
| Dataset | Task | Size used in paper | Metric(s) | Notes |
|---|---|---:|---|---|
| LoCoMo | Episodic recollection | 1,986 queries | F1, BLEU-1, LLM-J | Includes single-hop, multi-hop, open-domain, temporal, and adversarial subsets |
| REALTALK | Episodic recollection | 728 queries | F1, BLEU-1, LLM-J | Real human conversation memory |
| Complex-TR | Episodic reasoning | 1,000 queries | F1, BLEU-1, LLM-J | Sampled from the benchmark |
| Test of Time | Episodic reasoning | 2,800 semantic queries | EM | Anonymous entities and relations; memory-heavy temporal reasoning |
| MuSiQue | Semantic memory capability | 1,000 queries | F1, BLEU-1, LLM-J | Appendix-only extension |
| 2Wiki | Semantic memory capability | 1,000 queries | F1, BLEU-1, LLM-J | Appendix-only extension |

## Main Results
| Benchmark | Best REMem result | Most relevant comparison from the paper |
|---|---|---|
| LoCoMo | Ours-I: 42.4 F1 / 32.7 BLEU-1 / 76.2 LLM-J | Beats NV-Embed-v2 at 39.6 / 31.0 / 73.0 |
| REALTALK | Ours-S: 26.2 F1 / 19.2 BLEU-1 / 65.3 LLM-J | Slightly above Full-Context at 25.3 / 18.6 / 65.1 |
| Complex-TR | Ours-I: 83.3 F1 / 77.6 BLEU-1 / 89.6 LLM-J | Ours-I w/ TISER reaches 90.6 / 86.0 / 92.0 |
| Test of Time | Ours-I: 93.1 EM | Highest EM in the table; only method above 90 EM |

- On episodic recollection, the iterative version and the single-step version trade off differently: Ours-I is stronger on F1/BLEU, while Ours-S often has the best LLM-J on LoCoMo and REALTALK.
- On episodic reasoning, the iterative retrieval loop matters more. The paper reports Ours-I beating Ours-S by 7.0 LLM-J points and 20.6 EM points on the harder reasoning setting.
- The strongest reasoning configuration is Ours-I with TISER-style prompting, which the paper says gives the highest overall Complex-TR scores.

## Ablations / Analysis
- Removing gists causes the largest drop. On LoCoMo, LLM-J falls from 76.2 to 48.9; on Complex-TR, it falls from 89.6 to 80.9.
- Removing facts hurts less than removing gists, but it still degrades multi-hop reasoning and graph exploration.
- Removing synonymy edges mainly hurts lexical robustness and recall, which shows that semantic clustering of gist nodes is useful.
- Removing either semantic retrieval or lexical retrieval reduces performance, so the paper treats the two retrieval modes as complementary.
- The paper also notes that LoCoMo has a bias toward single-session questions: only 14.2% of queries are multi-session.
- For refusal behavior on LoCoMo adversarial questions, REMem reaches the highest F1 at 64.0 with 73.3% precision and 56.8% recall.

## Implementation Clues
- Default LLM: GPT-4.1-mini-2025-04-14.
- Default embedding model: nvidia/NV-Embed-v2.
- Retrieval scope: top-10 chunks or messages for embedding baselines; REMem operates over the top-10 gists and facts.
- HippoRAG 2 is configured with the top-3 sessions for final generation.
- Iterative inference depth is selected from 2 to 5 steps; the paper uses 3 steps for recollection tasks and 5 steps for reasoning tasks.
- The paper reports the code and data repository as `https://github.com/intuit-ai-research/REMem`, but no local repo checkout was present here.

## Limitations
- The paper does not include a standalone limitations section, so these are the limitations explicitly surfaced in results and discussion.
- Error analysis shows that the biggest failure mode on LoCoMo is selection or grounding error at 46%.
- Complex-TR errors are often temporal window mismatches at 42%, plus incomplete lists and offset-direction mistakes.
- Human evaluation is not perfect either: the LLM judge matched human labels in 93 of 100 sampled LoCoMo cases, with 7 disagreements.
- The conclusion explicitly points to more complex environments and streaming memory construction as open engineering challenges.

## Takeaways
- REMem’s core idea is that episodic memory should preserve both the event summary and the event-linked facts, not just a flattened semantic retrieval target.
- Time awareness matters most when the query requires multi-hop reasoning or temporal disambiguation.
- Gists are the primary carrier of situational context; facts are supporting anchors for multi-step inference.
- Iterative retrieval is worth the extra complexity mainly on harder reasoning tasks, while single-step retrieval can be competitive on simpler recollection queries.
- LLM-based judging correlates better with human evaluation than F1 or BLEU-1 in the paper’s validation sample.

## Open Questions
- How much of the gain comes from the memory structure itself versus the prompting and retrieval loop around it?
- Can the graph construction remain stable in a fully streaming, online setting without batch indexing?
- How can the system reduce grounding mistakes where the right episode is found but the wrong slot value is selected?
- What is the best way to extend episodic memory to more complex, noisy, or multi-modal environments?

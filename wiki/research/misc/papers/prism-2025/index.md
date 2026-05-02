---
title: "PRISM: Agentic Retrieval with LLMs for Multi-Hop Question Answering"
domain: research
area: misc
type: paper
status: processed
updated: 2026-04-19
tags: [paper, misc, prism, agentic-retrieval, multi-hop-qa]
---
# PRISM: Agentic Retrieval with LLMs for Multi-Hop Question Answering

## Paper Meta
- Title: PRISM: Agentic Retrieval with LLMs for Multi-Hop Question Answering
- Authors: Md Mahadi Hasan Nahid, Davood Rafiei
- Year: 2025
- Venue: not reported; manuscript is formatted as an `iclr2026_conference` submission template
- Topic: multi-hop QA, agentic retrieval
- Paper Slug: prism-2025
- arXiv: https://arxiv.org/abs/2510.14278
- PDF: `2510.14278.pdf`
- Code Repo: not found in this paper directory
- Reading Source: TeX/source
- PDF Fallback: not used

## TL;DR
- PRISM is a three-agent retrieval loop for multi-hop QA: a Question Analyzer decomposes the query, a Selector filters distractors for precision, and an Adder recovers missing evidence for recall.
- The system iterates the Selector and Adder for at most `N = 3` rounds, then passes the merged evidence set to a zero-shot Answer Generator.
- The paper argues that separating precision and recall at the retrieval stage improves both retrieval quality and downstream QA, especially on HotpotQA, MuSiQue, and MultiHopRAG.
- The source bundle was sufficient to complete the note; no PDF fallback was needed.

## Problem
- Multi-hop QA requires evidence from multiple passages, but naive retrieval often trades recall for precision or precision for recall.
- Missing one bridge fact can break the reasoning chain, while noisy context can obscure the signal and trigger hallucination in long-context LLMs.
- Existing retrieval-and-reasoning systems often improve one side of the tradeoff without a clean mechanism for recovering missing evidence after pruning.
- The paper frames retrieval as an active control problem rather than a static preprocessing step.

## Method
- The Question Analyzer decomposes a complex question into a short list of subquestions that make the required evidence explicit.
- The Selector receives the question, the subquestions, and candidate passages, then removes items that are definitely irrelevant.
- The Adder sees the same candidate pool plus the currently selected set, and adds bridging or missing evidence that the Selector may have left out.
- Selector and Adder iterate together and the final evidence set is deduplicated before being sent to the Answer Generator.
- All agents are prompted LLMs in a zero-shot setting with structured outputs such as lists of passage titles or indices.
- The paper uses GPT-4o, Gemini-2.5-Flash-Lite, and DeepSeek-Chat as backends.

## Benchmarks / Datasets
| Dataset / Benchmark | Setting | Notes |
|---|---|---|
| HotpotQA | open-domain multi-hop QA | Supporting sentences are available for evaluation |
| 2WikiMultiHopQA | open-domain multi-hop QA | Uses the structured text component and dev set |
| MuSiQue | open-domain multi-hop QA | Uses the answerable subset from prior work |
| MultiHopRAG | retrieval-focused multi-hop QA | News-article knowledge base, used to study retrieval precision and recall |

- The paper samples 500 instances from each dataset because of computational budget.
- Retrieval is evaluated with passage-level precision and recall, plus sentence-level fact retrieval on HotpotQA and 2WikiMultiHopQA.
- End-to-end QA is evaluated with Exact Match and token-level F1.
- The paper also reports partial match accuracy, passage-level QA, and error analysis by question type or hop count.

## Baselines
| Baseline | Role | Notes |
|---|---|---|
| BM25 | lexical retriever | Used as the weak retrieval reference point |
| OneR | one-pass retriever | BM25 over the original question |
| IRCoT | iterative retrieval + CoT | Strong recall-oriented baseline |
| SetR / SETR-CoT \& IRI | set-wise selection | LLM-based selection baseline |
| RankGPT | listwise reranker | Also used in MultiHopRAG retrieval comparison |
| RankZephyr | zero-shot reranker | Included in QA comparisons |
| DSP | retrieval + prediction | QA baseline on HotpotQA |
| DecomP | decomposition baseline | Appears in QA comparison table |
| Oracle Context / Oracle Gold | upper bound | Uses gold supporting evidence |
| Full Context | no retrieval | Reader sees all retrieved passages including distractors |

## Main Results
| Setting | Metric | Baseline / Reference | PRISM | Delta / Note |
|---|---|---|---|---|
| HotpotQA recall | passage recall | OneR 61.5, IRCoT 72.8 | 90.9 | Large gain in recall |
| 2Wiki recall | passage recall | OneR 68.1, IRCoT 90.7 | 91.1 | Slightly above IRCoT |
| MuSiQue recall | passage recall | OneR 44.6, IRCoT 57.1 | 83.2 | Largest recall gain |
| HotpotQA fact-level retrieval | P/R/F1 | not reported | 56.70 / 75.51 / 64.77 | Sentence-level evidence recovery |
| 2Wiki fact-level retrieval | P/R/F1 | not reported | 60.81 / 74.42 / 66.93 | Sentence-level evidence recovery |
| HotpotQA QA | EM / F1 | Full Context 44.18 / 58.28 | 54.20 / 66.96 | Strong gain over full context |
| 2Wiki QA | EM / F1 | Full Context 43.20 / 52.11 | 48.60 / 56.97 | Competitive, not best-in-table |
| MuSiQue QA | EM / F1 | Full Context 19.77 / 29.42 | 31.17 / 41.78 | Clear gain on harder multi-hop reasoning |
| MultiHopRAG QA | ACC | Full Context 44.37 | 49.16 | Best QA score in the table |

- On HotpotQA, the paper claims PRISM improves over IRCoT and SetR by about +5 EM / +6 F1, and the table supports a sizable margin over full context.
- On MultiHopRAG retrieval, the source has an internal inconsistency: the table reports 24.74 precision / 40.64 recall, while the following paragraph states 28.18 precision / 42.22 recall. I kept the table value as canonical in this note.
- The model-backend table shows that the framework generalizes across GPT-4o, Gemini-2.5-Flash-Lite, and DeepSeek, with the strongest QA numbers varying by dataset.

## Ablations / Analysis
| Variant | HotpotQA recall | 2Wiki recall | MuSiQue recall | Avg # passages |
|---|---|---|---|---|
| Full model | 90.9 | 91.1 | 83.2 | 2.67 / 2.74 / 6.15 |
| w/o Question Analyzer | 86.8 | 85.8 | 68.8 | 2.88 / 2.68 / 7.68 |
| w/o Selector \& Adder loop | 79.7 | 80.5 | 69.3 | 2.63 / 2.71 / 2.82 |

- Removing the Question Analyzer hurts MuSiQue the most, which fits the paper's claim that decomposition matters more as hop count rises.
- Removing the Selector-Adder loop drops recall sharply, which supports the main design claim that precision filtering and recall recovery are complementary.
- Partial Match Accuracy improves over full context on all four datasets: 61.4 to 71.6 on HotpotQA, 52.2 to 57.8 on 2Wiki, 25.4 to 38.4 on MuSiQue, and 46.1 to 54.5 on MultiHopRAG.
- Passage-level QA from retrieved evidence is close to oracle-level on HotpotQA and 2Wiki: 62.80 EM / 59.26 F1 on HotpotQA and 61.17 EM / 54.55 F1 on 2Wiki.
- Error analysis shows that a meaningful share of failures still come from the QA reader even when retrieval recall is perfect, especially on HotpotQA and MuSiQue.

## Implementation Clues
- The system is implemented as prompted LLM agents rather than task-specific fine-tuned models.
- The Selector and Adder operate over candidate passages and sentence indices, with structured outputs to make parsing reliable.
- Iteration depth is bounded at `N = 3` to keep the number of LLM calls tractable.
- The paper evaluates multiple LLM backends in the same zero-shot pipeline, which suggests the method is meant to be model-agnostic.
- The source says the authors plan to release code, prompts, and the retrieval pipeline upon publication, but no local repo was present in this directory.
- Source reading was sufficient for this ingest, so PDF fallback was not used.

## Limitations
- The multi-agent design increases compute relative to single-pass retrieval.
- The loop can still miss subtle reasoning chains or add redundancy when passages are loosely connected.
- Results are benchmark-driven and may require adaptation for scientific, biomedical, or legal corpora.
- Performance depends partly on the underlying LLM backend, so stronger readers and agents can change absolute scores.
- The source has one unresolved numeric inconsistency in the MultiHopRAG retrieval discussion.

## Takeaways
- PRISM’s main idea is to split retrieval into precision-first filtering and recall-first recovery instead of expecting one retriever to do both.
- Question decomposition is not a side detail here; it is an explicit control input for the later retrieval stages.
- Better retrieval can materially improve downstream QA even when the reader is zero-shot.
- The paper’s strongest evidence is on MuSiQue and HotpotQA, where distractors and multi-hop structure are both hard.

## Open Questions
- Can the Selector-Adder loop be made cheaper without losing recall?
- How much of the gain comes from decomposition versus selection versus addition?
- Would a smaller open model preserve the same retrieval gains across all datasets?
- What parts of PRISM transfer best to domain-specific corpora with different evidence structure?

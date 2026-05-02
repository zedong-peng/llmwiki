---
title: "FAIR-RAG: Faithful Adaptive Iterative Refinement for Retrieval-Augmented Generation"
domain: research
area: misc
type: paper
status: processed
updated: 2026-04-18
tags: [paper, misc, processed, fair-rag, rag, multi-hop, flashrag]
---
# FAIR-RAG: Faithful Adaptive Iterative Refinement for Retrieval-Augmented Generation

## Paper Meta
- Title: FAIR-RAG: Faithful Adaptive Iterative Refinement for Retrieval-Augmented Generation
- Authors: Mohammad Aghajani Asl; Majid Asgari-Bidhendi; Behrooz Minaei-Bidgoli
- Year: 2025
- Venue: not reported
- Topic: misc
- Paper Slug: fair-rag-2025
- arXiv: https://arxiv.org/abs/2510.22344
- PDF: 2510.22344.pdf
- Code Repo: not reported
- Reading Source: TeX / source

## TL;DR
FAIR-RAG turns RAG into an evidence-driven agent loop: adaptive routing, multi-query decomposition, hybrid retrieval, evidence filtering, Structured Evidence Assessment (SEA), and faithful generation. The paper’s strongest reported gains are on multi-hop QA, with the abstract highlighting HotpotQA F1 0.453 under the Adaptive LLM configuration and the full table showing slightly higher HotpotQA F1 at 0.456 for FAIR-RAG 4.

## Problem
- Standard retrieve-then-read RAG underperforms on complex multi-hop and comparative questions.
- Existing iterative methods can propagate noise, while adaptive routing alone does not guarantee evidence sufficiency.
- The paper targets a concrete control problem: detect what evidence is missing, then issue targeted follow-up queries before answering.

## Method
- Adaptive Routing classifies queries into OBVIOUS, SMALL, LARGE, or REASONING and can bypass retrieval for trivial questions.
- The core loop runs for up to 3 iterations: semantic decomposition -> hybrid retrieval and reranking -> evidence filtering -> SEA -> query refinement if gaps remain.
- SEA is the central control module: it converts the query into a checklist of required findings, audits the evidence, and returns confirmed facts plus explicit remaining gaps.
- Query refinement uses the SEA gaps to generate narrow follow-up queries rather than recycling the previous answer as a query.
- Final generation is constrained to evidence-only answering with citations and an explicit instruction to abstain if evidence is insufficient.
- The full framework also supports adaptive model allocation, with smaller models for simpler internal tasks and larger/reasoning models for harder ones.

## Benchmarks / Datasets
| Dataset / Benchmark | Task | Metric(s) Used | Notes |
|---|---|---|---|
| HotpotQA | multi-hop QA | EM, F1, ACC, ACC_LLM | 1000 sampled test/dev examples |
| 2WikiMultiHopQA | multi-hop QA | EM, F1, ACC, ACC_LLM | 1000 sampled test/dev examples |
| MuSiQue | multi-hop QA | EM, F1, ACC, ACC_LLM | 1000 sampled test/dev examples |
| TriviaQA | open-domain QA | EM, F1, ACC, ACC_LLM | 1000 sampled test/dev examples |

## Baselines
| Baseline | Type | Why It Matters | Notes |
|---|---|---|---|
| Standard RAG | sequential | Simple retrieve-then-read reference | Dense-only setup in experiments |
| SuRe | branching | Candidate-answer summarization baseline | Compares a different control strategy |
| Adaptive-RAG | conditional | Complexity-based routing baseline | Routes once at the start |
| ReAct | reasoning-based | Action/Reasoning interleaving baseline | Strong agentic reference point |
| Iter-Retgen | iterative | Prior output drives the next retrieval | Strongest multi-hop baseline on some datasets |
| Self-RAG | faithfulness-focused | Self-critique and reflection baseline | Uses the released selfrag-llama-7b model |
| IRCoT | iterative | Retrieval interleaved with CoT | Strong on retrieval-heavy reasoning |

## Main Results
The paper evaluates FAIR-RAG under a controlled FlashRAG setup. The abstract’s headline claim is HotpotQA F1 0.453 for FAIR-RAG 3 (Adaptive LLMs), which is +0.083 over the strongest iterative baseline. The full main table also reports a slightly higher HotpotQA F1 of 0.456 for FAIR-RAG 4 under the uniform-model setting.

| Dataset / Benchmark | Best FAIR-RAG Variant | EM | F1 | ACC | ACC_LLM | Strongest Baseline F1 | Delta |
|---|---|---:|---:|---:|---:|---:|---:|
| HotpotQA | FAIR-RAG 3 (Adaptive LLMs) | 0.338 | 0.453 | 0.399 | 0.694 | 0.370 | +0.083 |
| 2WikiMultiHopQA | FAIR-RAG 3 (Adaptive LLMs) | 0.206 | 0.320 | 0.350 | 0.452 | 0.251 | +0.069 |
| MuSiQue | FAIR-RAG 3 (Adaptive LLMs) | 0.178 | 0.264 | 0.222 | 0.472 | 0.190 | +0.074 |
| TriviaQA | FAIR-RAG 3 (Adaptive LLMs) | 0.645 | 0.731 | 0.710 | 0.847 | 0.676 | +0.055 |

- Best HotpotQA F1 in the full table is 0.456 from FAIR-RAG 4, not the adaptive variant.
- Best TriviaQA ACC_LLM in the full table is 0.847 from FAIR-RAG 3 (Adaptive LLMs).
- The strongest F1 baseline differs by dataset: Iter-Retgen on HotpotQA, MuSiQue, and TriviaQA; Self-RAG on 2WikiMultiHopQA.

## Ablations / Analysis
### Component-Level Evaluation
| Component | HotpotQA | 2WikiMultiHopQA | MuSiQue | TriviaQA | Takeaway |
|---|---:|---:|---:|---:|---|
| Query decomposition | 4.19 | 4.12 | 4.10 | 4.33 | Consistently high quality |
| Evidence filtering | 67.3% | 55.5% | 68.5% | 76.1% | Clear precision-recall tradeoff |
| SEA | 72.0% | 81.7% | 83.2% | 54.4% | Strong on complex tasks, weaker on TriviaQA |
| Query refinement | 4.45 | 4.39 | 4.42 | 4.52 | Highest-rated internal component |

### Iteration vs. Cost
| Dataset | Best Max Iter. | Avg. Answer Rank | Improvement Rate vs Iter 1 | Avg. API Calls | Avg. Tokens / Query |
|---|---:|---:|---:|---:|---:|
| HotpotQA | 2 | 2.23 | 58.50% | 6.64 | 14,332 |
| 2WikiMultiHopQA | 3 | 2.18 | 70.90% | 8.79 | 19,812 |
| MuSiQue | 2 | 2.20 | 63.40% | 7.25 | 15,688 |
| TriviaQA | 1 | 1.83 | not reported | 4.97 | 9,572 |

- The paper argues that 2 to 3 iterations are the sweet spot for multi-hop tasks.
- A fourth iteration usually hurts quality while increasing API calls and token use.
- On TriviaQA, extra iterations are mostly harmful, which supports the need for adaptive stopping.

### Failure Mode Analysis
- The authors analyze 200 errors and split them into component-level failures (63.5%) and architectural failures (36.5%).
- Retrieval failure is the largest single source of error at 32.5%.
- Generation failure accounts for 31.0% of errors even when evidence is retrieved correctly.
- SEA failure is the largest architectural issue at 24.5%, followed by query decomposition at 9.0%.

## Implementation Clues
- Evaluation is built on FlashRAG, with the source bundle explicitly pointing to the FlashRAG repository in the appendix.
- The benchmark setup standardizes retrieval to `e5-base-v2`, top_k = 5, and Faiss `IndexFlatIP`.
- Baselines use `Llama-3-8B-Instruct`; Self-RAG uses `selfrag-llama-7b`; the adaptive configuration also uses `Llama-3.1-70B-Instruct` and `DeepSeek-R1` for harder internal tasks.
- All benchmarks in the main comparison use dense-only retrieval and disable the "OBVIOUS" shortcut to keep the comparison fair.
- The source bundle includes the full prompts for routing, decomposition, filtering, SEA, and generation.
- Reported evaluation uses 1000 samples per dataset rather than the full benchmark splits.

## Limitations
- Performance depends on the underlying LLMs and on prompt quality for each agent.
- Iteration improves hard questions but increases latency, API calls, and token usage.
- Early-stage mistakes can cascade through retrieval, filtering, SEA, and final generation.
- The maximum of 3 iterations is a fixed heuristic, not a query-specific stopping policy.

## Takeaways
- SEA is the key differentiator: it makes iterative RAG gap-driven rather than answer-driven.
- The strongest gains are on multi-hop benchmarks, not on simple factoid QA.
- More iterations are not always better; the paper’s own analysis shows diminishing returns after 2 to 3 loops.
- The reported gains are tied to a controlled setup, so the architecture is the main claim, not a specific retrieval stack.

## Open Questions
- Can SEA be replaced with a cheaper learned sufficiency classifier without losing quality?
- Would a dynamic stopping policy outperform the fixed three-iteration cap?
- How much of the gain persists if the dense-only fair-comparison restrictions are relaxed and the full hybrid retriever is enabled?

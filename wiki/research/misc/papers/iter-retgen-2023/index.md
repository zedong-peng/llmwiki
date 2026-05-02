---
title: "Enhancing Retrieval-Augmented Large Language Models with Iterative Retrieval-Generation Synergy"
domain: research
area: misc
type: paper
status: processed
updated: 2026-04-18
tags: [paper, misc, retrieval, generation, multihop-qa, emnlp-2023]
---
# Enhancing Retrieval-Augmented Large Language Models with Iterative Retrieval-Generation Synergy

## Paper Meta
- Title: Enhancing Retrieval-Augmented Large Language Models with Iterative Retrieval-Generation Synergy
- Authors: Zhihong Shao, Yeyun Gong, Yelong Shen, Minlie Huang, Nan Duan, Weizhu Chen
- Year: 2023
- Venue: EMNLP 2023
- Topic: misc
- Paper Slug: iter-retgen-2023
- arXiv: https://arxiv.org/abs/2305.15294
- PDF: 2305.15294.pdf
- Code Repo: not reported
- Reading Source: TeX / source

## TL;DR
- Iter-RetGen alternates retrieval-augmented generation and generation-augmented retrieval: the model’s previous output becomes the next retrieval query context, then the newly retrieved passages are fed back into another generation step.
- The paper’s main claim is that this simple loop is strong on complex-information tasks because it preserves full-generation flexibility while still letting retrieval benefit from the model’s own intermediate reasoning.
- Across six datasets, the method is consistently better than or competitive with retrieval-augmented baselines, and the strongest reported gain is +8.6 Acc^dag on HotPotQA versus Self-Ask.
- Two iterations are usually the sweet spot: the second round gives the biggest boost, and later iterations mostly plateau.
- Generation-augmented retrieval adaptation further improves the retriever, showing that LLM outputs are useful not only for prompting but also for distillation.
- The paper also argues that EM can miss semantically correct answers, so `Acc^dag` is often the more reliable evaluation signal.

## Problem
- One-time retrieval is often enough for direct fact lookup, but it breaks down when the information need only becomes clear after partial reasoning.
- Structured multi-round methods such as ReAct, Self-Ask, and IRCoT can retrieve more often, but they also interleave generation with retrieval in a way that can constrain the model and add overhead.
- The paper targets a simpler alternative: use the model’s own full previous response as a better retrieval context, then let the next generation step consume the retrieved evidence as a whole.
- The motivation is especially strong for multi-hop QA, fact verification, and commonsense reasoning, where the supporting evidence is often not explicit in the original question.

## Method
- Iter-RetGen repeats a two-step loop for `T` iterations: retrieve paragraphs using `q` plus the previous output `y_{t-1}`, then generate a new answer `y_t` from the retrieved paragraphs and the original question.
- The first iteration is effectively retrieval-augmented CoT; later iterations reuse the full previous generation to bridge semantic gaps between the question and the evidence.
- Unlike interleaving approaches, Iter-RetGen does not interrupt generation with retrieval mid-answer, so it keeps the prompt structure simpler and avoids forcing intermediate answers into a rigid workflow.
- The paper also proposes generation-augmented retrieval adaptation: a re-ranker sees `y_1 || q`, and its signal is distilled into a dense retriever that otherwise only sees `q`.
- This adaptation is meant to move the retriever closer to the model’s inferred information need, especially when the question alone is underspecified.
- In the experiments, retrieval uses Contriever-MSMARCO, and the main LLM backend is `text-davinci-003`.

## Benchmarks / Datasets
| Dataset / Benchmark | Task | Metric | Notes |
|---|---|---|---|
| HotPotQA | Multi-hop question answering | EM, F1, Acc^dag | 500 development questions; Wikipedia retrieval corpus from the October 2017 dump. |
| 2WikiMultiHopQA | Multi-hop question answering | EM, F1, Acc^dag | 500 development questions; Wikipedia retrieval corpus from the December 2018 dump. |
| MuSiQue | Multi-hop question answering | EM, F1, Acc^dag | 2-hop subset only; 500 development questions. |
| Bamboogle | Multi-hop question answering | EM, F1, Acc^dag | All 125 questions; used as a compact compositional QA benchmark. |
| Feverous | Fact verification | Acc, Acc^dag | 500 development questions; Wikipedia retrieval corpus from the December 2021 dump. |
| StrategyQA | Commonsense reasoning | Acc, Acc^dag | First 500 train questions; Wikipedia retrieval corpus from the December 2021 dump. |

## Baselines
| Baseline | Type | Why Important | Notes |
|---|---|---|---|
| Direct Prompting | No-retrieval prompting | Establishes how far the LLM gets without external evidence | With retrieval, the question is prepended with retrieved paragraphs. |
| CoT Prompting | No-retrieval reasoning prompt | Main non-retrieval reasoning baseline | Shares demonstrations with Iter-RetGen but omits retrieval. |
| ReAct | Interleaved reasoning and retrieval | Strong structured retrieval baseline | Retrieval and reasoning alternate until a final answer is produced. |
| Self-Ask | Follow-up question decomposition | Closest structural baseline for multi-hop tasks | Retrieved paragraphs are accumulated before the original question. |
| DSP | Retrieval plus prediction pipeline | Another retrieval-augmented multi-hop framework | Compared only on a subset of datasets in the main table. |

## Main Results
| Dataset / Benchmark | Metric | Baseline | Ours | Gain / Delta | Notes |
|---|---|---|---|---|---|
| HotPotQA | Acc^dag | Self-Ask 64.8 | Iter-RetGen 4: 73.4 | +8.6 | Largest absolute gain reported in the paper. |
| 2WikiMultiHopQA | Acc^dag | Self-Ask 55.9 | Iter-RetGen 6: 59.4 | +3.5 | Stronger than ReAct, Direct, and DSP where reported. |
| MuSiQue | F1 | Self-Ask 41.5 | Iter-RetGen 7: 42.0 | +0.5 | Competitive rather than a large win on the paper’s preferred metrics. |
| Bamboogle | Acc^dag | Self-Ask 54.8 | Iter-RetGen 7: 60.8 | +6.0 | Clear improvement on the compositional QA benchmark. |
| Feverous | Acc^dag | Self-Ask 70.7 | Iter-RetGen 4: 71.5 | +0.8 | Small but consistent gain over the strongest baseline. |
| StrategyQA | Acc^dag | Self-Ask 70.2 | Iter-RetGen 7: 74.1 | +3.9 | Better than ReAct and Direct prompting with retrieval. |

## Ablations / Analysis
- Iteration depth matters. On HotPotQA, `Acc^dag` rises from 65.5 at iteration 1 to 73.4 at iteration 4; on 2WikiMultiHopQA it rises from 55.4 at iteration 1 to 59.4 at iteration 6.
- Retrieval adaptation helps. With `y_1` used during distillation, HotPotQA improves from 65.5 to 67.7 at iteration 1 and from 71.2 to 75.7 at iteration 2; Feverous improves from 67.0 to 70.7 and from 68.8 to 69.5.
- Answer recall of retrieved paragraphs jumps sharply in the second iteration, for example HotPotQA goes from 49.5 to 66.1 and StrategyQA from 20.8 to 36.0, then mostly plateaus.
- The subset analysis shows that Iter-RetGen is particularly good at preserving CoT-solvable cases while remaining robust when the retrieved knowledge does not explicitly mention the answer.
- The paper’s manual comparison against DSP suggests two failure modes for DSP: missing the right evidence and producing misleading summaries of retrieved content.
- A manual error analysis on HotPotQA attributes most remaining errors to retrieval issues, not pure reasoning failures.

## Implementation Clues
- The main experimental LLM is `text-davinci-003`; decoding is greedy.
- Retrieval uses Contriever-MSMARCO and top-5 paragraphs per query.
- ReAct and Self-Ask are capped at 5 retrieval interactions.
- Iter-RetGen and CoT share the same annotated demonstrations; the difference is the retrieval loop.
- The appendix also reports Llama-2-13B and Llama-2-70B runs, and the same pattern holds.
- No official repo was available in this paper directory, so there was nothing to read beyond the TeX source and appendix.

## Limitations
- The experiments use a fixed black-box LLM, so the results may depend on the promptability of `text-davinci-003`.
- The method is evaluated on QA-style tasks; long-form generation is explicitly left for future work.
- EM can severely underestimate quality: the paper reports many cases where EM is 0 but `Acc^dag` is 1.
- The approach still depends on retrieval quality, and the paper’s error analysis shows retrieval remains the dominant failure mode.

## Takeaways
- The paper’s core insight is that the model’s own previous answer is a better retrieval query than the raw question alone for complex tasks.
- Keeping the generation step unstructured, while moving retrieval to the next iteration, is a simpler alternative to interleaved prompting frameworks.
- Two iterations often deliver most of the benefit, so the cost/performance tradeoff is tunable.
- `Acc^dag` is an important practical lesson here: surface-form metrics can hide correct reasoning.
- The retriever-adaptation result suggests a broader pattern worth reusing: let LLM generations supervise retrieval, not just answer generation.

## Open Questions
- How much of the gain comes from the iterative loop itself versus the specific choice of CoT-style prompting?
- Would a stronger retriever or a retrieval model trained end-to-end on these tasks reduce the need for multiple iterations?
- Can the same retrieval-generation synergy be extended to long-form generation without becoming too expensive?
- What happens if the method is paired with newer base LLMs or non-Wikipedia retrieval corpora?

---
title: "Evaluating Very Long-Term Conversational Memory of LLM Agents"
domain: research
area: misc
type: paper
status: processed
updated: 2026-04-18
tags: [paper, misc, long-term-memory, dialogue, multimodal, benchmark]
---
# Evaluating Very Long-Term Conversational Memory of LLM Agents

## Paper Meta
- Authors: Adyasha Maharana, Dong-Ho Lee, Sergey Tulyakov, Mohit Bansal, Francesco Barbieri, Yuwei Fang
- Year: 2024
- Venue: not reported in source
- Topic: misc
- Paper Slug: `locomo-2024`
- arXiv: https://arxiv.org/abs/2402.17753
- Project page: https://snap-research.github.io/locomo
- PDF: `2402.17753.pdf`
- Code repo: not available locally
- Reading source: TeX

## TL;DR
- The paper introduces **LoCoMo**, a benchmark for **very long-term** conversational memory built from 50 synthetic-but-human-edited multi-session dialogues.
- It evaluates three capabilities: question answering over long dialogue history, event-graph summarization, and multimodal dialogue generation.
- Long-context models help, but they still lag far behind humans, and retrieval works best when the conversation is converted into compact **observations** instead of raw dialogue.

## Problem
- Existing long-term dialogue benchmarks mostly cover only a few sessions or roughly 1K tokens, so they do not stress memory over the kind of multi-month narratives that generative agents need.
- The paper asks whether LLM agents can retain persona, event history, temporal order, causal links, and image-grounded context over conversations that span up to 35 sessions.

## Method
- The authors build a human-machine pipeline: expand short persona seeds from MSC with `gpt-3.5-turbo`, generate temporal event graphs with `text-davinci-003`, run two virtual agents with reflect-and-respond memory, and let human annotators fix inconsistencies.
- Each agent has short-term summaries, long-term observations, and a multimodal branch that can share images and react to images.
- Human annotators edit long-range inconsistencies, remove or replace irrelevant images, and verify that the conversation matches the event graph.

## Benchmarks / Datasets
| Metric                          |   Value | Notes                                   |
| ------------------------------- | ------: | --------------------------------------- |
| Conversations                   |      50 | Human-edited outputs from the pipeline  |
| Avg. sessions per conversation  |    19.3 | Up to 35 sessions                       |
| Avg. turns per conversation     |   304.9 | Very long multi-session dialogue        |
| Avg. tokens per conversation    | 9,209.2 | About 9K tokens on average              |
| Avg. turns per session          |    15.8 | Session-level granularity from appendix |
| Avg. tokens per dialogue turn   |    30.2 | From appendix statistics                |
| Avg. tokens per observation     |    18.2 | Long-term memory atom                   |
| Avg. tokens per session summary |   127.4 | Short-term memory atom                  |
| Avg. images per conversation    |    32.3 | Multimodal conversations                |

## Baselines
| Baseline | Type | Why Important | Notes |
|---|---|---|---|
| Mistral-Instruct-7B | base QA model | Open-weight baseline with short context | Weak on long memory recall |
| Llama-2-Chat-70B | base QA model | Stronger open-weight baseline | Still far below human performance |
| GPT-3.5-turbo | proprietary QA model | Main mid-tier closed model baseline | Competitive but weak on adversarial QA |
| GPT-4-turbo | proprietary QA model | Strongest short-context baseline | Best base-model result in the main QA table |
| GPT-3.5-turbo-16K | long-context baseline | Tests whether more context alone solves memory | Improves overall F1 but still fragile |
| DRAGON + GPT-3.5 | RAG baseline | Tests retrieval over dialogue / summaries / observations | Observation retrieval is best |

## Benchmark Tasks
| Task | What It Tests | Metric(s) | Notes |
|---|---|---|---|
| Question answering | Recall across sessions, temporal reasoning, adversarial robustness | F1, retrieval accuracy | Five question types: single-hop, multi-hop, temporal, open-domain knowledge, adversarial |
| Event summarization | Causal and temporal understanding of life events | ROUGE, FactScore F1 | Summaries should match event graphs, not just surface wording |
| Multimodal dialogue generation | Persona consistency and image-grounded conversation | BLEU, ROUGE-L, MM-Relevance | MiniGPT-5 variants trained with different context types |

### QA Composition
| Category              | Count | Share |
| --------------------- | ----: | ----: |
| Single-hop            | 2,705 | 36.0% |
| Multi-hop             | 1,104 | 14.6% |
| Temporal reasoning    | 1,547 | 20.6% |
| Open-domain knowledge |   285 |  3.9% |
| Adversarial           | 1,871 | 24.9% |
| Total                 | 7,512 |  100% |

## Ablations / Analysis
- Base QA models: Mistral-Instruct-7B, Llama-2-Chat-70B, GPT-3.5-turbo, GPT-4-turbo.
- Long-context QA model: GPT-3.5-turbo-16k with increasing context windows.
- RAG QA: DRAGON retriever plus GPT-3.5-turbo-16k reader, using either dialog history, observations, or session summaries as retrieval units.
- Event summarization: base and long-context setups only, with incremental session-by-session summarization.
- Multimodal generation: MiniGPT-5 trained on 50 synthetic conversations with three variants: base, `+ summary`, and `+ observation`.
- Implementation details from appendix: OpenAI API and Hugging Face as of January 2024; temperature 0; top_p 1; experiments run on Nvidia A6000; MiniGPT-5 trained for 10 epochs.

## Main Results

### Question Answering
| Model | Context | Overall F1 | Key Takeaway |
|---|---:|---:|---|
| Human | - | 87.9 | Strong upper bound |
| Mistral-Instruct-7B | 8K | 13.9 | Very weak on long dialogue memory |
| Llama-2-Chat-70B | 4,096 | 17.9 | Slightly better, still poor |
| GPT-3.5-turbo | 4,096 | 22.4 | Best base-model overall among the listed base models |
| GPT-4-turbo | 4,096 | 32.1 | Best base-model overall in the main table |
| GPT-3.5-turbo-16K | 16K | 37.8 | Long context helps, but still far below humans |

- Temporal reasoning and adversarial questions are the hardest categories.
- The long-context model reaches 56.4 on single-hop and 42.0 on multi-hop, but adversarial performance collapses to 2.1.
- RAG helps most when the retriever works over **observations** instead of raw dialogue or summaries; observation top-5 reaches 41.4 overall F1.

### Event Summarization
| Model | Rouge-L | FactScore F1 | Key Takeaway |
|---|---:|---:|---|
| GPT-3.5-turbo | 20.9 | 45.9 | Best overall F1 in the table |
| GPT-4-turbo | 20.6 | 45.1 | Best precision, but not best F1 |
| GPT-3.5-turbo-16K | 16.4 | 39.9 | Long context does not beat the base model |

- Incremental summarization helps, but larger context alone does not solve the causal/temporal reasoning problem.
- The paper identifies recurring error modes: missing information, hallucination, cue misunderstanding, wrong speaker attribution, and saliency mistakes.

### Multimodal Dialogue Generation
| Variant | BLEU-1 / BLEU-2 | ROUGE-L | MM-Relevance | Takeaway |
|---|---:|---:|---:|---|
| Base | 57.1 / 34.2 | 12.4 | 56.1 | Strong baseline |
| `+ summary` top-1 | 58.2 / 34.1 | 12.8 | 56.9 | Small gain from summaries |
| `+ observation` top-5 | 59.7 / 35.1 | 13.6 | 57.8 | Best overall variant |

- Observations outperform summaries for multimodal generation because they preserve concise, speaker-specific assertions.
- MM-Relevance drops as dialogue history grows, and RAG partially offsets that decline.

## Implementation Clues
- The generative pipeline uses persona expansion, temporal event graph generation, reflection summaries, and observation extraction; these are the core artifacts worth reusing if you want to reproduce the dataset.
- Image behavior is implemented with image captioning and web image retrieval, while image reaction uses BLIP-2 for captions.
- The benchmark is designed so that raw dialogue can be replaced by image captions for QA and summarization, but not for the multimodal generation task.
- The source says code and data were to be released at the project page rather than through a local repo in this directory.

## Limitations
- The dataset is largely synthetic and then human-edited, so it may not fully capture the messiness of real-world long-term conversations.
- Images are web-sourced, so the benchmark does not strongly test stable visual identity over time.
- The pipeline is English-only.
- The work depends on closed-source LLMs for generation and evaluation, which limits reproducibility and portability.
- Long-form NLG metrics remain imperfect for very long answers and summaries.

## Takeaways
- Very long-term conversational memory is still unsolved: more context helps, but not enough.
- Compact, evidence-like memory representations are more useful than raw dialogue for retrieval and multimodal generation.
- LoCoMo is most useful as a stress test for temporal reasoning, causal linking, and memory consolidation over multi-session dialogue.

## Open Questions
- How much of the benchmark gap comes from retrieval quality versus reasoning quality?
- Can open-source models match the observation-based RAG results with better memory organization?
- What is the right metric for multimodal long-term consistency when the image stream itself is partly synthetic?
- How would performance change if the benchmark were built from real conversations instead of synthetic ones?

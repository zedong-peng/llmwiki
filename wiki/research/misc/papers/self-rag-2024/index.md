---
title: "Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection"
domain: research
area: misc
type: paper
status: processed
updated: 2026-04-19
tags: [paper, misc, self-rag, rag, reflection-tokens]
---
# Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection

## Paper Meta
- Title: Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection
- Authors: Akari Asai, Zeqiu Wu, Yizhong Wang, Avirup Sil, Hannaneh Hajishirzi
- Year: 2024
- Venue: ICLR 2024 camera-ready source
- Topic: misc
- Paper Slug: self-rag-2024
- arXiv: https://arxiv.org/abs/2310.11511
- PDF: 2310.11511.pdf
- Code Repo: https://github.com/AkariAsai/self-rag
- Reading Source: TeX / source
- Repo Read: README only in this snapshot
- PDF Fallback: not used

## TL;DR
- Self-RAG trains one LM to decide when to retrieve, generate answers, and critique its own output with special reflection tokens.
- The key move is offline annotation of training data with GPT-4-derived critique tokens, then distillation into an in-house critic and generator.
- Inference is controllable: the model can retrieve on demand, rank candidate continuations with critique scores, and trade off factuality, citation quality, and fluency.
- On six tasks, the 7B and 13B variants outperform standard instruction-tuned LMs and most retrieval-augmented baselines, with especially strong gains on factuality and citation accuracy.

## Problem
- Standard RAG retrieves passages even when retrieval is unnecessary, which can add irrelevant context and hurt output quality.
- Retrieval alone does not guarantee that generations are actually supported by the retrieved passages.
- The paper targets a single framework that keeps LLM versatility while improving factuality, support, and attribution.

## Method
- Self-RAG adds reflection tokens to the vocabulary: retrieval tokens (`Yes`, `No`, `continue to use evidence`), relevance tokens, support tokens, and usefulness tokens.
- The model first predicts whether retrieval is needed for the current segment, then retrieves passages on demand, generates candidates, and critiques them with fine-grained signals.
- The critic is trained from GPT-4-prompted supervision on reflection-token labels, then used offline to annotate the training corpus.
- The generator is then trained with standard next-token prediction on a corpus augmented with reflection tokens and retrieved passages.
- At inference, the model can use a threshold on retrieval probability or a segment-level beam search that combines generation likelihood with critique scores.

## Benchmarks / Datasets
| Dataset / Benchmark | Task | Metric | Notes |
|---|---|---|---|
| PubHealth | fact verification | accuracy | closed-set evaluation |
| ARC-Challenge | multiple-choice reasoning | accuracy | closed-set evaluation |
| PopQA | open-domain QA | accuracy | long-tail subset of 1,399 queries |
| TriviaQA-unfiltered | open-domain QA | answer inclusion / accuracy-style scoring | validation/test split used because open test set is unavailable |
| Biography generation | long-form generation | FactScore | factuality-focused |
| ALCE-ASQA | long-form QA with citations | str-em, MAUVE, citation precision/recall | official ALCE metrics |

## Baselines
| Baseline | Type | Why Important | Notes |
|---|---|---|---|
| Llama2 7B / 13B | non-retrieval LM | base pretrained reference | strong open models |
| Alpaca 7B / 13B | instruction-tuned LM | instruction-following reference | replicated on top of Llama2 |
| ChatGPT | proprietary LM | strong closed model comparator | no retrieval and retrieval-augmented variants both reported |
| Llama2-chat 13B | proprietary instruction-tuned LM | stronger chat baseline | retrieved and non-retrieved variants compared |
| Ret-ChatGPT / Ret-Llama2-chat | retrieval-augmented proprietary LMs | tests whether retrieval alone is enough | same augmentation pattern as other RAG baselines |
| Llama2-FT 7B | fine-tuned baseline | controls for training data only | trained on same data without reflection tokens |
| SAIL 7B | retrieval-trained method | compares to retrieval during training | uses retrieved passages prepended to instructions |
| Toolformer 6B | API-call / retrieval-like baseline | concurrent method for tool use | reported from paper numbers |
| CoVE 65B | iterative prompting baseline | strong factuality-oriented comparator | reported from concurrent work |

## Main Results
### Overall table from the paper
| Task | Best non-proprietary score | Self-RAG 7B | Self-RAG 13B |
|---|---:|---:|---:|
| PopQA | 48.7 | 54.9 | 55.8 |
| TriviaQA | 66.9 | 66.4 | 69.3 |
| PubHealth | 69.2 | 72.4 | 74.5 |
| ARC-Challenge | 65.8 | 67.3 | 73.1 |
| Biography FactScore | 78.2 | 81.2 | 80.2 |
| ASQA str-em | 34.8 | 30.0 | 31.7 |
| ASQA rouge | 36.7 | 35.7 | 37.0 |
| ASQA MAUVE | 57.9 | 74.3 | 71.6 |
| ASQA citation precision | 5.5 | 66.9 | 70.3 |
| ASQA citation recall | 7.5 | 67.8 | 71.3 |

### What the numbers mean
- The baseline column shows the strongest non-proprietary score for each metric, not one shared baseline model.
- Self-RAG is consistently stronger than non-retrieval LMs and usually stronger than retrieval-augmented baselines on factual and reasoning tasks.
- The biggest jump is on citation quality: ASQA citation precision and recall move from single digits or low tens in many non-proprietary baselines to the high 60s / low 70s.
- On ASQA exact-match-style scoring, the 13B model is not the single best non-proprietary model, but it matches or exceeds the best baseline on rouge and clearly dominates citation metrics.
- The paper also reports that Self-RAG outperforms ChatGPT on PopQA, biography generation, and ASQA rouge/MAUVE, while not uniformly winning every metric on every task.

## Ablations / Analysis
- Training ablations on a 50k subset show that removing the retriever hurts PopQA, PubHealth, and ASQA, and removing the critic hurts ASQA especially sharply.
- Inference ablations show that always taking the top retrieved passage is worse than critique-guided selection, especially on PopQA and ASQA.
- Removing the support critic (`cgr`) hurts ASQA, which supports the claim that fine-grained support checking matters beyond simple relevance.
- Soft weighting of critique signals lets users trade citation precision against fluency: increasing the support weight improves citation precision but tends to reduce MAUVE.
- Adaptive retrieval changes the retrieval-frequency versus accuracy curve, with the effect depending on the task.
- Data scaling helps, especially on PopQA and ASQA, and the authors note that performance may continue to improve with more than the 150k training examples used here.
- Human evaluation on sampled PopQA and bio outputs reports S&P scores of 92.5 and 70.0, with relevance and support judgments broadly aligned with GPT-4-derived labels.

## Implementation Clues
- Base generator models: Llama2 7B and 13B.
- Base critic model: Llama2 7B.
- Retriever: Contriever-MS MARCO by default, retrieving up to 10 documents per input.
- Extra retrieval for some tasks: Google Programmable Search plus Wikipedia snippets for biography and open-domain QA; GTR-XXL top-5 docs for ASQA.
- Default inference weights: `crel = 1.0`, `cgr = 1.0`, `cuse = 0.5`.
- Default retrieval threshold: `0.2` for most tasks, `0` for ALCE because citations are mandatory.
- Beam width: 2 at the segment level; greedy token decoding within each segment.
- Training setup: 4 x A100 80GB, 3 epochs, batch size 128, peak LR `2e-5`, 3% warmup, bf16, DeepSpeed ZeRO-3, FlashAttention.
- Context length: 2,048 tokens for 7B, 1,524 for 13B.
- Inference hardware: 1-2 Quadro RTX 6000 GPUs with 24GB memory.
- Repo snapshot in this directory is just a placeholder README, so there were no code-level implementation details to inspect here.

## Limitations
- The paper explicitly notes that the system can still generate outputs that are not fully supported by the cited evidence.
- Retrieval quality is a bottleneck: off-the-shelf retrievers trained on knowledge-intensive tasks are less effective for open-ended generation.
- The reported training set is large but finite; the appendix suggests that more data may further improve the model.
- Some downstream settings create metric tradeoffs, such as citation precision versus fluency on ASQA.
- The method improves verifiability, but it does not eliminate the need for human checking on high-stakes claims.

## Takeaways
- Self-RAG is best understood as an LM that learns a small control policy over retrieval and self-critique, not just a better retriever.
- The offline critic plus reflection-token training loop is the main technical contribution; it avoids needing a separate critic at inference.
- The strongest practical benefit is controllability: you can tune retrieval frequency and critique weights without retraining the model.
- The paper is strongest where factual grounding matters most, and weaker when tasks reward open-ended generation without easy evidence support.

## Open Questions
- How much of the gain comes from the reflection-token scheme versus the specific training data mixture?
- Would stronger retrievers or joint retriever-LM training change the balance between citation quality and fluency?
- How stable are the reflection-token behaviors when moved to newer base models or domains outside the paper's training mix?
- Can the same approach scale cleanly to longer-form generation where support checking is more complex than sentence-level critique?

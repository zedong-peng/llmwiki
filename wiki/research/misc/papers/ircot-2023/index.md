---
title: "Interleaving Retrieval with Chain-of-Thought Reasoning for Knowledge-Intensive Multi-Step Questions"
domain: research
area: misc
type: paper
status: processed
updated: 2026-04-18
tags: [paper, misc, retrieval, chain-of-thought, multihop-qa, open-domain-qa]
---
# Interleaving Retrieval with Chain-of-Thought Reasoning for Knowledge-Intensive Multi-Step Questions

## Paper Meta
- Title: Interleaving Retrieval with Chain-of-Thought Reasoning for Knowledge-Intensive Multi-Step Questions
- Authors: Harsh Trivedi, Niranjan Balasubramanian, Tushar Khot, Ashish Sabharwal
- Year: 2023
- Venue: not explicitly stated in the extracted TeX
- Topic: misc
- Paper Slug: ircot-2023
- arXiv: https://arxiv.org/abs/2212.10509
- PDF: 2212.10509.pdf
- Code Repo: https://github.com/stonybrooknlp/ircot
- Reading Source: TeX / source
- PDF Fallback: not used

## TL;DR
- IRCoT interleaves reasoning and retrieval: it generates one CoT sentence, retrieves more paragraphs from that sentence, then repeats until the model emits an answer or hits the step limit.
- The paper evaluates HotpotQA, 2WikiMultihopQA, MuSiQue, and IIRC with BM25 retrieval and GPT3 or Flan-T5 as the reasoning/reading models.
- Compared with one-step retrieval, IRCoT improves retrieval recall by 7.9-22.6 points with Flan-T5-XXL and by 11.3-22.6 points with GPT3, depending on dataset.
- QA improves by 5.0-15.3 F1 points on the main IID setup for Flan-T5-XXL, while GPT3 shows the largest gains on HotpotQA, 2WikiMultihopQA, and MuSiQue; GPT3 does not improve on IIRC.

## Problem
- One-step question-based retrieval is too coarse for multi-step questions because later evidence depends on earlier intermediate reasoning.
- The paper’s core claim is that retrieval and reasoning should condition on each other: retrieval should help produce the next reasoning step, and the next reasoning step should guide the next retrieval query.
- This is framed as an open-domain, few-shot QA problem where the knowledge source is large enough that a single query often misses the needed supporting paragraphs.

## Method
- Base pipeline: retrieve a small set of paragraphs with BM25, then alternate between a `reason` step and a `retrieve` step.
- `reason` step: feed the question, all retrieved paragraphs so far, and the CoT prefix into the LM; keep only the first generated sentence as the next reasoning step.
- `retrieve` step: use the last generated CoT sentence as the new query and retrieve more paragraphs; stop when the CoT contains `answer is:` or the step budget is exhausted.
- The method is model-agnostic as long as the LM can do zero/few-shot CoT generation; the paper instantiates it with GPT3 `code-davinci-002` and Flan-T5 sizes.
- For IIRC, the system first predicts relevant Wikipedia page titles from the main passage plus question, maps them with BM25, and then restricts paragraph retrieval to those pages.

## Benchmarks / Datasets
| Dataset / Benchmark | Task | Metric | Notes |
|---|---|---|---|
| HotpotQA | Open-domain multihop QA | gold-paragraph recall, answer F1 | Uses the Wikipedia corpus that ships with the dataset |
| 2WikiMultihopQA | Open-domain multihop QA | gold-paragraph recall, answer F1 | Corpus built from all supporting and non-supporting paragraphs across train/dev/test |
| MuSiQue (answerable subset) | Open-domain multihop QA | gold-paragraph recall, answer F1 | Corpus built from all available paragraphs across splits |
| IIRC (answerable subset) | Mixed open-domain / reading-comprehension QA | gold-paragraph recall, answer F1 | Main passage is always provided; supporting paragraphs are drawn from linked Wikipedia pages |

## Baselines
| Baseline | Type | Why Important | Notes |
|---|---|---|---|
| ZeroR QA / NoR QA | Retriever-less QA | Measures how far the LM gets from parametric knowledge alone | Used to expose hallucination and knowledge limits |
| OneR / One-step Retriever | Single retrieval pass | The main retrieval baseline IRCoT is trying to beat | Uses the question only as the query |
| Published ODQA systems | External comparison set | Provides leaderboard-style context | Includes InterAug, RECITE, ReAct, SelfAsk, DecomP, and DSP in the appendix |

## Main Results
### Gains over one-step retrieval
| Model | HotpotQA | 2WikiMultihopQA | MuSiQue | IIRC |
|---|---:|---:|---:|---:|
| IRCoT retrieval with Flan-T5-XXL | +7.9 recall | +14.3 recall | +3.5 recall | +10.2 recall |
| IRCoT retrieval with GPT3 | +11.3 recall | +22.6 recall | +12.5 recall | +21.2 recall |
| IRCoT QA with Flan-T5-XXL | +9.4 F1 | +15.3 F1 | +5.0 F1 | +2.5 F1 |
| IRCoT QA with GPT3 | +7.1 F1 | +13.2 F1 | +7.1 F1 | no gain reported on IIRC |

### Main published comparison
| Dataset / split | IRCoT GPT3 EM | IRCoT GPT3 F1 | Comparison in the paper |
|---|---:|---:|---|
| HotpotQA bridge | 45.8 | 58.5 | Compared against InterAug, RECITE, ReAct, SelfAsk, and DecomP |
| HotpotQA full | 49.3 | 60.7 | Leaderboard-style comparison only; not head-to-head |
| 2WikiMultihopQA | 57.7 | 68.0 | Strongest reported result in the main table |
| MuSiQue 2-hop | 34.2 | 43.8 | Strongest reported result in the main table |
| IIRC | 26.5 | 36.5 | Reported in the appendix comparison table |

### Nuance from the appendix
- The appendix updates the leaderboard with newer numbers: IRCoT remains SOTA on MuSiQue, but newer DecomP beats it on 2WikiMultihopQA and DSP beats it on HotpotQA by a small margin.
- The paper is careful that these comparisons are not strictly head-to-head because the systems use different corpora, APIs, LMs, and evaluation subsets.

## Ablations / Analysis
- Factual errors in GPT3 CoTs follow `NoR > OneR > IRCoT`; the paper reports about 50% fewer factual errors than OneR on HotpotQA and 40% fewer on 2WikiMultihopQA.
- Reader choice matters: Flan-T5-XXL works better with direct prompting, while GPT3 works better with CoT prompting.
- Removing the separate reader usually hurts performance, especially for Flan-T5-XXL; GPT3 is mixed, but the separate reader is still usually better or close.
- Scaling is favorable: IRCoT helps even small Flan-T5 models, and a 3B IRCoT model can outperform OneR and NoR with a 58x larger 175B GPT3 model on the QA task.

## Implementation Clues
- Retriever base: BM25 via Elasticsearch.
- Hyperparameters: OneR chooses `K` from `{5, 7, 9, 11, 13, 15}`; IRCoT uses per-step `K` from `{2, 4, 6, 8}` and `M` from `{1, 2, 3}` for distractor paragraphs in demonstrations.
- Retrieval budget: at most 15 paragraphs total; the paper reports `fixed-budget optimal recall` rather than standard ranked IR metrics.
- Prompting data: the authors manually wrote CoTs for 20 questions per dataset, then built 3 demonstration sets of 15 questions each and report mean plus standard deviation across them.
- Context limits: GPT3 `code-davinci-002` uses an 8K word-piece window; Flan-T5 is capped at 6K word pieces in the experiments.
- The source footnote points to `https://github.com/stonybrooknlp/ircot`, but this checkout has an empty local `repo/` directory, so no code files were available to read here.
- IIRC needs special handling: always include the main passage, predict page titles first, then scope retrieval inside the mapped Wikipedia pages.

## Limitations
- IRCoT depends on the base LM already being able to generate useful zero/few-shot CoT, which is weaker in smaller models.
- It also depends on long input windows because it has to keep multiple retrieved paragraphs plus demonstrations in context.
- The method adds compute because it makes an LM call for each reasoning sentence, so it is slower than one-shot retrieval.
- Some experiments used `code-davinci-002`, which the authors note was later deprecated, making exact reproduction harder.

## Takeaways
- Interleaving retrieval with reasoning is a robust way to reduce the mismatch between the evidence needed for the next step and the evidence fetched by a single question query.
- The gains are not just on retrieval metrics; they transfer into lower factual error rates and better downstream QA.
- The method is useful with both large and relatively small LMs, but the design is still constrained by context length and by the availability of CoT-capable prompting behavior.

## Open Questions
- How much of the gain comes from better query reformulation versus the extra context accumulated across steps?
- Can the pipeline be made cheaper by learning when to stop retrieving or by selecting fewer paragraphs before the reader step?

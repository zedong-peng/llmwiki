---
title: "Evoking User Memory: Personalizing LLM via Recollection-Familiarity Adaptive Retrieval"
domain: research
area: misc
type: paper
status: processed
updated: 2026-04-19
tags: [paper, misc, memory-retrieval, personalization, recollection, familiarity, rf-mem, iclr2026]
---
# Evoking User Memory: Personalizing LLM via Recollection-Familiarity Adaptive Retrieval

## Paper Meta
- Title: Evoking User Memory: Personalizing LLM via Recollection-Familiarity Adaptive Retrieval
- Authors: Yingyi Zhang, Junyi Li, Wenlin Zhang, Penyue Jia, Xianneng Li, Yichao Wang, Derong Xu, Yi Wen, Huifeng Guo, Yong Liu, Xiangyu Zhao
- Venue: not reported in the extracted source; the TeX uses the ICLR 2026 conference style
- Topic: misc
- Paper Slug: recollection-familiarity-retrieval-2026
- arXiv: https://arxiv.org/abs/2603.09250
- PDF: 2603.09250.pdf
- Code Repo: https://github.com/Applied-Machine-Learning-Lab/ICLR2026_RF-Mem
- Reading Source: TeX / source
- Repo Read: no local repo present in this workspace
- PDF Fallback: not used

## TL;DR
- RF-Mem is an uncertainty-gated dual-path memory retriever for personalized LLMs.
- It routes between fast \emph{Familiarity} retrieval and iterative \emph{Recollection} using probe mean score and entropy.
- On PersonaMem, PersonaBench, and LongMemEval, it generally improves over dense one-shot retrieval while keeping latency far below full-context prompting.

## Problem
- Personalized memory retrieval for LLMs is usually forced into one of two extremes: full-context prompting over all memories, or a single dense top-$K$ search.
- The first option is expensive and does not scale well; the second is fast but often shallow, because it cannot reconstruct chains of evidence.
- The paper frames this as a mismatch with human memory, where recognition can stay at \emph{Familiarity} or escalate to deliberate \emph{Recollection} when uncertainty rises.

## Method
- RF-Mem first runs a probe retrieval over the user's memory store and computes a temperature-scaled score distribution.
- It measures the familiarity signal with the mean score and entropy $H(p)$; if $\bar{s} \ge \theta_{\text{high}}$ or $H(p) \le \tau$, it returns the one-shot \emph{Familiarity} path.
- If $\bar{s} \le \theta_{\text{low}}$ or $H(p) > \tau$, it enters \emph{Recollection}: top-$N$ candidates are clustered with KMeans, cluster centroids are mixed with the query via $\alpha$, and retrieval iterates under beam width $B$, fanout $F$, and round limit $R$.
- The intended effect is chain-like evidence reconstruction in embedding space without paying the cost of full-context prompting.

## Benchmarks / Datasets
| Dataset / Benchmark | Task | Metric | Notes |
|---|---|---|---|
| PersonaMem | Personalized generation over long user histories | Accuracy | 32K, 128K, and 1M memory corpora; turn-level memory construction |
| PersonaBench | Retrieval from private user documents and interactions | Recall@5, Recall@10 | Multi-qa MiniLM, MPNet, and BGE backbones |
| LongMemEval | Long-term interactive memory retrieval | Recall@5, Recall@10, Recall@50 | Small and medium corpora; recall-focused evaluation |

## Baselines
| Baseline | Type | Why Important | Notes |
|---|---|---|---|
| Zero Memory | No retrieval | Lower bound | Answers without user memory |
| Full Context | No retrieval / full prompt | Upper-context comparison | Feeds all history into the model; becomes out-of-context at 1M PersonaMem |
| Dense Retrieval / Familiarity | One-shot top-$K$ | Main fast baseline | Corresponds to the Familiarity path |
| Recollection | Iterative retrieval | Slow-path baseline | Uses the recollection branch without gating |

## Main Results
| Dataset / Benchmark | Metric | Baseline | Ours | Gain / Delta | Notes |
|---|---|---|---|---|---|
| PersonaMem 32K | Overall accuracy | Dense 0.5908 | RF-Mem 0.6350 | +0.0442 | Full Context 0.6129; RF-Mem uses 3,566.6 avg tokens |
| PersonaMem 128K | Overall accuracy | Dense 0.5259 | RF-Mem 0.5394 | +0.0135 | Full Context 0.3231; RF-Mem remains stable at scale |
| PersonaMem 1M | Overall accuracy | Dense 0.4518 | RF-Mem 0.4589 | +0.0071 | Full Context is out of context |
| PersonaBench MiniLM | Recall@10 overall | Dense 0.5964 | RF-Mem 0.6071 | +0.0107 | RF-Mem is best overall under this retriever |
| PersonaBench MPNet | Recall@10 overall | Dense 0.5333 | RF-Mem 0.5553 | +0.0220 | Recollection is 0.5527 |
| PersonaBench BGE | Recall@10 overall | Dense 0.5002 | RF-Mem 0.5089 | +0.0087 | RF-Mem matches or exceeds the strongest baseline overall |
| LongMemEval-S MiniLM | Recall@50 | Dense 0.9761 | RF-Mem 1.0000 | +0.0239 | RF-Mem time 39.58ms; Recollection 50.62ms |
| LongMemEval-M BGE | Recall@50 | Dense 0.8305 | RF-Mem 0.8329 | +0.0024 | RF-Mem time 44.74ms; strong at larger corpus |

## Ablations / Analysis
- The gating hyperparameters are stable in the reported setup: PersonaMem uses $\lambda=20$, $B=3$, $F=2$, $\theta_{\text{high}}=0.6$, $\theta_{\text{low}}=0.3$; PersonaBench uses $\lambda=30$, $B=3$, $F=1$ or $2$, $\theta_{\text{high}}=0.6$, $\theta_{\text{low}}=0.0$; LongMemEval uses $\lambda=20$, $B=4$, $F=1$, $\theta_{\text{high}}=0.6$, $\theta_{\text{low}}=0.0$.
- Sensitivity on PersonaBench shows moderate $\alpha$ is best: roughly $0.3$--$0.6$ for Recall@5, while larger $\alpha$ helps Recall@50 by expanding deeper coverage.
- Sensitivity on $\tau$ shows moderate thresholds are best; too low triggers recollection too often, too high collapses back to Familiarity.
- Beam/fanout analysis on LongMemEval suggests small beams and low fanout, typically $B=2$ or $3$ with $F=1$ or $2$, give the best precision/coverage balance.
- Probe-size analysis shows performance is stable once $K$ is in the 10--20 range; the paper says the gains saturate beyond moderate probe sizes.
- The appendix also tests a learned gate: it has more room to improve with more data, but the hand-tuned thresholds are slightly better in the reported experiments.

## Implementation Clues
- Experiments run on a single NVIDIA A100 with Ubuntu, and runtime is measured with the GPU exclusively allocated to the process.
- PersonaMem uses the turn-level memory corpus with an \texttt{advanced LLM} generator and \texttt{multi-qa-MiniLM-L6-cos-v1} retriever.
- PersonaBench and LongMemEval are evaluated under multiple retrievers: \texttt{multi-qa-MiniLM-L6-cos-v1}, \texttt{all-MiniLM-L6-v2}, and \texttt{bge-base-en-v1.5}.
- The paper states that the similarity distribution is light-tailed and that the median familiarity statistics remain stable across corpus sizes, which motivates fixed thresholds.
- The source cites a code repository at `https://github.com/Applied-Machine-Learning-Lab/ICLR2026_RF-Mem`, but no local repo checkout was present here, so repository-level inspection was not possible.

## Limitations
- Recollection can drift toward coherent but irrelevant clusters, as shown in the failure case where the slow path over-focuses on financial-management memories instead of travel intent.
- The method depends on hand-set thresholds and retrieval hyperparameters in the reported setup, even though the appendix shows the gate can potentially be learned.
- Recollection improves coverage but increases latency, so it is not uniformly better than Familiarity on easy or highly aligned queries.
- The paper evaluates on simulated or benchmarked personal-memory datasets, not on live private user data.

## Takeaways
- The main contribution is not a new embedding model; it is a routing policy that decides when dense retrieval is enough and when structured expansion is needed.
- RF-Mem is modular: the paper shows it can sit on top of raw turn-level memory, MemoryBank summaries, HyDE-style query expansion, and iterative retrieval pipelines.
- The strongest result is a practical tradeoff: near one-shot latency on easy cases, with better recall or accuracy on harder cases that need deeper context reconstruction.

## Open Questions
- Can the gating policy be learned robustly enough to remove manual thresholds without losing stability?
- How well does the approach transfer from benchmarked synthetic memory to real user histories with stronger privacy and noise constraints?
- Would a richer graph-based or learned recollection operator outperform KMeans plus $\alpha$-mixing without raising latency too much?

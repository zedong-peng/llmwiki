---
title: "Parallelizing Linear Transformers with the Delta Rule over Sequence Length"
domain: research
area: linear-attention
type: paper
status: processed
updated: 2026-04-21
tags: [paper, misc, linear-attn, deltanet, delta-rule, householder]
---

# Parallelizing Linear Transformers with the Delta Rule over Sequence Length

> Status: processed from local TeX/PDF on 2026-04-21.

## Paper Meta
- Title: Parallelizing Linear Transformers with the Delta Rule over Sequence Length
- Authors: Songlin Yang, Bailin Wang, Yu Zhang, Yikang Shen, Yoon Kim
- Year: 2024
- Venue: NeurIPS 2024
- Paper Slug: deltanet-2024
- arXiv: https://arxiv.org/abs/2406.06484
- Reading source: `source/extracted/neurips_2024.tex`, `sections/intro.tex`, `sections/background.tex`, `sections/method.tex`, `sections/experiment.tex`, `sections/conclusion.tex`

## Local Assets
- PDF: `2406.06484.pdf`
- Source archive: `source/archives/2406.06484-source.tar.gz`
- Extracted source: `source/extracted/`
- Repo: no paper-specific official public repository identified during this import pass

## TL;DR
- DeltaNet replaces the additive update in vanilla linear attention with a delta-rule write, so the memory can both remove obsolete associations and add new ones.
- The main technical contribution is a memory-efficient, chunkwise-parallel training algorithm based on a generalized Householder / WY reparameterization.
- The paper’s practical message is simple: the delta-rule model improves retrieval-heavy behavior, but only becomes useful at scale once the training algorithm is parallelized across sequence length.

## Problem
- Vanilla linear attention is efficient, but its purely additive update has poor memory capacity and collides when the number of associations exceeds state size.
- Existing DeltaNet training was sequential over sequence length, so the model’s better recall properties were not enough to make it hardware efficient.
- The paper is trying to close that gap: keep the delta-rule update, but make training parallel enough to run on modern GPUs.

## Method
- The paper rewrites DeltaNet as a matrix-valued recurrence with a generalized Householder transformation: `S_t = S_{t-1}(I - \beta_t k_t k_t^T) + \beta_t v_t k_t^T`.
- Using the WY representation for products of Householder matrices, the authors derive a memory-efficient pseudo-value construction that avoids materializing the full `d x d` hidden state at each step.
- They then derive a chunkwise parallel form, where chunk-level state transitions and outputs can be computed with matrix operations while recomputing hidden states in backward pass to save memory.
- A UT transform is used to rewrite most of the remaining work into matmuls, which is what makes the Triton implementation practical.

## Results
- On synthetic benchmarks, DeltaNet performs strongly on MQAR and is better than Mamba and other baselines on the harder recall settings; it is especially competitive on fuzzy recall in MAD.
- On language modeling, a 1.3B DeltaNet trained on 100B tokens outperforms Mamba and GLA on perplexity and zero-shot downstream tasks.
- On recall-intensive real tasks such as SWDE, FDA, and SQuAD, DeltaNet is better than GLA at the same state size in the 340M setting, but that advantage weakens at 1.3B because the state-size scaling is poorer.
- Hybrid models help: adding sliding-window attention or a small amount of global attention beats strong Transformer++ baselines.
- Training throughput is close to GLA and clearly faster than Mamba, which is the practical payoff of the chunkwise algorithm.

## Limitations
- The paper is explicit that DeltaNet still trails GLA in training speed because state-to-state dependencies force head-dimension marginalization inside the kernel.
- The state-size scaling is weaker than GLA and RetNet, which hurts recall-heavy tasks at larger scales.
- Length generalization is also weaker than some gated linear models, and the authors suggest adding gating or block-diagonal Householder structure as future work.

## Takeaways
- DeltaNet is the delta-rule branch of the linear-attention family that is most useful when recall matters more than pure additive memory.
- The key contribution is not just the model update rule, but the parallel training reformulation that makes the model trainable at scale.
- For the current linear-attention reading queue, this paper is one of the clearest bridges between algorithm design, memory capacity, and GPU implementation constraints.

---
title: "Gated Linear Attention Transformers with Hardware-Efficient Training"
domain: research
area: linear-attention
type: paper
status: processed
updated: 2026-04-21
tags: [paper, misc, linear-attn, gla, gating, hardware-efficient-training]
---

# Gated Linear Attention Transformers with Hardware-Efficient Training

## Paper Meta
- Title: Gated Linear Attention Transformers with Hardware-Efficient Training
- Authors: Songlin Yang, Bailin Wang, Yikang Shen, Rameswar Panda, Yoon Kim
- Year: 2024
- Venue: ICML 2024
- Paper Slug: gla-2024
- arXiv: https://arxiv.org/abs/2312.06635

## TL;DR
- GLA is the clearest paper in this line to show that linear attention can recover a useful form of data-dependent gating without giving up chunkwise parallel training.
- The key systems contribution is `FlashLinearAttention`: an I/O-aware algorithm that makes linear attention faster than `FlashAttention-2` on short sequences and still competitive at longer ones.
- On the modeling side, GLA beats RetNet and is competitive with a strong Transformer++ baseline on several language-modeling and recall-oriented benchmarks.

## Problem
- Vanilla linear attention has a recurrent form, but naive implementations are slow in practice because the update is not I/O-aware and tends to underuse GPU tensor cores.
- Existing decay-based variants such as RetNet improve the recurrence, but their gates are data-independent and still leave performance on the table.
- The paper asks for a model that keeps linear-time inference, trains efficiently on modern GPUs, and improves the quality gap versus softmax Transformers.

## Method
- The base linear-attention state update is `S_t = S_{t-1} + k_t^T v_t`, which makes linear attention look like an RNN with matrix-valued hidden state.
- GLA replaces the simple decay with a data-dependent gate `G_t = alpha_t^T 1`, leading to `S_t = (alpha_t^T 1) ⊙ S_{t-1} + k_t^T v_t`.
- The full gate uses a low-rank parameterization `alpha_t = sigmoid(x_t W_{alpha_1} W_{alpha_2})^(1/tau)`, with `W_{alpha_1} in R^{d x 16}` and `W_{alpha_2} in R^{16 x d_k}` to keep the parameter count controlled.
- The paper derives a chunkwise parallel form for both vanilla linear attention and GLA so training can use matmuls and tensor cores instead of a pure recurrent scan.
- For GLA, the authors add secondary-level chunking to recover tensor-core-friendly matmuls even though the gated formulation is less stable in naive log-space form.

## Experiments
- Main training setup uses SlimPajama with the Mistral tokenizer, training from scratch at 340M/1.3B parameters on 15B/100B tokens.
- The baseline set is Transformer++, RetNet, and Mamba, all trained on the same data and token budget.
- In the main benchmark table, GLA reaches 28.65 WikiText perplexity at 340M and 17.22 at 1.3B, versus 32.33/18.64 for RetNet and 28.39/17.06 for Mamba.
- On the zero-shot average across the downstream set, GLA gets 41.5 at 340M and 51.0 at 1.3B, beating RetNet and slightly edging the Transformer++ baseline at 1.3B.
- On recall-heavy tasks, GLA is materially better than RetNet and Mamba on FDA, SWDE, and SQuAD at both scales, with the strongest 1.3B result being 42.6 on SQuAD.
- The length-extrapolation plots show GLA generalizes better than Mamba when trained on 2K contexts, and an 8K training regime improves extrapolation for all linear-time models.

## Implementation Clues
- `FlashLinearAttention` has two modes: a non-materialization version that keeps state in SRAM and a materialization version that stores chunk states in HBM to increase sequence-level parallelism.
- The materialization version is the one used for the best throughput setting in the paper, and recomputation is used to lower the memory footprint.
- The paper explicitly treats I/O awareness, tiling, and tensor-core utilization as the decisive hardware constraints, not just FLOP count.
- Appendix material shows the general gated form can also be expressed with a parallel form and chunkwise form for more expressive gates than the simplified main-text version.

## Limits
- The strongest experiments are still moderate scale, so the paper does not settle how far GLA scales beyond the 1.3B / 100B-token regime.
- The gating formulation improves quality and recall, but the authors still frame the design as a compromise between expressivity, stability, and tensor-core friendliness.
- The paper notes that some training settings require materialization, which adds a memory cost even when recomputation keeps it practical.

## Takeaways
- GLA is an important bridge between early linear attention and later gated/delta-rule lines: it preserves the linear recurrence but makes the gate data-dependent.
- The paper is also a key systems reference because it shows that a careful chunkwise implementation can make linear attention competitive on real GPUs.
- For this wiki, the most reusable facts are the recurrent update, the chunkwise algorithm idea, the secondary-level chunking trick, and the main benchmark deltas against RetNet and Mamba.

## Local Assets
- PDF: `2312.06635.pdf`
- Source archive: `source/archives/2312.06635-source.tar.gz`
- Extracted source: `source/extracted/`
- Repo: no paper-specific official public repository identified during this import pass


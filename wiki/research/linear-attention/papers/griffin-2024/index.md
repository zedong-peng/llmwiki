---
title: "Griffin: Mixing Gated Linear Recurrences with Local Attention for Efficient Language Models"
domain: research
area: linear-attention
type: paper
status: processed
updated: 2026-04-21
tags: [paper, misc, linear-attn, griffin, hawk, gated-linear-recurrence]
---

# Griffin: Mixing Gated Linear Recurrences with Local Attention for Efficient Language Models

> Status: fully read from local TeX and PDF assets on 2026-04-21.

## Paper Meta
- Title: Griffin: Mixing Gated Linear Recurrences with Local Attention for Efficient Language Models
- Authors: Soham De, Samuel L. Smith, Anushan Fernando, Aleksandar Botev, George Cristian-Muraru, Albert Gu, and others
- Year: 2024
- Venue: arXiv preprint
- Paper Slug: griffin-2024
- arXiv: https://arxiv.org/abs/2402.19427

## Local Assets
- PDF: `2402.19427.pdf`
- Source archive: `source/archives/2402.19427-source.tar.gz`
- Extracted source: `source/extracted/`
- Repo: no paper-specific official public repository identified during this import pass

## TL;DR
- Griffin is a hybrid model that replaces global MQA with a mix of RG-LRU recurrent blocks and local attention.
- Hawk is the pure recurrent variant; Griffin is the hybrid variant that keeps some local attention for better retrieval behavior.
- The paper's central claim is that these models preserve Transformer-like scaling and training efficiency while improving inference throughput and long-context behavior.

## Problem
- Global attention is expensive to train and infer at long sequence lengths because compute and KV cache both scale poorly.
- Pure recurrent models fix the cache problem, but they often lag on optimization, downstream quality, or exact retrieval/copying.
- The paper targets that tradeoff directly: keep the fixed-state efficiency of recurrence, but recover enough local attention to match stronger Transformer baselines.

## Method
- The core recurrent primitive is RG-LRU, a gated linear recurrent layer inspired by LRU and gated RNNs.
- Each residual block contains RMSNorm, temporal mixing, another RMSNorm, and an MLP, mirroring the pre-norm Transformer layout.
- Hawk uses only recurrent blocks for temporal mixing; Griffin mixes recurrent blocks with local sliding-window attention.
- The recurrent path uses a small Conv1D front-end before RG-LRU, and the paper notes that complex-valued recurrences were not helpful here.

## Results
- Training-scale curves are power-law-like up to and beyond 7B parameters, and Griffin reaches the lowest held-out loss across FLOPs budgets.
- The paper trains models from 100M to 7B, plus a 14B Griffin, and overtrains Hawk/Griffin on 300B tokens for downstream evaluation.
- Hawk-3B beats the reported Mamba-3B downstream performance despite using half as many training tokens.
- Griffin-7B and Griffin-14B match Llama-2 while using roughly 7x fewer tokens, which is the headline quality result.
- On inference, Hawk and Griffin beat the MQA Transformer on both latency and throughput, with the gap widening for longer samples and larger batches.
- For long-context modeling, both models extrapolate to at least 4x the training length, and 8k-trained variants do better on 8k+ evaluation than 2k-trained ones.
- On synthetic copying and retrieval, Griffin is much stronger than Hawk: it avoids the large slowdown on selective copying and keeps strong induction-head behavior.

## Implementation Clues
- The paper is explicit that device efficiency depends on a custom RG-LRU kernel.
- On TPU-v3, the authors implement the recurrent update with a Pallas linear scan rather than a naive JAX implementation.
- That kernel gives nearly 3x speedup over the naive JAX scan, and the paper says associative scan can be up to 50% slower.
- Training efficiency on TPU-v3 is described as comparable to Transformers because the custom kernel reduces memory transfers for the diagonal recurrent layer.
- The appendix also gives the TPU-v3 pod limits that motivate the memory-bound framing: 32 GB HBM, 900 GB/s bandwidth, and 136 FLOPs/byte peak MXU ratio.

## Limitations
- Hawk remains weak on exact copying/retrieval when evaluated on pretrained models, because its fixed-size state does not scale with context.
- Griffin improves that behavior, but only up to the point where the local attention window covers the relevant context.
- The paper itself says the copying/retrieval results still leave room for better long-horizon memory mechanisms.

## Takeaways
- Griffin is a strong bridge paper between pure recurrent models and hybrid long-context systems.
- For this wiki, it is most useful as the RecurrentGemma / Hawk precursor and as evidence that a carefully engineered recurrent kernel can be competitive with Transformer baselines.
- The most reusable numbers from the paper are 14B scale, 300B-token overtraining, 3x scan speedup, 4x extrapolation, and the Llama-2 / Mamba comparison points.

## Open Questions
- How much of Griffin's quality gain comes from the hybrid local-attention layer versus the RG-LRU recurrence itself?
- Would the same training recipe transfer to GPU kernels as cleanly as it does to TPU-v3 Pallas?
- Is the copy/retrieval degradation primarily a window-size issue, or does the recurrent state still need a better readout mechanism?

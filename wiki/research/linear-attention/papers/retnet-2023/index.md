---
title: "Retentive Network: A Successor to Transformer for Large Language Models"
domain: research
area: linear-attention
type: paper
status: processed
updated: 2026-04-21
tags: [paper, misc, linear-attn, retnet, retention, torchscale]
---

# Retentive Network: A Successor to Transformer for Large Language Models

> Status: processed from local TeX and repo assets on 2026-04-21.

## Paper Meta
- Title: Retentive Network: A Successor to Transformer for Large Language Models
- Authors: Yutao Sun, Li Dong, Shaohan Huang, Shuming Ma, Yuqing Xia, Jilong Xue, Jianyong Wang, Furu Wei
- Year: 2023
- Venue: NeurIPS 2023
- Paper Slug: retnet-2023
- arXiv: https://arxiv.org/abs/2307.08621
- Official repo: https://github.com/microsoft/torchscale

## Local Assets
- PDF: `2307.08621.pdf`
- Source archive: `source/archives/2307.08621-source.tar.gz`
- Extracted source: `source/extracted/`
- Repo: `repo/torchscale/`

## TL;DR
- RetNet is the paper that makes the "impossible triangle" explicit: training parallelism, strong performance, and low-cost inference are usually in tension, and the retention mechanism is the proposed way to get all three.
- The key move is a single recurrence that can be expressed three ways: parallel for training, recurrent for decoding, and chunkwise recurrent for long sequences.
- In this repo, `torchscale` is the practical implementation anchor for the RetNet line, with a first-class `RetNetDecoder` exposed in the library README.

## Problem
- Standard Transformers train well but pay for it at inference time through KV-cache growth, memory traffic, and longer decoding latency.
- Prior linearized-attention and recurrent alternatives improve one axis but usually lose either modeling quality or training parallelism.
- RetNet is positioned as a foundation architecture that keeps the Transformer-like optimization path while removing the inference bottleneck.

## Method
- The paper derives a recurrence `s_n = A s_{n-1} + K_n^T v_n` and then rewrites it into a retention operator with content-aware `Q`, `K`, and exponential decay.
- The parallel form computes `Retention(X) = (QK^T \odot D)V`, where the causal mask and decay live in one matrix `D`.
- The recurrent form uses `S_n = \gamma S_{n-1} + K_n^T V_n`, which gives `O(1)` decoding per step.
- The chunkwise recurrent form splits long sequences into chunks and combines intra-chunk parallel computation with inter-chunk recurrence.

## Results
- On training cost at 8k sequence length, RetNet is more memory-efficient than Transformer and competitive with Transformer + FlashAttention across 1.3B, 2.7B, 6.7B, and 13B models.
- On inference, the paper reports length-invariant memory, throughput, and latency behavior for RetNet, while Transformer degrades as the KV cache grows.
- The headline 7B / 8k comparison is strong: RetNet is reported to decode 8.4x faster and use 70% less memory than Transformer with KV cache.
- The paper also reports 25-50% training-memory savings and about 7x training speedup versus standard Transformer, while staying competitive with FlashAttention.
- Against efficient Transformer variants, RetNet has better perplexity than RWKV, H3, Hyena, and Linear Transformer on the in-domain and out-of-domain evaluation sets shown in the paper.

## Design Signals
- The gated multi-scale retention block matters: the ablation shows drops when removing the swish gate, GroupNorm, gamma decay, or multi-scale decay.
- Larger head dimension helps, which the authors interpret as more memory capacity in the recurrent state.
- The paper’s comparison section is useful because it separates algorithmic complexity from the practical cost of implementing the state update.

## Implementation Clues
- `torchscale` already exposes `RetNetConfig` and `RetNetDecoder`, so this paper is not just conceptual; it has a usable code path in the local repo.
- The README frames RetNet as one of the core architecture families in the library alongside DeepNet, Magneto, LongNet, and other foundation-model building blocks.
- For this wiki thread, RetNet is the clean bridge between early linear attention and later gated / SSM-style systems work.

## Takeaways
- RetNet is the strongest early statement that retention can unify training and inference requirements without collapsing into a pure approximation of attention.
- The paper is still useful today because the central tradeoff it isolates is exactly the one that later linear-attention kernel and hardware papers try to attack.
- If I need one historical anchor before Mamba-2, DeltaNet, or FLA, this is the one to keep.

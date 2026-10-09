---
title: "Retentive Network: A Successor to Transformer for Large Language Models"
domain: research
area: linear-attention
type: paper
status: active
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
- PDF: `paper-pdf/2307.08621.pdf`
- Source archive: `paper-tex/archives/2307.08621-source.tar.gz`
- Extracted source: `paper-tex/extracted/legacy/`
- Repo: `github-repo/torchscale/`

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

## 迁移来源与阅读边界

本页保留历史实质阅读笔记；本次迁移没有重新阅读或执行研究代码。原归档的书目信息、版本、hash、仓库 commit 与 metadata 快照见 [citation.bib](citation.bib)。
旧 metadata 将 reading.status 记为 `not_started`，与上述历史笔记及来源描述不一致；保留两者作为历史记录，具体阅读范围以上述已记载内容为限，不补写未记录的范围。
仓库缓存的 commit 与检索日期保留在 citation.bib；恢复的当前缓存不证明历史阅读时所用 revision，原笔记未记录的历史 commit 仍未知。
书目字段来自旧记录，作者列表及发表信息尚未在本次迁移复核。原文下载版本未记录时，不根据 slug 或文件名猜测版本。
旧 topic 目录称 Arxiv，原笔记称 NeurIPS 2023，发表信息存在冲突，待原始来源核对。

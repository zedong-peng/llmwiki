---
title: "FLA: A Triton-Based Library for Hardware-Efficient Implementations of Linear Attention Mechanism"
domain: research
area: linear-attention
type: engineering
status: active
updated: 2026-04-21
tags: [engineering, misc, linear-attn, fla, triton, kernels]
---

# FLA: A Triton-Based Library for Hardware-Efficient Implementations of Linear Attention Mechanism

> Status: repo-first source note processed from the local `flash-linear-attention` repository on 2026-04-21.

## TL;DR
- FLA is the practical Triton baseline for linear-attention kernels, not a single algorithm paper.
- The repo unifies RetNet, GLA, DeltaNet, Mamba2, Gated DeltaNet, RWKV6/7, Samba, MoBA, and related variants into one implementation stack.
- For this wiki, its main value is as an executable comparison point for kernel quality, benchmark design, and model coverage.

## Problem
- Linear-attention research has fragmented into multiple model families, but the implementation problem is shared: which kernels actually run fast on modern GPUs and vendor backends?
- The repo addresses that by packaging efficient PyTorch/Triton implementations for sequence modeling across linear attention, SSM-style models, and hybrids.
- The README explicitly frames the project as platform-agnostic and says verified platforms include NVIDIA, AMD, and Intel.

## Method
- FLA organizes its code around reusable kernels and fused modules rather than one monolithic model implementation.
- The README model table maps many published architectures directly into `fla` layers or model wrappers, including RetNet, GLA, DeltaNet, Mamba2, Gated DeltaNet, RWKV6, RWKV7, Samba, and MoBA.
- The benchmark registry exposes named ops such as `chunk_retention`, `chunk_linear_attn`, `chunk_gla`, `chunk_delta_rule`, `chunk_gdn`, `chunk_kda`, `chunk_rwkv6`, `chunk_rwkv7`, and `chunk_dplr_delta_rule`.
- That registry makes the repo a usable baseline harness instead of just a code dump.

## Results
- The README reports benchmarks on a single NVIDIA GB200 GPU with CUDA 12.9 and PyTorch 2.9.0, which grounds the performance claims in a concrete environment.
- In the forward table, `chunk_retention`, `chunk_gla`, and `chunk_gdn` are often competitive with FlashAttention2, but the winner depends heavily on shape.
- In the backward table, the same ops show large shape sensitivity, which is useful because it exposes the practical tradeoff surface rather than hiding it behind one headline number.
- The README also shows end-to-end usage for GLA and Samba-style hybrid configurations, so the repo is directly actionable for model construction.

## Implementation Clues
- The project currently ships as `fla-core` plus `flash-linear-attention`, with the latter depending on transformers and the former depending only on PyTorch, Triton, and einops.
- `ENVs.md` exposes backend and precision knobs such as `FLA_CONV_BACKEND`, `FLA_USE_TMA`, `FLA_USE_FAST_OPS`, `FLA_CACHE_RESULTS`, and `FLA_TRIL_PRECISION`.
- The benchmark suite is structured around `benchmarks/ops/run.py` and `benchmarks/ops/registry.py`, which makes it easy to compare kernels by op name and shape config.
- The repo README also links the official upstream implementation for many models, so FLA doubles as a map from paper names to practical kernel entry points.

## Limitations
- This is a repo-first systems note, not a formal paper with standalone methodological claims.
- The README is broad and release-note-like, so some evidence is benchmark driven rather than derived from controlled ablations.
- Because the repository covers many model families, the boundary between paper-specific code and shared kernel infrastructure is sometimes blurry.

## Takeaways
- FLA is the best local baseline for checking whether a new linear-attention idea is actually kernel-ready.
- The important comparison is not only algorithm versus algorithm, but also which op family can be expressed cleanly in Triton and benchmarked across backends.
- This note should remain the canonical systems reference whenever another linear-attention paper needs a practical implementation anchor.

## Source Notes
- Repo: `github-repo/flash-linear-attention/`
- Core source: `README.md`
- Benchmark registry: `benchmarks/ops/registry.py`
- Environment controls: `ENVs.md`

## 迁移来源与阅读边界

本页保留历史实质阅读笔记；本次迁移没有重新阅读或执行研究代码。原归档的书目信息、版本、hash、仓库 commit 与 metadata 快照见 [citation.bib](citation.bib)。
旧 metadata 将 reading.status 记为 `not_started`，与上述历史笔记及来源描述不一致；保留两者作为历史记录，具体阅读范围以上述已记载内容为限，不补写未记录的范围。
仓库缓存的 commit 与检索日期保留在 citation.bib；恢复的当前缓存不证明历史阅读时所用 revision，原笔记未记录的历史 commit 仍未知。
书目字段来自旧记录，作者列表及发表信息尚未在本次迁移复核。原文下载版本未记录时，不根据 slug 或文件名猜测版本。

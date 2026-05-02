---
title: "FlexLinearAttention: Compiling a Unified Abstraction into Scalable Kernels for Linear Attention"
domain: research
area: linear-attention
type: paper
status: processed
updated: 2026-04-21
tags: [paper, misc, linear-attn, flexla, forge, compiler, triton]
---

# FlexLinearAttention: Compiling a Unified Abstraction into Scalable Kernels for Linear Attention

> Status: PDF-first ingest complete. This note is based on the local paper PDF only; there is no arXiv TeX source.

## Paper Meta
- Title: FlexLinearAttention: Compiling a Unified Abstraction into Scalable Kernels for Linear Attention
- Authors: Haojie Duanmu, Size Zheng, Ningxin Zheng, Jianqiao Lu, Xuegui Zheng, Xingcheng Zhang, Li-Wen Chang, Xin Liu, Dahua Lin
- Year: 2026
- Venue: ICLR 2026 Poster (OpenReview)
- Paper Slug: flexla-forge-2025
- OpenReview: https://openreview.net/forum?id=N4jJQvQSiN

## Local Assets
- PDF: `9282_FlexLinearAttention_Compi.pdf`
- Source archive: none publicly exposed through arXiv
- Repo: no official public repository found during this import pass

## TL;DR
- FlexLA is a domain-specific compiler for linear attention that turns a small three-phase PyTorch abstraction into Triton-based kernels.
- The key idea is to split every supported variant into `chunk_mode`, `decay_mode`, and `merge_mode`, then lower that structure into fused compute-communication kernels.
- The paper’s main claim is that this gives both usability and speed: a few dozen lines of user code can produce kernels that match or beat hand-tuned baselines while also scaling across distributed clusters.

## Problem
- Linear attention has grown into a fragmented ecosystem: Mamba, RetNet, RWKV, GLA, Gated DeltaNet, and related variants share structure but differ enough that each one typically needs bespoke kernel work.
- Existing optimized libraries such as FLA improve single-device execution, but they still depend on manual expert implementations and do not solve distributed scaling cleanly.
- The paper treats that combination of rapid algorithmic churn and hand-written kernel maintenance as the core bottleneck.

## Method
- FlexLA defines a linear-attention-specific programming abstraction around three canonical phases: intra-chunk computation, inter-chunk state propagation, and merging/output generation.
- Users write idiomatic PyTorch callables for `chunk_mode`, `decay_mode`, and `merge_mode`; the compiler traces them into `torch.fx`, applies domain-specific rewrites, and lowers the result into Triton code.
- The backend targets Triton-Distributed rather than plain Triton so it can fuse communication into computation at tile granularity, use OpenSHMEM-style communication primitives, and avoid host-side synchronization overhead.
- FlexLA also adds system-level machinery: AOT compilation with a static dispatcher and an adaptive parallelism scheduler that chooses among fusion and tiling tradeoffs.

## Results
- The paper reports 1.01x to 4.9x speedups over the state-of-the-art FLA library on a single GPU.
- In the main distributed benchmark, FlexLA reduces latency from 34.6 seconds in PyTorch eager mode to 9.2 ms, and to 2.7 ms on 4 GPUs.
- For weak scaling, the paper reports near-linear behavior up to 128 GPUs and up to 7.2x better throughput than the strongest open-source distributed baseline.
- On an H100 cluster, FlexLA continues to beat LASP-2, including a 1.17x win at 16k sequence length on 4 GPUs, and it remains far faster than Ring-Attention at large global sequence lengths.

## Implementation Clues
- The abstraction is intentionally aligned with chunk-wise parallel forms, which means the compiler can separate local per-chunk work from cross-chunk state propagation.
- The compiler relies on graph rewrites such as operator substitution, common subexpression elimination, transpose elimination, and insertion of custom Triton kernels for domain-specific ops like lower-triangular inverse.
- The paper explicitly positions FlexLA as a high-level compiler rather than a low-level assembler: hardware details are delegated to Triton, and the system is meant to stay usable as GPUs evolve.
- The strongest practical lesson is that the communication pattern matters as much as the math; tile-level fusion and custom communication schedules are central to the speedup.

## Limitations
- FlexLA only covers architectures that can be expressed as chunk-parallel associative recurrences.
- Non-associative update rules are out of scope, and the paper names TTT as a concrete example that cannot be expressed in the FlexLA abstraction.
- The paper focuses on the prefill / forward path; it does not claim to solve every possible training or inference detail for all future linear-attention designs.
- The current backend is Triton-centered, so portability depends on the compiler stack rather than a fully backend-agnostic runtime.

## Takeaways
- Imported from the linear-attention thread as the main compiler paper for unified kernel generation.
- FlexLA is best read as the compiler counterpart to FLA: FLA shows what expert kernel tuning can do, while FlexLA argues for codifying that expertise into a reusable DSL and backend.
- Its most durable contribution is the three-phase abstraction, which makes linear-attention variants look less like unrelated model families and more like compiler targets with shared structure.

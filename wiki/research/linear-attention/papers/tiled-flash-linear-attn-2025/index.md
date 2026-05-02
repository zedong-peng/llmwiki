---
title: "Tiled Flash Linear Attention: More Efficient Linear RNN and xLSTM Kernels"
domain: research
area: linear-attention
type: paper
status: processed
updated: 2026-04-21
tags: [paper, misc, linear-attn, tfla, xlstm, kernels, mlstm]
---

# Tiled Flash Linear Attention: More Efficient Linear RNN and xLSTM Kernels

## TL;DR
TFLA is a kernel-level answer to the main problem in chunkwise linear-RNN execution: small chunks keep memory use low but waste compute, while large chunks raise arithmetic intensity but are constrained by SRAM and intermediate-state materialization. The paper introduces a second level of tiling inside each chunk, applies it to mLSTM, and shows that a sigmoid-gated variant (`mLSTMsig`) preserves language-model quality while running faster.

## Problem
- FLA already parallelizes linear RNNs over chunks, but its chunk size is bounded by on-chip SRAM.
- Small chunks force many intermediate states into HBM, which lowers arithmetic intensity and raises IO cost.
- The result is a hardware bottleneck: linear scaling in sequence length does not automatically translate into better wall-clock runtime.

## Method
- The core idea is Tiled Flash Linear Attention: keep the chunkwise parallel formulation, then add a second level of sequence parallelism by tiling matrix computations within each chunk.
- The implementation targets mLSTM, which uses matrix memory plus exponential gating, and reorganizes the recurrent and parallel passes around chunk materialization.
- The paper also proposes `mLSTMsig`, replacing the exponential input gate with a sigmoid input gate and removing some computation while preserving the same transfer behavior after normalization.
- A transfer-behavior analysis compares `mLSTMexp` and `mLSTMsig`, showing that both transition from suppressing to passing signal at similar negative input-gate preactivation values.

## Results
- On the kernel benchmark, the TFLA `xl_chunk` kernels are about 25% faster than the limited-chunk kernels.
- The paper reports that the new mLSTM kernels outperform highly optimized FlashAttention, Linear Attention, and Mamba kernels on H100.
- For language modeling at 4k context, validation perplexity stays nearly unchanged across formulations: for 160M, values stay around 21.01 to 21.18; for 1.4B, around 13.20 to 13.35.
- On the 1.4B, 8k-context step-time table, `mLSTMsig` with `xl_chunk` reaches 1.62s at 16 heads, compared with 2.39s for the Llama baseline and 1.60s for `mLSTMexp` limited-chunk in the same setup.
- The runtime-optimal chunk size is observed around 128 to 256 on H100, and the paper notes that this optimum is still below the theoretical runtime-optimal value.

## Implementation Clues
- The repo is the main implementation anchor: `mlstm_kernels` exposes JAX, PyTorch, and Triton modules plus benchmark utilities.
- The README shows three kernel families: `chunkwise`, `parallel`, and `recurrent`, with the TFLA path implemented as `chunkwise--triton_xl_chunk`.
- The benchmark stack is designed to sweep kernel specs, record runtime and memory, and compare mLSTM against FlashAttention, Mamba, GLA, and other baselines.
- The dev notes show the intended profiling workflow with Nsight Systems and Nsight Compute, which is useful if this entry later becomes a systems-analysis reference rather than only a paper note.

## Limitations
- TFLA still materializes intermediate states in HBM across chunks; it reduces the pain point but does not remove state traffic entirely.
- The paper explicitly says the measured runtime is still higher than the theoretical runtime model, indicating room for kernel-level optimization.
- Newer GPUs shift the runtime-optimal chunk size upward, so the best chunk size is hardware dependent rather than a fixed constant.
- The authors do not yet use advanced asynchronous loading to overlap memory movement with computation.

## Takeaways
- The key contribution is not just “faster mLSTM”, but a reusable kernel design principle: expose another parallel dimension inside each chunk so the chunk size can grow without collapsing occupancy or memory efficiency.
- `mLSTMsig` matters because it shows the runtime gain can come from both algorithmic tiling and a lighter gate formulation.
- The paper is a strong benchmark anchor for any future linear-RNN or xLSTM kernel work because it provides both kernel-level and model-level evidence.
- This entry should remain the canonical local reference for TFLA, mLSTMexp, and mLSTMsig in the linear-attention hardware thread.

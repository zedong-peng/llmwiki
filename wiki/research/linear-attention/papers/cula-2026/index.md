---
title: "cuLA: CUDA Linear Attention"
domain: research
area: linear-attention
type: engineering
status: processed
updated: 2026-04-24
tags: [engineering, linear-attn, cuda, cutlass, cute-dsl, kernels, blackwell, hopper]
---

# cuLA: CUDA Linear Attention

> Status: repo-first source note processed from GitHub API (README, REPO_LAYOUT.md, USAGE.md, docs/) on 2026-04-24. Repo clone pending (network issue).

## TL;DR
- cuLA 是 FLA 的 CUDA 原生加速层：用 CuTe DSL 和 CUTLASS C++ 为 Blackwell (SM10X) 和 Hopper (SM90) 手写 linear attention 内核。
- 当前支持 KDA（Kimi Delta Attention）和 Lightning Attention，设计为 FLA 的 drop-in 替换（一行 import 切换）。
- Blackwell 上 KDA modular forward 平均 1.45x 加速，Lightning Attention prefill 最高 1.86x，Hopper 上 KDA fused forward 平均 1.52x。

## Problem
- FLA 的 Triton 内核在 Hopper/Blackwell 上无法充分利用 TMEM、TMA、warp specialization 等新硬件特性。
- 线性注意力的 state 更新（KxV outer product 累加）是 memory-bound 瓶颈，需要手工调度才能压榨 TensorCore 利用率。
- 现有 CUDA 实现分散在各个 repo，缺乏统一的 FLA 兼容接口。

## Method

### 支持的算法

| 算法 | GPU | 模式 | 入口 |
|---|---|---|---|
| KDA (Kimi Delta Attention) | SM100 (Blackwell) | Modular Forward | `cula.kda.chunk_kda` |
| KDA | SM90 (Hopper) | Fused Forward | `cula.kda.kda_prefill_hopper` |
| Lightning Attention | SM100 | Prefill | `cula.ops.lightning_attn` |
| Lightning Attention | SM90 & SM100 | Decode | `cula.lightning.la_decode` |
| Generic Linear Attention | SM100 | Prefill | `cula.ops.linear_attn` |

### 内核架构（以 Lightning Attention 为例）

8 warp 分工：
- Warp 0-3（CUDA Core，128 threads）：K decay weighting、causal mask、O 合并、inter-chunk decay
- Warp 4（MMA）：执行 QK、VP、KV、SQ 四个 MMA
- Warp 5（Load）：TMA G2S 加载 Q/K/V
- Warp 6（Epilogue）：TMA S2G 写 O
- Warp 7：预留

TMEM 用于跨 chunk 持久化 state（KV FP32 累加器），避免 SMEM roundtrip。

### ChunkDeltaH 关键优化

`chunk_delta_h.py` 的 V2 版本：h state 在 CUDA warp 寄存器中跨 chunk 传递（register-carry），完全消除 GMEM roundtrip。这是相比 FLA Triton 实现的核心改进点。

### KDA 算法

KDA = Kimi Delta Attention，delta-rule 变体，带 per-head gating：
```
wh = h × W
v_new = u - wh
update = v_new^T × K^T
h_new = 2^gk · h + update
```
`safe_gate=True` 时启用 TensorCore (M=16) 加速。

## Results
- **KDA Modular Forward (Blackwell)**: avg 1.45x（fixed-length），avg 1.32x（variable-length，18 configs）
- **Lightning Attention Prefill (Blackwell)**: up to 1.86x（B=2）
- **Lightning Attention Varlen (Blackwell)**: avg 1.54x（126 configs）
- **KDA Fused Forward (Hopper)**: avg 1.52x（fixed + variable-length）
- Baseline：FLA v0.4.2 Triton 实现，测试环境 GB300/GB200/H200，CUDA 12.9，PyTorch 2.9.1

## Implementation Clues
- 依赖 CUDA Toolkit 12.9+、PyTorch 2.9.1+，要求 NVCC 版本与系统 CUDA 一致。
- `cula/ops/` 是 CuTe DSL Python 内核（import 时 JIT 编译），`csrc/` 是 CUTLASS C++ 内核（PyBind11 绑定）。
- KDA SM90 fused forward 仅支持 forward，backward 尚未实现；modular forward 支持完整 fwd+bwd（backward 复用 FLA 实现）。
- Persistent varlen 模式：Load warp 用 `atomicAdd` 动态调度，双缓冲 mbarrier 防 ABA 死锁。
- `safe_gate=True` 是使用 TensorCore 的必要条件，`beta` 支持 bf16/fp32，`initial_state` 必须 fp32，`cu_seqlens` 必须 int32。

## Limitations
- 早期阶段，API 可能变动，许多内核仍有优化空间。
- Backward pass 优化尚在 roadmap，当前 backward 依赖 FLA Triton 实现。
- 要求 Hopper/Blackwell GPU，不支持 Ampere 及以下。
- KDA fused forward (SM100) 尚未实现（roadmap）。

## Takeaways
- cuLA 是 FLA 在 Hopper/Blackwell 上的 CUDA 原生加速层，是评估新 GPU 上 linear attention kernel 上限的参考实现。
- register-carry h state 是消除 GMEM roundtrip 的关键技术，值得在其他 delta-rule 变体中复用。
- 与 FLA 的 drop-in 兼容设计使其可以直接插入现有训练框架，降低迁移成本。

## Source Notes
- Repo: `repo/cuLA/`（待 clone）
- 主要来源：`README.md`、`REPO_LAYOUT.md`、`USAGE.md`、`docs/lightning_attn_pipeline.md`、`docs/chunk_delta_h_pipeline.md`
- 关联论文：[GLA](../gla-2024/index.md)、[FLA](../fla-2024/index.md)、[Gated DeltaNet](../gated-deltanet-2025/index.md)

---
title: Linear Attention
domain: research
area: linear-attention
type: overview
status: active
updated: 2026-04-25
tags: [research, linear-attention, sequence-models, hardware]
---

# Linear Attention

这个 area 从 `misc` 中剥离出来，集中保存 linear attention、recurrent sequence models、SSM/retention/delta-rule variants，以及相关 GPU kernel、compiler、hardware co-design 笔记。

## Thread Directory

- [Linear Attention 在 GPU 上到底慢在哪](threads/2026-04-21-linear-attn-gpu-bottleneck-blog.md)


### Linear Attention And Hardware Co-Design

| Paper | Year | Venue | Importance | Wiki Status |
|---|---:|---|---|---|
| [Transformers are RNNs](assets/transformers-are-rnns-2020/index.md) | 2020 | ICML | First-generation linear attention foundation | `processed` |
| [RetNet](assets/retnet-2023/index.md) | 2023 | Arxiv | Second-generation retention-state formulation | `processed` |
| [GLA](assets/gla-2024/index.md) | 2024 | ICML | Mature gated linear-attention baseline | `processed` |
| [Mamba](assets/mamba-2023/index.md) | 2023 | NeurIPS | Selective-SSM baseline | `processed` |
| [Mamba-2](assets/mamba-2-2024/index.md) | 2024 | ICML | SSM and linear-attention unification | `processed` |
| [DeltaNet](assets/deltanet-2024/index.md) | 2024 | NeurIPS | Delta-rule state update line | `processed` |
| [Gated DeltaNet](assets/gated-deltanet-2025/index.md) | 2025 | ICLR | Gated delta-rule follow-up | `processed` |
| [Griffin](assets/griffin-2024/index.md) | 2024 | Arxiv | Recurrent local-attention hybrid | `processed` |
| [RecurrentGemma](assets/recurrentgemma-2024/index.md) | 2024 | Arxiv | Open Griffin-family implementation | `processed` |
| [Jamba](assets/jamba-2024/index.md) | 2024 | Arxiv | Hybrid Transformer-Mamba model | `processed` |
| [FLA](assets/fla-2024/index.md) | 2024 | Repo | De facto Triton kernel baseline | `processed` |
| [Linear Attn GPU Kernel](assets/linear-attn-gpu-kernel-2025/index.md) | 2025 | Arxiv | GPU kernel optimization ceiling | `processed` |
| [Pimba](assets/pimba-2025/index.md) | 2025 | MICRO | Near-memory linear-attention accelerator | `seed` |
| [PLENA](assets/plena-2025/index.md) | 2025 | Arxiv | Hybrid long-context accelerator baseline | `seed` |
| [FlexLinearAttention](assets/flexla-forge-2025/index.md) | 2026 | ICLR | Compiler-generated linear-attention kernels | `processed` |
| [Tiled Flash Linear Attention](assets/tiled-flash-linear-attn-2025/index.md) | 2025 | NeurIPS | Register-pressure kernel evidence | `processed` |
| [DANMP](assets/danmp-2026/index.md) | 2026 | Arxiv | Near-memory attention accelerator | `processed` |
| [cuLA](assets/cula-2026/index.md) | 2026 | Repo | CUDA/CUTLASS kernels for Hopper & Blackwell | `processed` |

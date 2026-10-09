---
title: Linear Attention
domain: research
area: linear-attention
type: overview
status: active
updated: 2026-10-09
tags: [research, linear-attention, sequence-models, hardware]
---

# Linear Attention

这个 area 从 `misc` 中剥离出来，集中保存 linear attention、recurrent sequence models、SSM/retention/delta-rule variants，以及相关 GPU kernel、compiler、hardware co-design 笔记。

书目与来源快照在各归档的 `citation.bib`；表中年份、venue 与研究定位保留旧目录记录，未在本次迁移重新核对。阅读状态以历史笔记和明确未读标识为依据；旧 metadata 的状态冲突见各笔记迁移说明。

## Thread Directory

- [Linear Attention 在 GPU 上到底慢在哪](threads/2026-04-21-linear-attn-gpu-bottleneck-blog.md)


### Linear Attention And Hardware Co-Design

| Paper | Year | Venue | Importance | Wiki Status |
|---|---:|---|---|---|
| [Transformers are RNNs](assets/transformers-are-rnns-2020/note.md) | 2020 | ICML | First-generation linear attention foundation | `历史笔记` |
| [RetNet](assets/retnet-2023/note.md) | 2023 | Arxiv | Second-generation retention-state formulation | `历史笔记` |
| [GLA](assets/gla-2024/note.md) | 2024 | ICML | Mature gated linear-attention baseline | `历史笔记` |
| [Mamba](assets/mamba-2023/note.md) | 2023 | NeurIPS | Selective-SSM baseline | `历史笔记` |
| [Mamba-2](assets/mamba-2-2024/note.md) | 2024 | ICML | SSM and linear-attention unification | `历史笔记` |
| [DeltaNet](assets/deltanet-2024/note.md) | 2024 | NeurIPS | Delta-rule state update line | `历史笔记` |
| [Gated DeltaNet](assets/gated-deltanet-2025/note.md) | 2025 | ICLR | Gated delta-rule follow-up | `历史笔记` |
| [Griffin](assets/griffin-2024/note.md) | 2024 | Arxiv | Recurrent local-attention hybrid | `历史笔记` |
| [RecurrentGemma](assets/recurrentgemma-2024/note.md) | 2024 | Arxiv | Open Griffin-family implementation | `历史笔记` |
| [Jamba](assets/jamba-2024/note.md) | 2024 | Arxiv | Hybrid Transformer-Mamba model | `历史笔记` |
| [FLA](assets/fla-2024/note.md) | 2024 | Repo | De facto Triton kernel baseline | `历史笔记` |
| [Linear Attn GPU Kernel](assets/linear-attn-gpu-kernel-2025/note.md) | 2025 | Arxiv | GPU kernel optimization ceiling | `历史笔记` |
| [Pimba](assets/pimba-2025/note.md) | 2025 | MICRO | Near-memory linear-attention accelerator | `agent-read` |
| [PLENA](assets/plena-2025/note.md) | 2025 | Arxiv | Hybrid long-context accelerator baseline | `agent-read` |
| [FlexLinearAttention](assets/flexla-forge-2025/note.md) | 2026 | ICLR | Compiler-generated linear-attention kernels | `历史笔记` |
| [Tiled Flash Linear Attention](assets/tiled-flash-linear-attn-2025/note.md) | 2025 | NeurIPS | Register-pressure kernel evidence | `历史笔记` |
| DANMP（原目录已移除） | 2026 | Arxiv | Near-memory attention accelerator | `历史笔记` |
| [cuLA](assets/cula-2026/note.md) | 2026 | Repo | CUDA/CUTLASS kernels for Hopper & Blackwell | `历史笔记` |

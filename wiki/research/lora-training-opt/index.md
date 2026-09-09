---
title: LoRA Training Optimization
domain: research
area: lora-training-opt
type: overview
status: active
updated: 2026-09-08
tags: [lora, training, unsloth, triton, qwen3, rtx-4090]
---

# LoRA Training Optimization

目标：在单卡 4090 / A100 上做出比 Unsloth 更快的 LoRA 训练框架（聚焦 Qwen3 / LLaMA3 架构）。

2026-09-08 按 Canonical Layout 收敛：本 `index.md` 是唯一正式合成页，由原先平铺的 6 个 loose 笔记（README、landscape、bottlenecks、opportunities、papers、unsloth-internals）折入后删除，全文见 git 历史。尚无本地归档的论文 PDF，`papers/` 待首个 TeX/PDF 归档时再建。

相关 repo：[unsloth](https://github.com/unslothai/unsloth)（`git clone --depth=1 https://github.com/unslothai/unsloth.git`）、[Liger-Kernel](https://github.com/linkedin/Liger-Kernel)（LinkedIn Triton kernel 库）、[Chronicals](https://arxiv.org/abs/2601.02609)（声称 3.51x over Unsloth）。

## Landscape（框架横向对比）

| 框架 | 速度 | 显存 | 多卡 | 易用性 | 模型支持 | 维护状态 |
|------|------|------|------|--------|---------|---------|
| **Unsloth** | ★★★★ | ★★★★★ | ✗（免费版） | ★★★★★ | 广泛 | 活跃 |
| **Chronicals** | ★★★★★ | ★★★★ | ✓ | ★★★ | 有限 | 新 |
| **Liger-Kernel** | ★★★★ | ★★★★ | ✓ | ★★★ | 广泛 | 活跃 |
| **LLaMA-Factory** | ★★★ | ★★★ | ✓ | ★★★★ | 广泛 | 活跃 |
| **Axolotl** | ★★★ | ★★★ | ✓ | ★★★ | 广泛 | 活跃 |
| **torchtune** | ★★★ | ★★★ | ✓ | ★★★ | 中等 | 官方 |
| **HuggingFace TRL** | ★★ | ★★ | ✓ | ★★★★★ | 最广 | 官方 |

- **Unsloth**：手写 Triton kernel + 手动 autograd + 智能 GC；单卡最快易用框架；局限是免费版单卡、部分 benchmark 有水分（梯度为零问题）。
- **Chronicals**（[2601.02609](https://arxiv.org/abs/2601.02609)）：Fused Triton Kernels + Cut Cross-Entropy + LoRA+ + Sequence Packing；声称全量 3.51x / rank=32 时 4.10x over Unsloth，MFU 39.6% vs 11.3%；新框架生态不成熟，需独立验证。
- **Liger-Kernel**：kernel 库非完整框架（RoPE、SwiGLU、Cross Entropy、Fused Linear CE、RMSNorm），与 torchtune/TRL 深度集成，可作构建块。
- **torchtune + torch.compile + Liger**（[PyTorch 官方 blog](https://pytorch.org/blog/peak-performance-minimized-memory/)）：官方支持、compile-friendly，但速度非首要目标。

技术栈建议：底层 Triton（易写、性能近 CUDA），框架层基于 HF PEFT + 自定义 kernel 替换，参考 Liger 写法 + Chronicals 思路，目标 Qwen3-7B + 4090 超过 Unsloth。

## Unsloth Internals（加速原理）

来源：[Introducing Unsloth](https://unsloth.ai/introducing)、[HuggingFace Blog](https://huggingface.co/blog/unsloth-trl/)。

1. **手写 Triton kernel**：关键算子重写，消中间 tensor 与多余 launch（RMSNorm 7x、SwiGLU 5x、QK-RoPE 2.3x）。
2. **手动 autograd**（LoRA 核心）：不用 PyTorch autograd，手推 attention + LoRA 矩阵微分；每 head 6 个矩阵微分贯穿 32 层；关键是链式乘括号顺序（rank ≤128 vs base 4096+）；终梯度用 in-place 操作省显存。
3. **智能梯度检查点**：非简单丢弃重算，按重算代价/保留价值取舍，比原生 GC 省约 30% 显存且少重算。
4. **Cut Cross-Entropy**：分块 online softmax，logit 内存 5GB → 135MB（37x，大词表 128k 场景），永不 materialize 完整 logit。
5. **Sequence Packing**：Best-Fit Decreasing 拼变长序列，恢复 60-75% 被 padding 浪费的算力。
6. **4-bit 量化集成**：bitsandbytes 4-bit dequant 迁入 Triton 并与后算融合。

性能：单卡 T4 + Alpaca，HF TRL 23.25h → Unsloth 2.5h（8.8x）。已知问题：免费版无多卡；曾报 46k tok/s 但该配置梯度为零（未在训练），正确训练约 11,736 tok/s（A100-40GB Qwen2.5-0.5B）。

## Bottlenecks（为什么 LoRA 会慢）

核心结论（[2507.08833](https://arxiv.org/abs/2507.08833)）：**LoRA 在某些配置下比全量微调还慢 30-60%**（A100 batch=4 seq=512-1024：GPT2-xl LoRA fwd 97.73ms/bwd 124.34ms vs Full-FT 61.89/114.92；TinyLlama 60.35/81.61 vs 37.14/66.89）。

- **GPU 顺序执行**：每次一 kernel；adapter A/B 矩阵是额外顺序 kernel；base GEMM 越快 adapter 占比越大。
- **Memory bandwidth**：LoRA down-projection 算术强度远低于 machine balance，rank 小 → 大读写小计算 → memory bound；A100（2TB/s）上算力浪费明显。
- **4090 vs A100**：4090（24GB/1008GB/s/165 BF16 TFLOPS）主限显存容量，QLoRA 4-bit 更常用；A100-80GB（2000GB/s/312 TFLOPS）主看 kernel launch 开销与算力利用率。
- **Optimizer 隐藏开销**（[2509.12229](https://arxiv.org/abs/2509.12229)，RTX 4060）：AdamW 4 操作是 4 独立 kernel；PagedAdamW 快 ~25%；BF16 在消费级卡比 FP16 慢（与数据中心相反）。参考点：AdamW+fp16+BS1+S512 500 tok/s / 0.19J / 6.2GB；PagedAdamW+fp16+BS2+S2048 628 / 0.15J / 8.1GB；PagedAdamW+bf16+BS2+S1024 360 / 0.26J / 7.9GB。
- **Sequence Packing 价值**：真实数据长度差异大，不 packing 则 60-75% 算力 waste 在 padding。

## Opportunities（超 Unsloth 的五个方向）

1. **Fused Optimizer（最现实）**：AdamW 4 kernel 合 1，少 4x 显存读写；参考 `AdamW(fused=True)`（有 [bug #121857](https://github.com/pytorch/pytorch/issues/121857)）与 bitsandbytes 8-bit Adam dequant 融合；A100 收益最大；难度中（Triton 约 200-300 行）。
2. **FusedLoRA Forward/Backward**：`y = xW + x(AB)` 两 GEMM + add 融合，在 low-rank intermediate 处分割只融 LoRA 部分（全融 base GEMM 会破坏其 compute-bound 性能）；参考 [2510.00206](https://arxiv.org/abs/2510.00206) FusedLoRA 与 [Axolotl blog](https://axolotlai.substack.com/p/accelerating-lora-fine-tuning-with)；难度较高（GEMM tiling）。
3. **Qwen3/DeepSeek MLA 专用 kernel**：Unsloth 对 MLA 支持新而浅；MLA KV 压缩矩阵本身 low-rank，与 LoRA 天然结合；V2/V3/R1 的 MLA LoRA backward 无专用实现；难度高。
4. **torch.compile + LoRA 全图优化**：Unsloth compile 支持不全；把 Triton kernel 写成 compile-friendly 让 compile 做跨 kernel fusion；难度中偏工程。
5. **Sequence Packing 改进**：Unsloth BFD 未计 attention mask 开销；Flash Attention 3 variable-length + document-level attention 可消 mask overhead；难度低偏集成。

起步路径：复现 Chronicals benchmark（验环境）→ Fused AdamW Triton kernel 对 bitsandbytes → FusedLoRA 对 Unsloth → 发 blog/arxiv。

## Papers（阅读清单，无本地归档）

顶会/高引必读：[LoRA 2106.09685](https://arxiv.org/abs/2106.09685)（ICLR22，Microsoft，冻结 base 只训 A/B）；[FlashAttention-2 2307.08691](https://arxiv.org/abs/2307.08691)（ICLR24，Tri Dao，IO-aware，~1.9x，现代框架基础）；[QLoRA 2305.14314](https://arxiv.org/abs/2305.14314)（NeurIPS23，NF4 4-bit，65B 单 48GB 可训）；[Liger-Kernel 2410.10989](https://arxiv.org/abs/2410.10989)（Triton kernel 库，+20% throughput / -60% 显存 vs HF）；[LoRA+ 2402.12354](https://arxiv.org/abs/2402.12354)（ICML24，B 学习率 16x A，2x 收敛）。

工程向（未顶会、细节有用）：[2507.08833](https://arxiv.org/abs/2507.08833)（LoRA 慢 30-60% + PaCA）；[2601.02609](https://arxiv.org/abs/2601.02609)（Chronicals，方法论待验）；[2509.12229](https://arxiv.org/abs/2509.12229)（4060 实测，4090 选配指导）；[2510.00206](https://arxiv.org/abs/2510.00206)（FusedLoRA，-2.64x 显存读写）。工具：[torchtune + compile + Liger](https://pytorch.org/blog/peak-performance-minimized-memory/)。待读（先核作者/venue）：[2603.16428](https://arxiv.org/abs/2603.16428)、[2502.08141](https://arxiv.org/abs/2502.08141)。

返回 [[research/index]]。

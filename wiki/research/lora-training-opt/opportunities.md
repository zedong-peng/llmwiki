# 可以超越 Unsloth 的方向

> 聚焦：单卡 RTX 4090 / A100，Qwen3 / LLaMA3 架构

## 方向一：Fused Optimizer（最现实）

**现状**：AdamW 的 4 个操作是 4 次独立 kernel
```
exp_avg update → exp_avg_sq update → param update → grad zero
```

**机会**：融合成 1 次 kernel，减少 4x 显存读写

**参考**：
- PyTorch `AdamW(fused=True)` 已有实现但有 bug（[issue #121857](https://github.com/pytorch/pytorch/issues/121857)）
- bitsandbytes 8-bit Adam 的 dequant 也可以进一步融合
- 在 A100 上收益最大（compute 强，memory-bound 的 optimizer 浪费算力）

**难度**：中等，Triton 实现约 200-300 行

---

## 方向二：FusedLoRA Forward/Backward

**现状**：LoRA 的 `y = xW + x(AB)` 是两次独立 GEMM + 一次 add

**机会**：
- 在 low-rank 维度上融合，消除中间 tensor 的显存读写
- 关键：不能把 base GEMM 和 LoRA GEMM 完全融合（会破坏 compute-bound 的 base GEMM 性能）
- 正确做法：在 low-rank intermediate tensor 处分割，只融合 LoRA 部分

**参考**：
- [Efficient LoRA Fine-Tuning (arxiv 2510.00206)](https://arxiv.org/abs/2510.00206) 的 FusedLoRA
- [Axolotl custom CUDA kernels blog](https://axolotlai.substack.com/p/accelerating-lora-fine-tuning-with)

**难度**：较高，需要理解 GEMM tiling

---

## 方向三：针对 Qwen3/DeepSeek MLA 的专用 Kernel

**现状**：Unsloth 对 MLA（Multi-head Latent Attention）支持很新，优化不深

**机会**：
- DeepSeek-V2/V3/R1 使用 MLA，LoRA 在 MLA 上的 backward 没有专用实现
- MLA 的 KV 压缩矩阵本身就是 low-rank，与 LoRA 有天然结合点

**难度**：高，需要深入理解 MLA 架构

---

## 方向四：torch.compile + LoRA 全图优化

**现状**：Unsloth 的 torch.compile 支持不完整，很多 custom kernel 无法被编译

**机会**：
- 把所有 Triton kernel 写成 compile-friendly 的形式
- 让 torch.compile 做跨 kernel 的 fusion（比手写 fusion 更灵活）
- 参考：[torchtune + torch.compile + Liger Kernel](https://pytorch.org/blog/peak-performance-minimized-memory/)

**难度**：中等，主要是工程问题

---

## 方向五：Sequence Packing 改进

**现状**：Unsloth 用 Best-Fit Decreasing，但没有考虑 attention mask 的开销

**机会**：
- 打包后的序列需要 block-diagonal attention mask
- Flash Attention 3 支持 variable-length attention，可以完全消除 mask overhead
- 结合 document-level attention（不同文档间不做 attention）

**难度**：低，主要是工程集成

---

## 推荐起步路径

```
第一步：复现 Chronicals 的 benchmark（验证环境）
第二步：实现 Fused AdamW Triton kernel，对比 bitsandbytes
第三步：实现 FusedLoRA，对比 Unsloth
第四步：发 blog / arxiv
```

## 竞争格局

| 框架 | 优势 | 劣势 |
|------|------|------|
| Unsloth | 生态好、易用、支持模型多 | 多卡不支持、部分 benchmark 有水分 |
| Chronicals | 声称 3.51x over Unsloth | 新框架，生态差，可信度待验证 |
| Liger-Kernel | LinkedIn 背书、kernel 质量高 | 只是 kernel 库，不是完整框架 |
| torchtune | PyTorch 官方 | 速度不是重点 |
| **你的框架** | 专注单卡极致性能 | 从零开始 |

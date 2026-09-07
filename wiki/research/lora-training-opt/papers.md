# 相关论文

## 顶会 / 高引 必读

### [LoRA: Low-Rank Adaptation of Large Language Models (2106.09685)](https://arxiv.org/abs/2106.09685)
- **发表**：ICLR 2022 ⭐ | 引用 10000+
- **作者**：Edward Hu et al. (Microsoft)
- **贡献**：LoRA 原始论文，冻结 base model，只训练低秩矩阵 A、B

### [FlashAttention-2 (2307.08691)](https://arxiv.org/abs/2307.08691)
- **发表**：ICLR 2024 ⭐ | GitHub 14k+ stars
- **作者**：Tri Dao (Stanford/Together AI)
- **贡献**：IO-aware attention，训练加速约 1.9x，是所有现代训练框架的基础

### [QLoRA (2305.14314)](https://arxiv.org/abs/2305.14314)
- **发表**：NeurIPS 2023 ⭐ | 引用 5000+
- **作者**：Tim Dettmers et al. (UW)
- **贡献**：4-bit NF4 量化 + LoRA，使 65B 模型在单张 48GB GPU 上可训练

### [Liger-Kernel: Efficient Triton Kernels for LLM Training (2410.10989)](https://arxiv.org/abs/2410.10989)
- **发表**：arXiv 2024 | GitHub 10k+ stars ⭐ | LinkedIn 出品
- **贡献**：Triton 实现的 kernel 库（RoPE, SwiGLU, RMSNorm, Fused Linear Cross Entropy）
- **效果**：比 HuggingFace 提升 20% throughput，减少 60% 显存
- **repo**：https://github.com/linkedin/Liger-Kernel

### [LoRA+ (2402.12354)](https://arxiv.org/abs/2402.12354)
- **发表**：ICML 2024 ⭐
- **贡献**：B 矩阵学习率设为 A 矩阵的 16x，2x 更快收敛
- **理论依据**：B 初始化为零，A 随机初始化，两者梯度尺度不同

---

## 工程向论文（质量参差，但技术细节有用）

### [LoRA Is Slower Than You Think (2507.08833)](https://arxiv.org/abs/2507.08833)
- **作者**：待核实，arXiv 2025
- **结论**：LoRA 在 A100 上比全量微调慢 30-60%
- **原因**：GPU 顺序执行 kernel，adapter 层是额外开销；low-rank GEMM 是 memory-bound
- **方案**：PaCA，只对上层 K 层做 adapter
- ⚠️ 未发表顶会，但实验数据有参考价值

### [Chronicals: 3.51x Speedup over Unsloth (2601.02609)](https://arxiv.org/abs/2601.02609)
- **作者**：待核实，arXiv 2025
- **核心技术**：Fused Triton Kernels + Cut Cross-Entropy + LoRA+ + Sequence Packing
- **关键发现**：Unsloth 报告的 46k tokens/sec 时梯度为零（没有在训练）
- **实测**：A100-40GB，Qwen2.5-0.5B，LoRA rank=32：11,699 vs 2,857 tokens/sec（4.10x）
- **MFU**：39.6% vs Unsloth 11.3%
- ⚠️ 未发表顶会，benchmark 方法论需独立验证

### [Profiling LoRA/QLoRA on Consumer GPUs (2509.12229)](https://arxiv.org/abs/2509.12229)
- **平台**：RTX 4060
- **发现**：BF16 在消费级 GPU 上比 FP16 慢；PagedAdamW 比 AdamW 快 25%
- ⚠️ 未发表顶会，但对 4090 配置选择有直接指导意义

### [Efficient LoRA Fine-Tuning for LLMs (2510.00206)](https://arxiv.org/abs/2510.00206)
- **FusedLoRA**：在 low-rank intermediate tensor 处分割，只融合 LoRA 部分
- **关键洞察**：不能把 base GEMM 和 LoRA GEMM 完全融合（会破坏 compute-bound 性能）
- **效果**：减少 2.64x 显存读写

---

## 工具/框架

### [torchtune + torch.compile + Liger](https://pytorch.org/blog/peak-performance-minimized-memory/)
- PyTorch 官方微调框架，集成 torch.compile + Liger Kernel

---

## 待读（需先确认作者/venue）

- [An Efficient Heterogeneous Co-Design for Fine-Tuning on a Single GPU (2603.16428)](https://arxiv.org/abs/2603.16428)
- [Accurate and Efficient LoRA Fine-Tuning under 2 Bits (2502.08141)](https://arxiv.org/abs/2502.08141)

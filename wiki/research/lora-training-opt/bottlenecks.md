# LoRA 训练瓶颈分析

## 核心结论

**LoRA 在某些配置下比全量微调还慢。**

来源：[LoRA Is Slower Than You Think (arxiv 2507.08833)](https://arxiv.org/abs/2507.08833)

## 为什么 LoRA 会更慢

### GPU 顺序执行问题
- GPU 每次只处理一个 kernel
- LoRA 的 adapter 层（A矩阵、B矩阵）是**额外的顺序 kernel**，无法并行
- 当 base model 的 GEMM 已经很快时，adapter 的 overhead 占比反而更大

### 实测数据（A100，batch=4，seq=512-1024）

| 模型 | 方法 | Forward (ms) | Backward (ms) |
|------|------|-------------|--------------|
| GPT2-xl (1.5B) | LoRA | 97.73 | 124.34 |
| GPT2-xl (1.5B) | Full-FT | 61.89 | 114.92 |
| TinyLlama (1.1B) | LoRA | 60.35 | 81.61 |
| TinyLlama (1.1B) | Full-FT | 37.14 | 66.89 |

LoRA 在这些配置下比全量微调慢 **30-60%**。

### Memory Bandwidth 问题
- LoRA 的 down-projection 计算 arithmetic intensity 极低（远低于 machine balance）
- rank 维度小 → 每次 kernel 读写大量数据但计算量很少 → **memory bound**
- 这在 A100（HBM 带宽 2TB/s）上尤其明显：带宽够用但算力浪费

## 4090 vs A100 的差异

| 特性 | RTX 4090 | A100-80GB |
|------|---------|-----------|
| VRAM | 24GB | 80GB |
| 显存带宽 | 1008 GB/s | 2000 GB/s |
| BF16 算力 | 165 TFLOPS | 312 TFLOPS |
| 主要瓶颈 | 显存容量 | kernel launch overhead / 算力利用率 |

**4090 上**：显存是主要限制，QLoRA（4-bit）更常用，memory-bound 问题更严重
**A100 上**：算力强但很多 kernel 没吃满，compute utilization 是关键指标

## Optimizer 的隐藏开销

来源：[Profiling LoRA/QLoRA on Consumer GPUs (arxiv 2509.12229)](https://arxiv.org/abs/2509.12229)

- AdamW 的 4 个操作（exp_avg, exp_avg_sq, param update, grad zero）是 4 次独立 kernel
- PagedAdamW 比标准 AdamW 快 **~25%**（在 RTX 4060 上测试）
- BF16 在消费级 GPU 上**比 FP16 慢**（与数据中心 GPU 相反）

| 配置 | Throughput | Energy/Token | VRAM |
|------|-----------|-------------|------|
| AdamW + fp16 + BS=1 + S=512 | 500 tok/s | 0.19 J | 6.2 GB |
| PagedAdamW + fp16 + BS=2 + S=2048 | 628 tok/s | 0.15 J | 8.1 GB |
| PagedAdamW + bf16 + BS=2 + S=1024 | 360 tok/s | 0.26 J | 7.9 GB |

## Sequence Packing 的价值

- 真实数据集序列长度差异大，padding 浪费严重
- 不做 packing：60-75% 的算力浪费在 padding token 上
- Best-Fit Decreasing bin packing 可以基本消除这个浪费

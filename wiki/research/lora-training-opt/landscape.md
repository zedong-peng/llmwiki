# 框架横向对比

| 框架 | 速度 | 显存 | 多卡 | 易用性 | 模型支持 | 维护状态 |
|------|------|------|------|--------|---------|---------|
| **Unsloth** | ★★★★ | ★★★★★ | ✗（免费版） | ★★★★★ | 广泛 | 活跃 |
| **Chronicals** | ★★★★★ | ★★★★ | ✓ | ★★★ | 有限 | 新 |
| **Liger-Kernel** | ★★★★ | ★★★★ | ✓ | ★★★ | 广泛 | 活跃 |
| **LLaMA-Factory** | ★★★ | ★★★ | ✓ | ★★★★ | 广泛 | 活跃 |
| **Axolotl** | ★★★ | ★★★ | ✓ | ★★★ | 广泛 | 活跃 |
| **torchtune** | ★★★ | ★★★ | ✓ | ★★★ | 中等 | 官方 |
| **HuggingFace TRL** | ★★ | ★★ | ✓ | ★★★★★ | 最广 | 官方 |

## Unsloth

- **repo**: https://github.com/unslothai/unsloth
- **核心技术**: 手写 Triton kernel + 手动 autograd + 智能 GC
- **单卡性能**: 目前最快的易用框架
- **局限**: 免费版单卡；部分 benchmark 有水分（梯度为零问题）
- **适合**: 快速实验、消费级 GPU

## Chronicals

- **paper**: [arxiv 2601.02609](https://arxiv.org/abs/2601.02609)
- **核心技术**: Fused Triton Kernels + Cut Cross-Entropy + LoRA+ + Sequence Packing
- **声称性能**: 3.51x over Unsloth（全量），4.10x（LoRA rank=32）
- **MFU**: 39.6%（vs Unsloth 11.3%）
- **注意**: 新框架，生态不成熟，需要独立验证

## Liger-Kernel

- **repo**: https://github.com/linkedin/Liger-Kernel
- **定位**: kernel 库，不是完整训练框架
- **提供**: RoPE, SwiGLU, Cross Entropy, Fused Linear Cross Entropy, RMS Norm
- **集成**: 与 torchtune、TRL 深度集成
- **优势**: LinkedIn 背书，kernel 质量高，可以作为构建块

## torchtune + torch.compile + Liger

- **blog**: [PyTorch 官方](https://pytorch.org/blog/peak-performance-minimized-memory/)
- **组合**: torchtune 框架 + torch.compile 全图优化 + Liger kernel
- **优势**: 官方支持，compile-friendly
- **局限**: 速度不是首要目标

## 技术栈选择建议

如果要自己开发：

```
底层 kernel：Triton（比 CUDA 更易写，性能接近）
框架层：基于 HuggingFace PEFT + 自定义 kernel 替换
参考实现：Liger-Kernel 的 kernel 写法 + Chronicals 的优化思路
目标：在 Qwen3-7B + 4090 上超过 Unsloth
```

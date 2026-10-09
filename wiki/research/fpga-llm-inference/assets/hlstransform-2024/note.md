---
title: "HLSTransform: Energy-Efficient Llama 2 Inference on FPGAs Via High Level Synthesis"
updated: 2026-10-09
---

# HLSTransform: Energy-Efficient Llama 2 Inference on FPGAs Via High Level Synthesis

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文 + 附录 A.1、A.2 的 Table 7）。图 1、图 2 只有残缺的文字提取，表格数字清晰可读。

## Summary

问题：GPU 推理能耗高，不适合边缘场景；作者想用 HLS（Vitis HLS，C/C++）代替 RTL，快速做出一个 Llama 2 的 FPGA 推理加速器。

方法（§3）：
- 基于 Karpathy 的 llama2.c，只加速一次 forward pass 的 kernel，host 通过 XRT/DMA 传 token 和 position，并在 host 端做采样。
- 模型为 TinyStories 上训练的 110M 参数 Llama 2（dim 768，12 层，12 头，上下文 1024）。
- 权重做 post-training 对称 int8 量化（GGML 的 "Q8_0" 方案，分组缩放），覆盖 embedding、attention、FFN；RMSNorm 参数保持 fp32。
- HLS 优化：pipelining（matmul 和 RoPE 主循环）、loop unrolling、array/memory partitioning、通过 AXI4 做 256-bit 宽 burst 读写（每周期读 64 个 int8）。
- 与 FTrans、NPE 等工作不同，作者保持稠密矩阵乘和精确的非线性函数，不做剪枝或分段线性近似。

结果（§4）：
- 硬件：AWS f1.2xlarge（VU9P）；CPU 为 t2.2xlarge（Xeon E5-2686 v4）；GPU 为 RTX 3090；batch size 1。
- Perplexity（Table 1）：量化 2.9679，未量化 2.9667（42M 模型为 3.1810）。
- 速度（Table 2）：FPGA 57.11 tok/s，CPU 23.21 / 19.63 tok/s（256 / 1024 tokens），GPU 107.00 / 107.24 tok/s。FPGA 约为 CPU 的 2.46 倍，约为 GPU 的 0.53 倍。
- 平均功耗（Table 5）：FPGA 9 W，CPU 42.5 W，GPU 126.9 / 130.6 W。
- 每 token 能耗（Table 6）：FPGA 0.04 mWh，CPU 0.51 / 0.60 mWh，GPU 0.33 / 0.34 mWh。256 tokens 时比 CPU 低 12.75 倍，比 GPU 低 8.25 倍。
- 代码开源，并记录了综合步骤。

## Evidence and Limits

- 能耗是用平均功耗乘以延迟算出来的（我用 Table 3 和 Table 5 核对过，数字吻合）。CPU 和 GPU 用 CodeCarbon 测量。AWS 虚拟化环境下 CPU 功耗无法直接读取，只能按经验数据估计。FPGA 功耗来自 Vivado 和 AWS 工具，未说明是实测还是估计，也未说明是否包含 host 端功耗。三者的测量口径不一致。
- FPGA 延迟 17.51 ms 与附录 Table 7 综合报告里 forward 的平均周期数换算出的 17.510 ms 完全相同，且 256 和 1024 tokens 两栏的 FPGA 数字一模一样。文中也说「参照 NPE，从系统仿真得到时序」。所以 FPGA 速度很可能是综合/仿真估计，不是板上实测，正文没有明说。
- 公平性：GPU 跑的是 Meta 原版实现（推测为浮点，文中未明说精度），CPU 的软件栈也未说明，FPGA 是 int8。作者承认无法给 GPU 提供同等量化的基准。因此速度和能耗的对比不是同精度对比。
- 实验用的是 110M 的 TinyStories 小模型，作者自己说明了原因：片上存储和外部内存带宽限制（受限于每周期读 64 个 int8）。没有 7B 及以上规模的结果。Perplexity 只在 TinyStories 验证集上测，没有下游任务评估。
- 只做 batch size 1；作者承认 GPU 在大 batch 下可能更省能耗。
- 每组实验重复 100 次取平均，temperature 1、空 prompt；未报告方差。
- 未与其他 FPGA transformer 加速器做定量对比，只做了文字上的相关工作比较。
- 文中提到的 hls4ml 不支持 attention 的说法没有实验验证。

## Open Questions

- FPGA 的 tok/s 和功耗是否在 F1 板卡上实测过？还是综合报告和 Vivado 估计值？
- 同样的 int8 方案放到 GPU 或 CPU 上（用专门 kernel），能耗差距会缩小多少？
- 换成更大的模型（需要外部内存、4-bit 量化或多块 FPGA），延迟和能耗优势还在吗？

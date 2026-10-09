---
title: "LlamaF: An Efficient Llama2 Architecture Accelerator on Embedded FPGAs"
updated: 2026-10-09
---

# LlamaF: An Efficient Llama2 Architecture Accelerator on Embedded FPGAs

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文、参考文献；无附录）。图 1-3 仅有提取出的文字标签，算法与表格基本完整可读。

## Summary

问题：1.1B 级 Llama2 类模型（TinyLlama，FP32 约 4.4GB）超出嵌入式 FPGA（ZCU102：4GB DDR、5.11MB 片上）的内存与带宽能力，作者称这是首个在嵌入式 FPGA 上加速 Llama2 架构的工作（§I, §VI）。

方法：
- 量化：对权重（embedding、attention、FFN、classifier）做 group-wise 对称 INT8，GS=256，激活运行时也量化为 INT8（W8A8）；RMSNorm 权重不量化。模型由 4.4GB 降到 1.1GB（§III-A）。
- Profiling：TinyLlama 在 ZCU102 PS（4 核 A53 + OpenMP）上，矩阵计算占前向时间 97.64%-98.98%，multi-head attention 占 0.47%-1.82%，随位置增大（Table II）。因此只把矩阵-向量乘（GQMV，Algorithm 1）放到 PL，attention、softmax、RoPE、RMSNorm、SwiGLU 留在 PS。
- 硬件（§IV）：HLS DATAFLOW 三级流水——pre-processing（INT8 转 INT16，x 及其 scale 缓存在 BRAM）、dot-product（GS 宽 SIMD 乘 + 深度 8 的加法树，INT32 累加）、accumulate（INT32 转 FP32 乘 scale）。两个 kernel 分别对应列数 dim（2048）与 hidden_dim（5632）。
- 软件（§III-B）：拼接共享输入的权重（Wq/Wk/Wv，W1/W3）以减少 kernel 启动；逐层把权重装入 111.5MB 缓冲而非一次装 1.1GB；下一层权重的传输与当前 kernel 执行重叠（异步调度，Fig. 2）。

结果（Table VI，ZCU102，205 MHz，batch=1，greedy）：GQMV 0.201 GOPS（PS）对 4.696 GOPS（FPGA），23.4x；step=64/128/256 时 LlamaF 为 1.478/1.424/1.328 tok/s，PS 约 0.093 tok/s，即 15.8x/15.3x/14.3x；能效 0.291 对 0.0480 tok/s/W，6.1x。无调度版本为 0.936/0.915/0.853 tok/s，异步调度带来 55.6%-57.9% 提升。资源占用：LUT 59.72%、FF 31.31%、BRAM 24.45%、DSP 20.95%（Table III）。
精度：WikiText-2 PPL 由 7.05 升至 7.09（Table V）。

## Evidence and Limits

- 唯一的对比基线是同一份量化模型在同板 ARM PS 上的实现，没有与其他 FPGA 工作（如 FlightLLM、FQ-BERT）或其他边缘硬件（GPU、手机 SoC）的数值对比；相关工作部分只做定性讨论。"14.3-15.8x"是相对一个很弱的 CPU 基线。
- 绝对速度仅 1.3-1.5 tok/s，仍然很慢；速度随 step 增大下降，作者归因于 PS 上的 attention（Table II），但没有给出分解测量。
- 功耗只在 step=256 下用 SCUI 测量，未给出具体瓦数，只给出 tok/s/W；测量方法粗略，未说明是否为整板功耗。
- 量化误差：Table IV 平均绝对误差 0.000265；平均相对误差 3.30%，标准差 11.57%。PPL 只比较了 TinyLlama 一个模型、一个数据集；SQuAD 子集仅用于测速，没有给出问答质量。
- 文中称"每周期传输 16 个 8-bit 值"，并给出 HP AXI 带宽，但没有做 roofline 或带宽利用率分析，GOPS 是否受带宽限制未验证。
- 摘要与正文对带宽优化的表述为主要贡献，实际证据是端到端 tok/s，没有单独的消融（如不同 GS、不同位宽）。
- 代码与比特流未在文中提及，复现需自行实现。文中未见 PPL 测试的序列长度与评测细节。

## Open Questions

- 在 4.7 GOPS 与 AXI 带宽之间，加速器离内存带宽上限还有多远？瓶颈是带宽、kernel 启动开销，还是 PS 端工作？
- 把 attention 移到 PL（作者未来工作，近似 softmax）后，长上下文下的 tok/s 衰减能否消除，近似带来的精度代价是多少？
- 更低位宽（如 W4）或更大模型在该平台上是否可行，精度与速度如何权衡？

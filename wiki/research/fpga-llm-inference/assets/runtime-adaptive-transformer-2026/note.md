---
title: "A Runtime-Adaptive Transformer Neural Network Accelerator on FPGAs"
updated: 2026-10-09
---

# A Runtime-Adaptive Transformer Neural Network Accelerator on FPGAs

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：正文全文与附录算法（Algorithm 1–17）的 PDF 文本；图 7–13 的数据点在文本提取中丢失（仅剩坐标轴标签），只能依据正文叙述；参考文献部分未细读。

## Summary

ADAPTOR 是用 Vitis HLS 写的稠密 Transformer encoder/decoder FPGA 加速器，目标是同一份比特流在不重新综合的情况下跑不同规模的模型，不依赖稀疏化（摘要、§1）。

- 架构（§4）：注意力部分拆成 QKVPM、QKPM、SVPM 三个顺序执行的处理模块，每个 head 一份实例；FFN 拆成 FFN1/2/3PM，其中 FFN1、FFN3 之后接 LayerNorm。每个 PE 对应一个 DSP48 做 MAC。另有 Load_Weights/Inputs/Biases、激活（LUT 实现的 softmax/ReLU/GeLU）、LayerNorm、Bias_add 单元。
- 分块（§5, Fig. 6）：MHA 权重只沿列分块（d_model/TS_MHA 块），FFN 权重沿行列两个方向分块，部分和在片上累加。块大小在综合时固定。
- 运行时可调（§5, Table 1）：序列长度、head 数、层数（enc/dec）、embedding 维、hidden 维、输出数，通过 MicroBlaze 经 AXI-Lite 写寄存器设置，上限由综合时的资源决定。软件侧用 Python 解析 PyTorch .pth 抽取参数，再生成 C 代码。
- 解析模型（§6）：给出 DSP（式 8）、BRAM（式 25）与各模块延迟（式 9–39）的估计公式。
- 评测（§7）：平台为 Alveo U55C、ZCU102、VC707。默认配置 d_model=768、12 head（Table 3 中为 8 head）、SL=64，TS_MHA=64、TS_FFN=128（实际为块数，见 §5 的“24 块/6 块”最优结论），频率 200 MHz，DSP 3612（40%）、LUT 391k（30%），动态功耗 11.8 W（Vivado 估计）。
- 关键结果：
  - 与 Qi 等人的稀疏加速器相比，浅层 Transformer 上 27 GOPS 对 14/12 GOPS；自定义 encoder 上 132 GOPS 对 75.94 GOPS（Table 2）。
  - BERT 上 40 GOPS，低于 TRAC（128 GOPS）和 Tzanos 等（65.7 GOPS）；论文自述 TRAC 的 GOPS 高 3.2 倍、GOPS/DSP 高 8.4 倍。
  - 功耗效率：BERT 上比 K80 GPU 高 1.2 倍、比 i7-8700K 高 2.87 倍（Fig. 10）；Jetson TX2 与 RTX K5000 在 BERT 上能效更高。
  - 解析模型与实测延迟平均偏差 1.8%，DSP 偏差 0.71–4.7%，BRAM 偏差 5.7–74%（Table 3）。
  - 可移植性：同一小模型（d=200, 3 head, 2 层, SL=64）在 U55C 用大块、ZCU102/VC707 用小块（25/50, 50/50），延迟随块变小而增加（Fig. 11）。

## Evidence and Limits

- 摘要和结论的“1.7 到 2.25 倍加速”只对应 Qi 等人的稀疏设计，且是在各自的网络上比较；在 BERT 上论文自己的 Table 2 显示 ADAPTOR 吞吐低于 TRAC 与 Tzanos。结论里的“outperforms leading FPGA accelerators”表述偏强。
- 功耗对比：ADAPTOR 用 Vivado 综合后的功耗估计（动态功耗，对所有模型恒为 11.8 W），而 CPU/GPU 的数据取自各自文献，模型、批量、精度与测量方式不一致；不是同条件复现。文中也承认 Jetson TX2 因稀疏算法能效更高。
- 理论峰值 1200 GOPS，实测仅约 53 GOP/s 上限（roofline，Fig. 12）；原因是各子模块顺序执行、循环依赖限制流水。块增大后频率下降，GOPS 反而降到 30–32（Fig. 13）。
- “运行时自适应”有边界：块大小固定，各维度只能在综合上限内变化；论文未在同一比特流上系统演示多个不同模型的端到端切换结果，主要实验是改参数后的延迟与资源。decoder 的单独评测未见数据。
- 精度：文中提到“fully quantized”，但所读文本未给出位宽与量化后的任务精度（如 BERT 准确率）。
- 解析模型 BRAM 误差大，原因是大块时用 LUTRAM 代替 BRAM；延迟验证只覆盖 4 组配置、仅注意力/FFN1/权重加载几项（Table 3），且最后一组 FFN1 为 0.18 对 0.23 ms，偏差明显大于 1.8% 的均值。
- 内存带宽公式（式 40）与 roofline 中“103,000 GB/s”的量级来自片上 BRAM/LUTRAM 宽度乘频率，不是片外 HBM 带宽；数值与单位的计算过程不易核对。
- 软件控制开销（秒级编译与下载）有描述，但未计入加速比较。
- 未复现：代码在作者 GitHub（见下），本人未运行；对比数字均取自论文。

## Open Questions

- 在同一比特流上，模型切换（如 BERT 与小型 encoder）的端到端延迟和利用率究竟是多少，是否都能接近解析模型的预测？
- 量化位宽与任务精度如何，decoder/生成式场景下的表现为何没有数据？
- 吞吐远低于理论峰值的瓶颈（顺序模块、频率下降）能否通过模块间流水或多模块并行消除，代价是什么？

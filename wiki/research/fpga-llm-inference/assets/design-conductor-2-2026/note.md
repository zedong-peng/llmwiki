---
title: "Design Conductor 2.0: An agent builds a TurboQuant inference accelerator in 80 hours"
updated: 2026-10-09
---

# Design Conductor 2.0: An agent builds a TurboQuant inference accelerator in 80 hours

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（12 页，含参考文献）。Figure 1/2 的文字内容在提取中有些混乱，Figure 5 仅有百分比标签；论文没有附录。

## Summary

Verkor 团队的技术报告（arXiv 2605.05170，2026-05）。上一版 Design Conductor 在 2025-12 用 12 小时做出一个 5 级流水 RISC-V CPU。这一版重写了多 agent harness（context 管理、subagent 管理、memory、knowledge，§3.1），并换用 2026 年 4 月发布的前沿模型。作者声称它能处理 80 倍大的任务，且全自动。

核心案例是 "VerTQ"（§2.1）：agent 从 TurboQuant 论文和一份软件实现出发，用约 80 小时完成架构探索、vLLM 集成、模块级设计与微架构、综合与 P&R、模块验证和系统仿真。VerTQ 位于主处理器与 DRAM 之间，压缩 KV cache（K 用 TurboQuant-Prod 加 1-bit QJL，V 用 TurboQuant-MSE），并在压缩域内做 FlashAttention 和 online softmax。

Table 1 给出的数字：KV cache 压缩 4.3x，内层 attention 循环乘法减少 16x，9-bank 内存接口，8 路 attention decoder 共 5,129 个 FP16/FP32 单元。单个 decoder 在 XCVU29P-3 上占 500,619 LUT、748 DSP48E2，时钟 125 MHz；8 路约 1.9M LUT。面积为 TSMC 16FF 估算值：单 decoder 约 2 mm2，8 路约 5.7 mm2。

另外三个设计（§2.2–2.4）：
- 全展开流水 AES-128 CTR 核：KU5P-3 上 >100 Gbps（1 GHz），ASAP7 7nm 上 >400 Gbps（3.2 GHz）。FPGA 与 ASIC 版本的 S-Box 实现不同。
- FP32 add/sub：KU5P-3 上 896 MHz、11 级流水、437 LUT，作者称时钟高于 Xilinx Floating-point v7.1 IP。
- 在 Corundum VOQ 交换核上加 line-rate BF16/FP32 in-network allreduce（用户给出非常详细的指令）：KU5P 上 14,236 LUT。

§3.2 列出新能力：自己写 spec（concept to layout）、架构取舍、根据时序/布局反馈重构 RTL（closing the loop）、数值优化（如 VerTQ 中自定义 exp 单元，改用五阶多项式、Horner 求值）。§4.1 Table 2 给出相对 token 和 wall-clock：以 VerCore 为 1.0x，VerTQ 为 12x token、6.7x 时间，AES 为 4x/4x。Figure 5 显示 token 主要花在验证和时序收敛。

## Evidence and Limits

- 这是技术报告，不是对照实验。每个设计只有一次展示，没有成功率、重复运行、方差、消融（harness 与模型各自的贡献）或人工基线耗时。"80x larger" 没有给出度量方式。
- VerTQ 的验证有限：系统仿真只跑 Qwen3-4B 的 36 层，上下文长度仅 64（§2.1.3，受仿真服务器限制）；没有给出端到端精度（perplexity 或任务指标）、吞吐、延迟、功耗。"maintaining full performance and quality" 是转述 TurboQuant，不是本文测量。
- 125 MHz 是用户在输入里指定的目标；FPGA 结果来自 Vivado out-of-context 的综合与 P&R，没有上板运行。ASIC 面积是估算，没有 ASIC 流程结果（VerTQ 部分）。
- 数值偏差：自定义 FP16/FP32 单元与 Python 参考有"小偏差"，作者称都追溯到合理的精度/成本取舍，但没给误差数据；高范数输入可能偏差更大（§2.1.4）。
- "to our knowledge novel" 的多项式分解、"superhuman clock rate"、"compares favorably with commercial IP" 均无独立验证，对比只列了时钟、流水深度和资源的大致关系，AES 对比对象是厂商 IP 页面。
- VerTQ 用户输入已指定许多关键选择（3 PQ bits + 1-bit QJL、Qwen3-4B、FP16 KV、125 MHz、DAZ/FTZ、不做错误处理），所以"自主架构判断"的程度难以评估。
- 作者自述局限（§4.2）：过度谨慎（简单问题也要 20 分钟复查）、有时用复杂 RTL 改动解决本可用后端脚本解决的问题、目标过激（如时钟过高）、人工 review 是瓶颈。
- 对前作"预训练数据里有开源 RISC-V"的质疑，作者仅在脚注里称其"specious"。AES、FP32 加法、Corundum 同样是公开存在的设计。
- 无代码、无设计文件链接；输入中的 repo URL 均被遮蔽。

## Open Questions

1. 在更长上下文（如 32k）和完整模型上，压缩域 attention 的精度与吞吐是否仍成立？论文只验证到 context 64，也未给出相对 GPU 或软件实现的性能。
2. 结果有多大比例来自 harness 重写，多大比例来自新模型？重复运行的成功率和成本波动如何？
3. 12x token 成本对应的绝对费用，以及与人工团队耗时/成本的比较，论文都没有给出。

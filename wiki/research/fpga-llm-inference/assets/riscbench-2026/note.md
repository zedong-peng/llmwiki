---
title: "RISCBench: Benchmarking RISC-V Orchestration Efficiency in FPGA and FPGA-Like Computing Engines"
updated: 2026-10-09
---

# RISCBench: Benchmarking RISC-V Orchestration Efficiency in FPGA and FPGA-Like Computing Engines

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（仅一页的 FPGA'26 extended abstract，含参考文献）。Fig. 1 只有图注，图本身在文本中缺失；全文没有表格和数字结果。

## Summary

论文关注异构系统中由 RISC-V 控制核（soft FPGA core 或 hard accelerator-class core）承担的 orchestration（数据搬运、同步、调度）。作者认为 FLOPs、TOPS/W、energy per operation 等指标只刻画算术能力，看不到 orchestration 效率，而后者常常决定持续吞吐（Introduction）。

作者提出 RISCBench：一个轻量 benchmark suite 加配套方法学。核心指标是 Sustained Instantaneous Throughput (SIT)，把"高效率执行"阶段的贡献累积成实际的持续吞吐，用来描述高效执行能维持多久，而不是峰值速率。文中没有给出 SIT 的公式。

实验快照：用 Nios-V soft RISC-V core 在 FPGA 上做原型，验证能集成进可重构环境；在嵌入大量 hard RISC-V 控制核的加速器平台（引用 Tenstorrent Wormhole）上做评估。负载是驻留在 SRAM 的 tiled matrix kernel，目的是去掉外部存储器的影响。执行 trace（Fig. 1）显示早期窗口吞吐接近 aggregate 峰值，随后因同步开销和 memory residency 切换累积而下降。作者的定性结论是：全片上驻留时出现峰值，随协调开销和带宽争用增加，持续性能下降。

套件声称开源，发布在 www.riscbench.com。

## Evidence and Limits

- 论文只给了定性描述，没有任何具体数值：没有吞吐、利用率、核数、矩阵尺寸、tile 大小、频率或 SIT 的取值。
- SIT 的定义、归一化方式、窗口选取、"platform-independent"的论证都没有写出；这一说法目前没有证据支持。
- 没有 baseline 对比：没有说明 SIT 比传统指标多揭示了哪些具体差异，也没有与其他 benchmark（如 MLPerf、Rodinia 等）比较。
- 评估只涉及 SRAM-resident tiled matmul；摘要提到适用于 AI inference，但没有跑任何 LLM 或模型级负载。
- Nios-V 平台只用于"验证集成"，没有报告结果；加速器平台的具体型号和配置只由参考文献 [3] 暗示。
- 作者来自工业界（Flapmax、Altera）和高校，文中未提利益冲突或独立复现。
- 代码与数据的可得性仅靠网站链接声明，本文本无法验证其内容。

## Open Questions

- SIT 的精确数学定义是什么？"high-efficiency execution"的阈值如何设定，不同平台间如何归一？
- Fig. 1 中的退化有多少来自控制核本身（同步、调度），有多少来自带宽争用和 memory residency，两者是否被分离测量？
- 在非 SRAM 驻留、带外部存储器和真实模型（如 transformer 推理）的负载下，SIT 与端到端吞吐的关系如何？

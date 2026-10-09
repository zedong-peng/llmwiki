---
title: "MEADOW: Memory-efficient Dataflow and Data Packing for Low Power Edge LLMs"
updated: 2026-10-09
---

# MEADOW: Memory-efficient Dataflow and Data Packing for Low Power Edge LLMs

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（MLSys 2025 版 arXiv 预印本，正文加参考文献，无独立附录）。图 6–13 的柱状图/表格在文本提取中只剩标注数字，部分图（如 Fig. 8/9/11/12b）的具体数值无法核对。

## Summary

问题：边缘低功耗 FPGA（Xilinx ZCU102，<10W，无 HBM，片外 DRAM 带宽 1–12 Gbps）上，LLM 把所有层按 GEMM 执行，prefill 阶段 Q、QK^T、softmax、SMxV 的中间结果反复写回/读出 DRAM，decode 阶段则被权重读取主导（§1, Fig. 1）。

方法有两部分：
- TPHS（token-parallel head-sequential）数据流（§3–4）：对 Q+SM(QK^T)xV 做跨 token 并行、逐 head 顺序的流水线，中间结果经 NoC 和 pipeline register 在 PE/softmax 模块之间直传，不落 DRAM。配套硬件有混合 GEMM/流水 PE、并行 MAC PE 与广播 MAC PE，以及 MAX/EXP/DIV 三级流水 softmax（EXP 用 LUT）。KV、Proj、MLP 仍走 GEMM。
- Weight Packing（§5）：把量化后权重矩阵沿内积维切成 C 个元素的 chunk，建 Unique Matrix 并用 chunk ID 编码（无损）；再用按 packet 变精度编码（mode bits）和按频率重排 ID 提高 DRAM 传输打包率；片上 WILU 模块解包并查表还原。文中称 OPT-125M/1.3B 权重的 reduction ratio 在 10^2 到 10^3 量级（Fig. 4a）。

结果（ZCU102，100 MHz，84 并行 + 12 广播 PE，8-bit W/A，SmoothQuant 量化 OPT-125M/OPT-1.3B；§6）：
- 对 GEMM 基线（同一架构全 GEMM 模式）：12 Gbps 下 TTFT 低 1.5–1.7×（125M）、1.5–1.6×（1.3B）；1 Gbps 下 1.57–2.5× 和 1.55–2×（Fig. 6）。TBT 在 12 Gbps 低 1.4–1.52×，1 Gbps 低 1.4–1.53×（Fig. 7）。
- 权重打包消融（OPT-125M 第 1 个 decoder 的 MLP1）：朴素打包 1.4×，packet 变精度 1.54×，加频率重排 2.63× 的权重传输延迟下降（Fig. 10a）；MLP1 分解出 1272 个 unique chunk，需 11-bit 编码。
- 对 CTA、FlightLLM（在 MEADOW 架构上自行实现，均 W8A8）端到端延迟改善“超过 40%”（§6.4, Fig. 11）。
- DeiT-S/DeiT-B 上延迟低 1.5–1.6×（§6.6）。
- 配置扫描（PE 数 14–96，带宽 1–51 Gbps）：高带宽时 GEMM 更优，低带宽时 TPHS 更优（Fig. 12）。

## Evidence and Limits

- 精度：OPT-125M 和 OPT-1.1B（原文正文称 1.1B，评测处写 1.3B，前后不一致）8-bit 量化后 LAMBADA 准确率为 60.7% 和 69.7%。权重打包声称无损，但文中没有给出打包前后的精度对比，也没有量化基线的 FP16 精度。
- 所有加速比来自 FPGA 上的实现，但延迟看起来是在同一架构的分析/周期模型上得到（文中未说明是实测还是仿真，也没给出板上功耗测量）；“<10W”是预算而非测量值。
- 基线偏弱：GEMM 基线是 MEADOW 自身架构的全 GEMM 模式，不是已发表加速器的原始实现；CTA 与 FlightLLM 也是移植到 MEADOW 架构上重新实现，且去掉了 FlightLLM 的 HBM 前提，对它们不一定公平。FlightLLM 的稀疏、CTA 的 token 压缩是否带来精度变化未讨论。
- 权重打包的收益依赖权重的 chunk 重复度，只展示了 OPT 两个模型；chunk 大小 C、unique matrix 本身的传输/存储开销、解包硬件的资源与周期开销没有给出具体数字。
- 模型很小（125M/1.3B），未覆盖 7B 级以上模型；KV cache 在 decode 阶段的读写开销以及更长序列未单独分析。decode 阶段的收益几乎全来自权重打包，TPHS 在 decode 只有边际作用（§6.1 自述）。
- 未找到代码或 artifact 声明，结果无法独立复现。

## Open Questions

- 权重打包的 unique matrix 与编码索引的总体积相对原始 8-bit 权重到底压缩多少，不同 chunk 大小下的取舍是什么？
- 延迟数字是板上实测还是模型预测？WILU 解包与频率重排在资源（LUT/BRAM）和时钟频率上的代价是多少？
- 对更大的模型（如 7B）或其他量化位宽（4-bit）后，chunk 重复度是否仍然足够高？

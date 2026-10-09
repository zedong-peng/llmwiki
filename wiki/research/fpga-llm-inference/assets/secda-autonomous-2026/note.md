---
title: "Towards Autonomous Accelerator Design: FPGA Accelerator Generation with SECDA"
updated: 2026-10-09
---

# Towards Autonomous Accelerator Design: FPGA Accelerator Generation with SECDA

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（6 页，含附录 prompt）。Figure 1/2 只有标题，图内容未提取；Table I 可读。

## Summary

MLArchSys@ISCA 2026 workshop 论文，是作者此前 SECDA-DSE（ref [17]）的评估扩展。SECDA-DSE 在 SECDA 生态内用 LLM 引导 FPGA 加速器的设计空间探索（DSE），输入为目标 workload、FPGA 设备和架构约束（§III）。

方法由三部分组成：
- DSE Explorer：枚举计算单元尺寸、tiling、buffer、dataflow 的参数组合，实例化为 SECDA 模板，得到延迟、资源、数据搬运指标（§III-A）。
- LLM Stack：RAG（向量化 SECDA 知识库，graph-based 检索，对代码注释做 fuzzy matching）、CoT prompting、LoRA 微调（数据为已探索的配置及其硬件评估结果，人工把关）（§III-B）。
- Evaluation/反馈环：SystemC 仿真、HLS、综合、FPGA 执行。失败设计作为负样本回灌给 LLM（§III-C）。

本文评估：用自然语言 prompt（附录）生成三个加速器，分别是逐元素向量乘（VMUL）、2D 卷积、矩阵转置。平台为 Xilinx Zynq-7000（xc7z020），Vivado HLS 2019.2，LLM 为本地 Ollama 部署的 TinyLlama 1.1B，之前只在矩阵加法和矩阵乘数据点上微调（§IV）。

主要结果（Table I）：
- 三个设计均通过与 CPU 参考结果逐元素比对的功能验证，生成的加速器逻辑未经手改。
- 延迟：Conv 163 ms，VMUL 135 ms，Transpose 238 ms。
- DSP 利用率：VMUL 21.82%，Conv 1.36%，Transpose 5.45%。Transpose 的 LUT 最高（8.85%）、DMA 传输最大（512/524 bytes）。
- HWC 周期（加载/计算/写回）：Conv 1251/76/1250，VMUL 52/26/51，Transpose 393/311/387。
- 收敛所需迭代数：Conv 1 轮，VMUL 4 轮，Transpose 9 轮（前 2 轮 HLS 可综合，后 7 轮才通过逻辑综合和 FPGA 执行）。

## Evidence and Limits

- 论文的结论是"生成的设计体现 workload 相关的计算/访存取舍"。证据只有三个小 kernel 的单次测量和 DSP/LUT/DMA 数字的对比，没有基线，也没有消融。
- 没有与手写 SECDA 设计、HLS 基线或其他 LLM 硬件生成方法比较。没有 DSE 效率数据（探索时间、搜索了多少配置、找到的 Pareto 点），摘要所称"reducing exploration time"没有数据支持。
- 作者明说目标是"端到端执行"而非优化性能（§IV），所以延迟数字（百毫秒级，对这类小 kernel 偏大）只说明能跑通，不说明设计好。
- 流程仍是 human-in-the-loop：HLS、综合、传文件、跑脚本由人操作，只是称不修改生成的逻辑。自主性目前只体现在题目里。
- 一次成功的案例只有 Conv；Transpose 需要 9 轮，VMUL 4 轮。每个 workload 只跑了一次，没有重复或成功率统计。
- RAG、CoT、微调各自的贡献没有隔离验证。"graph-based 检索降低开销、提高相关性"（§III-B）没有给数据。"负样本强化"没有给具体机制。
- 数字不一致：引言写 VMUL 延迟 154 ms，Table I 为 135 ms。
- 局限（作者自述，§V）：需要足够多样的初始硬件数据点做微调；人工评估环节；仅三个 workload、单一 FPGA；模型大小、架构、板卡的影响尚未研究。
- 参考文献 [17]（前作）的 arXiv 编号为 2401.12345，疑似占位符，无法据此核对前作内容。
- 未给出代码、数据集、微调数据或模型的链接。

## Open Questions

- 在不是 SECDA 模板能直接覆盖的 workload（更大的卷积、带复用的 GEMM 类）上，1.1B 模型加上少量微调数据能否稳定生成可综合的设计，成功率如何。
- "DSE"体现在哪里：论文展示的是单个设计的修复迭代，而不是在参数空间上优化延迟/资源的搜索，两者的关系和收益未量化。
- 去掉 RAG、CoT 或 LoRA 后迭代数和成功率会如何变化。

---
title: "SpeedLLM: An FPGA Co-design of Large Language Model Inference Accelerator"
updated: 2026-10-09
---

# SpeedLLM: An FPGA Co-design of Large Language Model Inference Accelerator

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（仅 2 页的 HPDC'25 摘要型论文）。Fig. 1、Fig. 2 的图内数据未能从文本中提取，只有正文对结果的文字描述。

## Summary

SpeedLLM 是在 Xilinx Alveo U280 上实现的 Tinyllama（Llama2 架构）推理加速器，面向边缘场景（§1、§2.1）。架构由 Matrix Processing Engine、Memory Management 和 Special Function Unit 组成（Fig. 1）。论文声称三点贡献（§2.1）：

- 定制数据流水线：多级 read-compute-write 迭代，让计算单元持续有数据可算，避免空转。
- 内存分配复用策略：内存段处理完即循环复用，不必等全部处理结束，由调度算法跟踪使用模式并预测可用性。
- Llama2 算子融合：把多个算子合并为一个复合算子，减少中间数据的读写。

结果（§3.2）：延迟比未优化加速器最高快 4.8 倍；能效比未优化加速器高 1.18 倍，比"无融合"版本高 1.01 倍。文中还称，按 V100S、A100、U280 约 12000、17000、8000 美元的价格，U280 的 tokens/s/美元更优（§3.2.2）。

## Evidence and Limits

- 评测设置（§3.1）：Llama2 架构、在 TinyStories 上训练的模型（llama2.c 项目），用 stories15M 和 tokenizer.bin；在真实 U280 上实现，用 Vitis 2021.1 做 RTL 仿真验证。
- 基线只是自家的"未优化"、"无并行"、"无融合"版本。没有与 GPU、CPU 或其他 FPGA LLM 加速器（如 FlightLLM）做实测对比。
- 4.8 倍是"最高"值，正文没有给出具体 batch、序列长度、token 数，也没有给出表格；latency 与 throughput 的定义见 §3.2.1，但未报告 throughput 数值。
- 能效的 1.18 倍只说"吞吐更高、功耗相当"，没有给出功耗测量方法和绝对数值。1.01 倍的融合收益基本在噪声量级。
- 成本效率的结论依赖引用的标价，没有在同一模型上测 GPU，因此"性价比更优"没有实测支持。
- 模型仅 15M 参数，远小于一般意义的 LLM；摘要称"edge"，但 U280 是数据中心卡，边缘部署的说法没有论证。
- 没有资源占用（LUT/DSP/BRAM）、频率、精度/量化、准确性验证的数据，也没有消融分析各项贡献的单独收益。
- 未见代码链接；未发现可复现所需的细节。

## Open Questions

- 4.8 倍加速在什么配置下取得，三项优化各自贡献多少？
- 方法能否扩展到参数量更大的模型（如 1B 以上），片上存储和 HBM 带宽是否成为瓶颈？
- 与 GPU 或其他 FPGA 加速器在同一模型上的实测延迟、能耗对比如何？

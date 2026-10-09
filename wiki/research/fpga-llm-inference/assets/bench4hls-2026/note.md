---
title: "Bench4HLS: End-to-End Evaluation of LLMs in High-Level Synthesis Code Generation"
updated: 2026-10-09
---

# Bench4HLS: End-to-End Evaluation of LLMs in High-Level Synthesis Code Generation

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文 + 参考文献）。Fig. 2/3/4 的图内文字提取杂乱，只能依据正文与 Table II 的数字；无附录。

## Summary

问题：LLM 生成 HLS（C/C++）代码的评测工作很少，已有基准（Gai et al. 52 题、HLS-Eval 94 题）只看语法/功能或可综合性，不含 PPA 和 DSE（§I, §II.C, Table I）。

方法：提出 Bench4HLS，包含 170 个 {自然语言指令, HLS C/C++ 参考实现, testbench} 三元组（§III.A）。来源包括 VerilogEval、Vitis-HLS-Introductory-Examples、教材、CHStone、HLS4ML、Rosetta；Verilog 部分由 GPT-5 移植成 HLS-C++，指令也由 GPT-5 生成，再人工检查并仿真验证。平均每题 88 行。

评测流程（§III.C-D, Algorithm 1）：Vitis HLS 编译、C 仿真、综合；Vivado 做布局布线与功耗估计；报告 Pass@K（K=1/5/10）以及相对参考设计的 LUT/FF/DSP/BRAM/延迟/功耗差值。工具层声称可插拔（Vitis 为主，称在 Catapult 上试过）。每题可附 YAML 描述 DSE 空间（clock、pipeline II、unroll、array partition、dataflow、Vivado strategy 等），自动扫描。

结果（§V, Table II）：Qwen2.5-Coder 14B/32B、Llama 3.3 70B、GPT-5 四个模型，目标器件 Artix-7 xc7a200，Vitis/Vivado 2024.1。Pass@10 下编译/仿真/综合通过率：GPT-5 97.65/72.35/71.76%，Llama 3.3 70B 97.65/64.12/63.53%，Qwen 32B 92.35/39.41/38.24%，Qwen 14B 65.88/30.59/28.82%。Pass@1 下 GPT-5 编译 85.29%、综合 50.00%。DSE 使 GPT-5 约 40% 的题至少一项 PPA 改善超过 20%，Qwen-14B 约 10%（Fig. 3）。

## Evidence and Limits

- 模型只有四个：Qwen 与 Llama 本地 4-bit 量化，GPT-5 走 API。没有任何 HLS 专用模型或微调模型，也没有 prompt 或温度的敏感性分析。Pass@K 的采样方式（样本数、温度）未交代，"top-K candidates" 的说法也含糊。
- 数据集规模前后不一致：摘要和正文说 170 题，Fig. 1 与 §III.B 又写 200 题。
- 参考设计的质量证据不足。正文称其为 "well-optimized, efficiency-oriented"，"establish a meaningful upper bound"，依据只是 GPT-5 生成结果在 Fig. 2 中 PPA 更差；但参考设计大部分由 GPT-5 从 Verilog 移植而来，prompt 里要求加 pragma，没有与专家实现或其他基线对比。这一论断证据不够。
- 指令由 GPT-5 生成、参考代码也由 GPT-5 移植，存在评测 GPT-5 时的自偏置风险，文中未讨论。
- 摘要宣称功能验证覆盖 C 仿真、协同仿真和实现后网表仿真，且 "only timing-clean" 的设计才计分；正文结果部分只给出编译/仿真/综合三级通过率，没有给出协同仿真或网表级、时序（WNS）的统计。
- Fig. 2 的 PPA 差值只针对 GPT-5，未给其余模型的 PPA 汇总数字。"smaller models diverge further" 主要靠图形观察，正文无数值。
- DSE 部分的比较口径（"至少一项 PPA 指标变化超过 20%"）较宽松，不同模型成功样本数不同，难以直接对比。
- 声称 "first holistic benchmark" 偏强；"模型与脚本在论文接收后发布"（脚注 2），而代码仓库链接已在脚注 1 给出。论文已发表于 DATE 2026。

## Open Questions

- 170 与 200 到底哪个是最终规模？参考设计与 DSE 搜索得到的最优解之间差距多大？
- 对以 GPT-5 生成/移植的数据，其他模型的结果是否被系统性低估？
- Catapult 上的"成功测试"具体覆盖了哪些题和指标？

---
title: "RTLLM: An Open-Source Benchmark for Design RTL Generation with Large Language Model"
updated: 2026-10-09
---

# RTLLM: An Open-Source Benchmark for Design RTL Generation with Large Language Model

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（arXiv v3，6 页短文，ASP-DAC 2024）。表格 III/IV 为文本抽取，版面有错位，Table IV 的颜色标注（红/绿）丢失，只能依据正文描述。无附录。

## Summary

问题：此前用 LLM 生成 RTL 的工作（Thakur et al.、Chip-Chat、Chip-GPT）的目标设计都很小，由作者自己提出，自然语言描述不统一，且只看正确性、不看设计质量，难以公平比较（§I, Table I）。

基准：RTLLM 含 30 个设计，其中 11 个算术、19 个逻辑，规模从 8 位加法器到简化 RISC CPU（Table II）。HDL 行数中位数 52、均值 86、最大 518；综合后网表 cell 数均值 408、最大 2435（Table I）。每个设计提供三个文件：自然语言描述 L（含模块名与 I/O 位宽）、testbench T、人工参考设计 V_H（§III.B）。

三级评测目标（§III.A）：syntax（能否被 Design Compiler 综合）、functionality（能否通过 testbench）、quality（综合后的 PPA，与 V_H 对比）。流程自动化，支持 Verilog/VHDL/Chisel，只要能综合和仿真。

Self-planning：两步 prompt。第一步让 LLM 先给出推理步骤，并列出需要避免的语法错误；第二步把原描述加上该 plan 再生成 RTL，不需要人工参与或已有设计数据（§IV）。

结果（§V, Table III）：每个设计向每个模型查询 5 次，只要有一次通过即记 functionality 成功。

| 模型 | Syntax | Func. |
|---|---|---|
| GPT-3.5 | 55% | 10/30 |
| GPT-4 | 81% | 15/30 |
| Thakur et al. (CodeGen-16B 微调) | 40% | 5/30 |
| StarCoder-15B | 27% | 5/30 |
| GPT-3.5 + SP | 73% | 14/30 |
| GPT-4 + SP | 90% | 19/30 |

质量（Table IV）：只对语法正确的生成设计做综合；在"各指标最优设计数"这一汇总上，GPT-4 最多，GPT-3.5+SP 次之，且两者在部分设计上优于人工参考。

## Evidence and Limits

- 设置：Synopsys DC（compile ultra）综合，VCS 仿真；时钟频率设得极高以使所有设计都出现负 slack，便于比较 timing（§V.A）。比较对象仅 GPT-3.5/4、Thakur、StarCoder；未给出温度等采样参数，GPT 版本号与调用时间也未说明。
- functionality 采用 5 次中任一次通过（pass@5 式）的口径；syntax 百分比是 30×5 个样本的通过比例。两者口径不同，表中 Func. 列不反映单次成功率。
- Testbench 只采样有限用例，作者明确承认通过并不等于功能 100% 正确（§III.A）。
- 质量对比较粗：作者自己指出各目标之间存在强 trade-off，"最优数量求和"不严谨（§V.C）。Table IV 里有一些异常值（如 parallel2serial 面积 1.06、功耗 0，adder_32bit 面积仅 58 对比参考 571），可能是生成的设计被综合优化掉或功能不同，正文未解释。
- Self-planning 的提升（GPT-3.5 从 10/30 到 14/30，GPT-4 从 15/30 到 19/30）基于单次实验、每设计 5 个样本，无方差或显著性分析，也没有消融（如只要 plan 或只要语法建议）。个别设计上 SP 反而变差（如 GPT-4 在 multi_pipe_4bit 加 SP 后 Func. 由 ✔ 变 ✘；GPT-3.5 在 mux 上 SP 使语法从 0 升到 4 但功能仍失败）。
- 个别设计（risc_cpu、div_8bit、asyn_fifo 等）所有模型几乎都失败，说明对复杂设计的区分度主要来自少数几个设计。
- 声称"接近 GPT-4"：GPT-3.5+SP 14/30 对 GPT-4 15/30，数据支持。声称"更全面"：以行数和 cell 数对比 Table I，数据支持，但 30 个设计规模仍较小。
- 未复现；代码与数据声称在 GitHub 开源。

## Open Questions

- 5 次中任一通过的 Func. 口径下，单次采样的成功率是多少？不同温度下 self-planning 的收益是否稳定？
- Self-planning 的增益来自推理 plan 还是语法错误提示？论文没有消融。
- 综合时设极高频率的做法下，timing 指标（WNS）是否真能反映设计本身的时序质量？

---
title: "VerilogEval: Evaluating Large Language Models for Verilog Code Generation"
updated: 2026-10-09
---

# VerilogEval: Evaluating Large Language Models for Verilog Code Generation

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（arXiv v2，含参考文献）。图 6–9 的曲线只有标题和说明，数值图无法读取；表格 I–IV 文本完整。

## Summary

问题：当时的 Verilog 代码生成评测规模小（Thakur 等 17 个设计，RTLLM 30 个设计），题目类型单一，缺少统一的自动功能测试。本文参照 HumanEval 构建 VerilogEval，并探索用合成数据做监督微调（SFT）(§I, §II)。

基准：
- 从 HDLBits 选出 156 道自包含（不含模块实例化）的题，覆盖组合电路到有限状态机 (§II-A)。
- 两套题面。VerilogEval-human 由人工把原站的电路图、真值表、卡诺图、状态转移图和波形改写成纯文本（状态图用边列表，波形用带时间步的表），共 156 题 (§II-B-2)。VerilogEval-machine 由 gpt-3.5-turbo 根据参考代码生成题面，先零样本，再用已通过的描述做 4-shot，最终保留 143 题（首轮 108 题，再补 35 题）(§II-B-1)。
- 测试：Docker 中用 Icarus Verilog 仿真，把生成代码与参考解在时钟边沿（组合电路则在输入变化时）逐点比对输出，激励包括人工设计与随机生成的样本 (§II-C)。
- 指标：pass@k，采用 HumanEval 的无偏估计。图 6 说明 BLEU 区分不了正确与错误解，图 7 说明 n 太小时 pass@k 方差大 (§II-D)。

SFT：用 gpt-3.5-turbo 为 GitHub 上筛出的自包含 Verilog 模块生成描述，得到 8,502 对 (描述, 代码)，共 11MB，用 MinHash 去重（Jaccard 0.8）(§III-A)。在 CodeGen 系列（350M 到 16B 的 nl / multi / verilog 版本）上微调，n=20 采样，top-p 0.95，温度 0.8，单个 8×A100 节点 (§III-B)。

主要结果（Table II，pass@1 / 5 / 10）：

| 模型 | machine | human |
|---|---|---|
| gpt-3.5 | 46.7 / 69.1 / 74.1 | 26.7 / 45.8 / 51.7 |
| gpt-4 | 60.0 / 70.6 / 73.5 | 43.5 / 55.8 / 58.9 |
| codegen-16B-verilog-sft | 46.2 / 67.3 / 73.7 | 28.8 / 45.9 / 52.3 |

- SFT 对 multi 模型提升明显，对 verilog 模型在 machine 上提升明显，在 human 上提升小甚至略降 (§III-B-2)。
- 更大的模型整体更好。
- Table III：16B 的 multi-sft 比 nl-sft 在 machine 上只高约 3 个点（pass@1 37.1 对 33.9），作者据此认为软件语言到 Verilog 的迁移有限。
- Table IV：2B-verilog 在 machine 上 pass@1 为 20.1，SFT 后 35.9，用错配的描述-代码对训练则为 21.4。
- 训练轮数增加时 pass@1 继续上升，pass@5 和 pass@10 下降，作者解读为过拟合 (§III-B-1)。

## Evidence and Limits

- 证据与结论大体吻合：基准构建方法写得清楚，开源，评测流程可复现；SFT 的对照（base 对 sft、sft 对 sft-error）能支持"数据质量重要"。
- "codegen-16B-verilog-sft 与 gpt-3.5 相当"只在 Table II 的数字上成立。human 上 pass@1 为 28.8 对 26.7，没有给置信区间或多次运行的方差。gpt-4 的数字是 v2 更正过的（脚注 4 承认 v1 有误）。
- machine 题面由 gpt-3.5 生成，并以"gpt-3.5 能做出通过的解"为过滤条件。这会使 machine 对 gpt-3.5 有利，题面也偏逐行翻译代码。作者自己承认不能保证没有歧义或错误。
- SFT 数据同样由 gpt-3.5 按同一模板生成，和 machine 基准同源。human 上收益小，作者归因于数据与 human 题面分布不一致，但没有做实验验证。
- "machine 与 human 结果相关性好，可作为下游指标"只由图 8 的趋势支持，文中没有给相关系数。
- 没有说明 SFT 数据与评测题之间是否做过去重或泄漏检查。4 道 human 题被用作生成描述的 few-shot 示例 (shift18、rule110、lemmings1、fsm3onehot)，而这些题也在 human 测试集中。
- 范围局限（作者自述）：只有小型、自包含模块，没有模块实例化；只测功能正确，不测可综合性和 PPA；受 Icarus Verilog 对标准支持程度的限制。
- 超参数和训练轮数（multi 10 轮，verilog 5 轮）看起来是按 VerilogEval 结果挑的，文中未说明是否有独立验证集。

## Open Questions

- human 与 machine 之间的差距有多少来自题面形式（图、表被改写成文本），有多少来自问题本身的难度？文中没有分离。
- SFT 数据与 machine 基准同源（都用 gpt-3.5 和同一模板）会让 machine 上的提升被高估多少，没有对照实验。
- 100 个样本内都没有通过的题被丢弃（156 到 143），这会使 machine 子集偏向容易的题，对难题上的结论有何影响尚不清楚。

---
title: "Exploring Code Language Models for Automated HLS-based Hardware Generation: Benchmark, Infrastructure and Analysis"
updated: 2026-10-09
---

# Exploring Code Language Models for Automated HLS-based Hardware Generation: Benchmark, Infrastructure and Analysis

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（ASP-DAC'25，8 页，含参考文献）。图 6–9 的柱状图数值只部分能从文本提取，反馈循环（Fig. 7/8）和耗时（Fig. 9）的具体数值未能完整读出；无附录。

## Summary

问题：HDL（Verilog 等）训练数据少（Fig. 1：StarCoder 中 HDL 不足 C++ 的 1%）、预训练代码 LLM 的知识难以迁移、生成 HDL 所需 token 多（Fig. 2 示例中约为 HLS 的 3~4 倍）。作者主张生成 C-based HLS（Vivado HLS）代码更合适，因为 HLS 与 C/C++ 语法语义相近。

方法（§3、§4）：
- 数据集：从 HLSyn、ML4Accel 收集 52 个 HLS 设计，按不同 pragma 组合（PIPELINE/PARALLEL/TILE 等）展开，过滤后得到 42,000+ 程序，设计按 4:1 划分训练/测试。每条数据为 Alpaca 格式 JSONL：指令 + 设计描述 + 参考设计。设计描述由 ChatGPT（3.5/4）从代码反向生成；测试集另有人工精修版 HumanRefine，对应 GPT 生成的 MachineGen。
- 评测：语法用 `gcc -fsyntax-only`；功能用每个测试样例的单元测试，对比生成代码与原代码的输出（矩阵则随机抽位置比对）。指标 pass@3。
- 框架：对 Code-Llama-7B 做 QLoRA SFT（axolotl）；推理时加 CoT 提示（4 步："考虑 FPGA 特性、确定程序结构、写逻辑、考虑数据类型与接口"）和两步反馈循环（先喂回语法错误位置，通过后再喂回功能缺陷）。

主要结果（MachineGen，§5）：
- SFT：语法 54.85% → 88.44%；功能 0% → 53.20%（Fig. 6a）。
- CoT：语法 88.44% → 94.33%；功能 53.20% → 61.45%（Fig. 6b）。
- 反馈循环：文中称第一轮提升明显、第二轮收益递减，语法反馈和功能反馈互相有益（Fig. 7/8，数值未在正文给出）。CoT 还降低了推理耗时；功能反馈最耗时（Fig. 9，约 5–11 秒/条）。
- 复杂度（Table 2）：easy/medium/difficult 语法 96.67/96.67/90%，功能 63.33/53.33/53.33%。
- MachineGen vs HumanRefine（Table 3）：语法 93.83% vs 47.29%，功能 62.24% vs 21.36%。
- 生成设计在 VCU118、200MHz、Vivado 2020.1 下综合（Table 1，8 个设计，延迟 0.304–579 ms，BRAM 均为 0）。

## Evidence and Limits

- 核心动机"HLS 比 HDL 更适合 LLM 生成"没有直接对比实验：没有在同一数据/模型上训练 HDL 生成作为基线。支持证据仅是 Fig. 1/2 的数据量与 token 数示例（单个乘法器的例子），以及 HLS 自身的通过率。作者在 §5.8 也承认综合运行时间等总成本的对比留待未来。
- 唯一的基线是未微调的 Code-Llama-7B；没有与其他模型（GPT-4 等）、其他 HLS 数据集或已有 HDL 方法比较。只用了 7B 一个模型，4×L20 GPU。
- 数据集仅 52 个基础设计，其余 42,000 个是 pragma 变体；文中说按设计 4:1 划分，但测试集条数、划分是否严格按设计隔离写得不清。测试集多样性有限（作者自认），结果的泛化性存疑。Fig. 9 用 120 条数据计时，可能即测试规模，但未明说。
- 功能正确性靠"输出对比 + 随机抽样位置"，不是形式化验证；"功能通过"不含 HLS 可综合性、PPA 质量检查（作者说未把硬件性能作为反馈）。Table 1 只是展示综合结果，无基线对照；其中 syrk 与 stencil3d 延迟均为 21.537 ms，原因文中未解释。
- 数字轻微不一致：Fig. 6b 的 94.33%/61.45% 与 Table 3 MachineGen 的 93.83%/62.24% 不同（可能是不同运行或配置，文中未说明）；摘要/贡献处"over 40,000"与正文"42,000"。
- 设计描述由 GPT 生成，MachineGen 上高分与 HumanRefine 上大幅下降（功能 21.36%）表明对提示风格敏感，作者归因于训练数据偏向机器生成提示。
- 单次实验，未报方差或重复次数；pass@3 采样设置（温度等）未给出。
- 作者未提供代码链接；"评测基础设施"是否开源文中未说明，无法验证。

## Open Questions

- 与同规模 HDL 微调的直接对比如何？HLS 的 token 优势在计入综合时间与 pragma 优化后是否仍然成立？
- 测试集是否与训练集共享同一基础设计的 pragma 变体？若是，53%–61% 的功能通过率可能被高估。
- CoT 提示与反馈循环各自的增益在更强模型（如推理模型，作者列为未来工作）上是否还存在？

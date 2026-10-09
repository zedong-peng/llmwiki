---
title: "LLM-Driven Design Space Exploration of FPGA-based Accelerators"
updated: 2026-10-09
---

# LLM-Driven Design Space Exploration of FPGA-based Accelerators

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（约 4 页 workshop 短文，含附录 prompt）。图 1–4 为图片，文本中只有题注，未读到图内容；表格完整。

## Summary

- 问题：FPGA 加速器的设计空间（计算单元维度、tiling、存储层次、dataflow）大，人工探索依赖专家经验，且每轮迭代需要 HLS 与评估，周期长 (§1)。
- 方法：SECDA-DSE，在 SECDA / SECDA-TFLite 生态上加两个组件 (§3)。
  - DSE Explorer：输入目标 workload、目标 FPGA、架构约束指令；按 SECDA 模板实例化候选配置，每个排列生成一个 run 目录（源码、HLS 生成的 RTL、FPGA 映射设计），收集性能与资源数据，汇总为 "hardware data points" (§3.1)。
  - LLM Stack：基于 Ollama 本地推理；RAG 检索带注释索引的 SECDA-TFLite 代码库片段；CoT 提示；Evaluation 模块通过 MCP 调用 SECDA 组件；用 LoRA 在探索产生的数据（配置、workload/器件上下文、仿真是否成功、延迟、资源）上微调 (§3.2)。
  - 评估流程：先 SystemC 仿真，再综合与硬件执行；失败配置记为负样本；初期 human-in-the-loop，数据积累后计划去掉人工。
  - 为避免陷入局部最优，称会保持探索多样性，同时利用成功与失败样本 (§3.2.2)。
- 结果（仅一个初步实验，§4）：用自然语言 prompt（附录）描述逐元素向量乘法加速器（X、Y 长度 L，AXI-Stream 加载，load-compute-store），LLM Stack 生成了完整 SECDA-native 工作区（SystemC 描述、构建集成、软件驱动）。Vivado HLS 2019.2，目标 xc7z020，5.00 ns 时钟，估计关键路径 3.950 ns，满足约束。总延迟 0–2060 周期（至多 10.3 us），II 同范围，顶层未流水 (Table 1)。资源：BRAM_18K 6/280，DSP48E 3/220，FF 993/106,400，LUT 1113/53,200 (Table 2)。
- 意义：展示了 LLM 从自然语言生成可过 HLS 的 SECDA 加速器的可行性；完整的 DSE 闭环属于设计愿景。

## Evidence and Limits

- 证据范围很窄：一个玩具 kernel（向量逐元素乘），仅 HLS 估计值，没有 FPGA 板上执行，没有 SystemC 仿真数据，没有与任何基线（人工设计、其他 LLM-DSE 方法、随机搜索）比较，也没有说明用的是哪个 LLM。
- 摘要与结论说 "demonstrate feasibility"，实际只证明了第一步（单次生成并通过 HLS），未验证 DSE 循环、RAG、CoT、LoRA 微调、反馈强化中任何一项的作用。
- "reinforced fine-tuning"、"reinforcement" 在文中实际是 human-in-the-loop 反馈加 LoRA 监督微调，没有给出强化学习目标或训练细节。
- 与 iDSE、LUMINA、LIMCA 的区别只在定性描述（LLM 嵌入加速器设计流程、带硬件反馈环），没有实验对比。
- 作者自述挑战 (§5.4)：仿真评估仍然昂贵；数据点的一致性和代表性；LLM 在欠探索区域仍可能给出次优设计。MCP 全集成、综合评估、大规模基准均为 future work (§5)。
- 延迟表中范围写法（如 Send 7-1030）未解释依赖什么参数；"0 到 2060 周期" 的上下界含义文中未说明。
- 未给出代码或数据链接，目前无法复现。

## Open Questions

- 在真实 DSE 任务（如 GEMM / 卷积加速器的 tiling 与阵列维度搜索）上，LLM 引导相对于传统搜索（贝叶斯优化、遗传算法）能否在评估次数或最终质量上占优？文中没有任何此类数据。
- 小规模本地 LLM（Ollama）加 LoRA 微调，在有限的 hardware data points 上能否学到可泛化的设计规律，还是只记忆已探索配置？
- 人工反馈环如何被替换为自动环，且保证生成设计的功能正确性（目前只看到 HLS 通过，没有功能验证结果）？

---
title: "HLSFactory: A Framework Empowering High-Level Synthesis Datasets for Machine Learning and Beyond"
updated: 2026-10-09
---

# HLSFactory: A Framework Empowering High-Level Synthesis Datasets for Machine Learning and Beyond

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本，含正文与 Artifact Appendix；图（Fig. 5-11）只有标题和正文描述，图中具体数值与 Table 1 的勾选符号在文本中缺失。

## Summary

问题：已有 HLS 数据集（Spector、Rosetta、HLSDataset、HLSyn、DB4HLS、MLSBench 等）规模小、只覆盖部分 benchmark、多绑定单一厂商、数据组织各自为政，外部用户难以贡献新设计（§1, §2, Table 1）。作者认为缺的不是又一个数据集，而是可复现、可扩展的数据集构建框架。

方法：HLSFactory 是 Python 库，分三个阶段，每个阶段前都有用户入口（Fig. 1）。
- Stage 1 设计空间扩展与采样：OptDSL 前端基于 Vitis HLS Tcl 脚本，用方括号参数化 directive（unroll、pipeline、array_partition 等），设计空间为各参数的笛卡尔积，可随机采样（§3.2）。扩展不由优化目标引导，刻意保留次优设计。
- Stage 2 设计综合：ToolFlow 子类调用 Vitis HLS/Vivado 或 Intel i++/Quartus 完成 HLS 与实现（§3.3）。
- Stage 3 数据聚合：DataAggregator 把综合/实现数据、工具运行元数据、构建产物统一成 JSON（§3.4, Fig. 4）。
- 并行后端基于 Python multiprocessing，把多个 dataset 的所有设计放进同一个进程池（fine-grained），可绑核（§4.3）。

内置设计来自 PolyBench、MachSuite、Rosetta、CHStone、Kastner 教材、Xilinx 示例及作者组的加速器（Appendix 7.1.2）。

七个 case study：
1. 复现 Dai 等人的方法，用 histogram-based gradient boosting 预测实现后 QoR；29 个基础设计扩展到 257 个，完整训练集比 25% 子集的 R² 和平均相对误差更好，多数资源项相对误差低于 HLS 自身估计（§5.1, Fig. 5）。
2. 采样设计在 latency、LUT、FF 上覆盖范围更宽；基础设计多数不用 DSP/BRAM，采样后才出现；PaCMAP 嵌入显示不同基础设计的覆盖区域基本不重叠（§5.2, Fig. 6-7）。
3. 32 核上 fine-grained 并行比 naive 并行快超过 20%（§5.3, Fig. 8）。
4. 加入 Intel i++ 流：对 PolyBench/MachSuite 采样 n=1340，array_partition 用 hls_numbanks/hls_bankwidth 近似替代；i++ 无 latency 估计，用时钟频率作性能代理（§5.4, Fig. 9）。
5. 通过 Stage 2 入口接入 LightningSim 的 33 个设计，一名研究生不到一小时完成（§5.5）。
6. 通过 Stage 3 入口并入 HLSyn 数据（n=3371），与自有 167 个设计的 HLS 估计分布对比（§5.6, Fig. 10）。
7. Vitis HLS 2021.1 与 2023.1 的回归对比，每个基础设计 16 个样本，用配对 Wilcoxon 检验（α=0.05）；部分指标均值与中位数的变化方向相反；该实验由一名研究生三小时搭好（§5.7, Fig. 11）。

## Evidence and Limits

- 论文本质是框架/系统论文，主张的“易扩展、多用途”主要靠 case study 演示，没有与现有数据集或其他构建流程做定量对比；Table 1 只做功能勾选对比。
- Case 1 数据量小（257 个设计，80/20 划分），只有一个模型类型，没有多次随机划分或置信区间；结论是“更多数据更好”，不能单独说明随机扩展优于其他采样策略。“优于 HLS 自身估计”仅限“多数”资源目标。
- Case 3 的“超过 20%”只在一个配置（32 核、一组设计）上给出，没有给出多次运行。
- 易用性数字（一小时、三小时）是作者自述的单人经历。
- Intel 流的 directive 并非一一对应，Xilinx 与 Intel 的具体设计点不互相对应；Intel 的 QoR 度量与 Xilinx 不同。
- 作者自述局限：不支持仿真后指标（向量功耗、仿真 latency）；采样目前只有随机采样，主动学习等为未来工作；OptDSL 之外的设计空间需自写前端。
- 复现：代码 AGPLv3，数据 CC BY-SA 4.0，Zenodo 归档；复现需 Vitis HLS/Vivado 2023.1 与 2021.1、Intel HLS/Quartus 21.1.0 等商业工具，最大数据集约 24 小时（32 核），磁盘约 200 GB。可用预生成数据只跑分析脚本。PaCMAP 即使固定 random_state 也不完全确定。我没有重新运行任何实验。

## Open Questions

- 随机采样得到的设计分布与真实设计者会选择的配置有多大差距，扩展出的次优/冗余设计对 QoR 预测泛化的贡献如何量化？
- 数据集规模（几百到几千个设计）与基础设计数量（29 个）相比，对跨 kernel 泛化（留出整个基础设计）的效果没有评估。
- 新工具版本回归测试只展示分布差异，没有解释差异来源，也未说明不同版本间 directive 语义是否一致。

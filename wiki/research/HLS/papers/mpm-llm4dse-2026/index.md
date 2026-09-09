---
title: "MPM-LLM4DSE: Reaching the Pareto Frontier in HLS with Multimodal Learning and LLM-Driven Exploration"
domain: research
area: HLS
type: paper
status: processed
updated: 2026-09-08
tags: [paper, hls, dse, multimodal, llm, qor-prediction]
---

# MPM-LLM4DSE: Reaching the Pareto Frontier in HLS with Multimodal Learning and LLM-Driven Exploration

- **arXiv**: [2601.04801](https://arxiv.org/abs/2601.04801v1)
- **Venue**: DATE 2026
- **Authors**: Lei Xu, Shanshan Wang, Chenglong Xiao (Shantou University)
- **Code**: [github.com/wslcccc/MPM-LLM4DSE](https://github.com/wslcccc/MPM-LLM4DSE)

## 问题

HLS DSE 面临两个核心瓶颈：
1. **QoR 预测不准**：GNN 仅从 CDFG 提取控制/数据流信息，丢失了源码中的语义特征（如 pragma 的意图和作用域）
2. **DSE 算法不理解 pragma 语义**：传统多目标优化（NSGA-II、SA、ACO）不考虑 pragma 对 QoR 的领域知识

## 方法

### 1. Multimodal Prediction Model (MPM)

**数据表示**：Graph-Text 双模态
- **Graph 分支**：C/C++ → LLVM IR → ProGraML CDFG → ECoGNN 提取图级嵌入 $h_\mathcal{G}$
- **Text 分支**：pragma + 源码 → CodeBERT-c tokenize → 取最后一层 CLS token 平均 → 文本嵌入 $h_\mathcal{S}$

**ECoGNN**（Enhanced Cooperative GNN）：
- 基于 CoGNN 扩展为有向图，定义 5 种节点状态 {S, L_in, L_out, B, I}
- 用 Gumbel-Softmax 实现可微分的节点动作选择
- Global node attention 替代 average pooling 得到图级表示

**融合机制**：
- $h_\mathcal{G}$ 作为 Query，$h_\mathcal{S}$ 作为 Key/Value
- Multi-head attention 融合 → Gated network 动态控制信息流
- MLP prediction head → RMSE loss

### 2. LLM4DSE（LLM-Driven DSE）

**PEODSE prompt 工程方法**，包含 4 部分：
1. **Task description**：任务背景 + pragma 对 QoR 的影响分析
2. **High-quality solution examples**：OPRO 风格动态更新的优质配置
3. **Task instruction**：显式指导 + pragma 影响知识（如 pipeline=off 减少 LUT 但增加 latency）
4. **Solution generation exemplars**：CoT 推理示范

**迭代流程**：
LLM 生成配置 → Data Generator 生成 Graph-Text 嵌入 → MPM 预测 QoR → 更新 Pareto 集 → 重构 prompt → 循环

## 实验

### 数据集
- **训练集**：15 个 kernel（MachSuite + PolyBench），共 4353 个 graph-text 样本
- **推理/DSE 集**：6 个 unseen kernel（heat-3d, jacobi-1d, jacobi-2d, nw, seidel-2d, stencil）
- **平台**：AMD Ultrascale+ MPSoC ZCU104，Vitis-HLS 2022.1 + Vivado 2022.1

### QoR 预测结果（RMSE，unseen kernels）

| Model | Latency | LUT | DSP | FF | BRAM |
|-------|---------|-----|-----|----|----- |
| GNN-DSE | 0.7759 | 0.0025 | 0.0023 | 0.0078 | 0.0023 |
| ProgSG | 0.4061 | 0.0041 | 0.0018 | 0.0081 | 0.0025 |
| ECoGNN-only | 0.4019 | 0.0016 | 0.0015 | 0.0016 | 0.0015 |
| LM-only | 0.3920 | 0.0011 | 0.0011 | 0.0015 | 0.0009 |
| **MPM** | **0.3870** | **0.0004** | **0.0004** | **0.0015** | **0.0005** |

关键发现：LM-only > ECoGNN-only，说明源码语义对 QoR 预测的价值被低估。

### DSE 结果（ADRS，越低越好）

| Method | Avg ADRS |
|--------|----------|
| NSGA-II | 0.0447 |
| SA | 0.0572 |
| ACO | 0.0758 |
| LLMMH | 0.0388 |
| LLM4DSE (GPT-4o) | 0.0324 |
| **LLM4DSE (Qwen3-235B)** | **0.0305** |

LLM4DSE(Qwen3) 比 LLMMH 提升 21.39%，比传统元启发式平均提升 39.90%。

## 与 ForgeHLS 的关系

| 维度 | MPM-LLM4DSE | ForgeHLS |
|------|-------------|----------|
| 预测目标 | Latency + 资源（LUT/DSP/FF/BRAM） | 资源（LUT/FF/DSP） |
| 输入表示 | CDFG + 源码（多模态） | 纯文本（pragma + 源码序列化） |
| 模型 | ECoGNN + CodeBERT + MHA 融合 | LLaMA3-8B QLoRA 微调 |
| DSE | LLM 作为优化器生成配置 | 不做 DSE，直接预测 |
| 数据集 | GNN-DSE benchmark（15+6 kernels） | ForgeHLS-lite（425 kernels） |
| 评估指标 | RMSE | MAPE |
| 泛化方式 | 训练集 kernel → unseen kernel | design-level split / kernel-level split |

**互补性**：MPM-LLM4DSE 侧重 GNN+LM 多模态融合和 LLM-driven DSE；ForgeHLS 侧重端到端 LLM 微调做资源预测，数据规模更大（425 kernels vs 21 kernels）。

## 局限性

- 依赖 API 调用 LLM（GPT-4o/Qwen3），DSE 运行时间长（7000-11000s）
- 训练集仅 15 个 kernel，泛化能力有限
- 需要 LLVM + ProGraML 工具链生成 CDFG，部署复杂
- 未报告 MAPE，难以与 ForgeHLS 直接对比预测精度

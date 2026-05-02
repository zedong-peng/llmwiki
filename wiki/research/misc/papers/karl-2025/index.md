# KARL: Knowledge Agents via Reinforcement Learning

**Authors:** Databricks AI Research
**arXiv:** [2603.05218](https://arxiv.org/abs/2603.05218)
**Venue:** Databricks (preprint)

---

## 一句话总结

KARL 用 agentic synthesis pipeline 生成多样化训练数据 + iterative large-batch off-policy RL（OAPL）训练 grounded reasoning agent，在 KARLBench（6 个异构检索任务）上达到 Pareto-optimal，cost/latency 更低时质量超过 Claude 4.6 和 GPT 5.2。

---

## 问题与动机

**Grounded reasoning**（需要从外部知识库检索证据并推理的任务）在企业场景极具价值，但现有工作存在两大问题：

1. **Benchmark 碎片化**：HotpotQA、BrowseComp、FinanceBench 等各自只覆盖单一能力切片，无法评估跨领域泛化
2. **训练数据质量**：纯 prompting 或静态 synthesis 难以生成多样、grounded、高难度的训练数据

核心挑战：如何训练一个能在**约束驱动实体搜索、跨文档报告合成、表格数值推理、穷举实体检索、程序化技术推理、内部笔记事实聚合**等异构任务上都表现优秀的 agent？

---

## 方法

### 1. KARLBench：多能力评估套件

6 个任务，各自隔离一种结构性挑战：

| 任务 | 能力 | 语料规模 |
|---|---|---|
| **BrowseComp-Plus** | 约束驱动实体搜索 | 100k 文档 |
| **TREC-Biogen** | 跨文档报告合成（生物医学） | 26.8M 文档 |
| **FinanceBench** | 长文档遍历 + 表格数值推理 | 53k 页 |
| **QAMPARI** | 穷举实体搜索（百科） | 256k chunks |
| **FreshStack** | 程序化技术推理（软件文档） | 49k chunks |
| **PMBench** | 内部笔记事实聚合（企业场景） | 3.4k 文档 |

**设计原则**：
- 只提供 vector search 工具（隔离检索 + 推理能力，不混入工具编排效应）
- Closed-corpus（避免 live web 的不可控变量）
- 保留原始文档结构，不做 dataset-specific 的 re-chunking 或语义增强

### 2. Agentic Synthesis Pipeline

**核心思想**：让 agent 动态探索语料库，用 vector search 生成 grounded QA pairs。

**Pipeline**：
1. Agent 用 long-horizon reasoning + tool use 从语料中检索证据
2. 生成 question-answer pairs，确保 grounded（有检索证据支撑）
3. **Iterative bootstrapping**：用训练出的更强 agent 重新生成数据，持续自我改进

**泛化性验证**：同一 recipe 在 TREC 和 BrowseComp-Plus（两个完全不同的搜索行为）上都有效。

### 3. Iterative Large-Batch Off-Policy RL (OAPL)

**与 online GRPO 的区别**：
- **Off-policy**：收集大规模离线数据集，跨多次 policy update 和 training run 摊销数据生成成本
- **Robust to trainer–inference discrepancy**：不需要 clipped importance weighting、data deletion、router replay 等 heuristics（这些在 online GRPO 训练大规模 MoE 时被认为必需）
- **Multi-task training**：直接组合 BCP 和 TREC 的 loss，两个任务同时改进，且在 4 个 held-out 任务上 OOD 泛化

**理论基础**：拥抱 off-policyness，用 principled objective 设计，降低基础设施复杂度。

---

## 实验

**Base model**：GLM 4.5 Air

**对比基线**：Claude 4.6 (Sonnet/Opus)、GPT 5.2

**主要结果**：

| 维度 | KARL 优势 |
|---|---|
| **Cost-quality Pareto** | 在相同质量下成本更低 |
| **Latency-quality Pareto** | 在相同质量下延迟更低 |
| **Test-time compute scaling** | 3 parallel rollouts 超过 Sonnet 4.6；10 parallel rollouts 匹配 Opus 4.6 |
| **OOD 泛化** | 在 4 个训练时未见过的 KARLBench 任务上持续改进 |

**Multi-task training 效果**：
- 在 BCP 和 TREC 上联合训练，两个任务同时提升
- 在 FinanceBench、QAMPARI、FreshStack、PMBench 上 zero-shot 泛化优于单任务训练

---

## 核心贡献

1. **KARLBench**：首个覆盖 6 种异构 grounded reasoning 能力的评估套件
2. **Agentic synthesis**：动态探索语料库生成 grounded 训练数据，支持 iterative bootstrapping
3. **OAPL**：sample-efficient、robust、支持 multi-task 的 off-policy RL 范式
4. **Pareto-optimal 结果**：在 cost/latency/quality 三维空间上全面优于 Claude 4.6 和 GPT 5.2

---

## 与 MemRL / EvoMaster 的关系

| 维度 | KARL | MemRL | EvoMaster |
|---|---|---|---|
| **学习目标** | Policy（通过 RL 优化 agent 行为） | Memory retrieval policy（Q-value） | Harness orchestration |
| **训练** | Off-policy RL（有参数更新） | 非参数 RL（Q-value 更新） | 无训练 |
| **数据来源** | Agentic synthesis | Runtime feedback | 无（纯 inference） |
| **泛化机制** | Multi-task RL | Q-value 收敛 | 结构化 inference-time scaling |
| **应用场景** | Enterprise grounded reasoning | Runtime self-evolution | 科学研究 agentic workflow |

KARL 是**有训练的 RL agent**，MemRL 是**无训练的记忆学习**，EvoMaster 是**无训练的 inference-time orchestration**——三者在"agent 如何变强"的路径上完全不同。

---

## 局限

- Base model 是 GLM 4.5 Air，未公开与 Claude/GPT 同等规模模型的对比
- KARLBench 只有 6 个任务，覆盖面仍有限
- Agentic synthesis 的 cost 未量化（需要 agent 动态探索语料库）
- PMBench 是内部数据集，无法公开复现
- Off-policy RL 的 sample efficiency 相比 online RL 的优势未做 ablation

---

## 关键引用

- OAPL (off-policy RL): Ritter et al. 2026
- BrowseComp-Plus: Chen et al. 2025
- TREC-Biogen: Gupta et al. 2024
- FinanceBench: Islam et al. 2023
- QAMPARI: Amouyal et al. 2023
- FreshStack: Thakur et al. 2025
- GLM 4.5 Air: Zeng et al. 2025
- DeepSeek-MoE (online GRPO baseline): Dai et al. 2024

---
title: "SciMaster: Towards General-Purpose Scientific AI Agents — X-Master as Foundation"
domain: research
area: misc
type: paper
status: processed
updated: 2026-04-25
tags: [paper, misc, agent, scientific-ai, benchmark, hle, tool-use, reasoning, agentic-workflow, neurips-2025]
---

# SciMaster: Towards General-Purpose Scientific AI Agents — X-Master as Foundation

## Paper Meta
- Title: SciMaster: Towards General-Purpose Scientific AI Agents — Part I. X-Master as Foundation — Can We Lead on Humanity's Last Exam?
- Author: Jingyi Chai, Shuo Tang, Rui Ye, Yuwen Du, Xinyu Zhu, Mengcheng Zhou, Yanfeng Wang, Weinan E, Yuzhi Zhang, Linfeng Zhang, Siheng Chen
- Affiliation: School of Artificial Intelligence, Shanghai Jiao Tong University; DP Technology
- Date: July 2025
- Venue: NeurIPS 2025 (preprint)
- arXiv: 2507.05241v2
- GitHub: https://github.com/sjtu-sai-agents/X-Master
- Topic: misc
- Paper Slug: scimaster-xmaster-2025
- Reading Source: arXiv TeX source (`neurips_2025.tex`)

## TL;DR
- X-Master 是一个以"代码为交互语言"的 tool-augmented reasoning agent，在 `<think>` 过程中生成 Python 代码调用外部工具，执行结果追加回 context，形成推理-工具调用的迭代循环。
- X-Masters 在 X-Master 基础上叠加 scattered-and-stacked agentic workflow（Solver → Critic → Rewriter → Selector），系统性扩展推理的广度（并行多解）和深度（迭代精炼）。
- 底座模型：DeepSeek-R1-0528（开源）；工具：Web Search + Web Parse（仅 2 个）。
- 在 HLE 文本子集（2,518 题）上达到 **32.1%**，首个突破 30% 门槛的开源方案，超越 OpenAI Deep Research（26.6%）和 Google Deep Research（26.9%）约 5 个点。
- 核心主张：不依赖大规模模型重训练，仅靠 inference-time computation + context 操控即可达到 SOTA；重点分享 practical know-how 而非新算法。

## Problem
- AI agent 要加速科学发现，首先需要真正理解人类知识前沿。HLE 作为极高难度 benchmark（~1,000 道专家题，500+ 机构）提供了合适的试金石。
- 现有 deep research 类产品（OpenAI 26.6%、Google 26.9%）均为闭源，社区无法复现和改进。
- 强推理模型（如 DeepSeek-R1）本身是 non-agentic 的，instruction-following 能力有限，如何在不 finetune 的前提下让其具备 agentic 行为？

## Method

### X-Master：单 Agent 基础架构

**代码作为交互语言（核心创新）**

在 `<think>...</think>` 推理过程中，agent 生成包裹在 `<code>...</code>` 标签内的 Python 代码：
- 代码通过 string matching 提取后在沙箱中执行
- 执行结果以 `<execution_results>...</execution_results>` 形式追加回 context
- Agent 可迭代调用，形成推理 → 工具 → 推理的循环

三大优势：
1. **通用性**：几乎所有功能都可以用代码实现
2. **精确性**：代码紧凑地表达精确需求
3. **兼容性**：可直接调用成熟 Python 库生态

**Initial Reasoning Guidance（Prompt 工程技巧）**

在模型输出初始 `<think>` token 后，直接嵌入引导文本（第一人称视角），例如：
- "I can answer this query effectively by leveraging access to external environments"
- "Every time I determine the need for interaction with external tools, I will generate Python code enclosed between `<code>` and `</code>` tags"

让模型"相信"自己具备 agentic 能力，无需 finetune。这是解决强推理模型 non-agentic 问题的关键 trick。

**工具集（仅 2 个）**

| 工具 | 功能 |
|---|---|
| Web Search | 调用 Google 搜索，返回：实体结构化事实 + 网页预览（标题/URL/摘要）+ 相关搜索词 |
| Web Parse | 通用网页解析（提取主内容 + 链接）；科学论文解析（优先 ar5iv HTML，fallback PDF，提取与问题相关段落） |

Solver 平均每题调用外部工具 **3 次**。

---

### X-Masters：Scattered-and-Stacked Agentic Workflow

四阶段流水线，类比 RL 中的 rollout（exploration-exploitation）：

| 阶段 | 角色 | 数量 | 职责 |
|---|---|---|---|
| Stage 1 | Solver | 5 个并行 | 生成 5 个初始解（tool-augmented reasoning） |
| Stage 2 | Critic | 5 个并行 | 逐一评估并修正每个 Solver 解 |
| Stage 3 | Rewriter | 5 个并行 | 综合所有 5 个解，生成 5 个精炼版本 |
| Stage 4 | Selector | 1 个 | 从 5 个 Rewriter 解中选出最优解 |

- **Scattered**（广度）：多路并行生成，探索不同解题路径
- **Stacked**（深度）：多轮迭代精炼，整合前序解的智慧

## Main Results

### HLE 主结果（文本子集，2,518 题）

| System | HLE Score |
|---|---|
| **X-Masters (ours)** | **32.1%** |
| Kimi-Researcher | 26.9% |
| Gemini Deep Research | 26.9% |
| OpenAI Deep Research | 26.6% |
| Gemini 2.5 Pro | 21.6% |
| DeepSeek-R1-0528（无工具） | 17.7% |
| Claude 4 Opus | 10.7% |

首个突破 30% 门槛；完全开源 vs. 闭源竞品。

### TRQA-lit（生物医学，172 题多选）

| System | Accuracy |
|---|---|
| **X-Masters** | **67.4%** |
| X-Master（单 agent） | 62.1% |
| OriGene（500+ 专业工具） | ~60% |
| STELLA | ~26% |

仅用 2 个通用 web 工具，超越配备 500+ 专业工具的 OriGene。

### HLE Biology/Medicine（222 题）

| System | Accuracy |
|---|---|
| **X-Masters** | **27.6%** |
| STELLA | ~26% |
| Biomni | 17.3% |

## Ablations

### 各阶段贡献（HLE）

| 配置 | Accuracy |
|---|---|
| DeepSeek-R1-0528（无工具） | 17.7% |
| + Solver（tool-augmented） | 21.1% |
| + Critic | 25.0% |
| + Rewriter | 30.6% |
| + Selector（完整 X-Masters） | **32.1%** |

- 工具增益：+3.4%
- Critic + Rewriter 增益：+9.5%（最大贡献来源）
- Selector：最终推至 32.1%

### Scattered vs. Stacked

| Scatter | Stack | Accuracy |
|---|---|---|
| ✗ | ✓ | 25.5% |
| ✓ | ✗ | 25.0% |
| ✓ | ✓ | **32.1%** |

两者缺一不可，组合产生协同效应。

### Rewriting 的作用
- Rewriting 显著提升"5 个解全部正确"的频率
- 是整个 workflow 中质量提升最大的单一环节

## Implementation Details
- **底座模型**：DeepSeek-R1-0528
- **Max completion tokens**：64k
- **Temperature**：0.6
- **评估次数**：3 次取平均
- **Judge model**：o3-mini（遵循 HLE 官方评测设置）
- **评测范围**：HLE 文本子集（2,518 题，遵循 Kimi-Researcher 设置）

## Key Judgments
- **"代码作为交互语言"比"特殊 token 触发工具"更通用**：无需为每个新工具手动修改 prompt，Python 生态直接可用。
- **Initial Reasoning Guidance 是关键 trick**：解决了强推理模型（R1 类）non-agentic 的核心问题，且无需 finetune，成本极低。
- **Rewriter 是 workflow 中最重要的环节**：+9.5% 的增益主要来自 Critic + Rewriter 阶段，而非 Solver 本身的工具调用（+3.4%）。
- **2 个通用工具 > 500 个专业工具**：在 TRQA-lit 上超越 OriGene，说明通用 web 工具 + 强推理能力的组合效率极高。
- **这是 inference-time scaling 的一个强数据点**：不训练模型，纯靠 agentic 架构设计，从 17.7% 提升到 32.1%（+14.4%）。

## Limitations
- 底座模型为文本模型，当前只评测 HLE 文本子集，多模态能力未涉及。
- Inference-time computation 开销较大（5 个并行 Solver + 多轮精炼）。
- 依赖外部网络工具，离线场景不适用。
- 论文定位为 Part I，科学专用工具（文献分析、科学计算、实验工作流）留待后续工作。

## Open Questions
- Scattered-and-stacked workflow 在 HLE 之外的科学任务（数学证明、实验设计）上的泛化性如何？
- Initial Reasoning Guidance 对不同底座模型的效果是否稳定？
- Part II 是否会引入 RL/SFT 来内化 agentic 能力，减少 inference-time overhead？
- Rewriter 的质量提升是否依赖 Solver 解的多样性？如何量化 scatter 的多样性？

## Takeaways
- **对 agent 架构研究**：scattered-and-stacked 是一个值得借鉴的 workflow 模式；Initial Reasoning Guidance 是让 non-agentic 推理模型具备 agentic 行为的低成本方案。
- **对 HLE leaderboard 追踪**：32.1% 是当前开源 SOTA（2025-07），可作为后续工作的参照基线。参见 [[../../threads/2026-04-25-llm-leaderboard-resources]]。
- **对 scientific AI 方向**：本文是"不训练模型，只设计 agent 架构"路线的一个重要数据点；2 个通用工具超越 500 个专业工具的结果值得重视。

## Related Work（来自 .bib）
- HLE benchmark: arXiv:2501.14249
- DeepSeek-R1: arXiv:2501.12948
- Search-R1: arXiv:2503.09516
- Search-o1: arXiv:2501.05366
- WebThinker: arXiv:2504.21776
- WebDancer: arXiv:2505.22648
- Agentic Reasoning: arXiv:2502.04644
- ToRL: arXiv:2503.23383
- ReTool: arXiv:2504.11536
- AI co-scientist: arXiv:2502.18864
- MetaGPT: ICLR 2024
- ChatDev: ACL 2024

---
title: "Dream-RSI: Recursive Self-Improvement through Evolving Worlds"
domain: research
area: misc
type: paper
status: active
updated: 2026-09-17
tags: [paper, recursive-self-improvement, exploration, replay, agent-harness, scientific-discovery]
---

# Dream-RSI: Recursive Self-Improvement through Evolving Worlds

## Paper Metadata

- Tong Zheng, Xidong Wu, Zheng Zhang, Zhankui He, Chaoyi Zhang, Benjamin Coleman, Ruoqiao Wei, Di Bai, Haolin Liu, Rui Liu, Xue Wang, Yue Zhuan, Wang-Cheng Kang, Renkai Xiang, Heng Huang, Xinwu Cheng, Yunsong Guo.
- Google、Google DeepMind、University of Maryland, College Park、University of Virginia 联合工作。
- [arXiv:2609.14858v1](https://arxiv.org/abs/2609.14858v1)，2026-09-14 提交；2026-09-17 查询时最新且唯一列出的版本。预印本，未核实会议录用。
- DOI: `10.48550/arXiv.2609.14858`；[项目页](https://dream-rsi.com/)；[官方仓库](https://github.com/zhengkid/Dream-RSI)。
- arXiv comments 写 12 pages；实际归档 PDF 含附录共 36 页。

## Local Assets

- [PDF](paper-pdf/2609.14858v1.pdf)
- [原始 TeX 压缩包](paper-tex/archives/2609.14858v1.tar.gz)、[main.tex](paper-tex/extracted/2609.14858v1/main.tex)、[结构化元数据](metadata.yaml)
- [官方仓库 README](github-repo/Dream-RSI/README.md)、[arXiv 身份与版本快照](supplementary/arxiv-abs-2609.14858.html)
- [检索记录与 API 错误](../../threads/2026-09-17-dream-rsi-search.md)

## Problem and Main Idea

昂贵的不是单个候选的评分，而是验证一个“如何分配长期搜索”的策略。Dream-RSI 将完整 discovery tree 变成历史回放环境，在已记录结果上廉价比较探索策略，再将选出的策略部署到真实搜索，积累新树并重复。

更新对象是 **exploration-policy code**，底层 coding agent、模型权重、evaluator 和执行接口保持固定。“Worlds”是已发生结果构成的 replay simulator；并非训练一个能够预测任意未见候选结果的生成式世界模型。

## Method

主要证据：[正式方法 §3](paper-tex/extracted/2609.14858v1/Main_Text/problem_formulation.tex)、[动机 §2](paper-tex/extracted/2609.14858v1/Main_Text/intuiton.tex)。

1. **Online explore**：根节点表示起始 workspace；非根节点保存一次生成—评估尝试的文件系统、产物、诊断与分数。每轮从根或当前叶节点选择至多 W 个起点并行执行；空 batch 表示停止。
2. **Replay**：从仅可见根节点开始，策略只看已揭示前缀。选择非根节点揭示其已记录后继；选择根则揭示最早尚未打开的根分支。没有记录的续接不产生新结果；顺序、分组和停止可以变化，候选产物本身不会重新生成。
3. **Dreaming**：固定的 policy-development agent 根据历史回放分数与轨迹修改策略代码。正式方法式 (1)：`V = best observed score − β₁ × revealed attempts + β₂ × attempts / max(1, rounds)`，对历史树平均后选最佳版本。
4. **Recursive deployment**：选中代码上线，新的真实轨迹加入累计 replay pool。包含原策略只保证固定历史池上的回放目标不下降，不保证新任务或下一轮真实搜索单调提升。

**附录与主文存在需要保留的差异**：[replay prompt](paper-tex/extracted/2609.14858v1/appendix/prompt/replay_learning_prompt.txt) 实际写 `pareto.reward = pareto.auc − lambda × parallel_penalty`，对固定 beta 网格扫描 attainment/work 曲线，要求 `OptimalPolicy.solve()` 和 `plan_grid()`；这不是主文线性目标的逐字实现。未发布完整 evaluator，因此不能断言二者等价。源包的 `Main_Text/method.tex` 是被 main.tex 注释掉的旧稿，不应当作正式主文。

Prompt 明确约束 deterministic、prefix-only、失败恢复、动态并行 portfolio、beta 跨轮调节和 width/depth 规划；这些是发布的设计要求，尚不是可核验的运行时隔离保证。线上 [exploration prompt](paper-tex/extracted/2609.14858v1/appendix/prompt/exploration_prompt.txt) 仍要求读历史 proposal 与评分，因此“history as simulator”不意味着完全取消历史上下文。

## Experiments

**全部为论文报告，未本地复现。** [实验 §4](paper-tex/extracted/2609.14858v1/Main_Text/experiments.tex) 覆盖 8 个任务、3 个领域。主要受控对照 Recursive Fixed Exploration 使用相同 agent、evaluator、初始化与每轮预算，第一轮策略相同。模型名称按原文记录：Gemini-3.1 Pro / Gemini-3.7-Flash，经 Gemini CLI 调用。

| 任务 / 指标 | Fixed Exploration | Dream-RSI | 边界 |
|---|---:|---:|---|
| Lasso Pro：6 个 held-out 数据集平均 runtime | 3587.1 ms / 550 calls | 2931.0 ms / 317 calls | 约 1.22× runtime 改善，1.74× fewer calls |
| Lasso Flash：相同指标 | 2516.7 ms / 3200 calls | 2350.6 ms / 1879 calls | 约 1.07× runtime 改善，1.70× fewer calls |
| Sum–Difference，越大越好 | 1.144047 | 1.145427 | Gemini-3.1 Pro，10 轮 |
| Circle Packing，越大越好 | 2.635983 | 2.635983 | 持平 |
| Autocorrelation，越小越好 | 1.456001 | 1.456375 | Dream-RSI 略差；SimpleTES 为 1.453675 |
| VGG16 / LayerNorm | 固定探索曲线 | 同等性能约少 2.43× / 1.79× generations | GPU kernel discovery call 效率 |
| ConvDiv / ConvMax | 固定探索曲线 | 相近预算下 2.09× / 1.44× inverse-runtime | 不等于整个系统端到端提速 |

Lasso 用 17 个 synthetic instances 搜索；held-out 为 Gisette、RCV1、DNA、Leukemia、Colon、Duke Breast。5 轮，每轮 Pro 最多 10×11=110 calls、Flash 最多 32×20=640。正确性要求每个 λ 的 objective 不超过 sklearn 对照 +1e-6，并使用与 timing 不同的 fresh instances；搜索分数为 runtime 的逆几何平均，表中 held-out 汇总是算术平均。

Lasso 完整表与曲线的正式来源是 [Figure 3 源码](paper-tex/extracted/2609.14858v1/Main_Text/Figures/scaling_lasso.tex)，不是未被引用且有空格子的旧 `table/lasso_main_results.tex`。162× 来自 SimpleTES 51,200 / 317 次调用；模型也不同（GPT-OSS-120B vs Gemini），不能解释成受控的美元/总算力节省。Dream-RSI 相比固定策略并非每个 held-out 数据集都更快，Pro 平均优势主要由 RCV1 驱动。

[数学结果 Table 1](paper-tex/extracted/2609.14858v1/Main_Text/table/math_optimization.tex) 和 [kernel Figure 4](paper-tex/extracted/2609.14858v1/Main_Text/Figures/kernelbench_scaling_curves.tex) 给出其余对照。数学每任务少于 1000 generations 是作者陈述，未给出逐任务完整 cost breakdown。论文未明确给出这些 kernel 测试的 GPU 型号、统一 dtype 和完整 timing 配置。

[分析 §5](paper-tex/extracted/2609.14858v1/Main_Text/further_analysis.tex)：ConvDiv 上额外注入方向性历史指导对两种方法均更差；策略在进步时减少尝试、平台期增加尝试。该结果范围是这个任务/提示，不支持“所有记忆/语义指导都会有害”。

## Code Inspection

官方仓库 commit `4149ea9181ab1db80f85717ffda2c9f0f130e85b`；检查 README、CITATION.cff 与文件清单，无 submodules。目前仅论文、网页展示素材；full codebase、discovered programs、reproduction scripts 都在准备发布。没有可检查的运行入口、policy/evaluator 实现、模型配置或训练代码。README 的 arXiv badge 与 CFF 占位符过时；以实时 arXiv 页面为准。

TeX 附录另含 [Lasso solver](paper-tex/extracted/2609.14858v1/appendix/discovered_programs/lasso/code.cpp)，已静态阅读：虽然扩展名 `.cpp`，内容是 Python 字符串包装的 C++，使用 Eigen double、OpenMP、64-byte aligned padding、active-set coordinate descent、lazy Gram 和 Cauchy–Schwarz KKT pruning，声明 `-fopenmp -ffast-math`。这些是产物实现观察，不是 Dream-RSI 控制器实现，也不构成正确性/性能验证。

## Limitations and Open Questions

- **作者方法边界**：历史只能覆盖已探索 support；不能评估真正未记录的候选结果。主文不是普适 RSI 收敛证明。
- **阅读判断：反事实偏差**。线上生成可能依赖跨分支历史；换探索顺序却固定已记录结果，不能完整模拟策略改变导致的候选分布变化。
- **阅读判断：成本口径**。主图累计 discovery-agent calls 未给出完整 policy-development LLM tokens/calls、回放、评估硬件与 wall-clock 成本；zero-execution-cost 指不重复执行 discovery/evaluator，不是整个 dreaming 免费。
- **阅读判断：泛化和不确定性**。Lasso 有 held-out 数据集；其余主要是同任务优化轨迹，不应据此断言跨任务策略泛化。未见多随机种子置信区间和完整复现配置。
- **待核验**：主文目标和 prompt AUC 目标的对应关系；固定 replay pool 过拟合；运行时 prefix-only enforcement。主文 policy-version 计数还存在 M 个候选 / M 次 revision 的索引表述不一致。

## Relation to This Wiki

归入 [[../../index#Self-Improving Agents and Harness Optimization]]，目前建立 misc 内的小分类，历史论文目录不迁移。

| 相关条目 | 改进对象 | 与 Dream-RSI 的关系 |
|---|---|---|
| [[../../papers/meta-harness/index|Meta-Harness]] | 整体 harness 代码 | 都利用完整历史和固定底层模型；Dream-RSI 专门优化探索调度，并增加离线 replay 反馈 |
| [[../../papers/erl-2026/index|ERL]] | 可检索经验 heuristics | 历史作为 test-time 指导，对照历史作为策略评测环境 |
| [[../../../agent-memory/index|Agent Memory]] | 记忆存储、检索与经验复用 | replay simulator 是经验复用的一种用途，不等于通用记忆架构 |
| [[../../../fpga-llm-inference/index|FPGA LLM Inference]] | 硬件实现与评估 | 阅读启发：昂贵编译/综合轨迹可复用作 DSE 调度反馈，但本论文没有 FPGA 实验 |

## Reading and Reproduction Status

阅读 arXiv v1 的 active TeX 主文、方法、实验、图表、分析、相关工作、结论、任务附录、两份完整 prompt、参考文献与附录 solver。PDF 核对标题/机构、版本与页数，图示另核对源图。归档原始 TeX/PDF、保持源码内部层级、记录哈希并固定官方仓库 commit。没有安装依赖、运行下载代码、调用模型或复现实验。

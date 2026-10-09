---
title: "Jev / System One：带概率的类型化决策模型"
domain: research
area: agent-memory
type: source
status: active
updated: 2026-09-22
tags: [jev, typesafe, system-one, structured-decisions, retrieval, calibration]
---

## Archive Reading Record

- Historical reading status: read; migrated existing notes without extending the reading scope.
- Recorded source: blog_and_documentation.
- Recorded scope: Blog visible body; FAQ hidden answers and visual media not inspected; Documentation bodies and relevant examples; Search core code; reranking sampling and scoring code; no execution.
- Recorded reading paths: `supplementary/introducing-system-one-models-and-jev.txt`, `supplementary/introduction.md`, `supplementary/models.md`, `supplementary/state.md`, `supplementary/confidence.md`, `supplementary/limitations.md`, `supplementary/line-by-line-search.md`, `supplementary/re-ranking.md`.
- Source versions, checksums, repository commits, and full historical metadata: [citation.bib](citation.bib).
- Source files currently absent (preserved existing deletion or unavailable cache): `supplementary/confidence.md`, `supplementary/introducing-system-one-models-and-jev.html`, `supplementary/introducing-system-one-models-and-jev.txt`, `supplementary/introduction.md`, `supplementary/limitations.md`, `supplementary/line-by-line-search.md`, `supplementary/llms.txt`, `supplementary/models.md`, `supplementary/re-ranking.md`, `supplementary/state.md`.

# Jev / System One：带概率的类型化决策模型

## 定位与结论

TypeSafe AI 创始人 Diogo Almeida 于 **2026-09-15** 发布 [Introducing System One Models & Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev)。Jev 是首个公开的 System One 模型，发布时处于 early access。核心接口是 **非结构化 state + 预定义 typed questions → 类型化答案及概率**；不生成自由文本，适合分类、路由、检索评分、验证和程序分支。这里按 blog / 产品技术资料收录，不作为已发表论文。

对 agent memory 的直接价值是低成本证据选择和相关性判断。已读材料没有给出持久记忆写入、更新、遗忘与跨会话管理的完整系统；不能把它等同于 Mem0 或 Hindsight。具体网络结构、参数规模、RLCD 训练目标和训练实现未在这些材料中充分披露，不能据此独立复现模型。

## 方法与接口（官方文档）

| Primitive | 问题 | 返回 | 可用位置 |
|---|---|---|---|
| Choice | 从给定选项选择 | choice、全选项 probabilities、confidence | 行号选择、路由、候选选择 |
| Score | 按有序标准评分 | score、各等级 probabilities、confidence | 多维质量判断 |
| Noul | 给定命题是否成立 | noul ∈ [0,1]，没有独立 confidence 字段 | 相关性、是否存在答案、独立筛选 |

一个请求共享 state，各问题并行且独立评估，再由代码组合结果。发布博客称其使用新架构、parallel sampler 和 **Reinforcement Learning for Calibrated Decisions (RLCD)**。这是官方方法描述，不是已审查的训练代码结论。复杂问题应拆成原子判断，数值运算与控制流留在代码中。

**confidence 不是额外的正确性判官。** 文档明确它由答案概率分布计算而来；页面交互示例的公式只是近似演示，不能当作服务端精确算法。分布集中不自动证明目标领域的经验校准，更不等于“confidence=0.9 就保证 90% 正确”。需要用自己的带标签样本检验校准与拒答阈值。

## 版本与使用边界（2026-09-22 抓取）

| 项目 | 官方当前说明 |
|---|---|
| 固定模型 ID | `jev-1.13.0`；`jev-latest`、`jev-preview` 当前均指向它 |
| API | `POST /v1/systemone` |
| 定价 | 输入 $0.042 / 百万 token；输出免费 |
| 上下文 | 请求总量 64k；state + 最长单个 question ≤32k |
| Choice 候选数 | 最多 255；超出需分层或分阶段 |
| 模态与语言 | 纯文本/JSON；英语最好，CJK 等准确率较弱 |
| 定制 | 官方称各账户共用权重，不提供客户数据 fine-tuning / LoRA |

限流与别名会变；实验应保存响应的版本 ID。两个检索 cookbook 的代码实际使用 **`jev-1.12`**，不能把其结果直接写成 1.13 的验证结果。

## 与检索最相关的两个实例

### 1. Line-by-line search：相对定位 + 绝对存在性

已阅读 cookbook 正文与核心搜索代码（历史文件已移除：`supplementary/line-by-line-search.md`）：GitHub Terms of Service 被分为 **218 行**，state 包含行号和文本；一个 Choice 对所有行 ID 输出分布，同时一个 Noul 判断文档是否包含答案。应用代码排序行号，再按 `exists` 决定回答或拒答。不是逐行发 218 次请求，也不是 embedding 索引。

这个拆分很关键：Choice 概率总和为 1，即使所有候选无关也会有第一名。官方仲裁问题示例中，第一行候选概率 **0.86**，而 `exists=0.14`，被判为文档不含答案。其演示阈值为 0.7 / 0.35，不是通用校准常数。四个示例展示可行性，不能支持大规模检索准确率结论。超过 255 行的官方建议是先选窗口再选窗口内行；前级漏选会限制后级召回。

### 2. BM25 + Noul reranking

已阅读 reranking cookbook 的方法、采样代码、评分与结果（历史文件已移除：`supplementary/re-ranking.md`）。从 CLERC 的 train 文件前 1,000 个满足条件的条目中随机选 170 条，汇总为 **3,565 passages**；排除池中前 20 条后抽取 40 queries。BM25 每个 query 取 30 候选，Jev 对每个 query–candidate 独立调用一次 Noul，以“是否为被引用的判例出处”评分，按值降序排列。

| 指标（官方示例，40 queries） | BM25 | + Jev rerank |
|---|---:|---:|
| Top-1 | 5% | 18% |
| Top-5 | 15% | 35% |
| Top-10 | 38% | 62% |

百分比沿用页面四舍五入展示。全部 **1,200 次调用**记录输入 1,536,002 token，总价 **$0.0645**。这不是单次查询成本。此切片 BM25 top-30 已包含全部 gold；reranker 只重排，无法找回 shortlist 外证据。它是小规模教程切片，不是完整 CLERC 测试集，也没有在这里与强 cross-encoder、dense/hybrid 检索做公平对照。

## 宣传结果及其证据边界

发布博客报告 System One shaped queries 约 **70–500ms**，并把首页 **193.6× 更快、444.6× 更便宜**归因于四个 workflow eval。官方承认这些倍率可能处于真实收益的高端，延迟主要从美国西海岸测量，短输入演示有利于 Jev。

Workflow eval 固定工作流，用 GPT-6 Astra 与 Fable 5.1 的平均预测概率作参考；衡量的是相对参考模型的一致性，不是独立人工真值的任务正确率。工作流由内部 capabilities 团队构建；LLM 对照经 System One adapter 输出兼容的概率决策，官方承认相比只输出决策会更慢、更贵。不得把这个倍率推广为所有聊天、代码或记忆任务的同等质量收益。评测站本次抓取失败，未独立核验其逐项数据；此段依据发布博客。

**“can't hallucinate / 0% type errors”须限定为输出空间与 schema 约束。** 模型仍可能选择错误的合法选项、把不存在的答案判为存在，或受对抗文本影响。结构合法性不能推出语义真实性。已读材料没有提供可供本次审查的内部模型实现或形式证明。

## 官方公开的失败模式

1.13 jaggedness（历史文件已移除：`supplementary/limitations.md`） 最近审阅日期为 2026-09-17：字面理解与隐含条件、计数和数值精度、日期排序/时间差、多跳间接推理、无关长 state、对抗内容、相互冲突的指令/criteria、跨问题结构不变量、自由文本生成均有局限。

特别值得保留：

- **增加并行问题**与**扩大 state**是两回事。文档称问题彼此隔离，但明确承认无关 state 会造成 context rot。
- 分别询问命题及其否定，不保证概率相加为 1；官方例子为 0.72 + 0.47 = 1.19。Noul 阈值不能直接搬到 Choice。
- state 中的注入指令可能影响结果；类型安全并不保证抗提示注入。
- 日期组件选择可以交给模型，日期合法性、大小比较和计数应由代码完成。

## 对现有研究的启发（本 wiki 判断，未经实验）

可以把 Jev 作为 [[research/agent-memory/threads/lazymem-related-work|LazyMem / BM25-window]] 后面的可选 reranker，或作为窗口内“证据在哪里 + 是否存在”的决策模块。与 [[research/agent-memory/assets/mem0-2025/note|Mem0]]、[[research/agent-memory/assets/hindsight-2025/note|Hindsight]] 比较时，应固定候选生成、上下文预算、回答模型和 judge，只替换检索评分部件，避免混合比较产品架构与底层模型。

建议评测：证据 Recall@k、缺证拒答、下游答案正确率、选择性风险/覆盖率、校准误差、端到端 p50/p95 延迟与总成本；纳入 BM25 原排序、成熟 reranker 和相同候选上的 LLM 判断对照。单独覆盖中文、长历史干扰、时序冲突与多跳问题。这里是后续实验建议，没有运行 API 或复现实验。

## 阅读与归档

- 发布博客原文 HTML（历史文件已移除：`supplementary/introducing-system-one-models-and-jev.html`） / 抽取正文（历史文件已移除：`supplementary/introducing-system-one-models-and-jev.txt`）：阅读全文；折叠 FAQ 仅抓到标题，不声称已读隐藏答案。图片/视频未独立核验。
- Introduction（历史文件已移除：`supplementary/introduction.md`）、Models（历史文件已移除：`supplementary/models.md`）、State（历史文件已移除：`supplementary/state.md`）、Confidence（历史文件已移除：`supplementary/confidence.md`）、limitations（历史文件已移除：`supplementary/limitations.md`）：阅读正文及相关接口示例。
- Line-by-line search（历史文件已移除：`supplementary/line-by-line-search.md`）：正文、核心搜索/阈值代码与示例输出；未分析 playground 编码 payload。
- Re-ranking（历史文件已移除：`supplementary/re-ranking.md`）：正文、数据选择、BM25、逐对打分代码与页面记录结果；未执行 notebook。
- 文档目录快照（历史文件已移除：`supplementary/llms.txt`）用于来源发现，不代表所有链接均已阅读。
- [citation.bib](citation.bib)记录来源、抓取日期、字节数、SHA-256 和失败状态。本条目为 blog/docs，未归档论文 PDF/TeX，未缓存或审查官方 adapter 仓库，未调用付费 API。

## 相关工作补充（2026-09-22）

[[research/agent-memory/threads/jev-related-work|LOTUS、UtilityQwen、SCARLet、OptiSet 通俗对照]]：区分通用决策模型、语义数据处理系统、效用选择器、检索器训练及集合选择。相同应用方向已有工作，不等于 Jev 与这些系统是同一种东西。

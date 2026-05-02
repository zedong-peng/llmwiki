# Meta-Harness: End-to-End Optimization of Model Harnesses

**arXiv**: 2603.28052
**Venue**: COLM 2026
**Authors**: Yoonho Lee, Roshen Nair, Qizheng Zhang (Stanford), Kangwook Lee (KRAFTON), Omar Khattab (MIT), Chelsea Finn (Stanford)
**Project page**: https://yoonholee.com/meta-harness/

---

## 核心问题

LLM 系统的性能不仅取决于模型权重，还取决于 **harness**（外围代码）：决定模型看什么、存什么、取什么的代码。
同一 benchmark 上，不同 harness 可造成 **6× 性能差距**（引用 SWE-Bench-MC）。
但 harness 工程目前主要靠人工设计。本文问：能否自动化这个过程？

---

## 方法：Meta-Harness

### 总体思路

一个"优化 harness 的 harness"——一个外层循环，使用 **coding agent proposer** 搜索 harness 代码空间。

**核心设计**：proposer 通过 **filesystem** 访问所有历史候选的完整信息（源代码 + 执行 trace + 分数），而不是压缩后的摘要或标量奖励。

### 搜索循环（Algorithm 1）
1. 初始化种群 $\mathcal{H}$（手工设计的基线 harness）
2. 每轮：proposer 查询 filesystem → 提出 $k$ 个新 harness → 评估 → 写入 filesystem
3. 最终返回 Pareto 前沿上的 harness

**Proposer**：Claude Code + `Opus-4.6`（with max reasoning）
每轮读取中位数 **82 个文件**（69-99 范围），约 41% 是源代码、40% 是执行 trace。

### 与现有文本优化器的区别

| 方法 | 反馈形式 | tokens/step |
|------|---------|-------------|
| OpenEvolve / AlphaEvolve | 标量分数 + 程序数据库 | 4K–22K |
| GEPA | 单候选 rollout trace | 2K–8K |
| Meta-Harness | 全历史 filesystem（可选择性访问） | 最多 10M tokens 诊断信息 |

---

## Search Set 与 Test Set 的分离情况

### 文本分类任务 ✅ 完全分离
- **Search set**：LawBench / S2D / USPTO-50k 的子集，用于候选 harness 评估
- **Test set**：同三个数据集的 held-out 集合
- 论文明确："we hold out the test sets until the final evaluation"
- 候选选择"solely based on search-set performance"
- 还额外测了 9 个 OOD 数据集（完全 unseen）

### 数学推理任务 ✅ 完全分离
- **Search set**：250 个奥林匹克级数学题（OlympiadBench + Omni-MATH hard），用 GPT-OSS-20B 评估候选
- **Test set**：200 个 IMO 级题目（IMO-AnswerBench、IMO-ProofBench、ArXivMath）——**proposer 从未见过**
- 还在 4 个**搜索时未见过的模型**上测试同一 harness（GPT-5.4-nano/mini, Gemini-3.1-Flash-Lite, Gemini-3-Flash）
- 语料库去重去污：用精确前缀匹配 + 模糊 Jaccard 相似度（阈值 0.8）去掉与评估集重叠的问题

### TerminalBench-2 ❌ 未分离——搜索集 = 测试集
- "we perform search and final evaluation on the same 89-task benchmark"
- 作者将其定位为 **discovery problem**，并援引先前工作中已有的同类做法（Terminus-KIRA、ForgeCode 等也都是直接在 benchmark 上迭代的）
- 理由：benchmark 规模小且昂贵，引入 split 会严重削弱搜索信号
- 通过人工检查 + regex 审计排查是否有 task-specific string 泄漏到 evolved harness

---

## 实验结果

### 文本分类
- **vs ACE（最强手工 harness）**：+7.7 pts，且仅用 1/4 的上下文 tokens（11.4K vs 50.8K）
- **vs 文本优化器**：4 次评估就追平 OpenEvolve/TTT-Discover 的最终性能，最终高出 >10 pts
- OOD 数据集（9 个）：平均 73.1%，优于 ACE（70.2%）

### 数学推理
- 在 200 个 IMO 级问题上，5 个模型平均提升 **+4.7 pts**（相比无检索基线）
- 优于 BM25 检索基线（+1.3 pts）；避免了密集检索和随机 few-shot 在部分模型上的性能下降

### TerminalBench-2
- Haiku 4.5：**37.6%**，全榜 #1（vs 次优 Goose 35.5%）
- Opus 4.6：**76.4%**，全榜 #2（vs Terminus-KIRA 74.7%；ForgeCode 81.8% 但无法从公开代码复现）

---

## 消融实验（文本分类）

| 接口 | 中位准确率 | 最优准确率 |
|------|-----------|-----------|
| 仅分数（scores-only） | 34.6 | 41.3 |
| 分数 + LLM 摘要 | 34.9 | 38.7 |
| **Meta-Harness（完整 traces）** | **50.0** | **56.7** |

结论：**完整 execution traces 是最关键的组件**；LLM 摘要不仅无法弥补差距，甚至可能因压缩掉诊断信息而更差。

---

## 发现的 Harness 示例

### 文本分类：两端点
1. **Draft Verification**（低上下文）：两次调用 — 先检索 top-5 相似样本做草稿预测，再按草稿标签检索 confirmer + challenger，决定是否修改预测
2. **Label-Primed Query**（最高精度）：一次大调用 — label primer（全标签列表）+ 每类代表样本（覆盖块）+ 同邻域不同标签的对比对（对比块）

### 数学：四路 BM25 路由器
- 词法路由：识别组合数学 / 几何 / 数论 / 其他（代数）
- 每路有定制的 BM25 参数、去重阈值、重排序策略

### TerminalBench-2：环境引导（Environment Bootstrap）
- 在 agent loop 开始**之前**，运行 compound shell 命令获取环境快照（OS、语言版本、包管理器、/app 内容）并注入初始 prompt
- 消除了 2-4 轮探索性调用；对"环境非显而易见"的任务帮助最大

---

## Proposer 的因果推理行为（TerminalBench-2 案例）

- 迭代 1-2：结构性 bugfix + prompt 改写，两者都 regress
- 迭代 3：proposer **识别混淆因素** — regression 根因是 prompt 修改，而非结构 fix
- 迭代 4-6：直接修复完成逻辑的 bug，仍然 regress；学到了"prompt/完成流改动高风险"
- 迭代 7：**转换策略** — 纯加法修改（加环境快照），不动完成流，取得最佳结果
- 迭代 10：跨 run 迁移知识（引用另一次搜索 run 的发现）

---

## 关键设计原则

1. **外层循环极简**：不硬编码搜索启发式，把诊断和提案都委托给 coding agent
2. **Filesystem 访问 >> 压缩摘要**：proposer 决定看什么，而不是系统决定给什么
3. **代码空间的可检查性**：过拟合（if-chain、硬编码映射）可在代码中直接看到，不像权重空间
4. **自动受益于更强的 coding agent**：搜索质量随 proposer 能力提升而提升

---

## 实现细节

- Proposer：Claude Code + `Opus-4.6`（max reasoning）
- Base model 视任务而定，固定不动
- 典型 run：约 60 个候选 harness，20 轮迭代
- 每个候选 harness：单文件 Python 程序，100-1000 行
- 技巧：写好 skill 文本 > 调 iteration count；search set 要足够"难"（对基线有挑战）；全量日志 + 可查询 CLI

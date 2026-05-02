# ARM Proposal vs. Awesome-RL-Agentic-Search: Overlap Analysis

**Date:** 2026-04-30（更新：精读两篇高危论文后）
**Source repo:** https://github.com/ventr1c/Awesome-RL-based-Agentic-Search-Papers
**Proposal:** Active Retrieval as Memory (ARM) — `/Users/pengzedong/Documents/GitHub/Active-Retrieval-as-Memory/README.md`

---

## ARM 的核心主张（一句话总结）

> 用 RL 训练一个能够主动、迭代地调用 `grep`/`read`/`find` 等符号检索工具的 Agent，将海量外部语料作为持久外部状态而非压缩进上下文，以 O(1)~O(k) 的 LLM 前向开销实现无损、精准的长上下文推理。

三个关键区分点：
1. **符号检索**（regex/exact match）而非向量语义检索
2. **lossless**：外部状态永不被压缩，只有命中片段送入 LLM
3. **Variable-Horizon MDP + V-GRPO**：轨迹长度完全动态，专门处理 credit assignment

---

## 重叠风险评估

### 🔴 高度重叠（核心思路几乎一致）

| 论文 | 重叠点 | 差异 |
|---|---|---|
| **Search-R1** (arXiv:2503.09516, COLM 2025) | 用 GRPO 训练 LLM 在推理中调用真实搜索引擎；多轮 tool-use trajectory；结果 interleave 进推理链 | 搜索引擎是向量/BM25 web search，不是 grep/symbolic；无 variable-horizon 概念；无 lossless 区分 |
| **R1-Searcher** (arXiv:2503.05592) | RL incentivize LLM search capability；multi-turn rollout；GRPO reward | 同上，web/dense retrieval，非 symbolic；无 O(1) LLM complexity 论述 |
| **ReSearch** (arXiv:2503.19470, NeurIPS 2025) | Reasoning + Search 交织；RL with multi-turn search trajectory | 同样是 web 检索；horizon 是固定的（固定搜索次数上限） |
| **StepSearch** (arXiv:2505.15107, EMNLP 2025) | Step-wise PPO；每一步检索单独计 reward | 强调 step-level reward，与 ARM V-GRPO 的 per-step advantage 直接重叠；但仍是 web search |
| **IGPO** (arXiv:2510.14967, ICLR 2026) | Information Gain 作为 step-level reward | 表面相似，实际技术完全不同——见下方精读分析 ⚠️ |
| **IG-Search** (arXiv:2604.15148) | Step-level information gain rewards for search-augmented reasoning | 同 IGPO 路线，2026.4 新出 ⚠️ |
| **MemSearcher** (arXiv:2511.02805) | 将 memory management 和 search 一起用 RL 训练；end-to-end | 接近 ARM 将记忆定义为"检索策略"；但用的是总结式记忆而非 external lossless state |
| **AutoSearch** (arXiv:2604.17337) | Adaptive search depth via RL；自适应决定何时停止搜索 | variable-horizon 的工程实现；但非 symbolic retrieval |
| **CriticSearch** (arXiv:2511.12159) | Fine-grained credit assignment for search agents | 解决同一问题（credit assignment），但方案完全不同——见下方精读分析 ⚠️ |

---

### 🟡 部分重叠（共享某一个子问题）

| 论文 | 重叠子问题 | ARM 的差异 |
|---|---|---|
| **DeepRetrieval** (arXiv:2503.00223, COLM 2025) | RL 优化查询生成，"hack"检索器 | ARM 的 search 动作是 symbolic regex，不是优化 query embedding |
| **BAPO** (arXiv:2601.11037) | "何时停止搜索"的决策边界 | ARM variable-horizon 直接涵盖此问题，但角度是 MDP 而非 boundary detection |
| **Agent-Omit** (arXiv:2602.04284) | 自适应省略 thought/observation，降低 token cost | 与 ARM 的 O(1) LLM complexity 目标一致，手段不同 |
| **ReSum** (arXiv:2509.13313) | Context summarization for long-horizon search | ARM 用 external lossless storage 替代 summarization，直接对立 |
| **SIGHT** (arXiv:2602.11551) | Self-evidence + information-gain diverse branching | 类似 ARM 的 intrinsic reward 动机，但应用在 web search branching |
| **Search-P1** (arXiv:2602.22576) | Path-centric reward shaping for stable agentic RAG | path/trajectory-level reward，和 V-GRPO 的设计动机一致 |
| **AgentGym-RL** (arXiv:2509.08755) | Multi-turn RL for long-horizon decision making | 与 ARM 的 variable-horizon MDP 共享框架设计问题 |
| **DeepDive** (arXiv:2509.10446) | KG + multi-turn RL for search | structured/symbolic navigation 方向有部分重叠 |

---

### 🟢 无实质重叠（不同赛道）

- **Multi-agent 系列**（PRISMA, WideSeek-R1, M-ASK）：协同架构，非单 agent symbolic 检索
- **Multimodal 系列**（VSearcher, MMSearch-R1 等）：视觉模态
- **Web Browsing 系列**（WebSailor, WebThinker）：网页导航，非本地语料库
- **Query reformulation 系列**（SmartSearch, ConvSearch-R1）：改写查询，非工具调用
- **KG navigation**（GRAIL, DynaSearcher）：图结构，非代码库/文档
- **Benchmark 系列**：纯评测，无算法贡献

---

## 精读分析：两篇高危论文的真实技术细节

### IGPO (arXiv:2510.14967, ICLR 2026)

**IG 的真实定义（非直觉描述，是原文实现）：**

$$\text{IG}_t = \log P_\theta(\text{answer} \mid \text{context}_{t}) - \log P_\theta(\text{answer} \mid \text{context}_{t-1})$$

即：每一轮检索后，模型输出 **ground-truth answer tokens** 的 token-level 对数概率提升了多少。这是一个有监督的、锚定在已知正确答案上的概率差分，用向量化 attention mask 在一次前向传播中同时计算所有轮次。

**三个关键限制（ARM 的攻击点）：**

1. **必须有 ground-truth answer 才能计算**：每步都要把 correct answer tokens 喂入模型。code generation / open-ended task 无法直接用，且无法处理"empty grep result 也是有价值信号"的场景——因为 null result 不改变 GT 概率
2. **Action space 是自然语言 web query**：IG 测的是语义层 belief 变化，和 symbolic oracle 的精确匹配语义完全不同
3. **Fixed max 10 turns**：没有任何 variable-horizon 的设计；advantage collapse 问题依然存在于 horizon 的尾端

**与 ARM Intrinsic Reward 的本质区别：**

- IGPO IG = "LM posterior probability gain for ground truth"（需要 GT，soft belief）
- ARM intrinsic reward = "symbolic oracle 返回的外部状态变化量"（不需要 GT，hard state change，null result 也是正信号）

表面都叫"信息增益"，但 IGPO 的信号来自 LM 内部对答案的置信度，ARM 的信号来自外部离散状态空间的结构变化。

---

### CriticSearch (arXiv:2511.12159)

**Credit assignment 的解法（原文实现）：**

引入第二个**冻结的 LLM** 作为 retrospective critic。Critic 看到完整信息：(question, full_trajectory, ground_truth) → 对每个 search action 输出 binary "Good"/"Bad"。

最终 advantage 是混合的：
$$A_{\text{hybrid}} = \alpha \cdot A^{\text{turn}} + (1-\alpha) \cdot A^{\tau}$$

其中 $A^{\text{turn}}$ 是 critic 的 binary 分数（normalized），$A^\tau$ 是全局 GRPO advantage。

**四个关键限制（ARM 的攻击点）：**

1. **Fixed 4 turns hard limit**：完全没有 variable-horizon 设计，无法处理"不知道需要几步才能找到答案"的场景
2. **需要额外的 frozen LLM**：训练时需要两个模型并行推理，计算和内存开销翻倍
3. **Binary reward 粒度低**：只能说 Good/Bad，无法量化"这一步贡献了多少"（而 V-GRPO 用的是轨迹组内连续归一化）
4. **同样是 web search / NLP QA 场景**：action = 生成自然语言 query；symbolic retrieval 场景完全未考虑

**与 V-GRPO 的本质区别：**

| 维度 | CriticSearch | V-GRPO (ARM) |
|---|---|---|
| Horizon | Fixed 4 turns | Variable（无上限，自主 Terminate） |
| Credit assignment 机制 | 外挂冻结 LLM 评委（binary） | 轨迹组内连续 advantage 归一化 |
| 额外开销 | 需要第二个 LLM | 无额外模型 |
| Reward 粒度 | Binary (Good/Bad) | 连续（reward - step cost） |
| Null result 处理 | 不考虑 | 核心场景（dead-end pruning） |

CriticSearch 是"外挂评委"方案，V-GRPO 是"组内相对评价"方案，两者解决同一问题但路径完全不同，且 V-GRPO 在 variable-horizon 场景下更自然。

---

## ARM 独有的贡献（无对应论文）

1. **Symbolic retrieval（grep/find/regex）作为 action space**：列表中近 200 篇全是 dense retrieval 或 web search，无一用 exact-match / regex 作为 tool
2. **Null result 作为正向信号（Dead-end Pruning）**：IGPO 无法处理（需要 GT 才能计算 IG），CriticSearch 未考虑，这是 ARM intrinsic reward 独有的贡献
3. **External lossless state 的 O(1) LLM complexity 论证**：明确的复杂度对比分析（vs. MemAgent 的 O(N)），现有工作无此框架
4. **Variable-horizon MDP 的 formal 定义 + V-GRPO**：虽然 variable-horizon 隐含在许多论文中，但没有人 formal 化并专门为此设计 RL 算法
5. **`Environment Protocol` 抽象**（search / read_context / submit 三原语）：统一代码库、文档、日志的检索接口，没有对应工作

---

## 审稿人质疑与回应 Cheat Sheet

### Q1："ARM 的 intrinsic reward 和 IGPO (ICLR 2026) 的 Information Gain 有什么区别？"

**回应：**
> IGPO 的 IG 定义为 `log P(GT_answer | context_t) - log P(GT_answer | context_{t-1})`，是一个**有监督的、以 ground-truth answer 为锚点的 LM 内部置信度变化**。它要求每一步都已知正确答案，因此（1）无法处理 code generation 等 open-ended 任务，（2）对于 empty grep result，由于不改变 LM 对 GT 的置信度，IGPO 会将其标记为无价值步骤。
>
> ARM 的 intrinsic reward 来自**符号 oracle 的外部状态变化量**（结果集的 set difference / entropy），完全不依赖 ground-truth。在代码搜索场景中，`grep "undefined_var" .` 返回空集本身就是一个强信号（证伪了"变量定义在这里"的假设），ARM 会给予正向奖励，而 IGPO 无法表达此语义。两者名字都叫"信息增益"，但信号来源（LM 内部 soft belief vs 外部 symbolic oracle）和适用场景完全不同。

---

### Q2："CriticSearch 已经解决了 credit assignment 问题，V-GRPO 有什么额外贡献？"

**回应：**
> CriticSearch 的 credit assignment 方案有三个根本局限：(1) **fixed 4-turn horizon**，无法处理 ARM 的核心场景（trajectory 长度未知，agent 自主决定终止）；(2) **需要额外的冻结 LLM 作为评委**，训练成本翻倍；(3) **binary reward 粒度（Good/Bad）**，丢失了步骤间的相对贡献信息。
>
> V-GRPO 在同一训练批次的 G 条轨迹内做连续 advantage 归一化，天然适配 variable-horizon：短轨迹和长轨迹共享同一 advantage 空间，不需要任何截断或 padding。V-GRPO 和 CriticSearch 是两种解决思路，前者在 ARM 的 symbolic + variable-horizon 场景下更简洁、更 principled。

---

### Q3："以 Agent Memory 而非 Agentic Search 定位，创新点是否够强？"

**回应：**
> 见下节"定位分析"。

---

### Q4："Symbolic retrieval 的局限：无法处理语义查询怎么办？"

**回应：**
> ARM 针对的是**精确性敏感**的场景（代码库、结构化文档、日志），这些场景中语义模糊性低、exact match 就是正确的检索方式。对于需要语义检索的场景（如开放域 QA），ARM 不是最优解，现有 dense retrieval 方法已经足够。这是 ARM 的**适用域边界**，而非弱点——我们的 claim 是在 lossless precision 比 semantic recall 更重要的任务上，symbolic retrieval + RL 的组合优于 dense RAG。

---

## 定位分析：Agent Memory vs. Agentic Search

### 如果定位为"Agentic Search"——贡献偏弱

**理由：** 面对 200+ 篇 RL-based agentic search 论文，ARM 的差异化主要在 symbolic retrieval，这对 web search 或 NLP QA benchmarks 无效，对比实验很难做，审稿人会质疑适用性。

### 如果定位为"Agent Memory"——贡献更强

**理由：** ARM 真正挑战的是 MemAgent/MemGPT 范式——这个赛道竞争少得多，且 ARM 的三大核心（symbolic retrieval / lossless / variable-horizon MDP）在此赛道中无对手。

**强写法（可直接用于 abstract/intro）：**
> "We challenge the dominant paradigm of agent memory as *lossy compression*. Rather than summarizing the environment into a fixed-length internal state, ARM redefines memory as a **learned retrieval policy**: an RL-trained agent that actively and iteratively probes a persistent external state via symbolic tools (grep/find/read). This yields O(k) LLM inference cost with 100% information fidelity—theoretically impossible under any compression-based memory scheme."

**最强 venue 建议：** ICLR / NeurIPS 的 agent/memory track，而非 IR/retrieval 类会议。这样 reviewers 对比的是 MemGPT/MemAgent，而不是 Search-R1/IGPO，ARM 的优势会非常清晰。

**可用的 baseline 对比矩阵：**
- vs. Context Scaling（RingAttention）：O(N²) vs O(k)，lossless vs lossless
- vs. Parametric Memory（MemAgent）：O(N) vs O(k)，**lossy vs lossless** ← 核心论点
- vs. Dense RAG（Search-R1）：semantic recall vs exact match，approximate vs symbolic oracle

---

## 建议

- **核心贡献要突出"symbolic/exact-match retrieval + lossless"**，这是最清晰的差异化壁垒
- **Intrinsic reward 不再是高危点**：精读后确认 IGPO/IG-Search 和 ARM 在技术层面完全不同，可以正面 cite 并 compare
- **V-GRPO 和 CriticSearch 的对比要清晰**：强调 variable-horizon + 无额外模型
- **以 Agent Memory 而非 Agentic Search 定位**：投稿方向选 agent memory / long-context reasoning track
- **MemSearcher 和 ARM 是互补关系**，用 MemSearcher 作为"lossy memory baseline"来对比
- 数据集优先考虑 **SWE-bench**（代码库 grep 场景），避免 HotpotQA（已被 web search 论文大量占据）

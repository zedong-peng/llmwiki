# MemRL: Self-Evolving Agents via Runtime Reinforcement Learning on Episodic Memory

**arXiv:** [2601.03192](https://arxiv.org/abs/2601.03192)
**Venue:** ICML 2026 (preprint)
**Code:** https://github.com/MemTensor/MemRL

---

## 一句话总结

MemRL 把 episodic memory 的检索策略形式化为 MDP，用非参数 RL（Q-value 更新）替代语义相似度来决定检索哪条记忆，让 backbone LLM 在 **权重完全冻结** 的情况下通过运行时反馈持续自我进化。

---

## 问题与动机

现有两条路线各有致命缺陷：

| 路线 | 问题 |
|---|---|
| Fine-tuning（SFT/RLHF）| 计算贵、catastrophic forgetting |
| RAG / 记忆系统（Reflexion、MemGPT 等）| 检索只看语义相似度，"similar ≠ useful"；没有机制评估记忆的实际效用 |

核心洞察：语义上相似的经验可能包含脆弱的 API 调用习惯或失败策略，直接注入 context 反而有害。需要一个能区分"高价值经验"和"相似噪声"的机制。

---

## 方法

### 形式化：Memory-Augmented MDP (M-MDP)

把 LLM agent 与外部记忆的交互建模为 $(\mathcal{S}, \mathcal{A}, P, \mathcal{R}, \gamma, \mathcal{M})$：

$$\pi(a_t | s_t, \mathcal{M}_t) = \sum_{m \in \mathcal{M}_t} \underbrace{\mu(m | s_t, \mathcal{M}_t)}_{\text{检索策略}} \cdot \underbrace{p_{LLM}(a_t | s_t, m)}_{\text{推理策略（冻结）}}$$

**目标**：不优化 $p_{LLM}$ 的参数，而是优化检索策略 $\mu$。

### Intent-Experience-Utility 三元组

每条记忆存为 $(z_i, e_i, Q_i)$：
- $z_i$：Intent 嵌入（当前 query 的向量）
- $e_i$：Experience（过去的解法轨迹或反思）
- $Q_i$：Utility（该经验在相似 intent 下的期望收益，即 Q-value）

### Two-Phase Retrieval

**Phase A（语义召回）**：cosine 相似度 + 阈值 $\delta$ 筛出候选池 $\mathcal{C}(s)$；若 $\mathcal{C}(s) = \emptyset$ 则不注入任何记忆（纯 LLM 探索）。

**Phase B（价值感知选择）**：从候选池中按组合分数取 top-$k_2$：

$$\text{score}(s, z_i, e_i) = (1-\lambda)\cdot\hat{\text{sim}} + \lambda\cdot\hat{Q_i}$$

其中 $\hat{\cdot}$ 为 z-score 归一化，$\lambda$ 控制探索/利用权衡。

### Non-Parametric RL 更新

每次执行后获得环境反馈 $r$，用 Monte Carlo 风格更新 Q-value：

$$Q_{\text{new}} \leftarrow Q_{\text{old}} + \alpha(r - Q_{\text{old}})$$

同时用 LLM 对轨迹做摘要，写入新三元组 $(z, e_{\text{new}}, Q_{\text{init}})$，持续扩充记忆库。

**关键**：所有学习发生在记忆空间，LLM 参数始终冻结。

### 理论保证

- Q-value 更新无偏且方差有界：$\lim_{t\to\infty}\mathbb{E}[Q_t] = \beta(s,m)$，$\limsup \text{Var}(Q_t) \le \frac{\alpha}{2-\alpha}\text{Var}(r_t|s,m)$
- 将系统建模为 Generalized EM：检索排序 = E-step（策略改进），Q-value 更新 = M-step（价值更新）；单调改进定理保证收敛到稳定点，防止 catastrophic forgetting

---

## 实验

**Backbones**：各 benchmark 选不同模型（GPT-4o / GPT-4o-mini / GPT-5-mini / Gemini-3-pro），避免无信号或天花板问题。

**4 个 benchmark**：

| Benchmark | 任务类型 | MemRL SR / CSR | 最强 baseline SR / CSR |
|---|---|---|---|
| BigCodeBench | 代码生成 | **0.595 / 0.627** | MemP: 0.578 / 0.602 |
| Lifelong Agent (OS) | 系统操作 | **0.788 / 0.804** | MemP: 0.736 / 0.742 |
| Lifelong Agent (DB) | 数据库 | **0.960 / 0.972** | MemP: 0.960 / 0.966 |
| ALFWorld | 具身导航 | **0.949 / 0.981** | Self-RAG: 0.907 / 0.962 |
| HLE | 多学科推理 | **0.570 / 0.606** | MemP: 0.522 / 0.570 |

**Runtime Learning 平均**：MemRL 0.772/0.798 vs. MemP 0.736/0.760 vs. RAG 0.679/0.699。

**Baselines**：RAG、Self-RAG、Mem0、MemP（程序记忆）、Pass@k。

---

## 与 EvoMaster / inference-time scaling 的关系

| 维度 | EvoMaster | MemRL |
|---|---|---|
| 学习发生在哪 | prompt + 多次 API 调用结构 | memory Q-value（外部状态） |
| 跨任务累积 | wisdom.json（启发式） | Q-value 有理论收敛保证 |
| 训练 | 无 | 无（非参数 RL） |
| "evolution" 的形式 | inference-time 迭代 × 角色分离 | runtime 记忆效用学习 |

MemRL 可视为"带 RL 理论基础的外部记忆 evolution"，EvoMaster 是"结构化 inference-time scaling"——两者都是 frozen LLM + 外部机制的路线，但 MemRL 更侧重**跨 session 的持续自进化**，EvoMaster 更侧重**单任务内的多轮精化**。

---

## 局限

- 理论分析依赖"stationary task distribution"假设，现实中任务分布可能漂移
- Q-value 更新依赖环境 reward 信号，reward 稀疏或噪声大时收敛慢
- 各 benchmark 用了不同 backbone，跨任务对比不完全公平
- HLE 上的 Gemini-3-pro 未必是最优选择，基线偏低

---

## 关键引用

- M-MDP 框架：zhou2025memento
- Reflexion：shinn2023reflexion
- MemGPT：packer2024memgptllmsoperatingsystems
- MemP：fang2025memp
- BigCodeBench：zhuo2025bigcode
- ALFWorld：shridhar2021alfworld
- Lifelong Agent Bench：zheng2025lifelong
- HLE：phan2025hle
- Era of Experience：silver2025era_of_experience

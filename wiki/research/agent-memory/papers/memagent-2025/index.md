# MemAgent: Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent

**Authors**: Hongli Yu, Tinghong Chen, Jiangtao Feng, Jiangjie Chen, Weinan Dai, Qiying Yu, Ya-Qin Zhang, Wei-Ying Ma, Jingjing Liu, Mingxuan Wang, Hao Zhou

**Affiliation**: ByteDance Seed, Tsinghua AIR, SIA-Lab

**arXiv**: [2507.02259](https://arxiv.org/abs/2507.02259)

**Code**: [github.com/BytedTsinghua-SIA/MemAgent](https://github.com/BytedTsinghua-SIA/MemAgent)

**Project Page**: [memagent-sialab.github.io](https://memagent-sialab.github.io/)

## 核心思想

MemAgent 通过 **固定长度的动态更新记忆机制** 和 **强化学习**，使 LLM 能够处理任意长度的文本，同时保持线性时间复杂度和近乎无损的性能外推。

关键洞察：模仿人类处理长文本的方式——不是记住每个细节，而是选择性地记录关键信息，丢弃冗余内容。

## 方法

### 工作流程

1. **分块流式处理**: 将长文档视为受控的证据流，分成多个 chunk 逐个处理
2. **固定长度记忆**: 每步只看两样东西：
   - 下一个文本块
   - 固定长度的记忆（总结之前所有重要信息）
3. **覆写策略**: 读取新 chunk 后，用更新的记忆覆写之前的记忆
4. **两阶段推理**:
   - **Context-Processing 模块**: 迭代处理 chunks，更新记忆
   - **Answer-Generation 模块**: 基于问题和记忆生成最终答案

### 复杂度分析

- **时间复杂度**: $O(N)$ 线性复杂度（N 为文档长度）
- **空间复杂度**: $O(C + M)$ 常数空间（C 为 chunk 大小，M 为记忆大小）
- 记忆长度固定，每个 chunk 的计算量恒定

### Multi-Conv DAPO 训练算法

MemAgent 扩展了 DAPO (Direct Advantage Policy Optimization) 算法来处理多轮独立上下文对话：

1. **多对话生成**: 每个样本生成多个独立上下文的对话（context-processing 轮次）
2. **奖励分配**: 使用最终答案计算奖励，分配给所有相关对话
3. **优势计算**:
   $$\hat{A}_{i,j,t} = r_i - \text{mean}(\{R_i\}_{i=1}^G)$$
4. **损失函数**: 扩展到 `(group, conversation, token)` 三维结构

### 从自回归建模角度理解

标准 LLM: $p(\mathbf{x}_{1:N})=\prod_{n=1}^N p(x_n\mid\mathbf{x}_{1:n-1})$

MemAgent 引入固定长度记忆 $\mathbf{m}$，分解为：
$$p(\mathbf{x}_{1:N}) = \sum_{\mathbf{m}^{1:K-1}} \prod_{k=1}^{K} \underbrace{p(\mathbf{c}^k\mid\mathbf{m}^{k-1})}_{\text{read}} \underbrace{p(\mathbf{m}^k\mid\mathbf{c}^k,\mathbf{m}^{k-1})}_{\text{write}}$$

- **Read**: 读取 chunk，条件于当前记忆
- **Write**: 更新记忆，条件于 chunk 和旧记忆

## 实验结果

### 训练设置

- **基础模型**: Qwen2.5-7B-Instruct, Qwen2.5-14B-Instruct
- **上下文窗口**: 训练时限制为 8K
  - 1024 tokens: query
  - 5000 tokens: context chunk
  - 1024 tokens: memory
  - 1024 tokens: output
- **训练数据**: HotpotQA，32K 样本，文档长度约 28K tokens

### 主要结果

在 RULER-HotpotQA 上的表现（准确率 %）：

| 模型 | 7K | 14K | 28K | 112K | 448K | 896K | 1.75M | 3.5M |
|------|-----|-----|-----|------|------|------|-------|------|
| Qwen2.5-14B-1M | 60.2 | 60.9 | 50.0 | 50.0 | 8.6 | 0.0 | N/A | N/A |
| QwenLong-L1-32B | 72.7 | 75.0 | 72.7 | 31.3 | 13.3 | 11.7 | N/A | N/A |
| DS-Distill-Qwen-14B | 64.1 | 64.8 | 57.0 | 14.8 | 3.1 | 6.3 | N/A | N/A |
| **RL-MemAgent-14B** | **83.6** | **82.0** | **84.4** | **76.6** | **75.0** | **77.3** | **76.6** | **78.1** |
| **RL-MemAgent-7B** | 82.0 | 79.7 | 78.9 | **79.7** | 74.2 | 76.6 | 75.8 | 71.1 |

### 关键发现

1. **近乎无损外推**: 从 8K 训练窗口外推到 3.5M tokens，性能下降 < 5%
2. **线性复杂度**: 处理时间和内存消耗随输入长度线性增长
3. **超越大模型**: 7B MemAgent 超越 32B 基线模型
4. **泛化能力强**: 在 RULER 的 10 个 OOD 任务上平均准确率 > 95%（8K-512K）

### 消融实验

- **无 RL 训练**: 配备记忆机制但未经 RL 训练的模型，性能随长度增加而下降
- **RL 的必要性**: RL 训练对于教会模型如何正确利用记忆至关重要
- 记忆机制提供结构支持，RL 提供优化策略

## 技术优势

### 三大核心优势

1. **无限长度**: 文档可达百万 tokens，因为采用流式处理
2. **无性能悬崖**: RL 鼓励记忆保留所需信息，实现近乎无损外推
3. **线性成本**: 固定窗口大小意味着解码时间和内存消耗线性增长 $O(N)$

### 与其他方法对比

- **vs 长度外推**: 避免 $O(n^2)$ 复杂度和性能退化
- **vs 稀疏/线性注意力**: 无需从头训练，保持标准 Transformer 架构
- **vs 上下文压缩**: 记忆在 token 空间，人类可读可编辑；不需要额外模块

## 实现细节

### 记忆更新提示模板

**Context-Processing**:
```
Question: {question}
Memory: {previous_memory}
New Context: {current_chunk}
Update the memory with relevant information.
```

**Answer-Generation**:
```
Question: {question}
Memory: {final_memory}
Generate the final answer.
```

### 奖励建模

- **单答案任务**: $R(\hat{y}, Y) = \max_{y \in Y} \mathbb{I}(\texttt{is\_equiv}(y,\hat{y}))$
- **多答案任务**: $R(\hat{y}, Y) = \frac{|\{y \in Y \mid \mathbb{I}(y \in \hat{y})\}|}{|Y|}$

## RL 训练详解（给 RL 小白）

### RL 基础概念

#### 什么是强化学习（RL）？

**传统监督学习**：
```
输入 → 模型 → 输出
      ↓
   对比标准答案
      ↓
   计算损失，更新权重
```

**强化学习**：
```
状态 → 智能体做决策 → 行动 → 环境反馈
                              ↓
                          奖励信号
                              ↓
                      根据奖励更新策略
```

**类比：学习做笔记**

- **监督学习**（有标准答案）：
  - 老师给你文章和标准笔记
  - 你模仿标准笔记
  - 老师说"这里应该记这个，那里应该记那个"

- **强化学习**（只有最终反馈）：
  - 老师给你文章和问题
  - 你自己决定记什么、怎么记
  - 最后根据能否答对问题给你打分
  - 你自己琢磨：哪些笔记有用，哪些没用

### MemAgent 的 RL 训练内容

#### 训练的是什么？

MemAgent 的 RL 训练的是**记忆管理策略**，具体包括：

**1. 什么信息该记住**
```python
chunk = "Arthur's Magazine was founded in 1844 in Philadelphia..."
question = "Which magazine was started first?"

# 模型学会：
memory = "Arthur's Magazine: 1844"  # ✅ 关键信息
# 而不是：
memory = "published in Philadelphia..."  # ❌ 无关信息
```

**2. 什么信息该丢弃**
```python
chunk = "The history of coffee cultivation in Brazil..."
# 模型学会：不更新记忆（无关内容）
```

**3. 如何组织记忆**
```python
# 好的记忆：
memory = "Arthur's: 1844, First for Women: 1989"

# 差的记忆：
memory = "Arthur's Magazine was founded in 1844..."  # 太冗长
```

### RL 训练的完整流程

#### Step 1: Rollout（生成轨迹）

```python
# 用当前模型处理训练样本
sample = {
    'question': "Which magazine started first?",
    'document': [chunk1, chunk2, ..., chunk200],  # 28K tokens
    'answer': "Arthur's Magazine"
}

# 模型逐个处理 chunks
memory_trajectory = []

# Turn 1
memory1 = model.update_memory(chunk1, "", question)
memory_trajectory.append(memory1)

# Turn 2
memory2 = model.update_memory(chunk2, memory1, question)
memory_trajectory.append(memory2)

# ... 继续处理所有 chunks

# 最后生成答案
predicted_answer = model.generate_answer(final_memory, question)
```

#### Step 2: 计算奖励

```python
# 简单的二元奖励
if predicted_answer == sample.answer:
    reward = 1.0  # 答对了！
else:
    reward = 0.0  # 答错了
```

**关键点**：
- 只有最终答案对错的反馈
- 没有告诉模型"第 3 轮记忆应该是什么"
- 模型需要自己推断：哪些记忆更新导致了正确答案

#### Step 3: 计算 Advantage（优势函数）

```python
# 在一个 batch 中生成多个轨迹
batch_rewards = [1.0, 0.0, 1.0, 0.0, ...]  # 16 个样本

# 计算每个样本的优势
for i, reward in enumerate(batch_rewards):
    advantage[i] = reward - mean(batch_rewards)
    # reward=1.0, mean=0.5 → advantage=+0.5 (好的轨迹)
    # reward=0.0, mean=0.5 → advantage=-0.5 (差的轨迹)
```

**含义**：
- Advantage > 0：这个轨迹比平均水平好，应该鼓励
- Advantage < 0：这个轨迹比平均水平差，应该抑制

#### Step 4: 更新模型权重

```python
# 对于每个 token 的生成
for turn in memory_trajectory:
    for token in turn:
        loss = -advantage * log_prob(token)

        # 如果 advantage > 0（好的轨迹）
        # → 增加这个 token 的概率

        # 如果 advantage < 0（差的轨迹）
        # → 降低这个 token 的概率

# 用梯度下降更新权重
optimizer.step()
```

### 关键澄清：不需要强模型！

**❌ 常见误解**：
```
用强模型生成训练集 → 让 base model 学习强模型的偏好
```

**✅ 实际情况**：

**训练数据来源**：
```python
# 只有：问题 + 文档 + 答案
training_data = {
    'question': "Which magazine started first?",
    'document': [200篇文章, 28K tokens],  # HotpotQA + RULER 合成
    'answer': "Arthur's Magazine"  # HotpotQA 原始答案
}

# 没有"标准笔记"！
# 没有"强模型生成的记忆"！
```

**RL 训练过程**：
```python
# 1. 让 base model 自己尝试
base_model = Qwen2.5-7B-Instruct  # 原始模型

for sample in training_data:
    # 模型自己做笔记（探索）
    memory_trajectory = base_model.process(sample)
    predicted = base_model.generate_answer(final_memory)

    # 2. 只看答案对错
    reward = 1.0 if predicted == sample.answer else 0.0

    # 3. 更新权重
    # 答对了 → 鼓励这种做笔记方式
    # 答错了 → 抑制这种做笔记方式
    update_weights(base_model, memory_trajectory, reward)
```

### 完整训练流程图

```
┌─────────────────────────────────────────────────────┐
│ 1. 准备训练数据                                      │
│    HotpotQA (问题+答案) + RULER方法 → 长文档        │
│    32,768 个样本，每个 28K tokens                   │
│    只有：问题 + 文档 + 答案（没有标准记忆！）       │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ 2. RL 训练（自我探索）                              │
│                                                      │
│    Base Model: Qwen2.5-7B-Instruct                  │
│         ↓                                            │
│    让模型自己尝试做笔记（没有老师！）                │
│         ↓                                            │
│    根据最终答案对错给奖励                            │
│         ↓                                            │
│    更新模型权重（学会做笔记）                        │
│         ↓                                            │
│    重复 32,768 个样本                                │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ 3. 得到 RL-MemAgent-7B                              │
│    模型学会了：                                      │
│    - 什么信息该记                                    │
│    - 什么信息该忘                                    │
│    - 如何组织记忆                                    │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ 4. 测试（分离的测试集）                              │
│    128 个样本，不同长度（7K - 3.5M tokens）         │
│    准确率：78.1% @ 3.5M tokens                       │
└─────────────────────────────────────────────────────┘
```

### With RL vs Without RL

| 方面 | Without RL | With RL |
|------|-----------|---------|
| **模型** | 原始 Qwen2.5-Instruct | RL-MemAgent |
| **做笔记能力** | 靠 prompt 引导（不会做） | 学会了做笔记 |
| **训练数据** | 无需训练 | 32,768 样本 |
| **有标准记忆吗？** | 无 | **无！只有最终答案** |
| **学习方式** | Zero-shot | 试错 + 奖励反馈 |
| **性能** | 随长度下降 | 保持稳定 |

### 训练前后对比

**训练前**（Without RL）：
```
Chunk 87: "Arthur's Magazine founded 1844..."
Memory: "Arthur's Magazine founded 1844 in Philadelphia
         published fiction and poetry..."  # 记了很多无关信息

Chunk 156: "First for Women started 1989..."
Memory: "Arthur's Magazine founded 1844 in Philadelphia
         published fiction and poetry First for Women
         started 1989..."  # 记忆越来越长，超出限制
```

**训练后**（With RL）：
```
Chunk 87: "Arthur's Magazine founded 1844..."
Memory: "Arthur's: 1844"  # 只记关键信息

Chunk 156: "First for Women started 1989..."
Memory: "Arthur's: 1844, First for Women: 1989"  # 简洁高效

Answer: "Arthur's Magazine"  # 正确！
```

### 为什么 RL 有效？

**核心思想**：从最终结果反推中间过程

```python
# 监督学习需要：
每一步的标准答案 → 模仿学习

# RL 只需要：
最终答案对错 → 自己探索最优策略
```

**优势**：
- 不需要昂贵的中间标注
- 模型可以探索多种策略
- 找到最适合自己的做笔记方式

### Multi-Conv DAPO 算法

MemAgent 的特殊之处：**多轮独立上下文对话**

```python
# 一个样本生成多轮对话
sample → [
    conversation1: (chunk1, memory1),
    conversation2: (chunk2, memory2),
    conversation3: (chunk3, memory3),
    ...
    final: (question, memory_final, answer)
]

# 关键：每轮对话是独立的（不在同一个上下文窗口）
# 但最终奖励要分配给所有对话
```

**解决方案**：
```python
# 用最终答案的奖励
final_reward = 1.0 if answer_correct else 0.0

# 分配给所有对话
for conversation in all_conversations:
    advantage[conversation] = final_reward - mean(batch_rewards)
```

### 训练 vs 测试

```python
# 训练集（32,768 个样本）
train_data = HotpotQA训练集 + RULER合成
- 用于 RL 训练
- 文档长度：28K tokens
- 模型在这些数据上学习做笔记

# 测试集（128 个样本）
test_data = HotpotQA验证集 + RULER合成
- 完全分离，训练时没见过
- 文档长度：7K - 3.5M tokens（多个版本）
- 测试外推能力
```

### 总结

**MemAgent 的 RL 训练**：
1. ✅ 训练的是记忆管理策略（什么该记、什么该忘）
2. ✅ 不需要强模型或标准记忆
3. ✅ 只需要：问题 + 文档 + 答案
4. ✅ 让模型自己探索 + 根据最终反馈学习
5. ✅ 训练后模型学会了高效做笔记

**核心理念**：
- 就像教学生做笔记
- 不是告诉他每句话该记什么
- 而是让他自己尝试
- 最后根据考试成绩调整方法

## 深入理解：关键问题解答

### Q1: RULER-HotpotQA 是什么？

**A**: RULER-HotpotQA 是 **RULER benchmark 本身就包含的任务**，不是 MemAgent 自己创造的。

- **RULER 的 QA 类别**包含：SQuAD（单跳）、HotpotQA（多跳）、MuSiQue、2WikiMultihop
- **构造方法**：将 HotpotQA 的黄金段落（包含答案）插入到随机采样的干扰段落中
- **MemAgent 的使用**：采用 RULER 的方法论，自己合成了训练和测试数据，并扩展到超长上下文（3.5M tokens）

### Q2: 为什么简单方法可能在 RULER-HotpotQA 上表现很好？

**A**: 因为 RULER-HotpotQA **本质上是检索任务，而非真正的多跳推理**。

**任务构造**：
```
黄金段落（needles，已包含答案）+ 干扰段落（haystack）
```

**为什么简单方法有效**：
1. 黄金段落已经包含完整答案
2. 任务退化为：找到相关 chunk → 提取答案
3. 不需要真正的"多跳推理"或"记忆聚合"

**真正的挑战**：
- 不在任务本身，而在**规模**（3.5M tokens，6400 篇文章）
- 需要高效检索和准确判断相关性
- 从 8K 训练窗口外推到超长上下文

**MemAgent 的贡献**：
- 通过 RL 学会了高效的检索策略
- 实现了短窗口到超长上下文的外推
- 而不是解决了复杂的多跳推理问题

### Q3: RL 训练是否更新模型权重？

**A**: **是的，MemAgent 的 RL 训练会更新整个 LLM 的权重**。

**证据**：
```python
# 损失函数
𝒥_DAPO(θ) = 𝔼[...优化目标...]

# 优化器
AdamW optimizer, lr=1e-6

# θ 是模型参数（权重）
```

**训练内容**：
1. 记忆更新策略（什么该记、什么该忘）
2. 上下文处理能力（如何提取关键信息）
3. 答案生成能力（基于记忆生成答案）

**训练流程**：
```
Rollout → 计算奖励 → 梯度更新 → 更新权重 θ
```

### Q4: 训练 vs 推理的区别

**训练阶段（一次性，离线）**：
```
32,768 个训练样本
↓
RL 训练（GRPO/DAPO）
- 生成轨迹
- 计算奖励
- 更新权重 θ
↓
得到：RL-MemAgent-7B
```

**推理阶段（每个新问题）**：
```
新的 QA 问题
↓
使用训练好的 RL-MemAgent-7B
- 权重固定，不更新
- 应用学到的策略
↓
输出答案
```

**关键点**：
- ❌ 不是每个新问题都要训练权重
- ✅ 训练一次，推理无数次
- 推理时只是**应用**训练时学到的记忆管理策略

### Q5: 没有 RL 的 MemAgent 在做什么？

**A**: **Zero-shot 记忆管理** = 原始模型 + 记忆机制 + Prompt 引导

**具体做法**：
```python
# 使用原始 Qwen2.5-Instruct（权重未改变）
# 通过 prompt 引导使用记忆机制

for chunk in document:
    prompt = f"""
    Memory: {old_memory}
    New Chunk: {chunk}
    Question: {question}
    Update the memory with relevant information.
    """
    new_memory = model(prompt)  # 用原始模型
    old_memory = new_memory
```

**与 RL 版本对比**：

| 方面 | 没有 RL | 有 RL |
|------|---------|-------|
| 模型权重 | 原始 Qwen2.5-Instruct | RL 训练后的权重 |
| 记忆策略 | 靠 prompt 引导 | 学习到的策略 |
| 性能 | 随长度增加而下降 | 保持稳定 |

**为什么表现较差**：
- 不知道什么该记（没学过选择性记忆）
- 记忆质量差（只靠 prompt，理解不够）
- 没有优化目标（RL 版本有明确的奖励信号）

**类比**：
- 没有 RL = 给学生纸和笔，告诉他"做笔记"，但没教怎么做
- 有 RL = 学生经过大量练习，学会了什么该记、什么该忘

### Q6: RL 训练集从哪里来？

**A**: 从 HotpotQA 数据集**合成**长上下文训练数据。

**构造过程**：

1. **原始数据**：HotpotQA 训练集（80,000 个样本）

2. **数据清洗**：
   ```python
   # 过滤掉模型已知的常识问题
   for question in hotpotqa_train:
       score = model.answer(question, context=None)
       if score == 100%:  # 不需要上下文就能答对
           continue  # 过滤掉
   ```
   - 过滤掉约 50%（40,000 个）
   - 剩余 40,000 个样本

3. **合成长上下文**（使用 RULER 方法论）：
   ```python
   for qa_pair in filtered_samples:
       # 获取黄金段落
       golden_paragraphs = qa_pair.supporting_facts

       # 随机采样干扰段落
       distractor_paragraphs = random_sample(
           hotpotqa_corpus,
           n=200  # 约 200 篇文章
       )

       # 插入黄金段落到干扰段落中
       long_document = insert_needles(
           golden_paragraphs,
           distractor_paragraphs
       )  # 约 28K tokens
   ```

4. **最终训练集**：前 32,768 个样本

**训练样本示例**：
```
{
  "question": "Which magazine was started first?",
  "document": [
    "Article 1: [无关内容]...",
    ...
    "Article 87: Arthur's Magazine was founded in 1844...",  # 黄金段落
    ...
    "Article 156: First for Women started in 1989...",  # 黄金段落
    ...
    "Article 200: [无关内容]..."
  ],  # 总共约 28K tokens
  "answer": "Arthur's Magazine"
}
```

**关键点**：
- 不是直接用 HotpotQA 原始数据
- 而是用 RULER 方法**合成**长上下文数据
- 黄金段落（needles）+ 干扰段落（haystack）
- 这样才能训练模型处理长上下文的能力

## 局限性与未来工作

- 需要 RL 训练才能有效利用记忆机制
- 记忆大小固定，可能限制某些任务的表达能力
- 当前主要在 QA 任务上验证，其他任务类型有待探索
- RULER-HotpotQA 本质上是检索任务，真正的多跳推理能力有待验证

## 数据集和资源

### 官方资源

- **数据集**: [HuggingFace - BytedTsinghua-SIA/hotpotqa](https://huggingface.co/datasets/BytedTsinghua-SIA/hotpotqa)
- **模型权重**:
  - [RL-MemAgent-14B](https://huggingface.co/BytedTsinghua-SIA/RL-MemoryAgent-14B)
  - [RL-MemAgent-7B](https://huggingface.co/BytedTsinghua-SIA/RL-MemoryAgent-7B)
- **代码仓库**: [GitHub - BytedTsinghua-SIA/MemAgent](https://github.com/BytedTsinghua-SIA/MemAgent)
- **项目主页**: [memagent-sialab.github.io](https://memagent-sialab.github.io/)

### 许可证

- **代码**: Apache 2.0 License
- **数据集**: 基于 HotpotQA（CC BY-SA 4.0）
- **可用于**: 研究和商业用途

### 使用数据集

#### 方法 1: 直接使用 MemAgent 处理好的数据

```python
from datasets import load_dataset

# 下载 MemAgent 的长上下文数据集
dataset = load_dataset("BytedTsinghua-SIA/hotpotqa")

# 数据格式
for sample in dataset['train']:
    question = sample['input']           # 问题
    context = sample['context']          # 长文档（约 28K tokens）
    answers = sample['answers']          # list of equivalent answers
    num_docs = sample['num_docs']        # 文档数量（约 200）
```

#### 方法 2: 从原始 HotpotQA 构造

```python
from datasets import load_dataset

# 下载原始 HotpotQA
hotpotqa = load_dataset("hotpot_qa", "fullwiki")

# 使用 MemAgent 的数据处理脚本
# 参考: taskutils/memory_data/ruler_data_prepare.py
```

### 数据集特点

- **训练集**: 32,768 个样本
- **测试集**: 128 个样本（多个长度版本）
- **文档长度**: 7K - 3.5M tokens
- **构造方法**: RULER 方法论（黄金段落 + 干扰段落）
- **答案格式**: 多个等价答案（list）

### 评测指标

**Accuracy 计算**：
```python
def compute_score(predicted, ground_truth_list):
    # 只要匹配任一等价答案就算对
    for gt in ground_truth_list:
        if is_equiv(predicted, gt):
            return 1.0
    return 0.0

# is_equiv() 进行字符串标准化：
# - 转小写
# - 去除标点
# - 去除冠词 (a, an, the)
# - 去除空格
```

### 快速开始

```bash
# 1. 克隆仓库
git clone https://github.com/BytedTsinghua-SIA/MemAgent.git
cd MemAgent

# 2. 安装依赖
pip install -r requirements.txt

# 3. 下载模型（可选）
# 使用 HuggingFace 模型或本地部署

# 4. 运行快速示例
python quickstart.py --model BytedTsinghua-SIA/RL-MemoryAgent-14B
```

## 关键引用

```bibtex
@misc{yu2025memagent,
  title={MemAgent: Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent},
  author={Hongli Yu and Tinghong Chen and Jiangtao Feng and Jiangjie Chen and Weinan Dai and Qiying Yu and Ya-Qin Zhang and Wei-Ying Ma and Jingjing Liu and Mingxuan Wang and Hao Zhou},
  year={2025},
  eprint={2507.02259},
  archivePrefix={arXiv}
}

@inproceedings{yang2018hotpotqa,
  title={HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering},
  author={Yang, Zhilin and Qi, Peng and Zhang, Saizheng and Bengio, Yoshua and Cohen, William W and Salakhutdinov, Ruslan and Manning, Christopher D},
  booktitle={EMNLP},
  year={2018}
}
```

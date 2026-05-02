# RULER: What's the Real Context Size of Your Long-Context Language Models?

**Authors**: Cheng-Ping Hsieh*, Simeng Sun*, Samuel Kriman, Shantanu Acharya, Dima Rekesh, Fei Jia, Yang Zhang, Boris Ginsburg

**Affiliation**: NVIDIA

**arXiv**: [2404.06654](https://arxiv.org/abs/2404.06654)

**Code**: [github.com/hsiehjackson/RULER](https://github.com/hsiehjackson/RULER)

**Conference**: COLM 2024

## 核心思想

RULER 是一个**合成基准测试**，用于全面评估长上下文语言模型的真实能力。通过灵活配置序列长度和任务复杂度，揭示模型声称的上下文长度与实际有效长度之间的差距。

关键洞察：简单的 needle-in-a-haystack (NIAH) 测试只能反映表面的长上下文理解能力，需要更全面的评测来检验检索之外的行为。

## RULER Benchmark 设计

### 四大任务类别

1. **Retrieval（检索）**: 扩展 NIAH 测试，包含多种类型和数量的 needles
   - **S-NIAH**: 单针检索（vanilla NIAH）
   - **MK-NIAH**: 多键检索（有干扰针）
   - **MV-NIAH**: 多值检索（同一键对应多个值）
   - **MQ-NIAH**: 多查询检索（检索多个不同的针）

2. **Multi-hop Tracing（多跳追踪）**:
   - **Variable Tracking (VT)**: 变量追踪任务
   - 模拟共指消解，测试追踪多跳连接的实体能力
   - 例如：`X1=V, X2=X1, X3=X2, ...` 找出所有指向 V 的变量

3. **Aggregation（聚合）**:
   - **Common Words Extraction (CWE)**: 常见词提取
   - **Frequent Words Extraction (FWE)**: 高频词提取
   - 作为摘要任务的代理，测试聚合长范围相关信息的能力
   - 相关信息占据更大比例的上下文

4. **Question Answering（问答）**:
   - 在现有短上下文 QA 数据集中添加干扰信息
   - 包括 SQuAD, HotpotQA, MuSiQue, 2WikiMultihop
   - 真实世界的 NIAH 适配版本

### 灵活配置

- **序列长度**: 4K, 8K, 16K, 32K, 64K, 128K（可扩展）
- **任务复杂度**: 可调整 needle 数量、类型、长度等
- **合成数据**: 减少对参数知识的依赖，确保黄金信息在上下文中

## 实验结果

### 评测设置

- **模型数量**: 17 个长上下文 LLM（15 开源 + 2 闭源）
- **模型范围**: 7B 到 8x22B（MoE），声称上下文长度 32K 到 1M
- **评测任务**: 13 个任务，每个长度 500 个样本
- **推理环境**: vLLM，BFloat16，8x A100 GPUs，贪婪解码

### 有效上下文长度（Effective Context Size）

使用 Llama2-7B 在 4K 的性能作为阈值，判断模型能有效处理的最大长度。

### 主要发现

1. **声称 vs 实际**:
   - 几乎所有模型在 vanilla NIAH 上接近完美
   - 但在 RULER 更复杂任务上随长度增加大幅下降
   - 只有**一半模型**能在 32K 保持满意性能
   - 几乎所有模型在达到声称长度前就低于阈值

2. **顶级模型特征**:
   - **Gemini-1.5-Pro**: 大幅领先，有效长度超过测试最大值（128K+）
   - **开源前三**: Llama3.1, Qwen2, Command-R-plus
   - 共同特点：更大模型尺寸、RoPE 更大基频
   - 训练长度不是决定因素（Llama3.1 训练 128K vs Qwen2 训练 32K）

3. **性能退化模式**:
   - Yi-34B（声称 200K）在长度和复杂度增加时大幅退化
   - 长上下文时常见问题：
     - 返回不完整答案
     - 无法精确定位相关信息
     - 增加对参数知识的依赖
     - 非检索任务时倾向从上下文复制

4. **模型架构影响**:
   - 更大模型尺寸 → 更好长上下文能力
   - 在更长序列上训练不总是带来更好性能
   - 非 Transformer 架构（RWKV, Mamba）仍大幅落后

### 加权平均排名

两种加权方案模拟真实使用场景：
- **wAvg. (inc)**: 权重随长度线性增加（长序列主导）
- **wAvg. (dec)**: 权重随长度线性减少（短序列主导）

顶级模型在两种方案下都保持一致的优势。

## 技术细节

### Needle 格式

- **Key-Value 对**: "The special magic number for XXX is: YYY"
- **类型多样性**:
  - Words（形容词-名词）
  - Numbers（7 位数字）
  - UUIDs（32 位）
- **Haystack 类型**:
  - 重复噪声句子
  - Paul Graham 文章

### 评测指标

- **Recall-based Accuracy**: 检查目标输出是否存在
- **Answer Prefix**: 防止模型拒绝回答或生成解释
- **每任务 500 样本**: 确保统计显著性

## 与现有 Benchmark 对比

| Benchmark | 类型 | 长度控制 | 任务多样性 | 参数知识影响 |
|-----------|------|----------|------------|--------------|
| ZeroScrolls | 真实 | 固定 | 中 | 高 |
| LongBench | 真实 | 固定 | 高 | 高 |
| L-Eval | 真实 | 固定 | 中 | 高 |
| **RULER** | **合成** | **灵活** | **高** | **低** |

RULER 的优势：
- 灵活配置序列长度和任务复杂度
- 合成数据减少参数知识干扰
- 保证黄金信息在上下文中
- 测试检索之外的多种行为

## 局限性

1. **缺少位置控制**: 不提供深度级别性能（如 lost-in-the-middle 现象）
2. **合成 vs 真实**: 合成任务可能不完全反映真实应用场景
3. **阈值选择**: 使用 Llama2-7B 4K 作为阈值可能需要随时间更新

## 关键引用

```bibtex
@inproceedings{hsieh2024ruler,
  title={RULER: What's the Real Context Size of Your Long-Context Language Models?},
  author={Cheng-Ping Hsieh and Simeng Sun and Samuel Kriman and Shantanu Acharya and Dima Rekesh and Fei Jia and Yang Zhang and Boris Ginsburg},
  booktitle={Conference on Language Modeling (COLM)},
  year={2024}
}
```

## 总结

RULER 揭示了长上下文 LLM 的真实能力与声称能力之间的显著差距。即使在简单的 NIAH 测试中表现完美的模型，在更复杂的检索、多跳追踪和聚合任务上也会随着上下文长度增加而大幅退化。这个 benchmark 为评估和改进长上下文模型提供了重要工具。

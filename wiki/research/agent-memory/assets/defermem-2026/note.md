---
title: "DeferMem: Query-Time Evidence Distillation via Reinforcement Learning for Long-Term Memory QA"
updated: 2026-10-09
---

# DeferMem: Query-Time Evidence Distillation via Reinforcement Learning for Long-Term Memory QA

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文 §1–5、参考文献、附录 A–E 含 prompt 与 Table 9）。图（Fig. 1–3）只有文字说明，Fig. 3 的数值未读到；Table 7/8 在文本中缺失（附录只见 Table 4–6、9）。

## Summary

问题：长期对话记忆 QA 中，证据分散在多个 session 里并混在大量无关内容中。已有系统在写入时就压缩/组织记忆，查询时按相似度检索，结果是召回集很大但噪声多，去噪和还原证据的负担留给下游 answerer (§1)。

方法：把流程拆成两步 (§3.1, Eq. 1)。
- 检索 R：保留原始消息，建 segment-link 结构（沿用 LightMem 的话语边界分段，段间按最大余弦相似度用阈值 τ2 串成 link）。查询时取 top-k 消息，扩展到所在 segment 和同 link 的 segment，得到高召回、高噪声的候选集 (§3.2)。
- 蒸馏 D：用 Llama-3.1-8B-Instruct 作 distiller，输出结构化动作 (U, Z)，即选中的消息 ID 加每条消息对应的自包含、忠实、与 query 相关的改写证据 (§3.3)。
- 训练算法 DistillPO，以 DAPO 为基础，三处改动：
  1. 把 reward 拆成 8 项 r0–r7（格式、ID 合法、覆盖 gold 支持消息、简洁、选择与证据对齐、忠实/自包含的 LLM 判定、答案正确、失败归因）(Table 9)。
  2. "leaky" 分层门控：结构类 reward 依赖前置项，覆盖与答案类 reward 只要格式合法就开放 (App. C.1)。
  3. 结构对齐 advantage：选择 span 和证据 span 分别用各自的 reward 求组内归一化 advantage (Eq. 11)。
- 另外每组加一条由 GPT-5.2 生成、满分的 anchor completion (App. C.2)。

结果（GPT-4o-mini 作 answerer 和 judge，Table 1）：
- LongMemEval-S：Acc 70.00，LightMem 68.64，NaiveRAG 61.00，A-Mem 62.60。内存操作 API token 为 0k，耗时 90.30s，LightMem 为 283.76s。
- LoCoMo（去掉训练用的 conv-26）：非对抗 87.90、对抗 96.99，对应最强基线约 79.5 和 92.7；耗时 83.56s，LightMem 为 815.32s。
- 消融 (Table 3a)：去掉 distiller，LoCoMo 降 5.82、LME-S 降 8.00。未训练的 base 模型降约 18 点。SFT 和原版 DAPO 都明显低于 DistillPO。去掉 reward 流水线与结构对齐 advantage 降约 7.6 点。
- 召回 (Table 2)：多数阈值组合下 Recall 在 98% 以上，候选 token 量从 14k 到 58k 不等。
- LongMemEval-M (§4.5, Table 3b)：Acc 63.00，耗时 802s。
- 误差 (Table 3c)：LME-S 上 distillation error 占 14.2%，answerer error 占 10.4%，retrieval miss 占 2.2%。

## Evidence and Limits

设置：distiller 为 Llama-3.1-8B + rank-16 LoRA，单张 A100 80G，G=5，训练数据为 LoCoMo conv-26 的 199 条 QA 加 130 条由 LongMemEval 历史构造语料派生的 QA (§4.1, Table 5)。训练需要 gold 证据消息标注，且 r5–r7 和 anchor 依赖外部 LLM（GPT-5.2、judge）。

论文声称与证据的对照：
- "最高准确率、最快、零 API token"基本被 Table 1 支持，但"零 token"只统计商业 API 的记忆操作，不含本地 8B 模型的 GPU 推理，也不含训练期的商业 LLM 调用（作者在 App. E 承认后者）。耗时也不含最终回答。
- LME-S 上相对 LightMem 只高 1.36 点，没有多 seed 或置信区间。单源变体 DeferMem†（只用 LoCoMo conv-26 训练）在 LME-S 为 66.20，低于 LightMem 的 68.64。因此"跨数据集泛化"只是部分成立，LoCoMo 上的优势主要来自含同分布数据的训练。
- LoCoMo 全量结果含训练用的 conv-26，作者因此另报 w/o conv-26，这是合理的处理。但训练和测试同属 LoCoMo 分布，QA 类型一致。
- 多数基线数字直接取自 LightMem 论文及其公开输出，在 A.3 说明；GAM、MemGAS 的来源在文本中不够明确。Memory-R1 无公开实现，只能引用其论文里的数字，且只有一格，不可比。
- LoCoMo 对抗题的 answer prompt 要求信息不足时弃答，这会抬高所有方法的对抗题分数，作者已指出。judge 提示偏宽松（"touches on the same topic"）。
- 错误分析的分类是作者自己做的，标注方式文中没有详述。
- 代码：正文和附录均未给出官方仓库地址。

## Open Questions

- 蒸馏出的证据由 8B 模型改写，faithfulness 只由 LLM judge（r5）在训练时约束。评测时没有独立衡量改写引入的幻觉或信息丢失，LME-S 上 14.2% 的 distillation error 具体由哪类错误构成也不清楚。
- 训练数据只有约 330 条 QA，且来自两个基准的相近分布。换到别的对话领域（如更长、更多噪声、非英文）时，distiller 是否仍有效未验证。LongMemEval-M 上 Recall-01 降到 87.2，检索瓶颈是否变成主要误差也未分析。
- 各 reward 项和门控设计的单独贡献只有整体消融（如去掉 reward 流水线加结构对齐 advantage 一起去），r0–r7 逐项的作用以及 leaky 与 strict 门控的直接对比没有给出。

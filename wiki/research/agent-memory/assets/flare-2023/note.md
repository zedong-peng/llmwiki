---
title: "Active Retrieval Augmented Generation"
updated: 2026-10-09
---

# Active Retrieval Augmented Generation

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文、附录 A–C 与 Prompt 部分的开头；Figure 4/5 为图，数值未提取，只能依据正文描述；Prompt D.3 之后的 few-shot 示例未细读）。

## Summary

问题：常见的 retrieve-and-generate 只依据输入检索一次，长文本生成（长篇 QA、摘要、CoT 推理）的信息需求在生成过程中才逐步出现，一次检索不够 (§1)。

方法：提出 active retrieval augmented generation 框架（§2.3），即在生成过程中决定何时检索、检索什么。具体实现 FLARE (§3)：
- 先不带检索文档，临时生成下一句 ŝ_t；若其中任一 token 概率低于阈值 θ，就用 ŝ_t 构造查询检索，再基于检索结果重新生成该句；否则直接接受。
- 查询构造有两种：把概率低于 β 的 token 遮掉作为 implicit query，或对低置信 span 用 gpt-3.5-turbo 生成问题作为 explicit query (§3.2.2)。
- 另有 FLARE_instruct：用 few-shot 让模型输出 "[Search(query)]"（§3.1）。
- 只作用于推理阶段，无需训练；基础模型 text-davinci-003，检索器为 BM25（Wikipedia）或 Bing（WikiAsp）。每步只保留当前检索的文档。

结果 (§6)：在 4 个任务上，每个数据集最多取 500 条样本。
- 2WikiMultihopQA EM（Table 1）：无检索 28.2，单次检索 39.4，previous-window 43.2，previous-sentence 39.0，question decomposition 47.8，FLARE_instruct 42.4，FLARE_direct 51.0。
- StrategyQA EM（Table 2）：无检索 72.9，单次检索 68.6，FLARE 77.3。
- ASQA EM 41.3（单次 40.0）；ASQA-hint EM 46.2（单次 43.2）；WikiAsp UniEval 53.4（单次 52.4，无检索 47.1）。
- 消融（§6.2）：用下一句检索优于用上一句（Table 3，2Wiki EM 48.8 对 39.0）；β=0.4 优于不遮掩（Table 5，EM 0.510 对 0.488）；implicit 与 explicit 查询效果相近（Table 6）；约 40%–80% 的句子触发检索时表现较好，StrategyQA 在检索比例超过 50% 后下降（Figure 5）。

## Evidence and Limits

- 主结论“FLARE 在所有任务上优于或持平基线”大体成立，但在多数数据集上差距很小（如 ASQA EM 41.3 对 40.0，WikiAsp UniEval 53.4 对 52.4），论文只给单次运行结果，没有方差或显著性检验。真正显著的提升在 2WikiMultihopQA 和 StrategyQA。
- 基线均为作者在同一设定下重新实现，并非原论文的精确复现 (§4)；question decomposition 基线用了手工标注的子问题示例。
- 超参 θ、β、查询方式、是否混合单次与多次检索按数据集在 dev set 上调（Table 9），说明方法并非完全 generic；各数据集 θ 为 0.4 或 0.8。
- 评测规模小：每个数据集最多 500 条（StrategyQA 为 229），只用一个闭源模型 text-davinci-003 和 BM25/Bing 检索器，没有验证更小或开源模型。
- 作者自述局限 (§9)：在 Wizard of Wikipedia 和 ELI5 上没有显著增益；交错检索与生成带来额外开销，需要多次调用 LM 并重新计算激活，附录 A 称平均 30%–60% 的句子触发检索，但没有给出实际延迟或成本数字。
- “低概率即缺乏知识”依赖 LM 校准良好的假设，由引用支持，本文没有直接验证；ASQA 上 explicit 查询还依赖另一个模型（gpt-3.5-turbo）。
- FLARE_instruct 明显弱于 FLARE_direct（Table 1），论文归因于 API 模型难以可靠地输出检索指令。
- 附录 A 提到对 exemplar 使用了检索结果以提升表现，这一细节只在 2WikiMultihopQA 上使用（Table 7）。

## Open Questions

- 概率阈值 θ 是否能跨模型和跨任务迁移？不同数据集需要分别调参，而更新或经过 RLHF 的模型校准性质不同。
- 上一句检索与下一句检索的差距（Table 3）有多少来自“前瞻”本身，多少来自任务结构（2Wiki 中相邻句常涉及不同实体）？
- 方法的收益与开销之比没有量化：多次触发检索与重新生成的实际代价，相对 +1~+10 点 EM 的收益是否划算，文中未说明。

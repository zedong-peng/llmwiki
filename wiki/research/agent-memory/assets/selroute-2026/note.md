---
title: "SelRoute: Query-Type-Aware Routing for Long-Term Conversational Memory Retrieval"
updated: 2026-10-09
---

# SelRoute: Query-Type-Aware Routing for Long-Term Conversational Memory Retrieval

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文 §1–7、附录 A–C、参考文献）。无图；表格提取清晰，未见乱码。

## Summary

问题：长期对话记忆检索（LongMemEval M，每题约 460–490 个 session 的 haystack）通常靠 110M–1.5B 的 dense 检索器或 LLM 生成 fact key。作者认为 query 类型决定最优检索策略，提出 SelRoute：按 query 类型把查询路由到不同 pipeline（§3）。

方法（§3）：
- 基础组件：SQLite FTS5（BM25）、embedding（bge-small 33M、MiniLM 22M、bge-base 109M，内容截断到 2000 字符）、两者的 RRF 融合（k=60）。
- 存储期规则式词汇扩展：210 条上位词、70 条动作桥接、13 个 topic room，只追加到 FTS5 索引，原文不变。
- 路由表（6 种类型）：knowledge-update 用 enriched FTS；multi-session 用 enriched hybrid；ss-assistant 与 ss-preference 用纯 embedding；ss-user 用纯 FTS5；temporal 用 hybrid。路由表由 51 条"至少一种策略失败"的难例子集经验推出。
- 推理时不需要 GPU，也不需要 LLM。

主要结果（§5.1，session 级、all-or-nothing Recall@5，500 题含 30 条 abstention）：
- 零 ML 的 FTS5 为 Ra@5 0.745 / NDCG@5 0.692，已高于文献中的 BM25（0.634 / 0.516）和 Contriever（0.723 / 0.634）。
- SelRoute 的 MiniLM、bge-small、bge-base 分别为 0.785、0.786、0.800；对比 Contriever + fact keys 的 0.762。
- 消融（§5.4，bge-small）：uniform hybrid 0.756，uniform enriched FTS5 0.751，路由 0.786。
- 分类型提升（§5.2）：ss-assistant 从 0.804 到 0.964，multi-session +0.055，ss-user 无提升。
- 词汇扩展帮助 FTS5，却会损害 embedding 检索（§3.2、§5.3、§6.2）。在难例子集上，multi-session 从 0.462 升到 0.751。
- 负面结果（§5.5）：8 步 "dream cycle" 重写存储内容，加权 Ra@5 从 0.829 降到 0.145。
- 用正则分类器预测类型（§5.8）：整体准确率 71.9%，"有效路由准确率" 83.0%。端到端 Ra@5：预测类型 0.689，oracle 类型 0.711，uniform FTS5 0.653，uniform hybrid 0.666。
- 跨 benchmark（§5.9，另 8 个，共 62,292 实例）：MSDialog 0.998，LMEB 0.977，LoCoMo 0.767，PerLTQA 0.745，QReCC 0.595，Episodic 0.667，RECOR 仅 0.149。

## Evidence and Limits

论文声称与证据：
- "路由而非模型规模带来收益"：MiniLM 与 bge-small 差 0.001，支持该点。
- 对 uniform 策略的提升有显著性检验（§5.6，bge-small）：对 FTS5 +0.057（p=0.0003），对 uniform hybrid +0.045。对"最佳单一 RRF 变体"仅 +0.011（p=0.121），不显著。作者自己承认路由的价值在于按类型选择策略，并不比所有融合方法都强。
- 对 Contriever + fact keys 的优势：bge-base 的 CI 为 [0.757, 0.830]，作者称优势"borderline"。
- 交叉验证（§5.7）：5 折分层，泛化差 1.3–2.4 点；4/6 类型的路由稳定。

局限（多数为作者自述）：
- 路由表来自评测集本身的难例子集，没有独立开发集（§6.5）。
- 与已发表 baseline 的比较有混杂：FTS5 比文献 BM25 高 0.111，比路由本身带来的增益还大。作者列出可能原因（tokenizer、query 预处理、BM25 参数），但没有用标准 BM25（如 Pyserini）重跑（§6.3）。baseline 数字直接取自 LongMemEval 原文 Table 9，没有自己重跑任何 dense 模型。
- 主结果依赖 oracle 类型元数据。正则分类器在 knowledge-update（38.9%）和 ss-user（46.9%）上很差。"有效准确率 83%"是把落在同一 route family 的误分类算作无害，是作者自定义的指标。
- 数字之间有不一致，文中未解释：bge-base 在 §5.1 的表里是 0.800，同一段的 bootstrap 给 0.794；§5.9 表中 LongMemEval M 最佳为 0.774；§5.7 中 bge-small 全数据为 0.711，而 §5.1 为 0.786；分类型表（§5.2）与附录 C 的 Ra@5 也对不上。可能因所用指标子集不同（如 470 题 vs 500 题），但文本没有说明。bge-base 的 NDCG@5 与 Ra@5 同为 0.800，也让人存疑。
- 手工编写的扩展词表；abstention 基本没解决（1/30）；preference 类型最弱（0.533，n=30）。
- 跨 benchmark 并非"路由"的检验：多个 benchmark 没有 LongMemEval 式的类型标签，表中很多最佳结果来自单一 FTS5，没有说明路由在这些集合上是否真起作用。
- RECOR 上 0.149，说明在需要推理的多跳检索上失败。
- 实验环境：消费级笔记本、CPU（MLX/ONNX），500 题约 43 分钟（bge-small）。单作者、arXiv 预印本、无同行评审。

## Open Questions

- 去掉 FTS5 与标准 BM25 的实现差异后，路由本身还剩多少增益？§5.6 显示相对最佳 RRF 变体不显著，这一点尤其需要澄清。
- 在没有类型元数据、且路由表不由评测集派生的真实部署里，增益是否保持？关键一步分类器在 2 个类型上准确率低于 50%，用更强的分类器能否缩小与 oracle 的差距尚未验证。
- 各表之间 0.800 / 0.794 / 0.774 / 0.711 的差异从何而来，哪个数字对应最终可复现配置？

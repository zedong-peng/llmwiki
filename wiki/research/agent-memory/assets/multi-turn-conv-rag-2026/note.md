---
title: "Comprehensive Comparison of RAG Methods Across Multi-Domain Conversational QA"
updated: 2026-10-09
---

# Comprehensive Comparison of RAG Methods Across Multi-Domain Conversational QA

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文、参考文献、附录 A–D）。图 1–4、6 只有标题和文字描述，曲线数值无法读取；表格可读。BibTeX 记录里的标题（"Multi-Turn Conversational RAG: Retrieval Stability"）与论文实际标题不一致，此处以论文为准。作者：Alushi, Strich, Biemann, Semmann（Hamburg），arXiv 2602.09552。

## Summary

问题：多轮对话式 QA 中，RAG 方法多半被孤立评测、且以单轮为主；缺少在统一设置下对多种 RAG 策略的系统比较，也缺少“对话轮次如何影响检索”的分析（§1）。

做法（§3–5）：
- 数据：ChatRAG-Bench 的 8 个子集（QuAC、SQA、QReCC、TopiOCQA、Doc2Dial、DoQA、CoQA、INSCIT），共 29,872 个 QA 对、246,635 个 context（Table 1）。排除 HybriDial（无标注 gold context）和 ConvFinQA（答案为数值，F1 不可靠）。
- 方法：No RAG（下界）、Oracle Context（上界）、Vanilla RAG、BM25、Hybrid BM25、Reranker（cross-encoder）、HyDE、Query Rewriting、Summarization、SumContext、HyDE+Reranker。
- 设置：EncouRAGe 库 + vLLM，Llama 3 8B Instruct，temperature 0，Chroma 向量库，all-MiniLM-L6-v2 嵌入，单张 RTX A6000。指标：检索用 MRR@5 与 Recall@1/5，生成用 SQuAD 式 F1（多参考取最大）。
- 附录 B 在 Gemma 3 27B 上重复，结论方向一致。

主要结果（Table 2，Llama 3 8B）：
- Oracle 与 No RAG 的 F1 差距：CoQA 83.9 对 28.9，SQA 69.6 对 25.1；多数数据集 Oracle 的 F1 低于 40（Figure 2，§4.2）。
- HyDE 检索最强，在 5/8 数据集上 MRR 最高；INSCIT 上 MRR 从 Vanilla 的 8.0 升到 25.2，TopiOCQA 上 8.7 升到 25.1。
- Reranker 与 Hybrid BM25 在多数数据集上 F1 略高于 Vanilla，如 CoQA 上 74.7 / 67.3 对 58.3，SQA 上 51.3 / 45.6 对 43.8。
- Query Rewriting、Summarization 在多个数据集上低于 No RAG（如 QReCC 32.5 对 35.9，TopiOCQA 26.9 对 34.2）。
- 检索与生成的 Spearman ρ（Table 3）：TopiOCQA 0.874、QReCC 0.857、INSCIT 0.788 较高；SQA 0.383、DoQA -0.157 很弱或为负。DoQA 的 MRR 超过 90 但 F1 低于 40，作者归因于非正式回答、模型拒答、回答格式。
- 分轮次分析（Figure 4，§5.7）：INSCIT、TopiOCQA 随轮次下降（topic switching、context/问题比很高）；CoQA、SQA 随轮次上升；QReCC、QuAC 在第 5 轮后下降。

结论（§6）：简单稳健的方法（Reranker、Hybrid BM25、HyDE）优于 Vanilla RAG；有效性取决于检索策略与数据集结构的匹配，而不是方法复杂度。

## Evidence and Limits

- 声称与证据有出入。摘要和结论称 Reranker / Hybrid BM25“在所有评测领域一致优于” Vanilla，但 Table 2 中 Reranker 在 QReCC（36.0 对 36.5）和 INSCIT（19.1 对 19.2）F1 更低，Hybrid BM25 在 INSCIT F1 更低（19.1 对 19.2），MRR 在 SQA、DoQA 也低于 Vanilla；多数差距只有零点几到一两个点，且没有显著性检验。正文 §5.5 称 Hybrid BM25 F1“在所有数据集上”略高，同样与表不符。
- “HyDE 使 TopiOCQA 的 F1 提高 9.6%”：表中是 33.9 到 43.5，即 9.6 个点而非百分比。“Oracle 提升 15–50%”同理是点数。
- 每个方法每个数据集只报一次运行，称多次运行差异可忽略，但没有给数据或方差。
- 嵌入模型是小型的 all-MiniLM-L6-v2，生成器是 8B（附录 27B）；结论是否迁移到更强的嵌入、检索器或模型未检验。
- 检索查询如何构造（是否拼接对话历史）正文未说明，却直接影响“轮次”结论；Query Rewriting 失败的原因只是推测（“话题切换更大、依赖链更长”），没有消融。
- 计算开销只有定性描述（Hybrid BM25 运行时间“略长”），无延迟或成本数字。
- 作者自述局限：方法与数据集异质、需要大量数据集相关的预处理；TopiOCQA、QuAC、INSCIT 的 context 过多使检索困难。
- 数据集层面：F1 对回答风格敏感（CoQA 短答案对 INSCIT 长答案），跨数据集的 F1 绝对值不可直接比；No RAG 只被当作预训练重叠的代理指标。
- 代码：脚注写了“GitHub Repository”，正文文本中没有给出 URL。

## Open Questions

- 方法间的小差距（Hybrid BM25、Reranker 对 Vanilla）在多次运行或不同嵌入模型下是否仍然稳定？
- 轮次下降究竟来自检索查询里累积的对话噪声，还是来自数据集本身（topic switching、context 数量），论文没有把两者分开。
- 更强的生成器或检索器下，HyDE 的大幅增益（INSCIT、TopiOCQA 上 MRR 约三倍）是否依然存在，还是主要补偿了小嵌入模型对短查询的弱点？

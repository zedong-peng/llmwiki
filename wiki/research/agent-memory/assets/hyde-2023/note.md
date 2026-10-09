---
title: "Precise Zero-Shot Dense Retrieval without Relevance Labels"
updated: 2026-10-09
---

# Precise Zero-Shot Dense Retrieval without Relevance Labels

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（arXiv v1，正文、参考文献与附录 A.1 的 prompt）。版面提取较乱但表格数字可读；Figure 1 只有文字残片。BibTeX 记录标注为 SIGIR 2023，而文本本身是 2022 年 12 月的 arXiv 预印本。

## Summary

问题：没有任何相关性标注（也不使用目标语料训练）时，如何做出有效的 dense retrieval。难点在于 query 与 document 两个 encoder 要在同一空间里让内积表示相关性，没有标签就无法学（§3.1）。

方法 HyDE（Hypothetical Document Embeddings，§3.2）把检索拆成两步：
- 生成：用 instruction-following LLM（InstructGPT text-davinci-003，temperature 0.7）按任务相关的 instruction 写一篇"回答该问题的段落"。该段落可能含事实错误，只需体现相关性的形态。
- 编码：用无监督对比学习的 encoder（英文用 Contriever，多语言用 mContriever）把假想文档编码，取 N 个样本向量的平均（式 7），也可把 query 本身向量并入平均（式 8）；再用该向量在真实文档向量中做内积检索。encoder 的稠密瓶颈被视为有损压缩，滤掉幻觉细节。
- 全程不训练任何模型，query-document 相似度不再被显式建模。

主要结果：
- 网页检索（Table 1）：DL19 上 HyDE 的 map/ndcg@10/recall@1k 为 41.8/61.3/88.0，Contriever 为 24.0/44.5/74.6，BM25 为 30.1/50.6/75.0。DL20 上 HyDE 为 38.2/57.9/84.4，Contriever 为 24.0/42.1/75.4。DL19 上与 ContrieverFT（41.7/62.1/83.6）相当，recall@1k 最高；DL20 上 map、ndcg@10 低于 ContrieverFT（43.6/63.2），也低于 ANCE 的 ndcg@10（64.6）。
- BEIR 六个低资源集（Table 2，nDCG@10）：HyDE 在 Scifact 69.1、Arguana 46.6、FiQA 27.3、DBPedia 36.8、TREC-NEWS 44.0 上高于 BM25 与 Contriever；TREC-Covid 为 59.3，比 BM25（59.5）低 0.2，Contriever 仅 27.3。FiQA、DBPedia 上 ContrieverFT（32.9、41.3）更高。
- Mr.TyDi（Table 3，MRR@100）：HyDE 在 Swahili/Korean/Japanese/Bengali 为 41.7/30.6/30.7/41.3，均高于 mContriever；Bengali 低于 BM25（41.8）。mContrieverFT 为 51.2/34.2/32.4/42.3，在 Swahili 差距明显。
- 换生成模型（§5.1，Table 4，DL19/DL20 nDCG@10）：Flan-T5 11b 为 48.9/52.9，Cohere 52b 为 53.8/53.8，GPT 175b 为 61.3/57.9，模型越大越好。
- 搭配微调 encoder（§5.2）：弱 LLM 会略微拉低 ContrieverFT，InstructGPT 在 DL19 上可从 62.1 提到 67.4，DL20 从 63.2 到 63.5。

## Evidence and Limits

- 论文的主张是"相关性建模可以交给 LLM，从而不需要相关性标签"。证据覆盖网页检索、六个 BEIR 子集、四种语言，对比基线较完整（BM25、Contriever、DPR/ANCE、ContrieverFT），支持"明显优于无监督 Contriever、可与部分微调模型相当"。
- "监督信号只存在于 LLM 的 instruction tuning 里"：InstructGPT 本身受过大量人类反馈数据训练，所谓 zero-shot 依赖这一点（§2 自己也承认）。
- instruction 按数据集手写（A.1），不同数据集措辞与限定词不同，没有消融 prompt 敏感性；Arguana 的 prompt 是写反驳论点，属于针对任务的设计。
- 只用 6 个 BEIR 低资源集，选择标准未说明，没有报告 BEIR 全集；没有方差、显著性检验，也没有多次采样的结果分布。N 的取值、式 7 与式 8 的选用及其对比，正文未给出数字。
- 未报告延迟与成本：每个 query 需调用一次 175B 级 LLM 生成，文中只在结论里提出"早期用 HyDE，积累日志后逐步切到监督检索"的使用设想。
- 公式推导中假设 query 无歧义（分布单峰），歧义 query 与多样性留作未来工作。
- 多语言上与微调模型差距较大，作者归因于低资源语言在 pre-training 与 instruction learning 中训练不足，这是假设，未验证。
- 对 FiQA、DBPedia 上落后的解释是 instruction 欠具体，同样没有实验验证。
- Cohere 模型细节未公开，作者只"tentatively"猜测训练技术也有影响。

## Open Questions

- 幻觉内容有多少被 encoder "滤掉"、有多少反而把检索带偏？论文没有对错误事实的案例或误检做分析。
- 收益有多少来自 LLM 的世界知识（相当于把答案直接写出来），有多少来自"相关性形态"？未与直接用 LLM 回答再检索等方式区分。
- 对歧义 query、多跳问题和对话式搜索是否仍成立，论文只说期待，没有实验。

---
title: "Dense Passage Retrieval for Open-Domain Question Answering"
updated: 2026-10-09
---

# Dense Passage Retrieval for Open-Domain Question Answering

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文、参考文献、附录 A–D）。Figure 1 只有坐标轴和图例文字，曲线本身未读到；Table 2–6 文本可读，列对齐略乱但数字清楚。

## Summary

问题：开放域 QA 的检索环节长期依赖 TF-IDF/BM25；此前唯一胜过 BM25 的稠密检索是 ORQA，但它需要计算量大的 inverse cloze task (ICT) 预训练，且 context encoder 不用问答对微调（§1）。

方法（§3）：Dense Passage Retriever (DPR) 是双编码器，问题和段落各用一个独立的 BERT-base (uncased)，取 [CLS] 向量（d=768），相似度为内积。段落事先编码并用 FAISS 建索引。训练目标是对正例段落的 NLL，关键在负例选择：batch 内其他问题的 gold 段落作 in-batch negatives（batch 128），再为每个问题加 1 条 BM25 hard negative。语料为 2018-12-20 的英文 Wikipedia，切成 100 词不重叠段落，共 21,015,324 条，段首加标题（§4.1）。数据集：NQ、TriviaQA、WebQuestions、CuratedTREC、SQuAD；只有答案的数据集用 BM25 top-100 中含答案的最高排名段落当正例（§4.2）。

检索结果（Table 2，测试集 top-20）：NQ 上 DPR 78.4 对 BM25 59.1；TriviaQA 79.4 对 66.9；WQ 73.2 对 55.0；TREC 79.8 对 70.9；SQuAD 例外，DPR 63.2 低于 BM25 68.8。Multi 训练（除 SQuAD）下 TREC 升到 89.1。BM25+DPR 线性组合（λ=1.1）在部分数据集上继续提升。引言另报 NQ top-5 为 65.2 对 42.9。

消融（§5.2，Table 3，NQ dev）：普通 1-of-N 设置下负例类型影响很小；换成 in-batch 后明显提升，且随 batch 增大而提高；再加 1 条 BM25 负例，top-5 到 65.0（仅 gold in-batch 为 51.1–55.8），加第 2 条无增益。内积与 L2 相当，均优于 cosine；triplet loss 与 NLL 差别不大（Appendix B）。只用 1,000 条训练样本就超过 BM25（Figure 1）。

端到端 QA（§6，Table 4）：reader 为 BERT-base，对 top-k（至多 100）段落打分并抽取 span。NQ EM 41.5（ORQA 33.3，REALM 39.2/40.4），TriviaQA 56.8；Multi 下 WQ 42.4、TREC 49.4。作者称在五个数据集中的四个上超过此前最好结果。效率（§5.4）：FAISS 995 问/秒，Lucene-BM25 每 CPU 线程 23.7 问/秒；但稠密向量编码 8 GPU 约 8.8 小时，建 FAISS 索引约 8.5 小时，Lucene 倒排索引约 30 分钟。

## Evidence and Limits

- 主要主张（简单双编码器微调即可超过 BM25，不需要额外预训练）有 5 个数据集上的 top-20/100 对比和训练方案消融支撑，证据较扎实。BM25 参数在 dev 上调过（b=0.4, k1=0.9）。
- SQuAD 是反例。作者解释为问题在看过段落后撰写所以词汇重叠高，且仅 500 多篇文章、分布偏；这是推测，文中未做验证。
- 端到端对比 ORQA/REALM 并不完全等价：DPR reader 用 100 词段落、最多 100 个候选（NQ 最优 k=50），ORQA 用 288 word pieces、5 段落。作者承认吞吐影响不易衡量；k=10 时 NQ EM 为 40.8，据称与 ORQA 的 5 段落设置大致可比。第一个块的基线数字直接抄自原论文。
- 「检索精度越高，端到端越好」只是整体趋势，SQuAD 反例也在其中。
- 联合训练消融（Appendix D）仅在 NQ dev 上做，固定 passage encoder，EM 39.8，与流水线相同，不能推广为联合训练无用。
- 跨数据集泛化只测了 NQ 训练、迁移到 WQ/TREC 一组（top-20 69.9/86.3，低于微调模型 3–5 点，仍高于 BM25）。
- 定性分析（Appendix C, Table 7）只给两个例子：DPR 能做语义匹配，但抓不住「Thoros of Myr」这类稀有关键短语。
- 文中未见多随机种子或显著性检验；每项结果看起来是单次运行。训练在八块 32GB GPU 上完成。
- 仅限英文 Wikipedia、事实型问题、extractive QA，评估口径是答案字符串是否出现在段落中。

## Open Questions

- 答案字符串匹配式的 top-k accuracy 会把含答案但不支持答案的段落算对，它与真实相关性差多少，文中没有分析。
- DPR 在稀有实体和精确关键词上的弱点，是编码器容量问题还是训练负例问题？文中只给了两个例子，并留给 BM25+DPR 混合来补。
- Figure 1 的样本效率结论仅来自 NQ dev；对其他数据集和领域外语料是否同样成立，没有验证。

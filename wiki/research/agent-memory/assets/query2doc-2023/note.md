---
title: "Query2doc: Query Expansion with Large Language Models"
updated: 2026-10-09
---

# Query2doc: Query Expansion with Large Language Models

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文、参考文献、附录 A–C，含 Table 1–11）；Figure 1、2 只有文字提取，Figure 2 的数值部分可读；表格基本完整。

## Summary

问题：检索 query 往往很短、有歧义、缺背景，稀疏检索存在词汇鸿沟；传统 query expansion（RM3 等）在主流数据集上收益有限，强 dense retriever 也基本不用扩展（§1）。

方法：用 4-shot prompt（指令 "Write a passage that answers the given query:" + 从训练集随机抽的 4 个 query-passage 对）让 text-davinci-003 生成 pseudo-document d'，再与原 query 拼接（§2）。
- 稀疏检索：把 query 重复 n=5 次再拼接 d'，用 BM25（式 1）。
- 稠密检索：`query [SEP] d'` 作为新 query（式 2），训练和推理都用扩展后的 query；两种训练设置：DPR（BERT-base，仅 BM25 hard negative）和在 SimLM / E5-base 上做 cross-encoder 蒸馏（式 3、4）。
- 与 PRF 的区别：扩展信号来自 LLM 记忆的知识，不依赖初次检索质量；与 HyDE 的区别：HyDE 零样本、只用 pseudo-doc 的 embedding。

主要结果（Table 1）：
- BM25 MS MARCO dev MRR@10 18.4 -> 21.4；TREC DL19 nDCG@10 51.2 -> 66.2；DL20 47.7 -> 62.9，无需任何微调。BM25+RM3 基本无提升（15.8 / 52.2 / 47.4）。
- DPR：MRR@10 33.7 -> 35.1，DL19 64.7 -> 68.7，DL20 64.1 -> 67.1。
- 带蒸馏的强模型增益变小：SimLM 41.1 -> 41.5（DL19 +1.5，DL20 +1.9）；E5-base+KD 40.7 -> 41.5（DL19 +0.6，DL20 +1.8）。
- 零样本 BEIR 五个数据集（Table 2）：BM25 全部提升（DBpedia +5.7，Trec-Covid +6.6）；SimLM 在 NFCorpus、Scifact 分别 -0.6、-2.9；E5 在 Scifact -2.9。

分析（§4）：
- LLM 规模（Table 3）：BM25 在 DL19 上 1.3B 52.0、6.7B 55.1、davinci-001 63.5、davinci-003 66.2、GPT-4 69.2。
- 只用 pseudo-doc 比 query+pseudo-doc 差很多，甚至低于纯 query（Table 4：48.7 vs 66.2 vs 51.2，DL19）。
- 不同标注数据比例下 DPR 增益稳定在约 1 个点（Figure 2）。
- 作者发布 text-davinci-003 的生成结果（Hugging Face 数据集）。

## Evidence and Limits

- 设置：LLM 为 text-davinci-003，temperature 1，最多 128 token；评测 MS MARCO dev、TREC DL19/20、BEIR 的 5 个低资源集；指标 MRR@10、R@50、R@1k、nDCG@10；稠密检索 4 卡训练，基础实现用 Pyserini（§3.1，Appendix A）。
- 训练 query 的 pseudo-doc 也要调用 LLM，共约 550k 次 API 调用，约 5k 美元（Appendix A）。
- 随机性：3 次重复下 BM25 结果 DL19 64.8±1.14、DL20 60.9±1.63（Table 10），均低于 Table 1 所报的 66.2 / 62.9，即主表数字偏乐观，近 1–2 个点内的差异应谨慎对待。
- 稠密检索上"增益被蒸馏削弱"是论文自己承认的；SimLM/E5 的对比里，部分 +0.1~+0.4 的差异没有显著性检验。
- 对 BM25 的强提升主要来自 TREC DL 的长尾实体型 query（作者人工检查得出，§3.2），论文未提供量化。
- OOD 结果混合，作者归因为"训练与评测分布不匹配"，没有验证（§3.2）。
- 事实错误：LLM 生成可能错（Table 5 中 Monk 主题曲年份错误，Table 9 中传真号错误），论文只做个例展示。Appendix B 让 GPT-4 自检改写，几乎无改动，效果无提升（Table 8）。
- 延迟：LLM 调用 >2000ms，BM25 索引检索由 16ms 升到 177ms（Table 6，Limitations）；LLM 延迟依赖服务负载，未精确测量。
- 数据泄漏：MS MARCO / TREC 的内容可能出现在 LLM 预训练语料中，论文没有讨论。GPT-4 只在附录和 Table 3 的 BM25 实验中出现，未用于主实验。

## Open Questions

- LLM 记忆泄漏（评测集内容进入预训练）对 BM25 大幅提升贡献多少？论文没有控制实验。
- 对稠密检索，增益来自 pseudo-doc 提供的事实，还是仅仅是更长的输入？没有拆分实验；也没有与用检索结果做 PRF 的强 LLM 基线对比。
- 如何在不显著增加延迟与成本的前提下使用（蒸馏小模型、按 query 选择性扩展），以及 pseudo-doc 出错时如何检测，论文留作未来工作（few-shot 按语义相似度选取也只是提议）。

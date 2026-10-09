---
title: "SPLADE v2: Sparse Lexical and Expansion Model for Information Retrieval"
updated: 2026-10-09
---

# SPLADE v2: Sparse Lexical and Expansion Model for Information Retrieval

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（短文，约 4 页加参考文献）。表格可读；图 1、图 2 只有坐标轴和图例文字，曲线数据缺失，只能引用正文给出的数字。

## Summary

问题：BM25 等 bag-of-words 第一阶段检索有词汇不匹配问题；dense 检索缺少显式词项匹配。作者在 SPLADE（SIGIR'21）基础上做三处改动，让稀疏表示在效果或效率上更好（§1）。

方法：
- SPLADE 用 BERT 的 MLM logits 给词表（30522 个 WordPiece）中每个词打重要性，经 log(1+ReLU) 饱和后按输入 token 聚合，再用 FLOPS 正则（Paria et al.）控制稀疏度，查询和文档用不同的正则权重 λ_q、λ_d（§3.1）。
- 池化：把对输入 token 的求和改为取最大（式 6），得到 SPLADE-max（§3.2）。
- SPLADE-doc：只编码文档，查询不做扩展和加权，得分为查询词在文档表示中的权重之和，文档侧可全部离线预计算（§3.3）。
- 蒸馏：先用 Hofstätter 等的三元组训练 SPLADE 和 cross-encoder（MiniLM-L-12），再用第一步的 SPLADE 挖更难的负例，用 cross-encoder 打分，以 Margin-MSE 从头训练，得到 DistilSPLADE-max（§3.4）。

结果（Table 1，MS MARCO dev MRR@10 / R@1000；TREC DL 2019 NDCG@10 / R@1000）：
- 原 SPLADE 0.322 / 0.955；0.665 / 0.813。
- SPLADE-max 0.340 / 0.965；0.684 / 0.851。
- SPLADE-doc 0.322 / 0.946；0.667 / 0.747。
- DistilSPLADE-max 0.368 / 0.979；0.729 / 0.865。
- 对比 dense：TCT-ColBERT 0.359，TAS-B 0.347，RocketQA 0.370（dev MRR@10）。
- 对比 sparse：doc2query-T5 0.277，COIL-tok 0.341，DeepImpact 0.326。

效率（§4.2–4.3）：SPLADE-doc 在平均每文档 19 个非零权重时 MRR@10 为 29.6，与 doc2query-T5 相当。DistilSPLADE-max 约 4 FLOPS 时 0.368，约 0.3 FLOPS 时 0.35（均来自正文）。

BEIR 零样本（Table 2，NDCG@10，13 个数据集子集含 MS MARCO）：平均（all）ColBERT 0.455，BM25 0.440，TAS-B 0.435，SPLADE sum 0.446，max 0.460，distil 0.500；distil 在 11 个数据集上最好（§4, Table 2）。

## Evidence and Limits

- 配置：DistilBERT-base 初始化，Adam，lr 2e-5，batch 124，最大长度 256，4 张 V100 32GB，150k 步（SPLADE-doc 50k 步取最后检查点），λ 取 1e-1 到 1e-4，用二次增长的 λ 调度。索引是基于 Python 数组的自制实现，用 Numba 并行检索（§4）。
- 数据：MS MARCO passage（约 8.8M 段落，dev 6980 条查询）和 TREC DL 2019（43 条查询）。只比较第一阶段，不与 MS MARCO 榜单上的 re-ranker 结果比。
- 表中 SPLADE 变体是在 λ 网格中选效果最好且 FLOPS「合理」的模型，选择标准没有量化；基线数字取自原论文，训练设置不同。
- 效率指标是 FLOPS 估计（约 100k 条 dev 查询上经验估计），没有给出真实延迟、索引大小或与 BM25 / ANN 的墙钟时间对比。「更高效」的说法主要靠 FLOPS 和非零项数支撑。
- BEIR 只用了「现成可获取」的子集，排除了 CQADupstack、BioASQ、Signal-1M、TREC-NEWS、Robust04。BEIR 对比的 baseline 是 ColBERT、调参后的 BM25、TAS-B，且 TAS-B 等的数字来自滚动榜单。DistilSPLADE-max 用了 MS MARCO 上训练的 cross-encoder 蒸馏，BEIR 上的优势有多少来自蒸馏而非稀疏表示，没有单独拆分。
- 摘要说 NDCG@10「提升超过 9%」：0.665 到 0.729 相对约 9.6%，和表一致。
- max 池化为何有效，只给了「更像 SPARTA / EPIC」的解释，没有消融或分析。
- 单次运行，无随机种子方差或显著性检验；论文没有附录。

## Open Questions

- 蒸馏版在 BEIR 上的大幅领先，有多少来自 cross-encoder 教师，有多少来自稀疏表示本身？论文没有给出非蒸馏 dense 模型同样蒸馏后的对照。
- 真实倒排索引（非 Python 数组原型）下，SPLADE-max 的查询扩展项数是否会让延迟超过 BM25 很多？FLOPS 与实际延迟的关系没有验证。
- 为什么取最大值比求和更好，以及它对词扩展质量和可解释性（扩展词是否更合理）的影响没有分析。

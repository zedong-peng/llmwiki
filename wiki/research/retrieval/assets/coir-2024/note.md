---
title: "CoIR: A Comprehensive Benchmark for Code Information Retrieval Models"
updated: 2026-10-09
---

# CoIR: A Comprehensive Benchmark for Code Information Retrieval Models

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文、附录 A–F、表格）。图 2、图 4 为乱码/仅有数值残片，图 3 箱线图只能看到轴标签，这些图的细节未能核对。

## Summary

CoIR 是面向代码检索的评测基准。作者认为现有基准（CodeSearchNet、CoSQA、XCodeEval）任务单一、领域窄，且很多模型已在 CodeSearchNet 上过拟合，也缺统一评测框架 (§1, Table 1)。

构成：10 个数据集，4 大任务、8 个子任务、14 种编程语言 (§3, Table 2, Figure 1)。
- Text-to-Code：APPS（竞赛题到解答）、CoSQA（web query）、Synthetic Text2SQL。
- Code-to-Text：CodeSearchNet 反向使用，用代码检索 docstring。
- Code-to-Code：CodeSearchNet-CCR（把函数按 40%–70% 字符切成前后两段，前段作 query、后段作文档）、CodeTransOcean-DL 与 -Contest（跨框架/跨语言的等价代码）。
- Hybrid：StackOverflow QA、CodeFeedback-ST、CodeFeedback-MT。
- 其中 CodeSearchNet-CCR 与 StackOverflow QA 为新建，其余 8 个来自已有数据，经去重、对齐过滤和人工检查 (附录 A、F)。语料规模 1K 到 1M，query 平均词数 37 到 4.4K。
- 发布 pip 安装的评测包，数据格式对齐 BEIR/MTEB，指标为 NDCG@10（另提供 MAP、Recall、Precision）。

评测 10 个检索器：BM25、Contriever、E5-base、BGE-base、GTE-base、UniXcoder、BGE-M3、E5-Mistral(7B)、OpenAI-Ada-002、Voyage-Code-002 (Table 3)。
- 平均 NDCG@10：Voyage-Code-002 56.26 最高，E5-Mistral 55.18，E5-base 50.90，OpenAI-Ada-002 45.59，BM25 29.79。
- 没有单一模型在所有任务上最优；APPS 上最高仅 26.52（Voyage），CosQA 上 E5-base 32.59 反而高于 E5-Mistral 的 31.27。
- 效率 (Table 4)：E5-Mistral 单样本 embedding 延迟 1840ms，其余开源 base 模型约 7.4–7.8ms；索引大小从 0.3GB 到 2.3GB。
- 输入长度 (Table 5)：GTE 从 512 扩到 4k，CodeFeedback-MT 38.20 升至 51.32（表中 512 栏数字与正文所述有出入，见下）；BGE-M3 在同一数据集上反而从 33.46 降到 27.49。
- 与 BEIR 排名对比 (Table 6)：E5-Mistral 两边都第一，GTE-Base 在 BEIR 第 2、在 CoIR 第 6。
- 过拟合分析 (§5.5, Figure 4)：多数模型在 CodeSearchNet 上得分明显高于 CoIR，OpenAI-Ada-002 和 Voyage-Code-002 差距最大，E5-Mistral 差距最小。

## Evidence and Limits

- 主结果表是单次评测、无方差或显著性检验；10 个模型里只有 E5-Mistral 为 LLM 基座，"LLM 检索器更有潜力、能减轻过拟合"的结论基本只靠这一个模型支撑。
- "过拟合"是由 CodeSearchNet 与 CoIR 的得分差推断的，没有查证这些模型的训练数据是否含 CodeSearchNet，也没有排除两个基准难度本身不同。该论断证据偏弱。
- 设置：单张 Tesla V100 32GB，Faiss IndexFlat；开源模型 query/语料均截断到 512 token，Voyage 因 TPM 限制 query 截断到 256。对 APPS、CodeFeedback-MT 等平均长度超过 1000 词的数据集，截断本身会压低分数，模型间比较混有长度因素 (§4, §5.3)。
- Table 5 的文字与表有对不上之处：正文称 GTE 在 CodeFeedback-MT 与 StackOverflow QA 上分别从 38.20、64.36 升到 51.32、78.63，而表中 GTE(512) 对应数字为 28.48 与 62.71；原文未解释。Table 3 中 GTE-Base 的 CodeFeedback-MT 也是 28.48。
- 数据细节不一致：正文表 2 称 CodeTrans-Contest 测试 query 446，附录写 221；APPS 正文 3.8K，附录 3,765；StackOverflow QA 正文称 19,931 对，split 为 13,951/3,986/1,994。数据量统计存在小幅差异。
- 每个 query 只有一个标注正确文档（作者在 Limitations 承认），不覆盖多相关文档情形；数据全为英文；不含版本、元数据等多维检索需求。
- 部分数据集（CodeFeedback、Synthetic Text2SQL）为 LLM 合成；Text2SQL 与 CodeFeedback 的标注质量依赖原数据集，"人工检查"的具体规模和一致性未量化。
- 难度筛选 (附录 A.1, Table 7)：HumanEval、XCodeEval、MBPP 因 NDCG@10 超过 90 被剔除，选择依据是模型分数，带有一定循环性。
- 结果表中的 Voyage、OpenAI 为闭源 API，版本和时间固定性无法核实。官方代码在 GitHub (CoIR-team/coir)。

## Open Questions

- 把 CodeSearchNet 与 CoIR 的分差解释为过拟合，如何排除任务难度差异和训练数据泄漏的影响？
- 512 token 截断下的排名，在长输入完整编码时是否仍成立（Table 5 只测了 GTE 与 BGE-M3 两个模型）？
- 单正例标注下，同一 query 的其他合理文档被当作负例，对 NDCG@10 的排名有多大影响？

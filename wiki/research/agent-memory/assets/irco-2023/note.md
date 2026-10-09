---
title: "Interleaving Retrieval with Chain-of-Thought Reasoning for Knowledge-Intensive Multi-Step Questions"
updated: 2026-10-09
---

# Interleaving Retrieval with Chain-of-Thought Reasoning for Knowledge-Intensive Multi-Step Questions

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文、Limitations、附录 A–G 含 prompt 清单）。图 3–9 只有标题，没有数值，相关数字取自正文和表格；表格文本基本完整。

## Summary

问题：多步 open-domain QA 里，下一步该检索什么取决于已推出的内容，只用问题做一次检索（OneR）不够（§1）。

方法 IRCoT（§3）：先用问题检索 K 段作为基础集合，然后交替执行两步。
- Reason：LM 基于问题、已收集段落和已生成的 CoT 句子，生成下一句 CoT，只取第一句。
- Retrieve：以最新一句 CoT 作为 query（BM25，Elasticsearch）再取 K 段，并入集合。
- 当 CoT 出现 "answer is:" 或达到 8 步时停止；段落总数上限 15。全部收集到的段落交给独立的 reader（Direct 或 CoT prompting）作答。
- 全程 few-shot：每个数据集人工写 20 条 CoT，抽 3 组各 15 条做 demonstration；没有训练。

设置（§4）：HotpotQA、2WikiMultihopQA、MuSiQue、IIRC，各取 100 条 dev 调参、500 条 test；模型为 GPT3（code-davinci-002）和 Flan-T5 base/large/XL/XXL。指标为 15 段上限下的 gold 段落 recall，以及答案 F1。

主要结果（§5）：
- 检索 recall 相对 OneR：Flan-T5-XXL 提升 7.9 / 14.3 / 3.5 / 10.2 点（HotpotQA / 2Wiki / MuSiQue / IIRC）；GPT3 提升 11.3 / 22.6 / 12.5 / 21.2 点。
- QA F1 相对 OneR：Flan-T5-XXL 提升 9.4 / 15.3 / 5.0 / 2.5；GPT3 在前三个数据集提升 7.1 / 13.2 / 7.1，IIRC 无提升（作者推测 GPT3 参数里已有相关知识，NoR 分数与之接近）。
- OOD（demonstration 来自另一数据集，不含 IIRC）趋势一致（图 5、6）。
- 人工标注每个数据集 40 题的 GPT3 CoT：含事实错误的题数 NoR > OneR > IRCoT；相对 OneR，HotpotQA 少 50%，2Wiki 少 40%（图 7）。
- 小模型：IRCoT 在 0.2B 上 recall 就优于 OneR；QA 上除最小模型外都优于 OneR；Flan-T5-XL（3B）+ IRCoT 超过 175B GPT3 + OneR（图 8、9）。
- 表 1/3 与已发表的 LLM ODQA 系统对比：GPT3 IRCoT QA 的 EM|F1 为 HotpotQA 49.3|60.7，2Wiki 57.7|68.0，MuSiQue 26.5|36.5。MuSiQue 最优；HotpotQA 上 DSP 高 2.0 点，2Wiki 上新版 DecomP 高 2.8 点（附录 C）。

## Evidence and Limits

- 核心结论（交互式检索优于一次检索）有较多证据支持：4 个数据集、2 类模型、IID 与 OOD、多种模型规模，结果为 3 组 demonstration 的均值±标准差（表 4）。
- 检索指标是自定义的"固定预算最优 recall"：检索结果无排序、每步数量可变，所以不用 Recall@k / MAP（脚注 7）。K 和 M 在 dev 上以该指标选取，IRCoT 与 OneR 都做了调参。
- 语料是自行构造的：2Wiki、MuSiQue 用各数据集所有段落（含干扰段）合并，IIRC 用提到的 Wikipedia 页面，且打乱段落顺序（附录 A）。语料远小于完整 Wikipedia（MuSiQue 139,416 段，2Wiki 430,225 段，HotpotQA 5,233,329 段），检索难度因此与真实开放域不同。
- IIRC 需要特殊处理：始终提供主段落，先让模型生成 3 个页面标题再在其中检索（附录 B），并非同一套流程。
- 与 SelfAsk、ReAct、DecomP、DSP、RECITE 等的对比作者自己声明"非 head-to-head"：LLM、语料、API、测试子集都不同（附录 C）。"SOTA"一说只在此限定下成立。
- 事实性评估只有每数据集 40 题、人工标注，样本小，无标注者一致性说明。
- reader 选择因模型而异（Flan-T5 用 Direct，GPT3 用 CoT）；表 6 显示去掉独立 reader 后 GPT3 在部分数据集持平或略升（如 2Wiki 70.4 vs 68.0）。
- 局限（作者所述）：依赖基础 LM 的 few-shot CoT 能力（小于 20B 的模型不常见）；需要长上下文；每句 CoT 调用一次 LM，成本更高；code-davinci-002 已被弃用，GPT3 部分难以复现，Flan-T5 部分可复现。
- 本次未运行任何代码，所有数字均来自论文文本。

## Open Questions

- 检索 query 只取最近一句 CoT，没有利用更早的推理或做 query 改写；对跨多句依赖的问题影响多大，论文没有消融。
- 固定每步取 K 段、总量 15 段的做法对不同跳数的问题是否合适？论文提到可动态决定何时检索，但未实验。
- 在 IIRC 上检索明显更好却没有提升 QA，说明检索 recall 与答案质量的关系取决于模型的参数知识；论文没有进一步验证这一解释。

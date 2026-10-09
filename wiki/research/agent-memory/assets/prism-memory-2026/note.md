---
title: "PRISM: Pareto-Efficient Retrieval over Intent-Aware Structured Memory for Long-Horizon Agents"
updated: 2026-10-09
---

# PRISM: Pareto-Efficient Retrieval over Intent-Aware Structured Memory for Long-Horizon Agents

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文 §1–5、参考文献、附录 A–E，含 prompts 与统计表）。图 1–4 只有提取出的文字标签，无法看到图形本身；arXiv 2605.12260v2，作者 Peng, Wan, Liu, Sun（SMU / OSU / Fudan）。

## Summary

问题：长程对话 agent 的记忆系统同时受答案准确率和 answer-side context 成本约束。作者认为现有方法分别只优化其中一头（写入侧抽取、检索侧压缩、图结构记忆），"高准确率 / 低 context"的角落是空的（§1, Fig. 1）。

方法：training-free 的检索侧框架，跑在已构建好的图记忆上。图有四层节点（Entity / FacetPoint / Facet / Episode），belongs_to 层级边加五种关系边（semantic、temporal、causal、evolution、involves_entity）；由 gpt-4o-mini 在写入时做 schema-guided 抽取，每 5 个 chunk 异步做一次 causal 归纳（§3.2, 附录 C.1）。查询时四个模块：
- N4 Adaptive Intent Routing：关键词正则 -> prototype 向量匹配 -> LLM 分类的三级级联，得到 temporal / causal 等意图（§3.6）。
- N2 Query-Sensitive Edge Cost：意图匹配时把 temporal / causal 边的代价乘 0.5，evolution 在 temporal 意图下乘 0.7（Eq. 4–5）。
- N1 Hierarchical Bundle Search：四层各做 FAISS top-30 取锚点，枚举 8 种路径模板（5 backbone + 3 relation-bridge），每个 Episode 取最小路径代价，取 top-K=10 候选（Eq. 2–3, 附录 C.2）。
- N3 Evidence Compression：一次 LLM 调用，只看 Episode summary（截 400 字符），给 0–10 分后取 top-M=5（Eq. 6, 附录 D.2）。

结果（LoCoMo cat 1–4，1,540 题，gpt-4o-mini 作答和判分，Table 1）：PRISM overall 0.831，每查询 2,023 tokens。同协议基线：Full Context 0.481 / 26,031；MAGMA 0.688 / 3,370；Mem0 0.669 / 1,764；Mem0g 0.684 / 3,616。四个子类别均最高。不同协议参考：M-Flow 0.818 / 2,588；PRISM 换 gpt-5.5 作答 0.891；Mem0 商业平台 0.916 / ~7,000。

消融（Table 2, §4.4）：去掉 N3，ER@5 从 0.694 降到 0.627，context 从 2,023 升到 4,108，judge 0.831 -> 0.825；去掉 N1 或 N2，所有指标几乎不变；加 N4 后 42.3% 的查询不用 LLM 分类，judge 0.833（Table 3–4）。

## Evidence and Limits

- 设置：单一 benchmark（LoCoMo 10 段对话，不含 cat 5），答案模型、N3、N4 fallback、判分器、写入抽取全是 gpt-4o-mini，embedding 为 all-MiniLM-L6-v2，seed 42。未提硬件和延迟。基线按作者协议重跑，超参固定在测试前（附录 C.3）。
- 摘要和引言称"typed relation paths 与 LLM 压缩都必要、不可互相替代"，但 §4.4 和附录 E.1 显示 N1、N2 消融在 ER@5、judge、token 上无差异（pre-rerank 候选集 1,536/1,540 题完全一致）。作者自己的解释是 LoCoMo 大多可由锚点直接找到：50 题 multi-hop 人工标注中仅 3 题（6%）真需要两跳桥接，73.4% 的题只引用一条证据，并推测 N1/N2 在 MuSiQue、HotpotQA 上会有用，但没有验证。所以 headline 提升实际来自"稠密锚点检索 + 摘要粒度 + LLM rerank"，图路径部分在本文中没有证据。
- N3 对 judge 的影响不显著（CI [−2.08, +0.91] pp）；它的作用是把 context 减半、提高 top 位置的 evidence recall。"13x context 缩减"是对 Full Context 而言，与 Mem0（1,764）相比 PRISM 反而更长。
- 与 Mem0 / MAGMA 的差距（+14 pp 左右）没有做配对显著性检验，只有内部消融有；基线在作者自己的 prompt 和抽取协议下运行，实现是否最优不清楚。Full Context 在 26K tokens 下仅 0.481，低于所有检索方法，这点值得与其他文献对照。
- Table 1 的 PRISM 默认不含 N4（Table 2 里 N4 是"+"），但摘要把 N4 列为四个核心组件之一。N3 在 §3.5 写成"选 top-M"，附录 D.2 实际是逐条打分再取 top-M。
- 写入阶段每个 chunk 的 LLM 抽取成本未计入"context cost"；比较只看查询时 token。semantic 边在 LoCoMo 配置中被关闭（C.1）。
- 作者承认的局限（附录 A）仅限于对话记忆，未覆盖含工具调用的 agent 轨迹。论文未给出代码链接。

## Open Questions

- 图结构（N1/N2）在真正需要桥接的数据集上是否有收益？论文只在 LoCoMo 上证明了"无损"，没有正向证据。
- 去掉 N3 后 judge 只掉 0.6 pp，说明 4K tokens 下 gpt-4o-mini 已够用；压缩的价值取决于 token 计价与作答模型，换更强或更弱的作答模型时 N3 的收益如何变化？
- 结果对写入侧抽取质量（gpt-4o-mini 的 FacetPoint / causal 边）有多敏感？所有实验共用同一份 ingest checkpoint，未测。

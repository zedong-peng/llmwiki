---
title: "LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory"
updated: 2026-10-09
---

# LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文、参考文献、附录 A–E，附录主要是 prompt 与补充表，仅做了浏览）。图 3、5、6 的数值来自文本抽取，部分排版错乱。注意：BibTeX 记录标注的是 Think-on-Graph 2.0（arXiv 2410.10813 实际对应 LongMemEval，bib 的标题与 code 字段与论文正文不符），本笔记以论文正文为准。

## Summary

问题：已有长期对话记忆基准多为人-人对话、历史仅数千 token、能力覆盖窄（缺跨 session 综合、知识更新、助手侧信息召回），无法检验带记忆的聊天助手。

基准：LongMemEval 含 500 道人工整理的问题，考察五项能力：信息抽取、多 session 推理、时间推理、知识更新、拒答（§3.2）。共 7 种题型，其中 30 道由其他题型改写为 false premise 题用于拒答。构造流程：164 个用户属性本体 → Llama 3 70B 生成背景段落 → 专家改写问题并拆成 evidence statements → 自对话生成 evidence session（用户间接透露信息），约 70% 的 session 经人工编辑 → 在 ShareGPT、UltraChat 和其他自对话 session 中穿插 evidence session，形成长度可配置的历史（类似 needle-in-a-haystack）。标准设置：LongMemEval_S（约 115k token）和 LongMemEval_M（500 个 session，约 1.5M token）。评测用 GPT-4o 作 judge，称与人工一致率超过 97%（§3.3，Table 6）。

难度验证（§3.4，图 3）：对 ChatGPT 和 Coze 抽取 97 题、配 3–6 个 session 的短历史，由人工逐轮交互。GPT-4o 版 ChatGPT 准确率 0.577，Coze 0.330，而同一 GPT-4o 读完整历史为 0.918。长上下文 LLM 在 S 设置下相比 oracle（只给 evidence session）下降 30%–60%，如 GPT-4o 0.870→0.606，Llama 3.1 70B 0.744→0.334。

统一框架（§4）：记忆视为 key-value 库，分 indexing、retrieval、reading 三阶段，四个控制点（value、key、query、reading strategy），并把 9 个已有系统放入该框架（Table 2）。

设计发现（§5，检索器为 Stella V5 1.5B，索引抽取用 Llama 3.1 8B）：
- Value：按 round 存储比按 session 存储在 GPT-4o 读者下更好；摘要或 fact 替换原文会因信息丢失而变差，但 fact 对多 session 推理题有帮助（图 5）。
- Key：用 value 拼接抽取的 user fact 作为 key，recall@k 平均提高 9.4%，最终准确率提高 5.4%（Table 3）。单独用 fact/keyphrase/summary 作 key 并不更好。
- Query：对时间敏感问题用 LLM 抽取时间范围过滤，时间推理子集的 recall 平均提高 11.3%（round）和 6.8%（session），需要 GPT-4o 级别的抽取器，Llama 8B 基本无增益（Table 4）。
- Reading：Chain-of-Note 加 JSON 结构化输入，在 oracle 检索下比最差组合高最多约 10 个点（图 6）。

## Evidence and Limits

- 主要实验模型：GPT-4o、Llama 3.1 70B/8B；附录 Table 8 另有 5 个模型。检索器对比在附录 E.2。贪心解码，最大生成 800 token。
- 商业系统对比仅 97 题、历史约短 10 倍，且是单次人工交互（2024 年 8 月），样本小，ChatGPT/Coze 的内部机制未知（Table 2 中多项标为未知），"记忆系统不如离线阅读"的结论只能说明这一设置。文中还观察到 ChatGPT 会覆盖关键信息，Coze 常漏记间接给出的信息（附录 B）。
- 数据主要为 LLM 自对话加人工编辑，问题与 evidence 由 3 名内部专家完成；干扰 session 来自 ShareGPT/UltraChat，文中称冲突极少，但未量化。用户模拟 LLM 以间接方式透露信息，真实性未与真实用户对话对照。
- judge 是 GPT-4o，与人工一致性按题型各抽 30 题报告，文中承认单 session 偏好题和拒答题略有偏差。拒答题仅 30 道。
- 设计结论多为单一检索器、单一数据集上的消融；各增益幅度以平均值给出，未见显著性检验或方差。Table 3 中 round 与 session 的绝对数字互有高低，"round 更优"主要依赖 GPT-4o 读者，Llama 8B 下与 session 持平。
- 错误分析（附录 E.5）：检索正确但生成错误占全部样本 15%–19%，占错误样本 40%–50%，说明读取阶段仍是瓶颈。
- 伦理部分自述的局限：记忆缺少删除操作、可能被注入恶意内容。

## Open Questions

- 自对话生成加人工编辑的历史，与真实用户长期对话在信息分布和干扰类型上差多少？基准分数能否迁移到真实使用？
- 在 M 设置（1.5M token）下，各设计的收益是否保持？正文大部分消融给出的是 M 的结果，但商业系统只在远短于 S 的历史上测过。
- 时间感知查询扩展依赖强 LLM 抽取时间范围；对相对时间表述错误时，过滤会直接丢掉证据，文中未量化这种失败的代价。

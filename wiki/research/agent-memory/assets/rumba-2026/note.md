---
title: "RUMBA: Russian User Memory Benchmark"
updated: 2026-10-09
---

# RUMBA: Russian User Memory Benchmark

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文、局限、附录 A–G 及全部表格）。图（Fig. 1–16）只有标题，内容未提取；Table 26 分类表可读。

## Summary

问题：现有长期对话记忆基准（LoCoMo、LongMemEval、Mem-Gallery）以英文为主，题型分类是扁平的，时间推理被当作单一题型，基本不覆盖"遗忘"；俄语没有专门的对话记忆基准（§1–2, Table 1）。

构建：85 段带时间戳的 user–assistant 对话，每段约 34 万字符、12–85 个 session、180–998 条发言，共 1,543 个 QA（§3.3, Table 3）。用户发言由 26 名人工撰写，助手回复由 GigaChat Max 实时生成（§3.4）。题目按三条正交轴标注：语义（Extraction 6 类 / Reasoning 10 类 / Abstention）、单 session 或多 session、时间相关与否；时间题再标 explicit / implicit / 无时间表达（§3.2, Table 2）。其中 DeleteInfo 题测"用户要求忘记后应答无此信息"。另提供自动翻译（gpt-4.1-mini）加人工校验的英文版（§3.4）。

评测：full-context 7 个模型（gpt-5.4、claude-sonnet-4.6、grok-4.1-fast、gemini-3.1-flash-lite、gpt-4.1-mini、minimax-01、llama-4-maverick）与 6 种检索式记忆（simple RAG、mem0、mem0g、graphiti、cortex、memOS）。检索式方法统一取 top-10 记忆，由 gpt-4.1-mini 回答。俄语用 POLLUX 判分，英语用 DeepSeek-R1（§4）。

主要结果（Table 5–7）：
- 总体准确率（RU/EN）：gpt-5.4 83.60/83.99，claude-sonnet-4.6 78.61/81.98，grok-4.1-fast 76.22/79.59；检索式最好为 simple RAG 68.89（RU）、memOS 69.99（EN）；mem0g 最低，34.93/35.26。
- 固定回答模型后，gpt-4.1-mini full-context 比 Agent/RAG 平均高 4.28（RU）和 8.64（EN）。逐方法看结果不一：cortex、memOS、simple RAG 在俄语显著高于它，graphiti 和 mem0g 低 17–28 点。
- 难度主因是跨 session：多 session 比单 session 低 20.7–23.0 点，两类系统一致（Table 7, 12）。
- implicit 时间表达明显更难：full-context 下 explicit 与 implicit 相差约 30 点（Table 17）。
- 时间题比非时间题低 2.1–7.2 点，效应较小，俄语 Agent/RAG 校正后不显著（Table 13）。
- Extraction 比 Reasoning 容易 9–14 点；Abstention 接近饱和，约 82–84（Table 19, 20）。
- 附录 G 用 claude-sonnet-4.6 做单模型画像：多 session 且时间题最差（RU 66.88），Reasoning 俄语 65.16、英语 76.77。

## Evidence and Limits

- 统计处理较认真：问题级 bootstrap 置信区间，Holm 校正，对比按 family 均值做。但"family 均值"是方法的简单平均，混入了 mem0g 这类很差的系统（时间对比中已排除 mem0g）。
- Full-context 与 Agent/RAG 的 family 差距（RU +11.86、EN +15.11，Table 11）不控制回答模型，主要差在模型强弱；控制后差距缩小，部分方法反超（Table 6）。正文已区分这两种比较。
- 俄英两种语言用不同判分器，作者承认跨语言差异可能来自判分器校准。附录 E.3 人工检查：POLLUX 偏严（错误里约 64% 低估），DeepSeek-R1 偏松（约 77% 高估，把错答判为正确 21 例）。主文只引用 POLLUX 与专家 ρ=0.704，没有给出两个判分器与人工的整体一致率。
- 英文版是机器翻译，仅抽 10%（9 段）人工评分，总分 0.88（Table 9）；证据 session 和 QA 另有三人校验，非证据 session 未校验，直接沿用 0.88。
- 数据规模小：85 段对话；Extraction 题占多数（1,079/1,543），Reasoning 310，Abstention 154；explicit 时间题仅 102，implicit 69，所以时间表达的结论置信区间很宽。作者自认对超长上下文模型的压力不足。
- "lost-in-the-middle"仅用 session 级代理检验，未发现显著效应（Table 22, 23）；作者说明不能代表 token 级位置效应。
- 检索式方法固定 top-k=10 与单一回答模型，不做检索设计的消融（作者列为局限）。排除了 Qwen3.5 系列（供应商内容审查报错）和无足够上下文的俄语模型，所以没有俄语专用模型的结果。
- 助手回复由 GigaChat 生成，部分框架（mem0g 通过托管 API）无时间戳，设置不完全对等。
- 摘要称"first benchmark"仅限俄语对话记忆这一范围，证据上可接受；Table 1 对其他基准的"No"判断来自作者自己的归类。

## Open Questions

- 判分器不同导致的跨语言差异有多大？同一判分器下两种语言的结果是否仍是 full-context 英文略高、Agent/RAG 俄文略高？
- 对话中人类写用户发言、GigaChat 写回复，这种单一助手来源是否影响不同模型的得分？论文没有与纯合成对话对比。
- 各系统在 DeleteInfo 上的表现拆开是什么样？Abstention 与 DeleteInfo 的结果在正文没有单独报告。

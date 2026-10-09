---
title: "Quantifying Label-Induced Bias in Large Language Model Self- and Cross-Evaluations"
updated: 2026-10-09
---

# Quantifying Label-Induced Bias in Large Language Model Self- and Cross-Evaluations

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文、参考文献、附录 A–D 的表格）。图 1–11 在文本提取中只剩图注，数值只能从附录表格和正文引用核对；表格序号在文中有 I–IV 与 A1–A4 两套标记。

## Summary

问题：LLM 当评审时，是否会被"作者标签"左右，而不是按内容打分。作者区分了 self-preference（偏爱自己的输出）和 label-induced bias（标签本身影响评分）。

方法（§III）：
- ChatGPT-4o、Gemini 2.5 Flash、Claude Sonnet 4 用同一个 prompt 各写 10 个标题的约 200 词博客，共 30 篇。
- 三个模型各自作为评审，在四种条件下给所有博客打分：无标签、真标签、两种循环错标（场景 1：ChatGPT 标成 Gemini、Gemini 标成 Claude、Claude 标成 ChatGPT；场景 2 反向循环）。
- 两种评分：(a) "best" 投票占比；(b) Coherence/Informativeness/Conciseness 0–10 分，再换算成百分比。

主要结果（§IV，附录表）：
- 无标签：三者都略偏爱自己。ChatGPT 自选 50.0，Gemini 12.0，Claude 46.7；Gemini 的输出只得 7–12（表 A1）。
- 真标签：Claude 得 54.0–60.0（Claude 自评 60.0），Gemini 对 Claude 打 0.00、对 ChatGPT 打 1.34、自评 11.32（表 A2）。
- 错标：Gemini 评审把"Gemini 文本冒充 Claude"选到 51.35（真标签下它自己的文本只有 11.32）。场景 2 中 ChatGPT 文本标成 Claude 时，Gemini 给 60.7，Claude 给 56.02；Claude 文本标成 Gemini 时，Claude 评审给 18.48（真标签 60.0）。
- 摘要称偏好投票最多摆动 50 个百分点，点数评分的换算摆动 ≤12 个百分点，Informativeness 最敏感，Conciseness 最稳定（§IV、§V）。
- 结论：Claude 标签加分、Gemini 标签扣分；建议盲评和多模型共识评审。

## Evidence and Limits

- 样本很小：10 个标题、30 篇文章、每个条件的评审次数未说明。"best"占比出现 44.66、1.34 这类数，说明可能有重复采样或平均，但文中没写，也没给方差、置信区间或显著性检验。
- 点数评分的差距多在 0.1–1.2 分（如 Gemini 评审对 Claude 文本的 Informativeness，无标签 7.44，真标签 7.90，表 A5/A6），没有重复评分的噪声估计，难以判断小差异是否可靠。
- 只有一个 prompt、一组评审提示词（评审提示词原文未给出）、三个具体模型版本，未提位置随机化、temperature、生成与评审是否多次运行。作者自己通读后称博客"很难排序"，说明内容质量差异本来就小，这会放大标签效应，也限制了推广。
- 标签含义的混杂：标签既代表"品牌声望"，也可能触发"这是我自己的"识别，二者没有分开。错标设计是循环置换，没有"随机/中性标签"（如 Model A/B）对照，所以"Claude 标签有声望加成"是推断，不是直接测得。
- 摘要说 "Gemini 的自评在真标签下崩塌"，但表中 Gemini 自评从 12.0 到 11.32（文中 -0.7 pp），本来就低；真正的大幅下降是 Gemini 文本被其他评审打到 0–1.34。该说法与自己的数据不完全一致。
- 正文数字有对应错位：如"Gemini 对 Claude-as-Gemini 从 11.32 升到 51.35"，按表 A3 应是 Gemini-as-Claude。"Claude 标签总是加分"也有反例：场景 1 中 ChatGPT 评审对 Gemini-as-Claude 只给 21.17。
- "标签身份压过文本质量"的结论只有部分被支持：错标后排名确实大幅变化，但所有评审都显示 Gemini 文本在无标签下也最低，没有排除真实质量差异与标签效应叠加。
- 相关工作中混入脑肿瘤、肺癌检测等与主题无关的引用（自引），论证价值低。未提供代码或数据。

## Open Questions

- 把标签换成中性代号，或随机分配模型名，Claude/Gemini 的非对称是否仍在？这决定它是品牌先验还是自我识别。
- 每个条件的评审重复次数是多少？换更多题目和多个评审 prompt 后，50 pp 的摆动和 ≤12 pp 的差异是否仍成立？
- 在这类文本上，Gemini 的低分有多少来自标签、多少来自真实写作差异？论文没有给出分离方法。

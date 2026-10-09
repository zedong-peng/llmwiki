---
title: "MGRetrieval: Memory-Guided Reflective Retrieval for Long-Term Dialogue Agents"
updated: 2026-10-09
---

# MGRetrieval: Memory-Guided Reflective Retrieval for Long-Term Dialogue Agents

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文、附录 A–C、提示词）。附录中的图 6/7 以及图 3/4 的坐标数值被抽取成乱码，只能读到零散数字，未据此引用；Table 4/6 完整可读。

## Summary

问题：长对话 agent 的记忆检索多为 one-shot，证据不足或引入冗余；MemR3 一类反思式检索由 LLM 根据有限证据生成下一轮 query，路径不稳定且慢 (§1)。

方法 (§3)：
- 存储：不压缩原始记忆，用 GPT-4o-mini 为每条记忆（一轮对话）抽关键词，并与已有词表匹配，建立 keyword -> memories 的映射。
- 检索：LLM 从词表中为 query 选 n 个关键词，枚举所有 l 个关键词的组合，形成 keyword pyramid；每个组合取其关键词对应记忆集合的交集；从最高层（最具体）往最低层（最宽）遍历，同层按关联记忆数降序。
- 每轮只保留本轮新记忆（去掉前几轮已出现的，RMR），与上一轮的 critical memories、上一轮答案和 query 一起交给主 LLM；LLM 输出答案、是否接受（sufficient）标志和 critical memories。直到 sufficient、达到最大轮数或 pyramid 用完。
- 最后一步 answer rewriting：只用最终 critical memories 和用户提示词规范答案格式（例如把 "three days ago" 改成 "26 April 2022"）。

设置：pyramid 深度 4，最多 4 轮。LoCoMo 上用 Qwen2.5-14B 和 Qwen3-14B 作主 LLM，Table 4 另列 GPT-4o-mini 与 GPT-4o。GVD 用 DeepSeek-R1 当评审。

结果：
- Table 1（两个 Qwen 模型的加权平均）：F1 42.77、BLEU-1 36.69，对比 MemoryOS 38.48/33.02、MemR3 35.30/30.46、FULL 39.27/32.92。摘要的"8.91% F1、11.11% BLEU-1"即相对次优基线。
- Table 4 分类别：在 Qwen2.5-14B 上 F1 43.61，比 MemoryOS 38.55 高；GPT-4o 上 47.08 vs MemR3 46.19，差距很小。Multi Hop 上 MGRetrieval 常低于 MemoryOS（如 Qwen2.5 的 32.37 vs 34.68）。
- Table 2（GVD）：Acc 93.0 / Corr 91.5 / Cohe 92.5，与 MemR3、MemoryOS 基本持平，作者承认已近饱和。
- Table 3 效率：主 LLM 平均 2.23 次调用、5799 token、6.98 秒；MemR3 为 3.27 次、5169 token、12.77 秒。MGRetrieval 不用主 LLM 重构记忆库，关键词抽取用 GPT-4o-mini，每条记忆 2 次调用约 1176 token，每个 query 1 次约 786 token。
- 消融 (Table 5, Qwen2.5-14B)：Round 1（相当于 one-shot）full F1 24.33，到 Round 4 为 41.07，再加 rewriting 为 43.61；去掉 RMR 分数无明显变化，但 token 增多（最终 7618 vs 5799）。

## Evidence and Limits

- 主要对比只在 LoCoMo 上有区分度，且只有一次运行，没有方差或显著性检验。GVD 上无优势。
- 文字称 MemoryOS 是"最强基线"，但 Table 1 里 FULL 的 F1（39.27）才是最高的基线，数字与叙述不完全一致；8.91% 的计算对应 42.77/39.27。
- 效率说法需要谨慎读：Table 3 里 MGRetrieval 的单次回答 token（5799）高于 MemoryOS（4537）；"比 MemoryOS 少 16.96% 主 LLM token"是整个 pipeline（含记忆重构）的口径，且不含 GPT-4o-mini 的关键词开销（作者单独列出）。A.5 称相对 FULL 省 86.63% token，而 Table 3 的 5799 vs 21332 算出来约 73%，口径不明。
- Rewriting 提示词包含 LoCoMo 风格的相对时间归一化示例（A.4 称参考了 LoCoMo 指南），带来约 2.5 F1；作者称该模块不检索新证据、不影响公平性，但基线未获得同等的格式后处理，这部分增益与检索无关。
- 基线按各自论文/默认配置运行，RAG 为 top-20 bce-embedding；未与其他基于 BM25、混合检索或图结构的检索控制方法比较。
- 作者自述局限：只是检索控制策略，未与记忆整理/遗忘结合；LLM 判断"够了"不保证证据完整，尤其 multi-hop；仍依赖多轮 LLM 调用；关键词质量决定 pyramid 质量，建议结合向量相似度。
- 硬件为单张 24GB GPU；LLM 走官方 API，temperature 0。关键词匹配全靠 LLM，可扩展到更大记忆库的情况未测。

## Open Questions

- 关键词 pyramid 对 LLM 抽取与匹配质量的依赖有多大？若换成向量检索做路径，增益是否仍在？文中无此对照。
- 组合数 C(n, l) 随选出的关键词数增长，实际每层组合数和每题检索次数的分布没有给出。
- 去掉 rewriting（并对基线做同样的格式后处理）后，相对 MemoryOS/MemR3 的优势还剩多少？

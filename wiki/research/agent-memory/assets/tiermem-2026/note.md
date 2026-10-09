---
title: "From Lossy to Verified: A Provenance-Aware Tiered Memory for Agents (TierMem)"
updated: 2026-10-09
---

# From Lossy to Verified: A Provenance-Aware Tiered Memory for Agents (TierMem)

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文、附录 A–F、参考文献）。图 1 只有文字残片，表格基本可读；附录末尾未见额外实验。

## Summary

问题：长期对话 agent 的记忆通常在写入时压缩成摘要或事实，此时还不知道未来的 query 要什么，于是出现"不可验证的遗漏"（如把 severe peanut allergy 压成 dietary preferences）。反过来，每次都读原始日志又贵又慢。作者把这称为 write-before-query barrier，并把检索看作推理时的 evidence allocation：用最便宜的足够证据回答（§1）。

方法（§2–3，附录 A–B）：
- Tier-2 是不可变的定长原文页（约 1000 token），Tier-1 是摘要索引，每条摘要带指向 Tier-2 页 id 的 provenance link。实现上基于 Mem0 的向量库，关掉了它的图构建。
- 查询先取 Tier-1 top-k，由小 router（ANSWER / ESCALATE 二分类）判断摘要是否足够。不够则优先读被链接的原文页，再做最多 Tmax=3 轮的 integrate-plan 检索（语义检索加 BM25 关键词检索）。
- Verified write-back：升级后把带证据引文的事实写回 Tier-1（ADD / UPDATE / SKIP），并继承 provenance。
- Router 训练：先用 GPT-5 的 thinking+action 做 SFT 蒸馏（只保留与 oracle 标签一致的样本），再用 GRPO，奖励为正确性减去 cost 和"误升级"惩罚。标签来自 hindsight：summary-only 答对记 S；summary 错而 raw 对记 R；两者都错的丢弃。训练数据取自 MemoryAgentBench 的 LRU 子集（2,000 条）。

结果（backbone 为 GPT-4.1-mini）：
- LoCoMo（Table 1）：raw-only 0.873，summary-only 0.755，router 0.851。输入 token 为 7398 对 3396（另有 router 584），延迟 17.18s 对 6.76s。摘要型基线 UOR 为 14.7%–23.3%。
- LongMemEval（Table 2）：raw 0.808，summary 0.678，router 0.752。Mem0 的 UOR 为 29.6%。
- Router 训练（Table 3）：zero-shot 0.806，SFT 0.831，SFT+GRPO 0.851。后者升级率 39.0%，hard-case recall 71.7%，router 开销约 678 token/query。GPT-4.1-mini 做 router 同为 0.851。
- Provenance 消融（Table 4）：Linked 85.1 对 No-Linked 83.6，Acc.@R 为 81.7 对 77.5；两者 route 一致的 1,306 条里 Linked 多对 6 条（C.2）。
- Replay 三轮（Table 5）：No-Recall 写回下 S-Traffic 932→1,245，平均 token 3,958→2,419，延迟 5.14s→3.39s，准确率 0.851→0.845。

## Evidence and Limits

- 摘要里的"token 减少 54.1%"只比较 QA 阶段的 3396 与 7398，没把 router 的 584 input 算进去。含 router 为 3980，约省 46%；Table 3 说的"总成本省 51%"是另一口径。延迟 60.7% 则已含 router。
- 准确率是 LLM judge 打分，judge prompt 明确要求宽松（"be generous"）。LoCoMo 多数对比只有一次运行，没有方差或置信区间。
- Router 在 LoCoMo 上比 raw-only 低 2.2 个点，LongMemEval 上低 5.6 个点；后者摘要路径和 raw 路径之间仍有明显差距，"nearly matches" 的说法在 LongMemEval 上偏强。
- Table 1 里 Mem0、LightMem 等基线的延迟、输出 token 口径与自家系统不同（如 O-mem 延迟 1.16s 却有 544 输出 token），不同系统的实现和部署环境未说明，跨系统效率比较需谨慎。MemR3、GAM 的 UOR 缺失。
- UOR 的定义（答案在原文中但没进摘要）依赖 judge 与 oracle 路径，没有人工核验。
- 一致性问题：§5.5.2 说 Summary-Only 错误为 378 条（24.5%），§5.6 又分析 431 条 Summary-Only 错误，未解释差异。
- Write-back 在主结果中被关闭；Table 5 的 replay 在同一批评测 query 上重复，写回内容来自这些 query 自己的升级过程，所以"摘要路径覆盖率上升"部分反映的是对已见问题的记忆，不等于对新问题的泛化。真正的在线写回没有评测（附录 A.7 末尾自述）。
- Router 错误（附录 E）：S→R 的 false cache hit 61 例，R→S 的过度升级 371 例；Summary-Only 错误上的 false cache hit 为 148 例。升级后仍答错的也很多（240/431），说明瓶颈有一部分在 raw 路径的检索和抽取。
- 硬件、GPU 型号、router 基座模型规模、生成器之外的 reranker 型号在正文中未写明；只给了 LoRA 超参（rank 64，SFT 5 epoch，GRPO 6 epoch）。
- 数据集仅 LoCoMo 与 LongMemEval，均为对话式问答；router 训练集与测试集来源不同，这点有利于泛化论证，但没有跨域或更长历史的测试。

## Open Questions

- Router 的 hindsight 标签依赖保守的 judge，这是否导致系统性过度升级（R→S 错误远多于 S→R）？校准后成本还能降多少？
- Write-back 在真正在线、query 分布漂移、事实被后续对话推翻时是否仍然"verified"？目前只有 replay 证据，没有冲突更新或过期处理的评测。
- LongMemEval 上的差距主要来自 router 误判，还是来自 raw 路径检索（提供的 provenance 只是 warm start）？论文只在 LoCoMo 上做了错误剖析。

代码：论文摘要给出 https://github.com/FreedomIntelligence/Tiermem 。

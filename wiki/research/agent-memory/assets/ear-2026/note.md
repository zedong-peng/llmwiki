---
title: "Exploratory and Assimilating Reflection: Reflective Recall Cycle for Long-term Memory (EAR)"
updated: 2026-10-09
---

# Exploratory and Assimilating Reflection: Reflective Recall Cycle for Long-term Memory (EAR)

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文、参考文献、附录 A–D 含 prompt）。图 3–6 只有标题和正文描述，曲线数值未能读到；无官方代码链接。

## Summary

问题：LLM agent 的外部长期记忆检索依赖静态 retriever，离线微调 reranker 不能适应分布漂移；Tan et al. 2025 的在线 RL reranker（REINFORCE，用 LLM 引用反馈更新）样本效率低，早期甚至比静态 retriever 差（§1）。

方法（§3，Alg. 1）：冻结 retriever 取 top-K 候选（K=20），在其上加残差线性 adapter（Wq、Wm 各 d×d，约 1.18M 参数 for Contriever，Table 10）。
- Exploratory Reflection：对每个 query 做 T=4 轮 slate 选择（s=5），把候选当 bandit arm，打分 = 0.4×相关性 − 0.3×与已选冗余（max cosine）+ 0.3×UCB（α=0.5）；外部 critic（LLM）对每条记忆给 ±1 引用标签，更新 arm 统计。
- Assimilating Reflection：把 (query, 候选, 多轮平均反馈) 存入 Experience Buffer，按 query 相似度取 top-4 做 replay（Gumbel 采样 slate，重算 reward），与当前 query 的 feedback-weighted 排序损失合并更新 adapter（λrep=1，baseline b=0.5）。
- 推理可关闭 Explorer（仅 adapter，无 critic 调用）或开启（多 T−1 次 critic 调用）。

结果（§4，Table 2，3 次平均，s=5，80% query 训练 / 20% 评估）：LongMemEval 上 Contriever 的 Recall@5 从 62.37 升到 80.28（摘要的 +17.9），RL baseline 为 59.71；LoCoMo 上 42.60 → 55.06（+12.5），RL baseline 25.97。J（LLM-as-judge）LongMemEval 54.84 → 65.23，LoCoMo 45.45 → 54.44。样本效率（§4.5.2，Fig. 3/4）：关闭 Explorer 测试时，EAR 在 80 个训练 query 后超过静态 retriever；按 LLM 调用数对齐，baseline 要约 1400 次才超过静态，EAR 约 320 次（即“少 77%”）。消融（Table 3）：adapter baseline 54.12，只加 Explorer 训练 69.91，只加 Buffer 66.32，二者 72.80，测试时再开 Explorer 80.28。多记忆库实验（§5，Table 4/5，Contriever）：episodic（对话）+ semantic（observation）混合时 J 从 47.73 升到 59.09；retriever 偏向 observation，EAR 的 top-5 更均衡。

## Evidence and Limits

- 设置：retriever 为 Contriever / Stella-1.5B / GTE-7B；答题与（部分）critic 用 GPT-5 Mini；数据 LongMemEval-S（500 query）与 LoCoMo（1,540 query，去掉 Adversarial）；turn 级粒度；评估集是 20% query（LongMemEval 约 100 条）。
- 主实验的 critic 是概率模拟器（precision 88 / recall 86，由 Tan et al. 报告校准），从 gold 引用按概率生成标签，不是真实 LLM（§4.4，A.2）。真实 GPT-5 Mini 只在 Table 9 做了单次运行：Recall@5 70.1 vs 模拟 72.8（precision 78）。噪声鲁棒性（Fig. 5）也基于模拟，最差 P=R=70 仍高于静态 retriever。
- “consistently outperforms”并不完全成立：GTE 在 LongMemEval 上 EAR 62.90 低于 retriever 68.89（Table 2）；Stella 在 LoCoMo 的 J 仅 63.09 vs 57.02。作者解释为 adapter 参数 2d² 随维度增长，训练 query 不够（B.5），属假说，未做 LoRA 等验证；只给了 Fig. 7 的趋势描述。
- 成本：Explorer 开启时每 query 延迟 16.88s，对比 retriever 1.80s、adapter 2.30s（Table 8，不含答题）；最佳 Recall@5 需要付出 T−1 次额外 LLM 调用。
- Recall@5 的 80.28 在 LongMemEval 上低于独立的 MonoT5-base reranker（82.20）；MonoT5+EAR 为 85.50（LoCoMo：61.46 → 62.08，Table 10）。即 EAR 单独不及强 cross-encoder，增益在其上较小，且该实验里 MonoT5 分数作为额外信号喂给 Explorer，细节简略。
- “对比 RL baseline”只有一个（Tan et al. 2025）；该 baseline 在多数设置低于静态 retriever，说明复现/调参条件（400 个训练 query 的低资源）可能对它不利。超参（T、replay batch）只在 LongMemEval 上扫（Table 6）。
- 异构记忆结论中，Open Domain 的 J 不变，作者归因于参数知识；几何分析（Table 12）仅 10 条手写 query，只是定性。
- 论文自述局限：replay 采样策略仍可改进；更大 retriever 增益变小。

## Open Questions

- 用真实 LLM critic 在线训练的完整结果（多次运行、更多 query）是否仍保持对 RL baseline 的优势？目前只有一次运行的单个数字。
- 增益有多少来自 Explorer 的多轮反馈聚合（降噪、去冗余）本身，而非 replay？Table 3 显示 Explorer 训练贡献更大，但没有在相同 critic 调用预算下与更强的非 RL 方法（如直接微调）对比。
- Experience Buffer 是否会随长期使用增长、过时或被分布漂移污染？论文没有评估真实时间漂移，也没有缓冲区容量或淘汰策略的实验。

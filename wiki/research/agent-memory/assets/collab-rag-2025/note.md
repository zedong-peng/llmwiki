---
title: "Collab-RAG: Boosting Retrieval-Augmented Generation for Complex Question Answering via White-Box and Black-Box LLM Collaboration"
updated: 2026-10-09
---

# Collab-RAG: Boosting Retrieval-Augmented Generation for Complex Question Answering via White-Box and Black-Box LLM Collaboration

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文、参考文献、附录 A–D）。Figure 3/4/5 只剩坐标轴文字，柱/曲线数值读不到；Table 1 排版尚可但部分格为空（—）。BibTeX 里的标题与论文标题不一致，以论文为准。

## Summary

问题：多跳 QA 中，单步检索会带入无关上下文，黑盒 LLM 自行分解问题（无训练）效果有限；微调黑盒 LLM 不现实。

方法（§4）：把"检索器 + 黑盒 LLM reader"当作环境，训练一个白盒小模型（Qwen-2.5-3B / Llama-3.1-8B）做 query decomposer，把问题拆成带 #k 引用的子问题序列。每个子问题单独检索（Dragon-Plus，top-10），由 LLM 逐步回答并汇总。奖励只看终局：格式奖励（子问题是否正确引用前序答案）× 准确率奖励 0.5·(EM+Acc)（式 2）。训练流程：对每题采样 N=5 个分解，best-of-N 作正例、worst-of-N 作负例（奖励全相同的题丢弃）；先用 reward≥0.5 的样本做 rejection-sampling SFT 热身，再做 3 轮迭代 DPO（β=0.5，用上一轮模型作 reference）。训练数据为 HotpotQA/MusiQue/2WikiMQA 训练集共 10000 题，训练时 reader 只用 GPT-4o-mini，8×A100。

结果（Table 1，EM 为主指标）：
- GPT-4o-mini reader：3B 在 HotpotQA 51.6 / MusiQue 25.4 / 2Wiki 63.0 / Bamboogle 47.2 / StrategyQA 82.0；8B 为 53.0 / 26.4 / 63.2 / 52.8 / 81.6。同 reader 下 vanilla RAG 为 41.8 / 11.4 / 37.2 / 23.2 / 78.6，GPT-4o-mini 自分解为 46.6 / 24.2 / 59.0 / 45.6 / 76.8。
- GPT-4o reader（训练时未见）：8B 在 HotpotQA 54.4、MusiQue 29.0、2Wiki 67.2、Bamboogle 63.2；GPT-4o 自分解为 52.2 / 27.8 / 62.2 / 62.4。
- 摘要称平均优于基线 1.8%–14.2%（§5.3 另有 6.6%），3B 平均比 GPT-4o 分解高 0.7%。
- 对比蒸馏（Figure 4）：用 GPT-4o-mini/GPT-4o 的分解蒸馏到 Qwen-2.5-3B，文中称 Collab-RAG 一致更好。
- 迭代轮数（Figure 5b）：前 1–2 轮 DPO 有增益，第 3 轮趋平。
- 偏好算法（Table 4）：ORPO、SimPO 在 HotpotQA 上约低 3–4 EM，DPO 最稳。

## Evidence and Limits

- 设置：5 个多跳数据集；HotpotQA/MusiQue/2Wiki 只评测 dev 前 500 题，StrategyQA 和 Bamboogle 全量。Bamboogle 仅 125 题量级（文中未给规模），单点差异噪声大。解码为贪心，每个设置看起来只跑一次，无方差或显著性检验。
- 基线公平性：作者对自己跑的基线在 k∈{5,10,15,20} 中取最优；表中大量基线数字来自原论文（不同模型、检索器、语料），文中自己标为 "For Reference Only"。RAG-Star、RAG-Gym、RQ-RAG 标记需 GPT-4 系列蒸馏；RQ-RAG 原设定有 gold passage，与此处设定不同。
- 消融（Table 2）：去掉格式奖励在两个骨干上都下降；但"w/o iterative DPO"在 Qwen-3B 的 HotpotQA 上 52.0 高于完整方法 51.6，Llama-8B 的 2Wiki 上 64.2 高于 63.2；"w/o Accuracy Reward"在 2Wiki 上 Qwen 持平。差异多在 1 EM 以内，文中"贡献提升"的说法仅部分被数字支持，迭代 DPO 的收益主要体现在 Llama-8B 的 HotpotQA（47.6→53.0）。
- 检索器（Table 3）：换成 COCO-DR/E5/GTE 后各数据集有升有降，Qwen-3B 在 HotpotQA 上换 COCO-DR/GTE 反而降 1.2；"mostly outperforms 最佳基线"成立，但并非每格都优于默认检索器。
- 参数量论断：Figure 5c 称 3B 超过冻结 32B、8B 超过冻结 72B。对照附录 Table 7（冻结模型直接提示，GPT-4o-mini reader）：Qwen-32B 的 EM 为 52.0 / 25.4 / 62.0，3B 为 51.6 / 25.4 / 63.0，实际接近持平；Qwen-72B 在 HotpotQA（55.6）和 2Wiki（67.0）上高于 8B（53.0 / 63.2），只在 MusiQue、Bamboogle 上低于。该说法只在跨五个数据集的平均意义上可能成立，正文没给出明细。
- 与 GPT-4o 自分解相比，3B 在 Bamboogle 上更低（60.0 vs 62.4），"超越"的幅度小（平均 0.7）。
- 与过程奖励/搜索类方法（RAG-Star、RAG-Gym）的对比只覆盖部分数据集，作者称方法正交、可组合，但未实验。
- 局限（文中提到）：未研究单步 QA；仅离线迭代 DPO，在线 RL 留作未来工作；格式奖励存在模型仍写成 "Question 1" 而非 "#1" 的失败情形（脚注 1）。训练和主要评测都用 GPT-4o-mini/GPT-4o 作 reader，开源 reader 只在 Figure 3 中测过 Llama-3.1-8B 和 Qwen-2.5-14B。
- 代码：摘要给出 https://github.com/ritaranx/Collab-RAG/。

## Open Questions

- 增益里有多少来自"拆成多次检索"本身，多少来自 DPO 学到的分解风格？SFT-only 与 RAG w/ 冻结分解已经接近，迭代 DPO 的净增量在若干格内小于噪声。
- 奖励只用终局答案；分解正确但 reader 答错（或分解错但猜对）会产生噪声偏好对，论文没分析偏好对的质量，也没有与人工或 gold 分解的对比。
- 泛化到训练分布外的 reader 和语料（如更强的开源 reader、非 Wikipedia 语料）以及更深的推理链（>3–4 跳）时是否稳定，文中证据有限。

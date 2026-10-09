---
title: "Preference Leakage: A Contamination Problem in LLM-as-a-Judge"
updated: 2026-10-09
---

# Preference Leakage: A Contamination Problem in LLM-as-a-Judge

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文 + 附录 A–I）；图中数值（Fig 2/3）因 PDF 提取而部分错乱，附录 Fig 4–6 的数字可读；参考文献仅略读。

## Summary

问题：当合成数据的生成模型 M_G 与评测用的 judge M_J 相关时，judge 会偏向由 M_G 数据训练出的 student 模型，抬高其得分。作者称之为 preference leakage，类比 data leakage（§1, §3）。

定义：定义 student 的得分在 M_G 与 M_J 相关时高于不相关 judge（式 1）。相关性分三种：同一模型、继承关系（fine-tune 或用对方输出训练）、同一模型家族（§3.3）。

度量：提出 preference leakage score (PLS)。对一对 student (i, j)，比较各自"自己的 judge"给的 win rate 与两个 judge 的平均 win rate 的相对差，再取平均（式 5–6，附录 C.2 有算例）。

主实验（§4）：
- generator/judge 为 GPT-4o、Gemini-1.5-flash、LLaMA-3.3-70B。
- student 为 Mistral-7B-v0.1 和 Qwen-2.5-14B 的 base 版本，用 UltraFeedback 抽出的 30k prompt 的合成回复做 SFT。
- 在 Arena-Hard 和 AlpacaEval 2.0 上两两比较。
- Table 1：GPT-4o/Gemini 对的平均 PLS 为 23.6%（Mistral）和 27.9%（Qwen）；LLaMA/Gemini 对为 16.4% 和 21.9%；GPT-4o/LLaMA 对接近 0（-0.1%、1.7%）。

进一步分析（均只在 Mistral-GPT-4o vs Mistral-Gemini 上做，§5）：
- 学生尺寸：更小的 student 平均 PLS 更高（Fig 2a，附录 Table 14）。
- 数据混合：PLS 随合成数据占比上升，没有明显阈值（Fig 2b）。
- 相关性类型（Table 2）：同模型 23.6%，继承 19.3%/22.3%，同家族同系列 8.9%，不同系列 2.8%。
- 学习方法（Table 3）：SFT 23.6%，DPO 5.2%，ICL -2.7%。
- 真实榜单（Table 4）：以 LMArena 与 AlpacaEval 2.0 的排名差衡量，Vicuna 系列为 1.33，GPT-4 Preview 的 egocentric bias 为 1.00。
- judge 识别 student 输出的准确率接近随机（Table 5，29.8%–53.2%），但 BERT 能以 82.4% 的准确率区分三个 student 的回复，说明风格/格式特征确实被学到。
- 去除风格/格式/措辞（Table 6）：风格和格式的改写使 GPT&Gemini 的 PLS 由 17.5% 降到约 9–10%，措辞影响小。
- 缓解（§5.8, Table 7）：在人工标注的偏好数据上，contextual calibration 将 Error Bias 从 17.8 降到 7.3，prompting、paraphrase、auto calibration 无效甚至更差。

附录补充：重复三次方差很小（Table 9）；换 prompt 后 PLS 基本保持正（Table 10）；bootstrap 检验，强泄漏的对显著（Table 11）；中文设置同样有泄漏（Table 12）；加入 Claude-3.5 作 judge 后现象类似（Table 13）；100 条人工标注（标注者一致率 78.6）显示 Gemini 对其 student 偏向最强（Fig 4）。

## Evidence and Limits

- 主结论（强相关的 judge 偏向自己的 student）在 Table 1 中、对 Gemini 相关的两个 pair 上很稳；但 GPT-4o 与 LLaMA-3.3 这一对没有泄漏，说明效应取决于具体模型对。作者称"大多数 pair"有泄漏，实际是 6 个 pair 中 4 个。
- 数据与规模：每个 student 为单次 SFT（3 epoch, lr 1e-5, 8×A100, LLaMA-Factory）；只有 Table 9 做了 3 次重复，且仅限 Mistral。bootstrap 只对 Arena-Hard 的 500 条 prompt 重采样，没有覆盖训练随机性。
- PLS 是作者自定义的归一化量，没有与已有指标对照；PLS 的阈值含义和绝对大小缺乏参照。
- 多数分析（§5.1–5.5）只在一个 pair、一个 student 上做，"普遍"这一说法外推较多。
- 区分"偏好泄漏"与"egocentric bias / 风格相似"并不严格：judge 偏向的是与自己风格相近的输出，Table 6 说明风格和格式是主要载体，但没有直接测 judge 的偏好是否来自"关系"本身而非表面特征。
- §5.4 真实榜单分析样本极少（Vicuna 三个模型、一个 judge），排名差 1.33 对 1.00 不足以支持"更强"的结论；作者自己也承认缺乏 distillation 元数据。
- §5.6 文字与图自相矛盾：先说主观问题偏差更大，结尾却写"在客观问题和维度上更显著"，应是笔误；另外 Fig 3b 中被称为"客观"的 completeness 与"主观"的 fairness 的划分未论证。
- §5.8 缓解实验用的是人工标注数据上的 Error Bias（新指标），与主实验的 PLS 不同；contextual calibration 需要额外 held-out 集，作者称为 preliminary。
- Table 5 中 LLaMA-3.3 pairwise 29.8% 低于随机，作者仍解读为"约等于随机"。
- 作者声明用 GPT-5 / Gemini 2.5 Pro 润色文字。代码地址 https://github.com/David-Li0406/Preference-Leakage，正文与摘要中给出，本文未验证其内容。

## Open Questions

- 泄漏究竟由"关系"本身（共享训练分布/偏好）造成，还是只由可被改写移除的表面风格造成？Table 6 只给出部分支持，改写后仍有残余泄漏。
- 在更大规模、经过 RLHF 的 student，或多个 generator 混合的现实流水线中，PLS 是否仍明显？目前数据混合实验只混了一个 generator 与人工/多源数据。
- 有没有不依赖额外标注集的检测或缓解方法？judge 自身无法识别 student，而 contextual calibration 依赖人工标注。

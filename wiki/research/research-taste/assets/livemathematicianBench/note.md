---
title: "LiveMathematicianBench: A Live Benchmark for Mathematician-Level Reasoning with Proof Sketches"
updated: 2026-10-09
---

# LiveMathematicianBench: A Live Benchmark for Mathematician-Level Reasoning with Proof Sketches

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文、附录 A–G）。图 1、3–8 的坐标轴文字被抽成乱码，只能依据正文和图注读数字；附录 F.1 引用了损坏的 "Figure ??"；各模型完整成绩表没有给出（只有正文提到的几个数）。

## Summary

问题：静态数学 benchmark（GSM8K、MATH、竞赛题）已被污染或饱和；RealMath 取自 arXiv，但只保留易于自动验证的定理类型。本文用 post-cutoff 的 arXiv math 论文持续生成研究级五选一选择题（§1）。

方法（§2，7 个阶段）：
- 按月从 arXiv API 取 math.* 论文，解析 LaTeX 源码，用规则（只看 Introduction 里的主定理）加 LLM agentic 兜底抽取一条主定理，展开宏和引用，并回收上下文。
- LLM 从论文自身提炼 proof sketch，并把定理分到 13 种逻辑形式（Implication、Universal、Existence、Inequality/Bound、Biconditional、Classification/Bijection、Independence 等，Table 1）。
- 每类定理有专用 prompt 生成题干和正确选项（"strongest statement" 式题干）。
- 干扰项由 proof sketch 引导生成：controlled perturbation、semantic weakening、semantic strengthening、property confusion；其中一个是 "weaker-true" 选项，附录 G 里的 prompt 要求干扰项必须违反 sketch 里的某个关键约束。
- Substitution-resistant 设计：对一部分题，把正确选项换成元选项 "其余选项之一正确，但可证明更强结果"，使模型无法靠逐项代回题干或排除法作答。
- 0–8 分质量 rubric（阈值 5）、"仅题干"可答性过滤、用一个前沿模型做 hardness calibration（保留该模型答错的变体）。
- 评测分两种：不给 sketch，给 sketch（dual-mode）。

结果（§3–4）：最终 hard split 共 177 题，来自 2025-11 至 2026-02 四个月。
- Gemini-3.1-pro-preview 总体 43.5%，GPT-5.4 (high) 41.8%，GPT-5.4 (medium) 41.2%（附录 F.2）。随机基线 20%。
- 原始选项子集上 Gemini 67.4%、GPT-5.4 52.2%；substitution-resistant 子集上 Gemini 17.6%（低于随机），GPT-5.4 29.4%–30.6%（Fig. 5a）。
- 给 sketch 后 GPT-5.4 (high) 41.8%→53.7%（+11.9 pp），Gemini 43.5%→57.1%（+13.6 pp）（Fig. 5b）。
- 不同逻辑类别上模型强弱不同：Gemini 在 equivalence 和 bijection 上较强，GPT-5.4 在 implication、universal、inequality 上较强（Fig. 4a）。
- 成本：Gemini 平均约 15.3k completion tokens，GPT-5.4 (high) 约 7.0k，(medium) 约 3.8k；Qwen3.5-397B-A17B、Kimi-K2.5 用更多 token 但成绩居中（Fig. 8）。

## Evidence and Limits

- 题目由 LLM 生成，人工验证是抽样：最终 177 题被审阅，上游各环节每类约 10 例抽查，且明说不是对源论文结论的逐一独立验证（附录 B）。"所有干扰项都是假的" 的主要依据是 prompt 设计加一个例子（Example 6），没有给出错误率统计。
- "Contamination-free by construction" 只靠论文提交时间晚于模型 cutoff；文中没列各模型的 cutoff。一些定理（如 Nešetřil–Rödl 1976 的结果在 Example 13 中出现）是旧结果，论文中重述的。
- Hardness calibration 用某个前沿模型的答错记录挑选变体，所用模型没有点名；这会偏向压低该模型系列的成绩，也使 "far from saturated" 的结论部分来自选题本身。
- Substitution-resistant 子集占比、各子集题数、各模型完整成绩没有在文本中给出。"Gemini 低于随机"的 17.6% 没有置信区间；全文没有重复采样或方差报告（评测脚本支持 --n，但结果未说明用了几次）。
- 正确选项被替换成元选项后，真实定理不在选项里，题目实际变成 "识别所有选项都弱于/偏离真值"，答对依赖对 "更强结果存在" 的判断；作者把它解读为"有限形式的 conjecturing"，这一解读文中没有直接检验。
- Sketch 来自源论文本身（有的例子只复述了引言里几句话，如 Example 5），且同一份 sketch 也用于生成干扰项；因此 sketch 带来的提升既可能是策略使用，也可能是 sketch 与干扰项构造相关。文中没有做控制实验。
- sketch 评测只对少数最强模型做（预算原因，附录 E）；每类别样本很小（少于 10 的类别并入 Other），类别层面的结论偏弱。
- 设置：评测 prompt 要求逐步推理并把答案写在 \boxed{}，选项确定性洗牌；模型含 Gemini-3.1-pro-preview、GPT-5.4（medium/high）、Qwen3.5-397B-A17B、Kimi-K2.5、GPT-oss-120b 等；硬件未说明。
- 未验证：论文中的图表数值均未能复算。

## Open Questions

- Substitution-resistant 子集上的分数有多少来自数学推理，有多少来自对"元选项"格式本身的偏好或惯性？缺少对元选项频率的控制实验。
- 去掉 sketch 的情况下，若干扰项不再由 sketch 构造，难度和 sketch 增益会如何变化？
- 按月更新后，不同月份的难度和分数波动（Fig. 4b 显示 2026/01 较高）是来自模型 cutoff 还是来自论文分布，尚未分开。

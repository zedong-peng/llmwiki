---
title: "Softermax: Hardware/Software Co-Design of an Efficient Softmax for Transformers"
updated: 2026-10-09
---

# Softermax: Hardware/Software Co-Design of an Efficient Softmax for Transformers

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（arXiv 2103.09301v1，DAC 2021）。图（Fig. 1、Fig. 3 算法伪代码、Fig. 4、Fig. 5）只有图注，无数据点；Table I–IV 文本可读。

## Summary

问题：Transformer 中 softmax 占运行时间的比例随序列长度增大（Fig. 1，BERT-Large 在 Volta GPU 上），而现有加速器主要针对矩阵乘。softmax 低效有两个原因：指数函数需要大 LUT / 泰勒展开；数值稳定版本需要先扫一遍求 max，多一次访存和延迟（§II.B）。

方法（§III）：
- 底数替换：把 e^x 换成 2^x。作者称仍满足 softmax 的三个性质（概率分布、可微、非线性放大差异），硬件上省掉 e 到 2 的换底乘法。
- 低精度定点：指数、累加、除法全用定点。位宽见 Table I（输入 Q(6,2)，Unnormed 值 Q(1,15)，PowSum Q(10,6)，倒数与输出 Q(1,7)），输入输出均为 8 bit。
- 在线归一化：沿用 Milakov & Gimelshein 的 online normalizer，把 max 换成整数 max（IntMax，对元素取 ceiling），使新旧 max 之差为整数，重新归一化只需移位。
- Softermax-aware finetuning：在下游任务微调时用 Softermax 代替 softmax，前向用定点实现，反向用 STE。

硬件（§IV）：Unnormed Softmax Unit（IntMax、Power-of-Two、Reduction）加 Normalization Unit（移位重归一化、线性分段倒数加整数乘法）。2^x 的小数部分用 4 段线性分段近似。集成进 MAGNet 加速器的 PPU，Normalization Unit 放在 PE 与全局缓冲之间。

结果：
- 精度（Table III）：BERT-Base/Large，SQuAD 与 8 个 GLUE 任务，对比 8-bit 量化基线。最大单项下降低于 0.5%，平均反而升高 0.9%（Base）和 0.7%（Large）。
- 硬件（Table IV，TSMC 7nm，序列长度 384）：Unnormed Softmax Unit 面积 0.25x、能耗 0.10x（即 4x 更小、9.53x 更省）；Normalization Unit 面积 0.65x、能耗 0.39x；整个 PE 面积 0.90x、能耗 0.43x（即 2.35x 能效）。
- 序列长度扫描（Fig. 5）：Softermax 的 PE 能耗随长度增长更缓。

## Evidence and Limits

- 精度实验基于改过的 HuggingFace PyTorch，8-bit 权重与激活的量化感知微调，99.999 百分位校准。基线是 8-bit 量化模型，不是浮点模型；论文没有给 FP32 基线。
- 摘要里的“negligible impact”与“平均精度上升”主要来自 RTE、CoLA 这类小数据集，这些任务本身方差大（如 CoLA Base 53.65 到 56.76）。文中没有多次运行或方差，所以“精度上升”不能视为 Softermax 带来的提升。
- 硬件结果来自 Catapult HLS 加 Design Compiler / PT-PX 综合与功耗仿真（Table II），没有流片或 FPGA 实测。基线是 Synopsys DesignWare 的 16-bit 浮点 softmax，作者承认这已是偏乐观的基线，实际加速器常用 32 bit。
- 所谓 2.35x 是 32 宽 MAGNet PE 内的能耗比，只含 SELF+softmax 部分；没有端到端 Transformer 的延迟、吞吐或能耗。
- 没有对三项技术（换底、低精度、在线归一化）分别做消融，也没有逐项给出各自的贡献。
- 与相关工作（Gao、Du、Ham、Zhu）只做了定性对比，没有定量对比。
- 未说明代码或 RTL 是否开源。
- 评测只涉及 encoder 型 BERT，序列长度 384 左右；没有解码器式 LLM、因果 mask 或长上下文的精度结果，虽然动机里提到了 GPT-3。

## Open Questions

- 各项改动（2 为底、定点位宽、IntMax、4 段 LPW）各自对精度和面积能耗的贡献是多少？
- 不做 Softermax-aware 微调、直接替换时精度掉多少？该方法能否用于不再微调的大模型？
- 在更长序列、解码器模型下，Q(6,2) 输入范围与 8-bit 输出是否仍够用？

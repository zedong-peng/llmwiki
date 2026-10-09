---
title: "FTRANS: Energy-Efficient Acceleration of Transformers using FPGA"
updated: 2026-10-09
---

# FTRANS: Energy-Efficient Acceleration of Transformers using FPGA

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（7 页，含参考文献）。图 3–7 为文本抽取后的碎片，只能读到图注和部分标签；表 2–4 基本完整，个别字符乱码。

## Summary

问题：Transformer 类语言模型（BERT、RoBERTa）权重和计算量大，放不进 FPGA 片上存储，也不适合功耗受限设备。论文提出 Ftrans，算法侧做压缩，架构侧做 FPGA 加速（§1）。

方法：
- 增强的 block-circulant matrix (BCM) 压缩（§4.1）：把线性层权重切成 b×b 的循环块，只存 index vector，用 FFT/IFFT 做乘法，复杂度从 O(b²) 降到 O(b log b)。与 CirCNN、C-LSTM 的区别是 index vector 取每个块各行的平均（式 3），而不是只取第一行/列。权重用 16 位定点。
- 架构（§5）：embedding 层（占参数 30.89%）放片外 DDR，encoder/decoder 栈放片上；层间粗粒度流水、层内细粒度流水；有 PE-A/PE-B（矩阵乘）和 FFT/IFFT PE，softmax 用分段线性近似 exp。
- 设计自动化（§6）：先在资源约束下最小化最慢层耗时（式 4–6），再用基于依赖图的算法（Algorithm 1）调度单个 encoder/decoder，生成 C/C++ 交给 Xilinx SDx HLS。

结果：
- 压缩（§7.1，Table 2）：浅层 Transformer（2 层，6M 参数，WikiText-2）block size 4 时精度损失 0，block size 8 时 0.6%；RoBERTa-base（125M，IMDB）block size 4/8 的精度分别降 4.2%/4.3%（95.7% 到约 91.5%/91.4%）。摘要称模型最多缩小 16 倍，正文表中未见 16 倍对应的配置说明。
- 硬件（§7.2，Table 3/4）：VCU118 上 RoBERTa batch 16 吞吐 101.79 FPS、功耗 25.13 W，能效 4.05 FPS/W；i7-8700K 为 3.76 FPS、80 W，RTX5000 为 57.46 FPS、126 W、0.46 FPS/W，Jetson TX2 为 9.75 FPS、5.86 W、1.66 FPS/W。据此文中称吞吐比 CPU 高 27.07 倍、能效高 81 倍，比 GPU 能效高 8.80 倍。

## Evidence and Limits

- 模型只有两个：2 层浅层 Transformer 和 RoBERTa-base，各只有一个任务（语言建模、情感分类）。没有更大模型，也没有 decoder-only 的生成式场景。
- 精度：RoBERTa 掉 4 个点以上，文中解释为预训练模型对压缩更敏感，但未给出缓解办法。Table 2 里 "ACC loss with BCM & Quant." 与单独 BCM 的数字有出入（如 ID 2 为 0，ID 5 为 4.3），未解释。文中还说"压缩部分层"（§7.1.1），没有说明哪些层被压缩。
- 性能比较的口径不清：Table 4 的 FPGA 数字对应 batch 16，CPU/GPU 的 batch size、序列长度、软件栈（是否用优化库）、是否同样压缩都未说明。功耗是否包含板级/主机功耗也未说明。文中"1.77× 吞吐"与表中 101.79/57.46 一致，但 "8.80×" 与表中 4.05/0.46 一致，GPU 功耗倍数 5.01 与 126/25.13 一致。
- 文中 §7.2.2 称 batch 8 为延迟/功耗最佳折中，但 Table 3 的吞吐在 batch 16 最高，选择依据只用 Latency/Power 比，说明较简略。
- 评估基于 HLS 综合与板上数据，未提供代码；FPGA 为 VCU118（6840 DSP，RoBERTa 用到 6531）。
- 相关工作中对比的是一份 HBM FPGA 白皮书，只做定性批评（序列长度 8/16 太短、未压缩），没有定量对比。
- 排版和文字有若干瑕疵（如 Jetson 写作 "Jason TX2"、"GPU TRX5000"、DDR5 等），表述不够严谨。

## Open Questions

- 摘要的 16 倍压缩比对应哪种配置？表中只有 block size 4 和 8，且 RoBERTa 的精度损失在 4% 以上。
- CPU/GPU 基线是否用同一压缩模型和同一 batch，序列长度是多少？这直接决定 27.07×、81×、8.80× 能否成立。
- 平均式 index vector 为何比取首行/列保留更多信息，除了精度表之外没有消融或理论分析。

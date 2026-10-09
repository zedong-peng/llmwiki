---
title: "FlexPosit: Tunable Fractional Precision for LLM Inference Accelerators"
updated: 2026-10-09
---

# FlexPosit: Tunable Fractional Precision for LLM Inference Accelerators

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文、参考文献；无附录）。图 9–12 的柱状图/曲线是乱码式提取，只能读到部分数值标注，细节以表格和正文为准。

## Summary

问题：LLM 权重量化在粒度和位宽两个维度上权衡。group-wise 精度好，但每个 PE 都要 rescale 单元（32×32 阵列面积开销 32.1%，Fig. 2）；channel-wise 硬件规整（<1%），但低比特下精度掉得多。现有 LLM 加速器只支持少数离散精度档，4 b 与 5 b 之间的"分数位宽"用不上。

方法（§IV–V）：
- 权重用 Posit(4,1) 做 channel-wise 量化，每通道带一个 2 的幂 scale（Alg. 1 按 SQNR 选），激活保持 FP16。Posit 的 tapered precision 与重尾权重分布吻合（Fig. 3、4）。
- 混合精度：以"channel window"（256 通道，Qwen 为 1024，与阵列列数对齐）为单位，先全部 4 b，逐个升到 5 b 测 ΔPPL 得到敏感度排序（Alg. 2），按排序把最敏感的窗口升位宽，直到平均"虚拟精度"达到目标（如 4.05 b = 升 5% 窗口）。
- 硬件：output-stationary 的 bit-serial 脉动阵列，全局精度控制单元（GPCU）发 P 周期窗口，精度只在窗口边界变化；4 个 PE 组成 MAC cluster 共享一个 FP16 累加器，吞吐 4/P MAC/周期（4≤P≤8）。SerialPosit 用 sign-magnitude 编码，regime 用相邻位 XOR 逐位解码。
- 精度即延迟：延迟随精度近似线性增长（Fig. 9）。

结果（§VI）：
- 精度（Table II，WikiText-2，9 个模型）：Posit(4,1) 均值 ΔPPL 1.57；FlexPosit 4.1 b 为 0.64；达到 BitMoD 4 b 同 PPL 所需的最小精度（PEB）为 4.1–5.0 b，均值 ΔPPL 0.35；4–5 b 内最佳为 0.14。BitMoD 4 b 为 0.43，OliVe 4 b 为 10.78。
- 消融（Table III、IV）：Qwen2.5-7B 4.1 b 下，随机/位置/Fisher/ΔPPL 排序分别为 8.25/8.36/7.92/7.76（基线 8.39）。相同 ΔPPL 信号用在 layer 粒度上不如 channel-window 粒度。
- 硬件（Table VII、Fig. 11，16 nm 综合 + 周期级模拟器，iso-area、iso-PPL，B=1、L=256）：PE 面积约为 FP16 的 0.12×（compute 部分）；归一化延迟 0.25（BitMoD 0.44，OliVe 0.36，FP16 为 1.0）；能耗 0.25（BitMoD 0.30，OliVe 0.51）。摘要的 1.8×/1.2×/1.5×/2.0× 即由此而来。per-PE rescale 把 rescale 面积开销从 0.4% 推到 9.4%（Table IX）。
- 下游（Table V）：MMLU/HellaSwag 随精度单调回升；FP8 激活下趋势不变（Table VI）。

## Evidence and Limits

- 硬件数字全部来自综合 + 自写周期级模拟器（DRAM 用 Ramulator 2.0 DDR4，buffer 用 CACTI），没有流片或 FPGA 实测。BitMoD/OliVe/FP16 的面积功耗是从各自论文数据按工艺因子缩放到 16 nm，不是同一流程重新综合。
- 对比口径不完全对等：FlexPosit 与 BitMoD 的 PPL 对齐用的是 4.1–5.0 b（平均高于 BitMoD 的 4 b）；OliVe 为 weight+activation 量化，且在 PPL 对齐设置下用 8 b 权重。OliVe 在 LLaMA-2-7B、Qwen2.5-14B 上无结果（表中"–"），均值 ΔPPL 是否按同一模型集计算文中未说明。
- "接近 FP16"需谨慎：Best-PPL 均值 ΔPPL 0.14，但 LLaMA-2-7B 为 5.63 对 5.47；下游任务在 5.0 b 仍有差距（LLaMA-2-7B MMLU 43.1 对 45.8；4.0 b 仅 35.5）。
- 敏感度排序用 WikiText-2 PPL 得到，评测也在 WikiText-2；文中没说清 profiling 与评测数据是否分开，存在 selection 偏乐观的可能。
- 评测限于权重量化、≤14B 模型、PPL 为主；下游仅 Table V 的 5 个模型的 MMLU/HellaSwag。批量/序列敏感性（Table X）显示 B=8、L=8192 时对 OliVe 仅 1.2× 加速，优势随负载缩小。
- 作者自述：Posit 仅作存储格式；SerialPosit 放弃编码域比较/取反。PIM 方向留作后续工作。
- 文中未给出官方代码链接。

## Open Questions

- 敏感度 profiling 需要对每个 channel window 重跑一次 PPL，开销（窗口数 × 评测）与校准数据的泛化性文中没有量化。
- 在更长上下文、更大批量下 decode 是否仍由权重位宽主导？Table X 的趋势表明 compute-bound 区间优势在收窄，但未分析 KV cache/激活瓶颈。
- 对其他基线的缩放（工艺换算、OliVe 的 8 b 配置）对结论的敏感度如何，若同流程重综合是否保持 1.5–1.8× 量级。

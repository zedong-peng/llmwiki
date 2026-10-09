---
title: "Pimba: A Processing-in-Memory Acceleration for Post-Transformer Large Language Model Serving"
updated: 2026-10-09
---

# Pimba: A Processing-in-Memory Acceleration for Post-Transformer Large Language Model Serving

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文 §1–9，读到参考文献开头；无附录）。图 12、13、14、16 的柱状图数值在文本中缺失或乱码，只能依据正文叙述的数字。

## Summary

问题：Mamba-2、RetNet、GLA、HGRN2 等 post-transformer LLM（作者称 SU-LLM）的内存和吞吐优于 transformer（Mamba-2 2.7B 相对同规模 transformer：显存少 2.3×，吞吐高 2.6×，Fig.1），但 batch 推理时 state update 同样受内存带宽限制，而且 per-request 的 state 不能跨请求复用。RetNet 的 state update 占生成延迟从 batch 32 的 41.9% 升到 batch 128 的 73.8%（§3.1, Fig.3）。

观察：多种模型的核心都能写成 S_t = d_t ⊙ S_{t-1} + k_t v_t^T，y_t = S_t^T q_t（式 2），即共用一个 state update 算子。

设计原则：
- 原则 1：per-bank 流水线 PIM 吞吐高但面积开销 32.4%（超过 25% 上限），time-multiplexed 只有 17.8% 面积和 2.8× 吞吐（Fig.5）。Pimba 让两个 bank 共用一个 SPU，一个 bank 读、另一个写（access interleaving），吞吐与 per-bank 相同，面积减半（§4.1, §5.2）。
- 原则 2：state 量化与 KV cache 量化表现不同。fp8（e4m3/e5m2）因 swamping 使 SU-LLM 困惑度崩溃（如 GLA e4m3 为 8,114），transformer 几乎不受影响；stochastic rounding 作用显著（Mamba-2 e5m2 困惑度 62 降到 11.9）。int8 精度好但需要反量化/重量化，面积大；MX8（组内共享指数加微指数）加法只需移位，面积小。结论是 MX8 加 stochastic rounding 位于精度-面积 Pareto 前沿（§3.2, §4.2, Fig.4/6）。

实现：四级流水线（取 state、衰减与外积、求和、与 q 点积并写回），MX 乘法/加法器，5 条自定义 DRAM 命令（ACT4、REG_WRITE、COMP、RESULT_READ、PRECHARGES）及调度；同一硬件通过 score/attend 两阶段支持 attention，因此可服务混合模型（Zamba2）和 OPT（§5）。

结果（周期精确模拟器）：相对 A100 GPU 和 GPU+HBM-PIM，生成吞吐最高 4.1× 和 2.1×，平均 1.9× 和 1.4×；state update 延迟低 14.6× 和 6.9×；能耗平均比 GPU 低 2.2×，比 GPU+PIM 低 1.3×。面积开销 13.4%（HBM-PIM 为 11.8%，Table 3）。Table 2 中 Pimba 与 GPU 精度差在几何平均上不超过 0.3 点。H100 配置下平均 1.8× 和 1.3×；对 NeuPIMs（Zamba2 70B）延迟和显存都更低（§6.2, Fig.15/16）。

## Evidence and Limits

- 全部性能与能耗数字来自自研基于 Ramulator2 的周期精确模拟器，加扩展的开源 GPU/NVLink 模拟器；GPU 不是实测。面积/功耗用 Synopsys DC 加 FreePDK 45nm，再按 DeepScaleTool 缩放到 10nm，并按 "DRAM 工艺密度低 10×" 的经验处理，属估算，没有流片。
- 模型：2.7B 的 RetNet/GLA/HGRN2/Mamba-2、7B Zamba2 与 OPT；70B 是把层数和隐藏维度按比例放大构造的，不是真实预训练模型，只用于性能评估（精度只在小模型上测）。
- 精度评测只有 WikiText-2 和 6 个 zero-shot 基准，没有长上下文或生成质量评测。
- 基线较窄：GPU、GPU+Q（int8 state）、HBM-PIM（作者改成只保留 state update 所需部件）、NeuPIMs；GPU+PIM 与 GPU+Q 相近的结论依赖作者对 HBM-PIM 的重新实现。没有对比其他 GPU kernel 优化（如融合 kernel）。
- 作者承认 GPU 与 PIM 阻塞式交替执行造成利用率不足，NeuPIMs 的 sub-batch interleaving 被视为正交的改进（§8）；attention 的收益小于 state update，因为没有写操作（§6.2）。
- 面积开销比 HBM-PIM 高约 1.5 个百分点，作者认为由吞吐提升抵消。
- 代码：模拟器和精度评测代码开源，但我没有核对仓库内容。

## Open Questions

- 对每个 bank 的 state 布局和 batch/head 数的假设，在 state 维度或头数不同的新模型（如 DeltaNet 类的非简单衰减更新）上是否仍能保持流水线满载，文中只覆盖式 2 形式的模型。
- MX8 加 stochastic rounding 在更长序列（state 累积更多步）下误差是否仍可忽略；评测只用 WikiText-2 等短文本基准。
- 70B 为比例放大的合成配置，真实大模型的 state 大小和头数对 PIM 收益的影响未知。

---
title: "LightMamba: Efficient Mamba Acceleration on FPGA with Quantization and Hardware Co-design"
updated: 2026-10-09
---

# LightMamba: Efficient Mamba Acceleration on FPGA with Quantization and Hardware Co-design

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文 + 参考文献，约 7 页，无附录）。图 2、3、6、9、10 为文本提取，坐标轴数值有错位，只采用正文和表格中明确给出的数字。

## Summary

问题：Mamba2 的激活 outlier 在不同 token 上落在不同 channel，SmoothQuant / OS+ 这类按 channel 缩放的方法失效；SSM 层有大量逐元素乘法（EM），直接量化后 re-quantization 开销大；SSM 内部数据依赖复杂，in_proj 与 SSM 只能串行，硬件利用率不到 60%，SSM 中间激活占 URAM 70% 以上 (§III)。

方法分算法和硬件两部分：
- 旋转辅助 PTQ (§IV-A)：对 in/out projection 用 Hadamard 旋转去 outlier，并尽量与 embedding、LM head、RMSNorm 的 scale 和权重融合，只有 out_proj 前的一处旋转需在线计算。作者指出 SSM 本身不满足旋转等价性（EM 不满足矩阵结合律，Eq. 1），所以不旋转 SSM。第二个 RMSNorm 的 scale 不融进 out_proj 权重，因为融合会增大量化误差 (Fig. 4b)。
- SSM 的 PoT 量化 (§IV-B)：INT8 per-group，scale 取 2 的幂，re-quantization 用移位实现。
- 硬件 (§V)：部分展开的 spatial 架构，展开一个 Mamba block。包含 MMU（tree MAC，DSP packing，din×dout/2 个 DSP）、全流水 SSMU（各算子独立 EMU，FIFO 相连）、HTU（128 点用 FHT，7 级 butterfly，比矩阵乘式 Hadamard 延迟低 72%；40 点用固定 ±1 的小 MMU）。
- Computation reordering：先算 Δ、B、C 存片上，再交替产出 X、Z，使 SSM 逐 head 流水，总计算时间降 32%，利用率 58% 到 96%。Fine-grained tiling/fusion：按 head 和 state 维度分块 (np×pp)，SSMU 的 URAM 降 4 倍。

主要结果：
- Mamba2-2.7B W4A4 (Table III)：FP16 平均 acc 60.2、LAMBADA ppl 4.10；RTN 51.6 / 17.46；SQ 55.5 / 8.26；OS+ 30.3 / >100；LightMamba（仅线性层）56.3 / 6.48；LightMamba*（含 SSM）55.9 / 6.35。W8A8 下与 FP16 基本持平 (60.2)。
- 硬件 (Table IV)：VCK190 W4A4 7.21 tokens/s，W8A8 3.61 tokens/s；能效 2.25 tokens/J（W4A4），RTX 2070 为 0.371，RTX 4090 为 0.484；平均能效比 GPU 高 6.06×（2070）/ 4.65×（4090）(Fig. 9b)。U280 上为周期精确仿真，93 tokens/s，对比 RTX 2070 的 65 与 RTX 4090 的 138，文中称相对 2070 平均 1.43×。
- 消融 (Fig. 10)：量化把吞吐从 2.23 提到 5.32 tokens/s；加旋转后精度提升约 4.3%，吞吐基本不变；加 reordering 到 7.21；加 tiling 后 URAM 从 246 降到 61。

## Evidence and Limits

- 声称“首个 Mamba PTQ 全模型方案”和“首个 FPGA Mamba 加速器”，与已有工作（[12] 仅 RTN 量化线性层，[13] Mamba-PTQ，[14] MARCA）比较主要是定性的。
- 精度只在 Mamba2-2.7B 上给出完整表；Fig. 9b 的能效覆盖 2.7B 到 130M，但精度表没有其他尺寸。校准用 WikiText2 128 条样本。基线 SQ、OS+ 是作者自己在 Mamba 上重新实现的。
- W4A4 仍有明显损失：平均 acc 比 FP16 低约 4 个点，LAMBADA ppl 从 4.10 升到 6.35-6.48。摘要称“minimum accuracy degradation”略强。LightMamba* 比 LightMamba 平均 acc 略低 (55.9 vs 56.3)，ppl 略好。
- 硬件对比的公平性有限：VCK190 实测只有 12GB/s 带宽、7.21 tokens/s，低于两块 GPU 的吞吐 (65 / 138)；高吞吐 93 tokens/s 来自 U280 仿真，且是 W4A4 FPGA 对 FP16 GPU。吞吐与前人 Transformer 加速器 (DFX、FlightLLM) 的对比用的是论文参数估算的数据，非实测。1.43× 是对 2070 的平均值，对 4090 吞吐更低。
- 能效来自 VCK190 BEAM 板级功耗对 GPU 的 nvidia-smi 读数，测量口径不同，文中未说明细节。
- 只评估 decode，prefill 未讨论；batch size、prompt 长度等设定未说明。
- 代码链接在摘要中给出，未验证内容。

## Open Questions

- 旋转后 W4A4 与 FP16 仍有约 4 点平均精度差，SSM 不能旋转是否是主要瓶颈，文中没有分析。
- 其他 Mamba 尺寸和 Mamba1 上的精度表缺失，方法的通用性不清楚。
- U280 仿真的 93 tokens/s 在真实板上能否达到（带宽、频率、布线）未验证。

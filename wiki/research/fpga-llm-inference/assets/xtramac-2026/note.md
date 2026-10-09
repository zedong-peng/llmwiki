---
title: "XtraMAC: An Efficient MAC Architecture for Mixed-Precision LLM Inference on FPGA"
updated: 2026-10-09
---

# XtraMAC: An Efficient MAC Architecture for Mixed-Precision LLM Inference on FPGA

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：正文全文及参考文献前半部分（PDF 文本）。图表为文本抽取，Fig. 6 的柱状数据和 Fig. 14 的具体数值基本不可读；Table IV/V/VII 可读。

## Summary

问题：量化 LLM 同时存在混合精度 MAC（如 INT4×BF16）和运行时数据类型切换（投影层 INT4×BF16，attention 层 BF16×BF16，见 Table I、Fig. 1）。现有 FPGA 方案要么 upcast（DSP 位宽利用率低，Xilinx FP Operator 平均 32.4%），要么空间复制多套数据通路（平均 26.7%），要么时间复用（TATAA 的 INT8 模式 71.1%，BF16 模式仅 8.9%）(§II, Fig. 3-4)。

方法：
- 把 INT×INT、FP×FP、INT×FP 的乘法统一分解为"整数尾数乘积 + 符号/指数旁路处理"（§III-A, Eq. 1-6）。加法则因对齐/归一化 barrel shifter 的代价，INT 与 FP 分开实现（§III-B）。
- 通过 Eq. 9-12 在一个 DSP48E2（27×18）输入端按位偏移打包多个 lane，并行度 ≤ min(LA/S, LB/S)；FP4/FP8 最多 4 lane，BF16 为 2 lane（§III-C, §V-B）。
- 固定四级流水（映射打包 / DSP 乘 + 后处理 / INT-FP 分离累加 / 输出选择），所有数据类型延迟 4 周期、II=1；datatype 信号随流水线传播，逐周期切换（§IV）。
- 特殊值：FTZ/DAZ，RN-even，异常标志随数据通路传递（§III-D）。

结果（U55c，Vivado 2022.2，综合后）：
- 对 AMD FP Operator（加 int-to-fp 转换模块），每操作 LUT/FF/DSP 平均减少 30.0%/47.9%/50.0%，compute density 1.4–2.0×（Table IV）。最高频率平均慢 22%，但均超 400 MHz，作者称每 DSP 有效吞吐约高 1.56×（Fig. 10）。
- 运行时切换：相对 TATAA，LUT/FF/DSP 减少 59.7%/72.5%/93.8%；相对 vendor IP 为 35.5%/58.7%/75.0%（Table V）。增加支持的数据类型时 DSP 不变，频率 483→462 MHz（Fig. 8）。
- GEMV 内核（最多 1920 个 XtraMAC，30 个 HBM 通道，250–300 MHz）：1×4096×4096 为 0.0246 ms / 85 W，H100 CUTLASS 为 0.0294 ms / 135 W，即 1.2× 加速、1.9× 能效（Table VII）。
- 端到端为 V80 上的解析仿真：batch 32 时相对 vendor IP 方案提升 1.5–1.8×；batch 1 受带宽限制，差异可忽略（§VI-D）。

## Evidence and Limits

- 位精确性：声称与 A100/H100 Tensor Core 及 AMD FP Operator 逐位一致，但文中未给出验证方法或测试规模。
- 基线：vendor IP 本身不支持混合精度，作者自行拼接开源 int-to-fp 模块（[10],[17]），基线强度取决于该拼接。TATAA 只评估了 FP 加法器与乘法器，省略 fapp 单元，作者注明资源低于原论文完整设计。
- 资源数据为综合后（非 place-and-route）结果，XtraMAC 加了 AXI wrapper 对齐比较；频率比较仅限单 DSP。
- GPU 对比只做了两个 GEMV 形状（1×4096×4096 和 1×4096×12288），batch=1、带宽受限场景；H100 PCIe 用 CUTLASS，功耗用 nvidia-smi，FPGA 用 xbutil，二者测量口径不同；未说明 GPU 是否使用了对应的量化核（INT4×BF16 / FP4×BF16）。FPGA 的 HBM 带宽 460 GB/s 低于 H100 的 2 TB/s，其优势来自无转换开销（作者称 HBM 利用率约 74%）。
- 端到端结果完全来自解析模型（引用 [7]），假设理想流式和权重复用，目标是 V80 而非实测的 U55c；没有真实整机运行结果。
- 精度与数值：未评估模型精度，FTZ/DAZ 与 FP 累加舍入对 LLM 质量的影响没有实验。
- 自述限制：频率比 vendor IP 低（平均 22%）；1920 实例时因 HBM 附近布线拥塞降至 250–270 MHz；INT 与 FP 累加器不能共享（Config II 几乎无节省）。
- 声称 "up to 1.9× energy efficiency and 1.2× speedup" 对应的是上述两个 GEMV 形状，摘要措辞容易被读成整体模型级结论。
- 开源地址见摘要；复现性未在文中另行说明。

## Open Questions

1. 在真实整机（非解析模型）和更大 batch、更长上下文下，端到端收益是否仍保持 1.5–1.8×？布线拥塞对频率的影响如何随规模变化？
2. 与 H100 的比较是否对等：GPU 侧使用的 INT4/FP4 混合精度内核是否已充分优化，功耗口径（板卡 vs 整卡）是否一致？
3. FTZ/DAZ 与简化的特殊值处理对量化模型端到端精度有无可测影响？

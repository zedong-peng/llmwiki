---
title: "GLITCHES: GPU-FPGA LLM Inference Through a Collaborative Heterogeneous System"
updated: 2026-10-09
---

# GLITCHES: GPU-FPGA LLM Inference Through a Collaborative Heterogeneous System

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（6 页会议论文，含参考文献）。图 7、8、9 只有坐标轴文字，柱状/曲线数值未提取，只能依据正文引用的数字；无附录。

## Summary

问题：小 batch 的低延迟推理中，prefill 是计算瓶颈（矩阵-矩阵乘），decode 是带宽瓶颈（矩阵-向量乘）。GPU 在 decode 阶段算力利用率极低（A100 上 LLaMA2-7B 为 0.19%，Table II），FPGA（U280）算力有限，prefill 1536 token 约 5 s，是 A100 的 28.44 倍（§III-A，Table I）。

方法：
1. 异构分工：GPU 做 FP16 prefill，FPGA 做 decode。prefill 产生的 KV cache 在 GPU 上量化后经 PCIe 先回主机内存，再写入指定 FPGA 的 HBM 预留地址；逐 transformer block 流水，传输与 prefill 计算重叠。首 token 在 CPU 采样，之后 decode 全在 FPGA 上，GPU 可释放 KV cache（§III-C）。
2. 主机调度器：先到先服务把 decode 分给空闲 FPGA；FPGA 全忙时由 GPU 自己做 decode（KV cache 留在 GPU）。每张卡存完整模型权重。
3. HBM 数据预取：以 FlightLLM 为基线，profiling 显示小访存指令因指令译码/发射开销使 HBM 带宽利用率只有约 40%（Fig. 5）。把后续 M 条 MV 指令所需的权重与量化元数据合并成一次大访存（如 q_proj 权重 8KB→32KB，元数据 256B→1KB），用误差 <5% 的性能模拟器逐层选预取比例（§IV）。

结果（§V-B）：
- 预取比例 4 最优，端到端 decode 在序列长 128/1024 时分别提速 1.20/1.16 倍（Fig. 9）。
- 1 张 A100 + 7 张 U280 相对 8 卡 A100 / 8 卡 U280：平均吞吐 1.28/1.23 倍，成本效率 2.38/1.08 倍；1 张 V100S + 7 张 U280 相对 8 卡 V100S / 8 卡 U280：吞吐 1.34/1.21 倍，成本效率 1.90/1.14 倍（Fig. 7）。
- KV cache 传输延迟在多数情况下（尤其长输入）小于 GPU prefill 延迟，可被重叠（Fig. 8）。

## Evidence and Limits

设置：LLaMA2-7B；GPU 为 HuggingFace FP16 实现；FPGA 为 FlightLLM 风格 W4A8 量化。输入/输出长度组合为 [128,128] 到 [1024,1024]，取几何平均。硬件价格取自 Table II（A100 $17000，V100S $12000，U280 $8000）。

证据范围：
- FPGA 性能来自基于 FlightLLM 的周期精确模拟器（225 MHz，含预取），不是实机端到端运行；8 卡异构系统同样是"模拟"（§V-B）。只有 KV cache 传输延迟是实测（重复 50 次）。
- 对比不对等：GPU 是 FP16 的 HuggingFace 实现，FPGA 是 4-bit 权重量化，没有用 vLLM/TensorRT-LLM 等优化引擎作基线，也没有报告量化对精度的影响。
- 只测了单一模型（7B）、小 batch、单节点；没有首 token 延迟、尾延迟、并发请求负载下的调度结果，只有吞吐和成本效率。
- 成本效率只用卡的标价，不含主机、功耗、互联。
- 摘要把 "1.28/1.34 倍" 说成相对 A100/V100S 的提升，正文 Fig. 7 中相对 FPGA-only 的提升较小（1.21-1.23 倍成本效率仅 1.08-1.14 倍）。
- 论文自述局限：异构型号混合的复杂调度、多节点（经 FPGA 以太网传 KV cache）留作未来工作。

## Open Questions

1. 在真实板卡上端到端跑通后，模拟器给出的吞吐增益还能保留多少？PCIe 经主机中转 KV cache 在高并发下是否成为瓶颈？
2. 1 GPU : 7 FPGA 的配比由 prefill/decode 吞吐比决定，但文中没给出配比敏感性；负载偏向长输入或大 batch 时最优比例如何变化？
3. 与采用同样量化、同样优化引擎的 GPU 基线，或 GPU 上 prefill/decode 分离（disaggregation）方案相比，增益是否仍然成立？

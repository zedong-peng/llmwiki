---
title: "Hummingbird: A Smaller and Faster Large Language Model Accelerator on Embedded FPGA"
updated: 2026-10-09
---

# Hummingbird: A Smaller and Faster Large Language Model Accelerator on Embedded FPGA

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文、参考文献，无附录）。图为文本抽取，Fig. 1/2/5/7/9/11 的内容混乱，仅能依据正文描述；Table V 的列对应有些错位，部分数字按正文交叉核对。

## Summary

问题：嵌入式 FPGA（Zynq UltraScale+，KV260 / ZCU104）上做 LLM 解码，受限于资源占用大、DDR 带宽利用率低（此前 SOTA 为同组 Li et al. [11] 的 84%）、4GB 内存装不下更大模型。此前 FPGA LLM 工作多在云端 FPGA 上，模型不超过 7B（§I）。

方法（均为 W4 权重 GPTQ、KV cache 8 bit 线性量化，不做额外压缩，§V-A）：
1. DSP 优化的 GEMV 引擎（§IV-A）：INT24 定点，分段 DSP MAC chain + 多输入 DSP 加法链构成 reduction tree；利用 DSP48E2 的 in-DSP prefetch / multiplexing / accumulating / offloading，同时支持 DOT 与 AXPY（后者免去 V 转置）。Table I 消融：Hybrid+ 优化后 1962 LUT、4355 FF、148 DSP，对比未优化 6570 LUT、11856 FF、160 DSP。
2. Column-aligned 访存（§IV-B）：针对 PS 侧 4 个 AXI 口仲裁造成的 "1+1+1+1<4" 带宽损失，令每次事务的 4 个端口访问同一 row/bank 的不同 column 段，BTT 取 2^13 或 2^14 字节。带宽利用率最高 95%；Table II 中 KV260 单次推理权重传输延迟 LLaMA3-8B 228ms→202ms。
3. 张量并行（§IV-C）：Megatron 式切分，ZCU104 双核（PS+PL 两路 DDR），声称 U250 四核可线性扩展。
4. Embedding 表卸载到 SD 卡 + 绕过 DDR 的直传（§IV-D）：Table III 单个 embedding 向量加载 152ms→2.8ms（FastSeek+缓冲）→1.5ms（绕过 DDR）。释放内存使 LLaMA3-8B 能放进 4GB。
5. GQA 数据流（§IV-E）：把 query 计算提前两个位置以隐藏 RoPE 尾部（78 周期），先算全部 qK 并存 softmax 结果再算 sV，K/V 缓冲 URAM 从 32 降到 16+2；用 online softmax。支持 4096 上下文（Li et al. 为 1K）。

结果（Table V，prefill:decode=32:32，单 batch）：LLaMA3-8B 在 KV260 上 4.8 token/s、带宽效率 94%、26K LUT、179 DSP、3.81W；ZCU104 上 8.6 token/s、93%。Li et al. 的 LLaMA2-7B 为 4.9 token/s、84%、78K LUT、291 DSP。Table VI：与 Jetson Orin Nano（15 token/s，79%）/AGX（40 token/s，71%）相比，带宽效率与能效更高（能效 1.44 / 1.39 vs 1.0 / 0.66），绝对速度低。Table VII：单核约 18K LUT，可放入 Spartan UltraScale+ SU150P/SU200P。

## Evidence and Limits

- 证据主要是资源报告（Vivado）和实测 token/s；资源与功耗来自 Vivado 报告，功耗并非板上实测（§V-A 原文说 "derived from Vivado reports"）。
- 摘要中的 "67% LUT、39% DSP、42% 功耗节省" 是对 Li et al. 的比较（78K→26K LUT，291→179 DSP，6.57→3.81 W），基线是作者自己前作，且模型不同（LLaMA2-7B vs LLaMA3-8B）。
- 速度比较的基线不对等：4.8 vs 4.9 token/s 对应不同模型，作者以 "模型大 10%" 解释；Norm. Perf. 按 7B、稠密 4-bit 归一化的方式是作者自定。Jetson 数据引自 Jetson AI Lab 公开基准，非同条件自测。
- 全文没有任何精度/困惑度评测；W4 GPTQ 与 8-bit KV 对 LLaMA3-8B 质量的影响未报告。声称 "不依赖会损失精度的进一步压缩" 但没有给出精度数据。
- 速度均为短上下文（32:32）下的数字；4K 上下文下的 token/s、prefill 速度未报告。正文自述实际推理中利用率会再降 1-2%。
- Embedding 从 SD 卡读取的方案依赖 SD 卡，单次 1.5ms，但 SD 卡寿命/不同卡的差异未讨论。
- Spartan UltraScale+ 的部署仅为资源适配（Table VII），没有实际上板，也无价格数据（"官方价格待定"）。
- U250 四核线性扩展、All-reduce 被隐藏的说法，仅有 Table V 中 U250 一列的数字（7.21 token/s，12/76.8 GB/s 两种带宽配置的效率 75%/12%）作支撑，缺少扩展性单独实验。
- 代码或 RTL 未在文中给出。

## Open Questions

- W4 GPTQ + KV8 + INT24 定点 GEMV 下，LLaMA3-8B 的精度损失有多大，与 FP16 比如何？
- 4K 上下文下的实际解码速度与 prefill 延迟如何？KV cache 增长对带宽效率的影响文中没有量化。
- column-aligned 策略是否依赖具体的 Zynq 地址映射与 DDR 配置，换到其他 SoC 或 DIMM 配置是否仍有效？

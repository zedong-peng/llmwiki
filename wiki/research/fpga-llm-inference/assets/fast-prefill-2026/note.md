---
title: "FAST-Prefill: FPGA Accelerated Sparse Attention for Long Context LLM Prefill"
updated: 2026-10-09
---

# FAST-Prefill: FPGA Accelerated Sparse Attention for Long Context LLM Prefill

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文、参考文献）；无附录。图 5-8 只有坐标轴文字，柱状数值未提取，只能依赖正文给出的数字；Table I-III 可读。

## Summary

问题：长上下文 prefill 中 self-attention 随长度二次增长；动态稀疏注意力（FlexPrefill）能减算，但 sparse index 生成控制流依赖数据、算强低，KV 访问随 head/query block 变化难以复用，使 GPU 上变成 memory-bound，且能耗高。作者认为 FPGA 上尚无针对动态稀疏 prefill 的加速器（"first"，自称）(§I)。

方法：在 Alveo U280 上实现 W8A8 加速器，沿用 FlexPrefill 的 index 生成算法（Algorithm 1，block=128，JSD 阈值 τ=0.1 选 query-aware 或 vertical-slash），采用 chunked prefill（chunk=128）。三个设计 (§IV)：
- SIGU：流式、memory-aware 的 index 生成。Key block 按递增顺序只取一次，对最后一个 query block 做增量 per-block 统计（vertical/slash accumulator），用 streaming top-k 代替全排序；中间张量从约 4GB 降到约 4KB，只写 O(⌈S/B⌉) 大小的数据 (§I, §IV-B)。
- SAU：以 KV block 为主序的调度，把 sparse index 转成 job list，用 block-use counter 作为精确剩余使用次数，做 liveness-driven 缓存（URAM，16MB）；分 Hot/Cold 两层，Hot 准入阈值为 query block 总数的 50%；用 keyed accumulation 处理乱序的部分结果 (§IV-C)。
- Hybrid MPU：6 个 32x32 DSP systolic array + 6 个 32x32 基于 bit-plane / nibble 分解的 LUT array，INT8 乘、INT32 累加 (§IV-D)。

结果 (§V)：模型 Llama3.2-1B、Qwen（图中 Qwen-2-1.5B，正文写 Qwen2.5-1B）、Llama3.2-3B，batch=1，上下文 4K-128K。相对 A5000 上 FlexPrefill 的 INT8 实现，TTFT 加速 1.5-2.5x（引言写 1.2-2.5x，摘要写平均最高 2.5x），能效最高 4.5x（Token/Joule）。消融：去掉 16MB 缓存后 TTFT 差 2.5x（命中率 65%，Fig. 7）；Hybrid MPU 比纯 DSP MPU 快 1.8x（Fig. 8）。资源 (Table II)：LUT 64.3%、BRAM 55.8%、URAM 95%、DSP 71.6%；实际频率 175MHz。

## Evidence and Limits

- 精度 (Table III, RULER 4k-64k)：FAST-Prefill 与 FlexPrefill INT-8 基本持平（1B 平均 33.07 vs 33.44；3B 平均 61.28 vs 63.45），但都远低于 BF16（1B 61.68；3B 77.74）。1B 在 4k 从 95.67 掉到 52.14。即 W8A8 本身带来大幅精度损失，论文只与 INT-8 基线比，未讨论该损失的原因或缓解。
- 精度只测到 64k，性能测到 128K；128K 的精度没有给出。Table III 只有两个模型，Qwen 无精度结果。
- 速度基线是 FlexPrefill 官方 GPU 实现（A5000，Table I：222 TOPS、768GB/s）；FPGA 为 5.4 TOPS、HBM 460GB/s。加速归因于 GPU 上部分 index 生成逻辑卸载到 CPU、访存不规则 (§V-B2)，这是对基线实现的解释，没有给出 GPU profiling 证据；基线并未用融合 kernel 重写。与更新的 GPU 或 H100 级别平台、其他稀疏 prefill 方案无对比。
- 能耗测量：FPGA 用 Vivado 工具估计，GPU 用 nvidia-smi，方法不对等，且未说明是否含 host CPU/板级功耗。
- 数字前后不一致：结论写 "up to 2x TTFT、4x 能效"，摘要/引言为 2.5x/4.5x；上下文长度列表在 §V-A 漏了 64K。
- 仅小模型（1B-3B），batch=1；URAM 占用 95%，限制缓存容量；未涉及 decode 阶段、多 FPGA、更大模型。作者自述可叠加 N:M 与 block pruning（未实现）。
- 未陈述官方代码链接。

## Open Questions

1. W8A8 导致的 RULER 大幅下降（如 1B 4k 95.67 到 52.14）有多少来自量化方式本身，多少来自稀疏 index 在 INT8 下的偏差？论文未拆分。
2. 加速比在多大程度上取决于基线 GPU 实现的次优（CPU 卸载、非融合）？融合良好的 GPU kernel 下差距会缩小多少？
3. 在 3B 以上模型、更长或更多样的任务（非 RULER）上，缓存命中率（65%）与 Hot 阈值（50%）是否仍有效？

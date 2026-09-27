---
title: A Persistent-State Dataflow Accelerator for Memory-Bound Linear Attention Decode
  on FPGA
domain: research
area: fpga-llm-inference
type: paper
status: active
updated: '2026-09-15'
tags:
- paper
- fpga
- verified-arxiv
---

# A Persistent-State Dataflow Accelerator for Memory-Bound Linear Attention Decode on FPGA

## 论文身份与资产

Neelesh Gupta、Peter Wang、Rajgopal Kannan、Viktor K. Prasanna；公开 [arXiv:2603.05931v1](https://arxiv.org/abs/2603.05931v1)，2026 preprint；本次未独立核实正式 venue。

[PDF（7 页）](paper-pdf/2603.05931v1.pdf) · [TeX](paper-tex/extracted/2603.05931v1/main.tex) · [Bibliography](paper-tex/extracted/2603.05931v1/main.bib) · [元数据](metadata.yaml)。

## 问题与机制

Qwen3-Next 风格 Gated DeltaNet 单层 batch-1 decode：16 q/k heads、32 value heads、d=128、FP32。32×128×128 的约 2 MiB 递归状态常驻 BRAM，跨 token 保留；每步只传 q/k/v 和 gates。这是固定大小线性 attention 状态，不是普通 Transformer 的增长式 KV cache。

方法/Architecture Design：把输出代数展开为旧状态乘 q 与校正项，令 retrieval 和部分 output 共用一次 state read，之后一次 write；三次 state pass 降为两次。五阶段融合、2:1 GVA 共享 q/k、列并行 P_K=16、head 并行 2/4/8/16，prepare/compute/store dataflow。论文模型由约 3072 降至 2106 cycles/iteration，报告 1.46×。

## 论文实验：估算不等于上板

HLS 2025.1，U55C，目标 300 MHz。2/4/8/16 heads 的 HLS cycles 分别 42538/26252/18978/23206，对应 141.7/87.4/63.2/77.4 μs；这些是 cycles/目标频率估算。GPU 对照是 NVLabs GatedDeltaNet PyTorch reference，H100 上 285 μs（warm-up 后 1000 runs）。4.5× 来自 285/63.2，不是 FPGA 实板请求级加速。

只有 2-head 设计完成布线到 263 MHz；4-head 有 88725 unroutable signals，8/16-head 尚需进一步 floorplanning。因此不能拿最佳 8-head 估算当已实现板级结果。2-head 的 9.96 W 是 Vivado on-chip 功耗估算；62× 能效还用了 H100 350 W TDP，两端测量边界不一致。

## 限制与源码

只涉及 GDN recurrence，未展示完整 Qwen3-Next checkpoint 的多层推理、prefill、生成循环或 llama.cpp/backend 接口。论文没有给出已核实的作者 FPGA 仓库；NVLabs/GatedDeltaNet 是 GPU baseline，不能误挂为作者 FPGA 实现。

读者质疑：2 MiB state 可容于 H100 50 MB L2，论文“GPU 每 token 必须 HBM 往返”的解释并不构成实际 cache miss 证据；需要优化 GPU kernel 和内存计数器对照。片上常驻状态与代数融合值得参考，但“常驻状态”本身并非首创。

## 与本项目关系及状态

列入机制相关论文，**不列为完整 llama.cpp FPGA backend 竞争者**；也不能与本地完整 GPT-2 decode token/s 直接比。

已读 v1 main.tex 全文（方法、性能模型、架构、实验、限制、结论）和 main.bib；核验 PDF 身份。未运行代码、HLS、综合或板上复现。回到 [[research/fpga-llm-inference/index]]。

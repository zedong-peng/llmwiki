---
title: HLS Research
domain: research
area: HLS
type: overview
status: active
updated: 2026-09-08
tags: [research, hls, qor-prediction, dse, fpga]
---

# HLS Research

高层次综合（HLS）设计空间探索：从 C/C++ 源码预测 post-route QoR，避免完整 C-to-bitstream 流程；以及 LLM 参与的 DSE 方法。

## Papers

见 [Papers Directory](papers/index.md)：2 篇已处理（TeX 精读 + PDF + source 归档）。

- [Hierarchical GNN QoR (2024)](papers/hierarchical-gnn-qor-2024/index.md) — 源码 → LLVM IR → pragma 扩展 CDFG → 分层 GNN（GNN_p/GNN_np/GNN_g），post-route 延迟/资源 MAPE <10%，DSE 从数十天缩到十几分钟。
- [MPM-LLM4DSE (DATE 2026)](papers/mpm-llm4dse-2026/index.md) — ECoGNN + CodeBERT 多模态融合预测 QoR，LLM（PEODSE prompt）做优化器；关键发现 LM-only > ECoGNN-only，源码语义价值被低估。

两篇对照：前者纯图方法、数据集 16 应用；后者多模态 + LLM 优化器、数据集 21 kernels。精度口径不同（MAPE vs RMSE），不直接对比。

与 [[research/fpga-llm-inference/index|FPGA LLM Inference]] 的关系：HLS QoR/DSE 是该项目 P1–P5（coarse region、HBM 布局、kernel 微架构）未来做综合闭合时的方法储备，当前无直接 board 证据关联。

返回 [[research/index]]。

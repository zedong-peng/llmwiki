---
title: "Understanding the Potential of FPGA-Based Spatial Acceleration for Large Language Model Inference"
domain: research
area: fpga-llm-inference
type: paper
status: active
updated: 2026-09-08
tags: [paper, fpga, llm-inference]
---

# Understanding the Potential of FPGA-Based Spatial Acceleration for Large Language Model Inference

Spatial LLM develops an analytical model and a per-model spatial FPGA dataflow design. It is a
useful reference for separating prefill and decode resource/bandwidth behavior.

## Paper Meta

- Authors: Hongzheng Chen, Jiahao Zhang, Yixiao Du, Shaojie Xiang, Zichao Yue, Niansong Zhang, Yaohui Cai, Zhiru Zhang
- Year: 2024
- Venue: ACM Transactions on Reconfigurable Technology and Systems
- BibTeX key: `spatial_llm`
- Related Work category: FPGA Transformer and LLM systems
- Public record: [DOI](https://doi.org/10.1145/3656177); [arXiv](https://arxiv.org/abs/2312.15159)

## Local Assets

- Paper PDF: [2312.15159.pdf](2312.15159.pdf) (28 pages; SHA-256 `75a69ed82c570491fb481fa149e635695cc0c583f071e7717a21931b131754cd`)
- arXiv source archive: [2312.15159-source.tar.gz](source/archives/2312.15159-source.tar.gz); extracted TeX: [3.2-modeling-constraints.tex](source/extracted/sections/3.2-modeling-constraints.tex), [5.2-accelerator.tex](source/extracted/sections/5.2-accelerator.tex)

## Read Notes

- The physical board result is GPT-2 on U280; LLaMA/Vicuna results in the paper are analytical rather than board demonstrations. The GPT-2 path uses W8A8 and reports separate prefill/decode performance and energy.
- The memory model explicitly buffers K and V and passes them to decode as the KV cache. It uses double buffering and discusses tiling KV on chip; this establishes a cache-aware accelerator design, not a framework-level runtime API.
- The paper's central lesson is that compute-intensive prefill and bandwidth-intensive decode need different allocation and scheduling choices. Its per-model spatial pipeline is not an unchanged GGML backend.
- Source-first paper read completed. On 2026-09-08, the paper-linked [Allo repository](repo/allo/) was archived at `8bafb0dcee27c96a72872184d2b106c59c8a1414`; [examples/README.md](repo/allo/examples/README.md) explicitly links this paper and provides a kernel library/HLS-generation path. This does not establish release of the exact complete-generation controller. Dependencies and FPGA execution were not attempted; repository inspection remains partial.
- The revised [[research/fpga-llm-inference/feature-level-evidence-matrix]] assigns E2E P for phase-level evidence, Multi-model P for analytical additional generative families, and public artifact Src for the kernel library. BERT is not counted as a second generative checkpoint.

Return to [[research/fpga-llm-inference/papers/index|FPGA LLM paper library]].

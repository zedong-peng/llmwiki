---
title: "F-BFQ: Flexible Block Floating-Point Quantization Accelerator for LLMs"
domain: research
area: fpga-llm-inference
type: paper
status: active
updated: 2026-09-27
tags: [paper, fpga, llama.cpp, ggml, edge, secda]
---
# F-BFQ: Flexible Block Floating-Point Quantization Accelerator for LLMs

Successor of [[research/fpga-llm-inference/assets/secda-llm-2024/index|SECDA-LLM]] by the same group
(Jude Haris, Jose Cano, University of Glasgow). Accepted at the LG-ARC workshop at ISCA 2025;
[arXiv 2510.13401](https://arxiv.org/abs/2510.13401). No PDF or source archived locally yet.

## Read notes (arXiv HTML v1, 2026-09-27)
- Platform: AMD Kria KV260 at 200 MHz.
- Models: GPT-2 (163M), TinyLlama (1.1B), MobileLLaMA (1.4B).
- Integration: through the SECDA-LLM platform into llama.cpp (`llama-cli` cross-compiled for ARMv8 with NEON); the driver receives MatMul operations and issues accelerator opcodes over AXI-Stream.
- Offload scope: MatMul with Q2_K and Q3_K block-floating-point weights and Q8_K inputs, switching formats at run time. KV cache and attention remain on the Arm CPU.
- Results: average 1.4x speedup over NEON CPU execution across the three models; up to 12.2 token/s (GPT-2); 5.2 token/s headline in the abstract.
- No public repository link in the paper.

## Role in the backend paper
Same category as SECDA-LLM and IMAX: native llama.cpp entry and complete generation with host operators, but per-operator MatMul offload with host-side KV (not device-resident).

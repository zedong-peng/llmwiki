---
title: "LUT-LLM: Efficient Language Model Inference with Memory-Based Computations on FPGAs"
domain: research
area: fpga-llm-inference
type: paper
status: seed
updated: 2026-09-15
tags: [paper, fpga, llm-inference]
---

# LUT-LLM: Efficient Language Model Inference with Memory-Based Computations on FPGAs

> Bibliographic record and local public asset cache. Full paper notes are pending.

## Paper Meta

- Authors: Zifan He, Shengyu Ye, Rui Ma, Yang Wang, Jason Cong
- Year: 2026
- Venue: 2026 IEEE 34th Annual International Symposium on Field-Programmable Custom Computing Machines
- BibTeX key: `lut_llm`
- Related Work category: FPGA Transformer and LLM systems
- Public record: [DOI](https://doi.org/10.1109/FCCM68464.2026.00027); [arXiv](https://arxiv.org/abs/2511.06174)

## Local Assets

- Paper PDF: [2511.06174.pdf](2511.06174.pdf) (11 pages; SHA-256 `6afab4bb78b9b92fa017b6c8aeed642b388d936f43054d76498f2fe9a1b1183c`)

## Ingest Status

- Metadata: verified against the manuscript bibliography.
- Paper PDF: `downloaded`.
- Reading note: seed; no unverified method or performance claims added.
- Source archive and code repository: not requested in this import pass.

Return to [[research/fpga-llm-inference/papers/index|FPGA LLM paper library]].

## Model input and coverage audit (2026-09-15)

**Classification: Model-specific implementation.** Qwen3-1.7B block; general checkpoint loader not established.

config/config.h fixes hidden=2048, FFN=6144, head dimension=128 and KV groups=8. The block composes Qwen operations with these compile-time dimensions. The decode testbench seeds random centroids/weights, so it is not a real-checkpoint portability demonstration. Changing constants and rebuilding may support variants, but no unchanged model-driven import flow was established.

Inspected code (pinned copies, not executed):

- [README.md](source/code-audit/README.md) — [upstream commit](https://github.com/LUT-FPGA/LUT-LLM/blob/9ee2259d312f9b1119a398d8ff7703154260a417/README.md).
- [config/config.h](source/code-audit/config/config.h) — [upstream commit](https://github.com/LUT-FPGA/LUT-LLM/blob/9ee2259d312f9b1119a398d8ff7703154260a417/config/config.h).
- [qwen_block/qwen_block.h](source/code-audit/qwen_block/qwen_block.h) — [upstream commit](https://github.com/LUT-FPGA/LUT-LLM/blob/9ee2259d312f9b1119a398d8ff7703154260a417/qwen_block/qwen_block.h).
- [qwen_block/qwen_block_decode_tb.cpp](source/code-audit/qwen_block/qwen_block_decode_tb.cpp) — [upstream commit](https://github.com/LUT-FPGA/LUT-LLM/blob/9ee2259d312f9b1119a398d8ff7703154260a417/qwen_block/qwen_block_decode_tb.cpp).

[Audit receipt](source/model-coverage-audit.json). See [[research/fpga-llm-inference/index#Model input and coverage audit (2026-09-15)|cross-paper comparison]] for definitions and input formats. This dated section supersedes older coverage/placement summaries where they conflict.

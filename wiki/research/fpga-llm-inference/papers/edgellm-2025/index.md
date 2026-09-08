---
title: "EdgeLLM: A Highly Efficient CPU-FPGA Heterogeneous Edge Accelerator for Large Language Models"
domain: research
area: fpga-llm-inference
type: paper
status: active
updated: 2026-09-07
tags: [paper, fpga, llm-inference]
---

# EdgeLLM: A Highly Efficient CPU-FPGA Heterogeneous Edge Accelerator for Large Language Models

EdgeLLM is a CPU-FPGA heterogeneous compiler/runtime reference for model-level generation on an
embedded FPGA. This note uses the validated PDF because an arXiv source request returned a PDF
payload rather than a TeX archive in this pass.

## Paper Meta

- Authors: Mingqiang Huang, Ao Shen, Kai Li, Haoxiang Peng, Boyu Li, Yupeng Su, Hao Yu
- Year: 2025
- Venue: IEEE Transactions on Circuits and Systems I: Regular Papers
- BibTeX key: `edgellm`
- Related Work category: FPGA Transformer and LLM systems
- Public record: [DOI](https://doi.org/10.1109/TCSI.2025.3546256); [arXiv](https://arxiv.org/abs/2407.21325)

## Local Assets

- Paper PDF: [2407.21325.pdf](2407.21325.pdf) (14 pages; SHA-256 `fedc5f501a766cde554f1ba62dfb6a77ebe65e555289c00e63c7d2aea4197099`)

## Read Notes

- The system evaluates GLM-6B and Qwen-7B on VCU128 and combines CPU control with an FPGA instruction engine; the reported boundary includes generation throughput, latency and power.
- The architecture text describes a dedicated DMA path that transfers online-generated KV cache into HBM, plus a common tensor layout for burst access. This is explicit KV placement/traffic optimization, though not a reusable llama.cpp backend ABI.
- PDF-first read completed; no TeX source was retained because the source endpoint did not return TeX. The numbers remain contextual rather than matched to the current U280/GPT-2 profile.

Return to [[research/fpga-llm-inference/papers/index|FPGA LLM paper library]].

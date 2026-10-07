---
title: "EdgeLLM: A Highly Efficient CPU-FPGA Heterogeneous Edge Accelerator for Large Language Models"
domain: research
area: fpga-llm-inference
type: paper
status: active
updated: 2026-09-15
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

- Paper PDF: [2407.21325.pdf](paper-pdf/2407.21325.pdf) (14 pages; SHA-256 `fedc5f501a766cde554f1ba62dfb6a77ebe65e555289c00e63c7d2aea4197099`)

## Read Notes

- The system evaluates GLM-6B and Qwen-7B on VCU128 and combines CPU control with an FPGA instruction engine; the reported boundary includes generation throughput, latency and power.
- The architecture text describes a dedicated DMA path that transfers online-generated KV cache into HBM, plus a common tensor layout for burst access. This is explicit KV placement/traffic optimization, though not a reusable llama.cpp backend ABI.
- PDF-first read completed; no TeX source was retained because the source endpoint did not return TeX. The numbers remain contextual rather than matched to the current U280/GPT-2 profile.

Return to [[research/fpga-llm-inference/threads/paper-library/index|FPGA LLM paper library]].

## Model input and coverage audit (2026-09-15)

**Classification: Cross-architecture (paper).** GLM-6B and Qwen-7B.

PDF section V-B/Fig. 8 describes compiling sparse/quantized models into instructions, prepared weights and control code; the evaluation includes GLM and Qwen. The conclusion explicitly identifies varying RotaryEmbedding as a limitation, requiring a model-custom operator or CPU plus element-wise operations. It is not single-model-only, but new-family support can require implementation work. No verified implementation is present in the reviewed record.

Classification uses the paper text and available public artifact; unavailable source is not treated as evidence of model restriction.

[Audit receipt](model-coverage-audit.json). See [[research/fpga-llm-inference/index#Model input and coverage audit (2026-09-15)|cross-paper comparison]] for definitions and input formats. This dated section supersedes older coverage/placement summaries where they conflict.

## Original-text verification (2026-09-27)

Checked against the original paper text or public code for the llama.cpp FPGA backend paper; supersedes earlier summaries where they differ.

- End-to-end compiler maps the whole model; CPU runs the dynamic compilation (PDF text lines 128-137).
- Weights and online KV cache in HBM via a dedicated DMA path; activations to on-card DDR (lines 169-195). MatMul at 280 MHz, other operators 140 MHz.
- Dense GLM-6B decode about 90 token/s below 512 decode tokens; Qwen-7B 42.5-69.4 token/s; matrix-layer HBM utilization 70-80%, average about 75% (lines 578-600). AccLLM Table VII instead lists EdgeLLM as ChatGLM2-6B, 125 MHz, 75 token/s.

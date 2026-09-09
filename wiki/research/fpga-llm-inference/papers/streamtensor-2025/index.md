---
title: "StreamTensor: Make Tensors Stream in Dataflow Accelerators for LLMs"
domain: research
area: fpga-llm-inference
type: paper
status: active
updated: 2026-09-07
tags: [paper, fpga, llm-inference]
---

# StreamTensor: Make Tensors Stream in Dataflow Accelerators for LLMs

StreamTensor introduces a Torch-MLIR compiler/runtime that turns Transformer blocks into streaming
dataflow accelerators. It is the closest compiler-style contrast to a native GGML backend, while
using a different application boundary.

## Paper Meta

- Authors: Hanchen Ye, Deming Chen
- Year: 2025
- Venue: Proceedings of the 58th IEEE/ACM International Symposium on Microarchitecture
- BibTeX key: `streamtensor`
- Related Work category: FPGA Transformer and LLM systems
- Public record: [DOI](https://doi.org/10.1145/3725843.3762817); [arXiv](https://arxiv.org/abs/2509.13694)

## Local Assets

- Paper PDF: [2509.13694.pdf](2509.13694.pdf) (16 pages; SHA-256 `03fd093b394054e7ddadf6cf06d5f70102f40f7c6a5ca91a9b8efa521ff26b6e`)
- arXiv source archive: [2509.13694-source.tar.gz](source/archives/2509.13694-source.tar.gz); extracted TeX: [main.tex](source/extracted/main.tex)

## Read Notes

- The compiler supports GPT-2, Qwen, Llama and Gemma examples and uses W4A8 block/dataflow generation on U55C. Reported metrics include total latency, TTFT and decode throughput.
- The source names input tokens and KV caches as dynamic tensors and uses maximum-shape hints. It does not expose a persistent append/read/position/reset protocol or a cross-call backend ABI at the granularity needed to verify llama.cpp-style state management.
- Its main system object is a generated Transformer block invoked with different layer weights; this demonstrates coarse-grained streaming and launch amortization, not a reusable native GGML runtime.
- Source-first read completed. A 2026-09-08 availability recheck found the author's
  [public API documentation](https://hanchenye.com/streamtensor/), but its linked
  `hanchenye/streamtensor` GitHub repository returned anonymous web/API 404. An
  accessible official implementation remains unverified; this does not prove
  nonexistence. See [[research/fpga-llm-inference/index|area index §Manuscript Recheck]].

Return to [[research/fpga-llm-inference/papers/index|FPGA LLM paper library]].

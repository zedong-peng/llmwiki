---
title: "StreamTensor: Make Tensors Stream in Dataflow Accelerators for LLMs"
domain: research
area: fpga-llm-inference
type: paper
status: active
updated: 2026-09-15
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

- Paper PDF: [2509.13694.pdf](paper-pdf/2509.13694.pdf) (16 pages; SHA-256 `03fd093b394054e7ddadf6cf06d5f70102f40f7c6a5ca91a9b8efa521ff26b6e`)
- arXiv source archive: [2509.13694-source.tar.gz](paper-tex/archives/2509.13694-source.tar.gz); extracted TeX: [main.tex](paper-tex/extracted/legacy/main.tex)

## Read Notes

- The compiler supports GPT-2, Qwen, Llama and Gemma examples and uses W4A8 block/dataflow generation on U55C. Reported metrics include total latency, TTFT and decode throughput.
- The source names input tokens and KV caches as dynamic tensors and uses maximum-shape hints. It does not expose a persistent append/read/position/reset protocol or a cross-call backend ABI at the granularity needed to verify llama.cpp-style state management.
- Its main system object is a generated Transformer block invoked with different layer weights; this demonstrates coarse-grained streaming and launch amortization, not a reusable native GGML runtime.
- Source-first read completed. A 2026-09-08 availability recheck found the author's
  [public API documentation](https://hanchenye.com/streamtensor/), but its linked
  `hanchenye/streamtensor` GitHub repository returned anonymous web/API 404. An
  accessible official implementation remains unverified; this does not prove
  nonexistence. See [[research/fpga-llm-inference/index|area index §Manuscript Recheck]].

Return to [[research/fpga-llm-inference/index#Paper Library|FPGA LLM paper library]].

## Model input and coverage audit (2026-09-15)

**Classification: Cross-architecture (paper).** GPT-2, Qwen, Llama and Gemma; block/phase evidence.

main.tex lines 951 and 1035–1065 report on-board experiments using Hugging Face models adapted for Torch-MLIR. All four families are compiled as transformer blocks and invoked with layer weights. This refutes a single-model-only classification, while adapted frontends and missing verified compiler source leave zero-porting deployment unestablished.

Classification uses the paper text and available public artifact; unavailable source is not treated as evidence of model restriction.

[Audit receipt](model-coverage-audit.json). See [[research/fpga-llm-inference/index#Model input and coverage audit (2026-09-15)|cross-paper comparison]] for definitions and input formats. This dated section supersedes older coverage/placement summaries where they conflict.

## Original-text verification (2026-09-27)

Checked against the original paper text or public code for the llama.cpp FPGA backend paper; supersedes earlier summaries where they differ.

- StreamTensor's GPT-2 comparison table is the original source of the DFX, Allo and StreamTensor rates later reprinted in CODO Table VI (`paper-tex/extracted/legacy/main.tex:892-906`): all values identical; setup U55C 250 MHz W4A8, Allo U280 250 MHz W4A8, DFX U280 200 MHz FP16 (main.tex:958-975).
- Tokens and KV caches are dynamic tensors that need maximum-shape hints (main.tex:941).

## Archive migration reading record (2026-10-09)

Preserves the historical reading record; this migration did not perform a new reading.

- Historical source: `tex`.
- Read path: `paper-tex/extracted/legacy/main.tex`.
- Recorded scope: Historical source-first reading recorded in index.md
- Recorded scope: Compiler and dataflow architecture, dynamic token/KV tensors, board evaluation and GPT-2 comparison table
- Full source/provenance snapshot: [citation.bib](citation.bib).

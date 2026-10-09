---
title: "Understanding the Potential of FPGA-Based Spatial Acceleration for Large Language Model Inference"
domain: research
area: fpga-llm-inference
type: paper
status: active
updated: 2026-09-15
tags: [paper, fpga, llm-inference]
---

# Understanding the Potential of FPGA-Based Spatial Acceleration for Large Language Model Inference

Spatial LLM develops an analytical model and a per-model spatial FPGA dataflow design. It is a
useful reference for separating prefill and decode resource/bandwidth behavior.

Repository availability recheck (2026-10-09): the complete `github-repo/` cache is absent in this checkout. Code links below use preserved `code-audit/` files where present or the official repository at the recorded commit; historical inspection does not imply a complete local cache today.

## Paper Meta

- Authors: Hongzheng Chen, Jiahao Zhang, Yixiao Du, Shaojie Xiang, Zichao Yue, Niansong Zhang, Yaohui Cai, Zhiru Zhang
- Year: 2024
- Venue: ACM Transactions on Reconfigurable Technology and Systems
- BibTeX key: `spatial_llm`
- Related Work category: FPGA Transformer and LLM systems
- Public record: [DOI](https://doi.org/10.1145/3656177); [arXiv](https://arxiv.org/abs/2312.15159)

## Local Assets

- Paper PDF: [2312.15159.pdf](paper-pdf/2312.15159.pdf) (28 pages; SHA-256 `75a69ed82c570491fb481fa149e635695cc0c583f071e7717a21931b131754cd`)
- arXiv source archive: [2312.15159-source.tar.gz](paper-tex/archives/2312.15159-source.tar.gz); extracted TeX: [3.2-modeling-constraints.tex](paper-tex/extracted/legacy/sections/3.2-modeling-constraints.tex), [5.2-accelerator.tex](paper-tex/extracted/legacy/sections/5.2-accelerator.tex)

## Read Notes

- The physical board result is GPT-2 on U280; LLaMA/Vicuna results in the paper are analytical rather than board demonstrations. The GPT-2 path uses W8A8 and reports separate prefill/decode performance and energy.
- The memory model explicitly buffers K and V and passes them to decode as the KV cache. It uses double buffering and discusses tiling KV on chip; this establishes a cache-aware accelerator design, not a framework-level runtime API.
- The paper's central lesson is that compute-intensive prefill and bandwidth-intensive decode need different allocation and scheduling choices. Its per-model spatial pipeline is not an unchanged GGML backend.
- Source-first paper read completed. On 2026-09-08, the paper-linked [Allo repository](https://github.com/cornell-zhang/allo/tree/8bafb0dcee27c96a72872184d2b106c59c8a1414) was archived at `8bafb0dcee27c96a72872184d2b106c59c8a1414`; [examples/README.md](https://github.com/cornell-zhang/allo/blob/8bafb0dcee27c96a72872184d2b106c59c8a1414/examples/README.md) explicitly links this paper and provides a kernel library/HLS-generation path. This does not establish release of the exact complete-generation controller. Dependencies and FPGA execution were not attempted; repository inspection remains partial.
- [[research/fpga-llm-inference/index|Area index §Evidence Matrix]] records phase-level evidence only (E2E —), no new-model entry (—), and kernel-library source (Public source ✓). BERT is not counted as a second generative checkpoint.

Return to [[research/fpga-llm-inference/index#Paper Library|FPGA LLM paper library]].

## Model input and coverage audit (2026-09-15)

**Classification: Reusable kernels; model-specific composition.** BERT and GPT-2 measured; larger LLaMA/Vicuna studies are not equivalent board evidence.

The paper-linked examples expose parameterized GEMM/attention/nonlinear kernels. transformer_hls.py instantiates dimensions and schedules, rather than loading an arbitrary checkpoint. Paper sections/4-sec-case-study.tex identifies BERT/GPT-2 board cases. This is reuse across models through composition, not a single fixed model and not an unchanged end-to-end model importer. The later Allo tree is supporting library evidence, not the exact experiment freeze.

Inspected code (pinned copies, not executed):

- [examples/README.md](code-audit/examples/README.md) — [upstream commit](https://github.com/cornell-zhang/allo/blob/8bafb0dcee27c96a72872184d2b106c59c8a1414/examples/README.md).
- [examples/transformer_hls.py](code-audit/examples/transformer_hls.py) — [upstream commit](https://github.com/cornell-zhang/allo/blob/8bafb0dcee27c96a72872184d2b106c59c8a1414/examples/transformer_hls.py).
- [allo/library/nn.py](code-audit/allo/library/nn.py) — [upstream commit](https://github.com/cornell-zhang/allo/blob/8bafb0dcee27c96a72872184d2b106c59c8a1414/allo/library/nn.py).
- [tests/test_nn.py](code-audit/tests/test_nn.py) — [upstream commit](https://github.com/cornell-zhang/allo/blob/8bafb0dcee27c96a72872184d2b106c59c8a1414/tests/test_nn.py).

[Audit receipt](model-coverage-audit.json). See [[research/fpga-llm-inference/index#Model input and coverage audit (2026-09-15)|cross-paper comparison]] for definitions and input formats. This dated section supersedes older coverage/placement summaries where they conflict.

## Original-text verification (2026-09-27)

Checked against the original paper text or public code for the llama.cpp FPGA backend paper; supersedes earlier summaries where they differ.

- The accelerator reads inputs from off-chip memory, stores results back after each layer, and fetches the next layer's parameters from the host (sections/5.2-accelerator.tex:17-21): not device-resident.
- GPT-2 board results use W8A8 (sections/6-experiments.tex); the 'Allo' GPT-2 rate of 204.05 token/s at W4A8, 250 MHz on U280 comes from StreamTensor's comparison table.

## Archive migration reading record (2026-10-09)

Preserves the historical reading record; this migration did not perform a new reading.

- Historical source: `tex`.
- Read path: `paper-tex/extracted/legacy/main.tex`.
- Read path: `paper-tex/extracted/legacy/sections/3.2-modeling-constraints.tex`.
- Read path: `paper-tex/extracted/legacy/sections/5.2-accelerator.tex`.
- Read path: `paper-tex/extracted/legacy/sections/6-experiments.tex`.
- Recorded scope: Historical source-first paper reading recorded in index.md
- Recorded scope: Modeling constraints, accelerator implementation, board evaluation and KV sections; Allo repository inspection remains partial
- Full source/provenance snapshot: [citation.bib](citation.bib).

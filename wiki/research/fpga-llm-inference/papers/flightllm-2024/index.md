---
title: "FlightLLM: Efficient Large Language Model Inference with a Complete Mapping Flow on FPGAs"
domain: research
area: fpga-llm-inference
type: paper
status: active
updated: 2026-09-15
tags: [paper, fpga, llm-inference]
---

# FlightLLM: Efficient Large Language Model Inference with a Complete Mapping Flow on FPGAs

FlightLLM presents a complete compiler-to-board mapping flow for generative LLMs on FPGA. The
paper is useful here as a system-level reference, not as a directly matched llama.cpp baseline.

## Paper Meta

- Authors: Shulin Zeng, Jun Liu, Guohao Dai, Xinhao Yang, Tianyu Fu, Hongyi Wang, Wenheng Ma, Hanbo Sun, Shiyao Li, Zixiao Huang, Yadong Dai, Jintao Li, Zehao Wang, Ruoyu Zhang, Kairui Wen, Xuefei Ning, Yu Wang
- Year: 2024
- Venue: Proceedings of the 2024 ACM/SIGDA International Symposium on Field Programmable Gate Arrays
- BibTeX key: `flightllm`
- Related Work category: FPGA Transformer and LLM systems
- Public record: [DOI](https://doi.org/10.1145/3626202.3637562); [arXiv](https://arxiv.org/abs/2401.03868)

## Local Assets

- Paper PDF: [2401.03868.pdf](2401.03868.pdf) (12 pages; SHA-256 `e0d38c8754516973d62749c846ebe63ea3984b569a1613b98340ef13249fd4da`)
- arXiv source archive: [2401.03868-source.tar.gz](source/archives/2401.03868-source.tar.gz); extracted TeX: [memory-hier.tex](source/extracted/content/memory-hier.tex), [evaluation.tex](source/extracted/content/evaluation.tex)

## Read Notes

- Physical evaluation uses U280 for OPT-6.7B and LLaMA2-7B at batch 1; the paper reports a 225 MHz implementation and end-to-end latency, decode throughput and energy.
- The memory section explicitly places large single-access objects, including weights and KV cache, in HBM, while small lookup tables use DDR. Decode activations are fused and kept on chip to reduce repeated off-chip accesses.
- This is persistent KV support at the model-system level; absence of a llama.cpp-style cache-position/append ABI does not remove that credit. Its generality is a compiler/mapping flow with model-specific instructions and prepared weights, not a native framework backend. Whether the exact released xclbin is reusable across additional models requires artifact validation; model-specific compilation alone does not imply mandatory bitstream regeneration.
- Source-first paper read completed. The public artifact has now been partially inspected; this does not establish independent reproduction or a matched result for the current backend.

## Artifact Audit (2026-09-08)

- Official [Zenodo record 10462167](https://zenodo.org/records/10462167): the top-level [README](supplementary/zenodo-10462167/README.md) explicitly withholds RTL as Infinigence-AI IP.
- Fully cached/extracted [profile.zip](supplementary/zenodo-10462167/profile.zip). Its README and `run.py` show that VHK158 timings come from an instruction simulator/profiler and CSV aggregation; only the GPU branch calls Transformers/vLLM generation. VHK158 is also explicitly simulation in the paper, unlike U280.
- The 6.41 GB hardware ZIP was not fully downloaded. HTTP range reads retained its [complete manifest](supplementary/zenodo-10462167/hardware-zip-manifest.json), [internal README](supplementary/zenodo-10462167/hardware-selected/fpga_implementation/README.md), host binary and two case configurations. The README invokes a precompiled case and compares binary outputs with goldens; this is not a documented prompt-to-text interface.
- No board run, complete package reproduction, or RTL-source reproduction was performed. See [[research/fpga-llm-inference/index|area index §Evidence Matrix]] for table marks, missing members and the distinction between paper generation claims and the public demo.

## Model-File Deployment Boundary

The 2026-09-08 manuscript revision replaced Multi-model evaluation with Model-file deployment
(now named New-model entry in [[research/fpga-llm-inference/index|the area index]]): a new supported
LLM checkpoint should enter through files/configuration without writing per-model exporters,
graph descriptions, compiler, hardware or host code. Automatic builds remain allowed.
FlightLLM's [mapping flow](source/extracted/content/software.tex) explicitly describes automatic
PyTorch structure parsing and IR/instruction generation, so Auto map retains its check.
The [artifact README](supplementary/zenodo-10462167/README.md), however, supplies precompiled
cases and refers generation of different cases to the authors' Infinigence-AI environment.
The reviewed package therefore does not establish a user-accessible new-checkpoint entry.
Its two named hardware demo directories denote decode lengths, not proof of a two-model
architectural limit. Preserve the paper's OPT/LLaMA2 evaluation while marking the new
model-file deployment predicate as unestablished. The local backend plan targets any GGUF
within the declared framework, operator/format and device-capacity envelope; this is a future
requirement, not current support for arbitrary GGUFs.

Return to [[research/fpga-llm-inference/papers/index|FPGA LLM paper library]].

## Model input and coverage audit (2026-09-15)

**Classification: Cross-architecture (paper).** OPT-6.7B and LLaMA2-7B.

content/software.tex describes automatic structure parsing and ISA generation with manually defined templates; content/evaluation.tex names both families and their U280 results. The public hardware artifact consists of prepared cases, while the source frontend/RTL is not available in that package. Thus paper-level cross-architecture coverage is supported; arbitrary checkpoint acceptance is not established by public code.

Classification uses the paper text and available public artifact; unavailable source is not treated as evidence of model restriction.

[Audit receipt](source/model-coverage-audit.json). See [[research/fpga-llm-inference/index#Model input and coverage audit (2026-09-15)|cross-paper comparison]] for definitions and input formats. This dated section supersedes older coverage/placement summaries where they conflict.

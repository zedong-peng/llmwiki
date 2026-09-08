---
title: "DFX: A Low-latency Multi-FPGA Appliance for Accelerating Transformer-based Text Generation"
domain: research
area: fpga-llm-inference
type: paper
status: processed
updated: 2026-09-07
tags: [paper, fpga, llm-inference]
---

# DFX: A Low-latency Multi-FPGA Appliance for Accelerating Transformer-based Text Generation

> Bibliographic record and local public asset cache. Full paper notes are pending.

## Paper Meta

- Authors: Seongmin Hong, Seungjae Moon, Junsoo Kim, Sungjae Lee, Minsub Kim, Dongsoo Lee, Joo-Young Kim
- Year: 2022
- Venue: Proceedings of the 55th IEEE/ACM International Symposium on Microarchitecture
- BibTeX key: `dfx`
- Related Work category: FPGA Transformer and LLM systems
- Public record: [DOI](https://doi.org/10.1109/MICRO56248.2022.00051); [arXiv](https://arxiv.org/abs/2209.10797)

## Local Assets

- Paper PDF: [2209.10797.pdf](2209.10797.pdf) (15 pages; SHA-256 `d817b30f1ac63d3b238e0d05e0db370eb6423c5e05c1df98879327b465c44cd0`)
- arXiv source archive: [2209.10797-source.tar.gz](source/archives/2209.10797-source.tar.gz) (SHA-256 `b1f7ed1b60ac5ab0466402856811d2a90d57af4164fd8c16e5efbef09052e99b`); extracted TeX: [4_architecture.tex](source/extracted/4_architecture.tex), [5_microarchitecture.tex](source/extracted/5_microarchitecture.tex), [6_evaluation.tex](source/extracted/6_evaluation.tex)

## Read Notes

- DFX is a custom GPT appliance with an ISA, model-parallel multi-FPGA execution and a complete GPT-2 text-generation path. The physical evaluation covers GPT-2 345M, 774M and 1.5B on U280 configurations.
- The source explicitly states that DMA loads/stores tiled weights, `Key` and `Value` to/from HBM. The generation controller tracks layer, input/output token counts and masking position; this is evidence of model-level persistent K/V use, although it is not a reusable llama.cpp cache-position ABI.
- The paper uses FP16 operators and reports model-level text-generation latency, throughput and energy. Its results are useful as a complete-generation reference, not as a matched throughput baseline for the current Q4/Q6 llama.cpp profile.
- Source-first read completed; no code repository was requested.

Return to [[research/fpga-llm-inference/papers/index|FPGA LLM paper library]].

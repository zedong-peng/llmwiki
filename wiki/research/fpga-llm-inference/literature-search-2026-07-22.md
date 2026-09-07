---
title: FPGA LLM Inference Literature Search, 2026-07-22
domain: research
area: fpga-llm-inference
type: note
status: active
updated: 2026-07-24
tags: [literature-search, fpga, llm-inference, provenance]
---

# FPGA LLM Inference Literature Search, 2026-07-22

## Overview

Search window: 2018-2026.

Broad queries:

- `FPGA large language model inference end-to-end`
- `FPGA GPT autoregressive inference prefill decode`
- `FPGA transformer accelerator LLM HBM quantization`
- `FPGA LLM compiler runtime`

The initial `paper-search` run queried arXiv, DBLP, OpenAlex, OpenReview, Semantic Scholar and Crossref. It returned 80 Crossref records, deduplicated to 76, but most were lexical false positives around generic “end-to-end”, “runtime” or non-FPGA LLM applications. A second pass used exact-title DBLP queries, DOI records, arXiv full text and the references from the private FPGA draft. On 2026-07-23, a five-query high-recall sweep and backward-reference pass expanded the deployment, quantization, distributed, long-context and model-family coverage. The core and extended corpora below include only works whose identity and relevance were verified.

## Connector Results And Errors

| Source | Broad-query outcome | Follow-up |
|---|---|---|
| Crossref | 80 hits / 76 unique; high recall, very low precision | exact DOI records used for venue/citation metadata |
| DBLP | zero hits for broad multi-term queries | exact-title searches recovered DFX, FlightLLM, EdgeLLM, StreamTensor, TeLLMe and others |
| arXiv API | HTTP 429, then 503/proxy disconnects | direct known-ID PDF downloads succeeded |
| OpenAlex | `401 Client Error: Unauthorized` | not used for factual claims |
| OpenReview | invalid configured credentials, then HTTP 429 | not needed for the hardware venue set |
| Semantic Scholar | `403 Client Error: Forbidden` | not used for factual claims |

These failures matter because the broad search is not a complete bibliometric census. The 2026-07-23 five-query rerun returned 125 raw Crossref hits and eight DBLP hits; arXiv API, OpenAlex, OpenReview and Semantic Scholar failed again with the recorded 429/proxy, 401, credential/rate-limit and 403 errors. Direct arXiv HTML metadata, DBLP exact-title records and DOI metadata supplied the expanded corpus. The resulting landscape is a high-recall verified reading set, not a claim that every lexical API hit is relevant.

## Core Verified Corpus

| Work | Year | Venue | Stable source | Why retained |
|---|---:|---|---|---|
| FTRANS | 2020 | ISLPED | [DOI](https://doi.org/10.1145/3370748.3406567) | early FPGA Transformer co-design |
| Sanger | 2021 | MICRO | [DOI](https://doi.org/10.1145/3466752.3480125) | sparse-attention algorithm/hardware co-design |
| DFX | 2022 | MICRO | [arXiv 2209.10797](https://arxiv.org/abs/2209.10797) | complete GPT-2 text-generation appliance |
| FlightLLM | 2024 | FPGA | [arXiv 2401.03868](https://arxiv.org/abs/2401.03868) | complete 7B mapping flow and strong GPU comparison |
| Spatial LLM | 2024/2025 | TRETS | [arXiv 2312.15159](https://arxiv.org/abs/2312.15159) | prefill/decode analytical and spatial-design foundation |
| GLITCHES | 2024 | HPEC | [DOI](https://doi.org/10.1109/HPEC62836.2024.10938498) | GPU-FPGA stage collaboration |
| EdgeLLM | 2025 | IEEE TCAS-I | [arXiv 2407.21325](https://arxiv.org/abs/2407.21325) | whole-model CPU-FPGA compiler/runtime |
| Embedded LLaMA2-7B decode | 2025 | DATE | [arXiv 2502.10659](https://arxiv.org/abs/2502.10659) | bandwidth/capacity limit on KV260 |
| BAQET | 2025 | FPGA | [DOI](https://doi.org/10.1145/3706628.3708849) | BRAM-aware quantization and streaming |
| SpeedLLM | 2025 | HPDC | [arXiv 2507.14139](https://arxiv.org/abs/2507.14139) | fusion/memory-reuse system on U280 |
| StreamTensor | 2025 | MICRO | [arXiv 2509.13694](https://arxiv.org/abs/2509.13694) | compiler-generated whole-block streaming |
| CODO | 2026 | ISCA | [arXiv 2604.12618](https://arxiv.org/abs/2604.12618) | priority GPT-2 TTFT/decode compiler baseline |
| TeLLMe v2 | 2026 | FPGA | [arXiv 2510.15926](https://arxiv.org/abs/2510.15926) | full prefill/decode on low-power edge FPGA |
| FAST-Prefill | 2026 | FCCM | [arXiv 2602.20515](https://arxiv.org/abs/2602.20515) | long-context sparse-prefill specialization |
| LUT-LLM | 2026 | FCCM | [DOI](https://doi.org/10.1109/FCCM68464.2026.00027) | memory/LUT-based LLM computation |
| Hummingbird+ | 2026 | FPGA | [DOI](https://doi.org/10.1145/3748173.3779189) | prototype-to-edge-product perspective |

## Extended Verified Corpus

This extension favors recall across FPGA LLM systems while keeping operator-only, generic Transformer and serving-coprocessor work visibly labeled rather than conflating all entries with complete generation systems.

| Work | Year | Scope | Stable source |
|---|---:|---|---|
| Scalable GPT-2 architecture | 2023 | parameterized GPT-2 inference hardware | [DOI](https://doi.org/10.1109/IJCNN54540.2023.10191067) |
| Multi-FPGA large-Transformer feasibility | 2024 | six-FPGA I-BERT proof and mapping tools | [arXiv 2404.16158](https://arxiv.org/abs/2404.16158) |
| HLSTransform | 2024 | HLS Llama 2 accelerator | [arXiv 2405.00738](https://arxiv.org/abs/2405.00738) |
| LlamaF | 2024 | TinyLlama on embedded FPGA | [DOI](https://doi.org/10.1109/WF-IOT62078.2024.10811385) |
| InTRRA | 2025 | inter-task resource repurposing for Transformer inference | [DOI](https://doi.org/10.1145/3706628.3708828) |
| METAL | 2025 | long-context Transformer memory architecture | [DOI](https://doi.org/10.1109/ASAP65064.2025.00023) |
| LoopLynx | 2025 | hybrid spatial-temporal, dual-FPGA GPT-2 | [DOI](https://doi.org/10.23919/DATE64628.2025.10993078) |
| MEADOW | 2025 | low-power prefill/decode dataflow and packing | [arXiv 2503.11663](https://arxiv.org/abs/2503.11663) |
| TerEffic | 2025 | ternary LLM, on-chip and HBM configurations | [arXiv 2502.16473](https://arxiv.org/abs/2502.16473) |
| LightMamba | 2025 | quantized Mamba FPGA accelerator | [arXiv 2502.15260](https://arxiv.org/abs/2502.15260) |
| AccLLM | 2025 | compressed long-context inference | [arXiv 2505.03745](https://arxiv.org/abs/2505.03745) |
| QLlama | 2025 | microscaling Llama 2 quantization | [DOI](https://doi.org/10.1109/LES.2025.3600563) |
| MoE-OPU | 2025 | expert-parallel MoE overlay | [DOI](https://doi.org/10.1109/ICCAD66269.2025.11240807) |
| LLM on FPGA | 2025 | quantization plus multi-query attention | [DOI](https://doi.org/10.1109/ISOCC66390.2025.11329964) |
| Robotics FPGA LLM inference | 2025 | real-time decision-making deployment | [DOI](https://doi.org/10.1109/IROS60139.2025.11247019) |
| TENET | 2025 | sparse LUT-centric ternary inference | [arXiv 2509.13765](https://arxiv.org/abs/2509.13765) |
| PD-Swap | 2025 | dynamic partial reconfiguration across prefill/decode | [arXiv 2512.11550](https://arxiv.org/abs/2512.11550) |
| CXL-SpecKV | 2025 | FPGA disaggregated KV-cache coprocessor | [arXiv 2512.11920](https://arxiv.org/abs/2512.11920) |
| Integer-only full fusion | 2025 | generic Transformer operator fusion | [DOI](https://doi.org/10.1109/ICCD65941.2025.00020) |
| FlexLLM | 2026 | composable HLS library and stage-customized Llama system | [arXiv 2601.15710](https://arxiv.org/abs/2601.15710) |
| LORA | 2026 | recurrent multi-FPGA architecture and communication | [DOI](https://doi.org/10.1109/TCAD.2025.3629537) |
| TeraFly | 2026 | cooperative multinode FPGA inference | [DOI](https://doi.org/10.1109/TCAD.2025.3616078) |
| TFLOP | 2026 | unified LUT optimization for LLM inference | [DOI](https://doi.org/10.1109/ASP-DAC66049.2026.11420766) |
| dLLM-OPU | 2026 | diffusion language-model overlay | [DOI](https://doi.org/10.1109/ASP-DAC66049.2026.11420284) |
| SkipOPU | 2026 | dynamically allocated token/layer computation | [arXiv 2603.14785](https://arxiv.org/abs/2603.14785) |
| XtraMAC | 2026 | mixed-precision operator substrate | [arXiv 2605.06052](https://arxiv.org/abs/2605.06052) |
| ELiTeFormer | 2026 | linear-attention/ternary algorithm-hardware co-design | [arXiv 2607.03652](https://arxiv.org/abs/2607.03652) |

## Trends

1. **2020-2022: operator co-design to complete generation.** FTRANS/Sanger focus on Transformer kernels and sparse attention; DFX is the transition to embeddings, decoder, LM head and autoregressive generation as one appliance.
2. **2023-2024: mapping flows and spatial-vs-overlay debate.** FlightLLM and Spatial LLM make model compilation, precision, residency and prefill/decode asymmetry central.
3. **2025: compiler/runtime and deployment diversity.** EdgeLLM, StreamTensor, embedded LLaMA2, BAQET and SpeedLLM cover heterogeneous systems, whole-block streaming, bandwidth-saturated edge decode and quantization.
4. **2026: coarse-grained automation and phase-specialized endpoints.** CODO targets comprehensive dataflow legality/optimization; TeLLMe handles both phases under 5 W; FAST-Prefill specializes for long contexts.
5. **The unit of optimization is growing.** Competitive systems optimize a block, phase or request. Isolated operator speed remains supporting evidence, not the system claim.

## Key Themes

| Theme | Description | Representative works |
|---|---|---|
| complete model mapping | cover embeddings/blocks/LM head or all model layers | DFX, FlightLLM, EdgeLLM |
| block/graph dataflow | fuse operators and keep intermediates on chip | Spatial LLM, StreamTensor, CODO |
| prefill/decode asymmetry | different compute/memory regimes require different strategies | Spatial LLM, TeLLMe, FAST-Prefill |
| quantization/sparsity | precision and model transformation must have matching datapaths | FlightLLM, BAQET, TeLLMe, LUT-LLM |
| memory topology/residency | effective HBM/DDR behavior controls decode | FlightLLM, EdgeLLM, embedded LLaMA2 |
| framework/compiler boundary | productivity and model portability compete with specialization | EdgeLLM, StreamTensor, CODO, current GGML backend |

## Keyword Frequency In Verified Titles

Normalized counts over the 16-title core set; the extended sweep is kept separate so this initial snapshot remains reproducible:

| Keyword | Count |
|---|---:|
| FPGA/FPGAs | 14 |
| LLM / language model | 12 |
| inference | 9 |
| accelerator/acceleration | 8 |
| dataflow/compiler/mapping | 5 |

## Citation Snapshot

Crossref `is-referenced-by-count`, queried 2026-07-22; counts are index-dependent and not used as quality scores.

| Rank | Work | Count |
|---:|---|---:|
| 1 | FlightLLM | 122 |
| 2 | DFX | 105 |
| 3 | EdgeLLM | 59 |

The remaining recent 2025-2026 papers are too new for a meaningful citation ranking.

## First-Author Snapshot

The retained set has little repeated first-author overlap; citation aggregation mostly reproduces the paper ranking.

| Rank | First author | Papers in set | Indexed citations |
|---:|---|---:|---:|
| 1 | Shulin Zeng | 1 | 122 |
| 2 | Seongmin Hong | 1 | 105 |
| 3 | Mingqiang Huang | 1 | 59 |

## Priority Reading Path

1. **DFX**: learn what a defensible “GPT end-to-end” claim includes.
2. **FlightLLM**: understand a modern 7B model-to-FPGA mapping flow and always-on-chip decode.
3. **Spatial LLM**: derive the prefill/decode compute-bandwidth model before reading more systems.
4. **StreamTensor**: inspect why whole-block fusion and FIFO sizing beat manually assembled graph boundaries.
5. **CODO**: focus on dataflow violation elimination, communication optimization, GPT-2 Table VI and artifact boundaries.
6. **EdgeLLM**: compare its CPU-FPGA compiler/runtime abstraction with a native GGML backend.
7. **TeLLMe**: use as an example of explicit heterogeneous boundary and complete prefill/decode reporting.

## Search-Derived Judgment

The current project is not missing another list of FPGA kernels. It is missing a coarse-grained execution mechanism that can preserve GGML semantics while approaching the block-level streaming granularity used by StreamTensor and CODO. This is the point where the literature most directly changes the engineering plan.

## Source Provenance

- Multi-source search executed with the Microsoft ResearchStudio `paper-search` skill; the 2026-07-23 expansion used five unioned FPGA/LLM queries with 2020-2026 coverage and exact-title follow-up.
- Public PDFs read locally for arXiv `2209.10797`, `2312.15159`, `2401.03868`, `2407.21325`, `2502.10659`, `2507.14139`, `2509.13694`, `2510.15926`, `2602.20515`, and `2604.12618`.
- CODO artifacts inspected from official GitHub commit `130b12bc63e6e6daa31a1227b7e8391c5039148d`, the `isca2026-ae` tag, and Zenodo `10.5281/zenodo.19425920`; the Docker v1 registry metadata was checked without downloading its 6.2 GB image layers.
- The private draft bibliography was used as a discovery seed; public DOI/arXiv records were used to verify paper identity.
- The expanded corpus was integrated into the private manuscript's Related Work as six categories plus a capability matrix; the wiki retains bibliographic synthesis rather than manuscript text.
- [[research/fpga-llm-inference/papers/index]] materializes all 68 Related Work citations as per-paper records. The 2026-07-24 pass cached 48 title-validated public full-paper PDFs and retained explicit metadata-only status for the 20 entries without a verified open copy.

## Related Pages

- [[research/fpga-llm-inference/system-landscape]]
- [[research/fpga-llm-inference/codo-2026]]
- [[research/fpga-llm-inference/foundations]]
- [[research/fpga-llm-inference/papers/index]]

返回 [[research/fpga-llm-inference/index]]。

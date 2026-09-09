---
title: FPGA LLM Inference Paper Library
domain: research
area: fpga-llm-inference
type: overview
status: active
updated: 2026-09-08
tags: [papers, fpga, llm-inference, related-work]
---

# FPGA LLM Inference Paper Library

This directory materializes the 68 papers cited by the manuscript's Related Work section plus 15 direct additions from the 2026-07-28 architecture search and SECDA-LLM from the 2026-09-08 framework-integration audit. It uses one directory per paper, matching the repository's agent-memory, HLS and linear-attention collections.

## Coverage

| Item | Count |
|---|---:|
| Original Related Work papers | 68 |
| Direct architecture-search additions | 15 |
| Framework-integration audit additions | 1 |
| Total paper records | 84 |
| Validated full-paper PDFs | 51 |
| Author presentation only | 0 |
| Metadata only | 33 |

A downloaded PDF must be publicly reachable, begin with a valid PDF signature, open successfully, contain at least two pages, and match the cited title. Publisher HTML, access-denied pages, ResearchGate/Scribd copies and unmatched search results are not accepted. A missing PDF means only that no verified public copy was found in this pass; the DOI record remains indexed.

## Layout

- `<paper-slug>/index.md`: seed paper page and provenance.
- `<paper-slug>/metadata.yaml`: machine-readable identity, links, download status and validation.
- `<paper-slug>/*.pdf`: validated public paper PDF, when available.
- `manifest.yaml`: collection-wide status.
- `related-work.bib`: the exact 68-entry citation subset.
- `checksums.sha256`: integrity hashes for every cached PDF asset and the selected source archives.

Most source archives and code repositories remain deferred. This pass completed source-first reading
for the five papers most relevant to the current runtime-boundary question: DFX, FlightLLM, Spatial LLM,
StreamTensor and CODO. Their archives and extracted trees live under the corresponding paper
directories; the per-paper metadata records the exact status.

The resulting cross-paper distinction is summarized in
[[research/fpga-llm-inference/kv-cache-runtime-boundary-comparison]]: K/V computation, persistent
cross-token state and KV-specific physical optimization are separate evidence items, as are
fixed-graph kernel latency and a complete stateful generation request.

The 2026-07-28 additions are selected from the unfiltered six-query union search (241 source records deduplicated to 142; see [[research/fpga-llm-inference/index]] Literature Provenance for method, admission rule and the 15-record table); they are not claimed to be manuscript citations.

The 2026-09-08 update adds [[secda-llm-2024/index|SECDA-LLM]] after reading its full TeX paper and
bibliography. Its official repository and two exact gitlink dependencies are pinned and archived;
backend/KV inspection is targeted and does not establish a reproduced build. Original Hummingbird's
source is archived for targeted thematic review and remains unprocessed. The revised nine-system
comparison plus local backend row and selection rationale are in [[research/fpga-llm-inference/feature-level-evidence-matrix]].

## Catalog

| Paper | Year | Related Work category | Cache status | Canonical source |
|---|---:|---|---|---|
| [[secda-llm-2024/index|SECDA-LLM: Designing Efficient LLM Accelerators for Edge Devices]] | 2024 | Framework-integrated FPGA LLM inference | `processed; code audit partial` | arXiv 2408.00462 |
| [[ftrans-2020/index|FTRANS: Energy-Efficient Acceleration of Transformers using FPGA]] | 2020 | FPGA Transformer and LLM systems | `downloaded` | arXiv 2007.08563 |
| [[sanger-2021/index|Sanger: A Co-Design Framework for Enabling Sparse Attention using Reconfigurable Architecture]] | 2021 | FPGA Transformer and LLM systems | `downloaded` | DOI `10.1145/3466752.3480125` |
| [[dfx-2022/index|DFX: A Low-latency Multi-FPGA Appliance for Accelerating Transformer-based Text Generation]] | 2022 | FPGA Transformer and LLM systems | `processed` | arXiv 2209.10797 |
| [[flightllm-2024/index|FlightLLM: Efficient Large Language Model Inference with a Complete Mapping Flow on FPGAs]] | 2024 | FPGA Transformer and LLM systems | `processed` | arXiv 2401.03868 |
| [[spatial-llm-2024/index|Understanding the Potential of FPGA-Based Spatial Acceleration for Large Language Model Inference]] | 2024 | FPGA Transformer and LLM systems | `processed` | arXiv 2312.15159 |
| [[edgellm-2025/index|EdgeLLM: A Highly Efficient CPU-FPGA Heterogeneous Edge Accelerator for Large Language Models]] | 2025 | FPGA Transformer and LLM systems | `processed` | arXiv 2407.21325 |
| [[glitches-2024/index|GLITCHES: GPU-FPGA LLM Inference Through a Collaborative Heterogeneous System]] | 2024 | FPGA Transformer and LLM systems | `downloaded` | DOI `10.1109/HPEC62836.2024.10938498` |
| [[streamtensor-2025/index|StreamTensor: Make Tensors Stream in Dataflow Accelerators for LLMs]] | 2025 | FPGA Transformer and LLM systems | `processed` | arXiv 2509.13694 |
| [[codo-2026/index|CODO: An Automated Compiler for Comprehensive Dataflow Optimization]] | 2026 | FPGA Transformer and LLM systems | `processed` | arXiv 2604.12618 |
| [[tellme-v2-2026/index|TeLLMe: An Efficient End-to-End Ternary LLM Prefill and Decode Accelerator with Table-Lookup Matmul on Edge FPGAs]] | 2026 | FPGA Transformer and LLM systems | `downloaded` | arXiv 2510.15926 |
| [[fast-prefill-2026/index|FAST-Prefill: FPGA Accelerated Sparse Attention for Long Context LLM Prefill]] | 2026 | FPGA Transformer and LLM systems | `downloaded` | arXiv 2602.20515 |
| [[flexllm-hls-2026/index|FlexLLM: Composable HLS Library for Flexible Hybrid LLM Accelerator Design]] | 2026 | FPGA Transformer and LLM systems | `downloaded` | arXiv 2601.15710 |
| [[hummingbird-plus-2026/index|Hummingbird+: Advancing FPGA-Based LLM Deployment from Research Prototype to Edge Product]] | 2026 | FPGA Transformer and LLM systems | `metadata-only` | DOI `10.1145/3748173.3779189` |
| [[lut-llm-2026/index|LUT-LLM: Efficient Language Model Inference with Memory-Based Computations on FPGAs]] | 2026 | FPGA Transformer and LLM systems | `downloaded` | arXiv 2511.06174 |
| [[pd-swap-2025/index|PD-Swap: Prefill-Decode Logic Swapping for End-to-End LLM Inference on Edge FPGAs via Dynamic Partial Reconfiguration]] | 2025 | FPGA Transformer and LLM systems | `downloaded` | arXiv 2512.11550 |
| [[scalable-gpt2-2023/index|A Scalable GPT-2 Inference Hardware Architecture on FPGA]] | 2023 | Multi-FPGA and distributed inference | `metadata-only` | DOI `10.1109/IJCNN54540.2023.10191067` |
| [[multi-fpga-transformer-2024/index|The Feasibility of Implementing Large-Scale Transformers on Multi-FPGA Platforms]] | 2024 | Multi-FPGA and distributed inference | `downloaded` | arXiv 2404.16158 |
| [[looplynx-2025/index|LoopLynx: A Scalable Dataflow Architecture for Efficient LLM Inference]] | 2025 | Multi-FPGA and distributed inference | `downloaded` | arXiv 2504.09561 |
| [[lora-2026/index|LORA: A Latency-Oriented Recurrent Architecture for Large Language Model on Multi-FPGA Platform With Communication Optimization]] | 2026 | Multi-FPGA and distributed inference | `metadata-only` | DOI `10.1109/TCAD.2025.3629537` |
| [[terafly-2026/index|TeraFly: A Multinode FPGA-Based Accelerator Design for Efficient Cooperative Inference in LLMs]] | 2026 | Multi-FPGA and distributed inference | `metadata-only` | DOI `10.1109/TCAD.2025.3616078` |
| [[hlstransform-2024/index|HLSTransform: Energy-Efficient Llama 2 Inference on FPGAs Via High Level Synthesis]] | 2024 | Embedded and low-bit LLM deployment | `downloaded` | arXiv 2405.00738 |
| [[llamaf-2024/index|LlamaF: An Efficient Llama2 Architecture Accelerator on Embedded FPGAs]] | 2024 | Embedded and low-bit LLM deployment | `downloaded` | arXiv 2409.11424 |
| [[embedded-bw-2025/index|Pushing up to the Limit of Memory Bandwidth and Capacity Utilization for Efficient LLM Decoding on Embedded FPGA]] | 2025 | Embedded and low-bit LLM deployment | `downloaded` | arXiv 2502.10659 |
| [[meadow-2025/index|MEADOW: Memory-Efficient Dataflow and Data Packing for Low Power Edge LLMs]] | 2025 | Embedded and low-bit LLM deployment | `downloaded` | arXiv 2503.11663 |
| [[hummingbird-2025/index|Hummingbird: A Smaller and Faster Large Language Model Accelerator on Embedded FPGA]] | 2025 | Embedded and low-bit LLM deployment | `downloaded` | arXiv 2507.03308 |
| [[qllama-2025/index|QLlama: An FPGA-Based Microscaling Quantization Accelerator for Energy-Efficient Llama2 Inference]] | 2025 | Embedded and low-bit LLM deployment | `metadata-only` | DOI `10.1109/LES.2025.3600563` |
| [[tereffic-2025/index|TerEffic: Highly Efficient Ternary LLM Inference on FPGA]] | 2025 | Embedded and low-bit LLM deployment | `downloaded` | arXiv 2502.16473 |
| [[tenet-2025/index|TENET: An Efficient Sparsity-Aware LUT-Centric Architecture for Ternary LLM Inference on Edge]] | 2025 | Embedded and low-bit LLM deployment | `downloaded` | arXiv 2509.13765 |
| [[tflop-2026/index|TFLOP: Towards Energy-Efficient LLM Inference, an FPGA-Affinity Accelerator with Unified LUT-Based Optimization]] | 2026 | Embedded and low-bit LLM deployment | `metadata-only` | DOI `10.1109/ASP-DAC66049.2026.11420766` |
| [[llm-on-fpga-2025/index|LLM on FPGA: Squeezing Language Models by Quantization and Multi-Query Attention and Its Efficient Hardware Architecture]] | 2025 | Embedded and low-bit LLM deployment | `metadata-only` | DOI `10.1109/ISOCC66390.2025.11329964` |
| [[robot-llm-fpga-2025/index|Computationally Efficient FPGA-Based Large Language Model Inference for Real-Time Decision-Making in Robotic Systems]] | 2025 | Embedded and low-bit LLM deployment | `metadata-only` | DOI `10.1109/IROS60139.2025.11247019` |
| [[accllm-2025/index|AccLLM: Accelerating Long-Context LLM Inference Via Algorithm-Hardware Co-Design]] | 2025 | Long-context and phase-specialized acceleration | `downloaded` | arXiv 2505.03745 |
| [[metal-2025/index|METAL: A Memory-Efficient Transformer Architecture for Long-Context Inference on FPGA]] | 2025 | Long-context and phase-specialized acceleration | `metadata-only` | DOI `10.1109/ASAP65064.2025.00023` |
| [[cxl-speckv-2025/index|CXL-SpecKV: A Disaggregated FPGA Speculative KV-Cache for Datacenter LLM Serving]] | 2025 | Long-context and phase-specialized acceleration | `downloaded` | arXiv 2512.11920 |
| [[eliteformer-2026/index|ELiTeFormer: An Efficient Transformer for FPGAs]] | 2026 | Long-context and phase-specialized acceleration | `downloaded` | arXiv 2607.03652 |
| [[transformer-opu-2023/index|Transformer-OPU: An FPGA-based Overlay Processor for Transformer Networks]] | 2023 | Programmable and specialized FPGA execution | `metadata-only` | DOI `10.1109/FCCM57271.2023.00049` |
| [[fet-opu-2023/index|FET-OPU: A Flexible and Efficient FPGA-Based Overlay Processor for Transformer Networks]] | 2023 | Programmable and specialized FPGA execution | `metadata-only` | DOI `10.1109/ICCAD57390.2023.10323752` |
| [[cstrans-opu-2024/index|CSTrans-OPU: An FPGA-based Overlay Processor with Full Compilation for Transformer Networks via Sparsity Exploration]] | 2024 | Programmable and specialized FPGA execution | `metadata-only` | DOI `10.1145/3649329.3657325` |
| [[chatopu-2024/index|ChatOPU: An FPGA-based Overlay Processor for Large Language Models with Unstructured Sparsity]] | 2024 | Programmable and specialized FPGA execution | `metadata-only` | DOI `10.1145/3676536.3676761` |
| [[moe-opu-2025/index|MoE-OPU: An FPGA Overlay Processor Leveraging Expert Parallelism for MoE-Based Large Language Models]] | 2025 | Programmable and specialized FPGA execution | `metadata-only` | DOI `10.1109/ICCAD66269.2025.11240807` |
| [[dllm-opu-2026/index|dLLM-OPU: An FPGA Overlay Processor for Accelerated Diffusion Large Language Models]] | 2026 | Programmable and specialized FPGA execution | `metadata-only` | DOI `10.1109/ASP-DAC66049.2026.11420284` |
| [[skipopu-2026/index|SkipOPU: An FPGA-Based Overlay Processor for Large Language Models with Dynamically Allocated Computation]] | 2026 | Programmable and specialized FPGA execution | `downloaded` | arXiv 2603.14785 |
| [[lightmamba-2025/index|LightMamba: Efficient Mamba Acceleration on FPGA with Quantization and Hardware Co-Design]] | 2025 | Programmable and specialized FPGA execution | `downloaded` | arXiv 2502.15260 |
| [[graphagile-2023/index|GraphAGILE: An FPGA-Based Overlay Accelerator for Low-Latency GNN Inference]] | 2023 | Programmable and specialized FPGA execution | `downloaded` | arXiv 2302.01769 |
| [[runtime-adaptive-transformer-2026/index|A Runtime-Adaptive Transformer Neural Network Accelerator on FPGAs]] | 2026 | Programmable and specialized FPGA execution | `downloaded` | arXiv 2411.18148 |
| [[flame-2024/index|FLAME: Fully Leveraging MoE Sparsity for Transformer on FPGA]] | 2024 | Programmable and specialized FPGA execution | `metadata-only` | DOI `10.1145/3649329.3656507` |
| [[baqet-2025/index|BAQET: BRAM-aware Quantization for Efficient Transformer Inference via Stream-based Architecture on an FPGA]] | 2025 | Programmable and specialized FPGA execution | `metadata-only` | DOI `10.1145/3706628.3708849` |
| [[speedllm-2025/index|SpeedLLM: An FPGA Co-design of Large Language Model Inference Accelerator]] | 2025 | Programmable and specialized FPGA execution | `downloaded` | arXiv 2507.14139 |
| [[xtramac-2026/index|XtraMAC: An Efficient MAC Architecture for Mixed-Precision LLM Inference on FPGA]] | 2026 | Programmable and specialized FPGA execution | `downloaded` | arXiv 2605.06052 |
| [[scalehls-2022/index|ScaleHLS: A New Scalable High-Level Synthesis Framework on Multi-Level Intermediate Representation]] | 2022 | Composable accelerator compilation | `downloaded` | arXiv 2107.11673 |
| [[tapa-2023/index|TAPA: A Scalable Task-parallel Dataflow Programming Framework for Modern FPGAs with Co-optimization of HLS and Physical Design]] | 2023 | Composable accelerator compilation | `downloaded` | arXiv 2209.02663 |
| [[allo-2024/index|Allo: A Programming Model for Composable Accelerator Design]] | 2024 | Composable accelerator compilation | `downloaded` | arXiv 2404.04815 |
| [[intrra-2025/index|InTRRA: Inter-Task Resource-Repurposing Accelerator for Efficient Transformer Inference on FPGAs]] | 2025 | Composable accelerator compilation | `metadata-only` | DOI `10.1145/3706628.3708828` |
| [[integer-fusion-2025/index|Enhancing Transformer Inference Efficiency on FPGA Through Fully Fusion and Integer-Only Quantization Techniques]] | 2025 | Composable accelerator compilation | `metadata-only` | DOI `10.1109/ICCD65941.2025.00020` |
| [[shuhai-2020/index|Shuhai: Benchmarking High Bandwidth Memory on FPGAs]] | 2020 | HBM topology and data movement | `downloaded` | arXiv 2005.04324 |
| [[hbm-connect-2021/index|HBM Connect: High-Performance HLS Interconnect for FPGA HBM]] | 2021 | HBM topology and data movement | `downloaded` | DOI `10.1145/3431920.3439301` |
| [[verilogeval-2023/index|Invited Paper: VerilogEval: Evaluating Large Language Models for Verilog Code Generation]] | 2023 | Kernel generation and evaluation | `downloaded` | arXiv 2309.07544 |
| [[rtllm-2024/index|RTLLM: An Open-Source Benchmark for Design RTL Generation with Large Language Model]] | 2024 | Kernel generation and evaluation | `downloaded` | arXiv 2308.05345 |
| [[gpt4aigchip-2023/index|GPT4AIGChip: Towards Next-Generation AI Accelerator Design Automation via Large Language Models]] | 2023 | Kernel generation and evaluation | `downloaded` | arXiv 2309.10730 |
| [[hlspilot-2024/index|HLSPilot: LLM-based High-Level Synthesis]] | 2024 | Kernel generation and evaluation | `downloaded` | arXiv 2408.06810 |
| [[llm-aid-2024/index|LLM-AID: Leveraging Large Language Models for Rapid Domain-Specific Accelerator Development]] | 2024 | Kernel generation and evaluation | `metadata-only` | DOI `10.1145/3676536.3697135` |
| [[rtlrewriter-2024/index|RTLRewriter: Methodologies for Large Models aided RTL Code Optimization]] | 2024 | Kernel generation and evaluation | `downloaded` | arXiv 2409.11414 |
| [[hls-codegen-benchmark-2025/index|Exploring Code Language Models for Automated HLS-based Hardware Generation: Benchmark, Infrastructure and Analysis]] | 2025 | Kernel generation and evaluation | `downloaded` | arXiv 2502.13921 |
| [[autodse-2022/index|AutoDSE: Enabling Software Programmers to Design Efficient FPGA Accelerators]] | 2022 | Evidence and optimization methodology | `downloaded` | arXiv 2009.14381 |
| [[ranktuner-2024/index|RankTuner: When Design Tool Parameter Tuning Meets Preference Bayesian Optimization]] | 2024 | Evidence and optimization methodology | `downloaded` | DOI `10.1145/3676536.3676782` |
| [[hlsfactory-2024/index|HLSFactory: A Framework Empowering High-Level Synthesis Datasets for Machine Learning and Beyond]] | 2024 | Evidence and optimization methodology | `downloaded` | arXiv 2405.00820 |
| [[bench4hls-2026/index|Bench4HLS: End-to-End Evaluation of LLMs in High-Level Synthesis Code Generation]] | 2026 | Evidence and optimization methodology | `downloaded` | arXiv 2601.19941 |
| [[softermax-2021/index|Softermax: Hardware/Software Co-Design of an Efficient Softmax for Transformers]] | 2021 | Evidence and optimization methodology | `downloaded` | arXiv 2103.09301 |

## 2026-07-28 Architecture Additions

| Paper | Year | Category | Cache status | Canonical source |
|---|---:|---|---|---|
| [[mpk-2025/index|MPK: A Compiler and Runtime for Mega-Kernelizing Tensor Programs]] | 2025 | Coarse-grained and persistent execution | `downloaded` | arXiv 2512.22219 |
| [[cd-llm-2026/index|CD-LLM: A Heterogeneous Multi-FPGA System for Batched Decoding of 70B+ LLMs Using a Compute-Dedicated Architecture]] | 2026 | HBM-aware and decode architectures | `metadata-only` | DOI `10.1145/3771288` |
| [[flightopu-2025/index|FlightOPU: An FPGA Overlay Processor for LLM with HBM-Aware Multi-Die Architecture]] | 2025 | HBM-aware and decode architectures | `metadata-only` | DOI `10.1109/ICFPT67023.2025.00048` |
| [[nyx-2025/index|Nyx: Virtualizing dataflow execution on shared FPGA platforms]] | 2025 | Shared and virtualized FPGA execution | `metadata-only` | DOI `10.1145/3695053.3731094` |
| [[pcie-coarse-systolic-2025/index|Hardware-Software Co-Design for Efficient LLM Inference on PCIe-Based FPGAs Using Coarse-Grained Systolic Arrays]] | 2025 | Coarse-grained and persistent execution | `metadata-only` | DOI `10.1109/SOCC66126.2025.11235351` |
| [[riscbench-2026/index|RISCBench: Benchmarking RISC-V Orchestration Efficiency in FPGA and FPGA-Like Computing Engines]] | 2026 | Evidence and orchestration methodology | `metadata-only` | DOI `10.1145/3748173.3779569` |
| [[h2-llm-2025/index|H2-LLM: Hardware-Dataflow Co-Exploration for Heterogeneous Hybrid-Bonding-based Low-Batch LLM Inference]] | 2025 | HBM-aware and decode architectures | `metadata-only` | DOI `10.1145/3695053.3731008` |
| [[mcore-opu-2024/index|An FPGA-Based Multi-Core Overlay Processor for Transformer-Based Models]] | 2024 | Programmable and specialized FPGA execution | `metadata-only` | DOI `10.1109/ISEDA62518.2024.10617729` |
| [[streaming-vpe-2024/index|An FPGA-Based Efficient Streaming Vector Processing Engine for Transformer-Based Models]] | 2024 | Coarse-grained and persistent execution | `metadata-only` | DOI `10.1109/ISEDA62518.2024.10617499` |
| [[dtcore-2026/index|DTCore: A Compiler-Directed Control-Minimal FPGA Compute Engine]] | 2026 | Coarse-grained and persistent execution | `metadata-only` | DOI `10.1109/FCCM68464.2026.00053` |
| [[festal-2026/index|FESTAL: Dataflow Accelerator Synthesis Framework with Graph-Based Fusion for FPGA]] | 2026 | Composable accelerator compilation | `metadata-only` | DOI `10.1109/ASP-DAC66049.2026.11420389` |
| [[fmc-llm-2025/index|FMC-LLM: Enabling FPGAs for Efficient Batched Decoding of 70B+ LLMs with a Memory-Centric Streaming Architecture]] | 2025 | HBM-aware and decode architectures | `metadata-only` | DOI `10.1145/3706628.3708863` |
| [[e2e-overlay-compiler-2025/index|End-to-end Compilation is All FPGAs Need: A Unified Overlay-based FPGA Compiler for Deep Learning]] | 2025 | Composable accelerator compilation | `metadata-only` | DOI `10.1145/3658617.3697562` |
| [[lembda-2026/index|Lembda: Optimizing LLM Inference on Embedded Platforms via CPU/FPGA Co-processing]] | 2026 | CPU-FPGA heterogeneous inference | `metadata-only` | DOI `10.1007/978-981-95-1021-4_35` |
| [[cgra-space-time-2025/index|Monomorphism-Based CGRA Mapping via Space and Time Decoupling]] | 2025 | Overlay and CGRA mapping | `downloaded` | arXiv 2512.02859 |

Return to [[research/fpga-llm-inference/index|FPGA LLM Inference]].

---
title: FPGA LLM Inference Foundations
domain: research
area: fpga-llm-inference
type: synthesis
status: active
updated: 2026-07-22
tags: [fpga, llm-inference, prefill, decode, hbm, dataflow]
---

# FPGA LLM Inference Foundations

## 1. What Is Being Accelerated

Decoder-only LLM inference is not one homogeneous workload. A request passes through at least the following stages:

```text
model/bitstream load
  -> prompt tokenization
  -> embedding
  -> prefill over N input tokens
  -> LM head + first-token sampling
  -> autoregressive decode, one new token per step
  -> detokenization / streaming output
```

A Transformer block usually contains normalization, Q/K/V projections, attention, output projection, residual operations, a gated or standard FFN, and another residual path. For one layer, the dominant linear operations can be sketched as:

\[
Q=XW_Q,\quad K=XW_K,\quad V=XW_V,
\]

\[
A=\operatorname{softmax}(QK^\top/\sqrt{d}),\quad O=AV,
\]

\[
Y=\operatorname{FFN}(X+OW_O).
\]

The same model creates two different hardware regimes.

### Prefill

- Processes many prompt tokens at once.
- Linear layers are predominantly GEMM-like and expose abundant parallelism.
- Attention cost grows with prompt length; dense attention has a quadratic component.
- Usually compute-bound at useful sequence lengths.
- Main user-facing metric: time to first token (TTFT), with prompt length stated.

### Decode

- Processes one newly generated token per iteration at batch 1.
- Linear layers become GEMV-like.
- Every step rereads a large fraction of model weights; arithmetic intensity is low.
- KV-cache traffic grows with context length.
- Usually bandwidth- and latency-bound.
- Main metrics: inter-token latency (ITL) and generated token/s.

This distinction explains a recurring result in the literature: GPUs are naturally strong in prefill because of dense compute, while FPGA designs can be competitive in batch-1 decode when they exploit exact precision, data layout, memory channels, fusion and persistent state.

## 2. FPGA Resource Model

| Resource | LLM inference role | Common failure mode |
|---|---|---|
| LUT / carry chain | low-bit arithmetic, control, custom nonlinear approximations, table lookup | routing pressure and frequency loss |
| DSP | FP/fixed-point MACs and dense GEMM/GEMV | underutilized during narrow decode or consumed by unsupported precision |
| BRAM / URAM | activation tiles, partial sums, FIFO, KV slices, lookup tables | capacity forces spills; poor banking causes port conflicts |
| HBM | model weights and large KV cache on datacenter cards | bank conflict, crossbar locality, short bursts, low outstanding traffic |
| DDR | capacity-oriented storage and embedded-board model weights | bandwidth ceiling dominates decode |
| PCIe / AXI | host-device commands and tensor movement | fine-grained transfers and synchronization dominate wall time |
| XRT/OpenCL runtime | bitstream, buffer and kernel orchestration | launch expansion, blocking waits, allocation and sync overhead |

HBM must not be modeled as a flat byte array. Shuhai and HBM Connect show that pseudo-channel placement, switch topology, burst length, outstanding requests and processing-element connectivity materially change effective bandwidth. A valid LLM design needs an explicit tensor-to-bank layout and a runtime that preserves residency.

## 3. Main Mapping Families

### Temporal overlay

A reusable compute core executes an instruction stream over many layers and models. DFX, Transformer-OPU, FET-OPU and related work emphasize programmability and bitstream reuse.

- Strength: model flexibility and manageable compile time.
- Cost: intermediate data often returns to off-chip memory; instruction and synchronization overhead remain.

### Model-specific spatial dataflow

Operators or whole blocks become pipeline stages connected by streams. Spatial LLM, StreamTensor and CODO are representative.

- Strength: producer/consumer overlap, on-chip intermediate forwarding, fewer large launches.
- Cost: resource pressure, routing difficulty, model/shape specialization and long compilation.

### Heterogeneous CPU-FPGA system

The CPU retains control-heavy or unsupported operations; FPGA executes linear and selected nonlinear kernels. EdgeLLM and the current llama.cpp backend fall into this broad class, but at different abstraction levels.

- Strength: practical framework integration and graceful division of labor.
- Cost: boundary crossings, layout conversions and silent fallback can erase acceleration.

### Multi-FPGA appliance

Weights or layers are partitioned across cards, using model/tensor parallelism and direct links. DFX, FlightLLM's scaling analysis and Terafly occupy this space.

- Strength: capacity and bandwidth scale beyond one card.
- Cost: synchronization and network traffic become first-class latency terms.

### Stage-disaggregated design

Prefill and decode are mapped to different hardware or datapaths because their optimal architectures conflict. GLITCHES uses GPU-FPGA collaboration; TeLLMe uses separate prefill/decode datapaths on one edge FPGA; FAST-Prefill deliberately accelerates only long-context prefill.

## 4. Quantization Is an Architecture Choice

Quantization changes more than storage size.

| Format family | Hardware implication |
|---|---|
| FP16/F16 | easiest semantic baseline; high bandwidth and DSP cost |
| W8A8 / W4A8 | denser packing and more MACs per DSP; requires scale/dequant handling |
| W4A16 | decode-friendly weight compression while retaining activation precision |
| mixed 3-5 bit | can match layer sensitivity but complicates decoder and memory format |
| ternary W1.58A8 | replaces multipliers with pass/negate/zero or table lookup; shifts pressure to LUT/URAM |
| structured/unstructured sparsity | reduces useful work only if metadata, load balance and sparse datapath overhead are controlled |

A paper-level comparison must report both model quality and the numerical path. A W4A8 GPT-2 result cannot be treated as a hardware-only comparison against F16 Gemma.

## 5. The Data-Movement Hierarchy

The desired residency hierarchy is:

```text
model weights: host storage -> FPGA HBM/DDR once -> reused across requests
activations: producer -> on-chip stream/buffer -> consumer
KV cache: persistent device memory -> incrementally updated
commands: block/region granularity, not tile granularity
outputs: logits/top-k/token candidates only when required by sampler boundary
```

The worst case is the inverse: repeatedly allocate, pack, transfer, launch, wait, copy back and unpack for every tensor tile or accepted graph node.

A useful performance decomposition is:

\[
T_{request}=T_{tokenize}+T_{prefill}+\sum_{i=1}^{N_{out}}(T_{decode,i}+T_{sample,i})+T_{detokenize},
\]

and each accelerator phase can be decomposed as:

\[
T_{phase}=T_{host}+T_{H2D}+T_{queue}+T_{kernel}+T_{D2H}+T_{sync}.
\]

Without device timestamps, a host-side `run::wait` contains an inseparable mixture of queueing, device execution and runtime wait overhead; it must not be labeled pure kernel time or pure scheduler overhead.

## 6. Five Meanings of End-to-End

Literature uses “end-to-end” at several incompatible levels:

| Level | Boundary | Example evidence |
|---|---|---|
| L0: kernel | one GEMM/attention/operator | HLS cycles, board kernel event |
| L1: block | one complete Transformer block | fused dataflow block invocation |
| L2: model phase | all layers for prefill or one decode step | TTFT, ITL, pp/tg |
| L3: generation harness | prefill + repeated decode + LM head | `[input:output]` latency and token/s |
| L4: application request | real text in to detokenized text out | CLI/server wall-clock including tokenization and sampling |

DFX explicitly implements embeddings, decoder layers, LM head and generation control. CODO and StreamTensor report L3-style GPT-2 metrics, but their public artifact host paths expose a narrower kernel-event measurement than a production CLI. The current `llama-bench pp512/tg128` result is a real framework/model-phase measurement (L2), not automatically L4.

## 7. Implications for This Project

1. F16 is appropriate for semantic bring-up, but not a credible final bandwidth point for FPGA LLM performance.
2. A native GGML backend is a valuable contribution only if framework integration does not force per-node/per-tile synchronous execution.
3. The next architectural unit should be a contract-closed graph region or Transformer block, not an isolated operator replacement.
4. Correctness must remain multi-level: operator oracle, graph support audit, zero fallback, model output/quality, and source-to-xclbin identity.
5. Performance should be optimized in this order: measurement boundary -> launch/sync reduction -> residency/overlap -> precision/layout -> kernel arithmetic.

## Key Sources

- [DFX, MICRO 2022](https://doi.org/10.1109/MICRO56248.2022.00051)
- [FlightLLM, FPGA 2024](https://doi.org/10.1145/3626202.3637562)
- [Spatial LLM, TRETS](https://doi.org/10.1145/3656177)
- [Shuhai, FCCM 2020](https://doi.org/10.1109/FCCM48280.2020.00024)
- [HBM Connect, FPGA 2021](https://doi.org/10.1145/3431920.3439301)
- [[research/fpga-llm-inference/system-landscape]]

返回 [[research/fpga-llm-inference/index]]。

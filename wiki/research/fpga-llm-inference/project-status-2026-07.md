---
title: llama.cpp FPGA Backbone Status, July 2026
domain: research
area: fpga-llm-inference
type: engineering
status: active
updated: 2026-07-24
tags: [llama-cpp, ggml, fpga, u280, xrt, project-status, private-draft]
---

# llama.cpp FPGA Backbone Status, July 2026

## Source And Sensitivity

This page is a synthesis of the private draft **Towards a General FPGA Backbone for LLM Inference** and its retained experiment notes on the `fpga-tailscale` development host. It records technical claims and aggregate evidence only; the unpublished manuscript and raw private repositories are not copied into the wiki.

Source snapshot inspected on 2026-07-22:

- draft repository commit: `7dc8a751362e95d802dc5b9ccfb0bb95b205d5d4`;
- matched backend commit: `2616bb6b0fabfe2974c00bf3a2d5be292a22e05e`;
- draft and experiment evidence had uncommitted updates, so this page is a time-stamped working snapshot rather than a frozen paper record.

## System Thesis

The project defines FPGA generality as a stable integration and replacement boundary, not as one universal bitstream:

```text
llama.cpp / GGML graph
  -> native FPGA backend registration and support query
  -> accepted GGML node
  -> operator/type/shape contract
  -> XRT runtime and resident tensor state
  -> ABI-compatible RTL or HLS implementation
  -> packaged xclbin identity
  -> observed board execution
```

A support decision is a promise: a node accepted by the FPGA backend must execute on FPGA or fail explicitly. Silent CPU fallback is not allowed in the declared strict scope.

## Current Validated Scope

| Dimension | Current setting |
|---|---|
| Framework | native `llama.cpp` / GGML backend |
| FPGA | AMD/Xilinx Alveo U280 development target |
| Model | Gemma 3 1B, F16 GGUF |
| Contexts | c64/c512 graph signatures; measured `pp512` and `tg128` |
| Operator families | 11 |
| Runtime | XRT 2.14.354; Vitis/Vivado 2022.2 |
| Correctness | CPU/operator oracles plus strict graph acceptance evidence |
| Sampling boundary | framework path; benchmark is pp/tg model phase rather than a standalone token-returning RTL engine |

The 11 operator families are `GET_ROWS`, `SCALE`, `MUL_MAT`, `RMS_NORM`, `MUL`, `ROPE`, `SET_ROWS`, `SOFT_MAX`, `ADD`, `GLU`, and `CONT`.

## Evidence Closure

| Claim | Evidence state |
|---|---|
| Native GGML registration and dispatch | implemented |
| Host and RTL units for 11 operator families | implemented |
| c64/c512 support corpus | 56 signatures per graph, 112 total |
| Strict board execution | 2,422/2,422 accepted dispatches, zero fallback, 11/11 families |
| Selected-point correctness | 11/11 GGML-RTL and 11/11 GGML-HLS pass at deterministic c64 decode-median points |
| CPU/RTL/HLS operator table | retained 33-row comparison |
| OOC QoR | 22/22 final builds with resource and 10 ns WNS records |
| Matched CPU/FPGA pp/tg | five repetitions, same backend commit/model/harness |
| Runtime phase profile | calls, launches, transfer, wait and host phases retained |
| Native XRT timeline | one tg1 diagnostic; 1,570 launches in selected graph |
| Matched power/energy | pending |
| Model-level quality | pending |
| Per-signature FPGA numerical replay | pending |
| Multi-model/multi-card portability | pending |
| Contract-preserving replacement with E2E gain | pending |

## Matched End-To-End Results

Five-repetition Gemma 3 1B F16 measurements:

| Backend | Prefill `pp512` latency | Prefill rate | Decode ITL (`tg128`) | Decode rate |
|---|---:|---:|---:|---:|
| CPU, 16 physical cores on socket 0 | 1.32 +/- 0.03 s | 387.18 +/- 8.51 token/s | 60.62 +/- 0.05 ms | 16.50 +/- 0.01 token/s |
| FPGA, U280 strict backend | 302.13 +/- 0.26 s | 1.6946 token/s | 759.88 +/- 4.38 ms | 1.3160 token/s |

The FPGA is currently 228.5x slower in prefill and 12.54x slower in decode. This result establishes framework integration and stable execution, not acceleration.

These are `llama-bench`-style model-phase measurements. They do not by themselves include text tokenization, sampling/detokenization or cold model/bitstream load.

## Runtime Bottleneck

### Aggregate profile

| Workload | GGML calls | XRT launches | Launch/call | XRT wait | Transfer | Other host |
|---|---:|---:|---:|---:|---:|---:|
| `pp512` | 1,626 | 224,936 | 138.34 | 96.25% | 1.65% | 2.10% |
| `tg128` | 104,877 | 202,530 | 1.93 | 79.58% | 11.37% | 9.05% |

The launch expansion is concentrated in two operators:

- `pp512`: 470 `MUL_MAT` calls become 198,176 launches; 52 `GLU` calls become 25,656 launches.
- `tg128`: each `MUL_MAT` becomes four launches and each `GLU` becomes three.

The backend traverses graph nodes in order and waits after each batch. A native XRT trace of one measured graph shows the repeating sequence:

```text
H2D sync -> run::start -> blocking run::wait -> D2H sync
```

For the selected 885.527 ms graph window:

| Phase | Time | Share |
|---|---:|---:|
| blocking wait | 636.256 ms | 71.85% |
| H2D + D2H sync | 114.231 ms | 12.90% |
| launch API | 6.429 ms | 0.73% |
| other host/API gaps | 128.610 ms | 14.52% |

The packaged xclbin lacks device trace monitors, so host-observed wait cannot yet be split into kernel-active time, queueing and runtime overhead.

## Why A Faster MUL_MAT Is Not Enough

`MUL_MAT` contributes 18.64% of profiled `pp512` operator wall time and 29.77% of `tg128`. Even reducing it to zero gives only:

\[
S_{pp512,max}=\frac{1}{1-0.1864}=1.229,
\]

\[
S_{tg128,max}=\frac{1}{1-0.2977}=1.424.
\]

Decode uses `n_vec=1`, so widening a multi-vector path does not solve that workload. The immediate problem is graph-wide launch/synchronization granularity.

## Structural Comparison With CODO

| Question | Current backend | CODO |
|---|---|---|
| What is stable? | GGML backend/device and operator ABI | high-level program/MLIR compiler flow |
| What is fused? | little beyond internal multi-CU batches | complete Transformer block/dataflow graph |
| How are layers run? | many accepted GGML operations and internal launches | paper reports GPT-2 Medium; public Fig. 9 host exposes one block command, while model-level lifting is unresolved |
| Main evidence | real framework graph, support receipts, zero fallback | compiler legality, dataflow optimization, GPT TTFT/decode |
| Main performance risk | fine-grained XRT synchronization | model specialization and unclear application-level boundary |

CODO's `231.48 token/s` is not a valid direct speedup over `1.316 token/s`, because the models (GPT-2 Medium vs Gemma 3 1B), precision (W4A8 vs F16), harness and measurement boundary differ. It is nevertheless a strong indication of the architecture required to enter a competitive regime.

## Recommended Architecture Roadmap

### P0: freeze measurement semantics

- Preserve current pp/tg evidence as the integration baseline.
- Add text-in/text-out request timing separately.
- Add device timestamps, power, logits/token correctness and cold/warm boundaries.

### P1: collapse command granularity

- Introduce a persistent command processor or command buffer on FPGA.
- Batch internal tiles without host waits.
- Return once per accepted region rather than once per internal launch batch.
- Set quantitative launch budgets: ideally O(layers) per token before aiming for O(1), not O(tensor tiles).

### P2: contract-preserving graph-region fusion

- Detect sequences of GGML nodes with closed producer/consumer semantics.
- Start with a block fragment such as norm -> projections -> RoPE/attention -> residual.
- Define region ABI, shape/type gates and a CPU oracle for the entire region.
- Keep unfused operators as explicit fallback outside the strict fused scope; never hide them.

### P3: residency and asynchronous execution

- Keep weights and KV cache resident in declared HBM banks.
- Eliminate repeated allocation and packing.
- Queue H2D, compute and D2H with events; overlap only when dependencies permit.
- Add trace monitors so active device intervals can be distinguished from host waits.

### P4: competitive numerical format

- Move from F16 bring-up to a GGUF-compatible quantized path such as Q4_0 or a clearly documented W4A8 design.
- Account for scale/zero-point decode and output quality.
- Compare bandwidth utilization before and after quantization.

### P5: portability and paper closure

- Add a second `llama.cpp` model or model family.
- Package one ABI-compatible kernel/region replacement and show matched end-to-end change.
- Measure power, energy/token and a pinned model quality metric.

## Defensible Paper Position

The present contribution can be stated as:

> A native, strict and evidence-closed FPGA execution boundary inside `llama.cpp`, with real Gemma graph coverage and replaceable operator implementations.

It cannot yet be stated as:

- an FPGA speedup over CPU/GPU;
- performance parity with CODO/FlightLLM/StreamTensor;
- a general high-performance LLM bitstream;
- proof that generated RTL improves end-to-end inference.

The strongest next paper result would be one contract-closed fused region that reduces launch count materially and produces a measured request-level improvement without weakening strict execution evidence.

## Idea Audit Update, 2026-07-24

A full `idea-spark` run did not emit a reviewer-defensible idea card. The audit confirmed the admission-to-launch granularity gap, but rejected integration/evidence closure as a sufficient paper mechanism. An asynchronous receipt-epoch design failed on XRT dependency/fault progress and KV alias semantics. A narrower single-output RegionSeal design was implementable using the existing graph-residency mirror path, but remained too close to ordinary effect-aware fusion and did not pass the final falsification re-audit.

The current recommendation is therefore conditional: keep this page as the integration baseline, do not submit the current general-backbone claim, and first build a calibrated region shell that measures one-region launch/wait, device event and certificate overhead. Only a shell with enough conservative headroom to support a downstream effect lower bound greater than 10% should advance to a full region artifact. See [[research/fpga-llm-inference/towards-idea-audit-2026-07]].

## Related Pages

- [[research/fpga-llm-inference/codo-2026]]
- [[research/fpga-llm-inference/end-to-end-evaluation]]
- [[research/fpga-llm-inference/towards-idea-audit-2026-07]]
- [[research/fpga-llm-inference/fpga-backbone-llamacpp-note]]

返回 [[research/fpga-llm-inference/index]]。

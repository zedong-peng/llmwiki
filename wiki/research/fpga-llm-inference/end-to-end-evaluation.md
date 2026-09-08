---
title: End-to-End Evaluation Protocol for FPGA LLM Inference
domain: research
area: fpga-llm-inference
type: checklist
status: active
updated: 2026-07-23
tags: [benchmark, end-to-end, ttft, itl, throughput, power, correctness]
---

# End-to-End Evaluation Protocol

## Goal

建立一个同时满足两件事的评测协议：

1. 能与 CODO、StreamTensor、DFX、FlightLLM 等论文的 GPT/LLM 指标对话；
2. 不牺牲当前 `llama.cpp` backend 的真实框架、strict execution 和 evidence-closure 优势。

协议必须把 **模型阶段** 与 **应用请求** 分开报告，避免所有系统都把不同边界称作 “end-to-end”。

## Benchmark Levels

| ID | Name | Timer starts | Timer ends | Required output |
|---|---|---|---|---|
| K0 | kernel | board kernel command starts | command completes | cycles/device time, bytes, shape |
| O1 | GGML operator | backend receives node | output tensor is available | host phases, launches, oracle error |
| R2 | fused region/block | accepted region begins | all region outputs are valid | region latency, launches, intermediate traffic |
| M3 | model phase | first prefill/decode graph begins | logits for phase are ready | pp/tg, TTFT component, ITL |
| G4 | generation harness | token IDs are ready | requested output token IDs are produced | TTFT, decode speed, total generation latency |
| A5 | application request | text request enters CLI/server | final detokenized text is emitted | cold/warm wall-clock and user-visible latency |

Each result table must carry its level. Results at different levels are not speedups over one another.

## Core Metric Definitions

Let:

- `N_in`: number of prompt tokens after tokenization;
- `N_out`: number of generated tokens requested and actually produced;
- `t_req`: request arrival;
- `t_first`: first sampled token available;
- `t_i`: sampled token `i` available;
- `t_done`: final detokenized output emitted.

### Time to first token

\[
TTFT=t_{first}-t_{req}.
\]

Report two variants:

- `TTFT_model`: from first model prefill dispatch to first logits/token;
- `TTFT_app`: from text request arrival, including tokenization and host preparation.

### Inter-token latency

For token `i > 1`:

\[
ITL_i=t_i-t_{i-1}.
\]

Report mean, median, p95 and p99. Do not infer the tail from aggregate token/s.

### Decode throughput

\[
R_{decode}=\frac{N_{out}-1}{t_{N_{out}}-t_1}
\]

is the clean steady-state definition when the first token belongs to prefill. If reproducing a paper that uses `N_out / decode_time`, report that convention in a separate column.

### CODO-compatible generation latency

Two of the three CODO Table VI rows are consistent with:

\[
T_{CODO}=TTFT+\frac{N_{out}}{R_{decode}}.
\]

Use this formula in a dedicated `CODO-compatible (recomputed)` column. Also retain the paper's published latency unchanged: its `[64:64]` row reports `313.44 ms`, whereas the formula gives `309.12 ms`; the other two rows match. Do not silently repair the source table or mix this convention with the steady-state definition above.

### Application latency

\[
T_{app}=t_{done}-t_{req}.
\]

Separate cold and warm requests:

- cold: process start + model parse + bitstream + weight upload + request;
- warm: model/bitstream/weights resident before request;
- steady: repeated warm requests after an explicit warm-up policy.

## Required Configuration Record

Every row needs the following immutable metadata:

| Category | Required fields |
|---|---|
| Model | family, exact variant, parameter count, layer/hidden/FFN dimensions, model hash |
| Numerical path | GGUF dtype/quantization, activation/KV precision, scale format, quality metric |
| Workload | prompt text or token IDs, `N_in`, `N_out`, batch, context, sampler, seed, stop policy |
| FPGA | card, device part, BDF or stable device ID, achieved clock, bitstream hash |
| Memory | HBM/DDR capacity, bank map, weight residency, KV policy, measured bytes |
| Host | CPU model, socket/NUMA/thread affinity, governor, RAM, OS |
| Toolchain | commit, compiler flags, XRT/Vitis/Vivado versions, firmware/platform |
| Timing | timer API, included/excluded phases, warm-up, repetitions, aggregation |
| Execution | accepted/rejected/fallback node counts, launch count, trace availability |
| Energy | measurement tool, sample rate, idle subtraction, host/card/system boundary |

## Correctness Gates

Performance is publishable only after all applicable gates pass.

1. **Operator numerical gate:** output against the CPU/GGML oracle for declared shapes and dtypes.
2. **Region graph gate:** fused region output against unfused graph output.
3. **Support gate:** accepted nodes execute on FPGA; rejected nodes are explicit.
4. **Fallback audit:** count and fraction; strict result requires zero fallback within declared scope.
5. **Artifact identity:** source hash -> synthesis report -> xclbin hash -> runtime loaded hash.
6. **Model gate:** next-token logits/top-k or deterministic greedy tokens match within declared tolerance.
7. **Quality gate:** perplexity or task metric for quantized/approximate paths.
8. **Real-input gate:** at least one retained nonzero real prompt/weight run; zero-filled smoke tests are not quality evidence.

## Runtime Decomposition

Instrument every operator/region with non-overlapping phases:

```text
support/control
allocation
packing
H2D sync
queue/launch
run wait
D2H sync
unpacking
sampling
```

When device traces exist, split `run wait` into queue, active kernel and host blocking. When they do not, retain the combined name `host-observed XRT wait`.

Report:

- GGML calls;
- physical kernel launches;
- launches per call/region/token;
- transferred bytes per request/token;
- resident bytes;
- allocation count;
- synchronization count;
- overlap ratio from timestamped events.

## Primary Experiment Matrix

### Matrix 1: current integration baseline

| Backend | Model | Precision | Workload | Purpose |
|---|---|---|---|---|
| CPU | Gemma 3 1B | F16 | pp32/64/128/512; tg32/64/128 | matched CPU oracle/performance |
| FPGA strict | same | same | same | current node-granularity baseline |
| FPGA batched/persistent | same | same | same | isolate launch/sync reduction |
| FPGA fused region | same | same | same | test region-level dataflow |

Primary plots:

- prefill rate vs prompt length;
- ITL/decode token/s vs context/output length;
- launch count and transferred bytes per token;
- phase breakdown;
- speedup waterfall from baseline -> batching -> region fusion -> quantization.

### Matrix 2: CODO-compatible shape

This is a separate fixed-shape graph/kernel axis. It is useful only when the executable, numerical
semantics and timer boundary are matched; it must not be merged with the stateful KV-generation
throughput table in Matrix 1 or with the application request metrics in Matrix 3.

| Field | Required setting |
|---|---|
| Model | GPT-2 Medium, 24 layers, hidden 1024, FFN 4096, 16 heads |
| Precision | W4A8 for direct CODO comparison |
| Device | U280 |
| Workloads | `[32:32]`, `[64:64]`, `[128:128]` |
| Metrics | TTFT, decode token/s, CODO-compatible total latency |
| Extra disclosure | H2D included?, LM head included?, sampling included?, real weights?, output verified? |

This matrix is not matched until the same executable model and numerical semantics run through both systems.

### Matrix 3: application end-to-end

Use a real text prompt corpus with fixed token IDs and output budget:

- short chat: 32 input / 32 output;
- medium: 128 / 128;
- long prompt: 512 / 128;
- optional long context after core closure.

Compare CPU and FPGA through the same `llama.cpp` CLI/server entry point. Report A5 and M3 side by side to show framework overhead rather than hiding it.

## CODO Reproduction Checklist

- [x] Inspect GitHub main, `isca2026-ae` and Zenodo; none contains the appendix-promised GPT xclbins, executables or raw board logs.
- [x] Recompute the three Table VI rows and infer all 12 Fig. 9 combinations; retain the `[64:64]` 4.32 ms discrepancy and unresolved headline aggregation gap.
- [x] Audit all four public Fig. 9 output paths; every final result remains local, every host buffer is read-only and D2H is omitted.
- [x] Audit source clock targets; the paper says 300 MHz, while the public 128-token build targets 250 MHz.
- [ ] Obtain the exact GPT-2 Medium checkpoint and quantization recipe.
- [ ] Confirm whether Table VI uses real checkpoint weights.
- [ ] Obtain the raw board logs and exact xclbins corresponding to Fig. 9/Table VI.
- [ ] Verify TTFT timer boundaries.
- [ ] Verify whether initial PCIe host-to-HBM migration is included separately from kernel-internal HBM traffic.
- [ ] Verify whether LM head and token selection are included.
- [ ] Locate or restore an externally observable output-producing board path.
- [ ] Run that host with nonzero inputs and real weights, then compare output to PyTorch.
- [ ] Record kernel event time separately from request/model time.
- [ ] Preserve the actual achieved clock per xclbin, platform, XRT and bitstream hashes.

## Power And Energy

Report at least two boundaries if possible:

1. card/FPGA rail power;
2. full host-system wall power.

For a warm request:

\[
E_{request}=\int_{t_{req}}^{t_{done}}(P(t)-P_{idle})dt,
\]

\[
E_{token}=E_{request}/N_{out}.
\]

Also retain total energy without idle subtraction. State sample rate and synchronization between the power stream and request timer.

## Statistical Protocol

- At least five repetitions for development; 20+ for final latency distributions.
- Fixed warm-up count and explicit exclusion from aggregates.
- Report mean +/- sample SD for throughput compatibility, plus median/p95/p99 for latency.
- Preserve every raw run; do not report only the best bitstream/run.
- Pin host affinity and governor.
- Fail the run if loaded model or xclbin hash differs from the manifest.

## Comparison Rules

A direct speedup requires all of:

- same model and effective parameter semantics;
- same numerical format or a quality-matched frontier;
- same input/output lengths and batch;
- same phase/application boundary;
- physical hardware measurements;
- explicit host and power boundary;
- no hidden fallback.

Otherwise label the result as one of:

- `matched`;
- `normalized estimate`;
- `paper-reported context`;
- `not directly comparable`.

## Near-Term Success Criteria

Before chasing CODO-level token/s, require the next backend revision to show:

1. at least 10x fewer physical launches on `pp512` and `tg128`;
2. no regression in the 11-family correctness and strict support gates;
3. observable reduction in host wait/sync share;
4. matched pp/tg wall-clock improvement;
5. one retained real-prompt token/logit comparison;
6. source-to-xclbin-to-dispatch identity.

The long-term performance target is a whole-block/region execution regime comparable in granularity to StreamTensor/CODO, while retaining native GGML semantics.

## Related Pages

- [[research/fpga-llm-inference/codo-2026]]
- [[research/fpga-llm-inference/project-status-2026-07]]
- [[research/fpga-llm-inference/system-landscape]]

返回 [[research/fpga-llm-inference/index]]。

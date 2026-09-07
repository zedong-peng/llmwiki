---
title: FPGA LLM Inference System Landscape
domain: research
area: fpga-llm-inference
type: comparison
status: active
updated: 2026-09-07
tags: [fpga, llm-inference, systems, compiler, accelerator, related-work]
---

# FPGA LLM Inference System Landscape

## Scope

这份地图优先收录满足至少一项条件的工作：

- 在真实 FPGA 上执行生成式 Transformer/LLM；
- 同时讨论 prefill 与 decode；
- 提供模型级 compiler/runtime；
- 对当前 `llama.cpp` FPGA backend 的端到端评测或系统架构有直接启发。

数字只用于理解论文自身的 operating point。除非模型、精度、板卡、batch、input/output length 和计时边界一致，否则不计算跨论文 speedup。

## Timeline And Roles

| Work | Year / venue | Model / device | Primary idea | Measurement relevance |
|---|---|---|---|---|
| [FTRANS](https://doi.org/10.1145/3370748.3406567) | 2020, ISLPED | Transformer/BERT-era FPGA | early Transformer arithmetic, quantization and FPGA co-design | operator/encoder foundation, not modern autoregressive E2E |
| [Sanger](https://doi.org/10.1145/3466752.3480125) | 2021, MICRO | sparse attention | algorithm-architecture co-design for sparse attention | attention specialization; not a full LLM runtime |
| [DFX](https://arxiv.org/abs/2209.10797) | 2022, MICRO | GPT-2 345M/774M/1.5B; 1/2/4 U280 | programmable multi-FPGA appliance, complete GPT operation coverage | strongest early true text-generation E2E reference |
| [FlightLLM](https://arxiv.org/abs/2401.03868) | 2024, FPGA | OPT-6.7B, LLaMA2-7B; U280 | sparse/mixed precision, always-on-chip decode, length-adaptive compilation | complete mapping flow; strong datacenter FPGA ceiling |
| [Spatial LLM](https://arxiv.org/abs/2312.15159) | 2024/2025, TRETS | GPT-2 on U280; analytical LLaMA/Vicuna studies | model-specific spatial dataflow plus performance model | clearest prefill-vs-decode hardware analysis |
| [CSTrans-OPU](https://doi.org/10.1145/3649329.3657325) | 2024, DAC | Transformer overlay | overlay plus full compilation and sparsity exploration | programmable mapping reference |
| [ChatOPU](https://doi.org/10.1145/3676536.3676761) | 2024, ICCAD | sparse LLM | overlay for unstructured sparsity | sparse execution reference |
| [GLITCHES](https://doi.org/10.1109/HPEC62836.2024.10938498) | 2024, HPEC | GPU-FPGA system | collaborative heterogeneous prefill/decode execution | stage-placement alternative |
| [EdgeLLM](https://arxiv.org/abs/2407.21325) | 2025, IEEE TCAS-I | GLM-6B/Qwen-7B; VCU128 | CPU-FPGA runtime, common layout, end-to-end compiler | closest heterogeneous compiler/runtime reference |
| [Embedded decode bandwidth](https://arxiv.org/abs/2502.10659) | 2025, DATE | LLaMA2-7B W4A16; KV260 | maximize DDR capacity/bandwidth, fused decode datapath | useful `llama.cpp`/edge decode baseline |
| [BAQET](https://doi.org/10.1145/3706628.3708849) | 2025, FPGA | Transformer | BRAM-aware quantization and stream architecture | quantization/resource co-design |
| [SpeedLLM](https://arxiv.org/abs/2507.14139) | 2025, HPDC | TinyLlama/Llama2-style; U280 | pipeline, memory reuse and operator fusion | model-level host-timed design, but limited evaluation detail |
| [StreamTensor](https://arxiv.org/abs/2509.13694) | 2025, MICRO | GPT-2, Qwen, Llama, Gemma; U55C | Torch-MLIR compiler, stream tensor type, block fusion, FIFO sizing | direct compiler baseline and CODO predecessor |
| [CODO](https://arxiv.org/abs/2604.12618) | 2026, ISCA | GPT-2 Medium; U280 | eliminate coarse/fine dataflow violations, communication optimization, DSE | priority comparison; exact GPT TTFT/decode table |
| [TeLLMe v2](https://arxiv.org/abs/2510.15926) | 2026, FPGA | BitNet 0.73B W1.58A8; KV260 | ternary table-lookup matmul, separate prefill/decode datapaths | strong low-power full-phase edge baseline |
| [FAST-Prefill](https://arxiv.org/abs/2602.20515) | 2026, FCCM | Llama 3.2/Qwen 1-3B; U280 | dynamic sparse long-context prefill and two-tier KV cache | phase-specialized long-context baseline |
| [LUT-LLM](https://doi.org/10.1109/FCCM68464.2026.00027) | 2026, FCCM | LLM on FPGA | memory/LUT-based computation | low-bit arithmetic direction |
| [Hummingbird+](https://doi.org/10.1145/3748173.3779189) | 2026, FPGA | edge FPGA | deployment from prototype toward product | productization and edge-system reference |

## Integration-Abstraction Comparison

| System | User/application boundary | Model adaptation | FPGA mapping unit | Runtime style | Relation to current work |
|---|---|---|---|---|---|
| DFX | custom GPT appliance | model-specific instruction/model partition | complete GPT pipeline across cards | programmable overlay + multi-FPGA sync | true E2E definition and model-parallel ceiling |
| FlightLLM | custom compiler/IR/runtime | compress and compile whole model | instructions + fused dataflow | temporal accelerator with on-chip decode | performance/energy ceiling; less framework-native |
| Spatial LLM | HLS library + model composition | analytical resource allocation and per-model HLS | spatial pipeline stage/layer | model-specific dataflow | explains why fusion can dominate isolated kernels |
| EdgeLLM | CPU-FPGA application/compiler | dynamic operator mapping with common tensor layout | heterogeneous model graph | CPU control + FPGA accelerator | close architectural cousin, but not GGML-native |
| StreamTensor | PyTorch/Torch-MLIR compiler | regenerate fused block per model | whole Transformer block | block invocation with streaming intermediates | direct evidence that block fusion reduces memory/launch cost |
| CODO | high-level program/Torch-MLIR | compiler fixes dataflow violations and explores parallelism | large fused dataflow graph | generated kernel/host/link artifacts | strongest compiler comparison for GPT-2 |
| TeLLMe | model-specific edge inference stack | ternary model and specialized prefill/decode | full decoder datapaths | PS+PL, LM head on PS | shows full-phase design under 5 W |
| Current project | unchanged `llama.cpp`/GGML application | support-gated operator/type/shape onboarding | accepted GGML node today; region is future target | native backend + XRT | unique framework/ABI evidence, currently too fine-grained |

## Representative Reported Results

### DFX

- Executes GPT-2 inference end-to-end, including embedding, all decoder operations and LM head, on one to four U280 cards.
- Uses FP16 and a custom instruction set; GPT-2 345M/774M/1.5B scale with 1/2/4 cards.
- Reports, relative to the same number of V100 GPUs, average 5.58x lower latency, 3.78x higher throughput and 3.99x energy efficiency for its evaluated text-generation workloads.
- For GPT-2 345M at `[64:64]`, one/two/four FPGA throughput is reported as 93.10/146.25/207.56 token/s.

### FlightLLM

- Evaluates OPT-6.7B and LLaMA2-7B at batch 1 on a physical U280; VHK158 numbers are estimates aligned to platform resources.
- Combines block sparsity, N:M sparsity, average 3.5-bit weights, 8-bit activations, HBM+DDR placement and always-on-chip decode.
- Reports better end-to-end latency than optimized V100S baselines and roughly 6x energy efficiency on the headline LLaMA2 case.
- Its key lesson is architectural: decode activations stay on chip while large weights stream efficiently; generic GPU compression alone does not guarantee wall-clock gain.

### Spatial LLM

- Implements GPT-2 on U280 and reports about 2.16x/1.10x improvement over DFX for prefill/decode in its matched GPT-2 comparison.
- Reports FPGA weakness in compute-intensive prefill but advantage in memory-intensive decode; its GPT-2 decode is reported 1.9x faster and 5.69x more energy efficient than A100 at the selected setting.
- Provides an analytical model linking MAC allocation, on-chip buffers, off-chip bandwidth and spatial pipeline balance.

### EdgeLLM

- Maps a whole model across CPU and VCU128 FPGA, with common tensor layout intended to avoid repeated reshapes/transposes.
- GLM-6B decode is roughly stable near 90 token/s below 512 generated tokens; Qwen-7B is reported in the 42.5-69.4 token/s range.
- Reports 56.86 W average board/system measurement for its FPGA setting and headline 1.91x throughput / 7.55x energy efficiency over its A100 baseline.
- These numbers are contextual only: model, sparsity, INT4 path and host responsibilities differ from current Gemma F16 measurements.

### StreamTensor

On U55C, W4A8 GPT-2 Medium:

| `[input:output]` | Total latency (ms) | TTFT (ms) | Decode (token/s) |
|---:|---:|---:|---:|
| `[32:32]` | 194.99 | 34.59 | 199.51 |
| `[64:64]` | 358.24 | 61.27 | 215.51 |
| `[128:128]` | 696.65 | 125.35 | 224.05 |
| `[256:256]` | 1387.76 | 272.85 | 229.61 |

It fuses one entire Transformer block, then invokes that block sequentially with different weights for all layers. This is the most relevant structural contrast to the current per-node XRT execution.

### CODO

CODO reports GPT-2 Medium on U280/W4A8/300 MHz at 231.48 decode token/s, with TTFT 20.40, 32.64 and 110.40 ms for input lengths 32, 64 and 128. See [[research/fpga-llm-inference/codo-2026]] for the exact table and artifact-boundary audit.

### Embedded KV260 LLaMA2-7B

- LLaMA2-7B W4A16 on a 4 GB KV260, 300 MHz.
- Reported decode: 4.9 token/s, 6.57 W, about 84.5% of the bandwidth-derived limit.
- Explicitly focuses on decode; it is useful because it exposes the simple bandwidth bound and includes a `llama.cpp` edge comparison, not because it competes with datacenter U280 throughput.

### TeLLMe v2

- BitNet 0.73B, W1.58A8, KV260, 4.8 W.
- Reports 143 token/s prefill and 25 token/s decode; 64-128 token prompt TTFT is about 0.45-0.96 s.
- Offloads LM head to ARM/PS and states its roughly 9 ms latency is included in end-to-end results.
- This is a good example of declaring the heterogeneous boundary explicitly.

### FAST-Prefill

- U280 W8A8 implementation for Llama 3.2 1B/3B and Qwen 2.5 1.5B over 4K-128K context.
- Reports about 1.5x-2.5x TTFT speedup and up to 4.5x energy efficiency versus an A5000 Flex-Prefill implementation.
- It is intentionally not a decode system; it should appear in a stage-specific table, not an overall LLM token/s ranking.

## What The Literature Says About The Current Bottleneck

Three independent lines converge:

1. **Whole-block fusion matters.** Spatial LLM, StreamTensor and CODO keep intermediates on chip and amortize orchestration over a block/graph.
2. **Decode is a bandwidth problem after launch overhead is controlled.** FlightLLM, EdgeLLM and the KV260 LLaMA2 work emphasize weight layout, effective bandwidth and persistent state.
3. **Prefill and decode need different datapaths or scheduling.** Spatial LLM, GLITCHES, TeLLMe and FAST-Prefill all treat their asymmetry as architectural, not a minor parameter choice.

The current backend has not reached the second regime because launch/wait expansion dominates before HBM bandwidth becomes the clean limiting factor.

## 2026-07-28 Architecture Refresh

The broader search adds four distinctions that sharpen this landscape rather than changing the measurement caveats above.

| New reference | What it adds | What it does not establish for this project |
|---|---|---|
| [[papers/mpk-2025/index|MPK]] | persistent mega-kernel scheduling as a concrete way to remove kernel-per-op barriers | FPGA/HBM placement, GGML support semantics, or XRT failure behavior |
| [[papers/nyx-2025/index|Nyx]] | temporal/spatial resource sharing plus dependency-aware virtual FIFOs | LLM arithmetic or a framework-native backend |
| [[papers/flightopu-2025/index|FlightOPU]] | HBM-channel-affine overlay placement and multi-die routing | an unchanged llama.cpp/GGML boundary |
| [[papers/riscbench-2026/index|RISCBench]] | a control-plane measurement lens for scheduling, synchronization, and residency | a validated LLM accelerator mechanism |
| [[papers/cgra-space-time-2025/index|CGRA space-time mapping]] | a formal separation of time scheduling from spatial placement | a claim that temporal reuse is itself sufficient for performance |
| [[papers/festal-2026/index|FESTAL]] | graph-based fusion as a compiler comparison | the strict zero-fallback safety contract |

The updated conclusion is therefore narrower: the current system should seek a **contract-preserving coarse execution boundary plus explicit HBM residency rule**, not merely an operator fusion, a generic overlay, or a new static spatial accelerator. The first audited candidate is VSTC, which keeps original GGML call identities and explicit-error behavior while admitting only fully observed, single-consumer device-only calls into exact streamed templates; it remains a proposal until the stated U280 controls are measured. The relevant terminology and system placement are detailed in [[research/fpga-llm-inference/execution-architecture-taxonomy]], the candidate and its stop conditions in [[research/fpga-llm-inference/ideaspark-shared-engine-2026-07-28]], and complete search provenance in [[research/fpga-llm-inference/literature-search-2026-07-28]].

## Vendor And Dataflow Toolchains

2026-09-07 补充 [[research/fpga-llm-inference/vitis-ai-dpu-finn-pynq]]，将产业工具链与 LLM 论文系统分层比较。下表定位基于该页已核对的官方文档，不表示已在当前 U280/Gemma 路径验证。

| Reference | Architectural role | Relevance and boundary |
|---|---|---|
| Vitis AI v3.5 DPU | 目标相关 ISA、复用异构计算引擎、XIR 子图与 VART 作业 | shared-engine 先例；须核对 arch.json、算子覆盖与 CPU 分区，不等于原生 GGML 支持 |
| FINN | 量化网络定制 streaming dataflow，层内 PE/SIMD folding | FIFO、参数流和硬件生成参考；现成 Alveo 示例以 U250 为主，未建立 U280 完整 LLM 证据 |
| PYNQ / DPU-PYNQ | Python 驱动与可加载硬件 overlay 生态 | 展示部署链；DPU-PYNQ 已归档，文档对应 Vitis AI 2.5.0 |

这些参考不加入上面的 LLM token/s 表。用户提及的 `pinn` 尚未确认；FINN、PYNQ 与 Physics-Informed Neural Networks 的区别见新页。

## Reading Order

1. DFX: establish a strict definition of complete GPT text-generation acceleration.
2. FlightLLM: understand a modern 7B complete FPGA mapping flow.
3. Spatial LLM: build the prefill/decode analytical model.
4. StreamTensor: study whole-block compiler fusion and FIFO sizing.
5. CODO: study violation elimination, communication optimization and GPT board metrics.
6. EdgeLLM: compare CPU-FPGA compiler/runtime boundaries.
7. TeLLMe and FAST-Prefill: understand edge and stage-specialized endpoints.

## Related Pages

- [[research/fpga-llm-inference/foundations]]
- [[research/fpga-llm-inference/codo-2026]]
- [[research/fpga-llm-inference/end-to-end-evaluation]]
- [[research/fpga-llm-inference/project-status-2026-07]]
- [[research/fpga-llm-inference/literature-search-2026-07-28]]
- [[research/fpga-llm-inference/execution-architecture-taxonomy]]
- [[research/fpga-llm-inference/ideaspark-shared-engine-2026-07-28]]

返回 [[research/fpga-llm-inference/index]]。

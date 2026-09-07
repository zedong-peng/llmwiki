---
title: Execution Architecture Taxonomy for the U280 FPGA LLM Path
domain: research
area: fpga-llm-inference
type: comparison
status: active
updated: 2026-09-07
tags: [fpga, llm-inference, temporal-reuse, spatial-mapping, dataflow, overlay, hbm]
---

# Execution Architecture Taxonomy for the U280 FPGA LLM Path

## Why These Terms Need Separation

`shared engine`, `temporal reuse`, `overlay`, `streaming dataflow`, and `spatial accelerator` describe different design decisions. Treating them as synonyms obscures the practical question: where is a dependency materialized, who schedules the next unit of work, and how many host-visible completions are needed before a token can advance?

| Term | Defining property | Does not imply |
|---|---|---|
| Shared-engine temporal reuse | The same physical compute resources execute different operations or tiles at different times under a schedule. | That the engine is programmable, streaming, or launch-efficient. |
| Overlay / CGRA | A programmable instruction/data-path substrate is configured or scheduled for multiple operations. | That all dependent tensors stream, or that hardware is spatially dedicated per layer. |
| Streaming dataflow | A producer emits fragments to a consumer through a FIFO/channel before the full tensor is materialized. | That the FPGA uses a CGRA or supports arbitrary operators. |
| Spatial mapping | Operations/layers are statically assigned to distinct hardware regions that work concurrently. | That resource reuse or runtime programmability is available. |
| Coarse-grained execution | The host/framework observes a region, block, or command stream rather than every internal tile/operator. | That the region is semantically safe or that it avoids data movement. |

## Axes

The taxonomy uses two independent axes, plus a data-movement overlay.

```text
                         placement / resource ownership
                    temporal reuse                    spatial reservation
              +------------------------------+------------------------------+
custom RTL    | shared compute or token       | fixed layer/block pipeline   |
              | sequencer                     | and dedicated FIFOs          |
              +------------------------------+------------------------------+
programmable  | overlay/CGRA instructions,    | statically configured PE     |
fabric        | modulo schedule, virtualized  | regions or a spatial dataflow|
              | tasks                         | graph                        |
              +------------------------------+------------------------------+

Streaming is a third property: it can run across either column when producer
and consumer exchange fragments through an on-chip channel rather than a full
host-visible tensor materialization.
```

## Representative Placement

| Work / system | Placement | Programming model | Tensor movement | Granularity | Relevance |
|---|---|---|---|---|---|
| Vitis AI DPU (v3.5 docs) | temporal reuse across heterogeneous engines | target-specific ISA, XIR compiler and VART | compiler/platform-dependent buffers and reuse | compiled DPU subgraph/job | industrial programmable-engine precedent; inspect CPU partitions |
| FINN | spatial dataflow between layers, temporal folding within layers | QONNX/FINN-ONNX to generated HLS/RTL | FIFO streams, DMA, configurable parameter memory modes | generated dataflow partition | shows spatial mapping and temporal reuse can coexist |
| Spatial LLM | predominantly spatial | model-specific HLS composition | on-chip buffers and stage communication | layer/block | baseline for static resource allocation |
| FlightLLM | mixed temporal + multi-CU | custom mapping flow | HBM/DDR plus always-on-chip decode state | instruction/block | datacenter mapping ceiling |
| MCore-OPU / FlightOPU | temporal reuse across overlay cores | overlay instructions/compiler mapping | synchronization router, HBM-channel affinity | instruction/tile | programmable-core comparison |
| Nyx | temporal and spatial sharing across regions | hypervisor plus virtual FIFOs | dependency-aware streaming across virtualized regions | task | shared-FPGA execution semantics |
| StreamTensor / CODO | generated dataflow graph | compiler IR and DSE | FIFO/stream tensors and fusion | Transformer block/graph | coarse dataflow contrast |
| MPK | temporal reuse inside a persistent GPU kernel | compiler-generated in-kernel scheduler | SM-level dependency graph | task/fragment | strongest launch-boundary contrast, not FPGA |
| CGRA space-time mapping | separates both axes explicitly | schedule first, spatial mapping second | architecture-dependent | loop/DFG | compiler vocabulary for the distinction |

The DPU/FINN entries are grounded in official documentation reviewed on 2026-09-07; see [[research/fpga-llm-inference/vitis-ai-dpu-finn-pynq]] for source links and platform limits. PYNQ is a deployment/driver ecosystem: its loadable hardware "overlay" does not by itself imply an instruction-programmable overlay processor. Neither entry establishes drop-in U280/GGML support.

## Positioning `llama.v` And The Active Backend

The historical `/home/zdpeng/llama.v` description in [[research/fpga-llm-inference/fpga-backbone-llamacpp-note]] was a **custom token-oriented CPU+FPGA system**: a host command ABI, HBM-resident weights/KV state, an inference controller, and dedicated math blocks. It belongs primarily in the **custom RTL + temporal reuse** cell because its token-level controller sequences reusable functional units over time. It is not automatically an overlay: its ABI is not a general instruction set or CGRA compiler target. It is not a fully spatial LLM accelerator either: the documented architecture does not reserve a distinct hardware pipeline for every layer. Its HBM-resident state and internal handoffs make it compatible with streaming techniques, but streaming must be demonstrated at an explicit producer/consumer boundary rather than inferred from the word `pipeline`.

The active remote `ggml-fpga` backend inspected on 2026-07-28 at commit `402214ed1` has a different present-day shape: it has native GGML support gates and separate operator RTL kernels (`mul_mat`, `rms_norm`, `rope`, `softmax`, `glu`, and others) driven through XRT. Its current mapping unit is an accepted GGML node and often multiple physical launches per node. It is therefore **framework-native temporal dispatch**, not yet a shared persistent engine or a fused streaming graph. The measured `pp512`/`tg128` launch and wait profile in [[research/fpga-llm-inference/project-status-2026-07]] is consistent with this placement.

The historical and active systems share an important constraint: they must preserve a strict external contract. A valid execution mechanism cannot gain performance by silently handing a supported GGML node back to the CPU, publishing a failed device result, or loading an unverified artifact.

## HBM-Aware Decode Is A Separate Overlay

HBM-aware decode means more than storing weights in HBM. A mechanism must state:

1. which weights, KV pages, intermediate fragments, and command buffers are resident in which banks;
2. whether a consumer sees a producer result through an on-chip channel, an HBM write/read, or host synchronization;
3. the bank/channel contention model under batch 1 decode; and
4. the boundary at which a region is allowed to publish a result to the unchanged GGML graph.

FlightOPU supplies channel-affine overlay placement; FMC-LLM/CD-LLM supply high-batch memory-centric decoding; H2-LLM supplies low-batch data-centric DSE. None of those facts establishes the current strict GGML boundary, so they are design references rather than drop-in solutions.

## Implication For The Idea Search

The useful proposal space is the narrow intersection below:

```text
native GGML support/failure/artifact contract
                +
coarse host-visible region or persistent command stream
                +
explicit U280 HBM residency and bank-affinity rule
                +
one measurable low-batch pp/decode downstream metric
```

This excludes a from-scratch universal spatial accelerator, a generic overlay claim, and an ordinary fusion wrapper with no independent control-plane or residency mechanism. The experiment must separately test the decomposition, the HBM/residency rule, and the shared-engine schedule against the strict per-node baseline.

## Related Pages

- [[research/fpga-llm-inference/literature-search-2026-07-28]]
- [[research/fpga-llm-inference/system-landscape]]
- [[research/fpga-llm-inference/end-to-end-evaluation]]
- [[research/fpga-llm-inference/project-status-2026-07]]

Return to [[research/fpga-llm-inference/index]].

---
title: "DANMP: Accelerating Multi-Scale Deformable Attention Using Near-Memory-Processing"
domain: research
area: linear-attention
type: paper
status: processed
updated: 2026-04-21
tags: [paper, misc, linear-attn, danmp, near-memory-processing, deformable-attention]
---

# DANMP: Accelerating Multi-Scale Deformable Attention Using Near-Memory-Processing

## TL;DR
DANMP is a DIMM-based near-memory accelerator for multi-scale deformable attention, not a linear-attention paper in the strict algorithmic sense. Its value for this wiki is architectural: it shows that irregular gather-interpolate-accumulate workloads are memory-bound on GPUs and benefit from a hardware/software co-design that pushes computation next to DRAM.

The paper's main result is strong: 97.43x speedup and 208.47x energy-efficiency improvement over an NVIDIA A6000 GPU on object-detection inference. The design is not just "more PEs near memory"; it combines non-uniform PE placement, a clustering-and-packing software pass, and a custom instruction/dataflow stack tuned for MSDAttn.

## Problem
Multi-Scale Deformable Attention (MSDAttn) is useful because it samples only a sparse set of locations across multi-scale feature maps, but that same sparsity makes memory access highly irregular. The paper's GPU case study shows MSDAttn sits near the roofline and is constrained primarily by memory bandwidth, not arithmetic throughput.

The bottlenecks are specific and recurring:
- Irregular sampling makes prefetching and cache reuse weak.
- Hundreds of detection queries have little spatial or temporal locality.
- Load imbalance is severe because query-specific sparsity varies across scales and tokens.

The paper also argues that prior near-memory accelerators are a poor fit for MSDAttn. Uniform PE deployment wastes compute on cold data, while reassigning work to idle PEs increases cross-bank transfers and aggravates bandwidth pressure.

## Method
DANMP is a hardware-software co-designed DIMM-based NMP system for MSDAttn.

On the hardware side, DANMP uses non-uniform integration across the DRAM hierarchy. It places processing elements at three levels:
- near-rank PEs for global aggregation and control
- near bank-group PEs for reductions and coordination
- near-bank PEs only in selected banks for hot entries

The key architectural idea is not uniform acceleration but selective placement. The design maps hot entries to bank-level PEs and cold entries to bank-group PEs so that the system keeps work close to data without creating cross-bank transfers.

On the software side, DANMP introduces clustering-and-packing (CAP). CAP clusters queries with similar sub-targets, then repacks them to improve temporal locality and reduce redundant sampling work. The paper reports a 1.45x speedup from CAP alone over a CPU baseline, and a 2.21x improvement from the non-uniform DANMP hardware versus the uniform variant.

The host/NMP interface is also explicit:
- a compressed 83-bit instruction format
- mode selection between DRAM and NMP execution
- opcodes for sum, weighted sum, interpolation, and related primitives
- a small instruction queue and bank-selective dispatch

## Results
The headline numbers are the ones to remember:
- 97.43x average speedup over an NVIDIA A6000 GPU
- 208.47x energy-efficiency improvement over the same GPU
- 557.31x speedup over CPU across evaluated datasets/models
- 13.74x average speedup over DEFA, the paper's strongest ASIC baseline
- 3.43x speedup over SADIMM
- 1.45x speedup from CAP alone over CPU
- 2.21x gain from DANMP over the uniform-integration variant

The paper also reports a 143x reduction in MSDAttn latency and a 67x end-to-end Deformable DETR inference improvement in the roofline-driven framing, and it argues that the GPU roofline can be lifted by 128x in bandwidth-constrained regions once the workload is moved into memory.

The default CAP setting uses a 20 percent clustering ratio, chosen as the best tradeoff between reuse and clustering overhead.

## Implementation Clues
This paper is most useful as a systems reference because it is unusually concrete about the memory hierarchy and simulation stack.

- The implementation is DIMM-based and DDR5-compatible, so it avoids exotic HBM/ReRAM assumptions.
- The memory hierarchy is modeled as 4 channels, 1 DIMM per channel, 2 ranks, 8 bank-groups, and 4 banks per group.
- The simulation stack uses gem5 for the processor/cache side and Ramulator for the DDR5/NMP memory side.
- Hardware synthesis targets 40 nm CMOS at 300 MHz, aligned with DDR5-4800 timing assumptions.
- Energy modeling uses Synopsys Design Compiler plus CACTI-3DD and CACTI-IO.

The most reusable idea is the workload mapping policy: classify data by access frequency, then pin the hottest 50 percent to PE-equipped banks while routing colder data through bank-group-level execution. That is the paper's concrete answer to the load-imbalance problem.

## Limitations
The paper is strong as a hardware study, but it is not a general-purpose attention solution.

- The target workload is MSDAttn in Deformable DETR, not standard linear attention.
- The accelerator assumes a fairly specialized DIMM/NMP stack and a custom instruction path.
- The software optimization is workload-specific and relies on clustering quality.
- The results are primarily from simulation and case-study evaluation, so the claims are architecture-bound rather than deployment evidence.

For this wiki, that matters because DANMP is best used as a near-memory design reference for irregular attention-like workloads, not as a direct baseline for linear-attention algorithms.

## Takeaways
DANMP supports a broader conclusion that shows up repeatedly in the linear-attention hardware thread: when the workload is dominated by irregular memory access, algorithmic asymptotics matter less than data movement and load balance.

The paper's strongest reusable lessons are:
- selective, non-uniform compute placement is better than uniform PE replication for irregular access patterns
- clustering can recover enough locality to matter even when the sampling pattern is sparse
- cross-bank transfer avoidance is a first-order design goal, not an implementation detail

Even though DANMP is about deformable attention rather than linear attention, it is still a useful anchor for the same systems question: how to keep attention-like state and sampling logic close to memory without turning the memory hierarchy into the bottleneck.

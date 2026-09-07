---
title: FPGA LLM Architecture Literature Refresh, 2026-07-28
domain: research
area: fpga-llm-inference
type: synthesis
status: active
updated: 2026-07-28
tags: [fpga, llm-inference, literature-review, hbm, dataflow, cgra, coarse-grained-execution]
---

# FPGA LLM Architecture Literature Refresh, 2026-07-28

## Scope And Method

This refresh asks a narrower question than a generic FPGA-LLM survey: which recent work informs a contract-preserving, low-batch `llama.cpp`/GGML execution path on a U280 when the limiting factor is launch/wait amplification rather than isolated arithmetic throughput?

The search used an unfiltered six-query union over arXiv, DBLP, OpenAlex, OpenReview, Semantic Scholar, and Crossref for 2024-2026. The complete 142-paper ranked table, every terminal connector error, keyword counts, citation statistics, model-knowledge anchors, and reading path are in [[allinone]]. Existing 2020-2023 papers remain historical anchors rather than being re-searched or replaced.

## Search Snapshot

| Source | Hits | Outcome |
|---|---:|---|
| arXiv | 60 | completed |
| OpenAlex | 60 | completed after five HTTP 504 retries |
| Crossref | 60 | completed |
| Semantic Scholar | 1 | one query returned; five rate-limited after bounded retries |
| DBLP | 0 | all six queries failed with timeout/TLS errors |
| OpenReview | 0 | completed without a hit in the canonical rerun |

The resulting 241 source records deduplicated to 142 unique papers, merging 39 cross-source duplicates. There was no relevance-score cutoff. This is intentionally high recall, so the query table contains unrelated records caused by broad terms such as `fusion`, `HBM`, and `coarse-grained`.

## Admission Rule

A search hit was added to [[research/fpga-llm-inference/papers/index]] only when it directly concerns at least one of:

- shared or temporally reused FPGA computation and its control plane;
- spatial, overlay, streaming, or graph-dataflow execution for Transformer/LLM work;
- HBM-aware or low-batch autoregressive decode;
- CPU-FPGA heterogeneous inference or a framework/offload boundary;
- coarse-grained, persistent, or graph-fused execution; or
- overlay/CGRA compiler mapping that clarifies the temporal-versus-spatial distinction.

The admission check uses DOI, arXiv ID, normalized title, and slug against the existing 68 records. It added 15 new records. Two public PDFs passed the local full-paper gate (PDF signature, parseability, title check, and at least two pages): MPK and the CGRA space-time mapping paper. The remaining 13 are explicitly `metadata-only`; RISCBench's public arXiv file is a one-page extended abstract, and publisher 403 pages were not cached as papers.

## Curated Additions

| Paper | Design relevance | Cache state |
|---|---|---|
| [[papers/mpk-2025/index|MPK]] | Persistent mega-kernel and decentralized in-kernel task runtime; GPU-specific but the clearest coarse-grained launch-boundary contrast. | PDF validated |
| [[papers/cd-llm-2026/index|CD-LLM]] | Published high-batch multi-FPGA decode contrast, with an HBM master and compute-dedicated slaves. | metadata-only |
| [[papers/flightopu-2025/index|FlightOPU]] | HBM-channel-affine overlay and multi-die control/mapping. | metadata-only |
| [[papers/nyx-2025/index|Nyx]] | Shared-FPGA temporal/spatial virtualization plus dataflow scheduling through virtual FIFOs. | metadata-only |
| [[papers/pcie-coarse-systolic-2025/index|PCIe coarse systolic arrays]] | Direct PCIe-FPGA LLM co-design and larger PE granularity. | metadata-only |
| [[papers/riscbench-2026/index|RISCBench]] | Explicit orchestration/residency measurement vocabulary for the control-plane bottleneck. | metadata-only; 1-page public abstract rejected |
| [[papers/h2-llm-2025/index|H2-LLM]] | Low-batch data-centric dataflow/DSE and compute-bandwidth tradeoffs. | metadata-only |
| [[papers/mcore-opu-2024/index|MCore-OPU]] | Temporal overlay execution plus reduced inter-core synchronization traffic. | metadata-only |
| [[papers/streaming-vpe-2024/index|Streaming VPE]] | Streaming nonlinear engine with look-ahead reduction dataflow. | metadata-only |
| [[papers/dtcore-2026/index|DTCore]] | Compiler-directed control-minimal FPGA engine; title/venue seed only. | metadata-only |
| [[papers/festal-2026/index|FESTAL]] | Graph-based dataflow fusion synthesis; title/venue seed only. | metadata-only |
| [[papers/fmc-llm-2025/index|FMC-LLM]] | Memory-centric streaming high-batch decode, likely useful lineage for CD-LLM. | metadata-only |
| [[papers/e2e-overlay-compiler-2025/index|Unified overlay compiler]] | End-to-end overlay compilation comparison point. | metadata-only |
| [[papers/lembda-2026/index|Lembda]] | CPU-FPGA LLM co-processing anchor pending full-text verification. | metadata-only |
| [[papers/cgra-space-time-2025/index|CGRA space-time mapping]] | Formal separation of temporal scheduling and spatial placement. | PDF validated |

## Synthesis

Four observations matter for the current U280 prototype.

1. **Spatial mapping, overlays, and streaming are not interchangeable.** Spatial LLM-style designs statically reserve hardware for a model mapping. Overlay designs reuse programmable cores over time. Streaming dataflow systems move produced fragments directly to dependent consumers. A design can combine these, but merely calling a design `dataflow` does not identify its scheduling or storage contract.
2. **A shared engine creates a control problem before it creates a compute win.** MPK, Nyx, RISCBench, DTCore, and the coarse-systolic work all point to scheduler, launch, and residency overhead as first-class design objects. This aligns with the measured U280 path, where host-observed wait dominates before HBM bandwidth becomes the clean bound.
3. **Decode literature is split by batch regime.** FMC-LLM/CD-LLM optimize high-batch 70B+ system throughput. FlightOPU and H2-LLM discuss memory/compute affinity and low-batch dataflow. Neither family proves strict native GGML admission, artifact identity, or a zero-fallback failure boundary.
4. **The missing intersection is a coarse-grained execution mechanism with framework semantics.** Existing fusion/dataflow papers generally own their compiler/runtime boundary. The current backend owns the native boundary but executes at node/tile granularity. A viable contribution must connect these without claiming that an ordinary fused region is novel by itself.

## Reading Path

1. [[papers/spatial-llm-2024/index]] for prefill/decode mapping constraints.
2. [[papers/edgellm-2025/index]] for a close CPU-FPGA heterogeneous system.
3. [[papers/streamtensor-2025/index]] and [[codo-2026]] for block/graph streaming and compiler-controlled dataflow.
4. [[papers/mpk-2025/index]], [[papers/nyx-2025/index]], and [[papers/riscbench-2026/index]] for execution granularity and control-plane evidence.
5. [[papers/flightopu-2025/index]], [[papers/h2-llm-2025/index]], and [[papers/fmc-llm-2025/index]] for HBM/dataflow placement and batch-regime limits.

## Resulting Design Boundary

The selected idea is not a from-scratch spatial accelerator and is not sold as universal fusion. VSTC is a measurable, U280-realizable coarse-grained/HBM-aware execution mechanism for the existing shared, temporally scheduled path. It retains all of the following:

- native llama.cpp/GGML execution;
- explicit support rejection and explicit runtime failure;
- artifact identity from source to loaded xclbin; and
- zero fallback inside the declared evaluation scope.

The vocabulary and exact placement of the historical `llama.v` architecture and active `ggml-fpga` backend are recorded in [[research/fpga-llm-inference/execution-architecture-taxonomy]]. The audited proposal, closest-work difference, controls, and stopping rules are in [[research/fpga-llm-inference/ideaspark-shared-engine-2026-07-28]].

Return to [[research/fpga-llm-inference/index]].

---
title: Shared-Engine GGML FPGA IdeaSpark Result, 2026-07-28
domain: research
area: fpga-llm-inference
type: research-result
status: proposal-audited
updated: 2026-07-28
tags: [fpga, llm-inference, llama-cpp, ggml, u280, xrt, coarse-grained-execution, ideaspark]
---

# Shared-Engine GGML FPGA IdeaSpark Result, 2026-07-28

## Terminal State

Fresh run: `DONE`. The run is independent of the earlier RegionSeal failure under `ideaspark_run/towards-general-fpga-backbone/`. It passed literature grounding, full-text gating, bottleneck diagnosis, candidate coherence tracing, signature and alias collision retrieval, an adversarial critique, a bounded revision, a falsification re-audit, an implementability audit, and five final validators (`5 pass`, `0 warn`, `0 fail`).

This is an audited research proposal, not a measured performance claim. It does not assert that the U280 implementation already reduces latency or that the mechanism is novel against every deferred-execution runtime; those are explicitly testable conditions below.

## Research Question

How can a U280 shared temporally multiplexed FPGA engine execute contract-closed, coarse-grained, HBM-aware GGML regions for low-batch LLM inference while preserving native `llama.cpp` execution, explicit failure, artifact identity, and zero fallback?

The concrete anchor is Gemma 3 1B F16 on U280. The current native path expands 1,626 GGML calls into 224,936 XRT launches for `pp512`; `tg128` expands 104,877 calls into 202,530 XRT launches. Host-observed XRT wait dominates before a clean arithmetic or HBM bandwidth bound is reached.

## Selected Mechanism: VSTC

**Visibility-Sensitive Trace Compression (VSTC)** emits a ticket for every original supported GGML call before it expands into XRT submissions. A ticket captures the operator/layout, patchable scalar arguments, logical allocation and byte span, producer tickets, all captured later readers/consumers, scratch demand, and host-observation, alias, and state-effect flags.

VSTC holds admission until a declared closed GGML execution boundary. It places a call in protected class `H` unless every later reader is captured, no host observation/status barrier, state write, or escaped alias exists, exactly one consumer is ticket-aware, the installed exact F16 kernel is available, and an exclusive scratch lease survives until the recorded consumption-complete event. Maximal eligible `B` runs become patchable exact template entries on the resident shared engine. `H` calls retain individual descriptors, materialization to their original native allocation, and per-call completion/error state. Every original logical call owns a completion-ring slot; no CPU implementation is used as a fallback.

The design is HBM-aware through explicit scratch-byte demand and lease lifetime, not through an unmeasured claim about a new HBM layout. Its load-bearing measurement is `rho`: the fraction of baseline XRT submissions represented by admitted `B` template entries on the same closed trace.

## Difference From Close Work

- **Big PE** increases an 8-bit systolic compute cell for TinyStories prompt processing. VSTC leaves the installed F16 data-plane kernels in place and changes the native control-plane representation across both prefill and decode.
- **LlamaF** uses static model-specific W8A8 matrix concatenations and leaves attention control/KV handling on the processing system. VSTC dynamically captures live GGML host-read, alias, state, allocation, consumer, scratch, and explicit-error facts before admitting an exact template.
- **CDA-GNN** is the closest collision hit: it runs compiler-predetermined dependency chains on a U280 for GNN state propagation. VSTC's claimed delta is dynamic per-original-GGML-call observation and failure preservation, not dependency scheduling alone.

The remaining prior-art condition is explicit: a targeted scoop check must establish whether dynamic CUDA Graphs, runtime command buffers, or XRT command-buffer schedulers already preserve the same full native semantic admission contract. The candidate only survives if that protocol is absent or materially different.

## Minimal Falsification

Implement the exact supported Gemma 3 1B F16 path in `llama.cpp` on U280 and run `pp512` and `tg128` with fixed 512-token prompts from `wikitext-2-raw-v1`. Compare native per-XRT dispatch, a naive resident descriptor engine, and VSTC. Require bytewise logits and ordered explicit-error traces to match the native path.

If VSTC is correct, `pp512` latency and `tg128` p50/p95 per-token latency fall as `rho` rises above zero; actual XRT run submissions fall in the same direction without CPU fallback. A full-observation oracle forces every produced tensor to be checked after each call, testing whether an incorrect result came from capture rather than template execution.

## Negative Controls And Stop Conditions

- Force B admission off for exactly otherwise eligible calls while retaining the same kernels, inputs, resident engine, tickets, and completion ring. If p50/p95 does not move back toward the naive resident-engine baseline, the visibility-sensitive claim is falsified.
- On an all-eligible homogeneous slice, compare the single-record and multi-record interpreter. On a mixed trace, toggle only B admission while holding the engine fixed. These controls separately identify the interpreter and H/B partition effects.
- Stop VSTC rather than relabeling an ordinary resident engine if there is no eligible B population, `rho = 0`, required scratch cannot be leased, or any later reader/alias/state effect cannot be captured.
- Stop the claim on any bytewise-logit mismatch, explicit-error/order mismatch, new CPU fallback, artifact-identity break, or a collision result showing an equivalent native semantic admission protocol.

## Run Artifacts

- [Final candidate](ideaspark_run/shared-engine-llama-fpga/phase3_revise/final_candidate.json)
- [Collision retrieval](ideaspark_run/shared-engine-llama-fpga/phase3_collision/collision_hits.json)
- [Critique and revision](ideaspark_run/shared-engine-llama-fpga/phase3_critique/phase3_critique_output.json) and [patches](ideaspark_run/shared-engine-llama-fpga/phase3_revise/phase3_revise_output.json)
- [Falsification re-audit](ideaspark_run/shared-engine-llama-fpga/phase3_critique/falsification_reaudit.json)
- [Chinese standard card](ideaspark_run/shared-engine-llama-fpga/phase4/idea.std.zh.md), [English standard card](ideaspark_run/shared-engine-llama-fpga/phase4/idea.std.en.md), and [reviewer card](ideaspark_run/shared-engine-llama-fpga/phase4/idea.detail.en.md)
- [Final validator evidence](ideaspark_run/shared-engine-llama-fpga/phase4/phase4_implementability.json)

Return to [[research/fpga-llm-inference/index]].

---
title: FPGA LLM Inference Backbone Development Note
domain: research
area: fpga-llm-inference
type: engineering
status: stale
updated: 2026-07-22
tags: [fpga, llm-inference, llama-cpp, ggml, history]
---

# FPGA LLM Inference Backbone Development Note

Original date: 2026-06-17

> [!NOTE]
> This is a historical integration snapshot. The backend and paper evidence advanced substantially after it was written. Use [[research/fpga-llm-inference/project-status-2026-07]] for current measured results and [[research/fpga-llm-inference/end-to-end-evaluation]] for the active comparison protocol.

## Context

Current related artifacts:

- Remote FPGA development target: `ssh fpga-tailscale`, project directory: `/home/zdpeng/llama.v`.
- Reference software implementation: `/Users/pengzedong/Documents/GitHub/llama.x/llama.cpp`.
- Slide / proposal material: `/Users/pengzedong/Documents/GitHub/EPCC/weekly_report_record/2026-06-16-Towards a General FPGA Backbone for LLM Inference/fpga_llm_inference_slides.tex`.
- Wiki location: `/Users/pengzedong/Documents/GitHub/llmwiki/wiki/research/llm-inference`.

## Evidence Read Before Judgment

### `llama.v` project shape

`/home/zdpeng/llama.v` is not just a single Verilog file. It is already a CPU+FPGA hybrid inference project with:

- `rtl/compute/`: `matvec_engine.sv`, `rmsnorm.sv`, `rope.sv`, `geglu.sv`, `softmax.sv`, `dequant_q4_0.sv`.
- `rtl/memory/`: `hbm_ctrl.sv`, `weight_loader.sv`, `kv_cache.sv`.
- `rtl/top/`: `vitis_kernel_top.sv`, `inference_ctrl.sv`, `config_regs.sv`, `cmd_interface.sv`.
- `host/`: `main.cpp`, `xrt_driver.*`, `gguf_loader.*`, layout/runtime contracts, and many contract tests.
- `tools/`: Gemma 3 1B layout/trace/package generators.
- `scripts/`: Vitis/Vivado build, link, smoke, and synthesis scripts.

The README explicitly says the project direction is a `llama.cpp`-compatible CPU+FPGA runtime: CPU keeps tokenizer/GGUF/EOG/detokenize/sampler/control duties, while FPGA focuses on the HBM-backed token hot path. It also says a full FPGA runtime is not the near-term goal.

The current hardware target is Xilinx Alveo U280 via Vitis/XRT. The reference path is Gemma 3 1B F16 with short-context bring-up. The current ABI is token-oriented: host writes a token and command flags over AXI-Lite; FPGA returns a greedy output token ID; CPU owns EOG/detokenization and future non-greedy sampling.

### `llama.cpp` backend shape

`llama.cpp` / `ggml` already has a backend abstraction that matches an accelerator integration:

- Public backend API: `ggml/include/ggml-backend.h`.
- Internal backend vtables: `ggml/src/ggml-backend-impl.h`.
- Backends live under `ggml/src/ggml-*`, e.g. `ggml-cuda`, `ggml-metal`, `ggml-vulkan`, `ggml-sycl`, `ggml-opencl`, `ggml-openvino`, `ggml-hexagon`, `ggml-rpc`.
- `ggml/src/CMakeLists.txt` uses `ggml_add_backend(...)` to include optional backend directories.
- Device capabilities include CPU/GPU/IGPU/ACCEL/META classes, async transfer, host buffers, buffer-from-host-ptr, event support, `supports_op`, `supports_buft`, and `offload_op`.

This means an FPGA integration can be represented naturally as either:

1. a normal `ggml` backend (`ggml-fpga` / `ggml-xrt`) that implements selected ops, or
2. a higher-level experimental path that uses llama.cpp tokenization/model metadata but calls a full-token FPGA decode engine.

## GitHub Issue / PR Scan

Searched `ggml-org/llama.cpp` open issues/PRs for FPGA/backend/accelerator/hardware terms.

Direct FPGA result:

- No direct open issue titled as a generic FPGA backend request.
- Open PR `#24179 Initial ET backend` appears in FPGA search results because it mentions that the open ET-SOC-1 RTL could in principle be implemented on FPGA.
- Closed FPGA-related history includes mostly SYCL/Intel FPGA mentions and older AMD XDNA discussion.

Relevant active backend signals:

- Issue `#21725 Feature Request: XDNA backend` proposes an AMD XDNA NPU backend using XRT and compiled kernels, starting with `GGML_OP_MUL_MAT`, then adding norms/RoPE/softmax/fusion. This is highly relevant because it is also XRT-style accelerator integration.
- Issue `#23219 RFC: tilelang backend for llama.cpp` proposes a codegen/multi-backend kernel path.
- Issue `#10453 ggml : add ANE backend` is a roadmap/research backend request.
- PR `#24179 Initial ET backend` is an active open backend PR for an open-source hardware processor, with maintainer/CI discussion.
- Many active PRs/issues are backend infrastructure work: shared backend scheduling, cross-backend profiler, async RPC backend APIs, dynamic backend loading, backend buffer interface changes, and backend op test coverage.

Interpretation: upstream is still receptive to new backend work, but it expects maintainability, tests, CI/story for hardware access, and integration through `ggml` backend conventions rather than a monolithic separate runtime.

## Revised Judgment

After reading both the `llama.v` project structure and `llama.cpp` backend structure, the better judgment is more nuanced:

**Yes, the long-term direction should be `llama.cpp` integration, but not immediately as a large monolithic upstream PR.**

`llama.v` is already doing the thing conceptually: it is a CPU+FPGA LLM inference engine where CPU keeps llama.cpp-like runtime responsibilities and FPGA owns the token hot path. However, its current shape is not yet a drop-in `ggml` backend:

- It owns a standalone host CLI (`host/main.cpp`).
- It parses/stages GGUF tensors through its own `GGUFLoader`.
- It has a token-level AXI-Lite ABI rather than a generic `ggml` op-level ABI.
- It is specialized around U280/XRT, Gemma 3 1B, F16, greedy output, and current short-context constraints.
- It returns sampled/argmax token IDs, while `ggml` backends normally compute tensor ops inside the llama.cpp graph.

So the right direction is not “move all of `llama.v` into llama.cpp now.” The right direction is:

1. keep `llama.v` as the hardware bring-up and contract-validation repository;
2. extract a narrow XRT/FPGA backend boundary that can map into `llama.cpp`/`ggml`;
3. decide whether the first upstreamable slice is op-level or token-engine-level.

## Two Possible Integration Paths

### Path A: `ggml` op-level FPGA backend

This is the most upstream-aligned path.

Shape:

```text
llama.cpp / ggml graph
  -> ggml-fpga backend
      -> XRT buffer allocation / HBM upload
      -> FPGA kernels for selected ggml ops
          -> matvec / mul_mat first
          -> RMSNorm / RoPE / softmax later
```

Pros:

- Fits existing backend abstraction.
- Easier to compare with CPU using `test-backend-ops`.
- Easier to upstream incrementally.
- Allows CPU fallback for unsupported ops.
- Similar to the direction proposed in XDNA issue `#21725`.

Cons:

- May underuse the existing `llama.v` token-level FSM.
- Requires exposing FPGA compute as ggml ops rather than a whole-token engine.
- More host/device transfer overhead unless buffers and fusion are handled carefully.

Best first primitive: `GGML_OP_MUL_MAT` / matvec for a narrow dtype/layout, possibly F16 first, then Q4_0 or a GGUF-compatible quant.

### Path B: llama.cpp-compatible token-engine backend

This matches the current `llama.v` architecture more directly.

Shape:

```text
llama.cpp model/tokenizer/sampler shell
  -> FPGA token decode engine
      -> upload full model layout to HBM
      -> send token IDs over command ABI
      -> receive logits or greedy token IDs
```

Pros:

- Reuses more of current `llama.v` design.
- Better for demonstrating end-to-end FPGA token throughput.
- Preserves the HBM-backed full transformer hot path.

Cons:

- Less aligned with `ggml` backend abstraction.
- Harder to upstream because it bypasses much of the ggml graph execution model.
- Current ABI returns greedy token IDs, not logits, which limits integration with llama.cpp samplers.
- Model support and context constraints are currently too narrow for a general upstream backend.

If following this path, the ABI should probably evolve from “return greedy token id” to “return logits or top-k candidate data,” so llama.cpp can keep sampler semantics.

## Recommended Direction

Continue developing `llama.v` as a standalone hardware bring-up repo for now, but structure the next milestones so they can become a `llama.cpp` backend later.

Concretely:

1. Do not attempt a broad upstream PR yet.
2. Keep using `llama.v` for Vitis/XRT, HBM layout, RTL simulation, and hardware smoke tests.
3. Add a clean host-side library boundary around the current XRT driver + ABI, separate from the standalone CLI.
4. Choose the upstream slice:
   - If aiming for upstream acceptance: start with a minimal `ggml-fpga` backend claiming one op, probably `MUL_MAT`.
   - If aiming for research demo first: keep token-engine mode, but change the ABI toward logits/top-k so llama.cpp can own sampling.
5. Use `llama.cpp` CPU output and `test-backend-ops` style contracts as correctness oracles.
6. Treat the current `llama.v` host CLI as a bring-up harness, not the final product interface.

## Updated Working Thesis

`llama.v` is already a llama.cpp-compatible CPU+FPGA inference engine in spirit, but it is not yet shaped like a llama.cpp upstream backend. The best path is staged convergence:

```text
llama.v standalone bring-up
  -> stable XRT/FPGA ABI + correctness contracts
  -> minimal llama.cpp/ggml FPGA backend prototype
  -> upstreamable small PR once one op or one clearly-scoped path is correct, tested, and maintainable
```

So the original intuition remains directionally right, but the immediate engineering conclusion changes: **develop the hardware and ABI in `llama.v` now; design every boundary so that the smallest credible next integration can live under `llama.cpp/ggml/src/ggml-fpga` later.**

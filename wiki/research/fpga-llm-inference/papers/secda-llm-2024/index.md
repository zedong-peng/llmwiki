---
title: "SECDA-LLM: Designing Efficient LLM Accelerators for Edge Devices"
domain: research
area: fpga-llm-inference
type: paper
status: active
updated: 2026-09-08
tags: [paper, fpga, llm-inference, llama-cpp, ggml, framework-backend, systemc]
---

# SECDA-LLM: Designing Efficient LLM Accelerators for Edge Devices

SECDA-LLM is a direct precedent for integrating FPGA acceleration into llama.cpp/GGML.
Its 2024 case study accelerates quantized MatMul within application-level TinyLlama inference;
it is neither a standalone full-model FPGA pipeline nor merely a disconnected MatMul benchmark.

## Paper Identity

- Authors: Jude Haris, Rappy Saha, Wenhao Hu, Jose Cano; University of Glasgow.
- Reviewed record: [arXiv:2408.00462](https://arxiv.org/abs/2408.00462), 2024, five pages.
- Manuscript key: `secda_llm`. Venue beyond the reviewed arXiv record was not verified.
- Source-first read: [main TeX](source/extracted/00_main.tex), all five included sections,
  [commands](source/extracted/commands.tex), and complete [compiled bibliography](source/extracted/00_main.bbl).
- [Source archive](source/archives/2408.00462-source.tar.gz), [PDF](2408.00462.pdf),
  [source receipt](source/download-audit.json), [metadata](metadata.yaml).

## Method

The design platform integrates SECDA (SystemC Enabled Co-design of DNN Accelerators) with
llama.cpp's application and GGML execution. Its context handler transfers memory pointers,
memory-mapped model data, tensors, quantization and layer parameters into a custom C++ driver.
The designer writes the driver and a SystemC accelerator and connects AXI-Stream, AXI-MM or
AXI-Lite channels. SystemC simulation permits application-level iteration before synthesis;
the SECDA interfaces select simulation versus hardware execution through a compiler flag.
This is a reusable co-design methodology, not automatic lowering of arbitrary model graphs.

The case study targets `MatMul_Q3_K_Q8_K`. A weight super-block represents 256 weights split
into 16 tiles, with 3-bit weights, per-tile scales and a super-scale. The proposed accelerator
contains an instruction decoder, data mapper, scheduler and Super-Block Vector Processor.
The scheduler tiles the target MatMul, accumulates results and returns them through AXI-Stream.
The paper calls this block floating point; do not silently equate its representation or accuracy
with another work's uniform INT3 format.

## Reported Evaluation

[Section IV](source/extracted/04_evaluation.tex) uses PYNQ-Z1 with a Z020 FPGA and a 650 MHz
dual-core Cortex-A9. The model is TinyLlama-1.1B, trained on the Guanaco dataset, occupying
approximately 460 MB with mixed quantization, predominantly Q3_K. The authors cross-compile
llama.cpp's `main` application for ARMv7a with NEON and the custom driver.

The paper reports 1.7 seconds/token, approximately 11x faster than CPU-only inference.
This is a paper-reported application result, not a locally reproduced number. No separate
prefill/decode timing table, specified prompt/output-length sweep, multi-checkpoint FPGA
comparison, detailed numerical-equivalence gate, or power comparison is provided in this
short paper. Its conclusion describes an open-source platform as future work.

## Public Code: A Later Snapshot

The author-maintained [SECDA-LLM repository](https://github.com/judeharis/SECDA-LLM) is archived
at `183376a652b47a30b5b57cd34965b45e9297f39a` in [repo/SECDA-LLM](repo/SECDA-LLM/).
Its README still says WiP; [docs/lpp_updates.md](repo/SECDA-LLM/docs/lpp_updates.md) explicitly
explains adaptation to a newer llama.cpp API. It must not be presented as the 2024 experimental freeze.

The root [Git tree](repo/SECDA-LLM-git-tree.json) pins two dependencies, both archived separately:

| Dependency | Commit | Local directory |
|---|---|---|
| judeharis/llama.cpp | `b8b0a4c46ab43f1f777a4a0250908997c539bf11` | [repo/llama.cpp](repo/llama.cpp/) |
| judeharis/secda_tools | `0b842d76df03546830037023f1281bd98aba4e5f` | [repo/secda_tools](repo/secda_tools/) |

These are sibling audit copies, not initialized submodules. Two llama.cpp symlinks reaching into
the parent project's `srcs/` were deliberately omitted from extraction; their original targets
remain in the untouched archive and [download receipt](repo/llama.cpp-download.json).
No setup/build scripts were executed. Model weights, compatible hardware images, SystemC/toolchain
installation and board runtime configuration are not included in this audit.

### Inspected Execution Path

- [setup.sh](repo/SECDA-LLM/setup.sh) links the custom backend into the vendored GGML tree;
  [CMakeLists.txt](repo/SECDA-LLM/CMakeLists.txt) enables `GGML_SECDA` and builds that llama.cpp tree.
  [CMakePresets.json](repo/SECDA-LLM/CMakePresets.json) distinguishes x64 SystemC simulation,
  backend-disabled builds, ARMv7 and AArch64 targets.
- [ggml-secda.cpp](repo/SECDA-LLM/srcs/ggml_backend/ggml-secda/ggml-secda.cpp) implements backend/device
  registration, `graph_compute`, a type/contiguity/dimension support gate and host-buffer access.
  `supports_op` admits selected quantized `MUL_MAT` nodes; it does not admit attention, softmax,
  normalization or KV-update operations. An `OUT_PROD` branch in the executor is not evidence of
  support: the admission function does not admit it and its helper is empty.
- [ops_support.cpp](repo/SECDA-LLM/srcs/ggml_backend/ggml-secda/ops_support.cpp) quantizes F32 inputs
  into Q8_K work buffers and calls `EntryMM` with tensor dimensions, strides and quantization type.
  The selected v1 [driver](repo/SECDA-LLM/srcs/ggml_backend/ggml-secda/acc_dels/bfpp_acc/v1/accelerator/driver/acc_driver.h)
  checks input/weight buffer limits, manages weight preloading and calls the accelerator path.
  The v1 configuration distinguishes Z1/Kria MMIO and DMA layouts; other versions were not fully audited.
- The pinned framework's [KV cache](repo/llama.cpp/src/llama-kv-cache.cpp) retains layer K/V tensors,
  provides historical views and appends current values through `ggml_set_rows`. SECDA returns the
  CPU buffer type and does not admit the update operators. This supports host/framework-managed
  persistent KV, not an FPGA-resident KV manager. Host state still counts under a system-level KV
  predicate; device residency is a separate property.
- [run_llama_cli.sh](repo/SECDA-LLM/benchmark/scripts/run_llama_cli.sh) invokes a GGUF model with a
  prompt, sampling parameters and output-token limit. It defaults to one token, so the script's
  presence alone is not a multi-step generation receipt. The newer CLI uses the framework server
  context; token selection/decode remain framework work. Config files for several models and runtime
  variants are experiment specifications, not proof those checkpoints ran on FPGA.

Repository inspection is targeted, not a full correctness or buildability review. No CPU inference,
SystemC simulation, synthesis, FPGA execution or independent reproduction was performed.

## Feature-Table Classification

| E2E generation | P+D | Multi-model | Auto mapping | Persistent KV | Framework backend | Public artifact |
|---|---|---|---|---|---|---|
| Y | P | NR | NR | Y (current source, host) | Y (current source) | Src (current source) |

E2E Y retains the paper's TinyLlama application-generation claim. P+D P records MatMul offload
without separate phase evidence; automatic operator dispatch and SystemC synthesis are not automatic
model mapping. These evidence classifications are retained in this note; the latest manuscript
moves SECDA to integration-precedent prose rather than the principal feature table because the
original evaluation protocol is limited. The prose separates the current source from 2024.
All marks describe evidence scope, not reproduced correctness.

## Implication For Our Backend

A new FPGA backend cannot claim novelty solely from llama.cpp/GGML integration. Relevant distinctions
to test are operator coverage, host versus FPGA KV placement, state semantics across calls, fallback
boundaries, model portability, and traceable correctness/performance receipts. Partial MatMul offload
within a real framework is still a meaningful framework-integration baseline.

The bibliography places this work after SECDA and SECDA-TFLite; it cites NPE and an earlier Transformer
accelerator for hardware context, and llama.cpp/GGML, TinyLlama, Guanaco and PYNQ-Z1 for its application
and case-study inputs. These citations do not supply missing FPGA phase or accuracy measurements.

See [[research/fpga-llm-inference/feature-level-evidence-matrix]] and return to
[[research/fpga-llm-inference/papers/index|FPGA LLM paper library]].

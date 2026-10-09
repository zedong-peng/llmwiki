---
title: "Efficient Kernel Mapping and Comprehensive System Evaluation of LLM Acceleration on a CGLA (IMAX)"
domain: research
area: fpga-llm-inference
type: paper
status: active
updated: 2026-09-27
tags: [paper, cgla, imax, llama.cpp, fpga-prototype]
---
# IMAX: LLM acceleration on a CGLA through llama.cpp

IEEE Access 2025 (bibkey `imax_cgla`; arXiv 2512.00335). Local files: `paper-pdf/2512.00335v1.pdf`,
`paper-tex/archives/2512.00335v1.tar.gz`, `github-repo/IMAX3-LLM`.

## Original-text verification (2026-09-27)
- Platform: IMAX3 CGLA prototype on AMD Versal Premium VPK180 evaluation kits (Vivado 2024.1), eight-lane IMAX at 145 MHz with an Arm Cortex-A72 PS host; two lanes used in the main experiments because the host limits scaling (experiments_and_results.tex:15-27; proposed.tex:179).
- Models: Qwen3-0.6B, 1.7B and 8B in Q3_K_S and Q8_0 GGUF (figure files and experiments section).
- Execution model: hybrid llama.cpp; the host handles tokenization, embedding, KV cache management, final softmax, RMSNorm and RoPE; quantized dot-product kernels (FP16, Q8_0, Q3_K, Q6_K) are offloaded, with host-side DMA coalescing (proposed.tex:27-43, 203-209).
- Throughput appears only in figures (E2E latency per model/format); no absolute token/s in the text. A 28 nm ASIC projection is estimated, not measured.
- (2026-09-28) Only absolute FPGA timing in the text: Qwen3-0.6B Q3_K_S, 32 prompt + 16 output tokens, 2 lanes, 16.3 s end to end (kernel 4.47 s, host CPU 5.43 s, DMA load 5.31 s; discussion.tex:106-110). Prefill and decode are not separated, so no decode token/s can be derived. Other quoted latencies (5.63 s, 14.7 s) belong to the 28 nm projection or are ambiguous (experiments_and_results.tex:298, 318).

## Role in the backend paper
Native llama.cpp entry with complete generation (host operators), but per-kernel offload and host-managed KV: not device-resident.

## Public code audit (2026-09-28)

Repository github.com/Takuto-Ando/IMAX3-LLM (2 stars, single commit 2025-11-19). It is a llama.cpp fork with the IMAX kernels as already-generated C (imax-emax7*.c) plus prebuilt .obj files and aarch64 binaries. It contains no bitstream, no hardware design and no benchmark scripts, logs or results. The README's build steps do not match the repo: scripts/load_bitstream.sh, imax_2lane.xclbin, the -DLLAMA_IMAX CMake option and src/kernels/ do not exist, and the clone URL points to naist-arch-lab/imax-llm. Regenerating the kernels needs ../../src/conv-c2d and conv-mark (the IMAX compiler), which are outside the repo. At runtime the code maps the accelerator through /sys/class/uio and /dev/mem, so it needs the unreleased VPK180 IMAX image. Without that hardware it cannot reproduce any paper number; only the CPU path (GGML_USE_CPU) runs.

## Archive migration reading record (2026-10-09)

Historical metadata says `not_started`, but the retained dated sections record original-text or code checks. This note preserves only those documented checks; complete paper reading is not established.

- Historical source: `not specified in metadata; see dated checks above`.
- Full source/provenance snapshot: [citation.bib](citation.bib).

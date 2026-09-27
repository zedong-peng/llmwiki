---
title: "FlexLLM: Composable HLS Library for Flexible Hybrid LLM Accelerator Design"
domain: research
area: fpga-llm-inference
type: paper
status: seed
updated: 2026-09-15
tags: [paper, fpga, llm-inference]
---

# FlexLLM: Composable HLS Library for Flexible Hybrid LLM Accelerator Design

> Bibliographic record and local public asset cache. Full paper notes are pending.

## Paper Meta

- Authors: Jiahao Zhang, Zifan He, Nicholas Fraser, Michaela Blott, Yizhou Sun, Jason Cong
- Year: 2026
- Venue: arXiv preprint
- BibTeX key: `flexllm_hls`
- Related Work category: FPGA Transformer and LLM systems
- Public record: [arXiv](https://arxiv.org/abs/2601.15710)

## Local Assets

- Paper PDF: [2601.15710.pdf](2601.15710.pdf) (10 pages; SHA-256 `68a8c0f9f483718cdf2ea63657253814536302c8648f77491d75446ba0af92c1`)

## Ingest Status

- Metadata: verified against the manuscript bibliography.
- Paper PDF: `downloaded`.
- Reading note: seed; no unverified method or performance claims added.
- Source archive and code repository: not requested in this import pass.

Return to [[research/fpga-llm-inference/papers/index|FPGA LLM paper library]].

## Model input and coverage audit (2026-09-15)

**Classification: Reusable library; model-specific implementation.** Llama-3.2-1B variants, plus HMT extension.

The selected U280 configuration fixes 16 layers, hidden=2048, KV hidden=512 and vocabulary=128256. The host uses per-layer prepared .bin weights; GGUF is vocab_only. The library supports composable operators and the paper implements HMT, so the method should not be called intrinsically single-model. The delivered generation path remains specialized to the Llama-3.2-1B family; cross-family checkpoint deployment is not demonstrated.

Inspected code (pinned copies, not executed):

- [README.md](source/code-audit/README.md) — [upstream commit](https://github.com/Crazy-James26/FlexLLM/blob/8fb9bab4f0ffabad1970b81ce34e857e70822ff0/README.md).
- [Modules/config.h](source/code-audit/Modules/config.h) — [upstream commit](https://github.com/Crazy-James26/FlexLLM/blob/8fb9bab4f0ffabad1970b81ce34e857e70822ff0/Modules/config.h).
- [SpinQuant_Llama_32_1B/config_u280_mem_opt.h](source/code-audit/SpinQuant_Llama_32_1B/config_u280_mem_opt.h) — [upstream commit](https://github.com/Crazy-James26/FlexLLM/blob/8fb9bab4f0ffabad1970b81ce34e857e70822ff0/SpinQuant_Llama_32_1B/config_u280_mem_opt.h).
- [SpinQuant_Llama_32_1B/SpinQuant_Prefilling_Decoding_mem_opt_demo.cpp](source/code-audit/SpinQuant_Llama_32_1B/SpinQuant_Prefilling_Decoding_mem_opt_demo.cpp) — [upstream commit](https://github.com/Crazy-James26/FlexLLM/blob/8fb9bab4f0ffabad1970b81ce34e857e70822ff0/SpinQuant_Llama_32_1B/SpinQuant_Prefilling_Decoding_mem_opt_demo.cpp).

[Audit receipt](source/model-coverage-audit.json). See [[research/fpga-llm-inference/index#Model input and coverage audit (2026-09-15)|cross-paper comparison]] for definitions and input formats. This dated section supersedes older coverage/placement summaries where they conflict.

## Original-text verification (2026-09-27)

Checked against the original paper text or public code for the llama.cpp FPGA backend paper; supersedes earlier summaries where they differ.

- arXiv-only (2601.15710) but public code with 32 GitHub stars on 2026-09-27 (Crazy-James26/FlexLLM).
- U280 decode architecture 292 MHz, 6.94 s per 1k decode tokens (about 144 token/s) for Llama-3.2-1B W4A4 with INT4 lm_head (source/extracted/fccm26.tex:896,1050).
- Public demo: separate prefill and decode xclbins; per-layer prepared .bin weights; GGUF used only for the llama.cpp tokenizer; the host copies the prefill KV cache into the decode bitstream's buffers (code-audit SpinQuant_Prefilling_Decoding_mem_opt_demo.cpp:15, 32, 740-745, 900-921); decode loop and sampling run on device (lines 932-947).

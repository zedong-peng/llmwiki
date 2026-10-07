---
title: "FlightLLM: Efficient Large Language Model Inference with a Complete Mapping Flow on FPGAs"
domain: research
area: fpga-llm-inference
type: paper
status: active
updated: 2026-09-15
tags: [paper, fpga, llm-inference]
---

# FlightLLM: Efficient Large Language Model Inference with a Complete Mapping Flow on FPGAs

FlightLLM presents a complete compiler-to-board mapping flow for generative LLMs on FPGA. The
paper is useful here as a system-level reference, not as a directly matched llama.cpp baseline.

## Paper Meta

- Authors: Shulin Zeng, Jun Liu, Guohao Dai, Xinhao Yang, Tianyu Fu, Hongyi Wang, Wenheng Ma, Hanbo Sun, Shiyao Li, Zixiao Huang, Yadong Dai, Jintao Li, Zehao Wang, Ruoyu Zhang, Kairui Wen, Xuefei Ning, Yu Wang
- Year: 2024
- Venue: Proceedings of the 2024 ACM/SIGDA International Symposium on Field Programmable Gate Arrays
- BibTeX key: `flightllm`
- Related Work category: FPGA Transformer and LLM systems
- Public record: [DOI](https://doi.org/10.1145/3626202.3637562); [arXiv](https://arxiv.org/abs/2401.03868)

## Local Assets

- Paper PDF: [2401.03868.pdf](paper-pdf/2401.03868.pdf) (12 pages; SHA-256 `e0d38c8754516973d62749c846ebe63ea3984b569a1613b98340ef13249fd4da`)
- arXiv source archive: [2401.03868-source.tar.gz](source/archives/2401.03868-source.tar.gz); extracted TeX: [memory-hier.tex](paper-tex/extracted/legacy/content/memory-hier.tex), [evaluation.tex](paper-tex/extracted/legacy/content/evaluation.tex)

## Read Notes

- Physical evaluation uses U280 for OPT-6.7B and LLaMA2-7B at batch 1; the paper reports a 225 MHz implementation and end-to-end latency, decode throughput and energy.
- The memory section explicitly places large single-access objects, including weights and KV cache, in HBM, while small lookup tables use DDR. Decode activations are fused and kept on chip to reduce repeated off-chip accesses.
- This is persistent KV support at the model-system level; absence of a llama.cpp-style cache-position/append ABI does not remove that credit. Its generality is a compiler/mapping flow with model-specific instructions and prepared weights, not a native framework backend. Whether the exact released xclbin is reusable across additional models requires artifact validation; model-specific compilation alone does not imply mandatory bitstream regeneration.
- Source-first paper read completed. The public artifact has now been partially inspected; this does not establish independent reproduction or a matched result for the current backend.

## Artifact Audit (2026-09-08)

- Official [Zenodo record 10462167](https://zenodo.org/records/10462167): the top-level [README](supplementary/zenodo-10462167/README.md) explicitly withholds RTL as Infinigence-AI IP.
- Fully cached/extracted [profile.zip](supplementary/zenodo-10462167/profile.zip). Its README and `run.py` show that VHK158 timings come from an instruction simulator/profiler and CSV aggregation; only the GPU branch calls Transformers/vLLM generation. VHK158 is also explicitly simulation in the paper, unlike U280.
- The 6.41 GB hardware ZIP was not fully downloaded. HTTP range reads retained its [complete manifest](supplementary/zenodo-10462167/hardware-zip-manifest.json), [internal README](supplementary/zenodo-10462167/hardware-selected/fpga_implementation/README.md), host binary and two case configurations. The README invokes a precompiled case and compares binary outputs with goldens; this is not a documented prompt-to-text interface.
- No board run, complete package reproduction, or RTL-source reproduction was performed. See [[research/fpga-llm-inference/index|area index §Evidence Matrix]] for table marks, missing members and the distinction between paper generation claims and the public demo.

## Model-File Deployment Boundary

The 2026-09-08 manuscript revision replaced Multi-model evaluation with Model-file deployment
(now named New-model entry in [[research/fpga-llm-inference/index|the area index]]): a new supported
LLM checkpoint should enter through files/configuration without writing per-model exporters,
graph descriptions, compiler, hardware or host code. Automatic builds remain allowed.
FlightLLM's [mapping flow](paper-tex/extracted/legacy/content/software.tex) explicitly describes automatic
PyTorch structure parsing and IR/instruction generation, so Auto map retains its check.
The [artifact README](supplementary/zenodo-10462167/README.md), however, supplies precompiled
cases and refers generation of different cases to the authors' Infinigence-AI environment.
The reviewed package therefore does not establish a user-accessible new-checkpoint entry.
Its two named hardware demo directories denote decode lengths, not proof of a two-model
architectural limit. Preserve the paper's OPT/LLaMA2 evaluation while marking the new
model-file deployment predicate as unestablished. The local backend plan targets any GGUF
within the declared framework, operator/format and device-capacity envelope; this is a future
requirement, not current support for arbitrary GGUFs.

Return to [[research/fpga-llm-inference/threads/paper-library/index|FPGA LLM paper library]].

## Model input and coverage audit (2026-09-15)

**Classification: Cross-architecture (paper).** OPT-6.7B and LLaMA2-7B.

content/software.tex describes automatic structure parsing and ISA generation with manually defined templates; content/evaluation.tex names both families and their U280 results. The public hardware artifact consists of prepared cases, while the source frontend/RTL is not available in that package. Thus paper-level cross-architecture coverage is supported; arbitrary checkpoint acceptance is not established by public code.

Classification uses the paper text and available public artifact; unavailable source is not treated as evidence of model restriction.

[Audit receipt](model-coverage-audit.json). See [[research/fpga-llm-inference/index#Model input and coverage audit (2026-09-15)|cross-paper comparison]] for definitions and input formats. This dated section supersedes older coverage/placement summaries where they conflict.

## Original-text verification (2026-09-27)

Checked against the original paper text or public code for the llama.cpp FPGA backend paper; supersedes earlier summaries where they differ.

- Model input in the paper is a PyTorch LLM converted to ISA through an IR with automated structure parsing (content/software.tex:52-53); 'prepared cases' describes only the public artifact, not the method.
- Each model is sparsified, quantized and fine-tuned before compilation (content/evaluation.tex:20, 63-68).
- Weights and KV cache in HBM; lookup tables in DDR (content/memory-hier.tex:56). 225 MHz (content/evaluation.tex:42); 65.9% HBM utilization (table/BW-utilization.tex).
- The paper gives no absolute U280 token/s (only normalized figures; VHK158 92.5 token/s is simulated). AccLLM Table VII lists FlightLLM U280 at 55 token/s, 45 W; TeLLMe's related work quotes 153 token/s without a traceable source.

## Correction (2026-09-28)

- The previous bullet is wrong about U280: the paper's own Figure 1 (content/introduction.tex:11-18, Figures/Introduction/overview.pdf) states U280 ~55 token/s at ~45 W vs V100 ~45 token/s. The figure does not name the model or prompt/decode lengths; the Zenodo README says the U280 demo "can verify Figure 1 in the paper (55 token/s)". Cite FlightLLM Fig. 1 directly, AccLLM Table VII only as corroboration.
- Reproducibility: the Zenodo hardware package (6.41 GB, not downloaded) ships stc-v1.xclbin, a closed host binary fpgaHost and two prepared cases (decode_token_128_ae, decode_token_512_ae; ~3.4 GB of HBM params each, model not named). The README's sample output only compares outputs against golden files; it shows no timing. RTL and the compiler are not released, so new models or lengths require Infinigence-AI. The profile package reproduces only the simulated VHK158 numbers (pre-generated CSVs).
- The local fpga-epcc U280 boards run shell xilinx_u280_gen3x16_xdma_base_1 with XRT 2.14 (2022.2); the artifact targets xilinx_u280_gen3x16_xdma_1_202211_1 with XRT 2.15 (2023.1). Same platform family, not tested.

## On-board measurement on our U280 (2026-09-28)

- Ran the Zenodo hardware package (fpga_implementation.zip, md5 78cbfb72abe678f6df94b344a571ef87) on fpga-epcc card 0000:5e:00.1 (shell xilinx_u280_gen3x16_xdma_base_1, XRT 2.14.354). The package targets XRT 2.15. `~/flightllm-artifact/shim/force_bdf.so` (LD_PRELOAD) adds the one missing XRT 2.15 symbol, xrt::bo(device, size, group), and redirects fpgaHost's hardcoded device 0 to FLIGHTLLM_BDF. Card 86 was already in a "critical temperature or power event, requires pci hot reset" state and was not used.
- Each case is ONE decode step at the named KV length. fpgaHost times start to done with steady_clock after weights, instructions and inputs are in HBM, and cross-checks the time with a cycle counter at register 0x28 (225 MHz).
- Results, all 25 outputs matching golden in every run:
  - decode_token_128_ae: 17.500 / 17.507 / 17.506 ms per token = 57.1 token/s (3,937,100-3,938,548 cycles).
  - decode_token_512_ae: 18.990 / 18.990 / 18.990 ms per token = 52.7 token/s (4,272,163-4,272,339 cycles).
  - This matches paper Fig. 1 (~55 token/s).
- Model: not named in the package. The instruction streams contain the 32-bit constant 11008 about 1800 times per SLR (LLaMA-7B FFN width); 16384 and 50272 (OPT-6.7B) never appear, hidden 4096 is ubiquitous, and weights total 3.43 GB (~4.1 bit/param). Hence LLaMA2-7B, the paper's only LLaMA model (inferred).
- Logs: fpga-epcc `~/flightllm-artifact/runs/*-5e-*/run.log`.

## Can the public code run another model? (2026-09-28)

No, not without substantial new work.
- The U280 package runs only its two prepared LLaMA2-7B cases: an instruction binary, packed weights, input and golden files, each a single decode step. fpgaHost only loads files, starts the kernel and compares against golden; it has no model entry, tokenizer or generation loop.
- profile.zip does include an IR to instruction generator (inst_gen/, ISA encoder with dump_inst_bin_file). But:
  - nothing calls the binary dump;
  - its config is the 4-SLR VHK158 (the U280 cases have 3 SLR instruction streams);
  - the only inputs are pre-generated LLaMA2 IR YAMLs, whose 2,442 tensor addresses are all 0 (no memory allocation);
  - there is no PyTorch to IR frontend, no weight quantizer, sparsifier or packer for the param/*.rtl.bin layout, and no input or golden generator;
  - the IR op set is attention/linear_mv/mm, layernorm (RMS flag), silu, softmax, eltwise and concat.
- The paper also requires sparsifying, quantizing and fine-tuning each model before compilation. The README says new cases are generated "in the environment at Infinigence-AI".

## What one FlightLLM "run" covers (2026-09-28)

- The profile IR (llama2_decode_token_128.yaml) is one step. Its input layer takes an already-embedded int8 hidden state [1,1,4096] plus RoPE sin/cos caches. It then runs 32 decoder layers, the final norm and lm_head (225 linear_mv), and ends at int8 logits [1,1,32000]. Embedding lookup, sampling and the token loop are not in the IR.
- Instruction programs are compiled per context-length bucket: decode every 16 tokens, prefill every 128 (run.py align_token_length). The U280 cases 128 and 512 carry different instruction streams.
- The profile tool's "end-to-end" time is composed, not a run: one prefill-bucket time plus the sum of single-step decode times over the aligned lengths (run.py:76-100).
- The paper never states how the token loop, embedding and sampling run on U280, or how U280 end-to-end latency was obtained. The public artifact shows only single steps: logits on device, lm_head on FPGA, KV in HBM.

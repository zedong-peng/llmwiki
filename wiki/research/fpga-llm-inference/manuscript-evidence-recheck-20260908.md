---
title: Manuscript Experimental Evidence and Deployment Recheck
domain: research
area: fpga-llm-inference
type: comparison
status: active
updated: 2026-09-08
tags: [fpga, llm-inference, evidence, deployment, related-work]
---

# Manuscript Experimental Evidence and Deployment Recheck

## Scope and Method

User request: recheck the works cited in the manuscript against llmwiki and update the paper.
The cited-key inventory contains 64 distinct references. The inventory checks paper metadata,
available full-text paths and existing source/artifact records. Detailed rechecking covers DFX,
FlightLLM, Spatial LLM, EdgeLLM, StreamTensor, CODO, FlexLLM, LUT-LLM, TeLLMe and SECDA-LLM,
focusing on original experiment sections and relevant public execution/build paths.
This is not a new full read of every cited paper, an exhaustive novelty search, or board
reproduction. Broader thematic citations retain only their stated architectural role.

Primary evidence takes precedence over a later paper's comparison table. Publication status,
experimental detail, public code, and demonstrated deployment are separate properties.
The scoop-check comparison method distinguishes integration overlap from an equivalent
implemented system; no numerical novelty score is assigned to the full backend.

## Rechecked Systems

| Work | Primary passages / implementation | Finding and manuscript treatment |
|---|---|---|
| DFX | [Implementation and Evaluation](papers/dfx-2022/source/extracted/6_evaluation.tex), model configuration, accuracy and performance methodology | Author-reported 1/2/4-U280 evaluation with length sweeps; accuracy check is on 345M; 1.5B head count is modified. Retain system credit without implying multi-family portability or public implementation. |
| FlightLLM | [Evaluation](papers/flightllm-2024/source/extracted/content/evaluation.tex); [artifact README](papers/flightllm-2024/supplementary/zenodo-10462167/README.md) | Physical U280 versus simulated VHK158; public profiler/binary cases and withheld RTL do not constitute an editable complete release. |
| Spatial LLM | [Experiments](papers/spatial-llm-2024/source/extracted/sections/6-experiments.tex), setup, GPT2 accelerator and scalability | Actual BERT/GPT-2 U280 designs; GPT-2 W8A8 versus BERT W4A8; larger generative families and multi-FPGA scaling projected. Do not copy W4A8 for GPT-2 from later comparison tables. |
| EdgeLLM | [PDF](papers/edgellm-2025/2407.21325.pdf), compilation/deployment and experimental results | VCU128 GLM/Qwen measurements, LAN client/server, sparsity and quality evaluation. Custom runtime is not evidence of a GGML backend; source release not established. |
| StreamTensor | [Main TeX](papers/streamtensor-2025/source/extracted/main.tex), Experiments, GPT-2, Emerging LLMs | Explicit on-board U55C measurements; modified Hugging Face graphs and block reuse. This supports compiler/model-phase results; complete generation controller remains unverified. |
| CODO | [GPT-2 evaluation](papers/codo-2026/source/extracted/main.tex); [decode host](papers/codo-2026/repo/codo-artifact/experiments/fig-9/gpt_decoding/host.cpp) | Substantive synthesis/board/compiler results. Host profiles one event, omits output readback and prints success without a comparison. Separate random-input verification block is not a checkpoint-driven generator. |
| FlexLLM | [Main TeX](papers/flexllm-hls-2026/source/extracted/fccm26.tex), final quantization ablation and Evaluation; [README](papers/flexllm-hls-2026/repo/FlexLLM/README.md) | Correct final configuration to W4A4KV8, with quantized LM head. PPL 12.68 versus BF16 8.94. U280 measured, V80 projected. Documented `make demo-run` is an application entry point; dependencies and prepared weights remain required. |
| LUT-LLM | [Main TeX](papers/lut-llm-2026/source/extracted/bare_conf.tex), evaluation/implementation; [calculator](papers/lut-llm-2026/repo/LUT-LLM/qwen_block/e2e_latency.cpp) | Qwen3-1.7B quality and V80 hardware evidence exist. AE uses `(prefill_cycles*28 + decode_cycles*28*output_len)/250e6`; this does not time token generation. Do not infer that every paper result has exactly that provenance. |
| TeLLMe | [Main TeX](papers/tellme-v2-2026/source/extracted/main.tex), Experimental Results and Analysis; [README](papers/tellme-v2-2026/repo/TeLLMe_FPGA_2026/README.md) | KV260 E2E timing uses PYNQ; breakdown uses RTL simulation; approximately 9 ms ARM LM-head included. Chatbot has external data and a required CPU build. |
| SECDA-LLM | [Case study](papers/secda-llm-2024/source/extracted/04_evaluation.tex), lines 87-97; [README](papers/secda-llm-2024/repo/SECDA-LLM/README.md); [backend](papers/secda-llm-2024/repo/SECDA-LLM/srcs/ggml_backend/ggml-secda/ggml-secda.cpp) | Paper reports 1.7 s/token and about 11x over Cortex-A9 NEON. Workload/phase/quality/power details are limited. Later WiP code has selective MatMul admission and host buffers; not built or run in this audit. Retain as preliminary integration precedent, not mature equivalent or principal performance baseline. |

## Bibliographic Correction

The [official ISCA 2026 program](https://www.iscaconf.org/isca2026/program/) lists CODO with
matching title/authors. Its [arXiv record](https://arxiv.org/abs/2604.12618) also states
acceptance. Corrected manuscript bibliography and wiki venue to ISCA 2026; no publisher
DOI or page numbers were guessed. The archived arXiv text remains the reviewed version.
FlexLLM's [arXiv record](https://arxiv.org/abs/2601.15710) does not establish a conference
venue; no venue was inferred from its TeX filename. SECDA's reviewed record remains the
[2024 preprint](https://arxiv.org/abs/2408.00462).

Secondary-source discrepancy: TeLLMe's comparison table labels SECDA as Cortex-A53/W4-A16,
whereas SECDA's original case study identifies Cortex-A9 and Q3_K/Q8_K MatMul.
The revised manuscript follows SECDA's original experiment.

## Availability Limits

The inventory found no local paper PDF in the corresponding metadata paths for BAQET,
ChatOPU, CSTrans-OPU, dLLM-OPU, FET-OPU, integer-only full fusion, InTRRA, LORA, METAL,
MoE-OPU, QLlama, scalable GPT-2, TeraFly, TFLOP and Transformer-OPU. These are thematic
references with existing bibliographic records, not newly verified deployment baselines.
FINN/FINN-R and Vitis AI use the separate toolchain note. Artifact and vendor citations use
their existing source records. Missing text is not evidence of missing capability.
TENET's locally available PDF explicitly distinguishes FPGA and ASIC implementations;
its ASIC headline speedup must not become an FPGA result.

## Implications for the Local Backend

Current Q4 implementation: one whole graph per call, HBM-resident weights/KV, GPT-2 Medium,
one sequence, contexts up to 1024, prepared image/model package and FPGA-specific hooks.
The [frozen receipt](/home/zdpeng/llama.cpp-fpga/build-fpga-q4/evidence-20260907-32x32-r3/README.md)
still records false board-correctness and full-qualification gates. Native integration is
shared with SECDA-LLM. Whole-model execution and persistent KV also have prior art.

A defensible comparison asks whether this particular framework execution/state boundary
reduces launches, transfers and latency under matched correctness. Deployment convenience
requires independent installation and model-porting evidence. The revised survey states
these as evaluation requirements, not as demonstrated advantages.

Old wiki descriptions of per-node launches, a future coarse region and unique framework
integration were corrected or marked historical in the area index and landscape.

## Follow-Up: Multi-Model and Public Availability

Rechecked live official endpoints on 2026-09-08 after the user challenged the
shortlist. Public documentation, implementation source, board binaries and complete
generation remain distinct; anonymous 404 cannot distinguish a private, removed or
renamed repository.

- **FlightLLM:** the [official GitHub tree](https://github.com/FlightLLM/flightllm_test_demo/tree/4a9625149e19c3baccad0786ae0d90bab2410890)
  is accessible and includes profiling Python, an xclbin, a compiled host and
  `token_64_single_layer` binary cases. Re-fetched the [Zenodo README](https://zenodo.org/records/10462167/files/README.md?download=1):
  RTL is explicitly withheld as Infinigence-AI IP; additional cases can require author
  assistance. This confirms partial public delivery, not full open source. Original
  paper evaluation remains OPT-6.7B/LLaMA2-7B on U280 versus VHK158 simulation.
- **Spatial LLM:** original experiments measure BERT and GPT-2 on U280; larger
  generative families are analytical. BERT qualifies only under a broad Transformer
  definition, not as a second generative checkpoint. The [Allo examples](https://github.com/cornell-zhang/allo/blob/main/examples/README.md)
  explicitly link Spatial LLM and also link the distinct PLDI Allo artifact. The latter
  has [GPT-layer HLS and a host](https://github.com/cornell-zhang/allo-pldi24-artifact/tree/f7e3fa200049ff9bf3cc730d68b1a162c1a63f31/llm),
  not just isolated arithmetic examples. Read its complete README and `llm/host.cpp`:
  one invocation and 24 repeated layer invocations are timed; the host does not load
  prompt tokens, sample output tokens, or feed selected tokens back. It prints success
  without a numerical comparison. Do not present it as a complete generation release
  or as the exact artifact of the separate Spatial LLM paper. No build was attempted.
- **StreamTensor:** [author projects](https://hanchenye.com/projects/) identify a
  public [documentation site](https://hanchenye.com/streamtensor/) with compiler,
  synthesizer and runtime API documentation. Its actual GitHub href is
  `https://github.com/hanchenye/streamtensor`; anonymous GitHub web lookup and
  `https://api.github.com/repos/hanchenye/streamtensor` return 404. Direct Python web
  access also timed out on a separate attempt. No accessible official implementation
  was verified. Do not equate the visible GitHub button with released source, and do
  not describe the work as having no public documentation. Original U55C GPT-2,
  Qwen, Llama and Gemma phase measurements support multi-model evaluation. Exact
  Llama checkpoint identity needs care: the cited model and configuration table are
  not obviously consistent; the shortlist does not rely on that precise identity.
- **DFX / EdgeLLM:** repeated title/author/FPGA repository searches did not identify
  an official implementation. AMD Dynamic Function eXchange repositories and mobile
  applications named EdgeLLM are unrelated. Keep implementation availability NR,
  not a categorical assertion of non-release; their original multi-model measurements
  are not withdrawn.

Under a broad multi-Transformer plus partial-public-artifact criterion, FlightLLM
and Spatial LLM are the practical shortlist among these nine works. Under the
manuscript's stricter multiple-generative-checkpoints criterion, Spatial LLM still
has only partial evidence. Requiring full implementation source also excludes
FlightLLM's withheld RTL. State the criterion instead of claiming that exactly two
systems satisfy every interpretation of "multi-model and public."

## Manuscript Changes

- Added per-claim evidence methodology; the initially added experimental-support/delivery
  table was subsequently removed at the user's request. Its per-work summaries are now
  integrated into Table 1 as an experimental/delivery-scope column. Separate P+D,
  Auto mapping, Framework backend and Persistent KV columns were removed; supporting
  architectural discussion remains in the text.
- Expanded SECDA's actual data, missing evaluation details and later-code limitations.
- Clarified CODO event timing, LUT-LLM extrapolation, FlexLLM/TeLLMe application entry points,
  DFX model changes, numerical formats, and measured versus simulated results.
- Added workflow-specific usability discussion and kept local qualification limits explicit.
- Corrected CODO's venue and the paper README's stale description of the survey scope.

## Validation

The initial `make -C paper` succeeded and produced a 13-page PDF. Its final LaTeX log had no warnings,
undefined references/citations, or overfull/underfull boxes. The new comparison table on
page 5 was rendered and visually inspected. The table has ten prior-work rows; this note's
local evidence links resolve, and the updated CODO YAML parses. `git diff --check` passes
for the three edited paper files. This describes the initial build before table removal;
the follow-up validation is recorded in the maintenance log. These are document checks,
not performance reproduction.

See [[research/fpga-llm-inference/feature-level-evidence-matrix]] and
[[research/fpga-llm-inference/backend-niche-and-baseline-audit]].

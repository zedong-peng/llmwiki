---
title: Feature-Level Evidence Matrix for FPGA LLM Systems
domain: research
area: fpga-llm-inference
type: comparison
status: active
updated: 2026-09-08
tags: [fpga, llm-inference, related-work, artifact, runtime, kv-cache]
---

# Feature-Level Evidence Matrix for FPGA LLM Systems

## Adopted Header

The manuscript feature table now uses:

`Work | Model source / interface | New-model entry | Auto map | Native backend | E2E gen. | Resident exec. | Public source | Scope / qualification`

The 2026-09-08 update replaces Multi-model evaluation with Model-file deployment at the
user's request. The new predicate asks whether a new supported LLM enters an unchanged
deployment flow through model files and ordinary configuration, without writing per-model
exporters, graph descriptions, compiler, hardware or host code. Automatic packing,
compilation and model-specific bitstreams are allowed. Model count alone does not qualify.

The 2026-09-09 update renames Model-file deployment to New-model entry at the user's
request: the predicate tests whether a third party can deploy one more supported
checkpoint without author-side case generation. It also adds Resident exec. as a sixth
filter: weights and KV state persist on-device for the request lifetime and
intermediates do not round-trip to the host per operator (e.g. resident HBM windows
with on-chip activation reuse and a single graph launch). Per-operator offload with
host-side staging does not qualify, even with end-to-end generation. SECDA-LLM's
per-op MatMul offload through a host-side context handler therefore takes NR on this
column while keeping its GGUF-entry credit; the local GPT-2 profile's HBM-resident
weights/KV and single launch take Y with the explicit failed-qualification footnote.
DFX, FlightLLM and EdgeLLM also take Y on Resident exec. at the paper-report level:
DFX serves whole generations from HBM-resident tiled weights/KV within a single
service launch, FlightLLM decodes over HBM-resident weights/KV with always-on-chip
activations, and EdgeLLM keeps weights/KV in HBM behind host-written configuration.
Residency alone is therefore recorded as prior art; the planned contribution is its
combination with a framework-native backend and third-party new-model entry.

For this new column, the current manuscript credits SECDA's inspected GGUF-to-GGML MatMul
offload path within its supported types/dimensions. The local fixed GPT-2 profile remains
unestablished, and the planned GGUF flow carries a design-requirement check. The remaining
systems have no established model-file entry under this predicate; their graph compilers,
parameterized hardware, model evaluations and prepared artifacts retain their separate
credits. These are evidence classifications, not upper bounds on architectural support.
All feature definitions are placed below the manuscript table; the earlier audit matrix
below retains its historical Multi-model/Public artifact predicates.

`Native backend` is acceptable if defined as native integration into an existing general-purpose
inference framework, not merely a custom host runtime. `Framework backend` makes this distinction
more explicit and need not privilege llama.cpp over other frameworks.

`Public artifact` is preferable to an unqualified `Reproducible artifact`. Public source, a runnable
binary demo, source-to-bitstream reproducibility, and independent reproduction of complete generation
are different facts. A compact artifact cell can say `Src`, `Bin`, `Src+Bin`, or `NR`, with scope in
footnotes. If the original heading is retained, name the result being reproduced and the evidence
standard in the caption; a repository URL alone is insufficient.

## Column Predicates

| Column | Positive evidence | Does not suffice |
|---|---|---|
| New-model entry | One more supported checkpoint deploys via files/configuration with no per-model code and no author-side case generation; packing/bitstreams allowed | Several evaluated models; a closed collection of prepared cases; a vocabulary-only GGUF |
| Auto map | Compiler/runtime maps an accepted model or graph to instructions, dispatched operations, or hardware | Manually composing model-specific hardware; this predicate alone does not establish a new-model entry |
| Native backend | Existing inference framework's backend interface executes the accelerated path | Borrowing a tokenizer or importing PyTorch alone |
| E2E generation | Actual checkpoint and prompt input, complete model including LM head and prior-context use, token selection fed back into successive decode steps, and observable generated tokens | One layer/graph event; synthetic tensors; separate phase timings combined analytically |
| Resident exec. | Weights and KV persist on-device for the request lifetime; intermediates do not round-trip to the host per operator | Per-operator offload with host-side staging, even with end-to-end generation |
| Public source | Implementation source for the accelerated path | Only binaries, profiling tools, or a promised release |
| Scope / qualification | Model/platform, operator and state coverage, execution/timing boundaries and inspected release scope | Treating projections as board measurements or code availability as reproduced generation |

E2E generation and Persistent KV are related but not identical: a working generator can recompute
its prefix instead of caching. P+D describes phase coverage; E2E describes their composition with
the model and generation controller. A native backend can exist without demonstrating either.
Persistent KV need not expose llama.cpp-specific names, paging, or reset APIs to qualify; those are
additional runtime capabilities. Device residency should be described separately if claimed.

Likewise, E2E functionality does not mean all work runs on FPGA or all work is inside the timer.
Tokenization/sampling may remain on the CPU. Report whether a latency includes them, initial model
loading, PCIe transfers, and host orchestration separately. `llama-bench pp/tg` alone is not proof of
a text-generation loop, and neither is a one-output-token smoke test proof of multi-step KV reuse.

For a boolean table, use `Y` for established support, `P` for explicitly identified partial support,
and `NR` for not established in reviewed evidence. `NR` is not `No`. Attach source notes to each
nontrivial cell and distinguish paper reports from inspected code. For `Multi-model`, DFX's several
GPT-2 sizes qualify under a checkpoint definition; use `Multi-family` if distinct architectures are
what the comparison intends. Recompilation is a separate axis, not an implicit exclusion.

## Earlier Audit Marks

An earlier 2026-09-08 selection kept nine evaluated prior systems plus one explicitly local
backend row. SECDA-LLM is retained as an integration precedent in prose, not a principal performance
baseline in that snapshot. The current table includes SECDA and separate current/plan rows as
described above. Phase-specific and access-limited works remain in the evidence notes below. Y can be supported by an explicit paper report
or inspected official implementation; it never means independent reproduction. SECDA-LLM's paper,
all included TeX sections and bibliography were read for its formal note; its code review remains
targeted. The earlier five newly downloaded papers remain targeted feature audits, not completed
full-paper/bibliography ingests. No FPGA was programmed and no performance result was reproduced.

| Work | E2E generation | Multi-model | Public artifact | Experimental and delivery scope |
|---|---|---|---|---|
| DFX | Y | Y | NR | GPT-2 345M/774M/1.5B on 1/2/4 U280s; public implementation unverified. |
| FlightLLM | Y | Y | Prof+Bin | OPT-6.7B/LLaMA2-7B on U280; binary cases, RTL withheld; VHK158 simulated. |
| Spatial LLM | P | P | Src | BERT/GPT-2 U280 phase measurements; other generative families projected; Allo kernel/layer code, not a verified generation release. |
| EdgeLLM | Y | Y | NR | GLM-6B/Qwen-7B on VCU128; custom compiler/LAN service; public implementation unverified. |
| StreamTensor | P | Y | NR | GPT-2/Qwen/Llama/Gemma U55C phase measurements; public docs, linked code unavailable; generation loop unverified. |
| CODO | P | NR | Src | GPT-2 phase/compiler U280 results; inspected host times one graph event without checking output. |
| FlexLLM | Y | NR | Src+Bin | Llama-3.2-1B U280 measurements; HLS, images and prompt/output demo; external parameters; V80 projected. |
| LUT-LLM | P | NR | Src+Bin | Qwen3-1.7B quality and V80 implementation; AE derives latency from block cycles, not timed generation. |
| TeLLMe | Y | NR | Src+Bin | BitNet-0.73B KV260 timings/chatbot; CPU LM-head included; external data and CPU build required. |
| Ours (local) | Y | NR | NR | GPT-2 Medium Q4, 32-output trace; whole graph and HBM KV; board correctness and full qualification false. |

`Src` is implementation source, not paper TeX. `Prof+Bin` means profiling source plus a board
binary package with withheld RTL. None of these marks promises that all weights, dependencies,
licenses, board images, and correctness receipts are locally available. The local row's footnote
states that generation was observed but board correctness and full qualification are false. Its
public artifact is NR: an anonymous lookup of the configured origin returned 404, not evidence of
a public release. Local availability alone does not justify Src.

Selection rationale: the user's admission rule requires substantive evaluation data, a meaningful
public reproduction path, or a verified leading-conference publication. All nine retained prior
systems have evaluation data; seven publication records were checked through DOI metadata. Repository
presence is not independent reproduction. See the complete
[baseline and niche audit](backend-niche-and-baseline-audit.md). SECDA's 1.7 s/token report and later
backend code justify citing the integration precedent, but its limited original evaluation does
not make it a principal performance baseline. Its source-derived host-KV/backend capabilities remain
credited in the note rather than being silently reclassified as absent.
Hummingbird+ is removed because its full text remains unavailable, not because it lacks capabilities.
The distinct original Hummingbird stays in the embedded-memory discussion. FAST-Prefill belongs in
prefill discussion; PD-Swap's distinguishing contribution is phase reconfiguration, poorly represented
by these comparison fields, and stays in the reconfiguration discussion. Their exclusion is not a
negative capability judgment. LUT-LLM and Spatial LLM remain useful examples of algorithm/hardware
co-design and programmable compilation with different evidence boundaries. The table is representative,
not exhaustive, and rows are not selected by their number of Y marks.

## Row Evidence

- **DFX:** [architecture](papers/dfx-2022/source/extracted/4_architecture.tex) includes the LM-head MM;
  [microarchitecture](papers/dfx-2022/source/extracted/5_microarchitecture.tex) describes per-token
  Key/Value HBM DMA and DDR output tokens; [evaluation](papers/dfx-2022/source/extracted/6_evaluation.tex)
  reports GPT-2 345M/774M/1.5B text-generation workloads with up to 256 outputs. Different sizes qualify
  for Multi-model, not Multi-family. No current official implementation was verified in this pass;
  NR is not a claim that DFX has no code.
- **FlightLLM:** [evaluation](papers/flightllm-2024/source/extracted/content/evaluation.tex) reports
  OPT-6.7B and LLaMA2-7B on U280; VHK158 is cycle-accurate simulation. Its
  [software](papers/flightllm-2024/source/extracted/content/software.tex) and
  [memory hierarchy](papers/flightllm-2024/source/extracted/content/memory-hier.tex) establish adaptive
  instructions and HBM KV. Generation Y retains the paper's model-level claims; the public package
  does not independently establish a prompt-to-text board loop. See the package audit below.
- **Spatial LLM:** [board evaluation](papers/spatial-llm-2024/source/extracted/sections/6-experiments.tex)
  measures GPT-2 phase performance; BERT is not another generative checkpoint. LLaMA/Vicuna are analytical
  extensions (Multi-model P). [KV modeling](papers/spatial-llm-2024/source/extracted/sections/3.2-modeling-constraints.tex)
  and [accelerator design](papers/spatial-llm-2024/source/extracted/sections/5.2-accelerator.tex) describe
  prefill/decode double buffers. [Allo examples](papers/spatial-llm-2024/repo/allo/examples/README.md)
  explicitly link this paper and provide kernel generation, not a verified release of its complete
  generation controller. E2E P is a phase-evidence boundary, not a claim that no generator existed.
  The separately published [Allo PLDI artifact](https://github.com/cornell-zhang/allo-pldi24-artifact/tree/f7e3fa200049ff9bf3cc730d68b1a162c1a63f31/llm)
  includes GPT-layer HLS and a host, but the host's repeated layer timing is not token feedback.
  Do not describe all associated public material as only isolated arithmetic kernels, or attribute
  this distinct artifact as an exact release of the Spatial LLM paper.
- **EdgeLLM:** [PDF](papers/edgellm-2025/2407.21325.pdf), Sections V-VI, describes a LAN service with
  client token encoding/decoding, whole-model CPU-FPGA compilation, dynamic token instructions,
  KV memory allocation and HBM write DMA, and GLM/Qwen board results. The runtime is custom, not an
  existing framework backend. TeX unavailable, used PDF fallback: both source and e-print requests
  returned PDF. No official implementation repository was verified.
- **StreamTensor:** [main TeX](papers/streamtensor-2025/source/extracted/main.tex) describes Torch-MLIR
  graph compilation, block reuse across layer weights, GPT-2/Qwen/Llama/Gemma phase evaluations, and
  dynamic tensors including KV. This supports P+D/Multi-model/mapping; the complete token-feedback
  controller and KV append/read path remain unverified (E2E/KV P). A lack of llama.cpp-specific reset
  APIs is not evidence of no KV. Its [official documentation](https://hanchenye.com/streamtensor/)
  is public. The linked `hanchenye/streamtensor` repository returned anonymous GitHub/API 404
  on 2026-09-08; accessible implementation source remains unverified, rather than asserting no release exists.
- **CODO:** see the pinned artifact audit below. E2E P credits phase/graph execution, not a demonstrated
  generator; K/V computed within the inspected block is not persistent history (KV NR). Other CNN and
  Transformer workloads do not establish two evaluated generative checkpoints (Multi-model NR).
- **FlexLLM:** [main TeX](papers/flexllm-hls-2026/source/extracted/fccm26.tex) describes composed TAPA
  HLS modules, hybrid phase-specific designs, W4A4KV8 Llama-3.2-1B and HMT. The final
  quantization ablation also quantizes the LM head (WikiText-2 PPL 12.68 versus BF16 8.94).
  U280 results are measured;
  V80 results are projected. [README](papers/flexllm-hls-2026/repo/FlexLLM/README.md) and
  [generation demo](papers/flexllm-hls-2026/repo/FlexLLM/SpinQuant_Llama_32_1B_Ins/SpinQuant_Prefilling_Decoding_mem_opt_demo.cpp)
  load vocabulary from GGUF, tokenize a prompt, run prefill, copy all layers' KV into decode layout,
  run decode and detokenize sampled IDs. The
  [decode kernel](papers/flexllm-hls-2026/repo/FlexLLM/SpinQuant_Llama_32_1B_Ins/SpinQuant_Decoding_mem_opt_logits.h)
  loops over output positions and feeds sampled embeddings back, with K/V managers. This is actual
  generation code, but vocabulary-only llama.cpp reuse is not a GGML FPGA backend. Manual module
  composition limits Auto mapping to P; one base model with HMT/quantization variants is not proof
  of two evaluated checkpoints. Included xclbins were cached, not executed.
- **Hummingbird+:** [metadata](papers/hummingbird-plus-2026/metadata.yaml) records the ACM DOI.
  A direct full-text request returned HTTP 403. No capabilities were inferred from the title or
  inherited from the distinct Hummingbird paper. Removed from the main table pending full text.
  Original [Hummingbird source](papers/hummingbird-2025/source/extracted/) is now durably archived
  after targeted review: LLaMA3-8B, DDR optimizations, embedding offloading and GQA dataflow,
  reporting 4.8 token/s on KV260 and 8.6 on ZCU104. Its complete paper/bibliography ingest is pending.
- **LUT-LLM:** [main source directory](papers/lut-llm-2026/source/extracted/) describes Qwen3-1.7B,
  activation/weight co-quantization, centroid search and hybrid temporal/spatial execution. The section
  "Other Design Features" explicitly streams prefill KV to HBM, prefetches prior KV during decode,
  and appends the new token (P+D/KV Y). The [AE README](papers/lut-llm-2026/repo/LUT-LLM/README.md)
  uses prefill/decode C-sim and RTL-sim blocks, then
  [e2e_latency.cpp](papers/lut-llm-2026/repo/LUT-LLM/qwen_block/e2e_latency.cpp) computes
  `(prefill_cycles*28 + decode_cycles*28*output_len)/250e6`. That is a latency derivation, not a
  token-generation timer (E2E P). The release includes HLS, a V80 `.pdi` and timing report. Modeling
  scripts/physical implementation tools alone do not establish automatic model mapping (NR).
  The README's latency-table note says batch/sequence, but calculator inputs are input/output lengths;
  retain this discrepancy when auditing the numbers.
- **TeLLMe:** [source directory](papers/tellme-v2-2026/source/extracted/) reports BitNet-0.73B on KV260
  using W1.58A8, 250 MHz, and an approximately 9 ms ARM NEON LM head included in E2E results.
  [chatbot.py](papers/tellme-v2-2026/repo/TeLLMe_FPGA_2026/on_board_test/src/chatbot.py) implements
  `prefill` (line 943), `decode_step` (1137), and `generate` (1215), with token selection, embeddings,
  K/V buffers and cache-length increments across successive decode calls. The
  [README](papers/tellme-v2-2026/repo/TeLLMe_FPGA_2026/README.md) provides interactive and golden-check
  commands and separately links required large weights/cache data on Google Drive. Source and a `.bit`
  are cached; that external data was not downloaded. This is a standalone PYNQ application, not a
  native inference-framework backend. No second model or automatic graph mapper was established.
- **SECDA-LLM (integration-precedent prose):** [formal note](papers/secda-llm-2024/index.md) and
  [evaluation TeX](papers/secda-llm-2024/source/extracted/04_evaluation.tex) describe TinyLlama-1.1B
  generation on PYNQ-Z1 with Q3_K/Q8_K MatMul offload (paper-reported E2E Y, 1.7 s/token, about 11x
  over ARM NEON). Separate phase evaluation is not provided (P+D P); configurations are not proof
  of multiple executed FPGA checkpoints (Multi-model NR). Driver/SystemC design is manual, and
  operator dispatch is not automatic model mapping (NR). The current
  [backend](papers/secda-llm-2024/repo/SECDA-LLM/srcs/ggml_backend/ggml-secda/ggml-secda.cpp) registers
  GGML execution, restricts admission to selected quantized MatMul types/shapes, and uses host buffers.
  The pinned framework's [KV implementation](papers/secda-llm-2024/repo/llama.cpp/src/llama-kv-cache.cpp)
  retains historical tensors and appends via `ggml_set_rows`, which SECDA does not offload.
  Hence current-source Framework/KV Y means a genuine backend and host-managed state, not full-model
  FPGA execution or device-resident KV. [Update notes](papers/secda-llm-2024/repo/SECDA-LLM/docs/lpp_updates.md)
  explicitly describe a later API port; this snapshot is not the 2024 paper freeze. No local build or
  generation run was performed. Src is public implementation, not a complete reproduced release.
- **Ours (local):** the retained GPT-2 Medium Q4 profile has native prefill/decode and 32 generated
  outputs, device-resident KV and real GGML execution (Y with the explicit failed-correctness footnote).
  Current context checks admit one sequence and contexts up to 1024; older Gemma traces do not establish
  multi-model capability of this release (NR). Template-specific packing/preparation is P mapping,
  not a general model compiler. The exact local profile's public availability remains unverified (NR).
  See the [niche audit](backend-niche-and-baseline-audit.md) for source paths and practical limitations.
- **PD-Swap (prose comparison):** [main TeX](papers/pd-swap-2025/source/extracted/main.tex), runtime workflow, decoding
  attention, automated implementation flow and Sections IV-A/B: a BitNet-0.73B KV260 system swaps
  attention logic after prefill while retaining KV in DDR. The paper reports autoregressive throughput
  and TTFT; these support E2E/P+D/KV at the paper-report level, not source-code verification.
  DSE outputs instantiate HLS templates and iterate implementation to timing closure (Auto mapping Y).
  No official repository was identified from the reviewed paper links.
- **FAST-Prefill (prose comparison):** [main TeX](papers/fast-prefill-2026/source/extracted/main_paper.tex), architecture
  and evaluation: CPU tokenization/embedding, FPGA chunks across layers through the first token,
  liveness-driven dual-tier KV caching, and a hybrid DSP/LUT MPU. Llama-3.2-1B/3B are identified FPGA
  evaluations, sufficient for Multi-model Y. The source also names Qwen2.5-1B; that exact checkpoint
  label needs clarification and is not needed for the mark. E2E/P+D/KV P means first-token and
  within-prefill reuse, not successive decode. No official FPGA code link was identified; GPU
  FlexPrefill is not the FAST-Prefill artifact. RULER accuracy falls substantially relative to BF16,
  e.g. Llama-1B averages 61.68 (BF16), 33.44 (INT8), 33.07 (FAST-Prefill); feature marks are not
  numerical-equivalence claims.

## Archived Material

The selection update adds [SECDA-LLM](papers/secda-llm-2024/index.md), with PDF, complete TeX source,
main repository `183376a652b47a30b5b57cd34965b45e9297f39a`, and separately archived exact gitlink
versions of llama.cpp (`b8b0a4c46ab43f1f777a4a0250908997c539bf11`) and secda_tools
(`0b842d76df03546830037023f1281bd98aba4e5f`). The root tree and per-archive download receipts retain
provenance. Two parent-project symlinks are omitted from the llama.cpp extraction and listed in its
receipt; these audit copies are not a configured build. secda_tools is archived but unread.
Original Hummingbird's TeX archive is also retained with a targeted-reading receipt.

The five newly extracted sources are FlexLLM (`2601.15710`), TeLLMe (`2510.15926`), PD-Swap
(`2512.11550`), LUT-LLM (`2511.06174`) and FAST-Prefill (`2602.20515`). Each paper directory retains
`source/download-audit.json` with URL, archive path and SHA-256. Prior cached DFX, FlightLLM,
Spatial LLM, StreamTensor and CODO sources were reused. PDFs already present were not re-downloaded.
The [consolidated receipts](feature-level-audit-receipts.json) record verified local sizes and SHA-256
values for the downloaded bundles and selected FlightLLM files; `profile.zip` also matched Zenodo's
official checksum. The pinned implementation archives and extracted trees are:

| Official repository | Full commit | Local receipt |
|---|---|---|
| Crazy-James26/FlexLLM | `8fb9bab4f0ffabad1970b81ce34e857e70822ff0` | [receipt](papers/flexllm-hls-2026/repo/FlexLLM-download.json) |
| UCI-CORSA/TeLLMe_FPGA_2026 | `139ad882aba8485048e08993022872128bc00f51` | [receipt](papers/tellme-v2-2026/repo/TeLLMe_FPGA_2026-download.json) |
| LUT-FPGA/LUT-LLM | `9ee2259d312f9b1119a398d8ff7703154260a417` | [receipt](papers/lut-llm-2026/repo/LUT-LLM-download.json) |
| cornell-zhang/allo | `8bafb0dcee27c96a72872184d2b106c59c8a1414` | [receipt](papers/spatial-llm-2024/repo/allo-download.json) |

Repository snapshots were extracted without executing build scripts. Allo's internal `_mlir`
symlink was preserved after validating its target stays within the extraction root. Dependencies,
external model data and toolchain licenses were not fetched. Current repository revisions can be
newer than the papers and are identified as such, not asserted to be the original experimental freeze.

## CODO Recheck

Official repository: <https://github.com/sjtu-zhao-lab/codo-artifact>, current main SHA independently
checked through GitHub API: `130b12bc63e6e6daa31a1227b7e8391c5039148d`.
A clean committed snapshot was cloned from the existing local Git cache into
[papers/codo-2026/repo/codo-artifact/](papers/codo-2026/repo/codo-artifact/), with the official origin
URL restored. Direct remote clone timed out. Dependency submodules were not initialized.

- [GPT2.py](papers/codo-2026/repo/codo-artifact/experiments/verify/pymodels/transformers/GPT2.py): one Pre-LN attention/MLP block, `forward(x)` returns its hidden-state tensor. No checkpoint loader, LM head, or past-KV input/output is present in this model.
- [data.py](papers/codo-2026/repo/codo-artifact/experiments/verify/data.py): seeded FP32 random input `[1,32,1024]`, 16 heads. The verification frontend generates raw binary input/output oracles; this is not the paper's W4A8 real-model generation workload.
- [decode host.cpp](papers/codo-2026/repo/codo-artifact/experiments/fig-9/gpt_decoding/host.cpp): host buffers and HBM binding, one migration and one `enqueueTask` at line 446, then event profiling at lines 452-453. The earlier host-to-device migration is outside that event interval. Output migration is commented out, and `TEST PASSED` is unconditional after execution without an output comparison.
- All four Fig. 9 host files have this single-event timing pattern. [run_all.sh](papers/codo-2026/repo/codo-artifact/experiments/run_all.sh) drives synthesis experiments, not a GPT generation application. This committed snapshot has no `.xclbin` or `host.exe`; Docker contents were not inspected here.

The user's report that an author described measuring one inference latency is consistent with this
public path, but the wording alone is ambiguous between a graph, token, and complete request.
Treat the conversation as user-reported private clarification, not a public citation. The inspected
code establishes the narrower artifact boundary; it does not establish the derivation of every
paper number, invalidate those numbers, or prove that the compiler cannot support state in principle.

## FlightLLM Discovery

The paper's introduction links <https://zenodo.org/doi/10.5281/zenodo.10422477>.
The API request resolves to version record `10462167`. Retained official material:

- [record.json](papers/flightllm-2024/supplementary/zenodo-10462167/record.json).
- [README.md](papers/flightllm-2024/supplementary/zenodo-10462167/README.md), read completely.

The README distinguishes a VHK158 software/simulation performance profile from U280 board testing.
It explicitly states that RTL is Infinigence-AI IP and is not released, while providing a pre-generated
U280 bitstream, precompiled cases and a host file. Generating different cases may require author
assistance. The catalog lists `profile.zip` (2,788,671 bytes) and `fpga_implementation.zip`
(6,409,565,790 bytes). The follow-up downloaded and extracted the complete
[profile.zip](papers/flightllm-2024/supplementary/zenodo-10462167/profile.zip).
Its [README](papers/flightllm-2024/supplementary/zenodo-10462167/profile/profile/README.md) and
[run.py](papers/flightllm-2024/supplementary/zenodo-10462167/profile/profile/run.py) were read:
FPGA timing reads/generated instruction-profile CSVs, aligns decode lengths to multiples of 16,
and sums phase times. Only the GPU branch calls `model.generate`/`llm.generate`; those imports
are not evidence of an FPGA framework backend.

Because `/home` had less than 3.1 GB free at the start, full hardware download was attempted in
`/var/tmp`, then stopped due to transfer time and local archive capacity. A partial file remains at
`/var/tmp/llmwiki-artifacts-zdpeng/flightllm-10462167/fpga_implementation.zip.part`, not counted as an
archived package. HTTP range reads via RemoteZip succeeded in archiving the
[complete ZIP manifest](papers/flightllm-2024/supplementary/zenodo-10462167/hardware-zip-manifest.json)
and selected members, with ZIP CRC checking:
[internal README](papers/flightllm-2024/supplementary/zenodo-10462167/hardware-selected/fpga_implementation/README.md),
`host/fpgaHost`, and the two cases' `info.yaml`. The manifest lists `stc-v1.xclbin` (84,179,297
uncompressed bytes) and precompiled `decode_token_128_ae`/`decode_token_512_ae` inputs, instructions,
weights and golden outputs. The internal README runs `fpgaHost <xclbin> <case>` and compares output
binaries against golden files. It is not a documented prompt-to-text generation command. The host
binary was not executed or reverse engineered. Large case tensors and the xclbin were not downloaded.
The package remains partially inspected, not independently reproduced or an open RTL mapping flow.

## Candidate Positioning

The candidate direction is **framework-native stateful generation with an auditable execution
path**, not "other FPGA papers are impractical" or "we invented persistent KV". SECDA-LLM already
provides direct llama.cpp/GGML integration, including a registered backend in the current source.
Native integration itself is not a unique advantage; coverage, state placement and verified execution
must be compared against this precedent.
For a paper claim, validate real checkpoint loading, several consecutive generated tokens, KV
continuation at several context depths, reset/reuse correctness, logits against a CPU oracle, and
host/FPGA responsibilities. Quantify latency, throughput, overhead and model portability separately.
A second model should use the same backend contract, with any profile or bitstream regeneration
reported explicitly. Native integration alone is an engineering property, not proof of novelty,
performance superiority, or production readiness.

Suggested comparison wording:

> Model-scale or phase-level acceleration does not by itself establish stateful autoregressive
> generation within an existing inference framework. The inspected CODO artifact exposes
> fixed-shape graph execution, whereas a framework-native backend must additionally preserve
> cross-token state and compose with the framework's model execution and token-selection path.

At the user's request, `paper/main.tex` now includes a separately marked local backend row.
The abstract states this limited positioning role, and no local speedup is presented as a
correctness-qualified result. The supporting local evidence is:

- [Retained GPT-2 evidence README](/home/zdpeng/llama.cpp-fpga/build-fpga-q4/evidence-20260907-32x32-r3/README.md)
  records native prefill/decode and a 32-output greedy generation path (CPU sampling, EOS disabled).
  Model SHA-256: `a58d0ee38091237c05766ea34f24529e10191760e380f602d1f488427d479f74`;
  xclbin: `893b810a31a146fd89a05ef2192d78bb5c7e4e0c6cdf0650714afdbc9684f4f0`.
- Despite the README's opening `Qualification: qualified`, its explicit gates say
  `Board correctness passed: False`, `Experimental delivery completed: False`, and
  `Fully qualified: False`. Do not cite these timings as a fully correctness-qualified delivery.
  Source identity includes a commit plus retained dirty patches; a clean current HEAD alone would
  not identify that build. No new board validation was performed here.
- Native GGML/framework integration is shared with SECDA-LLM, and generation and persistent
  KV alone are not unique: DFX, FlightLLM, EdgeLLM, FlexLLM, TeLLMe and PD-Swap have positive evidence
  at their stated boundaries. A release-level artifact and a second model still need separate gates.

## Validation

The subsequent [[research/fpga-llm-inference/manuscript-evidence-recheck-20260908]]
corrects FlexLLM's numerical format from the original ablation and confirms CODO's ISCA 2026
venue from the official conference program. A follow-up removes the extra experimental table
and the P+D column at the user's request, and records live StreamTensor/FlightLLM/Allo checks.
Validation below describes the earlier 11-page build, not the revised PDF.

- `make -C /home/zdpeng/Towards-a-General-FPGA-Backbone-for-LLM-Inference/paper` succeeded;
  `paper/build/main.pdf` has 11 pages. Final LaTeX log has no warnings, undefined citations or
  overfull boxes. The rendered table on page 3 was visually checked.
- Fourteen metadata YAML files pass duplicate-key and audit-path checks; local matrix evidence
  links, wiki backlinks and the new SECDA note's local links resolve. All ten manuscript rows match
  the matrix after normalizing the local-profile footnote marker.
- Fifteen source/repository receipts pass file-existence, size and available SHA-256 checks.
  All 59 entries in the library checksum list pass; manifest totals match 84 records and 51 paper PDFs.
  FlightLLM's complete profile archive matched its official catalog checksum. These are archive and
  document checks, not FPGA execution, model correctness or independent performance reproduction.

## Related Notes

- [[research/fpga-llm-inference/backend-niche-and-baseline-audit]]
- [[research/fpga-llm-inference/papers/secda-llm-2024/index]]
- [[research/fpga-llm-inference/codo-2026]]
- [[research/fpga-llm-inference/kv-cache-runtime-boundary-comparison]]
- [[research/fpga-llm-inference/papers/codo-2026/index]]
- [[research/fpga-llm-inference/papers/flightllm-2024/index]]
- [[research/fpga-llm-inference/papers/streamtensor-2025/index]]
- [[research/fpga-llm-inference/end-to-end-evaluation]]

Return to [[research/fpga-llm-inference/index]].

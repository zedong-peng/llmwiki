---
title: "CODO: An Automated Compiler for Comprehensive Dataflow Optimization"
domain: research
area: fpga-llm-inference
type: paper
status: active
updated: 2026-09-08
tags: [paper, codo, isca-2026, fpga, compiler, dataflow, gpt-2, end-to-end]
---

# CODO: An Automated Compiler for Comprehensive Dataflow Optimization

CODO is an automated MLIR/dataflow compiler for fixed-shape FPGA graphs. Its GPT-2 result is an
important compiler reference, but its public artifact must be kept separate from a stateful
llama.cpp generation baseline. (Earlier deep read merged from `codo-2026.md` on 2026-07-23;
raw IdeaSpark runs live under `threads/ideaspark_run/`.)

## Paper Meta

- Authors: Weichuang Zhang, Yiquan Wang, Xinzhou Zhang, Chi Zhang, Yu Feng, Xiaofeng Hou, Chao Li, Jieru Zhao, Minyi Guo.
- Year: 2026
- Venue: ISCA 2026, verified against the [official conference program](https://www.iscaconf.org/isca2026/program/) on 2026-09-08. The archived full text is the arXiv version; venue verification is separate from artifact reproduction. (Official artifact README also lists it as Best Paper Award Finalist.)
- BibTeX key: `codo`
- Related Work category: FPGA Transformer and LLM systems
- Code/artifact: [sjtu-zhao-lab/codo-artifact](https://github.com/sjtu-zhao-lab/codo-artifact); archived snapshot: [Zenodo 10.5281/zenodo.19425920](https://doi.org/10.5281/zenodo.19425920).
- Artifact revisions inspected: main commit `130b12bc63e6e6daa31a1227b7e8391c5039148d` (2026-06-03) and tag `isca2026-ae` at `8b85e41cfff6fc6a297f919f73dd14ed3fd728cb`; their `experiments/fig-9/` trees are identical.
- Why it matters here: it reports GPT-2 Medium board-level TTFT, decode speed and generation latency, and its artifact exposes a full PyTorch/Torch-MLIR -> MLIR -> Vitis HLS -> host/xclbin workflow.

## Local Assets

- Paper PDF: [2604.12618.pdf](2604.12618.pdf) (17 pages; SHA-256 `b31c6872fc51bf5f779fc501952b78fbfa6d6233a71464c1e07e5b0ac8ec5b2e`)
- arXiv source archive: [2604.12618-source.tar.gz](source/archives/2604.12618-source.tar.gz); extracted TeX: [main.tex](source/extracted/main.tex)

## Read Notes

- The paper reports GPT-2 Medium on U280 at W4A8/300 MHz, including TTFT, decode speed and total latency. These figures are useful for understanding fixed graph/dataflow performance, but are not inserted into the current CPU/FPGA throughput table.
- The public `GPT2.py` forward computes current-input Q/K/V but has no `past_key_values` input/output. The Fig. 9 host statically binds HBM buffers and invokes one `main_graph` event; no token loop, cache position, append pointer or cross-launch state object is exposed.
- Therefore “CODO has no K/V” is inaccurate, while “the public artifact does not demonstrate persistent KV-cache management or KV-specific optimization” is supported. This note records the user's report of a private author clarification about fixed-graph timing; this is separate from the paper's published methodology.
- Source-first read completed. Earlier standalone deep-read note folded into this record on 2026-09-09.

## What the Paper Says About Timing (2026-09-08)

Rechecked the archived 17-page arXiv v1 PDF against its TeX, including the implementation,
experiment setup, GPT-2 evaluation, execution breakdown and complete artifact appendix.
The page numbers below refer to this local PDF; a separate proceedings version was not reviewed.

| Location | Explicit statement | Remaining boundary |
|---|---|---|
| Section VII-C, p. 10 | CODO emits host and HLS kernel code; a generated testbench compares accelerator output against the input program's golden output. | No GPT token-feedback controller is described. |
| Section VIII setup, p. 10 | Synthesis reports supply latency/resource statistics; board evaluation supplies runtime/power statistics. | No GPT request timer or per-token aggregation method is specified. |
| Section VIII-C and Fig. 9, p. 12; Table VI, p. 13 | GPT-2 Medium, varying input/output lengths, TTFT for prefill and speed for decode. Table VI identifies its results as an on-board comparison. | No explanation of a 32-output generation loop, layer-repeat accounting, LM head, or total-latency derivation is given. |
| Artifact appendix, pp. 14-15 | AE focuses on synthesis experiments; board experiments were excluded from AE because bitstream generation requires over two weeks and a configured U280. The appendix states that GPT host/kernel source, reports and prebuilt xclbins are provided, with a host execution command. | This limits AE reproduction; it does not retract the paper's own board-evaluation claim or document the token loop. |

Neither the published text nor its figure/table captions state that GPT latency was obtained
by multiplying one graph/block event by the layer count or output length. The arithmetic
reconstruction below is our inference, not an author-described measurement procedure.
Conversely, the paper does not document enough generation orchestration to resolve the public
host's relationship to Table VI. Preserve the reported board results and mark the implementation
and timing boundary as unspecified pending clarification.

CODO remains direct related work for automated FPGA compilation and GPT evaluation. The user's
statement that it is work from their group provides a practical route to clarification, not a
reason to strengthen or weaken its evidence classification. A concrete author clarification
would identify whether Table VI latency comes from timing a checkpoint/prompt generation loop
or combining phase/layer timings, and account for the model layers, LM head, token selection,
KV updates, host transfers and first-token convention. No author was contacted in this audit.

## E2E Generation Interpretation (2026-09-08)

The manuscript's E2E-generation dash means that a checkpoint-driven token-selection and
feedback loop is **not established within the reviewed scope**. It must not be paraphrased
as "CODO has no E2E." Three evidence boundaries apply:

- The [paper](source/extracted/main.tex) describes an end-to-end compiler from an input algorithm to accelerator and host code. Table VI also reports GPT-2 Medium TTFT, decode speed and total latency; for `[32:32]`, these are 20.40 ms, 231.48 token/s and 158.64 ms. Preserve these as paper-reported results.
- The inspected [verification model](repo/codo-artifact/experiments/verify/pymodels/transformers/GPT2.py) is one Transformer block returning hidden states, without an LM head. The [decode host](repo/codo-artifact/experiments/fig-9/gpt_decoding/host.cpp) times one kernel event, comments out output readback, and exposes no token-selection/feedback loop. This supports an artifact-level qualification: complete autoregressive generation remains unverified.
- A single launch could contain a generation loop inside the kernel; launch count alone cannot decide E2E. Likewise, generation can recompute its prefix without a KV cache, and CPU token selection or a standalone runtime can qualify. Missing public orchestration is not proof that no private implementation exists; apply the same paper-report versus artifact-verification standard across comparison rows.

Suggested scope text: "Reports GPT-2 TTFT, decode speed and latency; complete token-feedback
generation is unverified in the inspected artifact."

### What the Released GPT Kernel Actually Executes

Tracing the generated [decode kernel](repo/codo-artifact/experiments/fig-9/gpt_decoding/gpt-1_32x32.cpp)
establishes more than a missing host loop. Line numbers below refer to that pinned file.

| Code location | Computation | Architectural consequence |
|---|---|---|
| `main_graph`, lines 2699-2712 and 2824-3106 | One set of four `1024x1024` attention projections and two `1024x4096` / `4096x1024` FFN projections, with residual/normalization operators. | This is one Transformer block, with no 24-layer weight-switch or layer-repeat controller. Numbered `main_graph_node*` functions are operator nodes, not model layers. |
| `main_graph_node28`, line 1572; callers at 2880-2891 | Q and K both have shape `[1][1][1024]`; QK scores have shape `[1][16][1][1]`. The head-feature reduction covers 64 components; both token-position loop bounds are 1. | Each head attends to only the current position. There is no traversal of the prompt's historical K vectors, including through streaming tiles. |
| `main_graph_node19`, line 1149 | Attention probabilities `[1][16][1][1]` multiply V from the same current-position `[1][1][1024]` tensor. | Historical values are not incorporated either. A cached decode step following a 32-token prompt would require a history axis exceeding 1. |
| `load_array`, line 2614; final graph call at 3106 | The external `vv853` pointer is read into local `v853` during loading; the last node writes only local `v853`. | No model result is stored back to the host-visible output pointer for another layer or token. |

The [host](repo/codo-artifact/experiments/fig-9/gpt_decoding/host.cpp) then profiles one event
without output readback or token selection. Thus this released GPT path is a fixed-shape block
benchmark, not a functioning generator. Simply wrapping it in a host token loop would still
omit historical attention, model-layer orchestration, output propagation and the LM head.
This conclusion concerns the inspected implementation; it does not imply that CODO's compiler
could never compile a larger program providing those operations.

### Phase Names Versus Computation Coverage

CODO's paper reports both prefill and decode, so the comparison issue is not an entirely
absent named phase. A complete forward includes embedding, all 24 Transformer layers, final
normalization and the LM head; prompt-conditioned decode must also incorporate historical
K/V at every layer. The inspected CODO graph covers a block within those phases, without
the complete model composition or historical decode attention. Token selection and feedback
are a further generation-loop requirement, separate from these missing forward computations.
For a decode evaluation processing the first continuation after a 32-token prompt, each head
needs a `1 x 33` attention score vector; the inspected kernel computes only `1 x 1`.

Phase-organized literature comparisons are valid when labeled with the reported scope.
If sampling were the only difference, that would not preclude comparison with llama-bench,
which also excludes logits-based sampling. A matched phase speedup additionally requires
matching model coverage, context and timing boundaries. Multiplying a block time by the
layer count would not restore omitted historical attention, embedding or the LM head.
Whether Table VI includes additional unpublished execution or accounting remains unspecified;
the inspected kernel alone does not prove the timing scope of every paper-reported value.

### Why `[32:32]` Requires Token Feedback

Table VI explicitly labels this pair `[Input Len: Output Len]`: 32 prompt tokens and 32
continuation tokens. In ordinary autoregressive generation, prefill supplies the logits for
the first output, then 31 successive decode forwards supply outputs 2 through 32. A forward
over 32 known input positions can compute 32 hidden states in parallel, but these are not 32
new continuation tokens. The public [prefill kernel](repo/codo-artifact/experiments/fig-9/gpt-32-prefill/gpt-32_16x16.cpp)
has hidden tensors `[1][32][1024]`; the [decode kernel](repo/codo-artifact/experiments/fig-9/gpt_decoding/gpt-1_32x32.cpp)
has `[1][1][1024]` and ends after the block's graph nodes without a token-selection loop.

The single-block structure makes model-layer and output-token scaling the natural reconstruction
of the reported model metrics. GPT-2 Medium's [checkpoint configuration](https://huggingface.co/openai-community/gpt2-medium/blob/main/config.json)
specifies 24 layers, 16 heads and hidden size 1024. Under the hypothesis that each layer is charged
the same block latency, the published `[32:32]` values imply:

```text
block prefill(32) = 20.40 / 24 = 0.85000 ms
block decode(1)  = 1000 / (231.48 * 24) = 0.18000115 ms
model token time = 24 * block decode(1) = 4.32003 ms
request latency  = 24 * (block prefill(32) + 32 * block decode(1))
                 = 158.64088 ms, rounding to the reported 158.64 ms
```

The 0.85/0.18 ms values are reverse-derived, not recovered board measurements. The identical
231.48 token/s across context lengths is consistent with the fixed `S=1` graph, but constant
throughput alone would not prove missing history in another implementation. Here the attention
dimensions and loop bounds establish the missing history directly.

The existing [decode HLS report](repo/codo-artifact/experiments/fig-9/gpt_decoding/report/main_graph_csynth.rpt)
instead estimates 43.090 us for one block, which would yield about 966.97 token/s after multiplying
by 24. It cannot be presented as the raw source of the published 231.48 token/s. No board trace
or aggregation script connecting the inspected host to the published table was identified.
The best-supported architectural reconstruction is block/phase timing followed by model/token
accounting, while the exact raw timings and experimental source revision remain unverified.

If TTFT includes the first generated token, the usual total for 32 outputs contains 31 decode
intervals; the table's counting convention needs clarification. The `[128:128]` row matches
the analogous reconstruction with an implied 4.60 ms block prefill. `[64:64]` implies 1.36 ms
block prefill but differs from the 64-interval total by about one decode interval, as recorded
in [GPT-2 End-To-End Table](#gpt-2-end-to-end-table) below.

## Placement in the Backend Blog

The backend blog's Section 9.1 now retains all three Table VI rows in a separate literature
reference table. Its local results are separated into llama-bench throughput, a breakdown of
the same pg32,32 measurement, and actual greedy generation from llama-fpga-acceptance. At the
user's request, all reported performance uses the preselected sample 0 for each backend and
workload; cross-run means and standard deviations have been removed. CODO's reported values
do not directly populate those tables because the reviewed execution and timing scope does
not match. llama-bench tests still execute the model and prescribed KV behavior; lack of
sampling alone would not prevent a valid phase comparison.

The former Standalone/Native labels did not identify different runtimes. The
[measurement script](/home/zdpeng/llama.cpp-fpga/scripts/measure-fpga-q4.py:386) runs llama-bench
once per backend, collecting both standard output and phase JSON. The blog now calculates
throughput from `samples_ns[0]` and takes the matching pg32,32 `sample=0` phase record from the
[retained evidence](/home/zdpeng/llama.cpp-fpga/build-fpga-q4/evidence-20260907-32x32-r3/README.md).
FPGA pp32/tg32/pg32,32 rates are 171.7/98.8/122.1 token/s, with CPU rates 75.2/28.8/41.1.
The tg32 test starts with empty KV; pg32,32 decode starts after a 32-token prompt and reports
94.3 token/s for FPGA. The original command retains `-r 5` as provenance, while the blog
reports only sample 0. ITL and per-evaluation phase times average intervals within that
single sample. llama-bench supplies random input tokens without logits-based sampling;
greedy generation feeds each selected output token into the next evaluation.

For `[32:32]`, `32 / 0.02040 = 1568.6 token/s` and `64 / 0.15864 = 403.4 token/s` are derived
rates under the paper's timing labels, not measured llama-bench pp/pg results or matched speedups.
The blog preserves the paper's TTFT/decode/latency labels, W4A8 precision and U280/300 MHz setup.

## Public Artifact Recheck (2026-09-08)

- Official repository: [sjtu-zhao-lab/codo-artifact](https://github.com/sjtu-zhao-lab/codo-artifact). Local cache: [README.md](repo/codo-artifact/README.md), commit `130b12bc63e6e6daa31a1227b7e8391c5039148d`. Reused the committed objects from `/home/zdpeng/codo` after direct GitHub cloning timed out; GitHub's API independently confirmed the same current main SHA. The cache does not include that working tree's uncommitted changes or initialized dependency submodules.
- Re-read the complete main TeX, bibliography, artifact README, verification entry/data/config/helpers, GPT2 model, decode host, and synthesis runner. `gen_mlir_designs.py` instantiates the single block with random initialized parameters; `data.py` supplies seeded FP32 random input `[1,32,1024]`, hidden size 1024 and 16 heads. `utils.py` exports raw input/output `.bin` tensors as a functional oracle, not a text-generation workload. This verification example must be distinguished from the paper's W4A8 on-board figures.
- All four Fig. 9 host files expose one `enqueueTask` and event-start/end profiling. In the fully inspected decode host, output migration is commented out and `TEST PASSED` is printed without a result comparison. This is not a board-level model-correctness receipt.
- `experiments/run_all.sh` runs synthesis experiments for Fig. 11 and Tables II-IV, not the GPT generation loop. No `.xclbin` or `host.exe` appears in this committed repository snapshot. Dependencies, Docker contents and board execution were not reproduced here.
- Thus **public artifact available** is supported; **independently reproduced stateful generation** is not established by this inspection. Do not erase CODO's compiler-artifact credit when narrowing its generation boundary. The user's report of a private author conversation is corroborating context, not a public citation or proof of how every published number was derived.
- Feature-table definitions and cross-paper artifact discovery: [[research/fpga-llm-inference/index|area index §Evidence Matrix]].

## Problem

Large HLS dataflow designs fail to become one efficient pipeline for two reasons:

1. **Coarse-grained dataflow violation:** producer and consumer regions cannot be streamed as one connected graph, leaving discontinuous regions and external-memory materialization.
2. **Fine-grained dataflow violation:** access order, iteration structure or layout differs across connected tasks; tools fall back to ping-pong buffers or deadlock-prone implementations.

Even after legality is restored, performance still depends on communication and balanced parallelism. CODO therefore treats legality, data movement and resource allocation as one compiler problem.

## Compiler Flow

```text
PyTorch model / high-level program
  -> Torch-MLIR / Polygeist
  -> CODO MLIR dialect
  -> coarse-grained violation elimination
  -> fine-grained violation elimination
  -> on-chip/off-chip communication optimization
  -> latency/resource-guided DSE and scheduling
  -> Vitis HLS C++
  -> generated host + link configuration
  -> xclbin / board execution
```

The current GitHub artifact's `experiments/verify/` GPT-2 example defines a single Pre-LN Transformer block with hidden size 1024, 16 heads and FFN width 4096. The verification frontend lowers this block from PyTorch. The paper labels the board evaluation as GPT-2 Medium (24 layers), but the public Fig. 9 host invokes `main_graph` once and contains no visible layer-repeat loop or per-layer weight-switch loop. The exact mechanism that lifts the single-block artifact to the model-level Table VI result is therefore not traceable from the inspected public host source.

The Zenodo snapshot contains a separate, unreferenced full-model prototype: root-level `gpt2.py` exports Hugging Face `GPT2Model` for a seven-token prompt, and `gpt_test.cpp`/`gpt_test2.cpp` encode a 12-layer, hidden-768 GPT-2 Base graph with an externally visible final hidden state. It is not GPT-2 Medium, does not include the LM head or autoregressive generation loop, and has no associated GPT HLS/P&R report, xclbin or board log in the archive. It demonstrates a broader lowering experiment but does not close the Table VI orchestration gap.

## Main Techniques

### Dataflow violation elimination

CODO transforms incompatible producer/consumer regions into legal streaming structures instead of conservatively materializing every boundary in memory. This is the main conceptual step beyond merely adding `DATAFLOW` pragmas.

### Communication optimization

The compiler aims to:

- keep intermediate tensors in FIFO/on-chip buffers;
- improve off-chip burst and data-layout behavior;
- reduce redundant memory movement;
- coordinate generated HLS kernel, host binding and FPGA link configuration.

### Automated scheduling and DSE

CODO estimates loop latency and DSP use, forms Pareto candidates and redistributes parallelism to balance pipeline stages. The goal is not maximum parallelism per operator; it is minimizing the slowest stage under global resource constraints.

## GPT-2 End-To-End Table

The paper's Table VI reports on-board GPT-2 Medium generation. CODO uses U280, 8 GB HBM, 300 MHz and W4A8.

| `[input length: output length]` | Latency (ms) | TTFT (ms) | Decode speed (token/s) |
|---:|---:|---:|---:|
| `[32:32]` | 158.64 | 20.40 | 231.48 |
| `[64:64]` | 313.44 | 32.64 | 231.48 |
| `[128:128]` | 663.36 | 110.40 | 231.48 |

The `[32:32]` and `[128:128]` rows are consistent with:

\[
T_{generation}=TTFT+\frac{N_{output}}{R_{decode}}.
\]

For example:

\[
20.40\text{ ms}+\frac{32}{231.48}\text{ s}=158.64\text{ ms}.
\]

The published `[64:64]` row is not consistent with this formula:

\[
32.64\text{ ms}+\frac{64}{231.48}\text{ s}=309.12\text{ ms},
\]

while Table VI reports `313.44 ms`. The 4.32 ms difference is approximately one decode interval (`1/231.48 s`). This may be a table typo or a token-count convention applied only to that row; preserve the published value but do not derive a comparison from it until the authors clarify the raw timing.

The same table compares:

| System | Platform | Precision | `[32:32]` TTFT | Decode token/s |
|---|---|---|---:|---:|
| DFX | U280, 200 MHz | FP16 | 177.20 ms | 185.19 |
| Allo | U280, 250 MHz | W4A8 | 81.50 ms | 204.05 |
| StreamTensor | U55C, 250 MHz | W4A8 | 34.59 ms | 199.51 |
| CODO | U280, 300 MHz | W4A8 | 20.40 ms | 231.48 |

The paper reports headline speedups of 3.54x, 2.03x and 1.23x over DFX, Allo and StreamTensor. These are not the direct geometric means of Table VI's three diagonal total-latency rows, which are approximately 2.169x, 1.486x and 1.138x (using the published `313.44 ms` unchanged).

Fig. 9 instead covers 12 combinations: input lengths 32/64/128 and output lengths 1/16/64/256. Reconstructing those points from Table VI's per-input TTFT/decode rates with `TTFT + N_output / speed` gives approximate geometric means of 3.135x, 1.940x and 1.229x.

| Aggregation | vs DFX | vs Allo | vs StreamTensor |
|---|---:|---:|---:|
| Paper headline | 3.54x | 2.03x | 1.23x |
| Three published diagonal latency rows, geometric mean | 2.169x | 1.486x | 1.138x |
| Twelve Fig. 9 points inferred from Table VI stage metrics, geometric mean | 3.135x | 1.940x | 1.229x |

The 12-point reconstruction closely explains the StreamTensor headline and approaches the Allo value, but still does not reproduce 3.54x for DFX or exactly 2.03x for Allo. The paper does not publish Fig. 9's raw points or aggregation script, so all three headline values should remain labeled paper-reported.

## What “End-To-End” Means Here

At the paper-claim level, CODO is substantially closer to model-level end-to-end than an isolated HLS kernel result:

- the reported workload separates prefill/TTFT and autoregressive decode;
- latency combines first-token time and repeated output-token generation;
- the model is identified as GPT-2 Medium;
- the comparison is labeled as on-board.

The public artifact, however, does not expose enough orchestration to independently establish the complete 24-layer model boundary, and the result is not automatically the same boundary as a production `llama.cpp` request.

### Public artifact observations

The inspected `experiments/fig-9/` artifact contains separate designs for:

- `gpt-32-prefill`;
- `gpt-64_predill`;
- `gpt-128_prefill`;
- `gpt_decoding`.

Each generated host:

1. allocates aligned arrays and binds them across HBM banks;
2. enqueues host-to-device migration;
3. launches one `main_graph` kernel;
4. calls `q.finish()`;
5. reads only the OpenCL profiling interval for that kernel event.

The public host path does **not** visibly perform:

- text tokenization;
- loading a Hugging Face checkpoint in the executable;
- a real prompt-to-token pipeline;
- logits sampling or top-k/top-p;
- detokenization/text streaming;
- model-quality validation during the board timing run.

The kernel event also starts after the queued migration, so that event itself does not directly time the earlier PCIe H2D migration. Fig. 12 reports `off-chip data transfer` shares of 22.9%, 14.3% and 4.2% for GPT prefill lengths 32, 64 and 128, but in context this is most plausibly HBM traffic within the accelerator event, not the preceding OpenCL host-to-device setup. It cannot be used as evidence that PCIe migration is included in TTFT.

The source allocates value-initialized arrays, creates every OpenCL buffer with `CL_MEM_READ_ONLY`, and comments out output migration. Across all four inspected Fig. 9 kernels, the final graph node writes only to a local on-chip array (`v853`, `v847` or `v825`); there is no visible store back to the corresponding external pointer. Consequently, these public paths have no host-observable model output and cannot perform board-level output correctness checking. It should be confirmed whether the Table VI xclbins were built from exactly these sources and whether omitted output traffic is part of the reported boundary. Therefore the safest interpretation is:

> The paper reports a strong GPT-2 model-compute/generation-stage result with prefill and decode accounting. The inspected public host directly demonstrates only one generated `main_graph` command and does not establish either the complete 24-layer orchestration or the same application boundary as text-in/text-out `llama.cpp` wall-clock.

This is not a reason to dismiss CODO. It is a reason to label the boundary precisely, obtain the raw board harness/logs, and reproduce it separately from an application-level benchmark.

### Reproducibility caveats

- The arXiv appendix says prebuilt GPT-2 xclbins and host files are provided, but the official main revision, `isca2026-ae` tag and Zenodo snapshot all lack visible `.xclbin` and `host.exe` files. The Zenodo archive contains no GPT board logs or GPT synthesis/P&R report tied to its full-model prototype.
- The artifact says all on-board experiments are not rerun during AE because rebuilding all bitstreams takes over two weeks.
- The included HLS reports are useful synthesis evidence, but their absolute latency is not a substitute for Table VI's board measurements.
- The paper states a 300 MHz CODO setting and a 3.33 ns target for all experiments, but the public `gpt-128_prefill/Makefile` explicitly passes `--kernel_frequency 250` and its HLS report uses a 4.00 ns target. The other GPT reports use a 3.33 ns target but have estimated periods of 3.432-4.943 ns. Actual routed clocks and board binaries must be checked per workload.
- The GPT-2 verification model is one Transformer block; the exact layer-repeat, weight-switch and generation harness used to derive every Table VI field should be confirmed before claiming a fully matched reproduction.

### Evidence ledger

| Evidence | What it establishes | What it does not establish |
|---|---|---|
| arXiv Table VI / Figs. 9 and 12 | published GPT-2 Medium TTFT, decode rate, latency, comparison and kernel-internal transfer breakdown | raw timing derivation, application boundary, correctness output |
| GitHub main and `isca2026-ae` Fig. 9 tree | one W4A8 Transformer-block kernel per length, HBM bindings and one-event OpenCL host timing | 24-layer orchestration, LM head/sampling, externally visible output, retained board binary/log |
| Zenodo snapshot | an independent full 12-layer GPT-2 Base lowering prototype with final hidden-state output | GPT-2 Medium, W4A8 generation, synthesis closure or Table VI board execution |
| Docker Hub v1 metadata | a 6.2 GB AE image exists and was built by copying a workspace into the image | whether missing xclbins/logs are present; image layers were not downloaded for this audit |

## Why CODO Is The Priority Baseline

CODO attacks exactly the structural weakness exposed by the current backend profile:

| Current backend issue | CODO design response |
|---|---|
| one GGML call can expand to hundreds of XRT launches | compile a large graph/block into one dataflow kernel |
| repeated H2D -> launch -> wait -> D2H sequence | stream intermediates and optimize communication globally |
| per-operator optimization has low Amdahl ceiling | balance the complete dataflow pipeline |
| host/runtime overhead obscures HBM potential | amortize orchestration over coarse-grained work |
| hand-integrated kernels are hard to scale | compile from high-level IR with legality checks and DSE |

The comparison also reveals a tradeoff. CODO's performance comes from aggressive block/model specialization, while the current project contributes native GGML integration, explicit support semantics and a replaceable per-operator ABI. The high-value bridge is **contract-preserving region fusion**, not copying CODO wholesale.

## Matched Comparison Plan

A defensible CODO comparison needs two tracks.

### Track A: reproduce CODO's own boundary

- U280 physical board;
- GPT-2 Medium;
- W4A8;
- input/output lengths 32/32, 64/64 and 128/128;
- batch 1;
- TTFT, decode token/s and `TTFT + output/speed`;
- separately record model load, H2D setup and kernel-event timing;
- verify nonzero real weights and output against a PyTorch oracle.

### Track B: compare application/framework integration

Run a `llama.cpp`-native model on CPU and FPGA with:

- identical GGUF hash and quantization;
- identical prompt token IDs and output count;
- identical sampler or greedy policy;
- framework-level pp/tg plus text-in/text-out wall-clock;
- zero-fallback receipt and per-op execution counts;
- model-level logits/token correctness;
- power at a declared system boundary.

Only after the same model is available in both CODO and the GGML backend should the two tracks be collapsed into one speedup table.

## Questions To Resolve With The Authors

1. Does Table VI latency include initial PCIe host-to-HBM migration, or only resident-weight generation with kernel-internal HBM traffic? How was Fig. 12's transfer/compute split measured?
2. How is the single-block public `main_graph` lifted to all 24 GPT-2 Medium layers, and where are the layer-repeat and per-layer weight-switch operations timed?
3. Is TTFT derived from block events, a complete-model host loop, or another retained harness?
4. Where are the exact prebuilt xclbins and raw board logs corresponding to Table VI?
5. Are real GPT-2 Medium weights used in the timed board run, and where is output/logit correctness retained?
6. Were the Table VI xclbins built from the four public top functions that never store their final local arrays back to external memory, or are output-producing sources/binaries missing from the artifact?
7. Does decode speed include LM head and token selection?
8. Why does the `[64:64]` row report `313.44 ms` when `TTFT + 64 / speed` gives `309.12 ms`, while the 32- and 128-token rows satisfy the formula?
9. What raw Fig. 9 points and aggregation produce `3.54x / 2.03x / 1.23x`? A 12-point reconstruction from Table VI gives about `3.135x / 1.940x / 1.229x`, while the three diagonal total-latency rows alone give `2.169x / 1.486x / 1.138x`.
10. Why does the public 128-token Makefile target 250 MHz while the paper labels CODO as 300 MHz for all experiments, and what clocks do the retained xclbins actually achieve?
11. Are the Allo/DFX/StreamTensor values reproduced or transcribed from prior papers, and are all total-latency formulas identical?
12. Can the current CODO frontend compile Gemma 3 1B or a GGML-extracted region without changing semantics?

## Takeaways For The llama.cpp FPGA Work

1. The current 200k-launch regime must disappear before token/s can be competitive.
2. Whole-block fusion is an empirically demonstrated target, not just an optimization intuition.
3. Preserve the GGML backend as the application boundary, but add a graph-region compiler/runtime below it.
4. Make residency and command batching explicit contracts alongside numerical semantics.
5. Keep two “end-to-end” columns: model-phase and application request. This gives a fair CODO comparison without weakening the framework-native claim.

## Sources

- [arXiv paper](https://arxiv.org/abs/2604.12618)
- [Official artifact](https://github.com/sjtu-zhao-lab/codo-artifact)
- [Official Zenodo snapshot](https://doi.org/10.5281/zenodo.19425920)
- [StreamTensor](https://arxiv.org/abs/2509.13694)
- [DFX](https://arxiv.org/abs/2209.10797)
- [[research/fpga-llm-inference/index]] for the active comparison protocol and project status (folded from the former `end-to-end-evaluation` / `project-status-2026-07` notes, 2026-09-08).

Return to [[research/fpga-llm-inference/papers/index|FPGA LLM paper library]]. See also [[research/fpga-llm-inference/index]].

---
title: "CODO: An Automated Compiler for Comprehensive Dataflow Optimization"
domain: research
area: fpga-llm-inference
type: paper
status: active
updated: 2026-09-08
tags: [paper, fpga, llm-inference]
---

# CODO: An Automated Compiler for Comprehensive Dataflow Optimization

CODO is an automated MLIR/dataflow compiler for fixed-shape FPGA graphs. Its GPT-2 result is an
important compiler reference, but its public artifact must be kept separate from a stateful
llama.cpp generation baseline.

## Paper Meta

- Authors: Weichuang Zhang, Yiquan Wang, Xinzhou Zhang, Chi Zhang, Yu Feng, Xiaofeng Hou, Chao Li, Jieru Zhao, Minyi Guo
- Year: 2026
- Venue: ISCA 2026, verified against the [official conference program](https://www.iscaconf.org/isca2026/program/) on 2026-09-08. The archived full text is the arXiv version; venue verification is separate from artifact reproduction.
- BibTeX key: `codo`
- Related Work category: FPGA Transformer and LLM systems
- Public record: [arXiv](https://arxiv.org/abs/2604.12618)

## Local Assets

- Paper PDF: [2604.12618.pdf](2604.12618.pdf) (17 pages; SHA-256 `b31c6872fc51bf5f779fc501952b78fbfa6d6233a71464c1e07e5b0ac8ec5b2e`)
- arXiv source archive: [2604.12618-source.tar.gz](source/archives/2604.12618-source.tar.gz); extracted TeX: [main.tex](source/extracted/main.tex)

## Read Notes

- The paper reports GPT-2 Medium on U280 at W4A8/300 MHz, including TTFT, decode speed and total latency. These figures are useful for understanding fixed graph/dataflow performance, but are not inserted into the current CPU/FPGA throughput table.
- The public `GPT2.py` forward computes current-input Q/K/V but has no `past_key_values` input/output. The Fig. 9 host statically binds HBM buffers and invokes one `main_graph` event; no token loop, cache position, append pointer or cross-launch state object is exposed.
- Therefore “CODO has no K/V” is inaccurate, while “the public artifact does not demonstrate persistent KV-cache management or KV-specific optimization” is supported. The comparison note records the user's report of a private author clarification about fixed-graph timing; this is separate from the paper's published methodology.
- Source-first read completed. Detailed artifact audit: [[research/fpga-llm-inference/codo-2026]].

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
in [[research/fpga-llm-inference/codo-2026]].

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
- Feature-table definitions and cross-paper artifact discovery: [[research/fpga-llm-inference/feature-level-evidence-matrix]].

Return to [[research/fpga-llm-inference/papers/index|FPGA LLM paper library]].

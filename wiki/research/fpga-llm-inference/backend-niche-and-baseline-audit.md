---
title: FPGA backend niche, baseline admission and public availability audit
domain: research
area: fpga-llm-inference
type: comparison
status: active
updated: 2026-09-08
tags: [fpga, llama-cpp, ggml, vendors, reproducibility, baseline, prior-work]
---

# FPGA Backend Niche And Baseline Admission

## Decision

A native llama.cpp FPGA backend is not an unprecedented idea: SECDA-LLM is a documented
integration precedent. That does not establish an equivalent, mature replacement for our
current whole-model/HBM-state execution path. Commercial FPGA LLM serving also exists:
Positron Atlas and Achronix VectorPath can substitute at the application/API layer, without
necessarily supplying an inspectable GGML backend for an existing Alveo deployment.

Our defensible opportunity is a usable, modifiable and reproducible framework-integrated
FPGA execution path, not a claim that nobody has run LLMs or integrated llama.cpp on FPGA.
That opportunity is not yet a demonstrated ecosystem advantage: the inspected active profile
is tightly specialized, the retained board correctness gate is false, and this audit could
not anonymously access our configured origin repository. Local files do not establish a
public release. Not finding an equivalent does not prove uniqueness.

## Main-Table Admission

The user's criterion is an OR: substantive paper evaluation data, a public implementation
sufficient to undertake reproduction, or a verified leading-conference publication. Apply it
before capability scoring. Publication venue and release availability are independent axes;
a preprint with real evaluation can qualify, while a repository name or a venue-style TeX
template is insufficient. Peer review does not establish independently reproduced results.

For this pass, nine prior systems qualify through evaluation data. Publication records provide
additional corroboration for eight after CODO's venue recheck; FlexLLM's preprint record is
not admitted on title alone.
No full independent board reproduction of any competitor was performed here.

| Work | Publication record | Concrete evaluation basis | Public implementation boundary | Decision |
|---|---|---|---|---|
| DFX | MICRO 2022; DOI metadata checked | GPT-2 345M/774M/1.5B; generation latency, throughput, energy and output-length workloads | No official implementation verified in this audit | Main table; system baseline |
| FlightLLM | FPGA 2024; DOI metadata checked | U280 OPT-6.7B/LLaMA2-7B; latency, decode throughput, energy; separate VHK158 simulation | Profiler and binary/golden-case package; RTL withheld; full archive not locally present | Main table; compiler/system baseline, not open-RTL baseline |
| Spatial LLM | ACM TRETS 2024; DOI metadata checked | Physical GPT-2 phase measurements; additional model-family analysis distinguished from hardware runs | Allo kernel generation examples, not an audited generation release | Main table; phase/compilation comparison |
| EdgeLLM | IEEE TCAS-I 2025; DOI metadata checked | GLM/Qwen CPU-FPGA measurements and compiler/runtime evaluation | No official source release verified | Main table; system/runtime comparison |
| StreamTensor | MICRO 2025; DOI metadata checked | GPT-2 [32:32] table reports 34.59 ms TTFT, 199.51 token/s; length sweep and other model-phase results | Official implementation discovery inconclusive | Main table; compiler/phase comparison |
| CODO | ISCA 2026, verified in the official program; reviewed full text remains arXiv 2604.12618 | GPT-2 [32:32] table reports 20.40 ms TTFT, 231.48 token/s and 158.64 ms latency; synthesis/evaluation data | Real public compiler/verification/synthesis source; inspected decode host is one task, not a generation loop | Main table on data, venue and artifact substance; not a matched generation baseline |
| FlexLLM | Reviewed citation remains arXiv 2601.15710; no venue inferred from fccm26.tex | U280 Llama-3.2-1B measured; table gives prefill 1.65 s/1k tokens and decode 6.94 s/1k tokens; V80 results projected | HLS, images and prompt/sampling/KV demo; external assets and dependencies still needed | Main table; strong public generation-artifact candidate |
| LUT-LLM | FCCM 2026; DOI metadata checked | Qwen3-1.7B accuracy, implementation and latency/energy figures | HLS, V80 image and AE; E2E calculator extrapolates block cycles | Main table; algorithm/hardware and phase evidence, not a reproduced chatbot |
| TeLLMe | FPGA 2026; DOI record checked | BitNet-0.73B/KV260, up to 25 token/s, prompt-length/TTFT sweep and quality/power comparison | HLS/bitstream/chatbot with prefill, repeated decode, KV and sampling; external weights needed | Main table; strong public application-artifact candidate |

Numbers above are paper-reported examples showing that data exists, not normalized performance
rankings or confirmation that a published E2E timer includes every application operation.
Spatial LLM and EdgeLLM are journal publications, not mislabeled top-conference papers.
Crossref title search for FlexLLM returned unrelated works sharing its name; those records
must not be substituted for the HLS-library paper.

The [official ISCA 2026 program](https://www.iscaconf.org/isca2026/program/) confirms
CODO's venue; the earlier preprint-only classification is superseded. This correction does
not change the inspected artifact's execution boundary. See
[[research/fpga-llm-inference/manuscript-evidence-recheck-20260908]] for the follow-up.

The manuscript now has **nine prior-work rows plus one explicitly local row**. SECDA-LLM
moves to the integration-precedent discussion, not because it has no evidence, but because
its original short evaluation is too limited to be a principal system-performance baseline.
FAST-Prefill and PD-Swap remain thematic comparisons; Hummingbird+ remains access-limited.

## SECDA: What The Evidence Actually Establishes

The original [abstract](papers/secda-llm-2024/source/extracted/00_main.tex) and
[Evaluation](papers/secda-llm-2024/source/extracted/04_evaluation.tex) explicitly state
"1.7 seconds per token" and about 11x versus dual-core ARM NEON, for TinyLlama-1.1B on PYNQ-Z1.
The reciprocal is about 0.59 token/s; it is a unit conversion, not a new measurement.
Saying that it reports no token-rate data is factually incorrect. Saying its measurement
protocol is insufficient for a rigorous head-to-head comparison is justified: there is no
complete prompt/output-length specification, separated phase sweep, or detailed quality gate.

Its [integration section](papers/secda-llm-2024/source/extracted/03_design.tex) documents
llama.cpp/GGML offload into a C++ driver/SystemC environment. Its later official code really
registers a GGML backend. This restricts a "first llama.cpp FPGA integration" claim, even if
it is not a competitive or reproduced release. The later code must not be backdated to 2024.
Only the arXiv publication was verified; the limited Crossref title query found no exact
publication match and does not prove that no later publication exists.

The current [SECDA note](papers/secda-llm-2024/index.md) distinguishes selective quantized
MatMul offload and host-managed KV from full-model device execution. Neither the arXiv venue
nor the mere presence of code proves or disproves maturity.

## Substitution Has Several Meanings

| User need | Most relevant alternatives | Does it replace this niche? |
|---|---|---|
| Add FPGA operator offload while retaining llama.cpp | SECDA-LLM | Direct partial substitute and integration precedent; different operator/state/platform boundary |
| Serve LLMs through standard APIs on FPGA hardware | Positron Atlas; Achronix VectorPath | Application-level commercial alternatives; native GGML integration is not necessary for this user |
| Modify and study a complete public FPGA generation implementation | FlexLLM; TeLLMe | Strong artifact candidates, but custom application/quantization/platform paths |
| Compare GPT-2 dataflow/compiler performance | DFX, Spatial LLM, StreamTensor, CODO | Relevant architectural controls; model/format/phase/host boundaries still need matching |
| Run existing GGUF workflows on a chosen FPGA with inspectable hardware and runtime | SECDA plus the above are partial substitutes | No equivalently qualified, drop-in package established in this bounded search; our own package also does not yet meet that bar |
| Simply run a local LLM efficiently | llama.cpp CPU/CUDA/Vulkan/other supported devices | Real practical alternatives even though not FPGA research baselines |

### Commercial Evidence

**Positron.** The official [platform page](https://www.positron.ai/) advertises Hugging Face
model ingestion and an OpenAI-compatible API. [Atlas](https://www.positron.ai/atlas) specifies
8 Archer accelerators, 32 GB HBM each, and an inference engine. Its official press page
links an Altera Agilex partnership. Atlas is the FPGA-generation comparison; future Asimov
silicon/Titan must not be conflated with the shipping Atlas generation. The vendor's
Llama-3.1-8B BF16 280 token/s/user claim is a system-level product claim, not a matched
single-U280 result. The organization exposes API documentation, clients and model/tool forks;
that is not proof of a public FPGA RTL/compiler/runtime release.

The public `positron-ai/llama.cpp` fork was inspected at
`a1cfb645307edc61a89e41557f290f441043d3c2`: its untruncated file tree and backend registry did
not identify an FPGA/Positron backend. A fork's existence alone is not native FPGA support.
This is a selected-file inspection, not proof about private code or every branch.

**Achronix.** Its official [LLM page](https://www.achronix.com/AI/large-language-model-acceleration)
explicitly describes VectorPath FPGA execution, model compilation, KV optimization and standard
APIs. The [AI Console](https://www.achronix.com/Achronix_AI_console) offers a request-based
30-day evaluation on VectorPath 815/7t1500 with GDDR6. This is a concrete vendor offering,
not evidence of an anonymously downloadable GGML backend or source-to-bitstream release.
No console registration, purchase or benchmark was performed. These vendors belong in the
commercial landscape, not the source-backed feature table on marketing claims alone.

**AMD tooling.** The existing [[research/fpga-llm-inference/vitis-ai-dpu-finn-pynq]] audit
covers specific Vitis AI v3.5, FINN and PYNQ interfaces. These are relevant toolflow precedents;
it does not establish a ready-to-use U280/GGUF LLM backend. SYCL/OpenVINO support for Intel
GPUs/CPUs/NPUs must not be converted into an Altera FPGA support claim.

## Our Actual Implementation Boundary

This pass re-read the fork's active Q4 runtime, graph matcher, model loader, context checks,
documentation and frozen generation receipt. `/home/zdpeng/llama.cpp` contains build remnants,
not a source checkout; upstream was read through the fork's `upstream/master` at
`bae36efa30012d5dbaf842f893c5d034c0ba0157` and the current official backend-registry API response.
No named native FPGA backend appears in those inspected upstream registration lists. This
is not an exhaustive search of upstream discussions, branches or out-of-tree plugins.

- [Active context checks](/home/zdpeng/llama.cpp-fpga/src/llama-context.cpp:58) require GPT-2 Medium,
  24 layers, hidden size 1024, one sequence, context at most 1024, F16 KV and full placement;
  alternate callbacks, linked contexts, attention and RoPE options are rejected.
- [Active Q4 runtime](/home/zdpeng/llama.cpp-fpga/ggml/src/ggml-fpga/ggml-fpga-q4-runtime.cpp:262)
  validates the graph, executes a bounded request, checks completion, then publishes logits and
  advances past position. Initialization permits only one active context; clear requires known-idle
  device state. This is useful implemented state ownership, not general multi-user serving.
- [Graph matcher](/home/zdpeng/llama.cpp-fpga/ggml/src/ggml-fpga/ggml-fpga-model-graph.cpp:903)
  explicitly restricts the Q4 profile to GPT-2 Medium. Frontend enums for another architecture and
  older Gemma traces are not multi-model evidence for this active release.
- [Model loading](/home/zdpeng/llama.cpp-fpga/src/llama-model.cpp:1625) tags stable tensor roles and
  treats FPGA weights as logical shells backed by prepared shards. FPGA-specific framework hooks
  exist. "Native backend" does not mean an unmodified-upstream binary can load it as a generic plugin.
- [Runtime documentation](/home/zdpeng/llama.cpp-fpga/docs/backend/FPGA.md:86) describes HBM-resident
  weights/KV, one XRT run per graph, bounded IO and no CPU arithmetic fallback on the accepted path.
  Sampling and application control still remain on the host; no-fallback is not an application-wide
  claim that the CPU does no work.
- [Frozen receipt](/home/zdpeng/llama.cpp-fpga/build-fpga-q4/evidence-20260907-32x32-r3/README.md)
  retains 32 generated output IDs and native phase measurements, but explicitly states board
  correctness false, full qualification false and experimental delivery incomplete. Older status
  prose saying no board result exists is stale; the actual retained gates still control acceptance.
- Anonymous GitHub API lookup of configured origin `zedong-peng/llama.cpp-fpga` returned 404.
  That does not prove deletion/private status, but does mean this audit cannot award public Src/Bin
  to the exact current profile. We did not publish or change access permissions.

The local table row is `Y / Y / NR / P / Y / Y / NR`, explicitly footnoted as execution evidence
with failed correctness qualification. Mapping P is fixed-template preparation/packing, not
arbitrary GGML-to-hardware lowering. Existing framework-native and device-state code is valuable
engineering, but reusable ecosystem value remains contingent on delivery and adoption.

## What Would Make Public Availability An Advantage?

Publicness should describe what a third party can actually do:

1. Obtain the licensed implementation, including meaningful runtime and hardware source.
2. Obtain a compatible image, exact model identity or legal acquisition recipe, dependencies and commands.
3. Generate multiple tokens, compare against a pinned CPU reference and inspect rejected configurations.
4. Modify a model/profile and rebuild without undisclosed compiler/IP dependencies beyond stated vendor tools.
5. Reproduce numerical and performance results on the stated board without author-specific machine paths.

A binary demo, a source-only compiler and an API service provide different subsets. None should
receive an undifferentiated "open/reproducible" check mark. FlexLLM and TeLLMe are especially
important comparisons because they already expose substantial generation artifacts. To demonstrate
our added value, measure model-porting effort, phase latency, device-state traffic and correctness,
not just the number of source files or framework-interface callbacks.

Priority comparisons: matched llama.cpp CPU and an available GPU for practical utility; a
SECDA-style MatMul-only mode versus full device-state execution on the same board/model for
mechanism isolation (label any reimplementation as such); FlexLLM/TeLLMe for artifact usability;
CODO/StreamTensor for graph execution; vendors for API-level deployment alternatives.

## Search And Archive Scope

[Retained source records](supplementary/backend-niche-20260908/receipts.json) contain official
HTML, GitHub metadata/selected source, discovery queries and Crossref records with hashes.
This is an official-source and repository-interface audit, not full ingestion of every found repo.

GitHub repository searches for `llama.cpp FPGA`, `ggml FPGA`, and `FPGA backend llama.cpp in:readme`
returned 3, 1 and 142 hits; only the first 50 of the broad query were screened. Exact queries did
not even return SECDA, illustrating why absence in search results proves little. CORDIC-softmax's
README says CPU work complete, integration in progress, HLS/deployment pending. WPU's README
separates its RTL/fit claims from no hardware throughput and excludes whole-runtime equality.
Vysh's README is inherited llama.cpp text. These are discovery leads, not promoted baselines;
none was independently built. Other broad-query candidates remain unread. Google/DDG access
failed and Bing results were unhelpful, so no claim of an exhaustive vendor search is made.

See [[research/fpga-llm-inference/feature-level-evidence-matrix]],
[[research/fpga-llm-inference/papers/secda-llm-2024/index]], and the historical
[[research/fpga-llm-inference/towards-idea-audit-2026-07]]. The latter's old Gemma timing and
per-operator launch model must not be used as current Q4 measurements.

Return to [[research/fpga-llm-inference/index]].

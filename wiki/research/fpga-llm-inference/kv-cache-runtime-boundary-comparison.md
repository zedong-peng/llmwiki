---
title: KV Cache and Runtime Boundary Comparison
domain: research
area: fpga-llm-inference
type: comparison
status: active
updated: 2026-09-07
tags: [fpga, llm-inference, kv-cache, hbm, runtime, related-work, codo]
---

# KV Cache and Runtime Boundary Comparison

## Comparison Rule

不能用一个 `KV cache: yes/no` 覆盖所有语义。核查时至少分三层：

1. **K/V computation**：attention 图是否生成 K、V tensor；Transformer 几乎都会满足。
2. **Persistent KV state**：历史 K/V 是否跨 autoregressive step 保存，并有 append、read、
   position、reset/commit 等状态语义。
3. **KV-specific optimization**：论文是否进一步说明 cache 的物理位置、布局、分 bank、
   paging/tiling、DMA 或带宽优化。

“实板模型”只记录论文明确在物理 FPGA 上运行的生成模型；分析结果与作者声称可支持的
模型不计入。类似地，“通用”需要说明是**重新编译不同模型的 toolflow generality**，还是
**同一框架/backend 接口下的 runtime generality**。

## System Comparison

| Work | System form / reuse boundary | Board-demonstrated generative models | Numeric format | Persistent KV state | KV placement / optimization | Stateful end-to-end flow (same metric boundary) |
|---|---|---|---|---|---|---|
| [DFX](https://arxiv.org/abs/2209.10797) | custom GPT appliance, ISA and multi-FPGA engine | GPT-2 345M/774M/1.5B | FP16 | **Yes**: generation appends one K/V row for each new token | tiled K/V are loaded/stored through DMA and HBM | model-level complete GPT-2 text generation; framework/runtime ABI is not exposed |
| [FlightLLM](https://arxiv.org/abs/2401.03868) | model compilation flow plus temporal accelerator | OPT-6.7B, LLaMA2-7B | sparse mixed precision, average W3.5/A8 | **Yes** | large KV cache and weights are explicitly placed in HBM; decode activations use an always-on-chip scheme | partial for this boundary: complete mapping and model-level generation, but runtime/sampling ABI is not exposed |
| [Spatial LLM](https://arxiv.org/abs/2312.15159) | HLS kernel library plus per-model spatial pipeline | GPT-2; LLaMA/Vicuna are analytical studies | GPT-2 W8A8 | **Yes**: K/V from prefill are passed to decode as KV cache | K/V double buffering; paper also models on-chip KV tiling | partial for this boundary: GPT-2 model-level prefill/decode, not a framework-native backend |
| [EdgeLLM](https://arxiv.org/abs/2407.21325) | heterogeneous compiler/runtime plus instruction engine | GLM-6B, Qwen-7B | FFN FP16×INT4; MHA FP16×FP16 | **Yes** | dedicated DMA writes online-generated KV cache to HBM; common tensor layout improves burst access | model-level CPU-FPGA generation path; reusable application/backend ABI is not exposed |
| [StreamTensor](https://arxiv.org/abs/2509.13694) | PyTorch/Torch-MLIR compiler generating a block dataflow accelerator/runtime | GPT-2, Qwen, Llama, Gemma | W4A8 | **Mentioned but protocol not exposed**: KV cache is named as a dynamic tensor | maximum-shape hints are described; append, placement and cross-call state protocol are not detailed | paper reports total latency, TTFT and decode throughput; runtime state boundary is not documented at backend-ABI granularity |
| [CODO](https://arxiv.org/abs/2604.12618) | general dataflow compiler generating a fixed-shape graph for each input program | GPT-2 Medium in the paper table | W4A8 | **Not shown in the public paper/artifact**; the graph still computes current-input Q/K/V | no KV-specific state/layout optimization is exposed | **Not established for this boundary**: public GPT host migrates buffers once and invokes `main_graph` once; artifact boundary is one fixed-graph kernel event, while the paper reports 231.48 tok/s/TTFT figures on that separate axis |
| Current llama.cpp FPGA backend | native GGML backend plus XRT model-graph engine; current xclbin is still profile-specific | GPT-2 Medium | Q4_0/Q6_K weights; F16 KV | **Yes**: append/read/clear/commit across llama.cpp decode calls | 96 MiB HBM-resident K/V, separated K/V ports and four-bank sharding | **Supported for the current profile**: GGUF load → GGML graph → stateful device execution → logits → llama.cpp sampling; `pp/tg/pg`, runtime TTFT/ITL and correctness |

## CODO: The Precise KV Conclusion

CODO 不能写成“Transformer 没有 K/V”。其 GPT-2 Python model 在每次 forward 中计算 Q、K、V，
固定图 HLS 代码也包含 attention tensor。能够从公开材料成立的结论更窄：

- paper TeX 的方法部分没有 KV cache、`past_key_values` 或持久状态协议；
- verification `GPT2.py` 的 `forward(x)` 只从当前 `x` 计算 Q/K/V，没有 cache input/output；
- Fig. 9 GPT host 一次性建立/迁移 buffer，只调用一次 `enqueueTask(main_graph)`；
- host 中没有 token loop、cache position、append pointer 或跨 launch state object；
- 作者补充说明该实验关注固定图的一次执行 latency，未考虑 KV cache 优化。

因此推荐表述为：

> CODO 公开展示的是固定-shape Transformer 图的 dataflow 编译与单次 graph execution；
> 公开 paper/artifact 没有展示跨 token 的 persistent KV-cache management，也没有展开
> KV-specific optimization。

这不是对论文 decode 数字真伪的判断，也不是说 CODO 编译器原则上不能扩展 KV；它只限定
当前可复核 artifact 的系统边界。基于这一边界，CODO 适合放在 Related Work 的 compiler/
fixed-graph 行，不适合作为 stateful llama.cpp generation 表中可直接计算倍数的 throughput
baseline。

## Metric Boundary by Execution Object

| Execution object | State carried by one invocation | Appropriate metrics | Placement in this comparison |
|---|---|---|---|
| Fixed-shape Transformer graph / kernel | fixed input tensors and graph shape; no requirement to continue a previous generation call | kernel/event latency, graph transfer time, cycle count and resource use | CODO |
| Stateful LLM backend / generation | model context, position, cross-token KV, logits and sampling state | pp/tg/pg, TTFT, ITL/TPOT, end-to-end latency, KV depth and correctness | Current llama.cpp FPGA backend |

Thus CODO's one-graph latency (including its reported 231.48 tok/s fixed-shape figure) and the
backend's stateful-generation throughput are different experimental axes. A numeric comparison is
meaningful only after model, shape, precision, state semantics and timing boundary are matched.

## Candidate Contribution and Insights (Not Established Claims)

The most defensible candidate contribution is a framework-native, profile-complete backend contract
that joins the real GGML graph, cross-token state, HBM buffer identity, XRT execution receipt and
llama.cpp sampling in one auditable path. This is a systems-contract claim, not a claim that one
xclbin already runs every model; a second profile and matched experiments are required before using
it as a paper contribution.

从比较表可以提出一个待验证的系统主线：FPGA LLM backend 需要同时闭合 graph、persistent
state 和 runtime 三层合同，而不仅是生成一张高效 dataflow 图。它能否成为论文 contribution，
取决于以下反证门槛：

- 用同一 backend/runtime contract 接入第二个模型 profile，而不是另写 host 路径；
- 在不同 context depth 上验证 KV continuation、reset 和 logits 对 CPU oracle 一致；
- 用 bank-map/context sweep 和 HBM counter 证明 K/V 分离与分 bank 确有收益；
- 只在模型、精度、状态语义和计时边界匹配后计算跨系统 speedup。

若第二模型仍需重写 backend，runtime generality 主张应收缩；若 KV bank 消融无性能变化，
HBM layout 应保留为实现细节，而不是方法贡献。

## Local Source Ledger

- DFX TeX: [4_architecture.tex](papers/dfx-2022/source/extracted/4_architecture.tex),
  [5_microarchitecture.tex](papers/dfx-2022/source/extracted/5_microarchitecture.tex) and
  [6_evaluation.tex](papers/dfx-2022/source/extracted/6_evaluation.tex); relevant passages describe
  model-level generation, per-token K/V use and HBM DMA for tiled K/V. The PDF remains at
  [2209.10797.pdf](papers/dfx-2022/2209.10797.pdf).
- FlightLLM TeX: [memory-hier.tex](papers/flightllm-2024/source/extracted/content/memory-hier.tex),
  which explicitly places large KV cache and weights in HBM.
- Spatial LLM TeX: [3.2-modeling-constraints.tex](papers/spatial-llm-2024/source/extracted/sections/3.2-modeling-constraints.tex)
  and [5.2-accelerator.tex](papers/spatial-llm-2024/source/extracted/sections/5.2-accelerator.tex);
  the source describes K/V buffering and tiling.
- EdgeLLM PDF: [2407.21325.pdf](papers/edgellm-2025/2407.21325.pdf); the architecture text
  describes the dedicated HBM KV-cache write DMA.
- StreamTensor TeX: [main.tex](papers/streamtensor-2025/source/extracted/main.tex), especially
  the dynamic-tensor shape-hint discussion.
- CODO TeX: [main.tex](papers/codo-2026/source/extracted/main.tex); artifact audit and open
  questions are retained in [[research/fpga-llm-inference/codo-2026]].
- CODO executable artifact audit: `/home/zdpeng/codo/paper/codo-study-notes.md` and
  `/home/zdpeng/codo/experiments/fig-9/gpt_decoding/host.cpp`.

返回 [[research/fpga-llm-inference/index]]。

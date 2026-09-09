# user_ref:arxiv_id:2601.15710

paper_id: user_ref:arxiv_id:2601.15710
tier: U
source_used: html_arxiv
warning: none

## Intro

Figure 1:
Comparison of three architectural styles for LLM accelerators across prefill and decode stages. Different colors indicate different tokens and blocks denote hardware modules. Only the linear layer is shown for clarity, where
A
A
denotes the Multi-Head Attention (Grouped-Query Attention here) and
O
O
denotes the output projection.
(a) One Transformer block.
(b–c) Temporal architectures achieve high utilization via module reuse but suffer from frequent off-chip memory access and limited flexibility.
(d–e) Spatial architectures dedicate modules per kernel for full on-chip streaming but are sensitive to pipeline stalls.
(f–g) Hybrid architectures combine temporal reuse and spatial parallelism to balance utilization, latency, and flexibility.
Large Language Models (LLMs) have emerged as one of the most transformative technologies of the modern era, driving breakthroughs across natural language processing
[
12
,
34
]
, code generation
[
10
,
28
]
, and multimodal understanding
[
1
,
2
]
. While cloud providers continue investing heavily in GPU-based infrastructures to support large-scale inference
[
26
]
, there is a growing demand for
domain-specific accelerators
that provide customized, efficient, and scalable alternatives across deployment environments—from data centers
[
23
,
8
]
to edge platforms
[
11
,
24
]
.
Compared to general-purpose CPUs and GPUs, domain-specific accelerators have demonstrated significant gains in performance and energy efficiency for prior DNN workloads (e.g., CNNs
[
39
,
5
]
, ResNets
[
27
,
31
,
18
]
). However, modern LLMs differ substantially from conventional DNNs: they contain billions of parameters and exhibit more complex computation and memory access patterns
[
7
,
13
,
29
]
, resulting in far higher demands on compute throughput, memory bandwidth, and architectural flexibility. These characteristics present three key challenges in designing efficient LLM accelerators:
Challenge 1: Divergent compute and memory behaviors in prefill vs. decode.
LLM inference with Transformer decoders consists of two stages with fundamentally different bottlenecks. During
prefill
, the model processes the prompt in parallel, offering high arithmetic intensity and abundant parallelism. During
decode
, tokens are generated autoregressively; computation is dominated by data dependencies and frequent memory accesses, making it strongly memory-bandwidth-bound. As a result, the same model is often compute-bound in prefill but memory-/dependency-bound in decode, creating conflicting optimization goals within one serving pipeline.
Existing FPGA accelerators primarily follow either
temporal architectures
[
23
,
38
]
or
spatial architectures
[
6
,
14
,
9
,
37
]
. Temporal designs reuse shared compute engines across layers, but incur frequent off-chip traffic in prefill due to limited buffering and struggle to support heterogeneous kernels/precisions within a single engine (Fig.
1
(b)(c)). Spatial designs map kernels to dedicated modules and stream intermediate data through on-chip FIFOs, but suffer from pipeline stalls when kernel latencies are unbalanced or when intrinsic dependencies dominate (Fig.
1
(d)(e)). Despite their differences, both paradigms typically share the same implicit choice: using a
single unified architecture
to serve both stages.
However, since prefill and decode are bottlenecked by different resources, a unified (temporal, spatial, or even hybrid) design inevitably over-optimizes one stage while under-serving the other. In other words,
any “one-size-fits-all” architecture is fundamentally mismatched to LLM serving: prefill and decode must be stage-customized
, with each stage adopting a different mix of spatial parallelism and temporal reuse to match its distinct compute/memory constraints.
Challenge 2: Balancing model accuracy and low-bit compute/memory efficiency.
LLMs have enormous parameter counts, making compression indispensable for accelerator deployment
[
8
,
38
]
. Quantization is an effective way to reduce compute and memory cost; however, prior FPGA LLM accelerators often rely on naive integer quantization, which can severely degrade accuracy when pushed to the aggressive low-bit regime required to approach GPU-level throughput, making such designs impractical for real deployment. For example, applying INT4 SmoothQuant
[
36
]
or GPTQ
[
15
]
to Llama 3.2-1B increases perplexity to over
1
​
e
​
2
1e2
on WikiText-2
[
30
]
. Given FPGAs’ limited compute capability relative to GPUs,
practical LLM acceleration must rely on state-of-the-art quantization with hardware-oriented co-design
, rather than naive quantization pipelines.
Challenge 3: High manual effort and slow iteration for model-specific accelerators.
As LLM architectures evolve rapidly, developing model-specific accelerators remains highly labor-intensive. RTL-based implementations can exceed 100K lines of code and impose a steep learning curve, making it difficult to iterate at the pace of LLM innovation. Recent HLS frameworks such as Allo
[
9
]
and StreamTensor
[
37
]
reduce RTL burden via MLIR-based mapping and automated compilation, but they largely target spatial architectures and offer limited support for hybrid designs that optimize prefill and decode specifically.
To close this productivity gap,
a high-level programming framework that enables flexible architecture design is necessary for the rapid growth of LLM-oriented accelerators.
Without a composable framework, accelerator development cycles (often 1–2 years) cannot keep pace with the rapid evolution of LLMs, where new model releases occur on the order of months. What is needed is a framework that exposes the key architectural degrees of freedom—especially stage-customized hybrid design and advanced quantization—while remaining accessible to both ML and accelerator developers.
Motivated by these challenges, we develop
FlexLLM
, a composable HLS library for domain-specific LLM accelerator design. Built on TAPA
[
19
]
, FlexLLM provides highly parameterized and templated modules that enable rapid construction of hybrid accelerators. Importantly, FlexLLM is, to our knowledge,
the first to explicitly go beyond the unified-design paradigm and enable stage-customized hybrid architectures
. This significantly improves design flexibility and accelerator performance while offering a reusable methodology for future LLM accelerator development. Using FlexLLM, we build a high-performance accelerator system that integrates state-of-the-art LLM techniques with fewer than 1K lines of C++ code, demonstrating that FlexLLM can rapidly incorporate new algorithmic innovations while significantly reducing development effort. We will open-source FlexLLM upon publication.
In summary, our main contributions include:
•
We present FlexLLM, a composable HLS library that supports
flexible hybrid, stage-customized architecture construction
for LLM accelerators. Its highly templated modules enable rapid model-specific customization while significantly reducing design complexity and code volume.
•
We integrate a comprehensive quantization stack—covering dynamic and static variants, multiple symmetry and granularity options, and outlier-handling modules—enabling accurate and efficient LLM deployment on customized accelerator platforms. To the best of our knowledge, this provides the most advanced quantization support among existing LLM accelerator frameworks.
•
Leveraging FlexLLM, we build a stage-customized hybrid accelerator for Llama-3.2 1B with a hardware-aware W4A4KV8 SpinQuant
[
30
]
scheme, reducing WikiText-2 PPL from 13.30 (original SpinQuant) to 12.68. Compared to the BF16 baseline on an NVIDIA A100 GPU, our FPGA implementation delivers 1.29
×
\times
end-to-end speedup, 1.64
×
\times
higher decode throughput, and 3.14
×
\times
better energy efficiency on AMD Alveo U280, and an estimated 4.71
×
\times
, 6.55
×
\times
, and 4.13
×
\times
gains, respectively, on Versal V80.
•
We further implement a Hierarchical Memory Transformer (HMT)
[
21
]
plug-in on top of FlexLLM for long-context processing, reducing prefill latency by up to 23.23
×
\times
and extending the effective context window by over 64
×
\times
with less than 7.5% resource and 0.6% latency overhead, demonstrating FlexLLM’s scalability to long-context acceleration.

## Method

III-A
stage-customized Module Templates
As discussed in
II-A
, prefill and decode stress fundamentally different resources, so a single unified architecture inevitably compromises one stage. FlexLLM addresses this by providing
stage-customized module templates
that expose the right parallelism knobs for each stage, enabling rapid construction of hybrid accelerators with balanced pipelines.
Prefill-stage modules:
Prefill exposes abundant inter-token parallelism. FlexLLM packs activations from multiple tokens and processes them concurrently for both linear and non-linear layers (Fig.
3
(a)). We define this inter-token parallelism as
token_parallelism (TP)
. Since linear layers dominate compute, we further introduce
weight_parallelism (WP)
to fetch and stream multiple weight channels from off-chip memory in parallel. Each prefill linear module implements a 2D systolic array of
TP
×
WP
\textit{TP}\times\textit{WP}
processing elements (PEs), optimized with an initiation interval (II) of one cycle for supported precisions.
Given a prompt of length
l
p
l_{p}
, the theoretical prefill latency of a linear layer with input dimension
d
i
​
n
d_{in}
and output dimension
d
o
​
u
​
t
d_{out}
can be expressed as
T
linear
p
=
l
p
​
d
i
​
n
​
d
o
​
u
​
t
TP
⋅
WP
,
T^{p}_{\text{linear}}=\frac{l_{p}\,d_{in}\,d_{out}}{\textit{TP}\cdot\textit{WP}},
(1)
and the corresponding off-chip bandwidth demand is
B
​
W
linear
p
=
B
W
⋅
WP
⋅
F
,
BW^{p}_{\text{linear}}=B_{W}\cdot\textit{WP}\cdot F,
(2)
where
B
W
B_{W}
is bytes per weight element and
F
F
is the operating frequency. These knobs allow users to balance layer throughput while respecting memory-bandwidth constraints.
Decode-stage modules:
Decode is constrained by autoregressive dependencies, leaving parallelism primarily within a single token. FlexLLM therefore exploits intra-token parallelism by partitioning each output hidden vector into blocks computed in parallel and reduced on-chip. We denote this as
block_parallelism (BP)
. Each decode linear module also supports
WP
, implemented as
BP
sets of 1D systolic arrays with
WP
/
BP
\textit{WP}/\textit{BP}
PEs each (Fig.
3
(b)). For decode length
l
d
l_{d}
, the idea latency of a linear layer with the same
d
i
​
n
d_{in}
and
d
o
​
u
​
t
d_{out}
is
T
linear
d
=
l
d
​
d
i
​
n
​
d
o
​
u
​
t
WP
.
T^{d}_{\text{linear}}=\frac{l_{d}\,d_{in}\,d_{out}}{\textit{WP}}.
(3)
The off-chip bandwidth follows Eq.
2
. Compared to prefill, decode PEs do not share weights across tokens, so the same resource budget can often support a higher
WP
, increasing bandwidth demand and motivating careful stage-specific tuning.
Figure 3:
stage-customized module design for (a) prefill, (b) decode, and (c) quantization module integration.
Quantization modules:
Quantization modules use the same configurable parallelism (
TP
for prefll and
BP
for decode) as the non-linear modules. As shown in Figure
3
(c), the quantizer converts FP inputs to low-bit integers using scales and zero offsets, which are either preloaded (static) or computed online (dynamic). After kernel computation, the dequantizer reconstructs FP outputs using the same scales and offsets, along with auxiliary data (e.g., per-channel weight scales and sums) buffered on-chip. In general, our framework supports static/dynamic and symmetric/asymmetric quantization with per-tensor, per-token, and per-channel granularities, and includes outlier-handling modules such as rotation and FHT.
Library components:
Following these principles, FlexLLM provides a comprehensive module library built on TAPA, comprising over 10K lines of highly parameterized code. It includes core LLM kernels, quantization/dequantization modules, and auxiliary components for on-chip streaming, buffering, and memory access management. Table
III
summarizes the key modules and configurable parameters. These templates enable rapid, composable hybrid architecture exploration while remaining accessible to non-expert developers, reducing model-to-silicon turnaround from months to weeks.
TABLE III:
Overview of primary module templates, configurable parameters, and Module interfaces provided in FlexLLM.
Module Template
Module Configurable Parameter
Module Interface
Kernel Library
Linear Layer
dtype, token_parallelism(prefill), block_parallel(decode), head_parallel(MHA), weight_parallelism, head_num(MHA), max_in_dim, max_out_dim, max_seq_len
in_stream, w_stream, out_stream, in_dim, out_dim, seq_len
Non-Linear Layer (RoPE, Softmax, LayerNorm, …)
dtype, token_parallelism(prefill), block_parallel(decode), head_parallel(MHA), head_num(MHA), max_io_dim, max_seq_len
in_stream, out_stream, io_dim, seq_len
Quant Library
Static/Dynamic Quant Layer
in_dtype, in_quant_bit, token_parallelism(prefill), block_parallel(decode), head_parallel(MHA), in_quant_type(sym/asym), in_quant_granularity(per-tensor/token), head_num(MHA), max_io_dim, max_seq_len
in_stream, in_scale_stream, in_zero_stream, quant_in_stream, io_dim, seq_len
Static/Dynamic Dequant Layer
in_quant_bit, w_quant_bit, out_dtype, token_parallelism(prefill), block_parallel(decode), head_parallel(MHA), in_quant_type(sym/asym), in_quant_granularity(per-tensor/token), w_quant_type(sym/asym), w_quant_granularity(per-tensor/channel), head_num(MHA), max_io_dim, max_seq_len
quant_out_stream, in_scale_stream, in_zero_stream, w_scale_stream, w_col_sum_stream, out_stream, io_dim, seq_len
III-B
Hybrid Accelerator Construction & Optimization
Built upon the FlexLLM and TAPA HLS flows, users can efficiently explore hybrid architectures for LLM accelerators and quickly transition from design exploration to on-board implementation. Figure
4
illustrates a simplified example that composes several modules in a hybrid style.
In the temporal-reuse part, the same templated module is instantiated and invoked multiple times within a single function to sequentially process similar operations. In this example, the prefill module of the linear layer and RoPE is reused for both
Key
and
Query
computations. This approach maximizes hardware utilization by reusing computation resources across similar tasks while minimizing redundant module instantiations.
In the spatial dataflow part, each instantiated module is explicitly invoked at the top level and connected through on-chip FIFOs to enable parallel execution and streaming communication. This module-based composition exploits inter-module pipelining and on-chip dataflow to achieve high throughput and overlap between computation stages.
The combination of temporal and spatial styles can effectively balance performance and resource efficiency in hybrid accelerator design. We illustrate a detailed methodology for stage-customized hybrid design through a case study in Sec.
IV
. After composing an accelerator with FlexLLM, users can leverage its seamless compatibility with AutoBridge
[
20
]
to optimize placement and routing (P&R), enabling parallel exploration of design candidates to achieve higher frequency and performance. This end-to-end toolchain accelerates iteration and supports efficient on-board deployment.
Figure 4:
Example code illustrating hybrid architecture construction combining temporal reuse and spatial dataflow with FlexLLM.
Figure 5:
Hybrid architecture design for (a) prefill & (b) decode, and (c) the integration diagram of HMT plug-in.

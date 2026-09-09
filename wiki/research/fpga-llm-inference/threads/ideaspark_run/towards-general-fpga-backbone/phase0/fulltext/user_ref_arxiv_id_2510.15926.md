# user_ref:arxiv_id:2510.15926

paper_id: user_ref:arxiv_id:2510.15926
tier: U
source_used: html_arxiv
warning: none

## Intro

Large language models (LLMs) have been evolving rapidly, delivering state-of-the-art results in machine translation, code generation, question answering, and conversational AI. Models such as GPT-3
(
brown2020language,
)
, LLaMA
(
touvron2023LLaMA,
)
, and DeepSeek-R1
(
guo2025deepseek,
)
highlight the benefits of scale, but those gains arrive with steep cost increases in computation, memory, and energy.
Deploying LLMs on edge devices (embedded CPUs, GPUs, FPGAs, etc.) preserves privacy, reduces latency, and enables autonomy, yet it is difficult due to tight limits on memory bandwidth and capacity, compute resources, and power budgets. Autoregressive decoding further stresses these constraints: growing key–value (KV) caches, long-context handling, and strict latency requirements often become the dominating performance bottlenecks.
Extreme model compression via low-bit quantization has emerged as a promising technique
(
qiao2022two,
;
10025006,
)
. BitNet
(
bitnet,
;
qiao2025cobra,
;
qiao2025tellme,
)
showed that Transformers can be trained with 1-bit weights; BitNet-1.58
(
bitnet158,
)
and DeepSeek
(
deepseek,
)
extend this idea to ternary quantization (
−
1
,
0
,
+
1
{-1,0,+1}
), approaching full-precision quality while drastically reducing model size and energy. However, closing the gap between algorithmic compression and efficient, end-to-end deployment on actual edge hardware requires a co-design solution that simultaneously optimizes compute, memory, and scheduling.
While researchers have proposed several solutions to accelerate the decoding stage of LLMs, the existing works often ignore the significant latency of the prefill stage, making prefill a critical performance bottleneck in the end-to-end LLM systems.
For example,
(
li2025pushing,
)
demonstrates efficient decoding on embedded FPGAs but leaves the prefill stage largely unaddressed. On device, prefill latency directly impacts users’ perceived responsiveness and safety; it is not hidden behind cloud-scale parallelism.
Therefore, prefill should also be treated as a first-class citizen and carefully accelerated alongside decoding when designing an edge accelerator.
We present
TeLLMe
—the
Te
rnary
L
arge
L
anguage
M
odel
e
dge accelerator—an edge FPGA accelerator, to our knowledge, the first to incorporate a table-lookup (TL) matrix multiplication (MatMul) approach tailored for ternary LLM inference with full support for both
prefill
stage and
decoding
stage. TeLLMe targets cost-effective low-power FPGAs (AMD Kria KV260), supports 1.58-bit (ternary) weights and 8-bit activations, and co-optimizes compute, memory, and scheduling for low-latency, energy-efficient LLM inference.
Prior FPGA accelerators
(
LUTNET,
;
SUMLUTNET,
;
TLMAC,
)
leveraged table-lookup techniques to speed up low-precision arithmetics in other domains, demonstrating the viability of lookup table (LUT)-centric accelerators. However, to our knowledge, TeLLMe is the first to apply a
ternary, table-lookup matmul
design to end-to-end LLM inference (prefill and decoding). Furthermore, it integrates LLM-specific optimizations—fused attention for prefill, disaggregated prefill/decoding dataflows, streaming fusion of dequantization, quantization, element-wise operations, etc., and URAM-aware weight orchestration. With these optimizations, our proposed TeLLMe delivers state-of-the-art efficiency on actual FPGA boards.
Our key contributions include:
•
End-to-end accelerator for ternary LLMs.
We build, to our knowledge, the first edge FPGA accelerator that employs a table-lookup matmul engine for ternary LLMs with full support for both prefill and decoding, achieving up to 25 tokens/s generation throughput and up to 143 tokens/s prefill throughput while consuming under 5 W.
•
Ternary table-lookup matmul.
We propose a table-lookup-based matrix multiplication (TLMM) unit optimized for FPGAs that reuses grouped activations and performs online accumulation for ternary multiplications across attention projections and the feed-forward network (FFN).
•
URAM-aware weight orchestration.
We introduce fine-grained URAM buffering for high-throughput weight streaming from off-chip memory and provide an analytic method to optimize TLMM engine parameter selection under URAM and LUT constraints.
•
Streaming fusion with mixed precision.
We fuse floating-point (FP) dequantization, integer (INT) quantization, and elementwise operations (residual add, rotary embedding, etc) around the INT-based TLMM to enable mixed-precision execution and overlap compute with dataflow architecture.
•
Disaggregated prefill and decoding attention.
We separate the attention pipelines to match their distinct compute/memory patterns. For prefill, we design a fused attention unit with a reversed-attention mechanism and a fully fused pipeline that minimizes off-chip traffic and avoids redundant masked computation. For decoding, we exploit on-chip memory to retain intermediate softmax scores and prevent DDR reloads.
In summary, TeLLMe demonstrates that a LUT/URAM-native, table-lookup matmul engine co-designed with LLM-specific dataflows can unlock end-to-end ternary inference on resource-constrained FPGAs. To our knowledge, it is the first accelerator to realize table-lookup matmul for LLMs with comprehensive support for prefill and decoding on real hardware, establishing a strong baseline for energy-efficient, low-latency generative AI at the edge.

## Method

Figure 2
.
System Architecture of TeLLMe
3.1.
Overview
The technical challenges of ternary LLM implementation on edge FPGA are shown as follows,
❶ Challenge of implementing TLMM for Ternary LLM on FPGA:
The TLMM approach is well-suited for implementing ternary linear operations. However, the current TL-based method on FPGA
(
TLMAC,
;
LOGICNET,
)
focuses solely on TL-based convolution or small-sized perception machine, overlooking its interaction with on-chip and off-chip memory. This interaction is critical for LLMs, which are memory-bound and heavily relying on efficient memory management.
❷ Hardware Support for Mixed-Precision in Low-bit Quantization:
Modern quantization strategies often employ a hybrid-precision approach, where weights and activations are represented with both FP16 (attention, dequant, quant, rotary embedding, etc) and quantized low-bit integers (linear).
Designing a unified hardware architecture that can process these varied data types without incurring significant performance or area overhead is a complex task.
❸ Diverse Computational Patterns in Attention Mechanisms:
The attention mechanism in transformer models exhibits two different computational profiles. The initial
prefill
phase is compute-bound and characterized by parallel processing of the input prompt, while the subsequent
decoding
phase is memory-bound and involves sequential, auto-regressive token generation. A successful FPGA accelerator should efficiently handle both distinct patterns.
The overall Bitnet model architecture is depicted in Fig.
1
, comprising attention computation, linear projections with quantization and dequantization, rotary position embedding (RoPE), RMSNorm, absolute maximum (ABSMAX) quantization, and SwiGLU modules. During the prefill phase, the KV projections are stored in the KV cache, whereas in the decoding phase, the cached KV values are loaded for attention computation.
As illustrated in Fig.
2
, the accelerator architecture comprises the following key modules to address the challenges: (1) a TLMM engine that handles both decoding and prefill passes, integrated with element-wise operations and quantization, referred to as the TLMM-FUSE unit to address ❶, ❷; (2) an on-chip weight buffer management unit (WBMU) that handles the off-chip DDR weight data transfer and accessing of the URAM weight buffer to address ❶; (3) a reversed-reordered prefill attention (RPA) unit that get rid of the redundant attention mask during prefill stage to address ❷, ❸; (4) a decoding attention (DA) unit that match the vector-wise computation in decoding stage to address ❷, ❸; and (5) an RMSNorm unit combined with a find-max operation for supporting the ABSMAX quantization, refered to as RMS-MAX unit to address ❷.
All modules are designed in a dataflow style to enable function-level pipelining. The DDR address ports are bound to distinct MAXI bundles, facilitating independent data streaming from DDR memory. Four temporary address ports are allocated for intermediate storage in DDR. The weight address ports handle weight loading, while the K cache and V cache address ports manage the prefill attention KV return values and decoding attention input values, respectively. The relationship between these modules and the model’s software logic is illustrated in Fig.
1
.
3.2.
Table-Lookup Matmul (TLMM) Engine
3.2.1.
TLMM Engine Design
The TLMM method, illustrated in Fig.
3
, consists of two main stages: offline weight preprocessing and online matrix multiplication. In the offline stage, the ternary weight matrix
𝐖
∈
{
−
1
,
0
,
1
}
n
×
k
{\bf W}\in\{-1,0,1\}^{n\times k}
is partitioned into groups of size
G
G
, which are then encoded into compact indices. This encoding yields
N
TB
=
3
G
N_{\text{TB}}=3^{G}
unique combinations per group, requiring an index bitwidth of
B
idx
=
⌈
log
2
⁡
(
3
G
)
⌉
B_{\text{idx}}=\lceil\log_{2}(3^{G})\rceil
bits.
During the online stage, the matrix-vector product between the activation matrix
𝐀
∈
INT8
m
×
n
{\bf A}\in\text{INT8}^{m\times n}
and the preprocessed weight indices is computed. For each output vector
𝐨
\bf o
, a group of
G
G
INT8 activation values is fetched to dynamically generate a small TL table implemented by distributed RAM. This table is populated by a pre-computation unit of adder/subtractor trees and stores all
N
TB
N_{\text{TB}}
possible partial sums for the current activations, with each entry sized at a bitwidth of
B
TB
=
8
+
⌈
log
2
⁡
G
⌉
B_{\text{TB}}=8+\lceil\log_{2}G\rceil
to prevent overflow. The preprocessed weight indices are then used to look up these partial sums from the TL table. To support the parallel multiple read requests of
Q
Q
of
T
T
TL tables, each TL table has to duplicate
Q
Q
times, resulting in the TL table size of
B
TB
×
N
TB
×
Q
×
T
B_{\text{TB}}\times N_{\text{TB}}\times Q\times T
. Finally, these values are accumulated to produce the output vector
𝐨
∈
INT32
1
×
k
{\bf o}\in\text{INT32}^{1\times k}
, which is pushed into the stream first-in-first-out unit (FIFO) channel for subsequent operations.
To better vectorize the TLMM and facilitate efficient on-chip URAM access, the consecutive
T
T
indices can be grouped into an index vector, enabling simultaneous access to different TL tables. The weight index vector matrix can be rewritten as
𝐖
idx
∈
{
B
idx
,
T
}
n
T
×
G
×
k
{\bf W}_{\text{idx}}\in\{B_{\text{idx}},T\}^{\frac{n}{T\times G}\times k}
.
Figure 3
.
High Level Dataflow of TLMM (
G
=
3
,
T
=
3
,
Q
=
3
G=3,T=3,Q=3
)
Regarding the scheduling in Fig.
3
with
G
=
4
G=4
,
T
=
3
T=3
, and
Q
=
3
Q=3
and the detailed architecture in Fig.
4(a)
, the innermost loop first performs vector operations to establish the
T
T
TL tables through the precompute tree in parallel, based on the first unpacked
T
×
G
T\times G
entries of the
𝐀
\bf A
matrix from the stream FIFO channel. Then, leveraging the multiple reading traits of multiple independent partitioned URAM blocks (array partition strategy and parameter will be detailed in the
3.4
),
Q
Q
𝐰
idx
∈
𝐖
idx
{\bf w}_{\text{idx}}\in{\bf W}_{\text{idx}}
index vectors are processed in parallel for TL table addressing, returning
Q
×
T
Q\times T
outcomes. The corresponding TL table return values are then accumulated in INT32 into an output buffer of size
k
k
. The
k
k
index vectors on each row of
W
W
are traversed in steps of
Q
Q
. The TL table addressing and accumulation process can be fully pipelined with an interval of one cycle, as there are no inter-iteration dependencies. After the first
T
×
G
T\times G
entries of the
𝐀
\bf A
matrix are processed, the
m
m
values of the row of
𝐀
\bf A
are traversed in steps of
T
×
G
T\times G
in the intermediate loop. Finally, the outermost loop traverses the different channels in
𝐀
\bf A
, corresponding to the tokens in the prefill stage of the LLM.
As for the interaction with the weight buffer,
𝐖
idx
{\bf W}_{\text{idx}}
is loaded onto the on-chip URAM in a single pack of DDR loading requests for each ternary linear operation and fully decouple with the computation of TLMM to prevent the compute engine from stalling. Moreover, our TLMM engine supports 3 sizes in the TLMM:
q
,
k
,
v
,
o
q,k,v,o
projection sized
d
model
×
d
model
d_{\text{model}}\times d_{\text{model}}
, up and gate projection in FFN sized
d
model
×
d
ffn
d_{\text{model}}\times d_{\text{ffn}}
, and down projection in FFN sized
d
ffn
×
d
model
d_{\text{ffn}}\times d_{\text{model}}
. This is also supported by the WBMU to convert the high-level address in weight matrices into a physical URAM access address, and additional zero-padding weight indices will be added to support the
T
×
G
T\times G
parallelism and transpose relationship between up and down projection. The detailed architecture will be presented in Sec.
3.4
.
3.2.2.
Comparison between Different Ternary Matrix Multiplication Designs
In general, three methods can be employed to implement TLMM using FPGA fabric.
Method 1 is a naive implementation that employs straightforward selection logic to pass, negate, or zero out the input value based on the ternary weight.
Method 2 partially stores results in a TL table. By exploiting the symmetry of ternary weights (+1, –1), only entries corresponding to positive weights are stored. The number of required entries is given by
N
TB
=
(
3
G
−
1
)
/
2
N_{\text{TB}}=(3^{G}-1)/2
, where
G
G
is the group size and the subtracted unit accounts for the all-zero state. However, to support
T
×
Q
T\times Q
parallel reads, this scheme requires extra logic to identify negative indices and invert the corresponding outputs retrieved from the table.
The third method—our implementation—stores all possible entries in the TL table, totaling
N
TB
=
3
G
N_{\text{TB}}=3^{G}
. This eliminates the need for additional selection logic and enables a purely lookup-based addressing scheme for
T
×
Q
T\times Q
parallel reads.
As for resource analysis, the LUT resources for precomputation can be estimated as
(1)
LUT
PRE
=
T
×
N
TB
×
LUT
tree
,
\displaystyle\text{LUT}_{\text{PRE}}=T\times N_{\text{TB}}\times\text{LUT}_{\text{tree}},
where the
LUT
tree
\text{LUT}_{\text{tree}}
is the average LUT utilized in each output of the precomputation tree.
The size of the TL table is formulated as
(2)
LUT
TB
=
T
×
Q
×
N
TB
×
LUT
entry
,
\displaystyle\text{LUT}_{\text{TB}}=T\times Q\times N_{\text{TB}}\times\text{LUT}_{\text{entry}},
where
LUT
entry
\text{LUT}_{\text{entry}}
is the number of LUTs needed to store one entry in TL table. The lookup logic LUT consumption is given by
(3)
LUT
LPL
=
T
×
Q
×
LUT
lp
,
\displaystyle\text{LUT}_{\text{LPL}}=T\times Q\times\text{LUT}_{\text{lp}},
where
LUT
lp
\text{LUT}_{\text{lp}}
represents the LUT cost of a single lookup, its associated conversion logic, and reduction logic.
In the highly parallel
T
×
Q
T\times Q
lookups in Methods 2, the dominant factor is
LUT
LPL
\text{LUT}_{\text{LPL}}
, since the
N
TB
×
LUT
entry
N_{\text{TB}}\times\text{LUT}_{\text{entry}}
is efficiently implemented using the distributed RAM architecture of primitives such as cascaded RAM32X1
(
AMD_UG974_ultrascale,
)
. These argument are further validated in the ablation study Sec.
4.4.1
.
(a)
Detailed Design of TLMM-FUSE Unit
(b)
Mem. Dependency of Different RoPE
(c)
Dataflow Overlapping
Figure 4
.
Overview of TLMM hardware components and dataflow. (a) The TLMM-FUSE unit design. (b) The comparison of different RoPE operations. (c) The dataflow execution schedule.
3.3.
Fused Element-wise Operations
Element-wise operations are computations performed on input tensors where each entry or entry pair is consumed only once. Within the Bitnet architecture, several such operations are critical: (1) quant from FP16 to INT8 and subsequent dequant from INT32 to FP16; (2) the channel-wise maximums for ABSMAX quantization; (3) the RoPE operator; (4) element-wise additions for residual connections; (5) element-wise multiplications in SwiGLU; and (6) the activation functions.
Previous research on LLM accelerators has overlooked the performance impact of these operations, often deeming them negligible
(
moitra2025meadow,
)
. In practical deployments, however, these operators can create performance bottlenecks, constraining the model’s overall latency and resource utilization. This issue is acute in quantized modules, which involve a mix of efficient high-throughput INT computations and demanding FP operations.
To address the above challenges, we introduce a specialized fusion unit designed to overlap the latency of these element-wise computations with the core TLMM operations, thereby optimizing execution efficiency. Moreover, a vector-wise operation is implemented to make sure we match the throughput of TLMM under resource constraints of DSP and LUT when designing FP operators. The detailed streaming pattern and datapath are displayed in Fig.
4(a)
. The stream FIFO channels are in grey color with the type of vector it is buffering.
3.3.1.
INT8 Quantization and FP16 Dequantization
To seamlessly fuse quantization with linear operations, a stream FIFO channel connects the respective functional units. To maximize data throughput, all FP16 values are packed into 256-bit vectors, each holding 16 elements. This vectorization enables parallel computation and efficient 256-bit wide AXI access to DDR memory. The quantization process involves a data-width transformation, converting these 16-element FP16 vectors into
T
×
G
T\times G
INT8 vectors for the TLMM input FIFO, which necessitates stream resizing logic. Conversely, dequantization performs vectorized multiplication operations on the 16-element INT32 vectors to convert them to FP16 precision.
3.3.2.
Elementwise Activation-fused Multiplication and Addition
The element-wise multiplication with SILU, element-wise addition, and RoPE operations are all performed in floating-point precision following dequantization. Both these three operations and bypass logic are implemented in TLMM-FUSE as displayed in Fig.
4(a)
with an arbitrary unit deciding which submodule the stream FIFO flow in. As shown in Fig.
1
, the element-wise multiplication is an integral component of the SwiGLU. This function operates on the outputs of the gate and up projections: the gate projection’s output is first processed by a SILU activation, and the result is then multiplied element-wise with the up projection’s output. The element-wise addition is applied immediately before the RMSNorm layer to incorporate the residual connection.
3.3.3.
RoPE Operation
For the RoPE implementation, we assume the necessary sinusoidal values are pre-computed and stored in DDR, as generating them on-the-fly would be resource- and time-intensive. The core RoPE function operates on a vector
𝐱
∈
FP16
d
h
\mathbf{x}\in\text{FP16}^{d_{h}}
by applying a rotation to pairs of elements. The mathematical formulation of the two implementations differs only in how the vector indices are grouped for these rotations:
(4)
{
x
~
m
(
2
​
t
)
=
x
m
(
t
)
​
cos
⁡
(
m
​
θ
t
)
−
x
m
(
t
+
d
h
/
2
)
​
sin
⁡
(
m
​
θ
t
)
x
~
m
(
2
​
t
+
1
)
=
x
m
(
t
+
d
h
/
2
)
​
cos
⁡
(
m
​
θ
t
)
+
x
m
(
t
)
​
sin
⁡
(
m
​
θ
t
)
\begin{cases}\tilde{x}_{m}^{(2t)}=x_{m}^{(t)}\cos(m\theta_{t})-x_{m}^{(t+d_{h}/2)}\sin(m\theta_{t})\\
\tilde{x}_{m}^{(2t+1)}=x_{m}^{(t+d_{h}/2)}\cos(m\theta_{t})+x_{m}^{(t)}\sin(m\theta_{t})\par\end{cases}
(5)
{
x
~
m
(
2
​
t
)
=
x
m
(
2
​
t
)
​
cos
⁡
(
m
​
θ
t
)
−
x
m
(
2
​
t
+
1
)
​
sin
⁡
(
m
​
θ
t
)
x
~
m
(
2
​
t
+
1
)
=
x
m
(
2
​
t
+
1
)
​
cos
⁡
(
m
​
θ
t
)
+
x
m
(
2
​
t
)
​
sin
⁡
(
m
​
θ
t
)
\begin{cases}\tilde{x}_{m}^{(2t)}=x_{m}^{(2t)}\cos(m\theta_{t})-x_{m}^{(2t+1)}\sin(m\theta_{t})\\
\tilde{x}_{m}^{(2t+1)}=x_{m}^{(2t+1)}\cos(m\theta_{t})+x_{m}^{(2t)}\sin(m\theta_{t})\end{cases}
where
0
≤
t
<
d
h
/
2
0\leq t<d_{h}/2
,
m
m
is the position, and the frequency basis
θ
t
=
10000
−
2
​
t
/
d
h
\theta_{t}=10000^{-2t/d_{h}}
.
As illustrated in Fig.
4(b)
, the canonical LLaMA architecture
(
HuggingFaceLLaMAGithub,
)
employs the interleaved pairing from eq.
4
. Although this pattern aligns well with the highly parallel and flexible memory systems of GPUs, it is fundamentally mismatched with streaming hardware architectures. In our FPGA-based streaming design, data flows through a function-level pipeline via FIFOs. The non-contiguous access pattern required by the interleaved pairing would force the pipeline to stall while buffering and gathering all elements for a given head.
By contrast, the consecutive pairing from eq.
5
applied to data within a packed-vector is more hardware-friendly. This approach simplifies data access, reduces FIFO dependencies, and enables a lower initiation interval. To preserve mathematical equivalence with the LLaMA-style implementation while leveraging the benefits of consecutive access, a lossless transformation is necessary for query and key weight matrices. This transformation, applied on a per-head basis, follows the index exchange formula below, which converts the weight organization from the interleaved to the consecutive pattern:
(6)
{
𝐰
N
h
(
2
​
t
)
⇔
𝐰
N
h
(
t
)
𝐰
N
h
(
2
​
t
+
1
)
⇔
𝐰
N
h
(
d
h
/
2
+
t
)
for
​
0
≤
t
<
d
h
2
.
\displaystyle\begin{cases}\mathbf{w}_{N_{h}}^{(2t)}\Leftrightarrow\mathbf{w}_{N_{h}}^{(t)}\\
\mathbf{w}_{N_{h}}^{(2t+1)}\Leftrightarrow\mathbf{w}_{N_{h}}^{(d_{h}/2+t)}\end{cases}\quad\text{for }0\leq t<\frac{d_{h}}{2}.
3.4.
Weight Buffer Management Unit (WBMU)
3.4.1.
Analytical Parameter Selection for TLMM based on Optimal URAM Utilization
In the design of LLM accelerators, external memory access for weights is a critical performance bottleneck, often dominating the latency of the decoding phase. This challenge is acute on edge FPGAs, where on-chip memory resources are limited. Among these resources, URAM is ideal for buffering large weight tensors.
Insufficient on-chip buffer capacity for weights leads to significant performance degradation. When the required weights cannot be stored on-chip URAM, the system must repeatedly access off-chip memory via the AXI bus, which will be severely limited by the low DDR bandwidth of the edge FPGA.
Therefore, this work proposes an analytical model for optimizing URAM utilization by selecting the relevant TLMM parameters. This model provides a systematic approach to designing the on-chip weight buffer and TLMM accelerators, ensuring optimal parameter selection for both modules within the memory constraints of edge devices.
As introduced by the
(
AMD_UG573_ultrascale_memory,
)
, the size of the URAM resource is set as 72 bitwidth
×
\times
4096 depth, which can equal up to 16 BRAM18K blocks. However, due to its fixed bitwidth of 72, the design of storage architecture is vital. We assume there are
N
URAM
N_{\text{URAM}}
URAM blocks in total in an edge FPGA. The total URAM memory size is
288
​
K
​
b
×
N
URAM
288Kb\times N_{\text{URAM}}
. In our design, each of the units saves a weight index vector
𝐰
𝐢𝐝𝐱
∈
𝐖
𝐢𝐝𝐱
\bf{w}_{idx}\in\bf{W}_{idx}
and the bit width is
T
×
B
idx
T\times B_{\text{idx}}
. On one hand, our goal is to have a TL table as large as possible within the resource limitations; on the other hand we want to make sure the bitwidth of URAM is fully utilized. Thus, the largest number of TL table
T
T
is set according to
(7)
T
=
⌈
72
×
c
URAM
B
idx
⌉
,
\displaystyle T=\left\lceil\frac{72\times c_{\text{URAM}}}{B_{\text{idx}}}\right\rceil,
where the factor
c
URAM
c_{\text{URAM}}
stands for the cascade factor that combine
c
URAM
c_{\text{URAM}}
URAM together to get a larger bitwidth. The
T
T
is also confined by the available LUT resource to ensure place and route to implement the TLMM. The number of LUT can be utilized for TLMM is
LUT
max
\text{LUT}_{\text{max}}
. According to Sec.
3.2.2
, the constraint can be given by
(8)
T
×
(
N
TB
×
LUT
tree
+
Q
×
N
TB
×
LUT
entry
+
Q
×
LUT
lp
)
≤
LUT
max
,
\begin{split}T\times(N_{\text{TB}}\times\text{LUT}_{\text{tree}}+Q&\times N_{\text{TB}}\times\text{LUT}_{\text{entry}}\\
&+Q\times\text{LUT}_{\text{lp}})\leq\text{LUT}_{\text{max}},\end{split}
Moreover, to enable the parallel read of
Q
Q
trait, we will try to partition the target buffer array size of
X
URAM
×
Y
URAM
X_{\text{URAM}}\times Y_{\text{URAM}}
to ensure the above memory banks are independent.
Since each URAM is a dual-port memory
(
AMD_UG573_ultrascale_memory,
)
, we partition the weight matrix cyclically with a factor of
Q
/
2
Q/2
. This strategy ensures that
Q
Q
consecutive elements are placed in independent blocks, enabling parallel access.
These logical blocks are then mapped to physical URAMs based on the memory depth. The total number of utilized URAMs
U
U
can be given as:
(9)
U
=
⌈
(
Y
URAM
Q
)
×
⌈
X
URAM
G
×
T
⌉
4096
⌉
×
c
URAM
×
Q
2
,
U
≤
N
URAM
,
\displaystyle U=\left\lceil\frac{(\frac{Y_{\text{URAM}}}{Q})\times\lceil\frac{X_{\text{URAM}}}{G\times T}\rceil}{4096}\right\rceil\times c_{\text{URAM}}\times\frac{Q}{2},\quad U\leq N_{\text{URAM}},
where the term wrapped by the ceil gives the depth required in total for a single partitioned array,
c
URAM
c_{\text{URAM}}
is the cascade factor to build the required bitwidth, and there are
Q
/
2
Q/2
blocks in total.
3.4.2.
TLMM Weight Accessing
Figure 5
.
The WBMU and AXI data packing strategy. The green arrows denote the connection to the weight access, and the yellow arrows are connected to the weight load module.
A key challenge is supporting the various TLMM dimensions presented in Sec.
3.2.1
. The first two matmul types share the dimension
n
=
d
model
n=d_{\text{model}}
, so adapting to them primarily involves controlling memory access along the
k
k
-dimension.
However, a complication arises because the weight matrices for the up- and down-projections are transposes of each other, and the address stride is supposed to be different. Furthermore, the dimension
d
ffn
d_{\text{ffn}}
is not necessarily an even multiple of
d
model
d_{\text{model}}
. This dimensional mismatch prevents aligned memory access, which would necessitate complex logic to handle unaligned weight indices access. To resolve this, we pad the weight buffers to make their dimensions evenly divisible, thereby ensuring all memory accesses are aligned.
Moreover, the logical dimensions
d
ffn
d_{\text{ffn}}
and
d
model
d_{\text{model}}
are padded to be multiples of
T
×
G
T\times G
, resulting in the dimensions
d
ffn
′
d_{\text{ffn}}^{\prime}
and
d
model
′
d_{\text{model}}^{\prime}
. Therefore,
X
URAM
=
d
FFN
′
X_{\text{URAM}}=d^{\prime}_{\text{FFN}}
and
Y
URAM
=
d
model
′
Y_{\text{URAM}}=d^{\prime}_{\text{model}}
.
The WBMU contains an address translation unit that converts a straightforward 2D software weight matrix index
(
a
,
b
)
(a,b)
into a 3D-indexed physical address
(
x
,
y
,
z
)
(x,y,z)
. This scheme treats the cyclically partitioned URAM array as a single, contiguous address space for simplified indexing explanation. Its array size is configured as [
⌈
d
ffn
′
d
model
′
⌉
\left\lceil\frac{d_{\text{ffn}}^{\prime}}{d_{\text{model}}^{\prime}}\right\rceil
,
d
model
′
(
T
×
G
)
\frac{d_{\text{model}}^{\prime}}{(T\times G)}
,
d
model
d_{\text{model}}
]. With weight index request
1
≤
a
,
b
≤
d
ffn
1\leq a,b\leq d_{\text{ffn}}
from TLMM engine, the address mapping is given by:
(10)
{
x
=
{
0
,
q, k, v, o projection
b
d
model
,
Up projection
a
d
model
′
,
Down projection
y
=
a
mod
d
model
′
,
z
=
b
mod
d
model
,
.
\begin{cases}x=\begin{cases}0,&\text{q, k, v, o projection}\\
\frac{b}{d_{\text{model}}},&\text{Up projection}\\
\frac{a}{d_{\text{model}}^{\prime}},&\text{Down projection}\\
\end{cases}\\
y=a\mod d_{\text{model}}^{\prime},\quad z=b\mod d_{\text{model}},\\
\end{cases}.
3.4.3.
Off-chip DDR Weight Transfer
As illustrated in Fig.
5
, the WBMU connects to the DDR memory system via three high performance (HP) ports: HP0, HP1, and HP3. The AXI interface for these ports is configured with a 256-bit data width, a burst size of 16, and an outstanding transaction limit of 16, following the guidelines in
(
Benchmark_AXI_ON_ZYNQ,
)
.
During weight loading, the three HP ports transmit data in parallel, as each is connected to an independent DDR Quality of Service (QoS) channel as shown in Fig.
2
. This parallelism results in a combined bandwidth of 768 bits per AXI access cycle. As shown in Fig.
5
(b), each 768-bit transfer is structured to carry
⌈
(
768
−
16
)
/
(
T
×
B
)
⌉
\lceil(768-16)/(T\times B)\rceil
𝐰
idx
{\bf w}_{\text{idx}}
and one FP16 RMSNorm weight. In our design, with parameters
T
=
28
T=28
and
B
=
5
B=5
, a single pipelined burst request can convey up to five weight index vectors and one RMSNorm weight in one transfer out of 16 burst AXI data.
3.5.
RMS-MAX Unit
The RMS-MAX hardware unit performs RMS normalization followed by channel-wise maximum finding for subsequent quantization and dequantization. Input data undergoes RMSnorm accumulation with upcasting to FP32 for precision, succeeded by FP16 division and FP16 RMSnorm weight scaling to compute the norm. A stream FIFO channel interfaces the RMSnorm output with the channel-wise max finding module: vector-wise maximums are first extracted per channel segment, and upon completion of the final channel flow, the global channel maximum is identified and stored in a dedicated buffer for quant/dequant operations. By decoupling the max-finding and quantization logic, memory dependencies are eliminated in computing the final quantized output. Furthermore, max-finding can proceed concurrently with vector-wise output FIFO due to their strictly sequential nature.
(a)
Schedule on the Attention Score Map (
N
pe
=
4
N_{\text{pe}}{=}4
)
(b)
Naive Attention Scheduling (
N
pe
=
4
N_{\text{pe}}{=}4
)
(c)
Reverse Attention Scheduling (
N
pe
=
4
N_{\text{pe}}{=}4
)
Figure 6
.
Attention Schedules Comparison
3.6.
Reversed Prefill Attention Unit
3.6.1.
Prefill Attention Challenge on edge FPGAs
The prefill attention of LLM requires significant resources and bandwidth for multi-token computation at the sequence length of
N
N
, especially for attention computation, which involves softmax and matrix-to-matrix multi-head operations with a complexity of
N
2
N^{2}
. Given the limited memory bandwidth and finite computational units of DSP for FP operation on edge FPGAs, the computation order of prefill attention should be carefully scheduled to meet these requirements. Otherwise, it may be constrained by the bandwidth limitations of the edge FPGA, as shown in the naive attention scheduling in Fig.
6(b)
(
edgemoe,
)
. When we have
N
pe
N_{\text{pe}}
processing elements (PEs), the bandwidth requirement will be
N
pe
N_{\text{pe}}
as well. The more PE we have, the larger the amount of data will be required from DDR, bounded by the total bandwidth.
Furthermore,
N
×
N
×
N
head
N\times N\times N_{\text{head}}
elements are stored back to DDR and loaded on chip as the softmax matrix
𝐒
\bf S
.
The fusion of operations such as
𝐐𝐊
T
{\bf Q}{\bf K}^{\text{T}}
, softmax, and
𝐒𝐕
\bf S{\bf V}
can reduce the additional accesses to DDR. The state-of-the-art kernel fusion implementation for resource-abundant GPUs is Flash Attention
(
dao2022flashattentionfastmemoryefficientexact,
)
. However, GPU-optimized computation is not suitable for FPGAs, as GPUs have many more computational cores and much larger on-chip SRAM compared to the on-chip BRAM/URAM available on FPGAs. To address these challenges, we propose the reverse attention method, which utilizes fused attention and reverse reorder scheduling, specifically tailored for edge FPGAs.
Figure 7
.
Design of Fused Attention at Iteration Step 4 (
N
PE
=
4
N_{\text{PE}}=4
)
Figure 8
.
Detailed Design of Decoding Attention
3.6.2.
Reversed and Fused Attention
The reverse attention scheduling is depicted in Fig.
6(c)
. Assume that the current sequence length of the prefill tokens is
N
N
, with
1
<
i
≤
N
1<i\leq N
and
1
<
j
≤
N
1<j\leq N
representing the current token indices for
𝐪
{\bf q}
and
𝐤
,
𝐯
{\bf k},{\bf v}
, respectively. There are a total of
N
h
N_{{\text{h}}}
heads. The operator of
𝐪𝐤𝐯
\bf{qkv}
denotes the fused operation.
The kernel fusion computation can be considered a special case of Flash Attention V2
(
dao2022flashattentionfastmemoryefficientexact,
)
when the block size is equal to 1. The head-wise formula for the case with two consecutive blocks can be written as follows:
(11)
{
s
(
i
)
=
𝐪
i
​
𝐤
i
T
d
h
,
m
(
i
)
=
max
⁡
(
m
(
i
−
1
)
,
s
(
i
)
)
ℓ
(
i
)
=
e
m
(
i
−
1
)
−
m
(
i
)
​
ℓ
(
i
−
1
)
+
e
s
(
i
)
−
m
(
i
)
𝐨
(
𝐢
)
=
e
m
(
i
−
1
)
−
m
(
i
)
​
𝐨
(
i
−
1
)
+
e
s
(
i
)
−
m
(
i
)
​
𝐯
i
\vskip-5.69054pt\left\{\small\begin{aligned} s^{(i)}&=\frac{{\bf q}_{i}{\bf k}^{\text{T}}_{i}}{\sqrt{d_{\text{h}}}},m^{(i)}=\max\left(m^{(i-1)},s^{(i)}\right)\\
\ell^{(i)}&=e^{m^{(i-1)}-m^{(i)}}\ell^{(i-1)}+e^{s^{(i)}-m^{(i)}}\\
\bf{o}^{(i)}&=e^{m^{(i-1)}-m^{(i)}}{\bf o}^{(i-1)}+e^{s^{(i)}-m^{(i)}}{\bf v}_{i}\end{aligned}\right.
where
m
(
i
)
m^{(i)}
denotes the running maximum value,
s
(
i
)
s^{(i)}
represents the dot product score,
ℓ
(
i
)
\ell^{(i)}
is the denominator factor, and
𝐨
(
i
)
{\bf o}^{(i)}
is the numerator vector. After all inputs have been processed (up to step N), the final attention output is computed as the division of the final numerator by the final denominator
𝐨
(
i
)
/
ℓ
(
i
)
{\bf o}^{(i)}/\ell^{(i)}
.
Compared to a naive implementation, this online algorithm avoids generating the large intermediate attention score matrix
𝐒
\bf S
, saving significant off-chip DDR access. It also breaks the data dependency on finding a global maximum value, which enables streaming computation and operation fusion.
Regarding detailed schedule, instead of starting from the first token
𝐪
1
{\bf q}_{1}
, our schedule begins from
𝐪
N
−
1
{\bf q}_{N-1}
. Specifically, the level of parallelism is set to
N
pe
N_{\text{pe}}
. The factor
N
pe
N_{\text{pe}}
also implies that the PE buffer can store
N
pe
N_{\text{pe}}
tokens of
𝐪
i
{\bf q}_{i}
. In each iteration, one
𝐪
i
{\bf q}_{i}
token is loaded onto the buffer of PEs with unicast (with the first batch loading
𝐪
N
{\bf q}_{N}
to
𝐪
N
−
3
{\bf q}_{N-3}
). Simultaneously, the corresponding
𝐤
j
{\bf k}_{j}
and
𝐯
j
{\bf v}_{j}
tokens are loaded to PEs in multicast. After all
N
N
𝐤
j
{\bf k}_{j}
and
𝐯
j
{\bf v}_{j}
tokens have been loaded and the fused-kernel computation is completed, the next iteration will evict
N
pe
N_{\text{pe}}
𝐤
j
{\bf k}_{j}
and
𝐯
j
{\bf v}_{j}
tokens, starting from
𝐤
N
−
3
{\bf k}_{N-3}
and
𝐯
N
−
3
{\bf v}_{N-3}
, to avoid redundant computations arising from the causal attention mask. Once all computation with regard to the loaded
𝐪
\bf q
s is completed, the
𝐨
(
i
)
/
ℓ
(
i
)
,
i
=
N
​
to
​
N
−
3
{\bf o}^{(i)}/\ell^{(i)},i=N\text{ to }N-3
for all heads are pushed to the as consecutive heads consist the hidden dimension. The microarchitecture state at step 4 is depicted in Fig.
7
. Each PE is divided into a head-wise multiplication and accumulation (MAC) unit, a rescale and accumulation unit for the output vector and denominator factor, and a final division and output unit.
The iteration continues until all
1
<
i
≤
N
1<i\leq N
,
1
<
j
≤
N
1<j\leq N
are traversed. In this approach, the only required input buffers are for
N
pe
N_{\text{pe}}
𝐪
i
{\bf q}_{i}
tokens, one
𝐤
j
{\bf k}_{j}
, and one
𝐯
j
{\bf v}_{j}
. Additionally, the intermediate buffers of the
N
h
N_{h}
heads include:
N
h
×
N
pe
N_{h}\times N_{\text{pe}}
multi-head MAC intermediate results
s
s
,
N
h
×
N
pe
N_{h}\times N_{\text{pe}}
multi-head previous max values
m
m
,
N
h
×
N
pe
N_{h}\times N_{\text{pe}}
intermediate denominators
ℓ
\ell
, as well as the output vector
𝐨
\bf o
buffer sized
d
model
×
N
pe
d_{\text{model}}\times N_{\text{pe}}
. The trade-off also includes minor computational overhead: an additional exponentiation,
e
m
(
i
−
1
)
−
m
(
i
)
e^{m^{(i-1)}-m^{(i)}}
, is required to rescale previous results when the running maximum is updated. Additionally, the state of the running numerator
𝐨
\bf{o}
and denominator
ℓ
\ell
are maintained with two extra floating point rescales.
To support the reverse reorder in the prefill stage, the embedding vectors are indexed by the reversed input prompt reordered token id, and the rope cache is also reversed. In this way, the RPA can be seamlessly utilized without extra reversed address DDR access logic that is not supported by the AXI address incremental burst access protocol
(
amd_ug1037,
)
. The advantage of the reversed attention is further proved in Sec.
4.4.2
.
3.7.
Decode Attention Unit
The computational characteristics of attention differ between prefill and decoding phases. The computation in the decoding phase attention involves primarily matrix-vector and vector-vector operations. The computational load per step
O
​
(
N
​
d
model
)
O(Nd_{\text{model}})
is significantly lower than the total matmul in prefill attention,
O
​
(
N
2
​
d
model
)
O(N^{2}d_{\text{model}})
. However, this phase requires fetching the large
𝐊
cache
{\bf K}_{\text{cache}}
and
𝐕
cache
{\bf V}_{\text{cache}}
matrices from memory (e.g., off-chip DDR) in every layer. Consequently, the decoding phase is often memory-bandwidth bound, especially as the sequence length
N
N
grows.
This heterogeneity of these workloads necessitates a system-level balance between performance and resource utilization to achieve optimal end-to-end efficiency.
For decoding attention, the marginal benefits of adding extra compute resources diminish compared with prefill attention. To address this, we decouple the fusion between
𝐐𝐊
T
\bf{QK^{\text{T}}}
multiplication (fetch
𝐊
c
​
a
​
c
​
h
​
e
{\bf K}_{cache}
) and the weighted aggregation with
𝐕
{\bf V}
(fetch
𝐕
c
​
a
​
c
​
h
​
e
{\bf V}_{cache}
), since these two operations are dominated by memory access.
Fig.
8
illustrates the hardware architecture of our decoding attention design. The query input
Q
(single token) is pre-loaded on-chip, while the
𝐊
cache
{\bf K}_{\text{cache}}
and
𝐕
cache
{\bf V}_{\text{cache}}
is loaded from off-chip DDR via AXI interface. We utilize a stream-like dataflow within the module to conceal the computation latency. We use an online softmax algorithm that partially fuses the softmax with
𝐐𝐊
T
\bf{QK^{\text{T}}}
vector-matrix multiplication. The intermediate attention score is stored in the on-chip stream buffer, so no off-chip memory access is required in softmax computation.
Table 1
.
Unified cross-platform and FPGA-based comparison for edge LLM inference. Resource utilization is reported for FPGA works. Throughput (TK/S) is tokens per second; energy efficiency (TK/J) is tokens per joule. Max DDR bandwidths are theoretical.
Work
Platform
Processor
Model
Precision
Max DDR Bandwidth(GB/s)
FPGA Resource Utilization
Power (W)
Throughput (TK/S)
Energy Efficiency (TK/J)
LUT
FF
DSP
BRAM
URAM
Prefill
Decode
Prefill
Decode
Raspberry Pi 5
(
adafruit2025qwen3,
)
SoC
4
×
4\times
Cortex-A76
Qwen 0.6B
W4-A16
17.1
—
—
—
—
—
7.8
61.8
16.6
7.92
2.12
Jetson Orin Nano
(
jetsonailab2025slm,
)
GPU SoC
8
×
8\times
GPU SM
TinyLLaMA 1.1B
W4-A16
68.3
—
—
—
—
—
25
324.9
67.6
12.9
2.70
SECDA
(
haris2024designing,
)
FPGA SoC
2
×
2\times
Cortex-A53
TinyLLaMA 1.1B
W4-A16
2.1
—
—
—
—
—
—
—
0.6
—
—
LLaMAF
(
LLaMAf,
)
FPGA SoC
ZCU102
TinyLLaMA 1.1B
W8-A8
19.2
164K
171K
528
223
—
5.1
—
1.5
—
0.29
MEADOW
(
moitra2025meadow,
)
FPGA SoC
ZCU102
OPT 1.3B
W8-A8
19.2
150K
—
845
2034
—
10
100
2
10
0.20
TeLLMe (KV260)
FPGA SoC
—
BitNet 0.73B
W1.58-A8
17.1
98K
137K
610
98.5
60
4.8
143
25
29.8
5.2
Table 2
.
Perplexity and Intelligence/J comparison on WikiText-2. Intelligence/J is defined as
t
​
o
​
k
​
e
​
n
​
s
/
s
(
P
​
P
​
L
⋅
P
​
o
​
w
​
e
​
r
)
\frac{tokens/s}{(PPL\cdot Power)}
(
tenent,
)
. Throughput (TK/S) is tokens per second.
Work & Platform
Model
Power (W)
WT-2 (PPL)
Throughput (TK/S)
Intelligence/J
Prefill
Decode
Prefill
Decode
Raspberry Pi 5
Qwen 0.6B
7.8
24.00
61.8
16.6
0.330
0.089
Jetson Orin Nano
TinyLLaMA 1.1B
25.0
12.42
324.9
67.6
1.046
0.218
SECDA (Pynq)
TinyLLaMA 1.1B
1.2
12.42
—
0.6
—
0.040
LLaMAF (ZCU102)
TinyLLaMA 1.1B
5.1
8.89
—
1.5
—
0.041
MEADOW (ZCU102)
OPT 1.3B
10.0
15.41
100.0
2.0
0.649
0.013
TeLLMe (KV260)
BitNet 0.73B
4.8
12.79
143
25
2.330
0.407

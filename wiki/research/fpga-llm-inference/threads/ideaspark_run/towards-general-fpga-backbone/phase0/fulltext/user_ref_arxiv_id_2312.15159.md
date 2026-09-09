# user_ref:arxiv_id:2312.15159

paper_id: user_ref:arxiv_id:2312.15159
tier: U
source_used: html_arxiv
warning: none

## Intro

The rapid advancement of Transformer-based large language models (LLMs)
(
vaswani2017transformer,
;
rishi2021foundation,
)
has sparked a revolution across a wide range of natural language processing tasks, such as conversational AI
(
openai2023gpt4,
;
zheng2023chatbotarena,
;
cohen2022lamda,
)
and code generation
(
chen2021codex,
;
li2022alphacode,
;
nijkamp2023codegen,
)
. Recent research has brought to light the phenomenon of “emergence” in LLMs, where advanced capabilities become evident as the models scale up to billions of parameters
(
wei2022emergence,
;
wei2022cot,
)
.
However, supporting this unprecedented scale poses significant challenges, particularly in terms of computational and memory resources.
At the same time, the increasing use of LLMs in interactive applications like voice assistants and autonomous systems requires hardware accelerators capable of providing both low latency and high energy efficiency
(
openai2023gpt4,
;
driess2023palme,
;
pope2022googleinf,
)
.
Recent efforts have primarily focused on improving the performance of LLM inference on GPUs
(
aminabadi2022dsinf,
;
fastertransformer2022,
)
, although GPUs are known for their high power consumption and are less suitable for latency-sensitive workloads
(
kim2023survey,
;
pope2022googleinf,
)
. There is also an active body of research dedicated to developing specialized hardware accelerators tailored for Transformer models, with several of these efforts using FPGAs as the target platforms
(
hong2022dfx,
;
liu2021fqbert,
;
li2020ftrans,
;
peng2021cbbp,
;
hur2023flexrun,
;
qi2021iccad,
)
.
(a)
Temporal architecture (i.e., overlay).
(b)
Partially unfolded spatial architecture with two PEs.
(c)
Fully unfolded spatial architecture with four PEs.
Figure 1
.
Temporal and spatial architectures — PE stands for processing engine;
f
1
subscript
𝑓
1
f_{1}
italic_f start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT
-
f
4
subscript
𝑓
4
f_{4}
italic_f start_POSTSUBSCRIPT 4 end_POSTSUBSCRIPT
represent different operators in the model.
FPGA-based LLM accelerators can be broadly categorized into two architectural paradigms:
temporal architecture
and
spatial architecture
.
In a temporal architecture, a processing engine (PE) capable of performing various tasks is constructed and reused across different layers and models, as shown in Figure
1
(a). For flexibility, these accelerators typically employ an overlay approach
(
hong2022dfx,
;
li2020ftrans,
;
khan2021npe,
)
, where a virtual hardware architecture that executes instructions is “laid” on top of the physical FPGA fabric. Overlays provide a more restricted configuration space, allowing for quicker compilation with bitstream reuse across multiple models. However, the use of such temporal architecture requires more frequent off-chip memory access, as intermediate results must be written back to memory. This incurs a cost in terms of both latency and energy consumption that is significantly higher than direct on-chip memory access. Additionally, one could argue that an FPGA overlay will inherently be less efficient than its hardened ASIC counterpart.
In contrast, an FPGA-based spatial architecture typically involves the specialization of distinct PEs for specific operators or layers, facilitating direct communication between them using streaming buffers (e.g., FIFOs or multi-buffers)
(
xiang2022heteroflow,
;
wang2021autosa,
;
yaman2017finn,
;
petrica2020dataflowcnn,
)
, as depicted in Figure
1
(b-c).
This dataflow-style execution substantially reduces off-chip memory accesses and enables the concurrent processing of multiple PEs in a pipelined manner.
Moreover, the fine-grained programmability of FPGAs allows efficient support of model-specific spatial architectures, which can further leverage efficiency optimizations such as low-bitwidth quantization, custom numerical types, and sparsity
(
zhang2021fracbnn,
;
sun2022autovit,
;
yang2023aim,
;
peng2022sparsefpga,
)
. These capabilities can potentially enable highly efficient LLM inference implementations that surpass GPUs, especially in small-batch low-latency scenarios.
However, implementing a spatial architecture for LLM inference presents significant challenges.
Challenge 1: Navigating diverse parallelism in LLMs.
The generative inference process of LLMs typically consists of two distinct stages: (1) simultaneously processing user prompts and (2) sequentially generating new tokens in an autoregressive manner.
These two stages exhibit significantly different computational and memory characteristics (detailed in §
3
), making it necessary to tailor hardware accelerators for their specific needs.
This challenge cannot be directly addressed by leveraging techniques from the traditional convolutional neural network (CNN) designs
(
kim2023survey,
;
zhang2015cnnfpga,
)
.
The large number of parameters and intermediate tensors further complicates the choice between on-chip and off-chip storage.
Additionally, harnessing multiple accelerators for distributed LLM inference adds complexity, particularly when dealing with intricate parallelization schemes
(
shoeybi2019megatron,
;
narayanan2019pipedream,
;
hong2022dfx,
)
.
Challenge 2: Lack of standard LLM building blocks in hardware accelerators.
The rapid evolution of LLM architectures
(
rishi2021foundation,
;
openai2023gpt4,
;
touvron2023llama,
)
contrasts with the comparatively slow pace of hardware development.
While a plethora of building blocks for Transformers have been proposed in the software domain
(
xFormers2022,
;
dao2022flashattention,
;
kernl2022,
)
, the absence of reusable blocks for hardware accelerator design hampers development progress.
Many frameworks have been designed to automatically map deep learning models to FPGAs
(
zhang2018dnnbuilder,
;
yaman2017finn,
;
fahim2021hls4ml,
;
suhail2023flexcnn,
;
zhang2020dnnexplorer,
)
, but they are constrained to small CNN designs and lack support for complicated Transformer models.
It is also hard to scale their designs to accommodate large models and multi-die FPGAs.
To tackle these challenges,
this paper is to provide a comprehensive set of hardware design considerations for LLMs and try to answer the following question:
What role can FPGA-based spatial accelerators play in enabling efficient LLM inference?
We start by conducting an in-depth analysis of the computational and memory requirements associated with each operator within Transformer models across two distinct stages of LLM generative inference – prefill and decode.
Subsequently, we extend our analysis to reveal the potential benefits of distributed inference using multiple FPGAs.
We believe that providing such an analysis, rather than presenting only positive results in selectively chosen settings for an FPGA LLM accelerator, offers more valuable insights to the community.
To validate the feasibility of our analytical framework, we implement a specific design point and demonstrate its viability.
Leveraging this analytical framework, we employ specific optimizations in HLS to craft each kernel and compose them into a hardware accelerator that achieves the expected performance.
While our primary focus is not to propose a new LLM accelerator architecture, we demonstrate that by using the analytical model, we can create a high-performance design that surpasses previous efforts.
Our major contributions are as follows:
•
We introduce an analytical framework that presents the first in-depth analysis of both the advantages and limitations of FPGA-based LLM spatial acceleration.
This framework not only allows us to estimate the performance of a specific accelerator configuration on a given FPGA device but also provides guidance for designing accelerators for LLM inference.
•
We create a suite of modular and reusable HLS kernels designed for building FPGA-based spatial accelerators for different Transformer models. We plan to open-source this kernel library
1
1
1
https://github.com/cornell-zhang/allo/tree/main/examples
and expect it to serve as a valuable resource for benchmarking HLS and FPGA acceleration more broadly.
•
Leveraging our kernel library, we design and implement a range of high-performance FPGA-based LLM accelerators that achieve speedups comparable to previous GPU and FPGA-based accelerators.
Specifically, for the BERT model, we achieve a 13.4
×
\times
×
speedup over prior FPGA-based accelerators.
For GPT generative inference, we achieve speedups of 2.2
×
\times
×
and 1.1
×
\times
×
in prefill and decode stages respectively, when compared to DFX, an FPGA-based overlay architecture.
Additionally, our accelerator is 1.9
×
\times
×
faster and 5.7
×
\times
×
more energy-efficient than the A100 GPU in the decode stage.

## Method

In this section, we propose a comprehensive analytical modeling framework aimed at understanding the computational requirements of a Transformer layer.
Our investigation begins by analyzing the compute demands and resource constraints on a single device.
We base our estimations on these constraints.
Finally, we extend the framework to the analysis of multiple devices.
3.1.
Computational Demands
Our first imperative is to calculate the computational demands of the model.
Given that the predominant computation in the Transformer model is general matrix-matrix multiplication (GEMM or Matmul) or general matrix-vector multiplication (GEMV)
(
pope2022googleinf,
;
kim2023survey,
)
, we employ the number of multiply–accumulates (MACs) as the proxy metric for quantifying compute requirements of the linear layers, as depicted in Table
1
.
For non-linear layers such as softmax and GeLU functions, they are elementwise operators that can be easily fused with the GEMM kernels in a pipeline design without affecting the final performance. More experimental results are provided in §
6.3
.
We denote
X
(
⋅
)
subscript
𝑋
⋅
X_{(\cdot)}
italic_X start_POSTSUBSCRIPT ( ⋅ ) end_POSTSUBSCRIPT
as the output tensors from preceding layers, and
W
(
⋅
)
subscript
𝑊
⋅
W_{(\cdot)}
italic_W start_POSTSUBSCRIPT ( ⋅ ) end_POSTSUBSCRIPT
represents the weights of corresponding linear layers.
For example,
X
sm
subscript
𝑋
sm
X_{\text{sm}}
italic_X start_POSTSUBSCRIPT sm end_POSTSUBSCRIPT
is the output of the softmax operator.
Our analysis here is restricted to a single batch; hence the tensors only have two dimensions.
We can observe that the computational demand during the prefill stage far surpasses that of the decode stage.
In the prefill stage, the required MACs of the two
Matmul
s within the SDP are quadratic to the sequence length (i.e.,
l
2
⁢
d
superscript
𝑙
2
𝑑
l^{2}d
italic_l start_POSTSUPERSCRIPT 2 end_POSTSUPERSCRIPT italic_d
).
Consequently, when input sequences exhibit substantial length, attention layers may extend computation time significantly.
On the contrary, in the decode stage, each operator processes a single token at a time, making the MACs independent of the sequence length except for SDP.
Table 1
.
MACs of the prefill and decode stages of the linear layers in the Transformer model in Figure
2
—
l
𝑙
l
italic_l
denotes input sequence length,
d
𝑑
d
italic_d
denotes input feature dimension size, and
d
FFN
subscript
𝑑
FFN
d_{\text{FFN}}
italic_d start_POSTSUBSCRIPT FFN end_POSTSUBSCRIPT
denotes FFN hidden dimension size.
Linear Layer
Abbreviations
Input Matrices
Prefill
Decode
Q/K/V linear
q
𝑞
q
italic_q
,
k
𝑘
k
italic_k
,
v
𝑣
v
italic_v
X
⁢
W
Q
,
X
⁢
W
K
,
X
⁢
W
V
𝑋
subscript
𝑊
𝑄
𝑋
subscript
𝑊
𝐾
𝑋
subscript
𝑊
𝑉
XW_{Q},XW_{K},XW_{V}
italic_X italic_W start_POSTSUBSCRIPT italic_Q end_POSTSUBSCRIPT , italic_X italic_W start_POSTSUBSCRIPT italic_K end_POSTSUBSCRIPT , italic_X italic_W start_POSTSUBSCRIPT italic_V end_POSTSUBSCRIPT
3
⁢
l
⁢
d
2
3
𝑙
superscript
𝑑
2
3ld^{2}
3 italic_l italic_d start_POSTSUPERSCRIPT 2 end_POSTSUPERSCRIPT
3
⁢
d
2
3
superscript
𝑑
2
3d^{2}
3 italic_d start_POSTSUPERSCRIPT 2 end_POSTSUPERSCRIPT
Matmul
1
1
{}_{1}
start_FLOATSUBSCRIPT 1 end_FLOATSUBSCRIPT
a
1
subscript
𝑎
1
a_{1}
italic_a start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT
Q
⁢
K
T
𝑄
superscript
𝐾
T
QK^{\mathrm{T}}
italic_Q italic_K start_POSTSUPERSCRIPT roman_T end_POSTSUPERSCRIPT
l
2
⁢
d
superscript
𝑙
2
𝑑
l^{2}d
italic_l start_POSTSUPERSCRIPT 2 end_POSTSUPERSCRIPT italic_d
(
l
+
1
)
⁢
d
𝑙
1
𝑑
(l+1)d
( italic_l + 1 ) italic_d
Matmul
2
2
{}_{2}
start_FLOATSUBSCRIPT 2 end_FLOATSUBSCRIPT
a
2
subscript
𝑎
2
a_{2}
italic_a start_POSTSUBSCRIPT 2 end_POSTSUBSCRIPT
X
sm
⁢
V
subscript
𝑋
sm
𝑉
X_{\text{sm}}V
italic_X start_POSTSUBSCRIPT sm end_POSTSUBSCRIPT italic_V
l
2
⁢
d
superscript
𝑙
2
𝑑
l^{2}d
italic_l start_POSTSUPERSCRIPT 2 end_POSTSUPERSCRIPT italic_d
(
l
+
1
)
⁢
d
𝑙
1
𝑑
(l+1)d
( italic_l + 1 ) italic_d
Projection
p
𝑝
p
italic_p
X
sdp
⁢
W
Proj
subscript
𝑋
sdp
subscript
𝑊
Proj
X_{\text{sdp}}W_{\text{Proj}}
italic_X start_POSTSUBSCRIPT sdp end_POSTSUBSCRIPT italic_W start_POSTSUBSCRIPT Proj end_POSTSUBSCRIPT
l
⁢
d
2
𝑙
superscript
𝑑
2
ld^{2}
italic_l italic_d start_POSTSUPERSCRIPT 2 end_POSTSUPERSCRIPT
d
2
superscript
𝑑
2
d^{2}
italic_d start_POSTSUPERSCRIPT 2 end_POSTSUPERSCRIPT
FFN
1
1
{}_{1}
start_FLOATSUBSCRIPT 1 end_FLOATSUBSCRIPT
f
1
subscript
𝑓
1
f_{1}
italic_f start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT
X
mha
⁢
W
FFN
1
subscript
𝑋
mha
subscript
𝑊
subscript
FFN
1
X_{\text{mha}}W_{\text{FFN}_{1}}
italic_X start_POSTSUBSCRIPT mha end_POSTSUBSCRIPT italic_W start_POSTSUBSCRIPT FFN start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT end_POSTSUBSCRIPT
l
⁢
d
⁢
d
FFN
𝑙
𝑑
subscript
𝑑
FFN
ldd_{\text{FFN}}
italic_l italic_d italic_d start_POSTSUBSCRIPT FFN end_POSTSUBSCRIPT
d
⁢
d
FFN
𝑑
subscript
𝑑
FFN
dd_{\text{FFN}}
italic_d italic_d start_POSTSUBSCRIPT FFN end_POSTSUBSCRIPT
FFN
2
2
{}_{2}
start_FLOATSUBSCRIPT 2 end_FLOATSUBSCRIPT
f
2
subscript
𝑓
2
f_{2}
italic_f start_POSTSUBSCRIPT 2 end_POSTSUBSCRIPT
X
act
⁢
W
FFN
2
subscript
𝑋
act
subscript
𝑊
subscript
FFN
2
X_{\text{act}}W_{\text{FFN}_{2}}
italic_X start_POSTSUBSCRIPT act end_POSTSUBSCRIPT italic_W start_POSTSUBSCRIPT FFN start_POSTSUBSCRIPT 2 end_POSTSUBSCRIPT end_POSTSUBSCRIPT
l
⁢
d
⁢
d
FFN
𝑙
𝑑
subscript
𝑑
FFN
ldd_{\text{FFN}}
italic_l italic_d italic_d start_POSTSUBSCRIPT FFN end_POSTSUBSCRIPT
d
⁢
d
FFN
𝑑
subscript
𝑑
FFN
dd_{\text{FFN}}
italic_d italic_d start_POSTSUBSCRIPT FFN end_POSTSUBSCRIPT
3.2.
Resource Constraints
We then model the compute and memory resource constraints on an FPGA.
In this section, we assume that one FPGA device can effectively compute at least a single Transformer layer, but our framework can be easily extended to more resource-constrained cases using a similar analysis proposed in §
3.4
.
3.2.1.
Compute Resource Constraints.
The core computational element for linear operators is the MAC unit.
Let
M
i
subscript
𝑀
𝑖
M_{i}
italic_M start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT
denote the compute power, in terms of the number of MACs per cycle allocated to each matrix multiplication kernel, where
i
𝑖
i
italic_i
ranges over
q
𝑞
q
italic_q
,
k
𝑘
k
italic_k
,
v
𝑣
v
italic_v
,
a
1
subscript
𝑎
1
a_{1}
italic_a start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT
,
a
2
subscript
𝑎
2
a_{2}
italic_a start_POSTSUBSCRIPT 2 end_POSTSUBSCRIPT
,
p
𝑝
p
italic_p
,
f
1
subscript
𝑓
1
f_{1}
italic_f start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT
, and
f
2
subscript
𝑓
2
f_{2}
italic_f start_POSTSUBSCRIPT 2 end_POSTSUBSCRIPT
, based on the notation in Table
1
.
We quantize the matrix multiplication to integer inputs for maximum efficiency, which has been proven to be effective by many recent studies
(
xiao2023smoothquant,
;
dettmers2022llmint8,
;
sheng2020qbert,
;
kim2021ibert,
)
.
Quantization enables single-cycle accumulation.
As a result, one multiply-accumulator (MAC) unit can provide a 1 MAC/cycle throughput with a properly pipelined multiplier.
Therefore, the latency for the
Q
𝑄
Q
italic_Q
projection can be calculated as
l
⁢
d
2
/
M
q
𝑙
superscript
𝑑
2
subscript
𝑀
𝑞
ld^{2}/M_{q}
italic_l italic_d start_POSTSUPERSCRIPT 2 end_POSTSUPERSCRIPT / italic_M start_POSTSUBSCRIPT italic_q end_POSTSUBSCRIPT
cycles, considering that the total number of MACs computed in this operator is
l
⁢
d
2
𝑙
superscript
𝑑
2
ld^{2}
italic_l italic_d start_POSTSUPERSCRIPT 2 end_POSTSUPERSCRIPT
.
Suppose we want to deploy
C
𝐶
C
italic_C
Transformer model layers on an FPGA.
The total MAC units must not exceed the capacity of the device.
Since we employ a dataflow design that unfolds all the layers on-board, the required MAC units are simply the sum of the MAC units for each layer.
This requirement can be expressed as:
(2)
∑
M
i
⁢
C
<
M
tot
,
i
∈
{
q
,
k
,
v
,
a
1
,
a
2
,
p
,
f
1
,
f
2
}
,
formulae-sequence
subscript
𝑀
𝑖
𝐶
subscript
𝑀
tot
𝑖
𝑞
𝑘
𝑣
subscript
𝑎
1
subscript
𝑎
2
𝑝
subscript
𝑓
1
subscript
𝑓
2
\sum{M_{i}}C<M_{\text{tot}},{i\in\{q,k,v,a_{1},a_{2},p,f_{1},f_{2}\}}\,,
∑ italic_M start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT italic_C < italic_M start_POSTSUBSCRIPT tot end_POSTSUBSCRIPT , italic_i ∈ { italic_q , italic_k , italic_v , italic_a start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT , italic_a start_POSTSUBSCRIPT 2 end_POSTSUBSCRIPT , italic_p , italic_f start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT , italic_f start_POSTSUBSCRIPT 2 end_POSTSUBSCRIPT } ,
where
M
tot
subscript
𝑀
tot
M_{\text{tot}}
italic_M start_POSTSUBSCRIPT tot end_POSTSUBSCRIPT
represents the total available compute power of an FPGA in terms of MACs per cycle,
which can be obtained from the official data sheets.
For FPGAs with specialized compute blocks (e.g., AI Engine
(
vck5000,
)
and AI Tensor Blocks
(
stratix10,
)
), we can convert their compute power to match the frequency of the programming logic, thus obtaining an overall value
M
tot
subscript
𝑀
tot
M_{\text{tot}}
italic_M start_POSTSUBSCRIPT tot end_POSTSUBSCRIPT
for the entire FPGA.
For example, the VCK5000 FPGA
(
vck5000,
)
has 400 AI Engines, each of which can compute 128 MACs/cycle at 1GHz.
Therefore, the equivalent compute power at 250MHz is 128
×
\times
×
400
×
\times
×
1GHz/250MHz, which is 204800 MACs/cycle.
3.2.2.
Memory Capacity Constraints.
The demand for memory capacity stems from a variety of on-chip buffers, including weight buffers for parameters, buffers for
K
𝐾
K
italic_K
and
V
𝑉
V
italic_V
matrices, and FIFOs interconnecting different stages.
Parameter buffers.
To optimize an FPGA-based dataflow design, we assume that all the quantized parameters can be accommodated in on-chip or off-chip memory.
Suppose all the linear weights are quantized to
b
W
subscript
𝑏
𝑊
b_{W}
italic_b start_POSTSUBSCRIPT italic_W end_POSTSUBSCRIPT
bits, and the size of the linear operator
i
𝑖
i
italic_i
is
s
i
subscript
𝑠
𝑖
s_{i}
italic_s start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT
.
The total size of the buffers is
S
param
=
∑
i
∈
{
q
,
k
,
v
,
p
,
f
1
,
f
2
}
s
i
⁢
b
W
=
(
4
⁢
d
2
+
2
⁢
d
⁢
d
FFN
)
⁢
b
W
subscript
𝑆
param
subscript
𝑖
𝑞
𝑘
𝑣
𝑝
subscript
𝑓
1
subscript
𝑓
2
subscript
𝑠
𝑖
subscript
𝑏
𝑊
4
superscript
𝑑
2
2
𝑑
subscript
𝑑
FFN
subscript
𝑏
𝑊
S_{\text{param}}=\sum_{i\in\{q,k,v,p,f_{1},f_{2}\}}s_{i}b_{W}=(4d^{2}+2dd_{%
\text{FFN}})b_{W}
italic_S start_POSTSUBSCRIPT param end_POSTSUBSCRIPT = ∑ start_POSTSUBSCRIPT italic_i ∈ { italic_q , italic_k , italic_v , italic_p , italic_f start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT , italic_f start_POSTSUBSCRIPT 2 end_POSTSUBSCRIPT } end_POSTSUBSCRIPT italic_s start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT italic_b start_POSTSUBSCRIPT italic_W end_POSTSUBSCRIPT = ( 4 italic_d start_POSTSUPERSCRIPT 2 end_POSTSUPERSCRIPT + 2 italic_d italic_d start_POSTSUBSCRIPT FFN end_POSTSUBSCRIPT ) italic_b start_POSTSUBSCRIPT italic_W end_POSTSUBSCRIPT
if storing on-chip.
If the parameters are too large to fit in on-chip memory, we can store the parameters in DRAM and tile the parameters with size
M
i
subscript
𝑀
𝑖
M_{i}
italic_M start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT
on-chip, then the total tiled buffer size is
S
tile
=
∑
i
∈
{
q
,
k
,
v
,
p
,
f
1
,
f
2
}
M
i
⁢
b
W
subscript
𝑆
tile
subscript
𝑖
𝑞
𝑘
𝑣
𝑝
subscript
𝑓
1
subscript
𝑓
2
subscript
𝑀
𝑖
subscript
𝑏
𝑊
S_{\text{tile}}=\sum_{i\in\{q,k,v,p,f_{1},f_{2}\}}M_{i}b_{W}
italic_S start_POSTSUBSCRIPT tile end_POSTSUBSCRIPT = ∑ start_POSTSUBSCRIPT italic_i ∈ { italic_q , italic_k , italic_v , italic_p , italic_f start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT , italic_f start_POSTSUBSCRIPT 2 end_POSTSUBSCRIPT } end_POSTSUBSCRIPT italic_M start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT italic_b start_POSTSUBSCRIPT italic_W end_POSTSUBSCRIPT
.
To hide the memory access latency, we need to double buffer those parameters, so the final buffer size of the
i
𝑖
i
italic_i
-th linear operator is
2
⁢
S
tile
2
subscript
𝑆
tile
2S_{\text{tile}}
2 italic_S start_POSTSUBSCRIPT tile end_POSTSUBSCRIPT
.
KV Cache.
When conducting matrix multiplication, at least one of the matrices’ elements must be accessed repeatedly so that a buffer is required.
Given that parameters are already buffered, only the SDP requires buffering for at least one of the input matrices.
In our case, we choose to buffer
K
𝐾
K
italic_K
and
V
𝑉
V
italic_V
, which will be later passed to the decode stage as the KV cache.
We also double buffer
K
𝐾
K
italic_K
and
V
𝑉
V
italic_V
matrices to improve throughput.
The final buffer size is
S
KV
=
4
⁢
l
max
⁢
d
⁢
b
A
subscript
𝑆
KV
4
subscript
𝑙
𝑑
subscript
𝑏
𝐴
S_{\text{KV}}=4l_{\max}db_{A}
italic_S start_POSTSUBSCRIPT KV end_POSTSUBSCRIPT = 4 italic_l start_POSTSUBSCRIPT roman_max end_POSTSUBSCRIPT italic_d italic_b start_POSTSUBSCRIPT italic_A end_POSTSUBSCRIPT
, where
b
A
subscript
𝑏
𝐴
b_{A}
italic_b start_POSTSUBSCRIPT italic_A end_POSTSUBSCRIPT
is the bitwidth of the activation and
l
max
subscript
𝑙
l_{\max}
italic_l start_POSTSUBSCRIPT roman_max end_POSTSUBSCRIPT
is the maximum sequence length supported by the model.
Notice KV cache can also be tiled on-chip, which can leverage a similar analysis above.
FIFOs.
The intermediate results between linear operators flow in FIFOs since the linear operators sequentially access them.
For the initial residual connection, we assume that the input tensors are fetched from off-chip memory to obviate the need for additional buffering.
However, for the second residual connection related to the FFN, it is necessary to use an intermediate buffer to store the projection’s activation
X
act
subscript
𝑋
act
X_{\text{act}}
italic_X start_POSTSUBSCRIPT act end_POSTSUBSCRIPT
before the FFN.
This buffer simultaneously serves as a bypass path.
To avoid deadlock, the buffer must possess sufficient capacity to store
X
act
subscript
𝑋
act
X_{\text{act}}
italic_X start_POSTSUBSCRIPT act end_POSTSUBSCRIPT
.
We simply create a FIFO of size
l
⁢
d
⁢
b
A
𝑙
𝑑
subscript
𝑏
𝐴
ldb_{A}
italic_l italic_d italic_b start_POSTSUBSCRIPT italic_A end_POSTSUBSCRIPT
to store it.
For other FIFO connections, we assume a FIFO depth of
s
𝑠
s
italic_s
and one FIFO connecting each layer in Figure
2
, so the total FIFO size is equal to
S
FIFO
=
16
⁢
s
⁢
b
A
+
l
⁢
d
⁢
b
A
subscript
𝑆
FIFO
16
𝑠
subscript
𝑏
𝐴
𝑙
𝑑
subscript
𝑏
𝐴
S_{\text{FIFO}}=16sb_{A}+ldb_{A}
italic_S start_POSTSUBSCRIPT FIFO end_POSTSUBSCRIPT = 16 italic_s italic_b start_POSTSUBSCRIPT italic_A end_POSTSUBSCRIPT + italic_l italic_d italic_b start_POSTSUBSCRIPT italic_A end_POSTSUBSCRIPT
.
In summary, the memory capacity constraint is expressed as:
(3)
S
param
⁢
C
subscript
𝑆
param
𝐶
\displaystyle S_{\text{param}}C
italic_S start_POSTSUBSCRIPT param end_POSTSUBSCRIPT italic_C
<
D
⁢
R
⁢
A
⁢
M
tot
,
absent
𝐷
𝑅
𝐴
subscript
𝑀
tot
\displaystyle<DRAM_{\text{tot}}\,,
< italic_D italic_R italic_A italic_M start_POSTSUBSCRIPT tot end_POSTSUBSCRIPT ,
∑
S
i
⁢
C
subscript
𝑆
𝑖
𝐶
\displaystyle\sum S_{i}C
∑ italic_S start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT italic_C
<
S
⁢
R
⁢
A
⁢
M
tot
,
i
∈
{
tile
,
KV
,
FIFO
}
,
formulae-sequence
absent
𝑆
𝑅
𝐴
subscript
𝑀
tot
𝑖
tile
KV
FIFO
\displaystyle<SRAM_{\text{tot}}\,,i\in\{\text{tile},\text{KV},\text{FIFO}\}\,,
< italic_S italic_R italic_A italic_M start_POSTSUBSCRIPT tot end_POSTSUBSCRIPT , italic_i ∈ { tile , KV , FIFO } ,
if the parameters are stored off-chip.
D
⁢
R
⁢
A
⁢
M
tot
𝐷
𝑅
𝐴
subscript
𝑀
tot
DRAM_{\text{tot}}
italic_D italic_R italic_A italic_M start_POSTSUBSCRIPT tot end_POSTSUBSCRIPT
and
S
⁢
R
⁢
A
⁢
M
tot
𝑆
𝑅
𝐴
subscript
𝑀
tot
SRAM_{\text{tot}}
italic_S italic_R italic_A italic_M start_POSTSUBSCRIPT tot end_POSTSUBSCRIPT
are the total available off-chip and on-chip memory.
3.2.3.
Memory Port Constraints.
Besides memory capacity, we also need to consider constraints on memory ports in a highly paralleled design.
For matrix multiplication, if different MAC units
work in parallel, they will visit the weight/result buffers simultaneously, hence contending for memory ports.
This issue can be addressed by either partitioning the buffer, effectively offering more memory ports; or packing data to create wider elements, subsequently reducing the number of memory ports required.
SRAM resources.
The on-chip SRAM resources of FPGAs are typically organized as blocks.
Each block has a fixed capacity and may support configurable bitwidth.
For example, on AMD UltraScale+ FPGAs, there are two types of SRAM resources:
Block RAM (BRAM)
and
Ultra RAM (URAM)
.
BRAM blocks can be configured to 1
×
\times
×
36 Kb block or 2
×
\times
×
18 Kb blocks, with two read and write ports each.
URAM blocks are 288 Kb with one read and one write port.
The port width of the BRAM block is flexible; it can be configured to 1, 2, 4, 9, 18, 36, or 72 (in 36 Kb mode) bits, while the port width of the URAM block is fixed at 72 bits.
Similar to BRAM and URAM, Intel FPGAs have M20K and eSRAM with different configurable port widths.
Memory blocks needed without data packing.
To begin with, we analyze the port constraints without data packing.
In this case, to eliminate the port contention, different MAC units may need different memory ports.
Consider the linear operator
i
𝑖
i
italic_i
with the size of
s
i
subscript
𝑠
𝑖
s_{i}
italic_s start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT
with
M
i
subscript
𝑀
𝑖
M_{i}
italic_M start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT
MAC units working in parallel, each loaded weight may feed multiple MAC units due to intrinsic data reuse in GEMM.
We use
r
i
subscript
𝑟
𝑖
r_{i}
italic_r start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT
to represent the data reuse factor (number of MAC units sharing the loaded weight).
Therefore, the weight buffer needs to be partitioned into
M
i
/
r
i
subscript
𝑀
𝑖
subscript
𝑟
𝑖
M_{i}/r_{i}
italic_M start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT / italic_r start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT
parts.
If we store all the weight buffers on-chip, then the number of
b
W
subscript
𝑏
𝑊
b_{W}
italic_b start_POSTSUBSCRIPT italic_W end_POSTSUBSCRIPT
-bit elements in each partition is
s
i
/
(
M
i
/
r
i
)
subscript
𝑠
𝑖
subscript
𝑀
𝑖
subscript
𝑟
𝑖
s_{i}/(M_{i}/r_{i})
italic_s start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT / ( italic_M start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT / italic_r start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT )
.
However,
b
W
subscript
𝑏
𝑊
b_{W}
italic_b start_POSTSUBSCRIPT italic_W end_POSTSUBSCRIPT
may not fully occupy one memory word as the memory bitwidth can only take limited options.
We introduce the effective bit width,
b
B
⁢
R
⁢
A
⁢
M
subscript
𝑏
𝐵
𝑅
𝐴
𝑀
b_{BRAM}
italic_b start_POSTSUBSCRIPT italic_B italic_R italic_A italic_M end_POSTSUBSCRIPT
, to be the smallest memory bitwidth larger than
b
W
subscript
𝑏
𝑊
b_{W}
italic_b start_POSTSUBSCRIPT italic_W end_POSTSUBSCRIPT
.
Let
S
B
⁢
R
⁢
A
⁢
M
subscript
𝑆
𝐵
𝑅
𝐴
𝑀
S_{BRAM}
italic_S start_POSTSUBSCRIPT italic_B italic_R italic_A italic_M end_POSTSUBSCRIPT
be the total capacity (in bits) of one memory block,
we can deduce the total number of memory blocks for one linear operator:
(4)
R
i
=
⌈
s
i
⁢
b
B
⁢
R
⁢
A
⁢
M
M
i
/
r
i
×
S
B
⁢
R
⁢
A
⁢
M
⌉
×
M
i
/
r
i
.
subscript
𝑅
𝑖
subscript
𝑠
𝑖
subscript
𝑏
𝐵
𝑅
𝐴
𝑀
subscript
𝑀
𝑖
subscript
𝑟
𝑖
subscript
𝑆
𝐵
𝑅
𝐴
𝑀
subscript
𝑀
𝑖
subscript
𝑟
𝑖
R_{i}=\left\lceil\frac{s_{i}b_{BRAM}}{M_{i}/r_{i}\times S_{BRAM}}\right\rceil%
\times M_{i}/r_{i}\,.
italic_R start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT = ⌈ divide start_ARG italic_s start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT italic_b start_POSTSUBSCRIPT italic_B italic_R italic_A italic_M end_POSTSUBSCRIPT end_ARG start_ARG italic_M start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT / italic_r start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT × italic_S start_POSTSUBSCRIPT italic_B italic_R italic_A italic_M end_POSTSUBSCRIPT end_ARG ⌉ × italic_M start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT / italic_r start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT .
If the parameters are loaded from off-chip memory and we only store a tile of the weight on-chip, then
s
i
subscript
𝑠
𝑖
s_{i}
italic_s start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT
is simply
M
i
subscript
𝑀
𝑖
M_{i}
italic_M start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT
, and
R
i
subscript
𝑅
𝑖
R_{i}
italic_R start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT
also becomes
M
i
subscript
𝑀
𝑖
M_{i}
italic_M start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT
as
b
B
⁢
R
⁢
A
⁢
M
≪
S
B
⁢
R
⁢
A
⁢
M
much-less-than
subscript
𝑏
𝐵
𝑅
𝐴
𝑀
subscript
𝑆
𝐵
𝑅
𝐴
𝑀
b_{BRAM}\ll S_{BRAM}
italic_b start_POSTSUBSCRIPT italic_B italic_R italic_A italic_M end_POSTSUBSCRIPT ≪ italic_S start_POSTSUBSCRIPT italic_B italic_R italic_A italic_M end_POSTSUBSCRIPT
.
Since we need to double buffer those parameters, the final buffer size of the
i
𝑖
i
italic_i
-th linear operator is
2
⁢
M
i
2
subscript
𝑀
𝑖
2M_{i}
2 italic_M start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT
.
Notice the
k
𝑘
k
italic_k
and
v
𝑣
v
italic_v
layers need to be double-buffered, so the required BRAM also doubles in these two layers.
We can obtain the total required BRAM as below:
(5)
∑
i
∈
{
q
,
k
,
v
,
p
,
f
1
,
f
2
}
C
⁢
R
i
+
2
⁢
C
⁢
(
R
a
1
+
R
a
2
)
<
M
⁢
e
⁢
m
tot
.
subscript
𝑖
𝑞
𝑘
𝑣
𝑝
subscript
𝑓
1
subscript
𝑓
2
𝐶
subscript
𝑅
𝑖
2
𝐶
subscript
𝑅
subscript
𝑎
1
subscript
𝑅
subscript
𝑎
2
𝑀
𝑒
subscript
𝑚
tot
\sum_{i\in\{q,k,v,p,f_{1},f_{2}\}}CR_{i}+2C(R_{a_{1}}+R_{a_{2}})<Mem_{\text{%
tot}}\,.
∑ start_POSTSUBSCRIPT italic_i ∈ { italic_q , italic_k , italic_v , italic_p , italic_f start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT , italic_f start_POSTSUBSCRIPT 2 end_POSTSUBSCRIPT } end_POSTSUBSCRIPT italic_C italic_R start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT + 2 italic_C ( italic_R start_POSTSUBSCRIPT italic_a start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT end_POSTSUBSCRIPT + italic_R start_POSTSUBSCRIPT italic_a start_POSTSUBSCRIPT 2 end_POSTSUBSCRIPT end_POSTSUBSCRIPT ) < italic_M italic_e italic_m start_POSTSUBSCRIPT tot end_POSTSUBSCRIPT .
Memory blocks needed with data packing.
Data packing can alleviate the strain on memory port contention by consolidating multiple narrow data into a single, wider data element.
This process allows multiple MAC units to access data from the same memory port.
We consider packing data into
b
p
⁢
a
⁢
c
⁢
k
subscript
𝑏
𝑝
𝑎
𝑐
𝑘
b_{pack}
italic_b start_POSTSUBSCRIPT italic_p italic_a italic_c italic_k end_POSTSUBSCRIPT
bits for the linear weights, and we have
b
p
⁢
a
⁢
c
⁢
k
=
k
⁢
b
W
subscript
𝑏
𝑝
𝑎
𝑐
𝑘
𝑘
subscript
𝑏
𝑊
b_{pack}=kb_{W}
italic_b start_POSTSUBSCRIPT italic_p italic_a italic_c italic_k end_POSTSUBSCRIPT = italic_k italic_b start_POSTSUBSCRIPT italic_W end_POSTSUBSCRIPT
.
Again, we denote
b
B
⁢
R
⁢
A
⁢
M
subscript
𝑏
𝐵
𝑅
𝐴
𝑀
b_{BRAM}
italic_b start_POSTSUBSCRIPT italic_B italic_R italic_A italic_M end_POSTSUBSCRIPT
as the smallest memory bitwidth larger than
b
p
⁢
a
⁢
c
⁢
k
subscript
𝑏
𝑝
𝑎
𝑐
𝑘
b_{pack}
italic_b start_POSTSUBSCRIPT italic_p italic_a italic_c italic_k end_POSTSUBSCRIPT
.
We need to partition
M
i
/
r
i
subscript
𝑀
𝑖
subscript
𝑟
𝑖
M_{i}/r_{i}
italic_M start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT / italic_r start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT
MAC units to
M
i
/
r
i
/
k
subscript
𝑀
𝑖
subscript
𝑟
𝑖
𝑘
M_{i}/r_{i}/k
italic_M start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT / italic_r start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT / italic_k
parts, and each partition has
⌈
s
i
/
k
×
b
B
⁢
R
⁢
A
⁢
M
/
(
M
i
/
r
i
/
k
)
⌉
subscript
𝑠
𝑖
𝑘
subscript
𝑏
𝐵
𝑅
𝐴
𝑀
subscript
𝑀
𝑖
subscript
𝑟
𝑖
𝑘
\lceil s_{i}/k\times b_{BRAM}/(M_{i}/r_{i}/k)\rceil
⌈ italic_s start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT / italic_k × italic_b start_POSTSUBSCRIPT italic_B italic_R italic_A italic_M end_POSTSUBSCRIPT / ( italic_M start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT / italic_r start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT / italic_k ) ⌉
bits.
Therefore, the total number of memory blocks needed is:
(6)
R
i
=
⌈
s
i
⁢
b
B
⁢
R
⁢
A
⁢
M
M
i
/
r
i
×
S
B
⁢
R
⁢
A
⁢
M
⌉
×
M
i
/
r
i
k
.
subscript
𝑅
𝑖
subscript
𝑠
𝑖
subscript
𝑏
𝐵
𝑅
𝐴
𝑀
subscript
𝑀
𝑖
subscript
𝑟
𝑖
subscript
𝑆
𝐵
𝑅
𝐴
𝑀
subscript
𝑀
𝑖
subscript
𝑟
𝑖
𝑘
R_{i}=\left\lceil\frac{s_{i}b_{BRAM}}{M_{i}/r_{i}\times S_{BRAM}}\right\rceil%
\times\frac{M_{i}/r_{i}}{k}\,.
italic_R start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT = ⌈ divide start_ARG italic_s start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT italic_b start_POSTSUBSCRIPT italic_B italic_R italic_A italic_M end_POSTSUBSCRIPT end_ARG start_ARG italic_M start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT / italic_r start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT × italic_S start_POSTSUBSCRIPT italic_B italic_R italic_A italic_M end_POSTSUBSCRIPT end_ARG ⌉ × divide start_ARG italic_M start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT / italic_r start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT end_ARG start_ARG italic_k end_ARG .
3.2.4.
Memory Bandwidth Constraints.
If the parameters are stored off-chip, we need to consider the impact of off-chip memory bandwidth.
Similar to §
4.2.2
, we use
r
i
subscript
𝑟
𝑖
r_{i}
italic_r start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT
to denote the data reuse factor of a linear operator with
M
i
subscript
𝑀
𝑖
M_{i}
italic_M start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT
MAC units.
Effectively,
M
i
/
r
i
subscript
𝑀
𝑖
subscript
𝑟
𝑖
M_{i}/r_{i}
italic_M start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT / italic_r start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT
weights must be loaded from off-chip memory per cycle to feed the MAC units, requiring a bandwidth of:
(7)
B
i
=
b
W
×
M
i
/
r
i
×
f
⁢
r
⁢
e
⁢
q
,
subscript
𝐵
𝑖
subscript
𝑏
𝑊
subscript
𝑀
𝑖
subscript
𝑟
𝑖
𝑓
𝑟
𝑒
𝑞
B_{i}=b_{W}\times M_{i}/r_{i}\times freq\,,
italic_B start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT = italic_b start_POSTSUBSCRIPT italic_W end_POSTSUBSCRIPT × italic_M start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT / italic_r start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT × italic_f italic_r italic_e italic_q ,
where
f
⁢
r
⁢
e
⁢
q
𝑓
𝑟
𝑒
𝑞
freq
italic_f italic_r italic_e italic_q
is the achieved frequency of FPGA.
If the total required bandwidth,
∑
i
C
⁢
B
i
⁢
(
i
∈
{
q
,
k
,
v
,
p
,
f
1
,
f
2
}
)
subscript
𝑖
𝐶
subscript
𝐵
𝑖
𝑖
𝑞
𝑘
𝑣
𝑝
subscript
𝑓
1
subscript
𝑓
2
\sum_{i}C{B_{i}}(i\in\{q,k,v,p,f_{1},f_{2}\})
∑ start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT italic_C italic_B start_POSTSUBSCRIPT italic_i end_POSTSUBSCRIPT ( italic_i ∈ { italic_q , italic_k , italic_v , italic_p , italic_f start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT , italic_f start_POSTSUBSCRIPT 2 end_POSTSUBSCRIPT } )
, exceeds the maximum device bandwidth, the inference becomes bandwidth bound.
Notice this bandwidth requirement needs to be analyzed for each operator individually if the data loading requires accessing multiple DDR or HBM channels.
3.3.
Performance Estimation
In this section, we estimate the overall latency based on the constraints and conduct work balancing for the dataflow.
Figure 4
.
Pipeline diagram. Different colors stand for different input samples.
Different blocks stand for different linear operators which also constitute the pipeline stages.
h
ℎ
h
italic_h
is the number of attention heads.
3.3.1.
Latency Estimation.
We construct the pipeline diagram as shown in Figure
4
.
As mentioned in §
3.2.2
, since we need to store the
K
𝐾
K
italic_K
and
V
𝑉
V
italic_V
values after the linear operators, there is an implicit synchronization point between the
q
𝑞
q
italic_q
/
k
𝑘
k
italic_k
/
v
𝑣
v
italic_v
operator and the latter SDP and FFN parts.
The computation of them cannot be overlapped.
Notice the
q
𝑞
q
italic_q
/
k
𝑘
k
italic_k
/
v
𝑣
v
italic_v
operator can be performed in parallel since they do not have any dependencies.
After
k
𝑘
k
italic_k
and
v
𝑣
v
italic_v
have been fully calculated, the subsequent computations of SDP and FFN can be greatly overlapped.
This is because these operations do not need to wait for all the results to perform the next operation.
The results of the previous operation can be directly streamed into the next operation as input.
Moreover, since different Transformer layers share the same architecture, their computation can also be overlapped without waiting for the result of the previous layer.
Suppose the Transformer model has
N
𝑁
N
italic_N
layers in total.
Since we have
C
𝐶
C
italic_C
layers on one FPGA, it needs to iterate
N
/
C
𝑁
𝐶
N/C
italic_N / italic_C
times to process the whole model.
We can calculate the latency of different stages, and the overall latency is the maximum latency of these stages (which defines the initiation interval of the pipeline) times the number of iterations, i.e.,
(8)
T
prefill
subscript
𝑇
prefill
\displaystyle T_{\text{prefill}}
italic_T start_POSTSUBSCRIPT prefill end_POSTSUBSCRIPT
=
1
f
⁢
r
⁢
e
⁢
q
⁢
N
C
⁢
(
l
⁢
d
2
M
k
+
C
⁢
max
⁡
(
l
⁢
d
2
M
k
,
l
2
⁢
d
M
a
1
,
l
⁢
d
⁢
d
FFN
M
f
1
,
T
mem
)
)
,
absent
1
𝑓
𝑟
𝑒
𝑞
𝑁
𝐶
𝑙
superscript
𝑑
2
subscript
𝑀
𝑘
𝐶
𝑙
superscript
𝑑
2
subscript
𝑀
𝑘
superscript
𝑙
2
𝑑
subscript
𝑀
subscript
𝑎
1
𝑙
𝑑
subscript
𝑑
FFN
subscript
𝑀
subscript
𝑓
1
subscript
𝑇
mem
\displaystyle=\frac{1}{freq}\frac{N}{C}\left(\frac{ld^{2}}{M_{k}}+C\max\left(%
\frac{ld^{2}}{M_{k}},\frac{l^{2}d}{M_{a_{1}}},\frac{ldd_{\text{FFN}}}{M_{f_{1}%
}},T_{\text{mem}}\right)\right)\,,
= divide start_ARG 1 end_ARG start_ARG italic_f italic_r italic_e italic_q end_ARG divide start_ARG italic_N end_ARG start_ARG italic_C end_ARG ( divide start_ARG italic_l italic_d start_POSTSUPERSCRIPT 2 end_POSTSUPERSCRIPT end_ARG start_ARG italic_M start_POSTSUBSCRIPT italic_k end_POSTSUBSCRIPT end_ARG + italic_C roman_max ( divide start_ARG italic_l italic_d start_POSTSUPERSCRIPT 2 end_POSTSUPERSCRIPT end_ARG start_ARG italic_M start_POSTSUBSCRIPT italic_k end_POSTSUBSCRIPT end_ARG , divide start_ARG italic_l start_POSTSUPERSCRIPT 2 end_POSTSUPERSCRIPT italic_d end_ARG start_ARG italic_M start_POSTSUBSCRIPT italic_a start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT end_POSTSUBSCRIPT end_ARG , divide start_ARG italic_l italic_d italic_d start_POSTSUBSCRIPT FFN end_POSTSUBSCRIPT end_ARG start_ARG italic_M start_POSTSUBSCRIPT italic_f start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT end_POSTSUBSCRIPT end_ARG , italic_T start_POSTSUBSCRIPT mem end_POSTSUBSCRIPT ) ) ,
(9)
T
decode
subscript
𝑇
decode
\displaystyle T_{\text{decode}}
italic_T start_POSTSUBSCRIPT decode end_POSTSUBSCRIPT
=
1
f
⁢
r
⁢
e
⁢
q
⁢
N
C
⁢
(
d
2
M
k
+
C
⁢
max
⁡
(
d
2
M
k
,
(
l
max
+
1
)
⁢
d
M
a
1
,
d
⁢
d
FFN
M
f
1
,
T
mem
)
)
,
absent
1
𝑓
𝑟
𝑒
𝑞
𝑁
𝐶
superscript
𝑑
2
subscript
𝑀
𝑘
𝐶
superscript
𝑑
2
subscript
𝑀
𝑘
subscript
𝑙
1
𝑑
subscript
𝑀
subscript
𝑎
1
𝑑
subscript
𝑑
FFN
subscript
𝑀
subscript
𝑓
1
subscript
𝑇
mem
\displaystyle=\frac{1}{freq}\frac{N}{C}\left(\frac{d^{2}}{M_{k}}+C\max\left(%
\frac{d^{2}}{M_{k}},\frac{(l_{\max}+1)d}{M_{a_{1}}},\frac{dd_{\text{FFN}}}{M_{%
f_{1}}},T_{\text{mem}}\right)\right)\,,
= divide start_ARG 1 end_ARG start_ARG italic_f italic_r italic_e italic_q end_ARG divide start_ARG italic_N end_ARG start_ARG italic_C end_ARG ( divide start_ARG italic_d start_POSTSUPERSCRIPT 2 end_POSTSUPERSCRIPT end_ARG start_ARG italic_M start_POSTSUBSCRIPT italic_k end_POSTSUBSCRIPT end_ARG + italic_C roman_max ( divide start_ARG italic_d start_POSTSUPERSCRIPT 2 end_POSTSUPERSCRIPT end_ARG start_ARG italic_M start_POSTSUBSCRIPT italic_k end_POSTSUBSCRIPT end_ARG , divide start_ARG ( italic_l start_POSTSUBSCRIPT roman_max end_POSTSUBSCRIPT + 1 ) italic_d end_ARG start_ARG italic_M start_POSTSUBSCRIPT italic_a start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT end_POSTSUBSCRIPT end_ARG , divide start_ARG italic_d italic_d start_POSTSUBSCRIPT FFN end_POSTSUBSCRIPT end_ARG start_ARG italic_M start_POSTSUBSCRIPT italic_f start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT end_POSTSUBSCRIPT end_ARG , italic_T start_POSTSUBSCRIPT mem end_POSTSUBSCRIPT ) ) ,
where the first term inside the parentheses is the latency of the
q
𝑞
q
italic_q
/
k
𝑘
k
italic_k
/
v
𝑣
v
italic_v
linear operator (i.e.,
t
𝑡
t
italic_t
in Figure
4
).
T
mem
subscript
𝑇
mem
T_{\text{mem}}
italic_T start_POSTSUBSCRIPT mem end_POSTSUBSCRIPT
is the off-chip memory access latency, which can be calculated based on Equation (
7
).
3.3.2.
Work Balancing.
As the overall latency is determined by the slowest stage in the dataflow, we can balance the execution time of each stage; hence we have
(10)
l
⁢
d
2
M
q
,
k
,
v
,
p
=
l
2
⁢
d
/
h
M
a
1
,
a
2
⁢
h
=
l
⁢
d
⁢
d
FFN
M
f
1
,
f
2
𝑙
superscript
𝑑
2
subscript
𝑀
𝑞
𝑘
𝑣
𝑝
superscript
𝑙
2
𝑑
ℎ
subscript
𝑀
subscript
𝑎
1
subscript
𝑎
2
ℎ
𝑙
𝑑
subscript
𝑑
FFN
subscript
𝑀
subscript
𝑓
1
subscript
𝑓
2
\displaystyle\frac{ld^{2}}{M_{q,k,v,p}}=\frac{l^{2}d/h}{M_{a_{1},a_{2}}}h=%
\frac{ldd_{\text{FFN}}}{M_{f_{1},f_{2}}}
divide start_ARG italic_l italic_d start_POSTSUPERSCRIPT 2 end_POSTSUPERSCRIPT end_ARG start_ARG italic_M start_POSTSUBSCRIPT italic_q , italic_k , italic_v , italic_p end_POSTSUBSCRIPT end_ARG = divide start_ARG italic_l start_POSTSUPERSCRIPT 2 end_POSTSUPERSCRIPT italic_d / italic_h end_ARG start_ARG italic_M start_POSTSUBSCRIPT italic_a start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT , italic_a start_POSTSUBSCRIPT 2 end_POSTSUBSCRIPT end_POSTSUBSCRIPT end_ARG italic_h = divide start_ARG italic_l italic_d italic_d start_POSTSUBSCRIPT FFN end_POSTSUBSCRIPT end_ARG start_ARG italic_M start_POSTSUBSCRIPT italic_f start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT , italic_f start_POSTSUBSCRIPT 2 end_POSTSUBSCRIPT end_POSTSUBSCRIPT end_ARG
(11)
⟹
\displaystyle\implies
⟹
M
=
M
q
,
k
,
v
,
p
=
d
/
l
⁢
M
a
1
,
a
2
=
d
/
d
FFN
⁢
M
f
1
,
f
2
,
𝑀
subscript
𝑀
𝑞
𝑘
𝑣
𝑝
𝑑
𝑙
subscript
𝑀
subscript
𝑎
1
subscript
𝑎
2
𝑑
subscript
𝑑
FFN
subscript
𝑀
subscript
𝑓
1
subscript
𝑓
2
\displaystyle M=M_{q,k,v,p}=d/lM_{a_{1},a_{2}}=d/d_{\text{FFN}}M_{f_{1},f_{2}}\,,
italic_M = italic_M start_POSTSUBSCRIPT italic_q , italic_k , italic_v , italic_p end_POSTSUBSCRIPT = italic_d / italic_l italic_M start_POSTSUBSCRIPT italic_a start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT , italic_a start_POSTSUBSCRIPT 2 end_POSTSUBSCRIPT end_POSTSUBSCRIPT = italic_d / italic_d start_POSTSUBSCRIPT FFN end_POSTSUBSCRIPT italic_M start_POSTSUBSCRIPT italic_f start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT , italic_f start_POSTSUBSCRIPT 2 end_POSTSUBSCRIPT end_POSTSUBSCRIPT ,
where
M
𝑀
M
italic_M
is defined as the global compute power in MACs/cycle.
Finally, Equation (
8
) can be simplified to
(12)
T
prefill
=
1
f
⁢
r
⁢
e
⁢
q
⁢
N
⁢
(
1
+
1
C
)
⁢
l
⁢
d
2
M
,
subscript
𝑇
prefill
1
𝑓
𝑟
𝑒
𝑞
𝑁
1
1
𝐶
𝑙
superscript
𝑑
2
𝑀
T_{\text{prefill}}=\frac{1}{freq}N\left(1+\frac{1}{C}\right)\frac{ld^{2}}{M}\,,
italic_T start_POSTSUBSCRIPT prefill end_POSTSUBSCRIPT = divide start_ARG 1 end_ARG start_ARG italic_f italic_r italic_e italic_q end_ARG italic_N ( 1 + divide start_ARG 1 end_ARG start_ARG italic_C end_ARG ) divide start_ARG italic_l italic_d start_POSTSUPERSCRIPT 2 end_POSTSUPERSCRIPT end_ARG start_ARG italic_M end_ARG ,
which shows the overall latency with work balancing.
We can obtain the latency for the decode stage using a similar analysis.
To derive the optimal
M
𝑀
M
italic_M
for a given model, we devise a linear search algorithm to identify the maximum available
M
𝑀
M
italic_M
based on the constraints in Equations (
2
), (
3
), and (
6
).
Notice the optimal
M
𝑀
M
italic_M
represents an upper bound of the compute power.
In practice, we also need to consider the routing issue to adjust the actual achievable
M
𝑀
M
italic_M
as discussed in §
5.2
.
3.4.
Distributed Inference
As a single FPGA may not be sufficient to process some extremely large models, we next extend our modeling to multiple FPGAs.
We first characterize the communication cost between two FPGAs and discuss the impact of different parallelism schemes.
3.4.1.
Communication.
Various methods exist for facilitating inter-FPGA communication, including communication through the host, PCI-E Peer-to-Peer (P2P), and on-device Ethernet.
We mainly consider the third approach since it does not necessitate orchestration from the host and provides higher bandwidth compared to other alternatives.
For example, the AMD Alveo U280 FPGA provides two QSFP ports
(
qsfp,
)
, each capable of carrying 100 Gb/s Ethernet data over optical fibers, which ensures robust and high-speed inter-FPGA communication.
Most of the time, we cannot fully utilize the network bandwidth and need to pay for the package header overheads.
Suppose the theoretical network bandwidth between two FPGA devices is
B
𝐵
B
italic_B
bits per second (bps), and the efficiency of the network is
α
𝛼
\alpha
italic_α
, so we can have the effective bandwidth as
α
⁢
B
𝛼
𝐵
\alpha B
italic_α italic_B
, where
α
𝛼
\alpha
italic_α
can be obtained through network benchmarking.
3.4.2.
Parallelization Schemes.
As mentioned in §
2.2
, we have various parallelization schemes when considering multiple devices.
We first analyze tensor parallelism (TP).
As shown in Figure
3
, the parameters of the linear operations are partitioned across different devices. For example, suppose the weight parameters of the two FFN layers
f
1
subscript
𝑓
1
f_{1}
italic_f start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT
and
f
2
subscript
𝑓
2
f_{2}
italic_f start_POSTSUBSCRIPT 2 end_POSTSUBSCRIPT
are
A
𝐴
A
italic_A
and
B
𝐵
B
italic_B
, then we can partition
A
𝐴
A
italic_A
along its column and partition
B
𝐵
B
italic_B
along its row, and obtain
σ
⁢
(
Z
⁢
A
)
⁢
B
=
σ
⁢
(
Z
⁢
[
A
1
A
2
]
)
⁢
[
B
1
B
2
]
=
σ
⁢
(
Z
⁢
A
1
)
⁢
B
1
+
σ
⁢
(
Z
⁢
A
2
)
⁢
B
2
,
𝜎
𝑍
𝐴
𝐵
𝜎
𝑍
matrix
subscript
𝐴
1
subscript
𝐴
2
matrix
subscript
𝐵
1
subscript
𝐵
2
𝜎
𝑍
subscript
𝐴
1
subscript
𝐵
1
𝜎
𝑍
subscript
𝐴
2
subscript
𝐵
2
\sigma(ZA)B=\sigma\left(Z\begin{bmatrix}A_{1}&A_{2}\end{bmatrix}\right)\begin{%
bmatrix}B_{1}\\
B_{2}\end{bmatrix}=\sigma(ZA_{1})B_{1}+\sigma(ZA_{2})B_{2}\,,
italic_σ ( italic_Z italic_A ) italic_B = italic_σ ( italic_Z [ start_ARG start_ROW start_CELL italic_A start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT end_CELL start_CELL italic_A start_POSTSUBSCRIPT 2 end_POSTSUBSCRIPT end_CELL end_ROW end_ARG ] ) [ start_ARG start_ROW start_CELL italic_B start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT end_CELL end_ROW start_ROW start_CELL italic_B start_POSTSUBSCRIPT 2 end_POSTSUBSCRIPT end_CELL end_ROW end_ARG ] = italic_σ ( italic_Z italic_A start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT ) italic_B start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT + italic_σ ( italic_Z italic_A start_POSTSUBSCRIPT 2 end_POSTSUBSCRIPT ) italic_B start_POSTSUBSCRIPT 2 end_POSTSUBSCRIPT ,
where
σ
𝜎
\sigma
italic_σ
is the GeLU function.
Therefore, apart from partitioning
A
𝐴
A
italic_A
and
B
𝐵
B
italic_B
, we need to insert an all-reduce operation to aggregate the partial results on each device to ensure correctness.
The partitioned parameters will be stored on different devices.
For example,
A
1
subscript
𝐴
1
A_{1}
italic_A start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT
will be on the first FPGA, and
A
2
subscript
𝐴
2
A_{2}
italic_A start_POSTSUBSCRIPT 2 end_POSTSUBSCRIPT
will be on the second FPGA.
A similar partition scheme can be applied for MHA, and we refer the readers to
(
shoeybi2019megatron,
)
for more details.
Based on this partition scheme, TP requires two all-reduce operations within one Transformer layer.
However, these communicative operations are implemented in a blocking way.
Figure
5
(a) shows the subsequent FFN module needs to wait for the completion of the all-reduce process before it can conduct computation
(
wang2023overlap,
)
.
Notice that the all-reduce operation only involves fetching results from other devices and adding the result to its local tensor.
Given that the output of MHA is a sequential stream, we can perform elementwise addition in a non-blocking manner.
As soon as the kernel receives enough data, it can initiate data transfer to other devices without waiting for the remaining data to be computed.
This leads to substantial synchronization time savings as shown in Figure
5
(b).
Figure 5
.
Blocking and non-blocking all-reduce in TP. The latency of different stages is not drawn to scale.
Since the size of the output tensor of MHA and FFN are both
l
⁢
d
𝑙
𝑑
ld
italic_l italic_d
, the communication time for one all-reduce is
(13)
T
comm
=
l
⁢
d
⁢
b
A
/
(
α
⁢
B
)
.
subscript
𝑇
comm
𝑙
𝑑
subscript
𝑏
𝐴
𝛼
𝐵
T_{\text{comm}}=ldb_{A}/(\alpha B)\,.
italic_T start_POSTSUBSCRIPT comm end_POSTSUBSCRIPT = italic_l italic_d italic_b start_POSTSUBSCRIPT italic_A end_POSTSUBSCRIPT / ( italic_α italic_B ) .
As we have already implemented dataflow inside a device, pipeline parallelism (PP) essentially extends the dataflow to
p
2
subscript
𝑝
2
p_{2}
italic_p start_POSTSUBSCRIPT 2 end_POSTSUBSCRIPT
devices with a tensor of size
l
⁢
d
𝑙
𝑑
ld
italic_l italic_d
communicated in between.
Here, we only split the pipeline between two Transformer layers so the results of the previous device can be directly streamed to the next device in the same PP group.
Notice TP and PP can be combined to conduct model inference
(
narayanan2021megatronv2,
)
, and the latency of Equation (
8
) becomes
(14)
T
prefill
=
1
f
⁢
r
⁢
e
⁢
q
⁢
N
p
2
⁢
C
⁢
(
l
⁢
d
2
p
1
⁢
M
k
+
p
2
⁢
C
⁢
max
⁡
(
l
⁢
d
2
p
1
⁢
M
k
,
l
2
⁢
d
p
1
⁢
M
a
1
,
l
⁢
d
⁢
d
FFN
p
1
⁢
M
f
1
,
T
mem
,
T
comm
)
)
,
subscript
𝑇
prefill
1
𝑓
𝑟
𝑒
𝑞
𝑁
subscript
𝑝
2
𝐶
𝑙
superscript
𝑑
2
subscript
𝑝
1
subscript
𝑀
𝑘
subscript
𝑝
2
𝐶
𝑙
superscript
𝑑
2
subscript
𝑝
1
subscript
𝑀
𝑘
superscript
𝑙
2
𝑑
subscript
𝑝
1
subscript
𝑀
subscript
𝑎
1
𝑙
𝑑
subscript
𝑑
FFN
subscript
𝑝
1
subscript
𝑀
subscript
𝑓
1
subscript
𝑇
mem
subscript
𝑇
comm
\small T_{\text{prefill}}=\frac{1}{freq}\frac{N}{p_{2}C}\left(\frac{ld^{2}}{p_%
{1}M_{k}}+p_{2}C\max\left(\frac{ld^{2}}{p_{1}M_{k}},\frac{l^{2}d}{p_{1}M_{a_{1%
}}},\frac{ldd_{\text{FFN}}}{p_{1}M_{f_{1}}},T_{\text{mem}},T_{\text{comm}}%
\right)\right)\,,
italic_T start_POSTSUBSCRIPT prefill end_POSTSUBSCRIPT = divide start_ARG 1 end_ARG start_ARG italic_f italic_r italic_e italic_q end_ARG divide start_ARG italic_N end_ARG start_ARG italic_p start_POSTSUBSCRIPT 2 end_POSTSUBSCRIPT italic_C end_ARG ( divide start_ARG italic_l italic_d start_POSTSUPERSCRIPT 2 end_POSTSUPERSCRIPT end_ARG start_ARG italic_p start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT italic_M start_POSTSUBSCRIPT italic_k end_POSTSUBSCRIPT end_ARG + italic_p start_POSTSUBSCRIPT 2 end_POSTSUBSCRIPT italic_C roman_max ( divide start_ARG italic_l italic_d start_POSTSUPERSCRIPT 2 end_POSTSUPERSCRIPT end_ARG start_ARG italic_p start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT italic_M start_POSTSUBSCRIPT italic_k end_POSTSUBSCRIPT end_ARG , divide start_ARG italic_l start_POSTSUPERSCRIPT 2 end_POSTSUPERSCRIPT italic_d end_ARG start_ARG italic_p start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT italic_M start_POSTSUBSCRIPT italic_a start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT end_POSTSUBSCRIPT end_ARG , divide start_ARG italic_l italic_d italic_d start_POSTSUBSCRIPT FFN end_POSTSUBSCRIPT end_ARG start_ARG italic_p start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT italic_M start_POSTSUBSCRIPT italic_f start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT end_POSTSUBSCRIPT end_ARG , italic_T start_POSTSUBSCRIPT mem end_POSTSUBSCRIPT , italic_T start_POSTSUBSCRIPT comm end_POSTSUBSCRIPT ) ) ,
where
p
1
subscript
𝑝
1
p_{1}
italic_p start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT
and
p
2
subscript
𝑝
2
p_{2}
italic_p start_POSTSUBSCRIPT 2 end_POSTSUBSCRIPT
are the size of a TP group and a PP group
(
shoeybi2019megatron,
)
.
Additionally, the memory requirements of Equations (
3
) and (
5
) need to be divided by
p
1
subscript
𝑝
1
p_{1}
italic_p start_POSTSUBSCRIPT 1 end_POSTSUBSCRIPT
to satisfy the constraints of multiple devices.
Notice we only discuss two basic parallelism schemes for Transformer models.
Some recent works may partition the sequence dimension and leverage reduce-scatter and all-gather to reduce the overheads of all-reduce
(
narayanan2021megatronv2,
;
korthikanti2022reducing,
)
.
The communication time can be similarly analyzed, and we will not discuss them here.
The optimal parallelism scheme on multiple devices
(
pope2022googleinf,
;
colin2022unity,
;
zheng2022alpa,
;
miao2022galvatron,
;
xie2022optimalplacement,
)
is out of the scope of this paper, and we will leave it as future works.

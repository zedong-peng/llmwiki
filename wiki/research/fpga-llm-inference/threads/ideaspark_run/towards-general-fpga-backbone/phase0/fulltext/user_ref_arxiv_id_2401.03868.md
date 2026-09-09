# user_ref:arxiv_id:2401.03868

paper_id: user_ref:arxiv_id:2401.03868
tier: U
source_used: html_arxiv
warning: none

## Intro

Figure 1.
FlightLLM on Alveo U280 FPGA outperforms NVIDIA V100S GPU
(using vLLM
(Kwon et al
.
,
2023
)
and SmoothQuant
(Xiao et al
.
,
2023
)
)
with better performance and cost efficiency.
Recently, we have witnessed the rapid development and significant impact of Large Language Models (LLMs)
(Bommasani et al
.
,
2021
; Wei et al
.
,
2022
)
.
LLMs demonstrate amazing power to understand all the users’ input requests (
prefill
stage) and generate accurate responses token-by-token (
decode
stage).
LLMs are being widely used in latency-sensitive scenarios
(Naveed et al
.
,
2023
)
,
such as
code completion
(Wang et al
.
,
2023a
)
,
real-time chatbots
(Chen et al
.
,
2023b
; Thirunavukarasu et al
.
,
2023
)
, customer support
(Jeong,
2023
)
, online legal advice
(Cui et al
.
,
2023
)
, and beyond.
The latency is critical for a good user experience, and the batch size is usually set as 1 to meet the real-time requirement.
However, current LLMs suffer from both heavy computation and memory overheads because of the explosive growth model size of LLMs. Taking GPT-3
(Brown et al
.
,
2020
)
as an example, it has 175 billion parameters (
i.e.
, 350GB in FP16), requiring about 660TOPS of computation amount to complete a single inference.
Model compression methods
(Deng et al
.
,
2020
)
(
e.g.
, sparsification, quantization, etc.) are commonly applied to address the above issues.
However, the unique computation schemes of these methods are not efficiently supported by current hardware platforms, like GPUs, for LLMs.
From the computation perspective, current GPUs only support structured sparsity (
e.g.,
2:4 sparsity), leading to significant algorithm accuracy loss of LLMs
(Frantar and Alistarh,
2023
)
.
In contrast, the unstructured sparsity ensuring algorithm accuracy cannot bring end-to-end acceleration for LLMs.
For example, the 75% unstructured sparsity only leads to negligible end-to-end speedup
(Feng et al
.
,
2023
)
.
From the memory perspective, quantization and large on-chip memory can reduce data access.
Recent algorithm studies
(Kim et al
.
,
2023
; Dettmers et al
.
,
2022a
)
are pushing the limit of bit-width with mixed-precision quantization.
However, the alignment feature of GPU’s cache and SIMD architecture requires homogeneous bit-widths of LLM parameters for weight access reduction
(Xiao et al
.
,
2023
)
.
Compounding the issue, GPU’s KB-scaled share memory of SMs cannot hold all the activations for LLM text generation.
FPGAs are potential solutions to accelerate LLM inference and explore the benefits brought by model compression, which has been proven in previous deep learning models
(Guo et al
.
,
2017
; Wang et al
.
,
2022
; Gong et al
.
,
2022
; Sun et al
.
,
2022
; Zhang et al
.
,
2021
)
. However, efficient LLM inference on FPGAs needs to solve the following challenges (Fig.
2
):
•
Low computation efficiency.
Flexible sparsity patterns (
e.g.,
block sparsity
(Zaheer et al
.
,
2020
)
, N:M sparsity
(Chen et al
.
,
2023a
)
, etc.) in LLM leads to low computation efficiency.
•
Underutilized memory bandwidth.
The
decode
stage of LLM repetitively accesses fine-grained data from off-chip memory, leading to underutilized bandwidth (
29-43%
).
•
Large compilation overheads.
The dynamic sparsity patterns and input lengths of LLMs constitute a large design space. For example, generating instructions for 2048 input token length results in
∼
similar-to
\sim
∼
TB storage overhead on FPGAs.
Figure 2.
Three challenges of LLM inference on FPGAs, and the corresponding solutions in FlightLLM.
In this paper, we propose
FlightLLM
, enabling efficient LLMs inference with a complete mapping flow on FPGAs
(Fig.
1
)
.
FlightLLM innovatively points out that the computation and memory overhead of LLMs can be solved by utilizing FPGA-specific resources (
e.g.
, DSP48 and heterogeneous memory hierarchy).
To address the challenges of low computation efficiency, FlightLLM exploits a configurable sparse DSP chain. We introduce a flexible cascaded DSP48 architecture to support different sparsity patterns with high computation efficiency (
i.e.
, runtime DSP utilization).
To tackle the underutilized memory bandwidth, FlightLLM proposes an always-on-chip decode scheme. Activations reside in the on-chip memory during the
decode
stage with the support of mixed-precision quantization.
To reduce the compilation overhead, FlightLLM proposes a length adaptive compilation method. Instructions for consecutive input token length are grouped, and the total storage overhead for instructions can be reduced.
The main contributions of this paper are as follows.
•
We propose a configurable sparse DSP chain to support different sparsity patterns. FlightLLM improves the computation efficiency by 1.6
×
\times
×
with block-wise and N:M sparsity.
•
We propose an always-on-chip decode scheme with mixed-precision support. FlightLLM boosts the memory bandwidth from
35.6%
to 65.9%.
•
We propose a length adaptive compilation method to reduce the instruction storage overhead by 500
×
\times
×
(
∼
similar-to
\sim
∼
GB), enabling deploying real-world LLMs onto FPGAs.
We implement FlightLLM on the Xilinx Alveo U280 FPGA
1
1
1
Artifact is available at:
https://zenodo.org/doi/10.5281/zenodo.10422477
. Evaluated on the OPT-6.7B and LLaMA2-7B, FlightLLM achieves better end-to-end latency than NVIDIA V100S GPU
using vLLM
(Kwon et al
.
,
2023
)
and SmoothQuant
(Xiao et al
.
,
2023
)
under the batch size of one
. Besides, FlightLLM outperforms NVIDIA V100S and A100 GPU with 6.0
×
\times
×
and 4.2
×
\times
×
higher energy efficiency, and 1.8
×
\times
×
and 1.4
×
\times
×
better cost efficiency on average, respectively. When evaluated on the latest Versal VHK158 FPGA, FlightLLM beats NVIDIA A100 with 1.2
×
\times
×
higher throughput.

## Method

Figure 4.
The overall architecture of FlightLLM, including task scheduler, memory controller and computing cores.
3.1.
Overall Architecture
We design a high-performance FPGA-based accelerator for generative LLMs by making full use of FPGA resources. Combined with compression techniques like sparsification and quantization, FlightLLM can effectively accelerate the generative LLMs and reduce the inference overhead.
As shown in Fig.
4
, the overall hardware architecture of FlightLLM mainly includes a task scheduler, memory controller, and multiple computing cores (short as cores).
The accelerator uses model parallelism on multiple cores to complete the LLM inference task. The task scheduler assigns tasks to different cores and controls data synchronization.
Figure 5.
The unified Matrix Processing Engine (MPE) can perform multiple types of matrix multiplications. (a) MPE includes multiple Matrix Processing Units (MPUs), which are composed of multiple Vector Processing Units (VPUs). By configuring the MPU, the MPE can support both (b) matrix-matrix multiplication (MM) mode and (c) matrix-vector multiplication (MV) mode. (d) We utilize DSP resources on the FPGA to implement the VPU.
The components of each core include the unified Matrix Processing Engine (MPE), Memory Management Unit (MMU), Special Function Unit (SFU), and Instruction Scheduler. The instruction scheduler decodes the input instructions and schedules different hardware units to perform computations. The main functions of the remaining hardware units are as follows:
MPE
handles all matrix (
i.e.
, dense and sparse) operations in LLMs. MPE utilizes the configurable sparse DSP chain to reduce the hardware overhead on FPGA.
MMU
reduces memory access overheads by designing customized quantization units for low-bit mixed-precision and optimizing data placement for off-chip memory.
SFU
handles miscellaneous operations (
e.g.
, Softmax, etc.) besides matrix processing operations. It also provides an additional data path to share data with other SFUs in different cores, accelerating the MV operation.
3.2.
Unified Matrix Processing Engine
Although sparsification can bring huge theoretical benefits to LLM inference, they cannot directly achieve these benefits on existing architectures. To maximize the benefits of sparsification, we design the unified Matrix Processing Engine (MPE) to handle all operations related to matrix computation, including General Matrix Multiplication (GEMM), Sparse Matrix-Matrix multiplication (SpMM), General Matrix-Vector multiplication (GEMV), Sparse Matrix-Vector multiplication (SpMV), and Sampled-Dense-Dense Matrix Multiplication (SDDMM). As shown in Fig.
5
(a), the MPE includes multiple Matrix Processing Units (MPUs), which transfer weights from the weight buffer using the streaming approach. The activation buffer and the global buffer store the input and output activations of the MPE, respectively.
By configuring the MPU, the MPE can support both matrix-matrix multiplication (MM) (Fig.
5
(b)) and matrix-vector multiplication (MV) mode (Fig.
5
(c)). The MPU is composed of multiple vector processing units (VPUs). The VPU is the basic component in the MPE, which performs the dot product of two vectors.
We build the unified MPE to support all the five operator on the same hardware achitecture. FlightLLM overcomes the challenge of low computational efficiency through hardware/software co-design.
To do this, we first introduce the MPU, which exploits configurable sparse DSP chain to reduce hardware overhead while supporting sparse reduction. We use the MM mode as an example to illustrate the main idea and the implementation of MPU. Then, we re-design MPE’s parallel scheme to maximize the performance in the MV mode. Finally, we introduce the SDDMM support through simple instruction scheduling.
3.2.1.
MPU Design
In transformer-based LLMs, sparsification methods including sparse attention and weight pruning are widely used to accelerate the LLM inference.
The sparse pruning generates sparse matrix, whose densities and sparse patterns are uncertain. It brings great challenges to hardware design, especially for FPGA-based architectures that use the fixed DSP48 as the multiplication unit. Existing work introduces large additional hardware architectures to support sparse computations, which leads to a significant increase in hardware resources (about 5
×
\times
×
(Srivastava et al
.
,
2020
)
). Without proper architectural design, the benefit of sparsification is weakened.
We utilize the DSP48 engine on FPGA to support sparse operations.
In order to reduce the hardware overhead, previous work cascades the DSPs to take full advantage of the hardware resources in DSP48. DSP cascading makes the most use of the accumulator, the result carry-out port, and the result carry-in port, improving the hard-core utilization. However, the fully cascaded DSP architecture are not friendly to sparse computation since the cascaded chain is a fixed path.
In FlightLLM, we propose a
configurable sparse DSP chain (CSD-Chain)
to supplement the fixed DSP chain. In the CSD-Chain, a long DSP chain is divided into several DSP groups. A DSP group (DG) has several DSP48 cores, that are cascaded in a fixed manner.
We pack two INT8 MACs on DSP48
(wp4,
2017
)
.
Different DGs are cascaded with a configurable path. A VPU is made up of a CSD-Chain and a MPU consists of several VPUs.
Fig.
5
(d) shows the architecture of the CSD-Chain based VPU. Each DG has two DSP48 cores. We use configurable cascading to support sparse matrix operations by adding three units to the fixed DSP chain.
Sparse Mux
. As shown in Fig.
5
(d), two activations (A and B) are delivered to one DSP48 core simultaneously for weight reuse. Before the delivery, they are sent to a sparse MUX unit. In the sparse MUX unit, each activation is selected from multiple inputs according to the sparse index (shown in Fig.
5
(b)). With this sparse-based multiplexer, only nonzero inputs are sent to the DSP48 core.
Reduction Node (RN)
. Compared to GEMM operations, calculating SpMM may produce more outputs, as demonstrated in Fig.
6
(b). Thus, DSPs are grouped in our design to implement non-breaking MAC and a reduction node are inserted at the end of a DG. When a SpMM operation wants to generate multiple outputs, the RN will break the configurable cascade path between DGs, and calculate the output. Other DGs on the CSD-Chain will start a new SpMM computation by selecting zero in the Z-MUX.
Overflow Adjust Unit (OAU)
. When a DSP48 shares a weight with two activations, only 18 bits can be accessed for each activation. As a result, a long cascade accumulation may overflow. Therefore, we adjust the output data before sending it to the next DG. In the overflow adjust unit, the result is split into a most significant part (MSP) and a least significant part (LSP).
The LSP cascades to the next DSP48 with limited bits to avoid accumulation overflow. The MSP are delivered to the RN in the next DG to calibrate the output result.
In this way, all accumulators in DSP48 are fully utilized. Since a 18-bit integer will never overflow if no more than eight 16-bit integer are accumulated, the OAU is skipped with no more than eight DSP48 cores.
Due to the configurable cascade path, VPU with the CSD-Chain can efficiently work on both dense and sparse multiplications.
As shown in Fig.
6
, all DSP48 cores are fully used in both cases. The only difference is that the RN in sparse case will break the CSD-Chain into two individual DSP chains to execute two different MACs and produce two outputs.
Supporting sparse matrix multiplication could improve the computation efficiency. But arbitrary sparsity may cause data mismatch between different DGs, leading to unexpected efficiency decrease.
Existing work shows that N:M sparse pattern is a promising sparsification method. It maintains the same sparsity ratio within each matrix block, and allocates different sparsity ratios among different matrix blocks. Where M is an integer power of 2, and N is the partial factor of M. For example, M=16, N=0, 2, 4, 8, 16. The N:M sparse method restricts the number and position of nonzero elements while maintaining flexible sparsity. It can be easily mapped to a CSD-Chain. For a N:M sparse architecture, a CSD-Chain can be splited into N groups. Each DSP will select one input from M inputs. In each cycle, the entire CSD-Chain can produce one MAC output in dense case and N MAC outputs in N:M sparse case. Fig.
6
shows the case of a VPU supporting 2:4 sparse pattern.
Figure 6.
By configuring the VPU, the MPE can support both (a) dense and (b) sparse cases.
3.2.2.
Matrix-Vector Multiplication Analysis
We explore the hyper-parameter space of compute tiling to fully utilize the off-chip memory bandwidth.
We model the memory access time
T
m
⁢
e
⁢
m
subscript
𝑇
𝑚
𝑒
𝑚
T_{mem}
italic_T start_POSTSUBSCRIPT italic_m italic_e italic_m end_POSTSUBSCRIPT
and computing time
T
c
⁢
m
⁢
p
subscript
𝑇
𝑐
𝑚
𝑝
T_{cmp}
italic_T start_POSTSUBSCRIPT italic_c italic_m italic_p end_POSTSUBSCRIPT
of general MM in equation
3
.
M
×
K
𝑀
𝐾
M\times K
italic_M × italic_K
,
K
×
N
𝐾
𝑁
K\times N
italic_K × italic_N
, and
M
×
N
𝑀
𝑁
M\times N
italic_M × italic_N
denote the shapes of two input matrices and one output matrix, respectively.
p
M
subscript
𝑝
𝑀
p_{M}
italic_p start_POSTSUBSCRIPT italic_M end_POSTSUBSCRIPT
,
p
K
subscript
𝑝
𝐾
p_{K}
italic_p start_POSTSUBSCRIPT italic_K end_POSTSUBSCRIPT
, and
p
N
subscript
𝑝
𝑁
p_{N}
italic_p start_POSTSUBSCRIPT italic_N end_POSTSUBSCRIPT
denote the three dimensions of computational parallelism in matrix computation.
B
⁢
W
𝐵
𝑊
BW
italic_B italic_W
denotes the off-chip bandwidth.
(3)
T
m
⁢
e
⁢
m
subscript
𝑇
𝑚
𝑒
𝑚
\displaystyle T_{mem}
italic_T start_POSTSUBSCRIPT italic_m italic_e italic_m end_POSTSUBSCRIPT
=
M
⋅
K
+
K
⋅
N
+
M
⋅
N
B
⁢
W
absent
⋅
𝑀
𝐾
⋅
𝐾
𝑁
⋅
𝑀
𝑁
𝐵
𝑊
\displaystyle=\frac{M\cdot K+K\cdot N+M\cdot N}{BW}
= divide start_ARG italic_M ⋅ italic_K + italic_K ⋅ italic_N + italic_M ⋅ italic_N end_ARG start_ARG italic_B italic_W end_ARG
T
c
⁢
m
⁢
p
subscript
𝑇
𝑐
𝑚
𝑝
\displaystyle T_{cmp}
italic_T start_POSTSUBSCRIPT italic_c italic_m italic_p end_POSTSUBSCRIPT
=
M
⋅
K
⋅
N
p
M
⋅
p
K
⋅
p
N
absent
⋅
𝑀
𝐾
𝑁
⋅
subscript
𝑝
𝑀
subscript
𝑝
𝐾
subscript
𝑝
𝑁
\displaystyle=\frac{M\cdot K\cdot N}{p_{M}\cdot p_{K}\cdot p_{N}}
= divide start_ARG italic_M ⋅ italic_K ⋅ italic_N end_ARG start_ARG italic_p start_POSTSUBSCRIPT italic_M end_POSTSUBSCRIPT ⋅ italic_p start_POSTSUBSCRIPT italic_K end_POSTSUBSCRIPT ⋅ italic_p start_POSTSUBSCRIPT italic_N end_POSTSUBSCRIPT end_ARG
To overlap the computation and memory access with double-buffer, we need to make sure that
T
m
⁢
e
⁢
m
<
T
c
⁢
m
⁢
p
subscript
𝑇
𝑚
𝑒
𝑚
subscript
𝑇
𝑐
𝑚
𝑝
T_{mem}<T_{cmp}
italic_T start_POSTSUBSCRIPT italic_m italic_e italic_m end_POSTSUBSCRIPT < italic_T start_POSTSUBSCRIPT italic_c italic_m italic_p end_POSTSUBSCRIPT
.
For MV operations,
M
=
1
𝑀
1
M=1
italic_M = 1
and
p
M
=
1
subscript
𝑝
𝑀
1
p_{M}=1
italic_p start_POSTSUBSCRIPT italic_M end_POSTSUBSCRIPT = 1
are set.
For the MV mode, we can iterate through the space to obtain a set of
[
p
K
′
,
p
N
′
]
superscript
subscript
𝑝
𝐾
′
superscript
subscript
𝑝
𝑁
′
[p_{K}^{\prime},p_{N}^{\prime}]
[ italic_p start_POSTSUBSCRIPT italic_K end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ′ end_POSTSUPERSCRIPT , italic_p start_POSTSUBSCRIPT italic_N end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ′ end_POSTSUPERSCRIPT ]
to guarantee the bound for double-buffer.
In other words, under the configuration of [
p
K
′
superscript
subscript
𝑝
𝐾
′
p_{K}^{\prime}
italic_p start_POSTSUBSCRIPT italic_K end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ′ end_POSTSUPERSCRIPT
,
p
N
′
superscript
subscript
𝑝
𝑁
′
p_{N}^{\prime}
italic_p start_POSTSUBSCRIPT italic_N end_POSTSUBSCRIPT start_POSTSUPERSCRIPT ′ end_POSTSUPERSCRIPT
], we can realize that the MPE can still fully utilize the off-chip memory bandwidth in MV mode, although the computing resources in the MPE are partially idle at this time (Fig.
5
(c)). By redesigning the computational parallelism, MPUs can maximize the execution performance of executing GEMV and SpMV on FPGAs.
3.2.3.
SDDMM Support
SDDMM is the key operator of the sparse self-attention layer. The block-wise sparsity of SDDMM can be used to reduce the amount of computation and improve the hardware energy efficiency. Therefore, we can treat SDDMM as multiple GEMMs in a block-wise manner. We only need to do some processing on the SDDMM operator with the instruction scheduler to efficiently complete the SDDMM computation on the MPE.
Figure 7.
SFU contains a MISC ALU, an instruction controller, a micro-operator controller, and a remote SFU access engine.
3.3.
Special Function Unit
Besides MM and MV computations, there are many other operations in LLMs, including softmax, layer normalization, etc. These miscellaneous (MISC) operations can be classified into two types: (a) Element-wise operation, which generates the result element by element (such as element-add and concat); (b) Two-phase operation, which will perform a reduction operation to get one or more parameters before the element-wise operation (such as softmax and layer normalization). Unlike MM and MV operations, these operations are not compute-intensive. Thus, we design a Special Function Unit (SFU) to handle all MISC operators, as shown in Fig.
7
. The SFU splits a MISC instruction into micro-operations, and delivers each micro-op to the ALU. The ALU will calculate the output according to the micro-op. All the input data is fetched from the MMU. For two-phase operations, the SFU will read an entire vector data from MMU to generate necessary parameters and read the same data again calculating the final output. For accuracy consideration, softmax and layer normalization operations are calculated in fp16 since the hardware cost of SFU is acceptable.
Hiding the computation latency of MISC operations is important to improve the end-to-end latency in LLMs. For MM and multi-head MV operations, MISC calculations can be hidden between different vectors. For MISC operations after single-head MV calculations, the SFU breaks the entire vector into several sub-vectors and performs MISC operations in fine granularity to hide the computation latency. In consideration of the scalability, multiple SFUs in different PEs may work together by accessing remote SFUs. A SFU can share parameters and calculation results with other SFUs. Thus, although a vector may be generated by different PEs simultaneously, the result could be sent to all other PEs without writing back to HBM. It reduces the end-to-end latency and the wire overhead on FPGA.

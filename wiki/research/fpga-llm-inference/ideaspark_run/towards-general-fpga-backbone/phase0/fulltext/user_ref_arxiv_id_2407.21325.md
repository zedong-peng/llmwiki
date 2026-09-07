# user_ref:arxiv_id:2407.21325

paper_id: user_ref:arxiv_id:2407.21325
tier: U
source_used: pdf_arxiv_pymupdf
warning: none

## Intro

Artificial Intelligence has captured keen interest and
worldwide attention in the past ten years [1-5]. This is mainly
associated with three pivotal advancements: First is the
exponential
escalation
in
computational
prowess,
which
mainly attributable to GPU; Second is the evolution of AI

## Method

for computer vision (CV), and the recurrent neural networks
for natural language processing (NLP); Third is the AI big data
[7,8], which serves as the foundational support for the training
of AI models, fueling their precision and efficacy. These
factors have coalesced to drive a transformative era in AI.
Since 2017, Transformer algorithm has rapidly become a
dominant force in the field of artificial intelligence in terms of
both NLP and CV research field [4-6]. By introducing the self-
attention mechanism, Transformer altered traditional sequence
modeling methods, no longer relying on convolutional neural
networks (CNNs) or recurrent neural networks (RNNs) for
feature extraction and sequence handling. This innovation not
only enhanced the parallelization capabilities of models,
making the training of large-scale models possible, but also
significantly improved model performance.
Following the success of Transformer, researchers began to
explore even larger models, which typically have billions or
more parameters, known as 'large language models' [9-11]. For
example, the GPT (Generative Pre-trained Transformer) series
of models from OpenAI, has showcased ability to understand
and generate high-quality human language [11]. Nowadays,
the large language models have begun integrating with other
modalities such as vision and audio, showing capable of
outstanding performance in cross-domain task. This interactive
capability makes AI assistants, chatbots, and virtual agents
more human-like and efficient [12-15]. In summary, large
language models not only enhance AI's language processing
capabilities but also advance broader technological progress in
AI, bringing revolutionary changes to industries such as
education, entertainment, healthcare, and business.
Nonetheless, the prevailing trend in contemporary AI
accelerator architectures, especially those geared towards the
demands of large language models, predominantly relies on the
GPU paradigm. This conventional design, while powerful,
exhibits inherent limitations that render it less than ideal for
deployment on edge devices. The constraints imposed by the
GPU architecture, such as high power consumption and
extensive computational overhead, pose significant challenges
to
the
practicality
and
efficiency
of
implementing
AI
capabilities at the network's periphery. Despite its attributes of
high flexibility and high-performance capabilities in specific
tasks, FPGA, a crucial component of heterogeneous computing,
receives scant mention. The FPGA based implementation of
LLM holds considerable promise for substantially enhancing
computational efficiency and performance [16-20]. However,
several critical challenges remain to be effectively addressed.
The first challenge within LLM is the heavy computation
and memory access [21, 22]. Large language models often
contain billions of parameters in matrix-matrix multiplication
(MatMUL) or vector-matrix multiplication (VMM). We often
refer to a model as LLM-6B or LLM-7B, where 6B or 7B
denotes the number of weight parameters in the matrix
multiplications. The sheer volume of parameters translates into
extensive memory requirements, making it difficult to fit these
This work was supported by STI 2030-Major Projects (2022ZD0210600),
National Natural Science Foundation of China (NSFC) (Grant No. 92464102,
62034007), Natural Science Foundation of Guangdong Province (Grant
2023B1515020051), Shenzhen Science and Technology Program (Grant No.
JCYJ20200109115210307). (Corresponding author: Hao Yu)
Mingqiang Huang and Ao Shen contribute equally in this work.
Mingqiang Huang is with Shenzhen Institute of Advanced Technology,
Chinese Academy of Sciences, Shenzhen 518055, China.
Ao Shen, Kai Li, Haoxiang Peng, Boyu Li, Yupeng Su and Hao Yu are
with School of Microelectronics, Southern University of Science and
Technology, Shenzhen 518055, China.(yuh3@sustech.edu.cn)

Fig. 1. (a) Architecture of the Transformer network and challenges in hardware design for Transformer-like accelerator. (b) Proposed CPU-FPGA
heterogeneous acceleration system for the large language model.
models into the memory of standard hardware. To address such
issue, several strategies have been developed, such as model
pruning and quantization. Existing solutions typically quantize
these weight parameters to INT4 format [21]. However, to
ensure computational accuracy, the activation functions in the
model remain in FP16 format. Therefore, the system requires
matrix
multiplications
using
FP16*INT4
format
in
the
FFN(Feed-Forward Neural Network) layers. Besides, despite
its theoretical advantages, sparse representation techniques
have yet to gain widespread traction within the industry
[23,24]. As such, there exists a clear opportunity of specialized
hardware components tailored to the unique requirements of
both sparse and INT4 quantized models. On the other hand, in
the
MHA
(Multi-Head
Attention)
block,
KVcache
is
dynamically generated as activation data, thus the matrix
multiplication involving KVcache requires FP16*FP16 format.
Therefore, it is highly desired to design mix-precision
computation elements for the acceleration of LLMs.
Another
challenge
lies
in
the
compilation
system,
specifically addressing the vast number of operators and
optimizing the linkage between them, which is crucial for
enhancing computational speed [25]. Current AI chips grapple

with the issue of non-uniform data formats for different
operators, particularly when dealing with deep learning models.
These models usually consist of a series of diverse operators:
CNN networks predominantly utilize linear operations such as
Matrix Multiplication, Convolution and Pooling operators [2];
while the Transformer networks heavily rely on complex
nonlinear operations such as Layer Normalization, Multi-Head
Attention Mechanisms (MHA), Embedding Lookups and
Positional Encoding [4,5]. Each operator potentially requires
distinct
data
formats
to
achieve
optimal
computational
efficiency. For instance, convolutional layers might prefer the
NHWC format (batch size, height, width, channels) or the
NCHW format (batch size, channels, height, width). While in
Transformer-like network, the diverse operators will bring
more complex data format requirements, especially for those
operators in MHA, which requires different operations for
different Heads. The absence of a standardized data format in
LLM means that when data transitions from one operator to
another, it often necessitates format transformations such as
reshaping
and
matrix
transposition.
These
additional
operations not only add to the computational load and consume
precious computational resources but also introduce extra time
lags, thereby reducing the overall system efficiency and
throughput.
Besides, in large language models, the operator graph,
which defines the computation flow, can be exceedingly
complex with hundreds/thousands of operators interconnected
in intricate ways. Ensuring that the transition from one
operator to another is seamless and efficient becomes a
significant challenge. Traditional compilers are designed to
optimize code for sequential execution, but the nature of deep
learning models requires a different approach. The dataflow
graphs of these models present opportunities for parallelism
and pipelining that traditional compilers might not fully exploit.
Therefore, specialized deep learning compilers and runtime
systems have emerged to address these unique requirements.
These compilers analyze the operator graph to identify
opportunities for optimization, such as operator fusion, which
combines adjacent operators into a single, more efficient
operation. Another critical aspect is the management of
memory access patterns. Efficiently handling the movement of
data between different memory hierarchies can significantly
impact performance. In summary, the compilation system for
large models must be sophisticated enough to handle the
complexity of the operator graph, optimize for parallelism, and
manage memory access efficiently.
In
this
work,
we
develop
an
efficient
CPU-FPGA
heterogeneous acceleration system for large language model,
where FPGA executes the core computational operators, and
CPU executes the dynamic compilation process. When it
comes
to
operational
efficiency,
our
innovative
design
proposal outperforms both conventional GPU chips and state-
of-the-art FPGA systems. Such superior performance is
achieved through a combination of optimized hardware
architecture, efficient data handling mechanisms, and advanced
dynamic compilation scheme.
The main contributions are:
1.
We analyzed the computational requirements of FFN
(Feed-Forward
Network)
and
MHA
(Multi-Head
Attention), and proposed high efficiency mix-precision
computation unit together with group systolic architecture.
Besides, log-scale structured-sparsity together with the
block-level quantization method are proposed to balance
the hardware efficiency and algorithm accuracy.
2.
We analyzed the compilation requirements in LLM and
devised unified and universal data format for all of the
operator and all of the high-dimensional tensor structures
within AI algorithms, enabling the system to execute the
operators swiftly and without any data rearrangement.
3.
We developed end-to-end compilation scheme, in which
dynamic compilation is used for different input token
length, and instruction pipeline strategy is used to reduce
latency. The scheme can dynamically compile all of the
operators and map the whole model on CPU-FPGA
heterogeneous system.
4.
Finally, the whole design has been successfully deployed
on AMD Xilinx VCU128 FPGA. Our result achieves
1.91×
higher
throughput
and
7.55×
higher
energy
efficiency than GPU, and 10~24% higher performance
than state-of-the-art FPGA accelerator of FlightLLM.

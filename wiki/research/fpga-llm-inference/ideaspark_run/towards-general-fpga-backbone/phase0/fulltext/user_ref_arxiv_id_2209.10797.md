# user_ref:arxiv_id:2209.10797

paper_id: user_ref:arxiv_id:2209.10797
tier: U
source_used: pdf_arxiv_pymupdf
warning: none

## Intro

Transformer [1] is a deep learning language model that
uses the mechanism of attention, which gives a different
weight of signiﬁcance to each part of the input data. By
solving the recursion and lack of global dependency problem
of recurrent neural network (RNN) [2] and long short-term
memory (LSTM) [3], the transformer is becoming the de facto
Language

## Method

"is"
"Hello, my name"
Input Tokens
"James"
"Smith"
"and"
Output Tokens
...
"."
Language
Model
Language
Model
Language
Model
Language
Model
...
Generation Stage
Summarization Stage
...
Figure 1.
Illustration of transformer-based text generation.
standard for natural language processing (NLP) applications
such as text generation [4], [5], text classiﬁcation [6], [7], and
machine translation [8], [9]. Among them, text generation,
broadly referred to as natural language generation (NLG),
is related to the automatic generation of human-readable
text by a computer. It has become of great importance in
emerging applications such as dialogue system [10], [11],
[12] and topic-to-essay generation [13], [14], [15], with a
rapid growth rate of 20% [16] in the NLG market. Among
transformer models, the Generative Pre-trained Transformer
(GPT) is widely used in cloud services, achieving remarkable
performance particularly in text generation applications.
In the text generation process, consisting of the summariza-
tion and generation stages, the language model continuously
generates sequential output words (i.e., output tokens) using
the input context made of multiple input words (i.e., input
tokens), as shown in Figure 1. In the summarization stage,
the language model processes a batch of input tokens with a
single run and generates a new output token. The generation
stage iterates the language model processing to generate the
subsequent output tokens, in which each iteration takes the
single output token from the previous iteration as input to
generate a single output token. Meanwhile, the language
model accumulates the contextual features throughout the
iterations. In current server platforms, GPU [17] is used to
accelerate text generation. Its massively parallel compute
units yield high performance in the summarization stage as
arXiv:2209.10797v1  [eess.SY]  22 Sep 2022

the input tokens can be computed simultaneously. However, a
signiﬁcant performance degradation occurs in the generation
stage because GPU is not suitable for sequential processing,
suffering from severe underutilization.
Several architectures [18], [19], [20], [21] have been pro-
posed to accelerate the transformer. The attention mechanism
[1], composed of matrix multiplication and softmax for
contextual understanding, has been their primary operation of
concern because it is the most computationally intensive task
in the transformer. However, a language service requires an
architecture that considers the entirety of the transformer
model. For datacenters to adopt the above accelerator
architectures, the server platforms would need CPU or extra
compute modules to cover the complete operations, which
would lead to large processing overhead. Therefore, a uniﬁed
and programmable architecture that can support the whole
GPT operations end-to-end is necessary.
In this paper, we propose DFX, a multi-FPGA acceleration
appliance that specializes in text generation workloads
covering end-to-end inference of variously sized GPT models.
To address the sequential characteristic of text generation,
DFX compute core is optimized for single token processing,
which is impracticable in GPU. It also uses an efﬁcient tiling
scheme and dataﬂow based on the characteristics of GPT for
maximum high bandwidth memory (HBM) [22] bandwidth
usage. To address the increasing model size, DFX uses
model parallelism on the multi-device system to increase the
physical number of compute cores that work in parallel while
evenly assigning full workload to each device. Furthermore,
we exploit FPGAs because the transformer-based model
continues to undergo modiﬁcations and expansions for
different language services in the datacenter. The FPGA-
based accelerator provides fully reprogrammable hardware to
support new operations and larger dimensions of the evolving
transformer with minimum cost for redesign when compared
to an ASIC-based accelerator.
The main contributions of our work are as follows.
• We identify that the generation stage of text generation
workload is the bottleneck on parallel hardware such as
GPU due to its sequential characteristic.
• We design a custom programmable compute core optimized
for the end-to-end acceleration of GPT inference with a
high hardware utilization.
• We utilize the full HBM bandwidth complemented with
an efﬁcient tiling scheme and dataﬂow based on the
characteristics of GPT to achieve low latency and high
throughput.
• We apply model parallelism and efﬁcient network to
the multi-FPGA system by evenly distributing the model
parameters to each FPGA in a way that requires minimal
data synchronization among FPGAs and achieves maximal
parallel computation.
• We build a multi-FPGA appliance with low upfront and
LM head
Token
Embedding
LM head
Token
Embedding
LM head
Token
Embedding
Positional 
Encoding
Generation Stage
"is"
"James"
"."
"Hello, my name"
..
..
..
Summarization Stage
Decoder Layer 1
Decoder Layer 1
Decoder Layer 1
Fully-
Connected
GELU
Fully-
Connected
Fully-
Connected
GELU
Fully-
Connected
Fully-
Connected
LayerNorm
Softmax
Fully-
Connected
LayerNorm
Softmax
Concat 
K, V
Input Tokens :
Output Tokens :
+
+
+
Feed-
Forward 
Network
Feed-
Forward 
Network
Feed-
Forward 
Network
Self-
Attention
Self-
Attention
Self-
Attention
Residual
LayerNorm
LayerNorm
Residual
Residual
LayerNorm
LayerNorm
Residual
Residual
LayerNorm
LayerNorm
Residual
Decoder Layer 2
Decoder Layer N
Decoder Layer 2
Decoder Layer N
Decoder Layer 2
Decoder Layer N
Vector
Vector
Vector
Matrix
Matrix
Matrix
ID
Emb 
Vector
vec0
0
vec1
1
...
...
vecn
n
WTE
Token 
ID
Vector
ID
Emb 
Vector
vec0
0
vec1
1
...
...
vecn
n
WTE
Token 
ID
Vector
Vector
Vector
Vector
Vector
Vector
Vector
Vector
Vector
Vector
Vector
Vector
Vector
n×emb 
1×emb 
1×emb 
1×emb 
1×emb 
1×emb 
Create Q, K, V
Concat K, V
Fully-
Connected
Softmax
MatMul
(S × V)
Masked MatMul
(Q × KT)
Multi-Head Attention
Create Q, K, V
Concat K, V
Fully-
Connected
Softmax
MatMul
(S × V)
Masked MatMul
(Q × KT)
Multi-Head Attention
Figure 2.
GPT-2 structure and illustration of summarization and generation
stages in text generation.
operating cost that accelerates transformer-based language
services, achieving multiple times better performance and
efﬁciency than the conventional GPU platform. We believe
this new hardware platform is promising for handling ever-
increasing text generation workloads in datacenters.

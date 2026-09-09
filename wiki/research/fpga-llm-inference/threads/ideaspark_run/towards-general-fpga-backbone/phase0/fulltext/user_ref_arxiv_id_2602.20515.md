# user_ref:arxiv_id:2602.20515

paper_id: user_ref:arxiv_id:2602.20515
tier: U
source_used: html_arxiv
warning: none

## Intro

Large language models (LLMs) have gained significant popularity in recent years for their exceptional performance across a wide range of natural language processing (NLP) tasks. Specifically, long-context inference is critical in tasks such as document summarization
[
12
,
2
]
, code generation
[
7
,
26
]
, and Q&A
[
25
,
23
]
. However, long-context inference incurs a huge computation cost due to self-attention that grows quadratically with context length (prompt length) in the prefill phase of LLM inference
[
21
]
. Recent works
[
28
,
8
,
24
,
3
,
9
]
target sparse attention, in which each token interacts with only a subset of tokens, resulting in a drastic reduction in computational requirements. Unlike weight compression and sparsification techniques such as N:M sparsity
[
17
]
and block sparsity
[
16
]
, which sparsify weight matrices, attention sparsity results in sparse attention scores during self-attention. State-of-the-art works
[
9
,
8
]
target dynamic sparsity in self-attention wherein the sparsity pattern varies for each input prompt. Additionally, for a given prompt, each attention head can exhibit a unique pattern.
Current works target GPUs for evaluating sparse attention algorithms due to the high computational capabilities they offer. However, sparse attention makes the inference memory-bound. This arises from two key factors. (1) Generating a specific set of tokens for each token (Sparse index generation) requires a data-dependent control flow with low compute intensity. This results in under-utilized compute resources and saturates the memory bandwidth on the GPU.
(2) Sparse attention requires each query to access a different subset of Key-Value (KV) vectors. Unlike dense attention where all queries access the complete KV cache
[
18
]
, sparse patterns cause each query to read different portions of the KV cache, preventing efficient data reuse.
Additionally, the high energy requirements of GPUs drive the consideration of energy-efficient platforms such as FPGAs. However, there has been limited exploration towards accelerating long-context LLM inference with dynamic attention sparsity on FPGAs.
Accelerating long-context LLM inference on an FPGA, however, faces substantial design challenges.
(1)
The naive design for sparse index generation results in large intermediary tensors. On-chip buffers are insufficient to hold these, and off-chip storage results in frequent access, contributing to increased latency.
(2)
The large size of the KV cache (
∼
\sim
3-4 GB) restricts it to off-chip storage. Ensuring efficient reuse of KV vectors across different queries is non-trivial, as the access is dependent on the sparsity pattern as opposed to naive streaming. Additionally, fetching vectors too early or too late can result in wasted bandwidth or compute stalls.
(3)
Long context inference involves multiple matrix multiplication operations. Current FPGA-based works
[
29
,
13
]
primarily rely on DSP-based multiplication. This bottlenecks the design as multiple matrix operations become largely sequential. We detail the challenges in Section-
III
.
Figure 1
:
FAST-Prefill Architecture
To address these challenges, we propose FAST-Prefill, an FPGA-based accelerator for efficient long-context LLM inference with dynamic sparse attention. The main contributions of the paper are summarized as follows:
•
To the best of our knowledge, we propose the first FPGA accelerator that targets dynamic sparse prefill-stage inference for long-context LLMs with W8A8 precision.
•
We propose a
streaming, memory-aware sparse index generation architecture
that computes block-level relevance scores through incremental aggregation, eliminating the need to generate large intermediate tensors. This transforms index generation from a generate-then-aggregate operation requiring
∼
\sim
4GB of intermediate storage, into a stream-and-accumulate operation requiring with
∼
\sim
4KB storage.
•
We propose a
liveness-driven custom cache
to store a small set of KV cache blocks. This analyzes sparse index patterns to prefetch KV cache blocks from off-chip memory (HBM) via efficient coordinated bursts.
•
The custom cache is
dual-tier
with a threshold-based admission policy that places high-reuse blocks of KV cache in the Hot tier and low-reuse blocks in the Cold tier to prevent cache thrashing.
•
We propose a hybrid Matrix Processing Unit (MPU) that includes systolic array grids for bit-plane matrix multiplication using LUTs, in addition to DSP-based systolic array grids.
•
Our implementation of FAST-Prefill on Xilinx Alveo U280 achieves up to 1.2-2.5
×
\times
improvement in Time To First Token (TTFT) over the implementation of dynamic sparse attention on Nvidia RTX A5000 GPU across context lengths of 4K-128K tokens. We also achieve 4.5
×
\times
energy efficiency over the GPU.
Figure 2
:
Prefill Workflow with Sparse Attention

## Method

In this section, we detail the challenges in accelerating long-context LLM inference on FPGA.
Challenge-1: Sparse index generation generates large intermediary tensors combined with irregular memory access to Key (K) vectors.
Computing sparse indices requires scoring all Key blocks against the last query-block vectors to identify the top-K most relevant blocks. Considering a context length of 128K tokens, this can produce 128
×
\times
128K per attention head, resulting in more than 2GB of intermediate storage. Additionally, operations such as softmax, exponentials, and block pooling produce 2GB of intermediate tensors. This is prohibitively large for on-chip storage, and frequent off-chip access explodes latency. Standard fusion techniques are not effective because they primarily fuse element-wise operations rather than operations with different dimensions.
Challenge-2: Sparsity pattern dependent KV cache access.
Reuse of KV cache blocks is dependent on the sparsity pattern corresponding to each attention head. This, neither purely streaming nor purely temporal, access pattern of KV cache blocks results in the following issues. (a) Naive prefetching along the memory hierarchy is ineffective as prefetch timing is critical. Prefetching a KV block too early can waste the limited on-chip resources, and prefetching the block too late results in pipeline stalls. (b) Fetching blocks on demand leads to many small off-chip memory reads, resulting in underutilized bandwidth and pipeline stalls. (c) Limiting the reuse of KV blocks across attention heads in the case of Group-Query-Attention (GQA) leads to independent fetching of the blocks, which increases memory traffic.
Challenge-3: Constrained Matrix multiplication throughput due to limited DSPs.
Long-context inference results in multiple block-sized matrix multiplications across various stages in the pipeline (QKV, Sparse Attention and FFN). Using DSPs limits the matrix multiplication architecture to about six 32x32 systolic arrays on U280 FPGA, insufficient for the large number of matmuls involved.

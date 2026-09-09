# user_ref:arxiv_id:2512.22219

paper_id: user_ref:arxiv_id:2512.22219
tier: U
source_used: html_arxiv
warning: none

## Intro

Enabling high-performance inference of ML models on GPUs is critical for modern AI applications, since inference latency directly affects both user experience and serving cost. Today’s ML systems generally express model computation as a tensor program structured as a directed acyclic graph, whose nodes denote tensor algebra operators (e.g., matrix multiplication) and whose edges represent tensors, i.e., the
n
n
-dimensional arrays produced and consumed by these operators.
Most existing systems execute each operator using a dedicated GPU kernel, either hand-optimized by domain experts
[
dao2023flash
,
ye2025flashinfer
]
or generated automatically by ML compilers
[
tillet2019triton
,
tvm
,
wu2025mirage
]
. However, this
kernel-per-operator
execution model limits several key cross-operator GPU optimizations.
First, modern GPUs impose an implicit
kernel barrier
between consecutive launches on the same stream to ensure that all threads from the previous kernel complete before any thread from the next kernel begins. While this mechanism correctly enforces data dependencies, it prevents
cross-operator software pipelining
and forces dependent operators to execute strictly sequentially. NVIDIA recently introduced
programmatic dependent launch
(PDL)
[
nvidia-pdl
]
, which allows partial overlap between kernels on the same stream. However, adopting PDL requires significant engineering effort, as it fundamentally alters kernel structure and control flow.
Second, the kernel-per-operator execution model prevents fine-grained compute-communication overlap. Since dependencies are represented only at the coarse granularity of operators, the runtime must enforce full-operator completion before launching dependent communication or computation.
For example, when a matrix multiplication is followed by an all-reduce in separate kernels, the all-reduce must wait for the entire matrix multiplication to complete, even though each fragment of the all-reduce depends only on a subset of the multiplication output. Exploiting such opportunities requires representing and enforcing dependencies at a granularity finer than individual kernels.
Finally, kernel-per-operator execution may require launching hundreds to thousands of kernels for each inference iteration. To reduce launch overhead, current systems rely heavily on
CUDA Graphs
, which capture a sequence of GPU operations and replay them with low overhead. However, CUDA Graphs are largely static: any changes to control flow, tensor shapes, or data dependencies require re-instantiating or modifying the captured graph, limiting their flexibility for the dynamic workloads commonly seen in model inference.
A promising approach to overcoming these limitations is to fuse all computation and communication of model inference into a single
mega-kernel
, also known as a
persistent kernel
.
In this design, the system launches one GPU kernel to execute the entire model, including layer computations and inter-GPU communication, without interruption.
Mega-kernels address the limitations of kernel-per-operator execution in several ways.
First, they eliminate repeated kernel launch overhead by replacing many operator-level launches with a single kernel invocation.
Second, by fusing
all
operators into one kernel, they enable cross-operator software pipelining, allowing data for the next operator to be prefetched while computation for the current operator is still in progress.
Third, they support fine-grained overlap of computation and inter-GPU communication, enabling concurrent execution that more effectively hides communication latency.
Despite these benefits, automatically transforming an ML model into a high-performance mega-kernel remains challenging. Existing ML systems—such as PyTorch
[
pytorch
]
, Triton
[
tillet2019triton
]
, and TVM
[
tvm
]
—do not support end-to-end mega-kernel generation.
Moreover, these systems rely on a fragmented ecosystem of specialized libraries: NCCL
[
nccl
]
or NVSHMEM
[
nvshmem
]
for communication, FlashInfer
[
ye2025flashinfer
]
or FlashAttention
[
dao2023flash
]
for attention, and CUDA or Triton for custom computation.
This fragmentation makes it difficult to unify the entire inference pipeline within a single kernel.
We present
Mirage Persistent Kernel
(MPK), the first compiler and runtime system that automatically transforms multi-GPU model inference into a high-performance mega-kernel.
MPK enables end-to-end kernel fusion with minimal developer effort: users can mega-kernelize a PyTorch model with only a few lines of code while achieving significant performance improvements compared to running the model in vanilla PyTorch with CUDA Graphs and
torch.compile
. MPK combines the performance benefits of mega-kernels with the usability of existing ML frameworks.
Figure 1:
An overview of MPK.
A key idea in MPK is to represent computation and inter-GPU communication at the granularity of individual streaming multiprocessors (SMs), rather than at the granularity of an entire GPU.
MPK introduces an
SM-level graph representation
, called
t
t
Graph, whose nodes denote
tasks
running on individual SMs and whose edges encode fine-grained dependencies between tasks.
This representation exposes additional parallelism and enables optimizations such as cross-operator software pipelining and fine-grained kernel overlap, which are difficult to realize in conventional kernel-per-operator execution models.
MPK realizes this idea using two key components shown in
Figure
˜
1
.
The MPK compiler.
The MPK compiler takes a tensor program and an inference configuration as input and automatically transforms the program’s computation graph into an optimized SM-level
t
t
Graph tailored to the given inference configuration and GPU architecture.
The compiler applies a range of optimizations, including event fusion, graph normalization, and graph linearization, to reduce synchronization overhead and improve the performance of generated
t
t
Graphs.
In addition, MPK automatically generates fast CUDA implementations for individual tasks using existing superoptimization techniques
[
wu2025mirage
]
, ensuring efficient SM-level execution.
In-kernel parallel runtime.
MPK executes the SM-level
t
t
Graph using an in-kernel parallel runtime embedded entirely within a mega-kernel, enabling fine-grained control over task execution and scheduling
without
additional kernel launches during model execution.
To achieve this goal, the runtime partitions a GPU’s SMs into
workers
and
schedulers
.
Each worker maintains a dedicated task queue and executes assigned tasks in a first-in-first-out order, while schedulers track dependencies across tasks and dispatch tasks once their prerequisites are satisfied.
The MPK runtime uses an
event-driven, fully asynchronous
execution model to keep GPUs highly utilized.
Finally, the runtime uses a
hybrid task-launch strategy
that combines just-in-time and ahead-of-time dispatch to minimize runtime overhead while preserving dynamic load balance across SMs.
Evaluation results.
We implement MPK as a PyTorch compiler backend: a PyTorch program can be compiled into an MPK mega-kernel with only a few lines of code changes.
We evaluate MPK on five widely used models across three generations of NVIDIA GPUs: A100, H100, and B200.
Even for workloads widely deployed and heavily optimized by existing kernel-per-operator systems, such as SGLang and vLLM for LLM serving, MPK outperforms current systems by 1.0–1.7
×
\times
on both single- and multi-GPU deployments, pushing LLM inference performance close to hardware limits.

## Method

This section introduces
t
t
Graph
, a representation that expresses the computation of a tensor program at the granularity of individual streaming multiprocessors (SMs). Unlike conventional computation graphs, which expose dependencies only between tensor operators,
t
t
Graph captures dependencies between SM-level units of work. This fine-grained representation exposes additional parallelism and enables optimizations such as cross-operator software pipelining and fine-grained kernel overlap, both of which are not supported by the existing kernel-per-operator execution model.
Figure
˜
4
illustrates an example
t
t
Graph, where each node represents either a
task
or an
event
. Each task—shown as a blue (or orange) rectangle—denotes a unit of computation (or communication) executed on a single SM. Each event—shown as a green circle—represents synchronization across tasks. Tasks and events alternate in the graph: every task only has outgoing edges to
triggering events
and incoming edges from
dependent events
. A task is ready for execution when its dependent events are all
activated
and notifies its triggering event upon completion. An event is activated once it has received notifications from all tasks associated with it.
This structure captures dependencies at a much finer granularity than traditional computation graphs. For example, multi-GPU LLM serving often involves a
MatMul
operator followed by an
AllReduce
operator (
Figure
˜
4
a). Existing systems generally execute these operators sequentially because coarse-grained kernel barriers synchronize entire kernels. In contrast, SM-level task graphs can represent precise task-level dependencies: since
AllReduce
performs element-wise communication and reduction, each of its tasks depends only on one corresponding
MatMul
task that produces its input tile. By inserting fine-grained events between dependent task pairs, MPK can overlap compute-intensive
MatMul
tasks with communication-intensive
AllReduce
tasks, improving overall GPU utilization.
Multiple
t
t
Graphs may represent the same computation graph.
Figure
˜
4
c shows an alternative but suboptimal
t
t
Graph where events capture only operator-level dependencies, analogous to traditional kernel barriers.
§
˜
4
describes how MPK generates high-performance task graphs by inferring
precise
data dependencies to maximize concurrency and minimize synchronization overheads.
Comparison with CUDA Graphs.
t
t
Graphs can be viewed as a lower-level extension of CUDA Graphs, sharing several structural similarities. Like CUDA Graphs,
t
t
Graphs are statically instantiated and encode explicit dependencies among operations. However, while CUDA Graphs capture dependencies only at the kernel level,
t
t
Graphs operate at the granularity of individual SM tasks and sub-kernel events. CUDA Graphs primarily describe kernel launch order and rely on stream semantics for synchronization, which confines overlap and fusion to kernel boundaries. In contrast,
t
t
Graphs explicitly model both intra- and cross-operator dependencies, enabling fine-grained synchronization across SMs and overlap of computation and communication within a single kernel. This design allows MPK to exploit parallelism that is inaccessible to CUDA Graphs and other kernel-level execution models.
Figure 5:
The MPK compiler workflow. In (b),
Q
Q
,
K
K
,
V
V
,
A
A
,
O
O
, and
R
R
denote the sets of tasks produced by decomposing the query projection, key projection, value projection, attention, output projection, and RMSNorm, respectively.
D
1
D_{1}
and
D
2
D_{2}
in (e) are dummy tasks inserted during
t
t
Graph normalization to ensure that each task has a single triggering event. Finally, (f) shows how MPK linearizes the
t
t
Graph and stores the resulting structure, where tasks and events use a uniform, canonical representation.

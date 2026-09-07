# user_ref:arxiv_id:2604.12618

paper_id: user_ref:arxiv_id:2604.12618
tier: U
source_used: html_arxiv
warning: none

## Intro

Dataflow architectures are suitable for workloads that require massive data movement and operations due to their low latency
[
1
,
18
,
11
]
.
Fundamentally, these architectures leverage task-level pipelining to allow distinct functions and loops to overlap in their execution, rather than running sequentially. Furthermore, they exploit efficient on-chip communication between tasks
[
44
,
42
]
, significantly reducing the overhead of frequent external memory accesses
[
6
,
28
]
.
FPGAs, with their reconfigurable logic and customizable data paths, are well-suited for implementing dataflow accelerators that process data in a streaming or pipelined manner
[
47
,
21
,
24
,
3
]
.
Note that while the term
dataflow
is also used to describe dynamic scheduling-based
dataflow
circuits
[
19
]
or
dataflow
mapping strategies like input/output stationary
[
8
]
, these concepts are conceptually orthogonal to the dataflow architecture discussed in this paper.
However, the high efficiency of dataflow accelerators comes at the expense of a complex design process using hardware description languages (HDLs). To simplify FPGA development, developers utilize high-level synthesis (HLS) to translate C/C++ code into HDL implementations automatically
[
9
]
.
Nevertheless, a notable gap still persists between HLS programming and efficient dataflow implementations.
Commercial HLS tools, such as AMD Vitis HLS
[
41
]
, provide basic dataflow scheduling primitives, i.e.,
the dataflow pragma
[
39
]
, to enable pipelined execution between loops or functions. However, this optimization works only if the coding styles satisfy stringent requirements
[
39
]
, which many handcrafted algorithms fail to meet. This mismatch hinders effective optimization or even leads to synthesis failures.
Consequently, developers must perform extensive code refactoring and optimization manually to convert algorithms into dataflow-feasible formats and produce dataflow accelerators.
Prior Research.
To reduce developing efforts, prior methods
enhance programming efficiency using domain-specific languages (DSLs)
[
22
,
40
,
46
]
, or directly parse C++ inputs or PyTorch models into intermediate representations (IRs)
[
43
,
16
,
49
]
.
They primarily focus on kernel computation optimization, with limited consideration for dataflow optimization. Recently, several compilers have been proposed for dataflow optimization across multiple kernels or tasks
[
44
,
7
,
5
,
42
]
, enabling automatic generation of dataflow accelerators.
However, these approaches fail to fully resolve potential issues (Fig.
2
) in the dataflow,
limiting their ability to further optimize code and exploit parallelism. As a result, the generated designs may suffer from suboptimal performance or even encounter deadlocks when deployed on FPGA boards.
Key Idea.
The performance of dataflow accelerators is influenced by multiple factors. Fundamentally, the input code must satisfy strict constraints to enable correct streaming execution (
correctness
). On top of that, achieving high-throughput communication necessitates effective optimization of communication buffers and careful alignment of computation patterns between adjacent tasks to enhance data transfer efficiency (
communication
).
Finally, balancing task latencies through techniques such as loop tiling, unrolling, and pipelining is essential for improving overall performance (
parallelism
).
The core problem is that these factors are deeply codependent, yet prior work typically handles them in a decoupled manner. This leads to conflicts where optimizing one aspect in isolation negatively impacts the others. For instance, aggressive code transformations to meet dataflow constraints may result in inefficient computation and memory access patterns that create a communication bottleneck. Conversely, communication or parallelism optimizations may violate dataflow constraints and produce invalid designs.
Moreover, the growing scale and structural complexity of modern DNNs further exacerbate the problem, making it increasingly difficult to construct deep, high-throughput pipelines for large models.
To overcome these issues, we build a compiler that jointly co-optimizes correctness, communication, and parallelism. Through advanced code analysis, versatile optimization techniques, and automated scheduling, the compiler performs coordinated transformations that harmoniously benefit all three aspects rather than creating conflicts, automatically generating high-performance accelerators for large-scale models.
Challenges.
Achieving the goal is challenging. Firstly, the input algorithm may violate dataflow constraints, resulting in
dataflow violations
that must be eliminated. At the coarse-grained level, existing HLS tools impose a strict single-producer-consumer constraint to enable dataflow optimization
[
39
]
. At the fine-grained level, producers and consumers must maintain consistent data access order and count to ensure correct and efficient streaming execution.
Although recent works attempt to address these violations
[
44
,
7
,
5
,
42
]
, their methods are difficult to fully eliminate all violations in large-scale models. Consequently, unresolved violations result in
discontinuous dataflow regions
, breaking end-to-end streaming (Fig.
2
, Issue 1).
Secondly, data is transferred through communication buffers, typically implemented as ping-pong buffers or FIFOs (First-In-First-Out), as shown in Fig.
1
.
To achieve high throughput, intermediate results must be produced and consumed just-in-time to prevent pipeline stalls.
This requires careful selection of buffer types.
Moreover, this idealized communication is often disrupted by other optimizations, such as violation elimination, which may unintentionally alter computation schedules and compromise communication efficiency. Without holistic coordination and advanced code analysis, such issues are easily overlooked
[
5
]
, resulting in
delayed buffer writes and performance degradation
(Fig.
2
, Issue 2).
Thirdly, improving dataflow performance requires balancing tasks through techniques such as loop tiling, unrolling, and pipelining. This becomes even more challenging in FIFO-based dataflow, as code optimizations affect data access patterns, requiring careful coordination between adjacent
producers and consumers to avoid new dataflow violations. Consequently, existing auto-scheduling methods for ping-pong-based dataflow
[
44
]
are not directly applicable. While some tools use manual scheduling
[
22
,
40
]
or nonlinear programming (NLP)-based methods
[
5
,
32
]
for FIFO-based dataflow, they lack effective pruning methods to handle the exponentially increasing design space. As a result, these approaches
fail to scale to large-scale models
.
Figure 1:
Dataflow execution with FIFO and ping-pong buffer. Numbers in (a) and (b) represent the data access order.
Our Solution.
To tackle the above challenges, we propose CODO, an open-source compiler that performs comprehensive dataflow optimizations and automatically generates high-performance accelerators. CODO resolves dataflow violations, ensures communication efficiency, and explores resource-aware parallelism strategies to guarantee balanced task execution for large-scale models.
TABLE I:
Comparison between representative compilers.
Feature
ScaleHLS
[
43
]
POM
[
46
]
Allo
[
7
]
HIDA
[
44
]
StreamHLS
[
5
]
StreamTensor
[
42
]
CODO
Compiler Front-end
PyTorch
DSL
PyTorch
DSL
PyTorch
PyTorch
PyTorch
Coarse-grained Violation Elimination
Limited
Manual
Manual
✔
✔
✔
✔
Fine-grained Violation Elimination
✘
✘
✘
✘
Limited
Limited
✔
Efficient Communication Buffer
✘
✘
✔
✔
✘
✘
✔
Resource-aware Node Balancing
✘
✘
✘
✘
✘
✘
✔
Automated Scheduling or DSE
✔
✔
✘
✔
✔
✔
✔
On-board Verification
✘
✘
✔
✘
✘
✔
✔
Open Source Project
✔
✔
✔
✔
✔
✘
✔
•
We present an end-to-end compiler that automatically transforms an input algorithm into high-quality dataflow accelerators, along with the host code.
•
We eliminate both coarse- and fine-grained dataflow violations and enable efficient data communication via on- and off-chip optimizations.
•
We propose an automated scheduling method that rapidly determines suitable parallelism strategies with high resource efficiency to generate a high-performance design.
•
We perform synthesis and on-board evaluations. CODO achieves
3.7
×
3.7\times
to
33.8
×
33.8\times
speedup on DNN models in synthesis and an average speedup of
7.3
×
7.3\times
for DNNs and
2.07
×
2.07\times
for GPT-2 on-board compared to SOTA compilers.

## Method

CODO is built on the MLIR
[
23
]
compilation framework. Figure
3
shows the compilation flow. The framework takes compute kernels implemented in C++ or PyTorch models as input, which are translated into MLIR dialects via Polygeist
[
26
]
and Torch-MLIR
[
36
]
, respectively. CODO offers
codo-opt
, which applies the full optimization flow in a single command, allowing users to optionally adjust input parameters like maximum parallelism and tiling factors.
CODO contains a holistic compilation flow that follows a main optimization order while being deeply integrated through co-optimization.
The flow begins with two dataflow correction passes. The coarse-grained violation elimination resolves single-producer-consumer violations between tasks, where each task is represented as a
node
in the dataflow graph. Subsequently, the fine-grained violation elimination fixes inconsistencies in data access order and count, enabling efficient FIFO-based communication.
This pass exemplifies our co-optimization principle: beyond ensuring correctness, it proactively restructures code for communication efficiency and provides guidance for later communication passes.
Based on this, CODO performs communication buffer determination, selecting either FIFO or ping-pong implementations and prioritizing FIFO whenever feasible for higher performance.
To further improve communication efficiency, CODO generates efficient reuse buffers and reinvokes the correctness passes to avoid new violations. This process also exposes loop-level parallelism, providing key information for subsequent parallelism exploration.
Afterward, CODO manages off-chip transfers to improve HBM bandwidth utilization.
Finally, CODO’s auto-scheduling engine determines tiling factors, unroll factors, pipelining, and array partitioning. These parallelism decisions are not made in isolation, as they can affect both correctness and communication efficiency. Therefore, a final inter-task optimization pass co-optimizes these choices across the entire graph, eliminating any newly introduced violations and ensuring a high-performance design.

# user_ref:arxiv_id:2509.13694

paper_id: user_ref:arxiv_id:2509.13694
tier: U
source_used: html_arxiv
warning: none

## Intro

1.1.
Dataflow Architecture
Dataflow architecture, as an alternative to Von Neumann-style architectures such as the NVIDIA H100
(Choquette,
2023
)
and Google TPUv4
(Jouppi et al.,
2023
)
, is increasingly adopted and studied to overcome the memory wall in emerging AI applications, such as Large Language Models (LLM). Because of LLMs’ autoregressive nature, the decoding stage is highly memory-bound, demanding more memory-efficient architectures. AMD Versal
(Gaide et al.,
2019
)
, Sambanova SN40L
(Prabhakar et al.,
2024
)
, and IBM AIU
(Burns et al.,
2022
)
are commercial AI accelerators with reconfigurable dataflow architectures; many studies
(Prabhakar et al.,
2017
; Nowatzki et al.,
2017
; Chen et al.,
2024a
)
have also demonstrated the latency and energy efficiency advantages of dataflow architecture.
Figure
1
shows the typical computation pattern of dataflow accelerators. As shown in Figure
1
(b), a dataflow accelerator contains the following on-chip components:
(1)
Kernel
: Computes an operator or coarse-grained
task
(e.g., matrix multiply) using a parallel processor (e.g., a systolic array), and provides stream interfaces for input and output.
(2)
Token
: Atomic element communicated between kernels.
(3)
First-in First-out (FIFO)
: Holds accumulated stream tokens to balance different token rates of the producer and consumer, and avoids deadlock or unnecessary kernel stalls.
(4)
Stream Layout Converter
: Converts stream layout on-the-fly to accommodate different computation patterns of producer and consumer kernels through a local ping-pong buffer.
(5)
Direct Memory Access (DMA)
: Communicates with external memory, and converts memory-mapped interfaces to stream interfaces or vice versa.
Figure 1
.
Computation pattern of dataflow accelerators.
Kernels may be designed using
dataflow
circuits through dynamic scheduling
(Josipović et al.,
2018
)
, or may adopt different
dataflow
strategies (e.g., input stationary) for efficient on-chip data reuse
(Chen et al.,
2016
)
. Although using the same terminology, these
dataflow
concepts are conceptually orthogonal to the dataflow architecture and accelerators discussed in this paper.
The key idea of dataflow architecture is to stream intermediate results between kernels through on-chip FIFOs instead of triggering frequent external memory accesses. For example, in Figure
1
(b), the intermediate results produced by
Kernel0
are streamed directly to
Kernel1
and
Converter0
without going through external memory, as in Figure
1
(a). Following the convention proposed in
(Prabhakar et al.,
2024
)
, we refer to enabling streaming between dataflow kernels as
stream-based kernel fusion
. Additionally, as illustrated in Figure
1
(c), the schedule of the dataflow accelerator allows
Kernel1
and
Converter0
to start execution before
Kernel0
completes. This overlapped execution can significantly improve both the overall throughput and latency.
Figure 2
.
Current paradigm of dataflow accelerator design.
1.2.
Dataflow Accelerator Programming
Figure
2
shows the current paradigm of dataflow accelerator programming. As dataflow accelerators generally fall into two categories, application-specific accelerators and domain-specific accelerators (DSAs), we discuss each separately.
1.2.1.
Application-specific Accelerator
In this category, the dataflow components and schedule are tailored for a single application. Thus,
programming
typically refers to the
design
or
generation
of architecture and microarchitecture. Traditionally, Hardware Description Languages (HDLs), High-level Synthesis (HLS), and meta-HDLs like Chisel
(Bachrach et al.,
2012
)
are used for this purpose
(Chen et al.,
2005
; Zhang et al.,
2018
; Chi et al.,
2018
; Sarkar et al.,
2023
)
. More recently, Accelerator Design Languages (ADLs) have emerged to improve productivity
(Chen et al.,
2024b
; Durst et al.,
2020
; Thomas et al.,
2020
)
, introducing typing systems and primitives to describe computation, memory layout, and dataflow schedules. As shown in Figure
2
, existing solutions require manual effort to convert applications into dataflow schedules and components, which are then passed to HLS, meta-HDL transpilers, or vendor EDA tools for hardware generation. While ADLs and HLS frameworks incorporate Design Space Exploration (DSE)
(Koeplinger et al.,
2016
,
2018
; Ben-Nun et al.,
2019
; Ye et al.,
2022
; Agostini et al.,
2022
; Zhang et al.,
2024
)
, these efforts focus mainly on optimizing individual kernels.
1.2.2.
Dataflow DSA
DSAs are designed to efficiently perform computations for a particular class of applications or a specific domain, rather than being a general-purpose processor. DSAs are often realized using Coarse-grained Reconfigurable Architecture (CGRA)-like architectures
(Gaide et al.,
2019
; Prabhakar et al.,
2024
,
2017
; Nowatzki et al.,
2017
)
, where on-chip resources are reconfigured to implement different dataflow designs. Modern DSAs are programmed using C/C++ primitives
(Gaide et al.,
2019
; Zhuang et al.,
2023
,
2024
)
or Domain-specific Languages (DSLs), such as Spatial
(Koeplinger et al.,
2018
)
, Halide
(Ragan-Kelley et al.,
2013
)
, and TVM
(Chen et al.,
2018
)
, to generate domain-optimized code. As illustrated in Figure
2
, developers must manually transform applications into logical components using these DSLs or APIs. Software compilers then map them to physical resources and generate the final binaries for on-chip execution. While these DSLs often provide auto-tuning capabilities for dataflow kernels, their primary focus is on optimizing individual kernels instead of the entire dataflow application, leaving substantial performance gains unrealized.
1.3.
Pitfalls
1.3.1.
Pitfall 1: Inter-kernel Correlation
Prior works
(Ye et al.,
2022
,
2024
)
show that inter-kernel correlation can affect accelerator performance. Since kernels execute in a pipelined manner, their latencies must be balanced for optimal throughput. Moreover, buffer-connected kernels need aligned parallelization strategies to avoid inefficient memory use. However, previous work only considered ping-pong buffers, which support memory-mapped access. FIFOs are more restrictive, as data must be pushed/pulled in order. This introduces the following challenges for each kernel:
(1)
Tiling
: Choosing tile sizes that enable streaming, minimize local buffering, and preserve memory efficiency.
(2)
Permutation
: Reordering loops to reduce memory utilization during data streaming.
(3)
Vectorization
: Selecting unrolling strategies to balance latency and improve streaming efficiency.
These decisions are interdependent across kernels, making global optimization challenging for analytical models or manual design.
1.3.2.
Pitfall 2: External Memory Access
Most existing compilers
(Ye et al.,
2022
; Agostini et al.,
2022
; Ye et al.,
2024
; Zhao et al.,
2022
; Zhang et al.,
2024
; Basalama and Cong,
2025
)
assume that all data fits on-chip, which is unrealistic for large applications. When off-chip memory is involved, each DMA must address the following issues:
(1)
How to overlap memory access with kernel execution?
(2)
What data layout best matches the streaming pattern?
(3)
How to pack/vectorize data to maximize bandwidth?
These require nontrivial pattern analysis and are error-prone when handled manually. DMA design is also tightly coupled with kernel tiling and scheduling, compounding the complexity.
1.3.3.
Pitfall 3: Stream-based Kernel Fusion
The goal of stream-based kernel fusion is to stream all intermediate results on-chip, limiting external memory use to inputs and outputs. However, producer and consumer kernels often have incompatible stream layouts due to different computation patterns. This requires:
(1)
Checking layout compatibility between kernels.
(2)
Generating minimal on-the-fly stream layout converters.
(3)
Ensuring the converter fits within available on-chip memory.
These steps involve complex pattern analysis and require a global view of the system, making manual solutions impractical.
1.3.4.
Pitfall 4: FIFO Sizing
As shown in Figure
1
, if
Kernel1
is slower than
Converter0
, FIFOs may overflow or underflow, leading to a stall cascade and eventual deadlock. Though dynamic scheduling solutions exist
(Josipović et al.,
2021
)
, coarse-grained accelerators still rely on manual sizing
(Chen et al.,
2024b
,
a
)
, which does not scale to a large number of FIFOs. A recent automated approach
(Honorat et al.,
2024
)
uses simulation to determine FIFO sizes, but it is time-consuming and lacks scalability.
Figure 3
.
Proposed paradigm of dataflow accelerator design.
1.4.
Our Proposal
Due to the pitfalls described in Section
1.3
, the current paradigm shown in Figure
2
is difficult to scale up to large dataflow accelerators. Therefore, we propose a shift in the design paradigm shown in Figure
3
. We do not advocate for full automation, as ADL/HLS/HDL or DSLs remain essential for designing individual dataflow kernels, such as local buffers and vectorization. However, once individual kernels are designed or generated, we argue that compilers should automatically generate the dataflow schedule, assemble the kernels into an application-level dataflow accelerator, and resolve the pitfalls identified in Section
1.3
algorithmically. This is analogous to the GPU software ecosystem, where DSLs like CUDA and Triton
(Tillet et al.,
2019
)
are used to design or auto-tune individual GPU kernels, while kernel assembly and scheduling are handled automatically by compilers, resulting in a programming paradigm that is both efficient and scalable.
In this spirit, we propose
StreamTensor
, a compiler that enables automatic tensor streaming in dataflow architectures. This paper describes how each pitfall is addressed in a systematic and hierarchical manner. As a pioneering work, StreamTensor proposes algorithmic solutions for each challenge and demonstrates their effectiveness through large benchmarks. While these solutions may not be optimal, they clearly expose well-defined optimization subproblems and enable co-optimization opportunities across different design spaces.
Overall, this paper makes the following contributions:
(1)
We propose StreamTensor, the first PyTorch-to-device dataflow compiler that automatically generates stream-based dataflow accelerators and their corresponding runtime systems.
(2)
We propose an iterative tensor (
itensor
) type that systematically encodes the stream information for the first time. This typing system forms the foundation for stream-based kernel fusion and dataflow component generation, improving the scalability and productivity of dataflow accelerator design.
(3)
We propose three design spaces, including tensor tiling space, kernel fusion space, and resource allocation space, that cover the sophisticated design space of dataflow architecture in an algorithmic and hierarchical manner. We further propose an exploration algorithm for each design space
to reduce resource utilization and improve latency and throughput.
(4)
We propose a piecewise function-based token behavior model that transforms the dataflow FIFO sizing problem of dataflow accelerators into a scheduling problem. We further propose a linear programming (LP) algorithm to solve this problem, reducing resource utilization while avoiding deadlock.
(5)
We evaluate StreamTensor on FPGA platforms with LLMs and observe up to 0.76x and 0.64x lower latency compared to the state-of-the-art FPGA LLM accelerators and GPUs, and up to 1.99x higher energy efficiency compared to GPUs.
Figure 4
.
Proposed StreamTensor framework.

## Method

StreamTensor is a compilation framework designed to transform PyTorch models into optimized dataflow implementations. It is built upon the MLIR
(Lattner et al.,
2021
)
compilation framework. The overall architecture of StreamTensor is depicted in Figure
4
. The compilation process begins with a PyTorch model from Torch-MLIR
(Torch-MLIR Contributors,
2021
)
and proceeds through several stages. Initially, tensor operations are converted into a structured Intermediate Representation (IR) using MLIR’s built-in Linear Algebra (Linalg) operations. This IR is then optimized by MLIR’s Linalg passes like element-wise operation fusion. StreamTensor subsequently applies Design Space Exploration (DSE) algorithms to determine optimal tiling strategies, considering factors such as tile sizes, unrolling factors, and permutations based on computational patterns. The Linalg IR is then transformed into a dataflow IR, where computations are organized as hierarchical tasks. All dataflow components, including DMAs, stream layout converters, and FIFOs, are generated during this stage. Critical optimizations are also performed here, such as stream-based kernel fusion to minimize external memory access and FIFO sizing to balance producer-consumer executions. In the final stages, StreamTensor generates hardware-specific code and a host runtime. StreamTensor handles memory allocation, stream connectivity, and directive materialization, which allows vendor compilers like HLS to generate the target dataflow architectures. Concurrently, it produces host runtime code that manages data transfer, kernel execution, and synchronization between the host CPU and the dataflow accelerator.
Figure 5
.
Iterative tensor (
itensor
) typing system.

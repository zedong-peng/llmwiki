# Transition-Aware Backend Dispatch for Edge LLM Inference

paper_id: arxiv:2607.17415v1
tier: T3
source_used: html_arxiv
warning: none

## Intro

Large language models (LLMs) are becoming an important component of interactive and agentic artificial intelligence systems. Although the largest models continue to require datacenter-scale infrastructure, smaller transformer models increasingly enable practical inference on edge platforms. Local execution can reduce network dependence and cloud-serving costs, improve response latency, and preserve privacy by keeping user data on the device. These benefits make efficient transformer inference important for embedded assistants, robotics applications, and real-time decision systems
[
28
,
27
,
17
,
26
,
30
,
4
]
.
Edge deployment presents different optimization constraints from cloud inference. Edge devices operate under tighter power, memory, and thermal limits while exposing heterogeneous resources such as multicore CPUs, embedded GPUs, and runtime-specific backends
[
18
,
12
,
16
,
9
]
. A common deployment strategy assigns a single backend to the model or to large portions of its computation graph. Although simple, static assignment cannot exploit performance differences across operator types, tensor shapes, inference phases, and optimization objectives
[
7
,
34
,
24
]
.
Transformer inference repeatedly invokes dense projections, multilayer perceptron (MLP) activations, and normalization operations. The relative performance of these operators can vary across tensor shapes and backend implementations. A backend that minimizes latency for one shape may be inefficient for another, and the backend that minimizes latency may differ from the one that minimizes energy or energy-delay product (EDP). Static assignment can therefore miss useful performance and energy-efficiency opportunities on heterogeneous edge platforms
[
9
,
23
,
15
]
.
Operator-local selection provides a more flexible alternative by assigning each supported operator to its lowest-cost backend. However, independent decisions can produce frequent backend, device, or framework switches over an ordered operator trace. These transitions can introduce synchronization, data movement, and framework-conversion costs that offset the benefit of selecting a faster backend for an individual operator
[
16
,
9
,
15
,
13
]
. Consequently, a dispatch policy should consider both the current operator cost and the backend selected for the preceding operator.
This paper presents a selective transition-aware backend dispatch approach for edge transformer inference. The selector uses current operator features together with the previous backend state to avoid transitions whose cost exceeds their local benefit. Three eager-mode execution backends are considered: PyTorch CPU, PyTorch CUDA, and ONNX Runtime CPU. Supported operators are assigned dynamically, while operators outside the dispatch scope retain a static backend assignment.
The approach is evaluated through measurement-backed replay of ordered traces collected from full-model inference runs. Exact operator shapes and backend transitions are measured on an NVIDIA Jetson platform, and the resulting costs are replayed in the original model-derived order. This methodology evaluates the performance potential of selective eager-mode dispatch without requiring an integrated mixed-framework runtime.
The evaluation covers seven transformer model traces, 9,584 ordered instances of four operator classes, and 278 exact shape groups. Transition-aware dispatch reduces replayed latency, energy, and EDP relative to the best static backend policy by 17.4%, 14.4%, and 28.5% on average, respectively. It also reduces switching relative to operator-local selection. Leave-one-model-out evaluation improves all three objectives for six of seven held-out models and improves energy for all seven.
The main contributions are as follows:
•
A full-model-derived operator-trace benchmark covering seven transformer models, 9,584 ordered operator instances, and 278 exact shape groups.
•
Exact-shape measurements across PyTorch CPU, PyTorch CUDA, and ONNX Runtime CPU, including latency, power, energy, EDP, correctness validation, and measured backend-transition costs.
•
Operator-local and transition-aware selectors for latency, energy, and EDP, with previous-backend state incorporated into transition-aware decisions.
•
A measurement-backed trace-replay evaluation that quantifies replay-cost improvements, switch reductions, and leave-one-model-out transfer.
•
An open-source implementation and reproducibility workflow that supports additional models, operators, and execution backends
[
1
]
.

## Method

The proposed methodology consists of model-trace collection, supported-operator extraction, exact-shape grouping, multi-backend benchmarking on Jetson, selector training, and measurement-backed trace replay. Fig.
1
summarizes this pipeline, while Fig.
2
illustrates the three evaluated dispatch policies.
III-A
Full-Model Inference Trace Collection
Ordered operator traces are collected from full-model inference runs on Jetson. Each trace preserves the operator sequence together with the context and tensor-shape metadata required for backend selection. The traced models are Qwen2.5-0.5B
[
21
]
, Qwen3-0.6B
[
22
]
, TinyLlama-1.1B
[
33
]
, SmolLM2-135M and SmolLM2-360M
[
6
]
, OLMo2-1B
[
20
]
, and ModernBERT-base
[
29
]
.
Trace collection uses synthetic tokenizer inputs with batch size 1 and FP32 data. Prefill sequence lengths are 16, 32, 64, and 128 tokens. Each input is constructed by repeating “hello” to the target length and tokenizing with maximum-length padding. For causal models, the decode trace contains one length-1 forward call rather than a complete autoregressive KV-cache generation loop.
Synthetic inputs are used to control sequence length and operator shape rather than to evaluate language-model accuracy. The collected metadata distinguishes prefill and decode phases, allowing phase-dependent shapes to be preserved during replay. The ordered trace files and extracted feature fields are included in the released artifact.
The dispatch scope covers Linear, multilayer perceptron (MLP) activation, root mean square normalization (RMSNorm), and layer normalization (LayerNorm). These classes contribute 9,584 ordered instances. Extracted features include model name, inference phase, batch size, sequence length, hidden and intermediate sizes, matrix dimensions
M
M
,
N
N
, and
K
K
, data type, and output size. Operators outside this scope retain a static assignment and are not selected dynamically.
The full model execution is used only to establish the model-derived order and operator contexts. Supported operators are subsequently evaluated through independent exact-shape measurements rather than by replacing operators inside an integrated model runtime.
III-B
Exact-Shape Grouping
Repeated instances are grouped by exact shape and execution context to avoid redundant benchmarking. Two instances share a group only when their operator type, phase, tensor dimensions, data type, and output size match. This produces 278 unique shape groups from the 9,584 supported instances.
Let
o
i
o_{i}
denote the
i
i
-th supported operator and
x
i
x_{i}
its feature vector. Exact-shape grouping maps
x
i
x_{i}
to shape identifier
s
i
s_{i}
. Each shape-backend cost is measured once and reused whenever that shape appears during replay.
III-C
Jetson Multi-Backend Benchmarking
Each shape group is independently benchmarked using PyTorch eager CPU (
torch_eager_cpu
), PyTorch eager CUDA (
torch_eager_cuda
), and ONNX Runtime CPU (
onnxruntime_cpu
). For each shape-backend pair, latency and active power are measured directly. An idle baseline is collected using the same repeat count and measurement procedure. Baseline-corrected power is
P
i
net
​
(
b
)
=
P
i
active
​
(
b
)
−
P
i
idle
​
(
b
)
.
P_{i}^{\mathrm{net}}(b)=P_{i}^{\mathrm{active}}(b)-P_{i}^{\mathrm{idle}}(b).
Energy and per-operator energy-delay product (EDP) are
E
i
​
(
b
)
=
P
i
net
​
(
b
)
×
L
i
​
(
b
)
1000
,
E
​
D
​
P
i
​
(
b
)
=
E
i
​
(
b
)
×
L
i
​
(
b
)
1000
,
E_{i}(b)=P_{i}^{\mathrm{net}}(b)\times\frac{L_{i}(b)}{1000},\qquad EDP_{i}(b)=E_{i}(b)\times\frac{L_{i}(b)}{1000},
where latency
L
i
​
(
b
)
L_{i}(b)
is measured in milliseconds. The resulting table contains 834 rows, corresponding to 278 shapes evaluated across three backends. All retained rows pass correctness validation and contain valid latency, power, energy, and EDP measurements.
III-D
Backend Selector Training
Selectors are trained separately for latency, energy, and EDP. The operator-local selector uses the current operator features, and its target is the backend with the lowest measured cost for the selected objective. The transition-aware selector additionally receives previous backend
b
i
−
1
b_{i-1}
and evaluates candidate backend
b
i
b_{i}
using
C
i
​
(
b
i
)
=
C
i
o
​
p
​
(
b
i
)
+
C
i
t
​
r
​
a
​
n
​
s
​
(
b
i
−
1
,
b
i
)
,
C_{i}(b_{i})=C_{i}^{op}(b_{i})+C_{i}^{trans}(b_{i-1},b_{i}),
where
C
i
o
​
p
​
(
b
i
)
C_{i}^{op}(b_{i})
is measured operator cost and
C
i
t
​
r
​
a
​
n
​
s
​
(
b
i
−
1
,
b
i
)
C_{i}^{trans}(b_{i-1},b_{i})
is the transition penalty estimated from directed backend-pair measurements. The transition term is zero when the backend is unchanged.
For the EDP objective, candidate cost is represented by an EDP proxy formed from the combined operator and transition latency and energy.
Directed transition measurements execute an operator on a source backend and then switch to a target backend. The resulting pair measurements estimate the switch latency and energy assigned to each directed candidate. For cost construction, every shape is expanded across three previous-backend states and three candidate backends, producing 2,502 candidate-cost rows. These include 834 same-backend candidates with zero transition cost and 1,668 directed backend-change candidates. The lowest-cost candidate for each shape and previous-backend state defines the label, yielding 834 transition-aware decision contexts.
The evaluated classifiers are Extra Trees and random forest with 200 estimators and a minimum leaf size of one, balanced logistic regression with 2,000 maximum iterations, and histogram-based gradient boosting (HistGBM). All use random seed 42. Model selection uses GroupKFold grouped by shape identifier, preventing candidate rows derived from the same exact shape from appearing in both training and validation folds. Models are selected by validation regret for each objective. HistGBM is selected for the reported transition-aware latency, energy, and EDP results.
Figure 2:
Comparison of static backend assignment, operator-local selection, and transition-aware dispatch for an ordered inference trace.
III-E
Transition-Aware Trace Replay
The trained policies are evaluated through analytical replay of the model-derived operator traces. Replay preserves operator order but retrieves execution costs from the Jetson measurement tables rather than executing the connected model through an integrated mixed-backend runtime. Operators outside the dispatch scope retain a static assignment. For supported operators, static assignment uses one backend throughout the trace, operator-local selection predicts independently, and transition-aware selection uses the current features and previous backend. The latter policy is causal and greedy rather than globally sequence-optimal.
At each supported trace position, the policy predicts a backend, the corresponding measured operator cost is retrieved, and any directed transition penalty is added. The selected backend then becomes the previous-backend state for the next supported decision. Static assignments for unsupported operators are common across policies and are not modified by the selector. This design isolates the contribution of selective dispatch while retaining model-derived ordering.
For trace
𝒯
=
(
o
1
,
o
2
,
…
,
o
T
)
\mathcal{T}=(o_{1},o_{2},\ldots,o_{T})
and backend sequence
(
b
1
,
b
2
,
…
,
b
T
)
(b_{1},b_{2},\ldots,b_{T})
, replayed latency and energy are
L
𝒯
=
∑
i
=
1
T
[
L
i
​
(
b
i
)
+
L
i
t
​
r
​
a
​
n
​
s
​
(
b
i
−
1
,
b
i
)
]
,
L_{\mathcal{T}}=\sum_{i=1}^{T}\left[L_{i}(b_{i})+L_{i}^{trans}(b_{i-1},b_{i})\right],
E
𝒯
=
∑
i
=
1
T
[
E
i
​
(
b
i
)
+
E
i
t
​
r
​
a
​
n
​
s
​
(
b
i
−
1
,
b
i
)
]
.
E_{\mathcal{T}}=\sum_{i=1}^{T}\left[E_{i}(b_{i})+E_{i}^{trans}(b_{i-1},b_{i})\right].
Trace-level EDP is computed after accumulation as
E
​
D
​
P
𝒯
=
E
𝒯
×
L
𝒯
1000
.
EDP_{\mathcal{T}}=E_{\mathcal{T}}\times\frac{L_{\mathcal{T}}}{1000}.
This differs from the per-operator EDP used for label construction. Replay also records backend, device, and framework switches. Integrated dispatcher and model-level framework overheads are outside the replay scope.
III-F
Experimental Setup
Measurements use an NVIDIA Jetson Orin Nano running JetPack 6.2 and Linux for Tegra (L4T) R36.4.3, with CUDA 12.6, PyTorch 2.8.0, ONNX Runtime 1.23.2, and Python 3.10.12. The device operates in NVIDIA 25 W mode without forced clocks, reflecting default clock behavior under the selected power mode.
Each exact-shape run uses three warmup iterations followed by 500 nominal measured iterations, with adaptive repetition for short operators. Retained rows contain between 10 and 27,077 iterations, with a median of 778. Power is sampled from the
VDD_IN
rail using
tegrastats
at 50 ms intervals. Short operators are repeated over an extended window to obtain sufficient active and idle samples. The benchmark records mean, median, percentiles, range, and standard deviation as within-run statistics. Latency summaries include the mean, median, p50, p90, p95, p99, minimum, maximum, and standard deviation. Correctness is checked against PyTorch CPU reference output. FP32 tolerances are
rtol
=
10
−
4
\mathrm{rtol}=10^{-4}
and
atol
=
10
−
5
\mathrm{atol}=10^{-5}
for RMSNorm, MLP activation, and LayerNorm, while Linear uses
atol
=
10
−
3
\mathrm{atol}=10^{-3}
. Correctness status and absolute, mean, and relative error statistics are retained with each result.
III-G
Evaluation Protocol
The main evaluation compares static, operator-local, and transition-aware policies across seven model-derived traces. Gains are calculated relative to the best static policy for each objective. The main evaluation measures represented shape contexts. Leave-one-model-out evaluation uses LeaveOneGroupOut by model name, holding out one model during training and using it only for replay to evaluate model-level transfer.

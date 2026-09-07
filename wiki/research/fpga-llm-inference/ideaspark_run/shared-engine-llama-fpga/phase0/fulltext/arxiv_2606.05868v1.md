# YouZhi: Towards High-Concurrency Financial LLMs via Adaptive GQA-to-MLA Transition

paper_id: arxiv:2606.05868v1
tier: T3
source_used: html_arxiv
warning: none

## Intro

The rapid iteration of general-purpose large language models (LLMs) has catalyzed a paradigm shift in digital finance, equipping the industry with unprecedented language understanding and reasoning capabilities
Nie
et al.
(
2024
)
. While scaling these foundation models unlocks substantial productivity gains across diverse financial applications
Wang
et al.
(
2025
); Kim
et al.
(
2024
)
, their deployment in real-time, high-traffic scenarios introduces formidable system-level challenges.
Specifically, current advancements in financial LLMs are predominantly gauged by static benchmark accuracy
Xie
et al.
(
2024
)
, which obscures a critical gap: the structural disconnect between theoretical performance and production deployability. Real-world financial services, as exemplified by high-concurrency mobile banking scenarios (Figure
2
), are governed by stringent operational constraints:
(i) low latency
,
(ii) high concurrency
, and
(iii) high task-completion rates
. Simultaneously, they demand deep, domain-specific expertise that general-purpose models often lack.
Figure 1:
Accuracy–efficiency trade-off on financial benchmarks.
YouZhi models improve over their base backbones in both average score and
maximum concurrency, and lie on the Pareto frontier.
A pragmatic and economically viable path is to
harness the robust capabilities of existing foundation models and repurpose them into high-performance financial specialists
through efficient architectural adaptation coupled with comprehensive domain-aware post-training. However, existing financial models—such as BloombergGPT
Wu
et al.
(
2023
)
, FinGPT
Yang
et al.
(
2023
)
, YiZhao-12B-Chat
Lab (
2024
)
, and DianJin-R1
Zhu
et al.
(
2025
)
—typically inherit the standard Transformer architecture with Grouped-Query Attention (GQA)
Ainslie
et al.
(
2023
)
or Multi-Head Attention (MHA)
Vaswani
et al.
(
2017
)
, enhanced solely through domain pre-training or supervised fine-tuning. While this paradigm improves financial knowledge understanding
Yang
et al.
(
2024a
)
, it treats
model capability
and
serving efficiency
as isolated concerns, leaving the fundamental KV cache bottleneck of GQA/MHA architectures unaddressed. As a result, they struggle to achieve an optimal accuracy-efficiency trade-off (as illustrated by the baselines in Figure
1
).
Figure 2:
High-Concurrency Mobile Banking.
To bridge this gap, we propose
YouZhi-LLM
, underpinned by a
layer-adaptive GQA2MLA transition framework
explicitly tailored for financial deployment. Instead of forcing a one-size-fits-all structural conversion, our approach dynamically optimizes transition parameters (e.g., FreqFold size) on a per-layer basis. This accommodates heterogeneous architectural sensitivities, thereby reaping the KV-cache compression benefits of Multi-Head Latent Attention (MLA) with minimal sacrifice to foundational language modeling capabilities. To recover domain capabilities eroded during the structural transition, we further introduce a
comprehensive post-training pipeline
featuring stratified data curation and targeted domain augmentation. As demonstrated in Figure
1
, our resulting models establish a new Pareto frontier, simultaneously maximizing both financial benchmark accuracy and inference concurrency.
Finally, by natively integrating MLA operators on Huawei Ascend clusters, we achieve efficient deployment with substantial memory and latency savings. Our main contributions are summarized as follows:
•
We conduct a layer-wise analysis of the GQA2MLA transition, revealing that shallow and deep layers exhibit diametrically opposed degradation characteristics during transition.
•
To capitalize on these layer-specific characteristics, we propose a layer-adaptive transition algorithm that dynamically assigns per-layer FreqFold sizes. Experiments across multiple mainstream LLMs demonstrate a substantial perplexity reduction compared to uniform conversion baselines.
•
We design a comprehensive post-training pipeline tailored for the converted MLA models, encompassing stratified data compression, financial domain augmentation, refusal data construction for compliance scenarios, and instruction-following reinforcement. This pipeline not only recovers capabilities lost during transition but also yields significant gains on both financial benchmarks and real-world mobile banking tasks.
•
We implement and deploy the resulting YouZhi-LLM on Huawei Ascend NPUs using the vLLM-Ascend inference framework. Extensive evaluations demonstrate a
72% KV cache reduction
and a
2.69
×
\times
improvement in maximum concurrency
, enabling highly efficient, high-concurrency serving for production-grade financial applications.

## Method

To investigate the layer-specific characteristics of the GQA2MLA transition, we perform a layer-wise analysis of perplexity degradation in the partial RoPE stage. More specifically in our ablation experiment, only a single layer is translated to MLA at a time, while all other layers remain to be GQA structure unchanged. This allows us to isolate and quantify the layer-specific characteristics in the perplexity degradation of GQA2MLA.
Figure 3:
Perplexity degradation of OpenPangu-7B on the WikiText-2 dataset in the partial RoPE modification stage using TransMLA with a RoPE dimension of 128.
Observations.
As shown in Figure
4
, we present the result of layer-wise perplexity degradation in the partial RoPE stage across different FreqFold sizes (e.g., 1, 2, 4, 8). Each polyline corresponds to a fixed FreqFold size. A point on the polyline denotes the perplexity degradation observed when a specific layer is converted to MLA, with all other layers kept in the original GQA structure.
The results reveal a distinct pattern across layers. In the shallow layers (e.g., 0-5), a larger FreqFold size (e.g., 8) yields the lowest perplexity. This suggests that in these layers, the benefit of concentrating principal components outweighs the cost of RoPE frequency approximation. Conversely, in middle layers (e.g., 16-25), the optimal strategy shifts: the minimal perplexity is achieved with a FreqFold size of 1 (effectively no folding). This indicates that in these layers, the frequency approximation error becomes the dominant factor, and preserving precise RoPE frequency information is more critical.
Figure 4:
Layer-wise perplexity degradation of OpenPangu-7B on the WikiText-2 dataset in the partial RoPE modification stage using TransMLA with a RoPE dimension of 128.
(a)
Tansition tajectory diagram of TransMLA.
(b)
Tansition tajectory diagram of layer-adaptive algorithm.
Figure 5:
Schematic Comparison of the Tansition Trajectory: TransMLA vs. Layer-adaptive.
Insights.
There are significant layer-specific characteristics in the perplexity degradation of GQA2MLA. The FreqFold size should set adaptively for each layer in LLMs.
3.1
Layer-Adaptive GQA2MLA Transition
In this section, we introduce a layer-adaptive FreqFold size selection algorithm to minimize perplexity degradation in the GQA2MLA transition. More specifically, we first formulate the layer-adaptive FreqFold selection problem as a combinatorial optimization problem. To tackle the combinatorial explosion of the feasible region with the number of layers, the combinatorial optimization problem is reformulated as a multi-round sequential decision process. Our method optimizes the perplexity in each decision round individually, progressively refining the final solution.
Due to the layer-specific characteristics in the process of GQA2MLA, we should find the optimal FreqFold size for each layer. Let function
d
​
(
α
0
,
…
,
α
k
,
…
,
α
N
)
d(\alpha_{0},...,\alpha_{k},...,\alpha_{N})
denote the perplexity degradation when FreqFold size
1
1
1
Since the head dimension is typically a power of 2, and the FreqFold size must be a divisor of the head dimension, the feasible choices for FreqFold size are consequently restricted to powers of 2 as well.
of layer
k
k
is selected as
α
k
∈
{
0
,
2
0
,
2
1
,
2
2
,
…
,
2
h
}
\alpha_{k}\in\{0,2^{0},2^{1},2^{2},...,2^{h}\}
, where
2
h
2^{h}
is head dimension of model. In particular, when
α
k
=
0
\alpha_{k}=0
means that layer
k
k
remains GQA structure.
As a result, the number of feasible solution in the minimization of function
d
​
(
α
0
,
…
,
α
k
,
…
,
α
N
)
d(\alpha_{0},...,\alpha_{k},...,\alpha_{N})
is
(
h
+
1
)
N
+
1
(h+1)^{N+1}
. For typical LLMs such as openPangu-7B, the number of feasible solution is
9
34
9^{34}
, which is too large to enumerate.
To overcome this, we should break down this highly complex problem into smaller, manageable subproblems. We can iteratively optimize the FreqFold size for one layer at a time, rather than attempting to solve the intractable global joint optimization directly. To this end, let
C
k
C_{k}
denote the increase of perplexity degradation attributable to the transition at layer
k
k
, given that layers after
k
k
have been translated. Then
C
k
C_{k}
can be present as follows,
C
k
=
d
​
(
𝟎
k
,
α
k
,
…
,
α
N
)
−
d
​
(
𝟎
k
+
1
,
α
k
+
1
,
…
,
α
N
)
,
C_{k}=\scalebox{0.82}{$\displaystyle\!\!d(\mathbf{0}_{k},\alpha_{k},\dots,\alpha_{N})-d(\mathbf{0}_{k+1},\alpha_{k+1},\dots,\alpha_{N})$},
(1)
where
𝟎
k
\mathbf{0}_{k}
in Eq. (
1
) indicates that the first
k
k
layers remain GQA.
Based on the definition of
C
k
C_{k}
, function
d
​
(
α
0
,
…
,
α
k
,
…
,
α
N
)
d(\alpha_{0},...,\alpha_{k},...,\alpha_{N})
can be further decomposed as
d
​
(
α
0
,
…
,
α
k
,
…
,
α
N
)
=
∑
k
=
0
N
C
k
.
d(\alpha_{0},\dots,\alpha_{k},\dots,\alpha_{N})=\sum_{k=0}^{N}C_{k}.
(2)
Although we cannot minimize the summation of all terms, i.e.
∑
k
=
0
N
C
k
\sum_{k=0}^{N}C_{k}
, the optimal solution
α
k
∗
\alpha_{k}^{*}
to minimizing each single term
C
k
C_{k}
can be easily obtained by simply enumerating the feasible region of
α
k
\alpha_{k}
as follows.
α
k
∗
=
arg
⁡
min
α
k
⁡
{
C
k
|
α
k
+
1
,
α
k
+
2
,
…
,
α
N
}
.
\alpha_{k}^{*}=\arg\min_{\alpha_{k}}\{C_{k}|\alpha_{k+1},\alpha_{k+2},\dots,\alpha_{N}\}.
(3)
The number of feasible solutions in the optimization problem shown in Eq. (
3
) is only
h
+
1
h+1
. Consequently, the complexity of searching solutions for all layers is
(
h
+
1
)
×
(
N
+
1
)
(h+1)\times(N+1)
, which is much smaller than the original complexity
(
h
+
1
)
N
+
1
(h+1)^{N+1}
.
Figure 6:
Two-stage Post-training Pipeline.
To provide an intuitive understanding of the optimization process, we illustrate the transition trajectories of both TransMLA and our method in Figure
5
. In the schematic, the trajectory of TransMLA is confined to a straight line, as shown in Figure
5(a)
. This limitation arises because TransMLA employs a uniform FreqFold size across all layers, which inherently restricts its search path. Consequently, the feasible solution space for the GQA2MLA transition is narrowly bounded. To overcome this limitation, we relax the uniform size constraint and propose layer-adaptive strategy given by Eq. (
3
), which allows the independent optimization of the FreqFold size per layer. As shown in Figure
5(b)
, this flexibility enables our method to find a superior path in the solution space, ultimately achieving lower overall perplexity degradation.
3.2
Training Pipeline
In this section, we present a comprehensive post-training pipeline for our translated MLA model, as shown in Figure
6
. The aim of post-training pipeline is to maintain the model’s general capabilities and enhance its performance of downstream tasks in the financial domain.
Following the architecture transformation of the base model, we design a two-stage post-training pipeline to develop the domain-specific financial LLM.
The pipeline was specifically designed to address the unique challenges introduced by GQA2MLA while systematically restoring general-purpose functionalities and improving performance on financial downstream tasks. The entire post-training pipeline is conducted on Ascend clusters, while training loss curve is presented in Figure
7
.
Stage 1: Generalized Knowledge Distillation.
The objective of this stage is to restore the general capabilities degraded during the GQA2MLA process.
To this end, we adopt generalized knowledge distillation (GKD)
Agarwal
et al.
(
2024
)
.
Specifically, we designate the original GQA-based model as the teacher and the translated MLA model as the student.
We employ forward KL divergence and an off-policy strategy, training the student on a mixed offline dataset curated from the teacher’s SFT data. This process enables the student to recover performance by learning from the teacher’s annotated sequences.
Stage 2: Financial Domain-Specific SFT.
The objective of this stage is to inject financial knowledge, building on the general capability restored from stage 1. To this end, we construct a comprehensive, multi-source supervised fine-tuning (SFT) dataset that spans all major financial sub-domains, comprising 970,000 high-quality instruction-response pairs.
The model is fine-tuned on this curated dataset for 2 epochs, optimized with a standard next-token prediction loss. We employ a cosine-decay learning rate schedule, initialized at
1
×
10
−
5
1\times 10^{-5}
and annealed to 0, coupled with a linear warmup (warmup ratio of 0.01) to stabilize the initial training phase.
(a)
Training loss curve at stage 1: GKD.
(b)
Training loss curve at stage 2: SFT.
Figure 7:
Training loss curve of two-stage post-training pipeline on Ascend A3 Cluster.
3.3
Construction of Training Data
The GQA-to-MLA structural transition inevitably introduces accuracy degradation, as discussed in last Section. To recover this degradation and simultaneously enhance the model’s financial domain capabilities, carefully constructed training data is essential. In this subsection, we present the data construction pipeline for both supervised fine-tuning (SFT) and reinforcement learning (RL), which aims to restore the general capabilities degraded by the structural transition while improving performance on financial downstream tasks.
Compression of General and Financial Data.
In the post-training stage, a proper data ratio between general and financial data is critical for simultaneously recovering transition-induced degradation and enhancing financial domain capabilities. However, the available general data typically far exceeds financial data in volume, leading to severe imbalance across capability dimensions. Directly applying entropy-based data compression
Yin
et al.
(
2024
)
to the entire dataset is efficient in that it requires only CPU resources, yet it suffers from poor interpretability and declining effectiveness as data scale increases, since samples of different categories and difficulty levels are compressed together without guaranteeing category completeness, quality priority, or difficulty balance. To address these limitations, we propose a stratified and hierarchical data compression method consisting of three stages.
Stage 1: Tag system construction.
We leverage open-source tagging models to automatically annotate the full dataset across multiple dimensions. For the category dimension, we adopt InsTagger
Lu
et al.
(
2024
)
to assign multi-class semantic tags capturing the intent and task type of each sample; for the quality dimension, we employ the DEITA quality scorer
Liu
et al.
(
2024b
)
to rate each sample on a 1–6 scale; for the difficulty dimension, we use the DEITA complexity scorer to rate sample difficulty on a 1–6 scale. This yields a unified tag system covering category, quality, and difficulty.
Stage 2: Stratified and hierarchical filtering.
Based on the tagging results, the dataset is partitioned into sub-clusters by category tag, and each sub-cluster is further divided by difficulty (easy/medium/hard). Each sub-cluster is assigned a compression target following the priority principle of “high quality first — broad domain coverage — difficulty balance — high information content”: high-quality samples (above the quality threshold) are retained first, then categories are ensured not to be missing, and finally different difficulty levels are balanced within each category.
Stage 3: Intra-cluster entropy compression.
Within each fine-grained sub-cluster, we apply the entropy-based compression method
Yin
et al.
(
2024
)
. By using lossless compression (zlib) to approximate the incremental information contribution of each candidate sample, we prioritize samples that significantly reduce overall redundancy and remove semantically repetitive or low-information data. Since all data within a cluster share the same category and similar difficulty, the compression process achieves more precise information coverage and avoids the bias caused by cross-category mixed compression.
Augmentation for Missing Domains.
After the structural transition, domain gaps that were previously tolerable become more pronounced, and open-source data often exhibits significant deficiencies in financial domain coverage, scenarios, and tasks. To systematically fill these gaps, we adopt a progressive diversity data generation approach that expands along the pipeline of “domain
→
\rightarrow
task
→
\rightarrow
scenario
→
\rightarrow
persona.”
Diverse persona construction.
Following the meta-decomposition mechanism of DecIF
Hui
et al.
(
2025
)
, we first prompt the model to generate meta-domains representing high-level conceptual categories, then produce meta-requests (general task formulations within each domain) and meta-scenarios (concrete situational contexts), and finally combine these elements into specific personas, ensuring systematic coverage and diversity.
Knowledge point extraction and composition.
For missing capability dimensions (e.g., geometry and statistics in mathematics), we use LLMs to extract specific knowledge points from existing relevant data, and then cross-combine these knowledge points to form task descriptions covering different knowledge dimensions.
SFT data construction.
The generated diverse personas and knowledge point compositions are combined to construct corresponding SFT training data. Objective and subjective constraints (e.g., professionalism, compliance, format requirements) are injected during the generation stage, and the same constraint system is applied for automated quality verification after generation, ensuring that the data maintains both diversity and high accuracy.
Figure 8:
Construction of Training Data.
Refusal Data Construction.
Financial scenarios frequently involve incomplete information, such as missing key financial data or contradictory premises, where the model should recognize the insufficiency and respond accordingly. However, since training data typically lacks “unanswerable” samples, the model tends to produce hallucinated answers rather than acknowledging ignorance. TreeCut
Ouyang (
2025
)
proposes constructing unanswerable questions through logic tree modeling and path pruning, where logical relationships are modeled as dependency trees and information absence is created by selectively removing edges at specific depths. Nevertheless, the original TreeCut method suffers from limited generalization in its rule-based generation mode and unstable quality in its LLM-based generation mode. To address this, we adopt a two-stage strategy: in the first stage, logic tree modeling and path pruning are used to generate a structured framework of unanswerable questions, where controlling the removal depth (
cutDepth
) precisely constructs information-absent scenarios, ensuring stability and high quality of the underlying information; in the second stage, LLMs translate the tree structures into natural language, converting structured logical relationships into diverse natural language expressions, thereby achieving both diversity and high quality.
Domain-Specific Capability Data Construction.
The structural transition can cause significant degradation in certain domain-specific capabilities, such as understanding Chinese uppercase financial amounts (e.g., converting “壹佰伍拾元整” to “150.00”) and performing bidirectional conversions between uppercase and lowercase numerals. To recover these degraded capabilities, we leverage Self-Instruct
Wang
et al.
(
2023
)
and Evol-Instruct
Xu
et al.
(
2025
)
to achieve large-scale data amplification from a small number of seed samples. Specifically, we first construct dozens of high-quality seed samples covering typical scenarios and edge cases for the target capability. The Self-Instruct iterative bootstrapping mechanism then guides LLMs to generate new instructions and instances based on the seed samples. Simultaneously, Evol-Instruct progressively evolves simple instructions into more complex variants, expanding the difficulty and coverage of the generated data. Finally, filter validation and similarity-based deduplication ensure the quality and diversity of the generated data. A key advantage of this approach is that it requires only a small number of initial samples (50–200) to achieve large-scale data amplification, making it particularly suitable for domain-specific scenarios where only limited annotated data is available.
Instruction-Following Data Construction.
After the structural transition, the model often suffers from diminished instruction-following capability, manifesting as an inability to output answers in the required format (e.g., JSON, Markdown, LaTeX) despite producing correct reasoning results. To address this, we select tens of thousands of high-quality domain samples, extract or generate corresponding questions, answers, and reasoning processes, and combine them using predefined instruction templates to batch-construct instruction-following training data. The instruction templates are managed via declarative configuration, where each format constraint type is defined as an independent template node containing the complete format constraint instruction and the standard output format definition. A weight control mechanism flexibly adjusts the sampling ratio of each format type, and a randomization mechanism supports diverse expressions of the same format constraint, thereby establishing the “instruction-format” mapping during supervised fine-tuning.
Models
Orig.
Trans.
L-Adap.
Δ
\Delta
PPL
OpenPangu-7B
14.1
50.3
37.6
-35%
Llama3-8B
6.1
25.8
12.9
-65 %
Qwen2.5-7B
6.8
8.4
8.3
-6 %
Qwen2.5-7B-Ins.
7.5
10.0
9.5
-20 %
MiMo-7B-SFT
16.2
22.1
20.4
-29%
MiMo-7B-Base
6.9
9.6
9.0
-22 %
Table 1:
Perplexity on WikiText-2 dataset. "Orig." denotes the original model without any modifications; "Trans."indicates the model modified by TransMLA. "L-Adap." indicates the model modified by our layer-adaptive algorithm. "Ins." denotes instruct model.
Δ
\Delta
PPL denotes the reduction of PPL degradation achieved by our algorithm compared to TransMLA.
Figure 9:
Perplexity Comparison on WikiText-2.
Group
Models
C-Eval
IFEval
MATH-500
LCB
H-Swag
SST-5
CrossNER
Average
Baselines
YiZhao-12B-Chat
70.3
43.9
46.5
3.6
70.2
54.3
49.8
48.4
DianJin-R1-7B
74.5
48.8
76.8
9.3
24.4
42.9
34.2
44.4
Base Models
OpenPangu-7B
73.4
77.8
76.6
34.6
67.8
51.5
55.2
62.4
Qwen2.5-14B-Ins.
80.2
79.6
80.6
20.4
85.9
54.3
59.7
65.8
Our Models
YouZhi-7B
72.9
77.1
76.0
30.1
90.5
62.6
58.1
66.8
YouZhi-14B
78.9
79.5
72.4
25.5
92.8
65.2
61.5
68.0
Table 2:
Performance evaluation of general benchmarks.
Group
Models
CFLUE-K
CFLUE-A
FinanceIQ
Fineval
OpenFinData
FPB
Average
Baselines
YiZhao-12B-Chat
62.1
39.6
63.8
84.5
86.0
82.4
69.7
DianJin-R1-7B
77.6
33.7
74.7
79.0
85.8
68.2
69.8
Qwen3-8B
66.9
37.9
69.5
80.1
83.7
82.2
70.1
Qwen3.5-9B
70.7
37.1
78.1
85.7
84.7
82.4
73.1
Base Models
OpenPangu-7B
50.7
36.5
57.2
70.1
81.7
66.5
60.5
Qwen2.5-14B-Ins.
73.4
35.6
72.7
83.3
85.6
83.5
72.4
Our Models
YouZhi-7B
71.2
43.3
70.2
86.5
86.7
86.8
74.1
YouZhi-14B
83.9
42.4
78.1
91.5
89.4
87.2
78.8
Table 3:
Performance evaluation of financial-domain benchmarks.

# FPGA LLM Architecture Literature Search (2026-07-28)

## Search Setup

- Year window: 2024-2026.
- Sources: arXiv, DBLP, OpenAlex, OpenReview, Semantic Scholar, and Crossref.
- Query union (no `--min-score` filter):
  - `FPGA LLM shared compute engine time multiplexed accelerator`
  - `FPGA LLM spatial dataflow streaming accelerator`
  - `HBM aware low batch autoregressive LLM decode FPGA`
  - `CPU FPGA heterogeneous llama.cpp GGML LLM inference offload`
  - `FPGA LLM operator fusion coarse grained execution persistent kernel`
  - `FPGA transformer overlay CGRA compiler mapping`

Canonical rerun snapshot: arxiv=60, dblp=0, open_alex=60, openreview=0, semantic_scholar=1, crossref=60 · 142 unique (39 cross-source duplicate records merged).

## All Unique Results

| # | Title | Date | Venue | Citations | Score | Sources |
|---:|---|---|---|---:|---:|---|
| 1 | [Understanding the Potential of FPGA-based Spatial Acceleration for Large Language Model Inference](https://doi.org/10.1145/3656177) | 2024-04-04 | ACM Transactions on Reconfigurable Technology and Systems | 63 | 11 | open_alex |
| 2 | [SDA: Low-Bit Stable Diffusion Acceleration on Edge FPGAs](https://doi.org/10.1109/fpl64840.2024.00044) | 2024-09-02 | n/a | 15 | 11 | open_alex |
| 3 | [MPK: A Compiler and Runtime for Mega-Kernelizing Tensor Programs](https://www.semanticscholar.org/paper/418857dee87aed6fdc4e1bff5ee76170baa7a41f) | 2025-12-22 | n/a | 9 | 10 | semantic_scholar |
| 4 | [CD-LLM: A Heterogeneous Multi-FPGA System for Batched Decoding of 70B+ LLMs Using a Compute-Dedicated Architecture](https://doi.org/10.1145/3771288) | 2025-10-22 | ACM Transactions on Reconfigurable Technology and Systems | 1 | 10 | open_alex |
| 5 | [FlightLLM: Efficient Large Language Model Inference with a Complete Mapping Flow on FPGAs](http://arxiv.org/abs/2401.03868v2) | 2024-01-08 | arXiv | 0 | 10 | arxiv |
| 6 | [CXL-SpecKV: A Disaggregated FPGA Speculative KV-Cache for Datacenter LLM Serving](http://arxiv.org/abs/2512.11920v1) | 2025-12-11 | arXiv | 0 | 9 | arxiv |
| 7 | [An Architecture-Agnostic Dataflow Mapping Framework on CGRA](https://doi.org/10.1109/ipdpsw63119.2024.00121) | 2024-05-27 | n/a | 1 | 8 | open_alex |
| 8 | [FlightOPU: An FPGA Overlay Processor for LLM with HBM-Aware Multi-Die Architecture](https://doi.org/10.1109/icfpt67023.2025.00048) | 2025-12-02 | 2025 International Conference on Field Programmable Technology (ICFPT) | 0 | 8 | open_alex, crossref |
| 9 | [Nyx: Virtualizing dataflow execution on shared FPGA platforms](https://doi.org/10.1145/3695053.3731094) | 2025-06-20 | n/a | 0 | 8 | open_alex |
| 10 | [StreamTensor: Make Tensors Stream in Dataflow Accelerators for LLMs](http://arxiv.org/abs/2509.13694v2) | 2025-09-17 | arXiv | 0 | 8 | arxiv |
| 11 | [Accelerating Recommender Model ETL with a Streaming FPGA-GPU Dataflow](http://arxiv.org/abs/2501.12032v3) | 2025-01-21 | arXiv | 0 | 8 | arxiv |
| 12 | [NEO: Saving GPU Memory Crisis with CPU Offloading for Online LLM Inference](http://arxiv.org/abs/2411.01142v1) | 2024-11-02 | arXiv | 0 | 8 | arxiv |
| 13 | [MIST: A Co-Design Framework for Heterogeneous, Multi-Stage LLM Inference](http://arxiv.org/abs/2504.09775v6) | 2025-04-14 | arXiv | 0 | 8 | arxiv |
| 14 | [LLMServingSim: A HW/SW Co-Simulation Infrastructure for LLM Inference Serving at Scale](https://doi.org/10.1109/iiswc63097.2024.00012) | 2024-09-15 | n/a | 16 | 7 | open_alex |
| 15 | [Pushing up to the Limit of Memory Bandwidth and Capacity Utilization for Efficient LLM Decoding on Embedded FPGA](https://doi.org/10.23919/date64628.2025.10993087) | 2025-03-31 | n/a | 7 | 7 | open_alex |
| 16 | [CSTrans-OPU: An FPGA-based Overlay Processor with Full Compilation for Transformer Networks via Sparsity Exploration](https://doi.org/10.1145/3649329.3657325) | 2024-06-23 | n/a | 4 | 7 | open_alex |
| 17 | [A CGRA Front-end Compiler Enabling Extraction of General Control and Dedicated Operators](https://doi.org/10.1109/asp-dac58780.2024.10473891) | 2024-01-22 | 2024 29th Asia and South Pacific Design Automation Conference (ASP-DAC) | 4 | 7 | open_alex, crossref |
| 18 | [LLM Acceleration on FPGAs: A Comparative Study of Layer and Spatial Accelerators](https://doi.org/10.1109/concapan63470.2024.10933896) | 2024-11-27 | n/a | 1 | 7 | open_alex |
| 19 | [Hardware-Software Co-Design for Efficient LLM Inference on PCIe-Based FPGAs Using Coarse-Grained Systolic Arrays](https://doi.org/10.1109/socc66126.2025.11235351) | 2025-09-29 | 2025 IEEE 38th International System-on-Chip Conference (SOCC) | 1 | 7 | open_alex, crossref |
| 20 | [LoopLynx: A Scalable Dataflow Architecture for Efficient LLM Inference](https://doi.org/10.48550/arxiv.2504.09561) | 2025-04-13 | arXiv (Cornell University) | 0 | 7 | open_alex |
| 21 | [RISCBench: Benchmarking RISC-V Orchestration Efficiency in FPGA and FPGA-Like Computing Engines](http://arxiv.org/abs/2603.06580v1) | 2025-12-27 | arXiv | 0 | 7 | arxiv |
| 22 | [A High-Throughput FPGA Accelerator for Lightweight CNNs With Balanced Dataflow](http://arxiv.org/abs/2407.19449v4) | 2024-07-28 | arXiv | 0 | 7 | arxiv |
| 23 | [Dataflow & Tiling Strategies in Edge-AI FPGA Accelerators: A Comprehensive Literature Review](http://arxiv.org/abs/2505.08992v3) | 2025-05-13 | arXiv | 0 | 7 | arxiv |
| 24 | [Mestra: Exploring Migration on Virtualized CGRAs](http://arxiv.org/abs/2604.04694v1) | 2026-04-06 | arXiv | 0 | 7 | arxiv |
| 25 | [A Unified Lightweight Compute Engine for Softmax, GELU, and SiLU Based on a Shared Exponential Unit](https://doi.org/10.2139/ssrn.6537486) | n/a | n/a | 0 | 7 | crossref |
| 26 | [A Critical Analysis on FPGA–CGRA Co-Design for Energy-Efficient Edge AI Systems](https://doi.org/10.54097/7mse0b90) | 2026-01-22 | Highlights in Science, Engineering and Technology | 0 | 7 | crossref |
| 27 | [EdgeLLM: A Highly Efficient CPU-FPGA Heterogeneous Edge Accelerator for Large Language Models](https://doi.org/10.1109/tcsi.2025.3546256) | 2025-03-06 | IEEE Transactions on Circuits and Systems I Regular Papers | 48 | 6 | open_alex |
| 28 | [H 2 -LLM: Hardware-Dataflow Co-Exploration for Heterogeneous Hybrid-Bonding-based Low-Batch LLM Inference](https://doi.org/10.1145/3695053.3731008) | 2025-06-20 | n/a | 16 | 6 | open_alex |
| 29 | [Make LLM Inference Affordable to Everyone: Augmenting GPU Memory with NDP-DIMM](https://doi.org/10.1109/hpca61900.2025.00129) | 2025-03-01 | n/a | 10 | 6 | open_alex |
| 30 | [E2EMap: End-to-End Reinforcement Learning for CGRA Compilation via Reverse Mapping](https://doi.org/10.1109/hpca57654.2024.00015) | 2024-03-02 | n/a | 10 | 6 | open_alex |
| 31 | [SAT-Based Exact Modulo Scheduling Mapping for Resource-Constrained CGRAs](https://doi.org/10.1145/3663675) | 2024-05-22 | ACM Journal on Emerging Technologies in Computing Systems | 8 | 6 | open_alex, arxiv |
| 32 | [TransFRU: Efficient Deployment of Transformers on FPGA with Full Resource Utilization](https://doi.org/10.1109/asp-dac58780.2024.10473976) | 2024-01-22 | n/a | 7 | 6 | open_alex |
| 33 | [An FPGA-based Multi-Core Overlay Processor for Transformer-based Models](https://doi.org/10.1109/iseda62518.2024.10617729) | 2024-05-10 | 2024 2nd International Symposium of Electronics Design Automation (ISEDA) | 5 | 6 | open_alex, crossref |
| 34 | [An FPGA-Based Efficient Streaming Vector Processing Engine for Transformer-Based Models](https://doi.org/10.1109/iseda62518.2024.10617499) | 2024-05-10 | n/a | 4 | 6 | open_alex |
| 35 | [Monomorphism-based CGRA Mapping via Space and Time Decoupling](https://doi.org/10.48550/arxiv.2512.02859) | 2025-12-02 | arXiv (Cornell University) | 2 | 6 | open_alex, arxiv |
| 36 | [FPGA Co-Design for Efficient N:M Sparse and Quantized Model Inference](http://arxiv.org/abs/2512.24713v2) | 2025-12-31 | arXiv | 0 | 6 | arxiv |
| 37 | [Multilayer Dataflow: Orchestrate Butterfly Sparsity to Accelerate Attention Computation](http://arxiv.org/abs/2411.00734v2) | 2024-11-01 | arXiv | 0 | 6 | arxiv |
| 38 | [Exploiting pre-optimized kernels with polyhedral transformations for CGRA compilation](http://arxiv.org/abs/2604.22297v2) | 2026-04-24 | arXiv | 0 | 6 | arxiv |
| 39 | [Versat-AI: An ONNX-to-SoC Compiler for Model-Agnostic CGRA Edge Inference](https://doi.org/10.20944/preprints202607.1442.v1) | n/a | n/a | 0 | 6 | crossref |
| 40 | [A comparative study of FPGA and CGRA technologies in hardware acceleration for deep learning](https://doi.org/10.54254/2755-2721/51/20241212) | 2024-03-25 | Applied and Computational Engineering | 0 | 6 | crossref |
| 41 | [MECLA: Memory-Compute-Efficient LLM Accelerator with Scaling Sub-matrix Partition](https://doi.org/10.1109/isca59077.2024.00079) | 2024-06-29 | n/a | 24 | 5 | open_alex |
| 42 | [TimelyHLS: LLM-Based Timing-Aware and Architecture-Specific FPGA HLS Optimization](https://doi.org/10.1109/coins65080.2025.11125726) | 2025-08-04 | 2025 IEEE International Conference on Omni-layer Intelligent Systems (COINS) | 4 | 5 | open_alex, crossref |
| 43 | [Stardust: Compiling Sparse Tensor Algebra to a Reconfigurable Dataflow Architecture](https://doi.org/10.1145/3696443.3708918) | 2025-02-22 | n/a | 4 | 5 | open_alex |
| 44 | [Accelerating LLMs using an Efficient GEMM Library and Target-Aware Optimizations on Real-World PIM Devices](https://doi.org/10.1145/3696443.3708953) | 2025-02-22 | n/a | 2 | 5 | open_alex |
| 45 | [Enhancing Inference Accuracy of Llama LLM using Reversely Computed Dynamic Temporary Weights](https://doi.org/10.36227/techrxiv.171743080.07522695/v1) | n/a | n/a | 2 | 5 | crossref |
| 46 | [NUPEA: Optimizing Critical Loads on Spatial Dataflow Architectures via Non-Uniform Processing-Element Access](https://doi.org/10.1145/3695053.3731061) | 2025-06-20 | n/a | 1 | 5 | open_alex |
| 47 | [Reconfigurable Domain‐Specific Architectures Based on Coarse‐Grained Operators in High‐Performance FPGAs](https://doi.org/10.1002/cpe.70170) | 2025-06-19 | Concurrency and Computation Practice and Experience | 1 | 5 | open_alex |
| 48 | [LLM-Driven Design Space Exploration of FPGA-based Accelerators](http://arxiv.org/abs/2605.05920v1) | 2026-05-07 | arXiv | 0 | 5 | arxiv |
| 49 | [ScoutAttention: Efficient KV Cache Offloading via Layer-Ahead CPU Pre-computation for LLM Inference](http://arxiv.org/abs/2603.27138v1) | 2026-03-28 | arXiv | 0 | 5 | arxiv |
| 50 | [Production-Grade Local LLM Inference on Apple Silicon: A Comparative Study of MLX, MLC-LLM, Ollama, llama.cpp, and PyTorch MPS](http://arxiv.org/abs/2511.05502v1) | 2025-10-09 | arXiv | 0 | 5 | arxiv |
| 51 | [LlamaF: An Efficient Llama2 Architecture Accelerator on Embedded FPGAs](https://doi.org/10.1109/wf-iot62078.2024.10811385) | 2024-11-10 | n/a | 10 | 4 | open_alex |
| 52 | [PipeInfer: Accelerating LLM Inference using Asynchronous Pipelined Speculation](https://doi.org/10.1109/sc41406.2024.00046) | 2024-11-17 | n/a | 9 | 4 | open_alex |
| 53 | [Lincoln: Real-Time 50~100B LLM Inference on Consumer Devices with LPDDR-Interfaced, Compute-Enabled Flash Memory](https://doi.org/10.1109/hpca61900.2025.00128) | 2025-03-01 | n/a | 6 | 4 | open_alex |
| 54 | [Towards Real-Time LLM Inference on Heterogeneous Edge Platforms](https://doi.org/10.1109/hipcw63042.2024.00076) | 2024-12-18 | n/a | 3 | 4 | open_alex |
| 55 | [Dovetail: A CPU/GPU Heterogeneous Speculative Decoding for LLM inference](http://arxiv.org/abs/2412.18934v2) | 2024-12-25 | arXiv | 3 | 4 | arxiv, crossref |
| 56 | [An Energy-Efficient FPGA Accelerator for Edge AI Inference applications with unified dataflow for both Convolutional Neural Network and Depthwise Convolutional Neural Networks](https://doi.org/10.1109/etecom66111.2025.11319073) | 2025-10-29 | 2025 IEEE International Conference on Emerging Trends in Engineering and Computing (ETECOM) | 2 | 4 | crossref |
| 57 | [Reducing Energy Footprint of LLM Inference Through FPGA-Based Heterogeneous Computing Platforms](https://doi.org/10.3390/electronics15051052) | 2026-03-03 | Electronics | 2 | 4 | crossref |
| 58 | [OpenCafeMol: A coarse-grained biomolecular simulator on GPU with its application to vesicle fusion](https://doi.org/10.1101/2025.02.20.639390) | n/a | n/a | 2 | 4 | crossref |
| 59 | [A Streaming Dataflow Accelerator for Sparse SVM Kernel Computation in Hyperspectral Image Classification](https://doi.org/10.13164/re.2025.0482) | 2025-09 | Radioengineering | 1 | 4 | crossref |
| 60 | [Sparsity-Aware Streaming SNN Accelerator with Output-Channel Dataflow for Automatic Modulation Classification](https://doi.org/10.1109/tcasai.2026.3657358) | 2026 | IEEE Transactions on Circuits and Systems for Artificial Intelligence | 1 | 4 | crossref |
| 61 | [A Composable Dynamic Sparse Dataflow Architecture for Efficient Event-based Vision Processing on FPGA](http://arxiv.org/abs/2401.05626v1) | 2024-01-11 | arXiv | 0 | 4 | arxiv |
| 62 | [SGDFuse: SAM-Guided Diffusion Model for High-Fidelity Infrared and Visible Image Fusion](http://arxiv.org/abs/2508.05264v6) | 2025-08-07 | arXiv | 0 | 4 | arxiv |
| 63 | [HYDRA: A Resource-Efficient Hybrid Data-Multiplexed, Run-time Layer-Reconfigurable Compute Engine for DNN Acceleration](https://doi.org/10.1109/iciis69028.2026.11450730) | 2026-01-16 | 2025 IEEE 19th International Conference on Industrial and Information Systems (ICIIS) | 0 | 4 | crossref |
| 64 | [DTCore: A Compiler-Directed Control-Minimal FPGA Compute Engine](https://doi.org/10.1109/fccm68464.2026.00053) | 2026-05-13 | 2026 IEEE 34th Annual International Symposium on Field-Programmable Custom Computing Machines (FCCM) | 0 | 4 | crossref |
| 65 | [FESTAL: Dataflow Accelerator Synthesis Framework with Graph-Based Fusion for FPGA](https://doi.org/10.1109/asp-dac66049.2026.11420389) | 2026-01-19 | 2026 31st Asia and South Pacific Design Automation Conference (ASP-DAC) | 0 | 4 | crossref |
| 66 | [ConsultChain: Progressive Context Distillation Across Heterogeneous LLM Fleets for Token-Optimal Inference](https://doi.org/10.21203/rs.3.rs-9368244/v1) | n/a | n/a | 0 | 4 | crossref |
| 67 | [Silence Speaks Volumes: The Coarse-Grained State as a Persistent Timelike Process](https://doi.org/10.20944/preprints202606.0075.v1) | n/a | n/a | 0 | 4 | crossref |
| 68 | [FPGA-based low-light image enhancement using Retinex algorithm and coarse-grained reconfigurable architecture](https://doi.org/10.1038/s41598-024-80339-9) | 2024-11-20 | Scientific Reports | 21 | 3 | crossref |
| 69 | [FPGA-based 1D-CNN accelerator for real-time arrhythmia classification](https://doi.org/10.1007/s11554-025-01642-w) | 2025-04 | Journal of Real-Time Image Processing | 14 | 3 | crossref |
| 70 | [Beyond Test-Time Compute Strategies: Advocating Energy-per-Token in LLM Inference](https://doi.org/10.1145/3721146.3721953) | 2025-03-30 | Proceedings of the 5th Workshop on Machine Learning and Systems | 11 | 3 | crossref |
| 71 | [CELLA: A 28nm Compute-Memory Co-Optimized Real-Time Digital CIM-Based Edge LLM Accelerator with 1.78ms-Response in Prefill and 31.32 Token/s in Decoding](https://doi.org/10.23919/vlsitechnologyandcir65189.2025.11075101) | 2025-06-08 | 2025 Symposium on VLSI Technology and Circuits (VLSI Technology and Circuits) | 10 | 3 | crossref |
| 72 | [SK Hynix AI-Specific Computing Memory Solution: From AiM Device to Heterogeneous AiMX-xPU System for Comprehensive LLM Inference](https://doi.org/10.1109/hcs61935.2024.10664793) | 2024-08-25 | n/a | 7 | 3 | open_alex |
| 73 | [SPAT: FPGA-based Sparsity-Optimized Spiking Neural Network Training Accelerator with Temporal Parallel Dataflow](https://doi.org/10.1109/iscas58744.2024.10558351) | 2024-05-19 | 2024 IEEE International Symposium on Circuits and Systems (ISCAS) | 7 | 3 | crossref |
| 74 | [Characterizing Mobile SoC for Accelerating Heterogeneous LLM Inference](https://doi.org/10.1145/3731569.3764808) | 2025-10-01 | n/a | 5 | 3 | open_alex |
| 75 | [TransMap: An Efficient CGRA Mapping Framework via Transformer and Deep Reinforcement Learning](https://doi.org/10.1109/ipdpsw63119.2024.00122) | 2024-05-27 | 2024 IEEE International Parallel and Distributed Processing Symposium Workshops (IPDPSW) | 5 | 3 | crossref |
| 76 | [GLITCHES: GPU-FPGA LLM Inference Through a Collaborative Heterogeneous System](https://doi.org/10.1109/hpec62836.2024.10938498) | 2024-09-23 | 2024 IEEE High Performance Extreme Computing Conference (HPEC) | 4 | 3 | crossref |
| 77 | [H 3 : H ybrid Architecture Using H igh Bandwidth Memory and H igh Bandwidth Flash for Cost-Efficient LLM Inference](https://doi.org/10.1109/lca.2026.3660969) | 2026-01-01 | IEEE Computer Architecture Letters | 3 | 3 | open_alex |
| 78 | [FineQ: Software-Hardware Co-Design for Low-Bit Fine-Grained Mixed-Precision Quantization of LLMs](https://doi.org/10.23919/date64628.2025.10993129) | 2025-03-31 | n/a | 3 | 3 | open_alex |
| 79 | [Accelerating LLM Inference with Flexible N:M Sparsity via A Fully Digital Compute-in-Memory Accelerator](https://doi.org/10.1109/islped65674.2025.11261770) | 2025-08-06 | 2025 IEEE/ACM International Symposium on Low Power Electronics and Design (ISLPED) | 3 | 3 | crossref |
| 80 | [HLS and FPGA-Powered Streaming Video Encoder Accelerator for IoTs Edge Computing](https://doi.org/10.12720/jait.15.1.59-65) | 2024 | Journal of Advances in Information Technology | 3 | 3 | crossref |
| 81 | [FMC-LLM: Enabling FPGAs for Efficient Batched Decoding of 70B+ LLMs with a Memory-Centric Streaming Architecture](https://doi.org/10.1145/3706628.3708863) | 2025-02-26 | n/a | 2 | 3 | open_alex |
| 82 | [Sparse-Sparse Matrix Multiplication Accelerator on FPGA featuring Distribute-Merge Product Dataflow](https://doi.org/10.1109/asp-dac58780.2024.10473865) | 2024-01-22 | 2024 29th Asia and South Pacific Design Automation Conference (ASP-DAC) | 2 | 3 | crossref |
| 83 | [An FPGA-Based High-Throughput Dataflow Accelerator for Lightweight Neural Network](https://doi.org/10.1109/iscas58744.2024.10558315) | 2024-05-19 | 2024 IEEE International Symposium on Circuits and Systems (ISCAS) | 2 | 3 | crossref |
| 84 | [End-to-end Compilation is All FPGAs Need: A Unified Overlay-based FPGA Compiler for Deep Learning](https://doi.org/10.1145/3658617.3697562) | 2025-01-20 | Proceedings of the 30th Asia and South Pacific Design Automation Conference | 2 | 3 | crossref |
| 85 | [Scaling LLM Speculative Decoding: Non-Autoregressive Forecasting in Large-Batch Scenarios](http://arxiv.org/abs/2511.20340v1) | 2025-11-25 | arXiv | 1 | 3 | arxiv, crossref |
| 86 | [Improving the Performance of Out-of-Core LLM Inference Using Heterogeneous Host Memory](https://doi.org/10.1109/iiswc66894.2025.00035) | 2025-10-12 | n/a | 0 | 3 | open_alex |
| 87 | [Microarchitectural extension of CGRA accelerator for efficient LLM code mapping](https://doi.org/10.26240/heal.ntua.30549) | 2025-01-01 | National Technical University of Athens (NTUA) | 0 | 3 | open_alex |
| 88 | [FPGA-Accelerated RISC-V ISA Extensions for Efficient Neural Network Inference on Edge Devices](http://arxiv.org/abs/2511.06955v1) | 2025-11-10 | arXiv | 0 | 3 | arxiv |
| 89 | [Not All Thoughts Need HBM: Semantics-Aware Memory Hierarchy for LLM Reasoning](http://arxiv.org/abs/2605.09490v1) | 2026-05-10 | arXiv | 0 | 3 | arxiv |
| 90 | [FBI-LLM: Scaling Up Fully Binarized LLMs from Scratch via Autoregressive Distillation](http://arxiv.org/abs/2407.07093v1) | 2024-07-09 | arXiv | 0 | 3 | arxiv |
| 91 | [Improving QA Efficiency with DistilBERT: Fine-Tuning and Inference on mobile Intel CPUs](http://arxiv.org/abs/2505.22937v1) | 2025-05-28 | arXiv | 0 | 3 | arxiv |
| 92 | [The classical limit of quantum mechanics through coarse-grained measurements](http://arxiv.org/abs/2503.15642v2) | 2025-03-19 | arXiv | 0 | 3 | arxiv |
| 93 | [Improved Multiscale Structural Mapping with Supervertex Vision Transformer for the Detection of Alzheimer's Disease Neurodegeneration](http://arxiv.org/abs/2604.14837v1) | 2026-04-16 | arXiv | 0 | 3 | arxiv |
| 94 | [Compiler Support for Speculation in Decoupled Access/Execute Architectures](http://arxiv.org/abs/2501.13553v1) | 2025-01-23 | arXiv | 0 | 3 | arxiv |
| 95 | [Fully integrating the Flang Fortran compiler with standard MLIR](http://arxiv.org/abs/2409.18824v1) | 2024-09-27 | arXiv | 0 | 3 | arxiv |
| 96 | [Balancing Compute in LLM Inference: Model Selection, Quantization, and Test-Time Scaling](https://doi.org/10.1145/3805621.3807631) | 2026-04-27 | Proceedings of the Sixth European Workshop on Machine Learning and Systems | 0 | 3 | crossref |
| 97 | [Enhancing Low-Light Image Reconstruction via Non-Autoregressive Transformers: A Mask-Aware Latent Integration Framework](https://doi.org/10.1109/isie62713.2025.11124638) | 2025-06-20 | 2025 IEEE 34th International Symposium on Industrial Electronics (ISIE) | 0 | 3 | crossref |
| 98 | [Operator Formulation of Topological Sectors and Coarse-Grained Multiplicity Geometry in Yang–Mills Theory](https://doi.org/10.2139/ssrn.5903410) | n/a | n/a | 0 | 3 | crossref |
| 99 | [BPS2025 - Learning memory kernel parameters for coarse-grained simulations](https://doi.org/10.1016/j.bpj.2024.11.1873) | 2025-02 | Biophysical Journal | 0 | 3 | crossref |
| 100 | [CFPara: a combination of coarse and fine-grained FPGA parallel routing methods](https://doi.org/10.1117/12.3033797) | 2024-06-13 | International Conference on Image, Signal Processing, and Pattern Recognition (ISPP 2024) | 0 | 3 | crossref |
| 101 | [BPS2026 – Correlations between lipid membrane fusion and membrane elastic properties in coarse-grained simulations](https://doi.org/10.1016/j.bpj.2025.11.1251) | 2026-02 | Biophysical Journal | 0 | 3 | crossref |
| 102 | [NX-CGRA: A Programmable Hardware Accelerator for Core Transformer Algorithms on Edge Devices](https://doi.org/10.23919/date69613.2026.11539188) | 2026-04-20 | 2026 Design, Automation &amp; Test in Europe Conference (DATE) | 0 | 3 | crossref |
| 103 | [Efficient LLMs for Edge Devices: Pruning, Quantization, and Distillation Techniques](https://doi.org/10.1109/icmlas64557.2025.10968787) | 2025-03-10 | n/a | 11 | 2 | open_alex |
| 104 | [Multi-Modal Instruction Tuned LLMs with Fine-Grained Visual Perception](https://doi.org/10.1109/cvpr52733.2024.01326) | 2024-06-16 | n/a | 10 | 2 | open_alex |
| 105 | [Sparrow ECC: A Lightweight ECC Approach for HBM Refresh Reduction towards Energy-efficient DNN Inference](https://doi.org/10.1145/3665314.3670825) | 2024-08-05 | n/a | 5 | 2 | open_alex |
| 106 | [AMALI: An Analytical Model for Accurately Modeling LLM Inference on Modern GPUs](https://doi.org/10.1145/3695053.3731064) | 2025-06-20 | n/a | 2 | 2 | open_alex |
| 107 | [SnipSnap: A Joint Compression Format and Dataflow Co-Optimization Framework for Efficient Sparse LLM Accelerator Design](https://doi.org/10.1109/asp-dac66049.2026.11420607) | 2026-01-19 | 2026 31st Asia and South Pacific Design Automation Conference (ASP-DAC) | 1 | 2 | crossref |
| 108 | [VEDA: Efficient LLM Generation Through Voting-based KV Cache Eviction and Dataflow-flexible Accelerator](https://doi.org/10.1109/dac63849.2025.11132861) | 2025-06-22 | 2025 62nd ACM/IEEE Design Automation Conference (DAC) | 1 | 2 | crossref |
| 109 | [Leveraging MLIR for Efficient Irregular-Shaped CGRA Overlay Design: (PhD Forum Paper)](https://doi.org/10.1109/asap61560.2024.00048) | 2024-07-24 | 2024 IEEE 35th International Conference on Application-specific Systems, Architectures and Processors (ASAP) | 1 | 2 | crossref |
| 110 | [MLIR-to-CGRA: A Versatile MLIR-Based Compiler Framework for CGRAs](https://doi.org/10.1109/asap61560.2024.00045) | 2024-07-24 | 2024 IEEE 35th International Conference on Application-specific Systems, Architectures and Processors (ASAP) | 1 | 2 | crossref |
| 111 | [Systolic Sparse Tensor Slices: FPGA Building Blocks for Sparse and Dense AI Acceleration](http://arxiv.org/abs/2502.03763v1) | 2025-02-06 | arXiv | 0 | 2 | arxiv |
| 112 | [YouZhi: Towards High-Concurrency Financial LLMs via Adaptive GQA-to-MLA Transition](http://arxiv.org/abs/2606.05868v1) | 2026-06-04 | arXiv | 0 | 2 | arxiv |
| 113 | [Inference on Variable Importance for Treatment Effect Heterogeneity: Shapley Values and Beyond](http://arxiv.org/abs/2510.18843v2) | 2025-10-21 | arXiv | 0 | 2 | arxiv |
| 114 | [Challenges and opportunities for AI to help deliver fusion energy](http://arxiv.org/abs/2603.25777v2) | 2026-03-26 | arXiv | 0 | 2 | arxiv |
| 115 | [SmartSwap: Swap-Based Memory Optimization for LLM Training under Varying Operator Sequences](http://arxiv.org/abs/2509.11076v2) | 2025-09-14 | arXiv | 0 | 2 | arxiv |
| 116 | [RCW-CIM: A Digital CIM-based LLM Accelerator with Read-Compute/Write](https://doi.org/10.1109/iscas66217.2026.11562180) | 2026-05-24 | 2026 IEEE International Symposium on Circuits and Systems (ISCAS) | 0 | 2 | crossref |
| 117 | [When More Thinking Hurts: Overthinking in LLM Test-Time Compute Scaling](https://doi.org/10.18653/v1/2026.findings-acl.1199) | 2026 | Findings of the Association for Computational Linguistics: ACL 2026 | 0 | 2 | crossref |
| 118 | [SATORU: Proactive Length-Aware Scheduling for High-Throughput Batch LLM Serving](https://doi.org/10.5220/0014919300004039) | 2026 | Proceedings of the 16th International Conference on Cloud Computing and Services Science | 0 | 2 | crossref |
| 119 | [Two-Sided Matching for Batch-Aware LLM Request Scheduling in Edge Networks](https://doi.org/10.1109/lcn65610.2025.11146293) | 2025-10-13 | 2025 IEEE 50th Conference on Local Computer Networks (LCN) | 0 | 2 | crossref |
| 120 | [Edge-Deployed Context-Aware LLM Framework for Low-Latency Bi-Directional Gaze-Speech HRI](https://doi.org/10.20944/preprints202602.0308.v1) | n/a | n/a | 0 | 2 | crossref |
| 121 | [Low Code RAG-LLM Framework for Context-Aware Querying in Electrical Standards, Design, and Research](https://doi.org/10.20944/preprints202507.0537.v1) | n/a | n/a | 0 | 2 | crossref |
| 122 | [Low-Complexity Content-Aware Encoding Optimization of Batch Video](https://doi.org/10.2139/ssrn.4772840) | n/a | n/a | 0 | 2 | crossref |
| 123 | [CPP: Clustered NPU-PIM Heterogeneous Computing Topology for LLM Inference](https://doi.org/10.1109/itc-cscc66376.2025.11137596) | 2025-07-07 | 2025 International Technical Conference on Circuits/Systems, Computers, and Communications (ITC-CSCC) | 0 | 2 | crossref |
| 124 | [Temperature-Zero Does Not Guarantee Hardware-Invariant Determinism: A Pilot Study of CPU-GPU Divergence in Llama 3 Inference](https://doi.org/10.2139/ssrn.6347418) | n/a | n/a | 0 | 2 | crossref |
| 125 | [Lembda: Optimizing LLM Inference on Embedded Platforms via CPU/FPGA Co-processing](https://doi.org/10.1007/978-981-95-1021-4_35) | 2026 | Lecture Notes in Computer Science Advanced Parallel Processing Technologies | 0 | 2 | crossref |
| 126 | [Adaptive Token Routing for Heterogeneous LLM Inference in Edge-Cloud Continuum](https://doi.org/10.1109/southeastcon63549.2026.11476596) | 2026-02-20 | SoutheastCon 2026 | 0 | 2 | crossref |
| 127 | [Fine-Grained and Coarse-Grained Contrastive Learning for Text Classification](https://doi.org/10.2139/ssrn.4691077) | n/a | n/a | 0 | 2 | crossref |
| 128 | [DynamoLLM: Designing LLM Inference Clusters for Performance and Energy Efficiency](https://doi.org/10.1109/hpca61900.2025.00102) | 2025-03-01 | n/a | 71 | 1 | open_alex |
| 129 | [HDLEval Benchmarking LLMs for multiple HDLs](https://doi.org/10.1109/lad62341.2024.10691770) | 2024-06-28 | n/a | 8 | 1 | open_alex |
| 130 | [Dual Grained Quantization: Efficient Fine-Grained Quantization for Llm](https://doi.org/10.2139/ssrn.4984291) | 2024-01-01 | SSRN Electronic Journal | 4 | 1 | open_alex |
| 131 | [Confidential LLM Inference: Performance and Cost Across CPU and GPU TEEs](https://doi.org/10.1109/iiswc66894.2025.00017) | 2025-10-12 | 2025 IEEE International Symposium on Workload Characterization (IISWC) | 3 | 1 | crossref |
| 132 | [Speculative Decoding on the SN40L Reconfigurable Dataflow Unit](https://doi.org/10.1109/mm.2025.3592570) | 2025-07-29 | IEEE Micro | 0 | 1 | open_alex |
| 133 | [Applications of Particle Accelerators](http://arxiv.org/abs/2407.10216v1) | 2024-07-14 | arXiv | 0 | 1 | arxiv |
| 134 | [Counting of lattices containing up to five comparable reducible elements and having nullity up to three](http://arxiv.org/abs/2503.13519v1) | 2025-03-14 | arXiv | 0 | 1 | arxiv |
| 135 | [Counting of lattices containing up to four comparable reducible elements and having nullity up to three](http://arxiv.org/abs/2412.03627v2) | 2024-12-04 | arXiv | 0 | 1 | arxiv |
| 136 | [ENN's Roadmap for Proton-Boron Fusion Based on Spherical Torus](http://arxiv.org/abs/2401.11338v3) | 2024-01-20 | arXiv | 0 | 1 | arxiv |
| 137 | [Perancangan Struktur Fitur Aplikasi Warung Kopi Menggunakan LLM](https://doi.org/10.51454/decode.v5i3.1442) | 2025-11-26 | Decode: Jurnal Pendidikan Teknologi Informasi | 0 | 1 | crossref |
| 138 | [AI-Powered, But Power-Hungry? Energy Efficiency of LLM-Generated Code](https://doi.org/10.1109/forge66646.2025.00012) | 2025-04-27 | n/a | 12 | 0 | open_alex |
| 139 | [Kangaroo: Lossless Self-Speculative Decoding for Accelerating LLMs via Double Early Exiting](https://doi.org/10.52202/079017-0381) | 2024-01-01 | n/a | 1 | 0 | open_alex |
| 140 | [Deblur e-NeRF: NeRF from Motion-Blurred Events under High-speed or Low-light Conditions](http://arxiv.org/abs/2409.17988v1) | 2024-09-26 | arXiv | 0 | 0 | arxiv |
| 141 | [[survey] Multimodal Fusion and Vision-Language Models: A Survey for Robot Vision](http://arxiv.org/abs/2504.02477v3) | 2025-04-03 | arXiv | 0 | 5 | arxiv |
| 142 | [[survey] A Review of FPGA-Driven LLM Acceleration](https://doi.org/10.1109/mcsoc67473.2025.00018) | 2025-12-15 | n/a | 0 | 3 | open_alex |

## Connector Errors

The snapshot kept results from healthy connectors instead of treating a failing source as zero evidence. DBLP failed all six queries. Semantic Scholar accepted one query and rate-limited five. OpenAlex completed 60 hits after five HTTP 504 retries; OpenReview completed with zero hits in the canonical rerun. The terminal source errors are reproduced verbatim:

```text
[dblp] Error on query 'FPGA LLM shared compute engine time multiplexed accelerator': HTTPSConnectionPool(host='dblp.org', port=443): Max retries exceeded with url: /search/publ/api?q=FPGA+LLM+shared+compute+engine+time+multiplexed+accelerator&format=json&h=10&f=0 (Caused by SSLError(SSLEOFError(8, 'EOF occurred in violation of protocol (_ssl.c:1129)')))
[dblp] Error on query 'FPGA LLM spatial dataflow streaming accelerator': HTTPSConnectionPool(host='dblp.org', port=443): Read timed out. (read timeout=15.0)
[dblp] Error on query 'HBM aware low batch autoregressive LLM decode FPGA': HTTPSConnectionPool(host='dblp.org', port=443): Max retries exceeded with url: /search/publ/api?q=HBM+aware+low+batch+autoregressive+LLM+decode+FPGA&format=json&h=10&f=0 (Caused by SSLError(SSLEOFError(8, 'EOF occurred in violation of protocol (_ssl.c:1129)')))
[dblp] Error on query 'CPU FPGA heterogeneous llama.cpp GGML LLM inference offload': HTTPSConnectionPool(host='dblp.org', port=443): Max retries exceeded with url: /search/publ/api?q=CPU+FPGA+heterogeneous+llama.cpp+GGML+LLM+inference+offload&format=json&h=10&f=0 (Caused by SSLError(SSLEOFError(8, 'EOF occurred in violation of protocol (_ssl.c:1129)')))
[dblp] Error on query 'FPGA LLM operator fusion coarse grained execution persistent kernel': HTTPSConnectionPool(host='dblp.org', port=443): Max retries exceeded with url: /search/publ/api?q=FPGA+LLM+operator+fusion+coarse+grained+execution+persistent+kernel&format=json&h=10&f=0 (Caused by SSLError(SSLEOFError(8, 'EOF occurred in violation of protocol (_ssl.c:1129)')))
[dblp] Error on query 'FPGA transformer overlay CGRA compiler mapping': HTTPSConnectionPool(host='dblp.org', port=443): Max retries exceeded with url: /search/publ/api?q=FPGA+transformer+overlay+CGRA+compiler+mapping&format=json&h=10&f=0 (Caused by SSLError(SSLEOFError(8, 'EOF occurred in violation of protocol (_ssl.c:1129)')))
[semantic_scholar] Error on query 'FPGA LLM shared compute engine time multiplexed accelerator': 429 Client Error:  for url: https://api.semanticscholar.org/graph/v1/paper/search?query=FPGA+LLM+shared+compute+engine+time+multiplexed+accelerator&offset=0&limit=10&fields=title%2Cauthors%2Cyear%2Cabstract%2CcitationCount%2Curl%2Cvenue%2CpublicationDate%2CexternalIds&year=2024-2026
[semantic_scholar] Error on query 'FPGA LLM spatial dataflow streaming accelerator': 429 Client Error:  for url: https://api.semanticscholar.org/graph/v1/paper/search?query=FPGA+LLM+spatial+dataflow+streaming+accelerator&offset=0&limit=10&fields=title%2Cauthors%2Cyear%2Cabstract%2CcitationCount%2Curl%2Cvenue%2CpublicationDate%2CexternalIds&year=2024-2026
[semantic_scholar] Error on query 'HBM aware low batch autoregressive LLM decode FPGA': 429 Client Error:  for url: https://api.semanticscholar.org/graph/v1/paper/search?query=HBM+aware+low+batch+autoregressive+LLM+decode+FPGA&offset=0&limit=10&fields=title%2Cauthors%2Cyear%2Cabstract%2CcitationCount%2Curl%2Cvenue%2CpublicationDate%2CexternalIds&year=2024-2026
[semantic_scholar] Error on query 'CPU FPGA heterogeneous llama.cpp GGML LLM inference offload': 429 Client Error:  for url: https://api.semanticscholar.org/graph/v1/paper/search?query=CPU+FPGA+heterogeneous+llama.cpp+GGML+LLM+inference+offload&offset=0&limit=10&fields=title%2Cauthors%2Cyear%2Cabstract%2CcitationCount%2Curl%2Cvenue%2CpublicationDate%2CexternalIds&year=2024-2026
[semantic_scholar] Error on query 'FPGA transformer overlay CGRA compiler mapping': 429 Client Error:  for url: https://api.semanticscholar.org/graph/v1/paper/search?query=FPGA+transformer+overlay+CGRA+compiler+mapping&offset=0&limit=10&fields=title%2Cauthors%2Cyear%2Cabstract%2CcitationCount%2Curl%2Cvenue%2CpublicationDate%2CexternalIds&year=2024-2026
```

## Model Knowledge / Locally Verified Anchors

These verified library anchors were not duplicated in the API table and are included as contextual recall rather than fresh API hits.

| # | Title | Year | Venue | Notes |
|---:|---|---:|---|---|
| 1 | [CODO: An Automated Compiler for Comprehensive Dataflow Optimization](https://arxiv.org/abs/2604.12618) | 2026 | arXiv | Compiler-level dataflow optimization reference already cached locally. |
| 2 | [FlexLLM: Composable HLS Library for Flexible Hybrid LLM Accelerator Design](https://arxiv.org/abs/2601.15710) | 2026 | arXiv | HLS composition anchor for implementation alternatives. |
| 3 | [TeLLMe: An Efficient End-to-End Ternary LLM Prefill and Decode Accelerator](https://arxiv.org/abs/2510.15926) | 2026 | FPGA | End-to-end prefill/decode specialization anchor. |
| 4 | [PD-Swap: Prefill-Decode Logic Swapping](https://arxiv.org/abs/2512.11550) | 2025 | arXiv | Dynamic phase-specialization contrast. |
| 5 | [SkipOPU: An FPGA-Based Overlay Processor for Large Language Models](https://arxiv.org/abs/2603.14785) | 2026 | arXiv | Overlay and dynamic-computation comparison. |

## Overview

The unfiltered six-query union returned 142 unique 2024-2026 records. It has high recall but deliberate noise: generic terms such as `coarse-grained`, `fusion`, and `HBM` pull in unrelated simulation, vision, and physics papers, so only a DOI/arXiv/title-deduplicated direct-relevance subset is promoted into the local FPGA LLM library.

## Trends

The strongest directly relevant movement is from isolated accelerator kernels toward execution granularity and control: persistent mega-kernels, graph fusion, streaming engines, HBM-channel-aware overlays, and orchestration measurement. The corpus also shows that high-batch multi-FPGA decode, spatial mapping, and low-batch memory-centric designs remain separate literatures; none establishes strict llama.cpp/GGML zero-fallback semantics on U280.

## Key Themes

1. Spatial and overlay mapping: static or programmable placement of transformer work across PEs/cores ([1], [8], [7]).
2. Coarse-grained/persistent execution: shrinking host-visible launch boundaries through a mega-kernel or larger PEs ([3], [19], [64]).
3. HBM and decode dataflow: memory placement, KV state, and master/slave or streaming decode architectures ([4], [8], [28]).
4. Heterogeneous runtime boundaries: CPU/FPGA or multi-stage systems expose scheduling and transfer decisions but generally permit ordinary fallback ([13], [27], [125]).
5. Dataflow and fusion: keeping tensors resident across dependent work rather than materializing host-visible intermediates ([10], [81], [65]).

## Keywords Frequency

| Keyword | Count |
|---|---:|
| LLM / LLMs | 65 |
| FPGA / FPGAs | 45 |
| inference | 40 |
| accelerator / acceleration | 37 |
| dataflow | 22 |

## Most Cited by Accepted Paper

| Rank | Title | Year | Citations |
|---:|---|---:|---:|
| 1 | DynamoLLM: Designing LLM Inference Clusters for Performance and Energy Efficiency | 2025 | 71 |
| 2 | Understanding the Potential of FPGA-based Spatial Acceleration for Large Language Model Inference | 2024 | 63 |
| 3 | EdgeLLM: A Highly Efficient CPU-FPGA Heterogeneous Edge Accelerator for Large Language Models | 2025 | 48 |
| 4 | MECLA: Memory-Compute-Efficient LLM Accelerator with Scaling Sub-matrix Partition | 2024 | 24 |
| 5 | FPGA-based low-light image enhancement using Retinex algorithm and coarse-grained reconfigurable architecture | 2024 | 21 |

## Most Cited by First Author

| Rank | Author | Papers in set | Total citations |
|---:|---|---:|---:|
| 1 | Jovan Stojkovic | 1 | 71 |
| 2 | Hongzheng Chen | 1 | 63 |
| 3 | Mingqiang Huang | 1 | 48 |
| 4 | Yubin Qin | 1 | 24 |
| 5 | S. Munaf | 1 | 21 |

## Recommendations for Reading

1. [Understanding the Potential of FPGA-based Spatial Acceleration for Large Language Model Inference](https://doi.org/10.1145/3656177): establishes the spatial-mapping baseline and its constraints.
2. [EdgeLLM](https://doi.org/10.1109/TCSI.2025.3546256): closest established CPU-FPGA heterogeneous LLM system in the corpus.
3. [StreamTensor](https://arxiv.org/abs/2509.13694): frames dataflow residency and tensor streaming at LLM scale.
4. [MPK](https://arxiv.org/abs/2512.22219): strongest persistent/coarse-grained execution contrast, while clearly GPU-specific.
5. [FlightOPU](https://doi.org/10.1109/ICFPT67023.2025.00048): direct HBM-aware overlay comparator for the U280-oriented design space.

The curated subset, PDF provenance, and architecture synthesis are in [[research/fpga-llm-inference/literature-search-2026-07-28]] and [[research/fpga-llm-inference/execution-architecture-taxonomy]].

---
title: FPGA LLM Inference
domain: research
area: fpga-llm-inference
type: overview
status: active
updated: 2026-09-07
tags: [fpga, llm-inference, llama-cpp, ggml, xrt, end-to-end]
---

# FPGA LLM Inference

这个 area 研究 FPGA 上的大语言模型推理，重点不是孤立 kernel 的峰值，而是从真实模型、推理框架和运行时出发，建立可验证的端到端系统。

当前项目主线是：在 AMD/Xilinx Alveo U280 上实现原生 `llama.cpp`/GGML FPGA backend，以 Gemma 3 1B F16 为当前验证模型，通过明确的 operator contract、XRT 执行收据和 zero-fallback 证据保证语义闭合，再逐步收缩运行时开销。

## Current Position

1. **系统集成已经成立，性能尚未成立。** 当前 backend 已严格执行 11 个 GGML operator family，开发板 trace 中有 2,422 次 accepted FPGA dispatch、zero fallback。
2. **首要瓶颈不是单个矩阵核。** `pp512` 有 224,936 次 XRT launch，`tg128` 有 202,530 次；host-observed XRT wait 分别占 operator wall time 的 96.25% 和 79.58%。
3. **CODO 是必须重点理解的对照。** 它把 GPT-2 block 编译成 coarse-grained dataflow kernel，并报告 U280 上 GPT-2 Medium 的 TTFT、decode token/s 和生成 latency。它说明 whole-block streaming、数据移动优化和 launch amortization 能把 FPGA 推理推到完全不同的性能区间。
4. **直接比较数字前必须统一边界。** CODO 的公开 artifact 计时边界、模型、W4A8 数值格式和生成 harness 与当前 Gemma 3 1B F16 `llama-bench` 路径不同，不能把 `231.48 tok/s` 与当前 `1.32 tok/s` 直接解释成加速比。
5. **一个受限 research idea 已通过审计，但尚无性能结论。** 新的 `idea-spark` run 生成了 Visibility-Sensitive Trace Compression (VSTC)：按原始 GGML 调用的可观察性分区来保留 H 边界、流式解释 B 模板，并以严格 zero fallback、artifact identity 和显式错误为前提。它是可证伪的提案，不是已测得的 U280 加速结果。

## Navigation

| Page | Role |
|---|---|
| [[research/fpga-llm-inference/foundations]] | LLM 推理阶段、FPGA 资源、映射方法和性能瓶颈背景 |
| [[research/fpga-llm-inference/system-landscape]] | DFX、FlightLLM、Spatial LLM、StreamTensor、CODO、EdgeLLM、TeLLMe 等工作地图 |
| [[research/fpga-llm-inference/vitis-ai-dpu-finn-pynq]] | Vitis AI DPU、FINN、PYNQ/PINN 消歧；官方工具链、架构对照、版本与 U280/LLM 支持边界 |
| [[research/fpga-llm-inference/codo-2026]] | CODO 论文与 artifact 深读，重点核对 GPT 端到端指标及其测量边界 |
| [[research/fpga-llm-inference/project-status-2026-07]] | 远端论文草稿和 retained evidence 的项目状态综合 |
| [[research/fpga-llm-inference/towards-idea-audit-2026-07]] | Idea Spark 对当前稿件和 RegionSeal 候选的失败审计、停止条件与重新启动证据门槛 |
| [[research/fpga-llm-inference/end-to-end-evaluation]] | 与 CODO/DFX/StreamTensor 可辩护对比的端到端评测协议 |
| [[research/fpga-llm-inference/literature-search-2026-07-22]] | 本轮多源检索、失败记录、验证来源和阅读顺序 |
| [[research/fpga-llm-inference/literature-search-2026-07-28]] | 2024-2026 全源 union search、142 条完整结果、connector 错误、15 篇增量归档与阅读路径 |
| [[research/fpga-llm-inference/execution-architecture-taxonomy]] | shared-engine temporal reuse、overlay、streaming dataflow 与 spatial mapping 的边界，以及 `llama.v`/active backend 定位 |
| [[research/fpga-llm-inference/ideaspark-shared-engine-2026-07-28]] | VSTC 的完整 IdeaSpark 结果、最近工作差异、最小伪证实验、负对照和停止条件 |
| [[research/fpga-llm-inference/papers/index]] | 68 篇原 Related Work 加 15 篇架构增量、50 份已验证全文 PDF、BibTeX、来源和完整性哈希 |
| [[research/fpga-llm-inference/fpga-backbone-llamacpp-note]] | 2026-06-17 的早期 llama.cpp 集成判断，保留作历史快照 |

## The Central Systems Gap

当前系统与 CODO/StreamTensor 的最关键差异可以压缩成一张表：

| Dimension | Current llama.cpp FPGA backend | CODO / StreamTensor style |
|---|---|---|
| Application boundary | 原生 GGML device/backend | PyTorch/Torch-MLIR 到专用 accelerator |
| Mapping unit | accepted GGML node / operator contract | fused transformer block / model graph |
| Runtime behavior | 大量细粒度 XRT launch + blocking wait | 少量 coarse-grained dataflow launch |
| Generality | framework-native、显式 support gate、可替换 ABI | compiler/model graph 可重生成 |
| Current strength | 真实 GGML graph、strict execution、evidence closure | 高吞吐 dataflow、通信优化、TTFT/decode 结果 |
| Current weakness | launch/sync expansion 极大，F16 带宽压力高 | artifact 与应用级 tokenizer/sampler 边界不完全等同 |

因此近期最有价值的问题不是“再优化一个 `MUL_MAT`”，而是：

> 能否从真实 GGML graph 中识别 contract-closed region，把多个 accepted node 编译或调度成 persistent/coarse-grained FPGA dataflow，同时保留 support semantics、数值 oracle、artifact identity 和 fallback audit？

2026-07-28 的新 run 将这个问题收束为 VSTC：以每个原始 GGML 调用的 host-read、alias、state、consumer、allocation、scratch 和 explicit-error 事实决定其是否可进入 B 模板，并保留每个逻辑调用的 completion-ring 状态。它通过了 coherence、collision、独立 anti-pattern 修订和伪证复审；完整定义、负对照与停止条件见 [[research/fpga-llm-inference/ideaspark-shared-engine-2026-07-28]]。[[research/fpga-llm-inference/towards-idea-audit-2026-07]] 保留为 RegionSeal 的历史失败审计，而非当前候选。

## Immediate Priorities

1. 按 [[research/fpga-llm-inference/end-to-end-evaluation]] 冻结测量边界、trace schema 和每个原始 GGML 调用的 baseline XRT submission 计数。
2. 在 pp512/tg128 上先观测 VSTC 的 H/B 分布、`rho`、拒绝原因和 scratch-pressure；没有可准入 B population 或 `rho = 0` 时停止该机制，而不是把普通 resident engine 重新命名为 VSTC。
3. 实现 H descriptor、B template、per-call completion ring 和 scratch lease 的最小控制面；任何未捕获 reader、alias/state effect、mandatory allocation failure 或 engine failure 都必须回到原始调用的显式错误，且不允许 CPU fallback。
4. 用同一内核和输入完成三个分离对照：native per-XRT、naive resident descriptor、VSTC；再分别比较 homogeneous single/multi-record interpreter 与 mixed-trace B-admission-off，检查每一条贡献是否独立成立。
5. 若 bytewise logits 或 explicit-error trace 不一致，或 forced B denial 不能使 p50/p95 向 naive resident baseline 回归，则停止 VSTC claim；只有控制面问题压低后再评估 Q4/W4A8、HBM layout 和 kernel microarchitecture。

## Claim Discipline

- `csynth` 或 RTL simulation cycles 不是 board latency。
- positive WNS 不是实测频率。
- operator speedup 不是 token speedup。
- FPGA 文件存在不代表实际 dispatch；必须有执行收据。
- `llama-bench pp/tg` 是 model-phase benchmark，不自动等价于包含 tokenizer/sampler 的 application end-to-end。
- 不同模型、precision、card、batch、prompt/output length 和测量边界下的 token/s 只能做背景定位，不能做加速比。

返回 [[research/index]]。

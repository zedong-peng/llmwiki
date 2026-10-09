---
title: FPGA LLM Inference
domain: research
area: fpga-llm-inference
type: overview
status: active
updated: 2026-09-15
tags: [fpga, llm-inference, llama-cpp, ggml, xrt, end-to-end]
---

# FPGA LLM Inference

这个 area 研究 FPGA 上的大语言模型推理，重点不是孤立 kernel 的峰值，而是从真实模型、推理框架和运行时出发，建立可验证的端到端系统。

当前实现以 GPT-2 Medium Q4/Q6 U280 profile 为准：每次调用执行完整模型图，权重和 KV 常驻 HBM；仍有单模型、单序列及上下文限制，保留结果的板上正确性和完整验收未通过。详见下文 §Niche and Baseline Audit。下方 Gemma 3 1B F16 的逐算子测量和 VSTC 路线保留为历史记录。

本 area 同时保留不同日期、不同 profile 的证据；Gemma 1B 集成记录与下方 2026-09-07 GPT-2
profile 快照不能混合计算性能。

2026-09-08 按 Canonical Layout 收敛：本 `index.md` 是唯一正式合成页；`assets/` 是参考资料资产库；历史论文集合、统计与 BibTeX/哈希入口见下文 §Paper Library；`threads/ideaspark_run/` 是两次 IdeaSpark 原始运行存档。原先平铺的 13 个 loose 笔记（foundations、landscape、taxonomy、工具链对照、评测协议、CODO 深读、项目状态、两次文献检索、检索底表、VSTC 结果、失败审计、06-17 历史快照）已折入本页后删除，全文见 git 历史。其中 CODO 深读已合并为 [[research/fpga-llm-inference/assets/codo-2026/note|CODO 正式 paper note]]。2026-09-09 又折入 4 份九月证据页（niche-audit、evidence-matrix、KV-boundary、manuscript-recheck；其 hash 总账与 niche 抓包已删，见 git 历史）。按约定不建 `threads/index.md`。

## Historical Position (July 2026)

1. **系统集成已经成立，性能尚未成立。** 当前 backend 已严格执行 11 个 GGML operator family（`GET_ROWS`、`SCALE`、`MUL_MAT`、`RMS_NORM`、`MUL`、`ROPE`、`SET_ROWS`、`SOFT_MAX`、`ADD`、`GLU`、`CONT`），开发板 trace 中有 2,422 次 accepted FPGA dispatch、zero fallback。
2. **首要瓶颈不是单个矩阵核。** `pp512`（1,626 calls → 224,936 launches，138.34/call）与 `tg128`（104,877 calls → 202,530 launches，1.93/call）的 host-observed XRT wait 分别占 operator wall time 的 96.25% 和 79.58%。`pp512` 的 470 个 `MUL_MAT` 展开成 198,176 launches、52 个 `GLU` 展开成 25,656 launches；`tg128` 每个 `MUL_MAT` 平均 4 launches、每个 `GLU` 平均 3 launches。单图 XRT timeline（885.527 ms 窗口）呈 `H2D sync -> run::start -> blocking run::wait -> D2H sync` 重复：blocking wait 71.85%，H2D+D2H 12.90%，launch API 0.73%。xclbin 无 device trace monitor，host wait 尚不能拆成 kernel-active、queueing 与 runtime overhead。
3. **CODO 是必须重点理解的对照。** 它把 GPT-2 block 编译成 coarse-grained dataflow kernel，报告 U280 上 GPT-2 Medium 的 TTFT、decode token/s 和生成 latency。详见 [[research/fpga-llm-inference/assets/codo-2026/note|CODO]]（含 Table VI 复算、`[64:64]` 行 313.44ms vs 公式 309.12ms 差一个 decode interval 的记录，以及单 block artifact 无法直接溯源 24 层整模型结果的缺口）。
4. **直接比较数字前必须统一边界。** CODO 的 U280/W4A8/GPT-2 Medium 与当前 Gemma 3 1B F16 `llama-bench` 路径在模型、精度、板卡、batch、长度与计时边界上都不同，不能把 `231.48 tok/s` 与当前 `1.32 tok/s` 直接解释成加速比。`MUL_MAT` 只占 `pp512`/`tg128` operator wall time 的 18.64%/29.77%，清零也只给 1.229x/1.424x Amdahl 上界；decode 用 `n_vec=1`，加宽多向量路径解决不了该 workload。
5. **一个受限 research idea 已通过审计，但尚无性能结论。** Visibility-Sensitive Trace Compression (VSTC)：按原始 GGML 调用的可观察性分区保留 H 边界、流式解释 B 模板，以严格 zero fallback、artifact identity 和显式错误为前提。它是可证伪的提案，不是已测得的 U280 加速结果。RegionSeal 保留为历史失败审计，而非当前候选。

项目证据快照（2026-07-22，draft commit `7dc8a75`，backend commit `2616bb6`，另有未提交更新）：c64/c512 各 56 signatures 共 112；11/11 GGML-RTL 与 11/11 GGML-HLS 在确定性 c64 decode-median 点通过；33 行 CPU/RTL/HLS 对照表；22/22 OOC 构建资源 + 10ns WNS 记录；matched CPU/FPGA pp/tg 各 5 次同 commit/模型/harness。Matched 结果：CPU（socket 0 上 16 物理核）pp512 1.32s / 387.18 tok/s、tg128 60.62ms ITL / 16.50 tok/s；FPGA strict backend pp512 302.13s / 1.6946 tok/s、tg128 759.88ms / 1.3160 tok/s——prefill 慢 228.5x，decode 慢 12.54x。结论：framework 集成与稳定执行成立，加速不成立。待补：matched 功耗/能量、模型级质量、per-signature FPGA 数值重放、多模型/多卡可移植、contract-preserving replacement 的 E2E 增益。

### 2026-09-07 Profile Snapshot

The newer GPT-2 Medium Q4/Q6 U280 delivery is a separate, profile-complete path: GGUF load →
GGML graph verification → one stateful model-graph execution per call → persistent F16 KV →
logits → llama.cpp sampling. Its CPU/FPGA numbers are kept in the project report's three-column
table; Gemma remains an unmeasured row for that matched snapshot. CODO is intentionally retained as
a fixed-shape graph/dataflow reference, not merged into the stateful throughput result. The detailed
boundary and source ledger are in §KV-Cache Boundary below.

## Foundations（推理阶段 / FPGA 资源 / 映射家族）

请求至少经过：模型/bitstream 加载 → prompt 分词 → embedding → N token prefill → LM head + 首 token 采样 → 每步一 token 自回归 decode → detokenize/流式输出。

- **Prefill**：多 prompt token 并行，线性层 GEMM-like，attention 有二次项，通常 compute-bound，用户指标是 TTFT（注明 prompt 长度）。
- **Decode**：batch 1 下每步一 token，线性层 GEMV-like，每步重读大比例权重，算术强度低，KV-cache 流量随 context 增长，通常带宽/延迟界，指标是 ITL 与 token/s。GPU 天然强于 prefill；FPGA 在 batch-1 decode 靠精确精度、数据布局、内存通道、融合与持久状态才有竞争机会。

| Resource | LLM 推理角色 | 常见失效模式 |
|---|---|---|
| LUT / carry | 低位运算、控制、非线性近似、查表 | 布线压力、频率损失 |
| DSP | FP/定点 MAC、稠密 GEMM/GEMV | 窄 decode 下利用率低，或被不支持精度占用 |
| BRAM / URAM | activation tile、partial sum、FIFO、KV 切片、查表 | 容量溢出；banking 不良致端口冲突 |
| HBM | 数据中心卡权重与大 KV cache | bank 冲突、crossbar 局部性、短 burst、低 outstanding |
| DDR | 容量型存储、嵌入式板权重 | 带宽天花板主导 decode |
| PCIe / AXI | host-device 命令与 tensor 搬运 | 细粒度传输与同步主导 wall time |
| XRT/OpenCL runtime | bitstream、buffer、kernel 编排 | launch 膨胀、blocking wait、分配与同步开销 |

HBM 不能当平坦数组建模：pseudo-channel 放置、switch 拓扑、burst 长度、outstanding 与 PE 连接显著改变有效带宽。设计必须有显式 tensor-to-bank 布局与保持 residency 的 runtime。

映射家族：temporal overlay（DFX、Transformer-OPU 系；可复用但中间数据常回片外，指令/同步开销残留）；model-specific spatial dataflow（Spatial LLM、StreamTensor、CODO；生产消费重叠、片上转发、launch 少，但资源/布线压力大、模型形状特化、编译慢）；异构 CPU-FPGA（EdgeLLM 与当前 llama.cpp backend 同属大类但抽象层不同；集成分工优雅，但边界穿越、布局转换与 silent fallback 会抹掉加速）；多 FPGA appliance（DFX、FlightLLM 扩展分析、Terafly；容量带宽扩展，但同步与网络流量成一阶延迟项）；阶段解耦（GLITCHES 用 GPU-FPGA 协作，TeLLMe 单卡分 prefill/decode datapath，FAST-Prefill 只做长 context prefill）。

量化是架构选择：F16 易做语义基线但带宽/DSP 贵；W8A8/W4A8  packing 密、每 DSP 更多 MAC，需 scale/dequant；W4A16 对 decode 友好；mixed 3-5bit 匹配层敏感度但 decoder/格式复杂；ternary W1.58A8 把乘法换成 pass/negate/zero 或查表，压力转到 LUT/URAM；稀疏只有 metadata、负载均衡与稀疏 datapath 开销受控才减少有效工作。跨论文比较必须同时报告模型质量与数值路径，W4A8 GPT-2 不能与 F16 Gemma 做纯硬件比较。

期望 residency 层次：权重 host→FPGA HBM/DDR 一次、跨请求复用；activation 生产者→片上 stream/buffer→消费者；KV cache 持久 device 内存增量更新；命令按 block/region 粒度而非 tile 粒度；只在 sampler 边界需要时才输出 logits/top-k/token。反模式：每 tensor tile 或每 accepted graph node 重复分配/pack/传输/launch/wait/拷回/unpack。分解式：`T_request = T_tokenize + T_prefill + Σ(T_decode,i + T_sample,i) + T_detokenize`；每加速阶段 `T_phase = T_host + T_H2D + T_queue + T_kernel + T_D2H + T_sync`。无 device timestamp 时 host 侧 `run::wait` 是 queueing + device 执行 + runtime 开销的混合物，不得标成纯 kernel 时间或纯调度开销。

对本项目的含义：F16 适合语义 bring-up，不是可信终点带宽点；native GGML backend 只有不强制 per-node/per-tile 同步执行才有价值；下一架构单元应是 contract-closed graph region/Transformer block 而非孤立算子替换；正确性保持多级（operator oracle、graph support audit、zero fallback、模型输出/质量、source-to-xclbin identity）；优化顺序：测量边界 → launch/sync 缩减 → residency/overlap → 精度/布局 → kernel 算术。

## Evaluation Protocol（K0–A5 / 指标 / 门控 / 对比规则）

目标：既能与 CODO/StreamTensor/DFX/FlightLLM 的 GPT/LLM 指标对话，又不牺牲当前 `llama.cpp` 的真实框架、strict execution 与 evidence-closure 优势。模型阶段与应用请求必须分开报告。

| ID | Name | Timer starts | Timer ends | Required output |
|---|---|---|---|---|
| K0 | kernel | board kernel command starts | command completes | cycles/device time, bytes, shape |
| O1 | GGML operator | backend receives node | output tensor available | host phases, launches, oracle error |
| R2 | fused region/block | accepted region begins | all region outputs valid | region latency, launches, intermediate traffic |
| M3 | model phase | first prefill/decode graph begins | logits ready | pp/tg, TTFT component, ITL |
| G4 | generation harness | token IDs ready | requested output IDs produced | TTFT, decode speed, total latency |
| A5 | application request | text enters CLI/server | detokenized text emitted | cold/warm wall-clock |

不同 level 的结果不得互算 speedup。`TTFT = t_first - t_req`，分 `TTFT_model`（首次 prefill dispatch 起）与 `TTFT_app`（文本到达起，含分词与 host 准备）；`ITL_i = t_i - t_{i-1}`（`i>1`），报告 mean/median/p95/p99，不从 aggregate token/s 反推尾部；稳态 decode 吞吐 `R_decode = (N_out-1)/(t_Nout - t_1)`，复现论文若用 `N_out/decode_time` 则另列一栏；CODO 兼容列专用 `T_CODO = TTFT + N_out/R_decode`，保留其 `[64:64]` 313.44ms 原值不静默修复；应用延迟 `T_app = t_done - t_req`，区分 cold（进程启动+模型解析+bitstream+权重上传+请求）/warm（常驻后）/steady（显式 warm-up 后重复 warm）。

每行结果必须带不可变元数据：模型（family/变体/参数/层-hidden-FFN/模型哈希）；数值路径（GGUF dtype/量化、activation/KV 精度、scale 格式、质量指标）；workload（prompt 文本或 token IDs、`N_in`/`N_out`、batch、context、sampler、seed、stop 策略）；FPGA（卡、器件、BDF、实测时钟、bitstream 哈希）；内存（HBM/DDR 容量、bank map、权重 residency、KV 策略、实测字节）；host（CPU/NUMA/亲和/governor/RAM/OS）；工具链（commit、编译 flags、XRT/Vitis/Vivado、firmware/platform）；计时（timer API、包含/排除阶段、warm-up、重复数、聚合方式）；执行（accept/reject/fallback 节点数、launch 数、trace 可用性）；能量（测量工具、采样率、idle 扣除、host/card/system 边界）。

正确性门控（性能可发表的前提）：operator 数值 gate（对 CPU/GGML oracle）；region 图 gate（fused vs unfused）；support gate（accepted 必 FPGA 执行，rejected 显式）；fallback audit（strict 要求声明 scope 内 zero fallback）；artifact identity（源码哈希→综合报告→xclbin 哈希→运行时加载哈希）；模型 gate（next-token logits/top-k 或确定性 greedy 在容差内）；质量 gate（量化/近似路径的 perplexity 或任务指标）；真实输入 gate（至少一次非零真实 prompt/权重 retained run，零填充 smoke 不算质量证据）。

Runtime 分解（非重叠 phases）：support/control、allocation、packing、H2D sync、queue/launch、run wait、D2H sync、unpacking、sampling；有 device trace 才把 run wait 拆成 queue/active/host blocking，否则保留 `host-observed XRT wait` 合名。报告：GGML calls、物理 launches、每 call/region/token launches、每请求/token 传输字节、常驻字节、分配数、同步数、timestamped event 的 overlap ratio。

实验矩阵：Matrix 1 当前集成基线（CPU vs FPGA strict vs batched/persistent vs fused region，同 Gemma 3 1B F16、同 pp32/64/128/512 + tg32/64/128；画 prefill rate vs prompt、ITL/decode vs context/output、每 token launch/字节、phase 分解、baseline→batching→fusion→quantization waterfall）；Matrix 2 CODO-compatible shape（GPT-2 Medium 24层 hidden1024 FFN4096 16头、W4A8、U280、`[32:32]/[64:64]/[128:128]` batch1、TTFT + decode + CODO-compatible 总延迟，额外披露 H2D/LM head/采样/真实权重/输出验证是否包含；同模型同语义跑通两套系统前不算 matched）；Matrix 3 应用 E2E（固定 token IDs 的 short 32/32、medium 128/128、long 512/128 真实文本语料，同 llama.cpp CLI/server 入口并排报告 A5 与 M3）。

CODO 复现 checklist：已完成 GitHub main/`isca2026-ae`/Zenodo 检查（三者均无附录承诺的 GPT xclbin/可执行/raw board log）、Table VI 三行复算 + 12 个 Fig. 9 点反推（保留 `[64:64]` 4.32ms 差异与 headline 聚合缺口）、四个 Fig. 9 输出路径审计（终结果全留片上、host buffer 全只读、D2H 省略）、时钟目标审计（论文称全 300MHz，128-token 公开构建用 250MHz/4.00ns）。待办：拿 GPT-2 Medium checkpoint 与量化 recipe、确认 Table VI 是否真实权重、拿 raw board log 与精确 xclbin、核 TTFT 计时边界、PCIe H2D 是否计入、LM head/采样是否计入、找到对外可见输出的 board 路径、非零输入+真实权重跑并对 PyTorch oracle、kernel event 与 request/model 时间分离记录、每 xclbin 实测时钟/platform/XRT/bitstream 哈希。

能量：至少报 card/FPGA rail 与整机 wall 两级；warm 请求 `E_request = ∫(P-P_idle)dt`、`E_token = E_request/N_out`，同时保留未扣 idle 总量，声明采样率与功率流-请求计时同步。统计：开发 ≥5 次、终版延迟分布 20+；固定 warm-up 并剔除；吞吐兼容 mean±SD、延迟 median/p95/p99；保留全部原始 run 不只报最优；pin host 亲和与 governor；模型/xclbin 哈希与 manifest 不符则判失败。

直接 speedup 要求：同模型与等效参数语义、同数值格式或质量对齐 frontier、同输入输出长度与 batch、同 phase/application 边界、物理硬件测量、显式 host 与功耗边界、无隐藏 fallback；否则标 `matched` / `normalized estimate` / `paper-reported context` / `not directly comparable`。下一版 backend 的 near-term 门槛：`pp512` 与 `tg128` 物理 launches 降 10x+、11-family 正确性与 strict support 无回归、host wait/sync 占比可观测下降、matched pp/tg wall-clock 提升、一次 retained 真实 prompt token/logit 对照、source-to-xclbin-to-dispatch identity。长期目标：StreamTensor/CODO 粒度的整 block/region 执行，同时保留 native GGML 语义。

## System Landscape（地图 / 可比操作点 / 瓶颈共识）

收录规则（满足其一）：真实 FPGA 上跑生成式 Transformer/LLM；同时讨论 prefill 与 decode；提供模型级 compiler/runtime；对当前 backend 的 E2E 评测或架构有直接启发。数字只表论文自身 operating point，模型/精度/板卡/batch/长度/边界不一致不算跨论文 speedup。

Timeline（角色）：FTRANS 2020 ISLPED（早期 Transformer 算术/量化协同，算子基础）；Sanger 2021 MICRO（稀疏 attention 软硬协同）；DFX 2022 MICRO（GPT-2 345M/774M/1.5B、1/2/4 U280 可编程多卡 appliance，embedding+decoder+LM head+生成控制，最强早期真 text-generation E2E 参考）；FlightLLM 2024 FPGA（OPT-6.7B、LLaMA2-7B U280，稀疏/混合精度、always-on-chip decode、长度自适应编译，完整映射流与数据中心天花板）；Spatial LLM 2024/2025 TRETS（U280 GPT-2 + LLaMA/Vicuna 解析研究，模型特异 spatial dataflow + 性能模型，最清晰 prefill-vs-decode 硬件分析）；CSTrans-OPU 2024 DAC、ChatOPU 2024 ICCAD（overlay 可编程映射/稀疏执行参考）；GLITCHES 2024 HPEC（GPU-FPGA 阶段协作）；EdgeLLM 2025 TCAS-I（GLM-6B/Qwen-7B VCU128，CPU-FPGA runtime + common layout + E2E compiler，最近的异构 cousin 但非 GGML-native）；嵌入式解码带宽 2025 DATE（LLaMA2-7B W4A16 KV260，DDR 容量带宽最大化 + fused decode datapath，有用 edge decode 基线）；BAQET 2025 FPGA（BRAM-aware 量化+流架构）；SpeedLLM 2025 HPDC（TinyLlama/Llama2 系 U280，pipeline+内存复用+算子融合，模型级 host 计时但评估细节有限）；StreamTensor 2025 MICRO（GPT-2/Qwen/Llama/Gemma U55C，Torch-MLIR 编译器 + stream tensor + block fusion + FIFO sizing，直接编译器基线与 CODO 前身）；CODO 2026 ISCA（GPT-2 Medium U280，粗/细 dataflow violation 消除 + 通信优化 + DSE，优先对照）；TeLLMe v2 2026 FPGA（BitNet 0.73B W1.58A8 KV260，三元查表 matmul + prefill/decode 分 datapath，5W 下全阶段 edge 基线）；FAST-Prefill 2026 FCCM（Llama3.2/Qwen 1-3B U280，长 context 稀疏 prefill + 两级 KV，阶段专用）；LUT-LLM 2026 FCCM（存算/LUT 计算方向）；Hummingbird+ 2026 FPGA（原型到产品化参考）。

集成抽象对照：DFX（custom GPT appliance，模型特异指令/分区，整流水跨卡，可编程 overlay + 多卡同步；真 E2E 定义与模型并行天花板）；FlightLLM（custom compiler/IR/runtime，整模型压缩编译，指令+fused dataflow，temporal 加速器 + on-chip decode；性能/能效天花板，framework-native 弱）；Spatial LLM（HLS 库+模型组合，解析式资源分配 + per-model HLS，空间流水 stage/layer，模型特异 dataflow；解释融合为何压倒孤立 kernel）；EdgeLLM（CPU-FPGA 应用/编译器，动态算子映射 + common layout，异构模型图，CPU 控制 + FPGA 加速）；StreamTensor（PyTorch/Torch-MLIR 再生每模型 fused block，整 Transformer block，block 调用 + 流式中间量；block 融合降内存/launch 的直接证据）；CODO（高级程序/Torch-MLIR，编译器修 dataflow violation + 搜并行度，大 fused dataflow 图，生成 kernel/host/link；最强 GPT-2 编译器对照）；TeLLMe（模型特异 edge 栈，三元模型 + 特异 prefill/decode，全 decoder datapath，PS+PL 且 LM head 在 PS；5W 全阶段设计示范）；当前项目（不改 `llama.cpp`/GGML 应用，support-gated onboarding，今日映射单元是 accepted GGML node、region 是未来目标，native backend + XRT；独特框架/ABI 证据，当前太细粒度）。

代表性数字（各表自身边界，不互算 speedup）：DFX（1/2/4 卡 GPT-2 345M `[64:64]` 93.10/146.25/207.56 token/s；相对同卡数 V100 平均延迟低 5.58x、吞吐高 3.78x、能效高 3.99x）；FlightLLM（U280 batch1 OPT-6.7B/LLaMA2-7B 实测，block/N:M 稀疏、平均 3.5bit 权、8bit 激活、HBM+DDR、always-on-chip decode；headline LLaMA2 端延迟优于优化 V100S、能效约 6x；要义是 decode activation 留片上、权重高效流）；Spatial LLM（U280 GPT-2 相对 DFX prefill/decode 约 2.16x/1.10x；compute 型 prefill FPGA 弱、memory 型 decode 强，选中 decode 比 A100 快 1.9x、能效高 5.69x；MAC/片上 buffer/片外带宽/空间流水平衡解析模型）；EdgeLLM（整模型跨 CPU+VCU128，common layout 避重复 reshape/transpose；GLM-6B decode 512 tokens 内 ~90 token/s，Qwen-7B 42.5-69.4 token/s；FPGA 设定平均 56.86W，headline 相对 A100 吞吐 1.91x/能效 7.55x；模型/稀疏/INT4/host 分工不同，仅上下文）；StreamTensor（U55C W4A8 GPT-2 Medium：`[32:32]` 194.99ms/TTFT34.59/199.51tok/s，`[64:64]` 358.24/61.27/215.51，`[128:128]` 696.65/125.35/224.05，`[256:256]` 1387.76/272.85/229.61；整 block 融合后每层换权重顺序调用，与当前 per-node XRT 最相关结构对照）；CODO（U280/W4A8/300MHz GPT-2 Medium decode 231.48 tok/s，TTFT 20.40/32.64/110.40ms 对 32/64/128，见正式 note）；嵌入式 KV260 LLaMA2-7B W4A16 300MHz（decode 4.9 tok/s、6.57W、约带宽导出极限 84.5%；价值在暴露简单带宽界 + 含 llama.cpp edge 对照）；TeLLMe v2（BitNet 0.73B W1.58A8 KV260 4.8W，prefill 143 tok/s、decode 25 tok/s，64-128 prompt TTFT 约 0.45-0.96s，LM head 在 ARM/PS 约 9ms 计入 E2E；异构边界声明示范）；FAST-Prefill（U280 W8A8 Llama3.2 1B/3B、Qwen2.5 1.5B 4K-128K，TTFT 约 1.5-2.5x、能效至多 4.5x vs A5000 Flex-Prefill；故意不是 decode 系统，只进阶段表不进总 token/s 排名）。

文献对当前瓶颈的三线共识：整 block 融合salient（Spatial/StreamTensor/CODO 把中间量留片上、摊销编排）；launch 开销受控后 decode 是带宽问题（FlightLLM/EdgeLLM/KV260 强调权重布局、有效带宽与持久状态）；prefill/decode 应分 datapath 或调度（Spatial/GLITCHES/TeLLMe/FAST-Prefill 把不对称当架构აცემ而非参数）。当前 backend 尚未进入第二区间，因为 launch/wait 膨胀先于 HBM 带宽成为干净 bound。

2026-07-28 架构刷新（只收窄结论，不改测量 caveat）：MPK（persistent mega-kernel 调度，破 kernel-per-op 边界的具体办法；不给 FPGA/HBM 放置、GGML 语义或 XRT 失败行为）；Nyx（跨 region 时空共享 + 依赖感知虚拟 FIFO；不给 LLM 算术或框架原生 backend）；FlightOPU（HBM-channel-affine overlay 放置 + 多 die 布线；不给不变 llama.cpp/GGML 边界）；RISCBench（调度/同步/residency 的控制面测量透镜；不给已验证 LLM 加速机制）；CGRA space-time mapping（时间调度与空间放置形式分离；不断言 temporal reuse 自足）；FESTAL（基于图的融合编译对照；不给 strict zero-fallback 安全契约）。更新后结论：要的是 **contract-preserving coarse execution boundary + 显式 HBM residency rule**，不是普通算子融合、通用 overlay 或新静态空间加速器；首个已审计候选 VSTC 保留原始 GGML 调用身份与显式错误行为、只准入完全可观测单消费者 device-only 调用进精确流模板，测到 U280 对照前仍是提案。

阅读序：DFX（完整 GPT text-generation 加速的严格定义）→ FlightLLM（现代 7B 整模型映射流）→ Spatial LLM（prefill/decode 解析模型）→ StreamTensor（整 block 编译融合 + FIFO sizing）→ CODO（violation 消除 + 通信优化 + GPT 板级指标）→ EdgeLLM（CPU-FPGA 编译/runtime 边界对照）→ TeLLMe/FAST-Prefill（edge 与阶段专用端点）。

## Execution Taxonomy（词表 / 定位 / HBM 覆盖）

`shared engine`、`temporal reuse`、`overlay`、`streaming dataflow`、`spatial accelerator` 不可混用。实问是：依赖在哪物化、谁调度下一单元、token 前进前要几个 host 可见 completion。

| Term | Defining property | Does not imply |
|---|---|---|
| Shared-engine temporal reuse | 同一物理算力在不同时间执行不同算子/tile | 可编程、流式或 launch 高效 |
| Overlay / CGRA | 可编程指令/数据通路基底服务多算子 | 张量全流式，或硬件按层空间独占 |
| Streaming dataflow | 生产者以 fragment 经 FIFO/通道发消费者，不等整 tensor 物化 | 用 CGRA 或支持任意算子 |
| Spatial mapping | 算子/层静态 pin 到不同硬件区并发 | 资源复用或运行时可编程 |
| Coarse-grained execution | host/框架只见 region/block/命令流，不见每 tile/算子 | region 语义安全或免数据搬运 |

双轴：placement（temporal reuse vs spatial reservation）× 实现（custom RTL vs programmable fabric），streaming 是可跨两列的第三属性（生产消费经片上通道交 fragment 而非整张量 host 可见物化）。代表性放置：Vitis AI DPU v3.5（异构引擎间 temporal reuse，目标特异 ISA+XIR+VART；产业可编程引擎先例，查 CPU 分区）；FINN（层间 spatial dataflow + 层内 temporal folding，QONNX→HLS/RTL，FIFO/DMA/参数 memory modes；空间与时间复用可共存的证明）；Spatial LLM（主导 spatial，模型特异 HLS 组合）；FlightLLM（temporal + multi-CU 混合）；MCore-OPU/FlightOPU（overlay core 间 temporal reuse，同步路由 + HBM-channel 亲和）；Nyx（跨 region 时空共享 + hypervisor + 虚拟 FIFO）；StreamTensor/CODO（生成式 dataflow 图，编译器 IR + DSE，Transformer block/graph 粒度）；MPK（持久 GPU kernel 内 temporal reuse，编译器生成核内调度；最强 launch 边界对照，非 FPGA）；CGRA space-time mapping（先调度后放置的编译词表）。

历史 `/home/zdpeng/llama.v` 是 **custom token-oriented CPU+FPGA 系统**（host 命令 ABI、HBM 常驻权重/KV、推理控制器、专用数学块），属 **custom RTL + temporal reuse** 格：token 级控制器随时间复用功能单元；ABI 非通用指令集/CGRA 编译目标故非 overlay；未给每层独占流水故非完全空间加速器；HBM 常驻与内部 handoff 兼容流技术，但流必须在显式生产消费边界证明。Active 远端 `ggml-fpga@402214ed` 是另一形状：native GGML support gate + 分立算子 RTL 核（`mul_mat`、`rms_norm`、`rope`、`softmax`、`glu` 等）经 XRT 驱动，映射单元是 accepted GGML node 且常一 node 多 launches，故为 **framework-native temporal dispatch**，尚非持久共享引擎或 fused 流图——与 `pp512`/`tg128` launch/wait 画像一致。两者共享约束：valid 机制不得以静默回 CPU、发布失败 device 结果或加载未验证 artifact 换性能。

HBM-aware decode 是独立覆盖层，机制必须声明：哪些权重/KV 页/中间 fragment/命令 buffer 常驻哪些 bank；消费者经片上通道、HBM 写读还是 host 同步见到生产者结果；batch 1 decode 的 bank/channel 争用模型；region 在哪条边界向不变 GGML 图发布结果。FlightOPU 给通道亲和 overlay 放置，FMC-LLM/CD-LLM 给高 batch 存算解码，H2-LLM 给低 batch 数据中心 DSE——均为设计参考，非当前 strict GGML 边界的 drop-in。

Idea 交集（窄）：native GGML support/failure/artifact contract ＋ coarse host-visible region 或持久命令流 ＋ 显式 U280 HBM residency/bank-affinity 规则 ＋ 一个可测低 batch pp/decode 下游指标。排除：从零通用空间加速器、通用 overlay 主张、无独立控制面/residency 机制的普通融合包装。实验必须把 decomposition、HBM/residency 规则、shared-engine 调度三者相对 strict per-node baseline 分开测。

## Toolchain Note（DPU / FINN / PYNQ / PINN 消歧，2026-09-07 核对）

回应“DPU 和 pinn 是否相关”：`pinn` 未确认，FINN 与 PYNQ 都是合理候选，字面 PINN 另属一类，此处分开登记。Vitis/Vitis HLS 是开发综合集成工具（用 Vitis ≠ 用 DPU）；Vitis AI 是量化编译IP运行示例工具链（本页核 v3.5 DPU 路线）；DPU（Deep Learning Processing Unit）是目标相关 ISA 推理引擎（shared-engine/可编程 overlay 产业参考）；FINN 是 AMD Research 量化网络 FPGA 编译框架（给网络生成定制 streaming dataflow，空间映射+层内时间复用参考）；PYNQ 是 Python 驱动+硬件 overlay+板卡软件生态（可控 DPU 也可控 FINN 生成硬件，自身不定义神经网络计算架构）；PINN/PINNs 是物理信息神经网络（JCP 2019，模型/科学计算方法，不能望文生义成 FPGA LLM 编译框架）。

DPU（v3.5 文档）：带自身 ISA 的微码机，内含异构 engines；兼容网络换模型≈换编译程序+权重，无需每网重出 bitstream，但这是受算子/形状/ISA 约束的可编程性，不意味任意 GGML 可跑。`训练模型 → 量化 → arch.json + Compiler → XIR 图划分 + DPU 指令 → .xmodel → VART 提交完成 → 已集成 DPU 平台`。工程事实：编译目标是契约（`arch.json` 不匹配即运行时错）；量化器能力≠DPU 能力（通用 CNN DPU 路线主 INT8，量化工具列 FP16/BFP/matmul 不能单独证明 IP 支持）；图划分必须可见（Inspector 查算子排列，WeGO/ONNX-RT 可划 CPU，strict GGML 项目必须审计原接受算子是否仍在 device、未支持部分如何处理）；VART 异步是参考，高层作业对底层提交数仍需实测；开源边界逐组件核（编译器无源码，仓库 Apache-2.0 ≠ 全工具链/IP 可改）。目标板边界：DPUCZDX8G 是 Zynq MPSoC/Kria K26 PL IP（KV260/ZCU104 教程非 U280 包）；DPUCV2DX8G 面向 Versal AI-ML tiles（VEK280 等，`VEK280` ≠ `Alveo U280`）；v3.5 按 IP 核工具版本（release notes 给 2023.1 兼容，部分成熟 IP 无更新参考设计）。以上**未建立 U280 Gemma 3 1B/GGML 现成完整部署证据**（证据限制，非“不支持”断言；只谈 v3.5 文档，不代表 2026 AMD 全产品线）。

FINN：实验性框架，`Brevitas 量化 → QONNX → FINN-ONNX → streamlining/HW层转换/dataflow partition → HLS/RTL + PE/SIMD folding → DMA/位宽转换/FIFO/IP 拼接 → bitstream + 生成驱动 → 板卡`。对 taxonomy 的价值是层间空间+Folding 层内时间可共存。QONNX/FINN-ONNX 串量化语义硬件转换模型验证（ONNX 输入≠任意 Transformer 可编）；PE/SIMD folding 换资源吞吐平衡流水（prefill/decode 最优可能不同）；FIFO/DWC/DMA 显式建模流连接位宽外存入口（动态序列/KV/GGML 可观察边界仍需设计）；参数 memory modes 分内嵌常量/独立权重流/external 参数流（external 标 experimental/limited，不自动给 U280 HBM bank 分配与 LLM 权重管理）。易误读：ONNX 任意模型直转不支持（FAQ 明示，缺层自补，HLS/RTL 层与目标限制以文档为准）；位宽无统一上限（FAQ 并存“高位宽大网资源贵”与 1-8bit 建议，按层/backend/器件/综合核）；网络定制≠权重永固（`internal_embedded` 常量综合、`internal_decoupled` 存算分离、`external` 运行时参数但受限）；示例支持≠编译器可移植（`finn-examples` 预构建 Alveo 为 U250 + Zynq 示例，生成 IP 可集成他板，但本轮无 U280 实测、无完整 Gemma 自回归验证）。基础论文入口（本轮未全文深读，题录经官方 README/publication list 核）：FINN FPGA2017（1612.07119）、FINN-R TRETS2018（1809.04570）。

PYNQ/PINN：PYNQ 是部署生态（FINN 可生 PYNQ driver，DPU-PYNQ 给 `.bit/.hwh/.xclbin` + notebook；文档 overlay 常指可加载硬件包≠架构论文可编程 overlay processor）；DPU-PYNQ 是历史参考（2026-09-07 官方 README 已归档、`archived=true`，对应 PYNQ 3.0 + Vitis AI 2.5.0，不可套 3.5/U280）；PINN 是模型方法（Raissi 仓库 PDEs，另需按具体 FPGA PINN 工作核边界，本轮未确认特定工作，不入 LLM 性能表）。

对主线启发（分析非新测量）：DPU 作共享引擎先例（“一份硬件跑多份编译程序”成熟，未来贡献须在 GGML contract/可观察边界/HBM residency 上讲增量，不以 shared engine 命名为创新）；FINN 作流式构建验证参考（先读 folding/FIFO/参数流/生成驱动如何支撑 coarse execution，比直导 Gemma F16 更对 launch/wait 瓶颈）；先建覆盖矩阵再谈替换（逐项查 `MUL_MAT`/RMSNorm/RoPE/softmax/GLU/KV/dtype/shape，记编译分区/CPU 部分/artifact identity）；统一测量边界（后做原型分记编译-bitstream/packing-DMA/设备计算/host wait/完整 pp-tg，不拿 CNN samples/s 当 LLM token/s）。阅读序：DPU 架构编译 S1-S2 → FINN 准备构建 memory modes S7-S9 → VART/PYNQ 部署 S3/S10-S11 → 两 FINN 基础论文。一手资料（2026-09-07，搜索两次 503 后直读官方 raw + API；FINN `main@38c42bf`  pin 版）：S1 DPU IP 与系统集成、S2 模型开发（Inspector/INT8/XIR/arch.json/CPU 分区/编译器源码界）、S3 模型部署（VART 异步/XRT/整应用边界）、S4 v3.5 release notes + 版本兼容、S5 FINN README、S6 Brevitas 导出、S7 网络准备、S8 硬件构建部署、S9 memory modes、S10 finn-examples、S11 PYNQ + DPU-PYNQ、S12 FINN FAQ、S13 PINNs 作者仓、S14 FINN publications。未下载验证 bitstream，未装工具链，无板卡实验。

## Literature Provenance（两次检索 + 底表）

07-22 宽检索（2018-2026；初轮 Crossref 80→76 多假阳性，二轮 exact-title+DOI+arXiv 全文+私稿引用补齐）：connector 多故障（DBLP 宽查询 0 中、exact-title 找回 DFX/FlightLLM/EdgeLLM/StreamTensor/TeLLMe 等；arXiv 429/503 后直下已知 ID；OpenAlex 401、OpenReview 凭证/429、Sematicscholar 403 均未用于事实主张；07-23 五查询 rerun Crossref 125 + DBLP 8 同样失败模式）。核心 16（FTRANS/Sanger/DFX/FlightLLM/Spatial/GLITCHES/EdgeLLM/嵌入式LLaMA2/BAQET/SpeedLLM/StreamTensor/CODO/TeLLMe/FAST-Prefill/LUT-LLM/Hummingbird+）+ 扩展 27（起止 IJCNN 可扩展 GPT-2 经 HLSTransform/LlamaF/InTRRA/METAL/LoopLynx/MEADOW/TerEffic/LightMamba/AccLLM/QLlama/MoE-OPU/ISOCC LLM/CXL-SpecKV/整数全融合/FlexLLM/LORA/TeraFly/TFLOP/dLLM-OPU/SkipOPU/XtraMAC/ELiTeFormer 等，至 IROS 机器人部署）。趋势：20-22 算子到整机（FTRANS/Sanger→DFX）、23-24 映射流与空间-overlay 之争（FlightLLM/Spatial）、25 编译运行时与部署多样（EdgeLLM/StreamTensor/edge decode/BAQET/SpeedLLM）、26 粗粒度自动化与阶段专用（CODO/TeLLMe/FAST-Prefill）；优化单元在变大，孤立算子速只算支撑证据。07-24 pass 缓存 48 标题验证 PDF，20 无验证公开版记 metadata-only；本地读过 arXiv `2209.10797/2312.15159/2401.03868/2407.21325/2502.10659/2507.14139/2509.13694/2510.15926/2602.20515/2604.12618`；CODO artifact 看官方 `130b12bc` + `isca2026-ae` + Zenodo，未下 6.2GB Docker 层。

07-28 窄刷新（launch/wait 放大下 U280 GGML 契约路径有何可用文献；六查询无过滤 241→142：arXiv60/OpenAlex60（504 重试5次后恢复）/Crossref60/Semantic1（5限流）/DBLP0（超时TLS）/OpenReview0；39 跨源合并；高召回故 `fusion/HBM/coarse` 词面噪声多，2020-23 只作锚不再重搜）：准入六类（shared/temporal 控制面、spatial-overlay-streaming-graph、HBM-aware 低 batch decode、异构框架边界、coarse/persistent/融合、overlay-CGRA 编译映射），DOI/arXiv/归一标题/slug 对 68 去重后新增 15 条 `papers/` 记录，仅 MPK + CGRA space-time 过全文 PDF 门（签名/可解析/标题/≥2页），余 13 记 metadata-only（RISCBench 公开文件仅1页摘要拒收，403 页不缓存）。新增：MPK（持久 mega-kernel + 核内任务 runtime，GPU 但最清 launch 边界对照，PDF）、CD-LLM（高 batch 多卡 decode，HBM master + 计算从）、FlightOPU（HBM 通道亲和 overlay + 多 die）、Nyx（共享 FPGA 时空虚拟 + 虚拟 FIFO）、PCIe 粗 systolic（直连 PCIe-FPGA 大 PE）、RISCBench（编排/residency 测量词表，1页拒收）、H2-LLM（低 batch 数据中心 DSE）、MCore-OPU（temporal overlay + 降核间同步）、Streaming VPE（流式非线性 + 前瞻归约）、DTCore（编译器极简控制引擎，题录种子）、FESTAL（图融合编译对照，题录种子）、FMC-LLM（高 batch 存算流解码，CD-LLM 谱系）、统一 overlay 编译器（E2E overlay 编译对照）、Lembda（CPU-FPGA 协同锚，待全文验证）、CGRA space-time（时空调度与空间放置分离，PDF）。四综合：空间/overlay/流不可混；共享引擎先控后算（MPK/Nyx/RISCBench/DTCore/粗 systolic 皆指调度launch residency 为一阶对象，与 U280 host wait 主导对齐）；decode 按 batch 分治（FMC/CD 高 batch 70B+ vs FlightOPU/H2 低 batch，皆不证 strict GGML 准入/artifact/zero-fallback）；缺失交集是带框架语义的粗粒度机制（fusion/dataflow 论文自有编译边界，当前 backend 自有原生边界但 node/tile 粒度，贡献须连两者而非把普通 fused region 当新）。未过滤 142 行全表（`allinone.md`）与本轮 connector 错误、关键词计数、引用统计、阅读路径已随删除归档 git 历史，策展子集与 PDF 来源见下文 §Paper Library。

历史快照（06-17，已 stale，被本页 + 评测协议取代）：当时 `/home/zdpeng/llama.v` 是 CPU+FPGA 混合（`rtl/compute` matvec/rmsnorm/rope/geglu/softmax/dequant、`rtl/memory` hbm/loader/kv、`rtl/top` kernel/inference_ctrl/config/cmd、`host` main/xrt/gguf/contracts、`tools` Gemma布局trace打包、`scripts` 构建综合；README 定 CPU 留 tokenizer/GGUF/EOG/detokenize/sampler/控制、FPGA 做 HBM token 热路径；短 context Gemma 3 1B F16 U280 bring-up；token AXI-Lite ABI 回 greedy token ID）；llama.cpp 侧已有 `ggml-backend.h` + `ggml-backend-impl.h` + `ggml/src/ggml-*` + `ggml_add_backend` + device 能力（async/host buffer/event/supports_op 等），FPGA 可做普通 `ggml-fpga` backend 或高层 token 引擎；上游扫描（XDNA `#21725`、tilelang `#23219`、ANE `#10453`、ET `#24179` 及 backend 基建）判上游接受新 backend 但要可维护测试CI；当时定两条路（`llama.v` bring-up + 窄 XRT backend 切入）与分阶段收敛（单机 bring-up → 稳定 ABI + oracle → 最小 `ggml-fpga` 原型 → 单 op 小 PR），现行结论以 taxonomy + 项目基线为准。

## Idea History（失败审计 + VSTC 提案，均可证伪）

总判（07-24）：已立住 native GGML integration、strict no-fallback、evidence closure、artifact identity；未立住加速与 load-bearing 机制；不以 general high-performance backbone 投稿。首轮 `idea-spark`（`threads/ideaspark_run/towards-general-fpga-backbone/`，终态 `phase_3_failed.md`）无 reviewer-defensible 卡，死因非 scoop 而是两候选连过 coherence + novelty/recipe + falsification。Phase 1 瓶颈命题成立：单点合法准入可组合成全局病态 launch/wait 放大；未解的是保 support/显式失败/tensor state/artifact/zero-fallback 下压放大。注册/support/ABI/收据/多算子替换是必要基础非性能机制。Phase 0 只召回 10 frontier（多 `backend` 噪声）另注 DFX/FlightLLM/Spatial/EdgeLLM/StreamTensor/CODO/TeLLMe/FAST-Prefill/FlexLLM user anchors + 公开全文；collision 98 hits 无直接 subsume RegionSeal，但只支“未见直接 collision”不支“已证 novel”。

Attempt 1 Receipt-Carried Epochs（vector-descriptor 包 + 异步 graph epoch + tensor version + COW KV，把每 accepted call 内 launches 压成一次、host wait 推迟到 graph 边）：死于 device 依赖/alias MVCC coherence——host `start()` 序非 XRT completion 依赖（producer fault 致 dependent 永久等，first-error epoch commit 完不成）；Tensor ID ≠ canonical storage alias（无 allocation/range/view 关系 KV COW 读 stale/等错 version）；补 device dependency/abort 传播/memory ordering/alias-safe MVCC/11 vector wrappers 已超五月可信 scope，且 novelty 易被读作 command batching + transaction 包装。

Attempt 2 RegionSeal（同步纯区：per-node strict → canonical range/effect → 单 exact recurring region → 单 terminating U280 artifact → 单同步 wait → 成功才 residency 发布 → 余 node 走 strict；禁 KV mutation/in-place/外部 alias/host 可见 state，只要单 unaliased terminal output；可用 backend `2616bb6` 的 `mirrors`/`residency_store`/`get_input`/`wait_for_run` timeout-abort 发布 graph-local mirror，失败不发布、abort 存疑则 quarantine + 禁 backend）：仍非 paper idea——novelty residue 弱（alias/effect/subgraph fusion/delegate/residency 皆现成件，digest seal 易读成普通 effect-aware fusion 包装）；为过 C13 补 relation-typed effect 图 + 不动点 RTECC certificate，仍须证相对普通 checker 不可替代；falsification 不可执行（pre-synthesis `C_R` 测不出未建 region 真实 launch/wait；decomposition/RTECC/ordinary fused controls 不正交；30-pair bootstrap 不完备证 effect lower bound >10%）。

Go/No-Go 原型（先 calibrated region shell，不直上整 block 编译器/持久 runtime）：Stage A 找长 2-6 recurring 连续 region（全 strict 通过、F16 精确匹配、无 KV/in-place/外部 state、canonical 无 outside alias、单 terminal、同 XRT memory group 下游、不重叠不重复计数；无则停）；Stage B 建同 BO 数/group/ABI/status/residency 路径 terminating shell，测 seal/RTECC 分析、`run.start` host、`wait` host-device event、mirror 发布、manifest 失配/失败路径；当前 per-node waits 减 shell 只算可移除控制时间上界，不猜 region 延迟；Stage C 冻五臂（strict 基线/certificate-only/ordinary effect-aware/RegionSeal/manifest-disabled，同 R* artifact 输入输出时钟，RTECC-off 不得换数据集挑 fixture）；Stage D 预注册统计（主估计 paired `d_i`、pairing/warmup/随机-block/thermal、样本量有据、bootstrap unit/count/seed/区间、`pp512`/`tg128` 多重校正、adjusted one-sided lower bound `>0.10` 硬门 + 正确/strict/artifact/zero-fallback/fault 全硬门）。停止任一即停 RegionSeal 主线：无 eligible region、shell headroom 不支 10%、mirror 消费失败、F16/token/support/artifact/fallback 回归、RTECC 等价普通 baseline、full artifact 只改善 region event 不改善 downstream wall clock。发表阶梯：现有证据只到工程报告/artifact-demo/workshop（不称加速）；shell 只算内部 go/no-go；单 R* 过正确 + >10% 下界才算 scoped Gemma F16/U280 系统结果；RTECC 在真实安全/执行性质胜普通 baseline 才谈机制贡献；第二模型 + 最好第二 FPGA 系才重议 general backbone。若 RegionSeal 死但 admission-to-launch 放大多模型多配置可复现，可另议窄 characterization（如框架原生 FPGA LLM backend 的 granularity gap），仍需新样本。

VSTC（07-28 新 run `threads/ideaspark_run/shared-engine-llama-fpga/`，`DONE` 5 pass/0 warn/0 fail；提案非性能断言）：问题是 U280 共享时分引擎如何在保原生执行/显式失败/artifact/zero-fallback 下跑 contract-closed coarse HBM-aware GGML region（锚 pp512 1626→224936、tg128 104877→202530，host wait 先于算术/HBM 界）。机制：每原始 support GGML call 膨胀成 XRT 提交前先发 ticket（算子/布局、可 patch 标量、逻辑分配字节跨度、生产 ticket、全捕获后 reader/consumer、scratch、host 观察/alias/state 旗）；到声明 closed GGML 边才准入；除“后 reader 全捕获、无 host 观察/状态 barrier/状态写/逃逸 alias、恰单 ticket 感知消费者、有精确 F16 已装 kernel、独占 scratch lease 活到消费完成事件”全满足进 B，其余进受保护 H；最大 eligible B 成常驻共享引擎可 patch 精确模板，H 留单 descriptor + 原生分配物化 + 每逻辑调用 completion-ring 槽；无 CPU fallback。HBM-aware 经 scratch 字节需求 + lease 寿命体现，不空称新 HBM 布局；load-bearing 量是 `rho`（同 closed trace 基线 XRT 提交中 B 模板代表比例）。近工作差：Big PE（8bit systolic 算子放大 TinyStories prompt；VSTC 不动 F16 数据面改原生控制面，跨 prefill+decode）、LlamaF（静态 W8A8 矩阵拼接 + PS 留 attention/KV；VSTC 动态捕获 live host-read/alias/state/分配/consumer/scratch/显式错误再准入精确模板）、CDA-GNN（最近 collision：U280 编译器定链跑 GNN；VSTC 差在动态 per-call 观测 + 失败保留非调度本身）；剩余 prior-art 条件：须 targeted scoop 查动态 CUDA Graphs/runtime command buffer/XRT command-buffer 调度是否已保同样完整原生语义准入契约，否则不存活。最小伪证：同内核输入跑原生 per-XRT vs naive 常驻 descriptor vs VSTC（pp512/tg128 固定 512-token wikitext-2-raw-v1），要 bytewise logits + 有序显式错误 trace 与原生一致；VSTC 成立则延迟与实际 XRT 提交随 `rho>0` 同向降；全观测 oracle 每 call 后验张量以分清捕获错 vs 模板错。负对照/停止：B-admission-off（同核同输入同引擎ticket环只关 B）p50/p95 不向 naive 基线回归则 visibility claim 伪；同质全 eligible 切片比单/多 record 解释器、混合 trace 只拨 B 开关以分离解释器与 H/B 效应；无 B 人口/`rho=0`/scratch 租不到/后 reader-alias-state 捕获不住则停（不把普通常驻引擎改名 VSTC）；bytewise/显式错误不一致、强制 B-denial 不回归、CPU fallback/artifact break/等价原生语义准入协议出现即停 claim。卡证链（新径）：`threads/ideaspark_run/shared-engine-llama-fpga/phase3_revise/final_candidate.json`、`phase3_collision/collision_hits.json`、`phase3_critique/phase3_critique_output.json` + `phase3_revise/phase3_revise_output.json`、`phase3_critique/falsification_reaudit.json`、`phase4/idea.std.zh.md` + `idea.std.en.md` + `idea.detail.en.md`、`phase4/phase4_implementability.json`。

近期优先级：按评测协议冻边界/trace schema/每原始 GGML 调用基线 XRT 提交数；pp512/tg128 先观测 VSTC H/B 分布/`rho`/拒绝原因/scratch 压（无 B 人口或 `rho=0` 即停机制）；实现 H descriptor + B 模板 + per-call completion ring + scratch lease 最小控制面（漏 reader/alias-state/强制分配失败/engine failure 必回原始调用显式错误，禁 CPU fallback）；同核同输入三对照（native per-XRT、naive 常驻、VSTC）再分 homogeneous 单-多 record 与 mixed-trace B-off 查独立贡献；bytewise/显式错误不一致或 forced-B-denial 不回归即停；控制面压低后再议 Q4/W4A8、HBM 布局与 kernel 微架构。

## Roadmap（P0–P5）

- P0 冻语义：留 pp/tg 为集成基线，另加 text-in/out 请求计时、device 时间戳、功耗、logits/token 正确性、cold/warm 界。
- P1 收命令粒度：持久命令处理器/命令 buffer，内部 tile 不 host wait，每 accepted region 回一次，launch 预算先 O(layers)/token 再 O(1)，非 O(tensor tiles)。
- P2 保契约 region 融合：探 producer/consumer 闭合 GGML 序列，先 norm→投影→RoPE/attention→残差等 block 片段，定 region ABI + shape/type 门 + 整 region CPU oracle；未融合算子在 strict 外显式处理，永不隐藏。
- P3 常驻异步：权重/KV 常驻声明 HBM bank，消重复分配 packing，H2D/计算/D2H 事件队列（依赖允许才 overlap），加 trace monitor 分 device active 与 host wait。
- P4 竞争数值：F16 bring-up → GGUF 兼容 Q4_0 或文档清 W4A8，算 scale/zero decode 与输出质量，对比量化前后带宽利用。
- P5 可移植与 paper 闭环：第二 llama.cpp 模型/系，一 ABI 兼容 kernel/region 替换 + matched E2E 变化，测功耗、energy/token 与 pin 住的模型质量 metric。

可辩护 position（现在）：原生 strict evidence-closed `llama.cpp` 内 FPGA 执行边界 + 真 Gemma 图覆盖 + 可替换算子实现。不可称：FPGA 加速 CPU/GPU、持平 CODO/FlightLLM/StreamTensor、通用高性能 LLM bitstream、生成 RTL 改善 E2E。最强下一篇是单 contract-closed fused region 实降 launch + 实改善请求级指标且 strict 证据不弱。

## Claim Discipline

- `csynth` 或 RTL simulation cycles 不是 board latency。
- positive WNS 不是实测频率。
- operator speedup 不是 token speedup。
- FPGA 文件存在不代表实际 dispatch；必须有执行收据。
- `llama-bench pp/tg` 是 model-phase benchmark，不自动等价于包含 tokenizer/sampler 的 application end-to-end。
- 不同模型、precision、card、batch、prompt/output length 和测量边界下的 token/s 只能做背景定位，不能做加速比。

## Evidence Matrix (New-model entry + Resident exec., folded 2026-09-09)

表头与 paper Table 1 同文：`Work | Model source/interface | New-model entry | Auto map | Native backend | E2E gen. | Resident exec. | Public source | Scope/qualification`。`—` = 未确立（partial/absent/unreported），不是“不行”；✓ 不意味独立复现。

- New-model entry：第三方不经作者侧 case 生成、用模型文件 + 常规配置部署下一个受支持 checkpoint；多模型数、预编译 case 集、纯词表 GGUF 不算。自动打包/bitstream 重建允许。
- Auto map：编译器/runtime 把已接收模型/图降为指令/分派算子/硬件；手拼模型硬件不算，且不自动确立新模型入口。
- Native backend：经已有推理框架 backend 接口执行；仅借 tokenizer/导 PyTorch 不算。
- E2E gen.：真实 checkpoint + prompt、完整模型含 LM head 与历史上下文、逐 token 选择反馈、可观测输出；单层/单图事件、合成 tensor、阶段计时拼凑不算。
- Resident exec.：权重/KV 在请求生命周期驻留 device，中间量不逐算子回 host（如驻留 HBM 窗口 + 片上复用 + 单次 graph launch）；逐算子 offload + host staging 即使有 E2E 也不算。
- Public source：加速路径实现源码；仅 binary/profiling/承诺不算。

行判（paper-report 级除非另注）：DFX（E2E ✓ Resident ✓，整服务单 launch 下 HBM 分片权重/KV；新模型入口 —，无公开实现）；FlightLLM（Auto ✓ E2E ✓ Resident ✓，HBM 权重/KV + always-on-chip decode；新模型入口 —，预编译 case 需作者协助，RTL withheld）；EdgeLLM（Auto ✓ E2E ✓ Resident ✓，HBM 权重/KV，host 只写配置；custom runtime，无公开源码）；Spatial（Auto — E2E —，phase 证据；Allo kernels/layers 源码 ✓）；StreamTensor（Auto ✓ E2E —；文档公开，repo 404）；CODO（Auto ✓ E2E —，单固定 block，无历史 attention/LM head；源码 ✓）；FlexLLM（E2E ✓；host 侧 KV 拷贝 + prompt embedding，GGUF 仅词表；Auto —；源码 + binary ✓）；TeLLMe（E2E ✓，含约 9ms ARM LM head；host 驱动 decode_step + host 侧 KV；源码 + binary ✓）；LUT-LLM（E2E —，block-cycle 推导非实测；源码 + binary ✓）；SECDA（New-model ✓ Auto ✓ Native ✓ E2E ✓ Resident —，逐算子 MatMul offload + host buffers，KV host-managed；源码 ✓；集成先例，不做主性能基线）；本地 current（Native ✓ E2E ✓ Resident ✓，HBM 权重/KV + 单次 launch；正确性/完整验收 false；公开性 NR）；plan 行六项全 ✓（设计要求）。

Residency 单列是 prior art（DFX/FlightLLM/EdgeLLM 均有）；contribution 是 resident + 框架原生入口 + 第三方新模型部署的组合。归档包 hash 总账（16 条 repo tarball/源包字节数 + SHA-256）已于 2026-09-09 删除（当时的 `papers/checksums.sha256` 只覆盖 PDF；保留的历史清单现位于 [threads/paper-library/checksums.sha256](threads/paper-library/checksums.sha256)；包实体与总账全文见 git 历史）。

## Niche and Baseline Audit (folded 2026-09-09)

判：原生 llama.cpp FPGA backend 不是首创（SECDA 是文档化集成先例），也不等价于成熟替代（当前 whole-model/HBM-state 路径）；商用 serving（Positron Atlas、Achronix VectorPath）只在应用/API 层可替代，不提供可审查 GGML backend。可辩护机会 = 可用、可改、可复现的框架集成执行路径；等价物不存在 ≠ 唯一。

历史准入（已被下方 2026-09-15 paper-only 规则覆盖；仅保留旧审计背景）：实质论文评测数据，或可承担复现的公开实现，或经核实的顶会发表；发表与公开是独立轴。本轮九系凭评测数据入表（CODO venue 经 ISCA 官网补核；FlexLLM 维持 preprint）；无任何对手的独立板级复现。

替代关系：llama.cpp 内加 FPGA 算子卸载 → SECDA（直接部分替代，边界不同）；标准 API 跑 FPGA 服务 → Positron/Achronix（应用层替代；Positron fork `a1cfb64` 未见 FPGA backend；Achronix 为 request 制评估，无匿名可下载 GGML backend）；改/学完整公开生成实现 → FlexLLM/TeLLMe（路径定制）；GPT-2 dataflow/编译器性能 → DFX/Spatial/StreamTensor/CODO（须先对齐边界）；现有 GGUF + 可审查硬件 → 本轮有限搜索内无等价 drop-in（自家包也不达标）；本地高效跑 LLM → llama.cpp CPU/CUDA 等（非 FPGA 基线但是真替代）。

本地边界（Q4）：GPT-2 Medium/24 层/1024/单序列/≤1024/F16 KV；单 active context + known-idle clear；logits 发布后 P 推进；HBM 权重/KV + 单 XRT run + accepted 路径无 CPU fallback（采样仍在 host）；frozen receipt 保留 32 输出但 correctness/qualification/delivery 三门 false；origin 404 ≠ 已删，公开性 NR。

公开性五条（第三方视角）：拿得到源码（含 runtime/硬件）→ 拿得到镜像/模型身份/依赖命令 → 能跑多 token 并对 CPU oracle → 能改模型/profile 并重建（除声明 vendor 工具无隐藏依赖）→ 能在声明板上复现数字。binary/demo/纯编译器/API 服务各给子集，不共享一勾。artifact 可用性的关键对照是 FlexLLM/TeLLMe；机制隔离建议 SECDA-style MatMul-only vs 全 device-state 同板同模型对照。

发现口径（raw 抓包已删，全文见 git 历史）：GitHub `llama.cpp FPGA` / `ggml FPGA` / `FPGA backend llama.cpp in:readme` 返回 3/1/142 hits（宽查询只筛前 50；精确查询连 SECDA 都搜不出，缺席证明力弱）；上游 `upstream/master bae36e` 注册表与官方 backend-registry API 回包无具名 FPGA backend（非穷举）；CORDIC-softmax（CPU 完、集成中）、WPU（RTL/fit 自称之外无硬件吞吐）、Vysh（继承 llama.cpp 文本）只记为 leads，未立基线。

## Manuscript Recheck 2026-09-08 (folded 2026-09-09)

方法：64 引用 inventory + 10 系原实验节/公开执行路径复核；primary 证据优先于后发 paper 对比表；integration overlap ≠ 等价实现。

DFX（1/2/4-U280 + 长度 sweep；精度只在 345M；1.5B 改 head 数；不引申多系可移植/公开实现）。FlightLLM（U280 实测 vs VHK158 仿真分开；profiler/binary case + withheld RTL ≠ 可编辑完整 release）。Spatial（实测 BERT/GPT-2：GPT-2 W8A8 vs BERT W4A8，别从后发表抄 W4A8 给 GPT-2；大系/多卡 projected；Allo PLDI artifact 有 GPT-layer HLS + host 但 host 计 1 次 + 24 层重复、无 prompt/sampling/回授、无数值比对，不是 Spatial 论文 exact artifact）。EdgeLLM（VCU128 GLM/Qwen + LAN service + 稀疏/质量；custom runtime ≠ GGML backend；源码未确立）。StreamTensor（U55C 板上实测 + 改写 HF 图 + block 复用；完整 token 反馈控制器/KV append-read 未确立；文档公开，repo 404；Llama 精确 checkpoint 存疑，不影响短名单）。CODO（合成/板/编译器结果实质；host 计单 event、无输出回读、无条件 TEST PASSED；随机输入验证 block ≠ checkpoint 驱动生成器）。FlexLLM（终态 W4A4KV8 + 量化 LM head，PPL 12.68 vs BF16 8.94；U280 实测、V80 projected；`make demo-run` 是应用入口，仍需依赖/预备权重）。LUT-LLM（Qwen3-1.7B 质量 + V80 硬件实证；AE 系推导非 token 计时；别把每行数当同一 provenance）。TeLLMe（KV260 E2E 用 PYNQ 计时，breakdown 用 RTL 仿真，约 9ms ARM LM head 计入；chatbot 需外部数据 + CPU 构建）。SECDA（1.7 s/token、约 11x A9 NEON；workload/phase/质量/功耗细节缺；后期 WiP 码 selective MatMul + host buffers，未构建运行；preliminary 集成先例，不做主基线）。

纠正：CODO venue = ISCA 2026（官网 program + arXiv 记录；无 publisher DOI/页码不猜）；FlexLLM 无 venue 不推断；SECDA 维持 2024 preprint。TeLLMe 对比表把 SECDA 标 A53/W4-A16 是二手误差，以原文 A9 + Q3_K/Q8_K 为准。

本地含义：Q4 单图/调用 + HBM 权重/KV + GPT-2/单序列/≤1024 + 预备 image/package + FPGA hooks；frozen receipt 三门仍 false。Native 集成与 SECDA 共享；whole-model 执行与持久 KV 皆有 prior art。可辩护比较 = 同正确性下 launch/transfer/latency 是否降；部署便利 = 独立安装 + 模型移植证据。皆为待验证要求，非已证优势。

## KV-Cache Boundary (folded 2026-09-09)

规则：不用一个 yes/no 覆盖三层——(1) K/V computation（attention 图产 K/V，Transformer 几乎全有）；(2) Persistent KV state（历史 K/V 跨 step 存活 + append/read/position/reset-commit 语义）；(3) KV-specific optimization（物理位置/布局/分 bank/paging/DMA/带宽）。“实板模型”只计论文明确上板的生成模型；“通用”须分清 toolflow generality vs 同一 backend 接口 runtime generality。

分系：DFX Yes（每 token append 一行 K/V；tiled K/V 经 DMA/HBM）。FlightLLM Yes（大 KV + 权重放 HBM，decode 激活 always-on-chip；runtime/sampling ABI 未暴露）。Spatial Yes（prefill K/V 交 decode；double buffer + 片上 tiling 建模；非框架原生）。EdgeLLM Yes（KV 在线生成经专用 DMA 写 HBM）。StreamTensor 仅具名 dynamic tensor，append/位置/跨 call 协议未展开。CODO 公开 paper/artifact 无跨 token 持久（精确结论见下），当前输入 Q/K/V 照算。本地 Q4 Yes（跨 llama.cpp decode 调用的 append/read/clear/commit；96MiB HBM K/V + 分离端口四 bank；GGUF → GGML → stateful device → logits → sampling + pp/tg/pg + TTFT/ITL + 正确性）。

CODO 精确结论（只限可复核边界）：方法节无 KV cache/past_key_values/持久协议；`GPT2.py forward(x)` 只算当前 Q/K/V；Fig.9 host 建/迁 buffer 一次 + `enqueueTask(main_graph)` 一次；无 token loop/position/append 指针/跨 launch state；作者补充说明该实验只关心固定图单次 latency、未考虑 KV 优化。→公开的是固定-shape dataflow 编译 + 单次 graph execution，无跨 token 持久 KV 管理与 KV 优化。不对论文数字真伪下判，不说编译器原则上不能扩展 KV；只宜作 compiler/fixed-graph 行，不宜作 stateful generation throughput baseline。

指标按执行对象：fixed-shape 图/kernel → kernel/event latency、搬运、cycle、资源（CODO）；stateful backend/generation → pp/tg/pg、TTFT、ITL、E2E、KV depth、正确性（本地）。跨对象 token/s 只在模型/shape/精度/状态语义/计时边界全对齐后可比。Contribution 门槛（待验证）：同 backend/runtime 约定接第二模型（bitstream 再生如实报）；多 context depth 下 KV continuation/reset/logits-CPU-oracle；bank-map/context-sweep + HBM counter 证 K/V 分离确有效；只在边界匹配后算跨系统 speedup。第二模型仍重写 backend 则收回 runtime-generality；bank 消融无效则 HBM 布局降格为实现细节。

## Layout

```text
wiki/research/fpga-llm-inference/
  index.md            # 本页：唯一正式合成（含 09-09 折入的证据矩阵/审计/复核/KV 边界）
  threads/
    ideaspark_run/    # 两次 IdeaSpark 原始运行（成功 VSTC 链 + 失败 RegionSeal 链）
    paper-library/    # 历史 manifest、BibTeX、checksums 原样保留
  assets/             # 参考资料：index、metadata、paper-pdf、paper-tex、github-repo
```

论文库统一为 `assets/<ref_slug>/`（2026-10-07 从旧 `papers/` 迁入）。目录见下文 §Paper Library。

## Paper Library

This historical collection materializes the 68 papers cited by the manuscript's Related Work section plus 15 direct additions from the 2026-07-28 architecture search and SECDA-LLM from the 2026-09-08 framework-integration audit. Its paper records now live in `assets/<ref_slug>/`. The catalog below preserves that collection and its later annotations; it is not a count of every reference currently in this topic.

### Coverage

The 84 / 51 / 33 figures are the historical collection snapshot recorded in [manifest.yaml](threads/paper-library/manifest.yaml), not current topic-wide totals. Later references and availability changes must be checked against individual metadata.

| Item | Count |
|---|---:|
| Original Related Work papers | 68 |
| Direct architecture-search additions | 15 |
| Framework-integration audit additions | 1 |
| Total paper records | 84 |
| Validated full-paper PDFs | 51 |
| Author presentation only | 0 |
| Metadata only | 33 |

A downloaded PDF must be publicly reachable, begin with a valid PDF signature, open successfully, contain at least two pages, and match the cited title. Publisher HTML, access-denied pages, ResearchGate/Scribd copies and unmatched search results are not accepted. A missing PDF means only that no verified public copy was found in this pass; the DOI record remains indexed.

### Layout

- `assets/<ref_slug>/note.md`: documented reading or targeted verification only.
- `assets/<ref_slug>/citation.bib`: citation and preserved historical provenance snapshot.
- `assets/<ref_slug>/paper-pdf/`: validated public paper PDF, when available.
- `assets/<ref_slug>/paper-tex/{archives,extracted}/`: source archive and extracted TeX, when available.
- [manifest.yaml](threads/paper-library/manifest.yaml): preserved historical collection status.
- [related-work.bib](threads/paper-library/related-work.bib): the exact 68-entry citation subset.
- [checksums.sha256](threads/paper-library/checksums.sha256): preserved historical integrity hashes for cached PDFs and selected source archives. Its legacy paths describe the original collection layout; current paths are recorded in each reference metadata.

Most source archives and code repositories remain deferred. This pass completed source-first reading
for the five papers most relevant to the current runtime-boundary question: DFX, FlightLLM, Spatial LLM,
StreamTensor and CODO. Their archives and extracted trees live under the corresponding paper
directories; the per-paper metadata records the exact status.

The resulting cross-paper distinction is summarized in
[[research/fpga-llm-inference/index]]: K/V computation, persistent
cross-token state and KV-specific physical optimization are separate evidence items, as are
fixed-graph kernel latency and a complete stateful generation request.

The 2026-07-28 additions are selected from the unfiltered six-query union search (241 source records deduplicated to 142; see [[research/fpga-llm-inference/index]] Literature Provenance for method, admission rule and the 15-record table); they are not claimed to be manuscript citations.

The 2026-09-08 update adds [[research/fpga-llm-inference/assets/secda-llm-2024/note|SECDA-LLM]] after reading its full TeX paper and
bibliography. The historical audit pinned and archived its official repository and two exact gitlink dependencies;
backend/KV inspection is targeted and does not establish a reproduced build. Original Hummingbird's
source is archived for targeted thematic review and remains unprocessed. The revised nine-system
comparison plus local backend row and selection rationale are in [[research/fpga-llm-inference/index]].

### Catalog

| Paper | Year | Related Work category | Cache status | Canonical source |
|---|---:|---|---|---|
| [[research/fpga-llm-inference/assets/secda-llm-2024/note|SECDA-LLM: Designing Efficient LLM Accelerators for Edge Devices]] | 2024 | Framework-integrated FPGA LLM inference | `processed; code audit partial` | ARC-LG @ ISCA 2024; arXiv 2408.00462 |
| [[research/fpga-llm-inference/assets/f-bfq-2025/note|F-BFQ: Flexible Block Floating-Point Quantization Accelerator for LLMs]] | 2025 | Framework-integrated FPGA LLM inference | `abstract and HTML read 2026-09-27` | LG-ARC @ ISCA 2025; arXiv 2510.13401 |
| [[research/fpga-llm-inference/assets/imax-llm-2025/note|Efficient Kernel Mapping and Comprehensive System Evaluation of LLM Acceleration on a CGLA (IMAX)]] | 2025 | Framework-integrated FPGA LLM inference | `TeX read 2026-09-27` | IEEE Access 2025; arXiv 2512.00335 |
| [[research/fpga-llm-inference/assets/ftrans-2020/citation.bib|FTRANS: Energy-Efficient Acceleration of Transformers using FPGA]] | 2020 | FPGA Transformer and LLM systems | `downloaded` | arXiv 2007.08563 |
| [[research/fpga-llm-inference/assets/sanger-2021/citation.bib|Sanger: A Co-Design Framework for Enabling Sparse Attention using Reconfigurable Architecture]] | 2021 | FPGA Transformer and LLM systems | `downloaded` | DOI `10.1145/3466752.3480125` |
| [[research/fpga-llm-inference/assets/dfx-2022/note|DFX: A Low-latency Multi-FPGA Appliance for Accelerating Transformer-based Text Generation]] | 2022 | FPGA Transformer and LLM systems | `processed` | arXiv 2209.10797 |
| [[research/fpga-llm-inference/assets/flightllm-2024/note|FlightLLM: Efficient Large Language Model Inference with a Complete Mapping Flow on FPGAs]] | 2024 | FPGA Transformer and LLM systems | `processed` | arXiv 2401.03868 |
| [[research/fpga-llm-inference/assets/spatial-llm-2024/note|Understanding the Potential of FPGA-Based Spatial Acceleration for Large Language Model Inference]] | 2024 | FPGA Transformer and LLM systems | `processed` | arXiv 2312.15159 |
| [[research/fpga-llm-inference/assets/edgellm-2025/note|EdgeLLM: A Highly Efficient CPU-FPGA Heterogeneous Edge Accelerator for Large Language Models]] | 2025 | FPGA Transformer and LLM systems | `processed` | arXiv 2407.21325 |
| [[research/fpga-llm-inference/assets/glitches-2024/citation.bib|GLITCHES: GPU-FPGA LLM Inference Through a Collaborative Heterogeneous System]] | 2024 | FPGA Transformer and LLM systems | `downloaded` | DOI `10.1109/HPEC62836.2024.10938498` |
| [[research/fpga-llm-inference/assets/streamtensor-2025/note|StreamTensor: Make Tensors Stream in Dataflow Accelerators for LLMs]] | 2025 | FPGA Transformer and LLM systems | `processed` | arXiv 2509.13694 |
| [[research/fpga-llm-inference/assets/codo-2026/note|CODO: An Automated Compiler for Comprehensive Dataflow Optimization]] | 2026 | FPGA Transformer and LLM systems | `processed` | arXiv 2604.12618 |
| [[research/fpga-llm-inference/assets/tellme-v2-2026/note|TeLLMe: An Efficient End-to-End Ternary LLM Prefill and Decode Accelerator with Table-Lookup Matmul on Edge FPGAs]] | 2026 | FPGA Transformer and LLM systems | `downloaded` | arXiv 2510.15926 |
| [[research/fpga-llm-inference/assets/fast-prefill-2026/citation.bib|FAST-Prefill: FPGA Accelerated Sparse Attention for Long Context LLM Prefill]] | 2026 | FPGA Transformer and LLM systems | `downloaded` | arXiv 2602.20515 |
| [[research/fpga-llm-inference/assets/flexllm-hls-2026/note|FlexLLM: Composable HLS Library for Flexible Hybrid LLM Accelerator Design]] | 2026 | FPGA Transformer and LLM systems | `downloaded` | arXiv 2601.15710 |
| [[research/fpga-llm-inference/assets/hummingbird-plus-2026/citation.bib|Hummingbird+: Advancing FPGA-Based LLM Deployment from Research Prototype to Edge Product]] | 2026 | FPGA Transformer and LLM systems | `metadata-only` | DOI `10.1145/3748173.3779189` |
| [[research/fpga-llm-inference/assets/lut-llm-2026/note|LUT-LLM: Efficient Language Model Inference with Memory-Based Computations on FPGAs]] | 2026 | FPGA Transformer and LLM systems | `downloaded` | arXiv 2511.06174 |
| PD-Swap: Prefill-Decode Logic Swapping for End-to-End LLM Inference on Edge FPGAs via Dynamic Partial Reconfiguration (原目录已移除；历史内容见 git 记录) | 2025 | FPGA Transformer and LLM systems | `downloaded` | arXiv 2512.11550 |
| [[research/fpga-llm-inference/assets/scalable-gpt2-2023/citation.bib|A Scalable GPT-2 Inference Hardware Architecture on FPGA]] | 2023 | Multi-FPGA and distributed inference | `metadata-only` | DOI `10.1109/IJCNN54540.2023.10191067` |
| The Feasibility of Implementing Large-Scale Transformers on Multi-FPGA Platforms (原目录已移除；历史内容见 git 记录) | 2024 | Multi-FPGA and distributed inference | `downloaded` | arXiv 2404.16158 |
| [[research/fpga-llm-inference/assets/looplynx-2025/citation.bib|LoopLynx: A Scalable Dataflow Architecture for Efficient LLM Inference]] | 2025 | Multi-FPGA and distributed inference | `downloaded` | arXiv 2504.09561 |
| [[research/fpga-llm-inference/assets/lora-2026/citation.bib|LORA: A Latency-Oriented Recurrent Architecture for Large Language Model on Multi-FPGA Platform With Communication Optimization]] | 2026 | Multi-FPGA and distributed inference | `metadata-only` | DOI `10.1109/TCAD.2025.3629537` |
| [[research/fpga-llm-inference/assets/terafly-2026/citation.bib|TeraFly: A Multinode FPGA-Based Accelerator Design for Efficient Cooperative Inference in LLMs]] | 2026 | Multi-FPGA and distributed inference | `metadata-only` | DOI `10.1109/TCAD.2025.3616078` |
| [[research/fpga-llm-inference/assets/hlstransform-2024/citation.bib|HLSTransform: Energy-Efficient Llama 2 Inference on FPGAs Via High Level Synthesis]] | 2024 | Embedded and low-bit LLM deployment | `downloaded` | arXiv 2405.00738 |
| [[research/fpga-llm-inference/assets/llamaf-2024/citation.bib|LlamaF: An Efficient Llama2 Architecture Accelerator on Embedded FPGAs]] | 2024 | Embedded and low-bit LLM deployment | `downloaded` | arXiv 2409.11424 |
| [[research/fpga-llm-inference/assets/embedded-bw-2025/note|Pushing up to the Limit of Memory Bandwidth and Capacity Utilization for Efficient LLM Decoding on Embedded FPGA]] | 2025 | Embedded and low-bit LLM deployment | `downloaded` | arXiv 2502.10659 |
| [[research/fpga-llm-inference/assets/meadow-2025/citation.bib|MEADOW: Memory-Efficient Dataflow and Data Packing for Low Power Edge LLMs]] | 2025 | Embedded and low-bit LLM deployment | `downloaded` | arXiv 2503.11663 |
| [[research/fpga-llm-inference/assets/hummingbird-2025/citation.bib|Hummingbird: A Smaller and Faster Large Language Model Accelerator on Embedded FPGA]] | 2025 | Embedded and low-bit LLM deployment | `downloaded` | arXiv 2507.03308 |
| [[research/fpga-llm-inference/assets/qllama-2025/citation.bib|QLlama: An FPGA-Based Microscaling Quantization Accelerator for Energy-Efficient Llama2 Inference]] | 2025 | Embedded and low-bit LLM deployment | `metadata-only` | DOI `10.1109/LES.2025.3600563` |
| TerEffic: Highly Efficient Ternary LLM Inference on FPGA (原目录已移除；历史内容见 git 记录) | 2025 | Embedded and low-bit LLM deployment | `downloaded` | arXiv 2502.16473 |
| TENET: An Efficient Sparsity-Aware LUT-Centric Architecture for Ternary LLM Inference on Edge (原目录已移除；历史内容见 git 记录) | 2025 | Embedded and low-bit LLM deployment | `downloaded` | arXiv 2509.13765 |
| [[research/fpga-llm-inference/assets/tflop-2026/citation.bib|TFLOP: Towards Energy-Efficient LLM Inference, an FPGA-Affinity Accelerator with Unified LUT-Based Optimization]] | 2026 | Embedded and low-bit LLM deployment | `metadata-only` | DOI `10.1109/ASP-DAC66049.2026.11420766` |
| [[research/fpga-llm-inference/assets/llm-on-fpga-2025/citation.bib|LLM on FPGA: Squeezing Language Models by Quantization and Multi-Query Attention and Its Efficient Hardware Architecture]] | 2025 | Embedded and low-bit LLM deployment | `metadata-only` | DOI `10.1109/ISOCC66390.2025.11329964` |
| [[research/fpga-llm-inference/assets/robot-llm-fpga-2025/citation.bib|Computationally Efficient FPGA-Based Large Language Model Inference for Real-Time Decision-Making in Robotic Systems]] | 2025 | Embedded and low-bit LLM deployment | `metadata-only` | DOI `10.1109/IROS60139.2025.11247019` |
| [[research/fpga-llm-inference/assets/accllm-2025/note|AccLLM: Accelerating Long-Context LLM Inference Via Algorithm-Hardware Co-Design]] | 2025 | Long-context and phase-specialized acceleration | `downloaded; verified 2026-09-27` | IEEE TVLSI 2026, DOI `10.1109/TVLSI.2026.3658524` |
| [[research/fpga-llm-inference/assets/metal-2025/citation.bib|METAL: A Memory-Efficient Transformer Architecture for Long-Context Inference on FPGA]] | 2025 | Long-context and phase-specialized acceleration | `metadata-only` | DOI `10.1109/ASAP65064.2025.00023` |
| [[research/fpga-llm-inference/assets/cxl-speckv-2025/citation.bib|CXL-SpecKV: A Disaggregated FPGA Speculative KV-Cache for Datacenter LLM Serving]] | 2025 | Long-context and phase-specialized acceleration | `downloaded` | arXiv 2512.11920 |
| ELiTeFormer: An Efficient Transformer for FPGAs (原目录已移除；历史内容见 git 记录) | 2026 | Long-context and phase-specialized acceleration | `downloaded` | arXiv 2607.03652 |
| [[research/fpga-llm-inference/assets/transformer-opu-2023/citation.bib|Transformer-OPU: An FPGA-based Overlay Processor for Transformer Networks]] | 2023 | Programmable and specialized FPGA execution | `metadata-only` | DOI `10.1109/FCCM57271.2023.00049` |
| [[research/fpga-llm-inference/assets/fet-opu-2023/citation.bib|FET-OPU: A Flexible and Efficient FPGA-Based Overlay Processor for Transformer Networks]] | 2023 | Programmable and specialized FPGA execution | `metadata-only` | DOI `10.1109/ICCAD57390.2023.10323752` |
| [[research/fpga-llm-inference/assets/cstrans-opu-2024/citation.bib|CSTrans-OPU: An FPGA-based Overlay Processor with Full Compilation for Transformer Networks via Sparsity Exploration]] | 2024 | Programmable and specialized FPGA execution | `metadata-only` | DOI `10.1145/3649329.3657325` |
| [[research/fpga-llm-inference/assets/chatopu-2024/citation.bib|ChatOPU: An FPGA-based Overlay Processor for Large Language Models with Unstructured Sparsity]] | 2024 | Programmable and specialized FPGA execution | `metadata-only` | DOI `10.1145/3676536.3676761` |
| [[research/fpga-llm-inference/assets/moe-opu-2025/citation.bib|MoE-OPU: An FPGA Overlay Processor Leveraging Expert Parallelism for MoE-Based Large Language Models]] | 2025 | Programmable and specialized FPGA execution | `metadata-only` | DOI `10.1109/ICCAD66269.2025.11240807` |
| [[research/fpga-llm-inference/assets/dllm-opu-2026/citation.bib|dLLM-OPU: An FPGA Overlay Processor for Accelerated Diffusion Large Language Models]] | 2026 | Programmable and specialized FPGA execution | `metadata-only` | DOI `10.1109/ASP-DAC66049.2026.11420284` |
| [[research/fpga-llm-inference/assets/skipopu-2026/citation.bib|SkipOPU: An FPGA-Based Overlay Processor for Large Language Models with Dynamically Allocated Computation]] | 2026 | Programmable and specialized FPGA execution | `downloaded` | arXiv 2603.14785 |
| [[research/fpga-llm-inference/assets/lightmamba-2025/citation.bib|LightMamba: Efficient Mamba Acceleration on FPGA with Quantization and Hardware Co-Design]] | 2025 | Programmable and specialized FPGA execution | `downloaded` | arXiv 2502.15260 |
| [[research/fpga-llm-inference/assets/graphagile-2023/citation.bib|GraphAGILE: An FPGA-Based Overlay Accelerator for Low-Latency GNN Inference]] | 2023 | Programmable and specialized FPGA execution | `downloaded` | arXiv 2302.01769 |
| [[research/fpga-llm-inference/assets/runtime-adaptive-transformer-2026/citation.bib|A Runtime-Adaptive Transformer Neural Network Accelerator on FPGAs]] | 2026 | Programmable and specialized FPGA execution | `downloaded` | arXiv 2411.18148 |
| [[research/fpga-llm-inference/assets/flame-2024/citation.bib|FLAME: Fully Leveraging MoE Sparsity for Transformer on FPGA]] | 2024 | Programmable and specialized FPGA execution | `metadata-only` | DOI `10.1145/3649329.3656507` |
| [[research/fpga-llm-inference/assets/baqet-2025/citation.bib|BAQET: BRAM-aware Quantization for Efficient Transformer Inference via Stream-based Architecture on an FPGA]] | 2025 | Programmable and specialized FPGA execution | `metadata-only` | DOI `10.1145/3706628.3708849` |
| [[research/fpga-llm-inference/assets/speedllm-2025/citation.bib|SpeedLLM: An FPGA Co-design of Large Language Model Inference Accelerator]] | 2025 | Programmable and specialized FPGA execution | `downloaded` | arXiv 2507.14139 |
| [[research/fpga-llm-inference/assets/xtramac-2026/citation.bib|XtraMAC: An Efficient MAC Architecture for Mixed-Precision LLM Inference on FPGA]] | 2026 | Programmable and specialized FPGA execution | `downloaded` | arXiv 2605.06052 |
| [[research/fpga-llm-inference/assets/scalehls-2022/citation.bib|ScaleHLS: A New Scalable High-Level Synthesis Framework on Multi-Level Intermediate Representation]] | 2022 | Composable accelerator compilation | `downloaded` | arXiv 2107.11673 |
| [[research/fpga-llm-inference/assets/tapa-2023/citation.bib|TAPA: A Scalable Task-parallel Dataflow Programming Framework for Modern FPGAs with Co-optimization of HLS and Physical Design]] | 2023 | Composable accelerator compilation | `downloaded` | arXiv 2209.02663 |
| [[research/fpga-llm-inference/assets/allo-2024/citation.bib|Allo: A Programming Model for Composable Accelerator Design]] | 2024 | Composable accelerator compilation | `downloaded` | arXiv 2404.04815 |
| [[research/fpga-llm-inference/assets/intrra-2025/citation.bib|InTRRA: Inter-Task Resource-Repurposing Accelerator for Efficient Transformer Inference on FPGAs]] | 2025 | Composable accelerator compilation | `metadata-only` | DOI `10.1145/3706628.3708828` |
| [[research/fpga-llm-inference/assets/integer-fusion-2025/citation.bib|Enhancing Transformer Inference Efficiency on FPGA Through Fully Fusion and Integer-Only Quantization Techniques]] | 2025 | Composable accelerator compilation | `metadata-only` | DOI `10.1109/ICCD65941.2025.00020` |
| [[research/fpga-llm-inference/assets/shuhai-2020/citation.bib|Shuhai: Benchmarking High Bandwidth Memory on FPGAs]] | 2020 | HBM topology and data movement | `downloaded` | arXiv 2005.04324 |
| [[research/fpga-llm-inference/assets/hbm-connect-2021/citation.bib|HBM Connect: High-Performance HLS Interconnect for FPGA HBM]] | 2021 | HBM topology and data movement | `downloaded` | DOI `10.1145/3431920.3439301` |
| [[research/fpga-llm-inference/assets/verilogeval-2023/citation.bib|Invited Paper: VerilogEval: Evaluating Large Language Models for Verilog Code Generation]] | 2023 | Kernel generation and evaluation | `downloaded` | arXiv 2309.07544 |
| [[research/fpga-llm-inference/assets/rtllm-2024/citation.bib|RTLLM: An Open-Source Benchmark for Design RTL Generation with Large Language Model]] | 2024 | Kernel generation and evaluation | `downloaded` | arXiv 2308.05345 |
| [[research/fpga-llm-inference/assets/gpt4aigchip-2023/citation.bib|GPT4AIGChip: Towards Next-Generation AI Accelerator Design Automation via Large Language Models]] | 2023 | Kernel generation and evaluation | `downloaded` | arXiv 2309.10730 |
| [[research/fpga-llm-inference/assets/hlspilot-2024/citation.bib|HLSPilot: LLM-based High-Level Synthesis]] | 2024 | Kernel generation and evaluation | `downloaded` | arXiv 2408.06810 |
| [[research/fpga-llm-inference/assets/llm-aid-2024/citation.bib|LLM-AID: Leveraging Large Language Models for Rapid Domain-Specific Accelerator Development]] | 2024 | Kernel generation and evaluation | `metadata-only` | DOI `10.1145/3676536.3697135` |
| [[research/fpga-llm-inference/assets/rtlrewriter-2024/citation.bib|RTLRewriter: Methodologies for Large Models aided RTL Code Optimization]] | 2024 | Kernel generation and evaluation | `downloaded` | arXiv 2409.11414 |
| [[research/fpga-llm-inference/assets/hls-codegen-benchmark-2025/citation.bib|Exploring Code Language Models for Automated HLS-based Hardware Generation: Benchmark, Infrastructure and Analysis]] | 2025 | Kernel generation and evaluation | `downloaded` | arXiv 2502.13921 |
| [[research/fpga-llm-inference/assets/autodse-2022/citation.bib|AutoDSE: Enabling Software Programmers to Design Efficient FPGA Accelerators]] | 2022 | Evidence and optimization methodology | `downloaded` | arXiv 2009.14381 |
| [[research/fpga-llm-inference/assets/ranktuner-2024/citation.bib|RankTuner: When Design Tool Parameter Tuning Meets Preference Bayesian Optimization]] | 2024 | Evidence and optimization methodology | `downloaded` | DOI `10.1145/3676536.3676782` |
| [[research/fpga-llm-inference/assets/hlsfactory-2024/citation.bib|HLSFactory: A Framework Empowering High-Level Synthesis Datasets for Machine Learning and Beyond]] | 2024 | Evidence and optimization methodology | `downloaded` | arXiv 2405.00820 |
| [[research/fpga-llm-inference/assets/bench4hls-2026/citation.bib|Bench4HLS: End-to-End Evaluation of LLMs in High-Level Synthesis Code Generation]] | 2026 | Evidence and optimization methodology | `downloaded` | arXiv 2601.19941 |
| [[research/fpga-llm-inference/assets/softermax-2021/citation.bib|Softermax: Hardware/Software Co-Design of an Efficient Softmax for Transformers]] | 2021 | Evidence and optimization methodology | `downloaded` | arXiv 2103.09301 |

### 2026-07-28 Architecture Additions

| Paper | Year | Category | Cache status | Canonical source |
|---|---:|---|---|---|
| [[research/fpga-llm-inference/assets/mpk-2025/citation.bib|MPK: A Compiler and Runtime for Mega-Kernelizing Tensor Programs]] | 2025 | Coarse-grained and persistent execution | `downloaded` | arXiv 2512.22219 |
| [[research/fpga-llm-inference/assets/cd-llm-2026/citation.bib|CD-LLM: A Heterogeneous Multi-FPGA System for Batched Decoding of 70B+ LLMs Using a Compute-Dedicated Architecture]] | 2026 | HBM-aware and decode architectures | `metadata-only` | DOI `10.1145/3771288` |
| [[research/fpga-llm-inference/assets/flightopu-2025/citation.bib|FlightOPU: An FPGA Overlay Processor for LLM with HBM-Aware Multi-Die Architecture]] | 2025 | HBM-aware and decode architectures | `metadata-only` | DOI `10.1109/ICFPT67023.2025.00048` |
| [[research/fpga-llm-inference/assets/nyx-2025/citation.bib|Nyx: Virtualizing dataflow execution on shared FPGA platforms]] | 2025 | Shared and virtualized FPGA execution | `metadata-only` | DOI `10.1145/3695053.3731094` |
| [[research/fpga-llm-inference/assets/pcie-coarse-systolic-2025/citation.bib|Hardware-Software Co-Design for Efficient LLM Inference on PCIe-Based FPGAs Using Coarse-Grained Systolic Arrays]] | 2025 | Coarse-grained and persistent execution | `metadata-only` | DOI `10.1109/SOCC66126.2025.11235351` |
| [[research/fpga-llm-inference/assets/riscbench-2026/citation.bib|RISCBench: Benchmarking RISC-V Orchestration Efficiency in FPGA and FPGA-Like Computing Engines]] | 2026 | Evidence and orchestration methodology | `metadata-only` | DOI `10.1145/3748173.3779569` |
| [[research/fpga-llm-inference/assets/h2-llm-2025/citation.bib|H2-LLM: Hardware-Dataflow Co-Exploration for Heterogeneous Hybrid-Bonding-based Low-Batch LLM Inference]] | 2025 | HBM-aware and decode architectures | `metadata-only` | DOI `10.1145/3695053.3731008` |
| [[research/fpga-llm-inference/assets/mcore-opu-2024/citation.bib|An FPGA-Based Multi-Core Overlay Processor for Transformer-Based Models]] | 2024 | Programmable and specialized FPGA execution | `metadata-only` | DOI `10.1109/ISEDA62518.2024.10617729` |
| [[research/fpga-llm-inference/assets/streaming-vpe-2024/citation.bib|An FPGA-Based Efficient Streaming Vector Processing Engine for Transformer-Based Models]] | 2024 | Coarse-grained and persistent execution | `metadata-only` | DOI `10.1109/ISEDA62518.2024.10617499` |
| [[research/fpga-llm-inference/assets/dtcore-2026/citation.bib|DTCore: A Compiler-Directed Control-Minimal FPGA Compute Engine]] | 2026 | Coarse-grained and persistent execution | `metadata-only` | DOI `10.1109/FCCM68464.2026.00053` |
| [[research/fpga-llm-inference/assets/festal-2026/citation.bib|FESTAL: Dataflow Accelerator Synthesis Framework with Graph-Based Fusion for FPGA]] | 2026 | Composable accelerator compilation | `metadata-only` | DOI `10.1109/ASP-DAC66049.2026.11420389` |
| [[research/fpga-llm-inference/assets/fmc-llm-2025/citation.bib|FMC-LLM: Enabling FPGAs for Efficient Batched Decoding of 70B+ LLMs with a Memory-Centric Streaming Architecture]] | 2025 | HBM-aware and decode architectures | `metadata-only` | DOI `10.1145/3706628.3708863` |
| [[research/fpga-llm-inference/assets/e2e-overlay-compiler-2025/citation.bib|End-to-end Compilation is All FPGAs Need: A Unified Overlay-based FPGA Compiler for Deep Learning]] | 2025 | Composable accelerator compilation | `metadata-only` | DOI `10.1145/3658617.3697562` |
| [[research/fpga-llm-inference/assets/lembda-2026/citation.bib|Lembda: Optimizing LLM Inference on Embedded Platforms via CPU/FPGA Co-processing]] | 2026 | CPU-FPGA heterogeneous inference | `metadata-only` | DOI `10.1007/978-981-95-1021-4_35` |
| [[research/fpga-llm-inference/assets/cgra-space-time-2025/citation.bib|Monomorphism-Based CGRA Mapping via Space and Time Decoupling]] | 2025 | Overlay and CGRA mapping | `downloaded` | arXiv 2512.02859 |

### Model coverage recheck — 2026-09-15

Ten manuscript comparison entries now have source/paper-based model-input and coverage audits in their individual indexes. See [[research/fpga-llm-inference/index#Model input and coverage audit (2026-09-15)|comparison and evidence boundaries]]. Selected implementation sources and hash receipts accompany each open-source entry.

返回 [[research/index]]。

## Model input and coverage audit (2026-09-15)

Coverage describes implementation binding and observed model scope separately. Missing filename suffixes do not imply fixed-model hardware. A reusable compiler/library/backend is not a demonstrated arbitrary-model deployment flow. Source-based classifications use pinned implementation files; unavailable implementations use paper claims, explicitly labeled.

| Work | Model input | Implementation / evidence scope | Models |
|---|---|---|---|
| [[research/fpga-llm-inference/assets/lut-llm-2026/note|lut-llm-2026]] | Original checkpoint format NR; random-data testbench | Model-specific implementation | Qwen3-1.7B block; general checkpoint loader not established. |
| [[research/fpga-llm-inference/assets/streamtensor-2025/note|streamtensor-2025]] | PyTorch model; suffix NR | Cross-architecture (paper) | GPT-2, Qwen, Llama and Gemma; block/phase evidence. |
| [[research/fpga-llm-inference/assets/spatial-llm-2024/note|spatial-llm-2024]] | Hugging Face checkpoint; suffix NR | Reusable kernels; model-specific composition | BERT and GPT-2 measured; larger LLaMA/Vicuna studies are not equivalent board evidence. |
| [[research/fpga-llm-inference/assets/dfx-2022/note|dfx-2022]] | Megatron/OpenAI GPT-2 checkpoint; suffix NR | Single family, multiple sizes (paper) | GPT-2 345M, 774M and 1.5B. |
| [[research/fpga-llm-inference/assets/tellme-v2-2026/note|tellme-v2-2026]] | Original format NR; prepared .bin runtime weights | Model-specific implementation | BitNet-0.73B ternary model. |
| [[research/fpga-llm-inference/assets/flexllm-hls-2026/note|flexllm-hls-2026]] | Original format NR; prepared .bin weights; GGUF tokenizer only | Reusable library; model-specific implementation | Llama-3.2-1B variants, plus HMT extension. |
| [[research/fpga-llm-inference/assets/codo-2026/note|codo-2026]] | PyTorch nn.Module in .py | Reusable compiler; one LLM example | GPT-2 block; additional CNN/MLP/operator benchmarks. |
| [[research/fpga-llm-inference/assets/edgellm-2025/note|edgellm-2025]] | Sparse/quantized model; file format NR | Cross-architecture (paper) | GLM-6B and Qwen-7B. |
| [[research/fpga-llm-inference/assets/flightllm-2024/note|flightllm-2024]] | PyTorch model; suffix NR; prepared board .bin files | Cross-architecture (paper) | OPT-6.7B and LLaMA2-7B. |
| [[research/fpga-llm-inference/assets/secda-llm-2024/note|secda-llm-2024]] | GGUF (later source) | Reusable operator backend; one model evaluated | TinyLlama paper evaluation; multiple model configurations in later source. |

Code availability audit: several pre-existing `repo/` paths were empty despite metadata saying archived. Restored local source caches for five repositories and retained the inspected files under each paper’s `source/code-audit/` so evidence is versioned despite the existing `**/repo/` ignore rule. FlexLLM cache is partial; selected files and their hashes are recorded explicitly. Existing paper PDFs/TeX were reused; EdgeLLM was read through PDF extraction. No bitstreams, weights, toolchains or synthesis outputs were downloaded. Input-format NR means not established, not unsupported.

## Paper-only competition audit (2026-09-15)

**当前准入：必须有可核验论文；公开 arXiv preprint 算论文，但不等于同行评审录用。GitHub star 仅用于发现候选，仓库/README/endorsement 本身不算论文。此规则覆盖上方历史 OR 准入。** 先匹配论文标题、作者和项目关联，再区分完整系统、单层/kernel、设计工具。没有公开 arXiv 不证明没有正式出版论文，但在未获得替代论文证据前不纳入本轮。

| 核实对象 | 公开论文证据 | 本轮结论 |
|---|---|---|
| [[research/fpga-llm-inference/assets/imax-cgla-2025/note|IMAX / IMAX3-LLM]] | arXiv:2512.00335v1；PDF 首页 IEEE Access DOI；论文直接链接官方仓库 | 新增正式深读条目；llama.cpp CPU MatMul 内 FPGA offload，直接集成相关。不是已证独立 GGML device backend；44.4× 能效为 ASIC 投影 |
| Persistent-state GDN (原目录已移除；历史内容见 git 记录) | arXiv:2603.05931v1；PDF/TeX 标题作者一致 | 新增正式深读条目；单层状态更新，HLS 估算性能，不是完整 backend，不关联 Tyler913 仓库 |
| WPU | README 自称论文题目 “Bit-Exact by Construction: A Verification-First RTL Accelerator that Inherits the GGUF k-Quant Checkpoint Ecosystem”，链接寻求 arXiv endorsement | 项目名/标题检索未找到匹配公开 arXiv；暂不计入。Endorsement 不是公开论文 |
| Tsavorite / tsisw | Tsavorite 名称检索无匹配公开 arXiv | 实现证据不代替论文，暂不计入 |
| Loom、fable5、APEX、XMC（Streaming Compressed-Weight）、PolarFire llama、GEMMA3 FPGA、Spanker、KEV GPT | 见归档查询；无项目身份匹配的 arXiv（部分返回无关结果） | 暂不计入，不能把关键词相似论文挂到这些仓库 |

保留现有有论文条目作比较：SECDA 是已读集成先例；IMAX 表明不能只找到 2024 SECDA 就结束。CODO/StreamTensor 等按既有 notes 的 fixed-graph/phase 边界评估；DFX/FlightLLM/EdgeLLM 等是完整系统或状态驻留相关先例。**“做了 llama.cpp FPGA backend”本身不足以支撑首创；论文机会要落到正确性、整图/状态驻留、第二模型部署和匹配条件实测改善。** 当前项目范围不能拿计划中的自动跨模型映射当已实现优势。

### 已下载但未进入正式比较的外围论文

以下均已取得公开 arXiv v1 源码及 PDF，核对首页标题、页数并保存 SHA-256；**未完成全文阅读，metadata 保持 not_started/downloaded，无占位正式 paper note，也不据此作性能判断**。它们是扩展检索缓存，不是“又找到五个完整 backend”。

| 候选 | arXiv | 缓存与状态 |
|---|---|---|
| Design Conductor 2.0 | 2605.05170v1 | [metadata](assets/design-conductor-2-2026/citation.bib)，12 页；设计自动化方向 |
| LLM-Driven Design Space Exploration of FPGA-based Accelerators | 2605.05920v1 | [metadata](assets/secda-dse-2026/citation.bib)，6 页；SECDA DSE 后续 |
| Towards Autonomous Accelerator Design: FPGA Accelerator Generation with SECDA | 2606.11117v1 | [metadata](assets/secda-autonomous-2026/citation.bib)，6 页；SECDA 设计生成后续 |
| UNISON: A Co-Designed Near-Memory Scheduler of Session KV Residency for LLM Agents | 2609.09643v1 | [metadata](assets/unison-2026/citation.bib)，13 页；session KV scheduler |
| FlexPosit: Tunable Fractional Precision for LLM Inference Accelerators | 2609.04724v1 | [metadata](assets/flexposit-2026/citation.bib)，15 页；数值格式/架构方向 |

检索证据：[查询与结果](threads/paper-eligibility-2026-09-15/arxiv-results.txt)、[脚本](threads/paper-eligibility-2026-09-15/search_arxiv.py)、[WPU README 快照](threads/paper-eligibility-2026-09-15/WPU-README.md)、[哈希清单](threads/paper-eligibility-2026-09-15/manifest.yaml)。查询 HTML 同目录保留，查询名为文件名；检索有名称召回局限，负结果只表示截至本轮未找到匹配，不能证明论文不存在。

归档状态：两篇全文阅读+正式 note，七篇 PDF/TeX 缓存及身份检查；未运行下载代码、综合或 FPGA 板级复现。发现已有未完成的 `assets/imax-llm-2025/` PDF 缓存，保持原样，不将其另计论文；本轮正式入口为 canonical `assets/imax-cgla-2025/`。

## Decode-speed anchor and original-text verification (2026-09-27)

**Inclusion rule for comparisons:** only formally published work (conference, journal or peer-reviewed workshop) or arXiv work with a usable public repository that has GitHub stars. Wiki summaries are leads, not evidence: every table cell must be checked against the paper text or public code.

**Single-request decode rates as reported** (checked in the original; details and line numbers in each paper note):

| System | Board (peak GB/s) | MHz | Model | Weights | token/s | Implied weight GB/s (% peak) | Basis |
|---|---|---:|---|---|---:|---:|---|
| DFX | U280 (460) | 200 | GPT-2 345M | FP16 | 185.19 | 131 (28%) | board, via StreamTensor table |
| Allo (spatial) | U280 (460) | 250 | GPT-2 Medium | W4A8 | 204.05 | 36 (8%) | board, via StreamTensor table |
| StreamTensor | U55C (460) | 250 | GPT-2 Medium | W4A8 | 199.51 at 32:32 | 35 (8%) | board |
| CODO | U280 (460) | 300 | GPT-2 Medium | W4A8 | 231.48 | 41 (9%) | model-level rate from a one-block kernel |
| FlexLLM | U280 (460) | 292 | Llama-3.2-1B | W4A4 | ~144 (6.94 s/1k) | 89 (19%) | board |
| FlightLLM | U280 (460) | 225 | LLaMA2-7B | W3.5A8 + N:M | 55 | paper: 65.9% util. | secondary (AccLLM Table VII) |
| AccLLM | U280 (460) | 225 | Llama-2-7B | W2A8 + 2:4 | 164 | — | cycle-accurate simulation |
| EdgeLLM | VCU128 (460) | 280 | GLM-6B | W4, FP16 act. | ~90 | 279 (61%); paper ~75% for matmul | board |
| Li et al. (DATE'25) | KV260 (19.2) | 300 | LLaMA2-7B | W4 AWQ | ~5 | 17 (88%); paper 85% | board |
| TeLLMe v2 | KV260 (19.2) | — | BitNet 0.73B | W1.58A8 | up to 25 | — | board, LM head on ARM |
| F-BFQ | KV260 (19.2) | 200 | GPT-2 163M | Q2_K/Q3_K | up to 12.2 | — | board, llama.cpp MatMul offload |
| SECDA-LLM | PYNQ-Z1 | — | TinyLlama 1.1B | Q3_K | 0.59 (1.7 s/token) | — | board, llama.cpp MatMul offload |

Implied traffic = matrix parameters read per token (incl. vocabulary head) x weight bits / 8 x token/s; a lower bound that ignores KV, scales and activations. Without absolute rates in the text: FlightLLM (normalized only), Spatial Allo (relative to DFX), LUT-LLM (relative to GPUs), IMAX (figures only).

**Corrections to earlier wiki content found in this pass:**
- CODO Table VI's DFX, Allo and StreamTensor values originate in StreamTensor's own GPT-2 table (identical values); CODO's 64:64 total is one token interval above TTFT + G/speed.
- CODO public artifact (fig-9): the decode kernel is one block and one token with no KV input and no vocabulary matrix, timed as one launch.
- FlightLLM's method takes a compressed PyTorch model through an automated IR/ISA flow; "prepared cases" applies only to the public artifact. The paper has no absolute U280 token/s; the 55 token/s figure is AccLLM's tabulation, and TeLLMe's "153 token/s" has no traceable source.
- AccLLM is published (IEEE TVLSI 2026, DOI 10.1109/TVLSI.2026.3658524); its 164 token/s is simulated. SECDA-LLM appeared at the ARC-LG workshop at ISCA 2024.
- EdgeLLM's own text reports GLM-6B ~90 token/s at 280 MHz (MatMul), whereas AccLLM tabulates ChatGLM2-6B at 125 MHz and 75 token/s.
- Spatial Allo fetches each layer's parameters from the host (not device-resident); FlexLLM relays KV through the host between separate prefill and decode bitstreams; TeLLMe runs embedding, LM head and sampling on the ARM host.
- New entries: [[research/fpga-llm-inference/assets/f-bfq-2025/note|F-BFQ]] (llama.cpp MatMul offload, KV260) and an [[research/fpga-llm-inference/assets/imax-llm-2025/note|IMAX]] note (VPK180 prototype, Qwen3, host-managed KV).

### Table eligibility decisions (2026-09-27)
- Excluded from comparison tables: F-BFQ (LG-ARC workshop, no public code) and SECDA-LLM (ARC-LG workshop; github.com/judeharis/SECDA-LLM created 2026-06-03, labelled [WiP], 0 stars, only SystemC-simulation and cross-compile presets, no bitstream or board flow, so the paper results are not reproducible). SECDA-LLM stays as a one-sentence prose precedent for llama.cpp FPGA offload.
- Kept: DFX (MICRO), FlightLLM (FPGA), EdgeLLM (TCAS-I), Allo spatial (TRETS), TeLLMe (FPGA), StreamTensor (MICRO), CODO (ISCA), IMAX (IEEE Access), FlexLLM (arXiv but public repo with 32 stars).
- Public code (checked 2026-09-27): FlexLLM, Allo, TeLLMe, CODO artifact, IMAX3-LLM released; FlightLLM releases only a bitstream and profiler (RTL is Infinigence-AI IP); no released code found for DFX, EdgeLLM, StreamTensor (documentation site only).
- Feature split used in the paper: whole graph on FPGA vs per-kernel offload, and KV persisting on device vs host-managed KV. IMAX: neither (host runs tokenization, embedding, KV, softmax, RMSNorm, RoPE). CODO public decode kernel: neither (one block, no KV input).


## Archive layout and unread records (2026-10-09)

Each reference uses `assets/<slug>/citation.bib`; the BibTeX key equals the unchanged slug. Historical metadata is preserved verbatim in BibTeX comments. `note.md` exists only for recorded reading or targeted original-text checks. Original assets, versions, hashes and repository commits are preserved; this migration did not rerun paper eligibility screening.

[Migration gaps and reading-status conflicts](threads/archive-migration-gaps.md).

- [allo-2024](assets/allo-2024/citation.bib) — unread.
- [autodse-2022](assets/autodse-2022/citation.bib) — unread.
- [baqet-2025](assets/baqet-2025/citation.bib) — unread.
- [bench4hls-2026](assets/bench4hls-2026/citation.bib) — unread.
- [cd-llm-2026](assets/cd-llm-2026/citation.bib) — unread.
- [cgra-space-time-2025](assets/cgra-space-time-2025/citation.bib) — unread.
- [chatopu-2024](assets/chatopu-2024/citation.bib) — unread.
- [cstrans-opu-2024](assets/cstrans-opu-2024/citation.bib) — unread.
- [cxl-speckv-2025](assets/cxl-speckv-2025/citation.bib) — unread.
- `design-conductor-2-2026` — unread asset-only archive; [citation](assets/design-conductor-2-2026/citation.bib).
- [dllm-opu-2026](assets/dllm-opu-2026/citation.bib) — unread.
- [dtcore-2026](assets/dtcore-2026/citation.bib) — unread.
- [e2e-overlay-compiler-2025](assets/e2e-overlay-compiler-2025/citation.bib) — unread.
- [fast-prefill-2026](assets/fast-prefill-2026/citation.bib) — unread.
- [festal-2026](assets/festal-2026/citation.bib) — unread.
- [fet-opu-2023](assets/fet-opu-2023/citation.bib) — unread.
- [flame-2024](assets/flame-2024/citation.bib) — unread.
- `flexposit-2026` — unread asset-only archive; [citation](assets/flexposit-2026/citation.bib).
- [flightopu-2025](assets/flightopu-2025/citation.bib) — unread.
- [fmc-llm-2025](assets/fmc-llm-2025/citation.bib) — unread.
- [ftrans-2020](assets/ftrans-2020/citation.bib) — unread.
- [glitches-2024](assets/glitches-2024/citation.bib) — unread.
- [gpt4aigchip-2023](assets/gpt4aigchip-2023/citation.bib) — unread.
- [graphagile-2023](assets/graphagile-2023/citation.bib) — unread.
- [h2-llm-2025](assets/h2-llm-2025/citation.bib) — unread.
- [hbm-connect-2021](assets/hbm-connect-2021/citation.bib) — unread.
- [hls-codegen-benchmark-2025](assets/hls-codegen-benchmark-2025/citation.bib) — unread.
- [hlsfactory-2024](assets/hlsfactory-2024/citation.bib) — unread.
- [hlspilot-2024](assets/hlspilot-2024/citation.bib) — unread.
- [hlstransform-2024](assets/hlstransform-2024/citation.bib) — unread.
- [hummingbird-2025](assets/hummingbird-2025/citation.bib) — unread.
- [hummingbird-plus-2026](assets/hummingbird-plus-2026/citation.bib) — unread.
- [integer-fusion-2025](assets/integer-fusion-2025/citation.bib) — unread.
- [intrra-2025](assets/intrra-2025/citation.bib) — unread.
- [lembda-2026](assets/lembda-2026/citation.bib) — unread.
- [lightmamba-2025](assets/lightmamba-2025/citation.bib) — unread.
- [llamaf-2024](assets/llamaf-2024/citation.bib) — unread.
- [llm-aid-2024](assets/llm-aid-2024/citation.bib) — unread.
- [llm-on-fpga-2025](assets/llm-on-fpga-2025/citation.bib) — unread.
- [looplynx-2025](assets/looplynx-2025/citation.bib) — unread.
- [lora-2026](assets/lora-2026/citation.bib) — unread.
- [mcore-opu-2024](assets/mcore-opu-2024/citation.bib) — unread.
- [meadow-2025](assets/meadow-2025/citation.bib) — unread.
- [metal-2025](assets/metal-2025/citation.bib) — unread.
- [moe-opu-2025](assets/moe-opu-2025/citation.bib) — unread.
- [mpk-2025](assets/mpk-2025/citation.bib) — unread.
- [nyx-2025](assets/nyx-2025/citation.bib) — unread.
- [pcie-coarse-systolic-2025](assets/pcie-coarse-systolic-2025/citation.bib) — unread.
- [qllama-2025](assets/qllama-2025/citation.bib) — unread.
- [ranktuner-2024](assets/ranktuner-2024/citation.bib) — unread.
- [riscbench-2026](assets/riscbench-2026/citation.bib) — unread.
- [robot-llm-fpga-2025](assets/robot-llm-fpga-2025/citation.bib) — unread.
- [rtllm-2024](assets/rtllm-2024/citation.bib) — unread.
- [rtlrewriter-2024](assets/rtlrewriter-2024/citation.bib) — unread.
- [runtime-adaptive-transformer-2026](assets/runtime-adaptive-transformer-2026/citation.bib) — unread.
- [sanger-2021](assets/sanger-2021/citation.bib) — unread.
- [scalable-gpt2-2023](assets/scalable-gpt2-2023/citation.bib) — unread.
- [scalehls-2022](assets/scalehls-2022/citation.bib) — unread.
- `secda-autonomous-2026` — unread asset-only archive; [citation](assets/secda-autonomous-2026/citation.bib).
- `secda-dse-2026` — unread asset-only archive; [citation](assets/secda-dse-2026/citation.bib).
- [shuhai-2020](assets/shuhai-2020/citation.bib) — unread.
- [skipopu-2026](assets/skipopu-2026/citation.bib) — unread.
- [softermax-2021](assets/softermax-2021/citation.bib) — unread.
- [speedllm-2025](assets/speedllm-2025/citation.bib) — unread.
- [streaming-vpe-2024](assets/streaming-vpe-2024/citation.bib) — unread.
- [tapa-2023](assets/tapa-2023/citation.bib) — unread.
- [terafly-2026](assets/terafly-2026/citation.bib) — unread.
- [tflop-2026](assets/tflop-2026/citation.bib) — unread.
- [transformer-opu-2023](assets/transformer-opu-2023/citation.bib) — unread.
- `unison-2026` — unread asset-only archive; [citation](assets/unison-2026/citation.bib).
- [verilogeval-2023](assets/verilogeval-2023/citation.bib) — unread.
- [xtramac-2026](assets/xtramac-2026/citation.bib) — unread.

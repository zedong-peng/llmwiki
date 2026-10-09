---
title: "MPK: A Compiler and Runtime for Mega-Kernelizing Tensor Programs"
updated: 2026-10-09
---

# MPK: A Compiler and Runtime for Mega-Kernelizing Tensor Programs

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文、参考文献、Artifact Appendix）。图 9–13 为图中文字抽取，只有柱上标注的加速比，没有原始延迟数值；图中的 y 轴与柱高无法还原。

## Summary

问题：主流系统按 kernel-per-operator 执行，kernel barrier 阻碍跨算子 software pipelining、计算与通信的细粒度重叠，并带来数百上千次 kernel launch（靠 CUDA Graphs 缓解但较静态）。现有编译器（PyTorch、Triton、TVM）不支持端到端 mega-kernel，已有 mega-kernel（FlashDMoE、LLaMA-1B megakernel）靠手写（§1, §2.2）。

方法：MPK（Mirage Persistent Kernel）把多 GPU 模型推理自动编译成单个 persistent mega-kernel，由两部分组成。
- tGraph（§3）：SM 级任务图，节点是单个 SM 上的 task 与 event，task 与 event 交替连接，只在有数据区域重叠的 task 对之间建依赖。
- 编译器（§4）：按输出张量切分算子为 task；event fusion（successor-set / predecessor-set）；normalization（插入空 task，使每个 task 至多一个依赖 event 和一个触发 event）；linearization（BFS 排序，使一个 event 触发的 task 下标连续，只存首尾下标）；每个 task 的 CUDA 实现用 Mirage superoptimizer 在 thread block 级生成。
- 运行时（§5）：SM 分为 worker 和 scheduler（每 SM 4 个 scheduler warp），事件驱动，去中心化调度；混合 JIT/AOT 发射（attention 等耗时依赖数据的算子用 JIT，其后遇到全局 barrier 才转 AOT）；paged shared memory（页 32 KB）；跨 task 预加载流水；task 描述预取（每个 352 字节）。连续批处理与 paged attention 的调度逻辑也放进 kernel 内；为 2 的幂 batch size 各生成一个 tGraph。
- 实现：PyTorch 编译后端 `torch.compile(backend=MPK)`，约 44K 行 C++、42K 行 CUDA、10K 行 Python，通信用 NVSHMEM（§6.1）。

结果（§6）：
- 5 个模型（Qwen3-0.6B/1.7B/8B/30B-A3B、Llama-3.2-1B）× A100/H100/B200，batch 1–16，离线批推理（prompt 64，生成 1024 token），对比 PyTorch、vLLM、SGLang；MPK 相对最佳基线 1.0–1.7×，小模型和新 GPU 收益大（Figure 9）。
- Qwen3-8B 在 A100 上 per-token 延迟从 14.5 ms 降到 12.5 ms，论文估计的硬件下界为 10 ms（16 GB 参数 / 1.6 TB/s）。
- 多 GPU（H100 DGX，Qwen3-1.7B，张量并行）：相对 PyTorch 最高 10×；8 卡相对 SGLang/vLLM 1.1–1.4×（Figure 11）。
- MoE（Qwen3-30B-A3B，B200）：hybrid workload balancer 相对 SGLang MoE 算子 1.07–1.18×，并优于纯静态划分（Figure 10）。
- 消融：跨 task 流水使 Qwen3-8B 末层线性层快 1.2–1.3×（Figure 12）；计算通信重叠降低每轮延迟约 1.1×（Figure 13）；Qwen3-8B 每 token 293 次 launch，B200 上 eager 每次 3.8 µs，CUDA Graphs 每次 0.8 µs；in-kernel scheduler 占总运行时间 0.28%。
- 编译阶段（Table 2）：Qwen3-8B 293 个算子拆成 13,867 个 task，event fusion 使 event 数减少 37–118×，最终仅 1,142–2,366 个 event；linearization 使依赖存储缩小 4.4–15.0×（Qwen3-8B 从 110,932 B 到 18,928 B）；normalization 开销小于 1%。

## Evidence and Limits

- 评测只覆盖 LLM decode 服务，且为离线批推理、greedy decoding、batch ≤ 16；摘要和结论声称模型无关，但没有非 LLM 模型的结果。没有在线到达负载、长上下文、prefill 占比高的场景。
- 基线：vLLM、SGLang 用 FlashInfer / FlashAttention / cuBLAS / CUTLASS 等；论文说明 CPU 侧的 page 分配和请求调度是基线额外开销的来源之一，因此部分增益来自把这些逻辑搬进 kernel，而非 mega-kernel 本身。基线版本与配置细节正文未给出。
- MPK 配置（Table 1）：A100 108 SM（104 worker、16 scheduler warp），H100 132（128），B200 148（144）。
- 论文称 tGraph 里“没有 fork/join”，因为 QKV 投影已融合；normalization 在实测模型上基本未起作用，这一部分的正确性/收益没有被真实负载检验。
- 加速集中在 batch 小、模型小；大模型（Qwen3-8B、30B-A3B）在很多配置下只有约 1.0–1.2×。
- 寄存器数按全部 task 类型的最大值固定（§7），作者承认这是资源占用的例外。
- Figure 9 的相对性能只是比值，没有绝对吞吐表；未见误差棒或方差（附录写明取 5 次运行的中位数，预热 4 次）。
- 复现：附录给出 `tgx-osdi26-ae` 分支（commit 8b981a4）与 Zenodo 归档，脚本复现单卡延迟与消融；我没有运行任何东西。

## Open Questions

- 去中心化调度与 JIT/AOT 分类在高度动态负载（长序列混合、在线到达、投机解码）下是否仍然保持负载均衡，论文没有测。
- 增益中有多少来自 mega-kernel 本身，多少来自把 CPU 侧调度搬到 GPU 上？论文没有把两者单独剥离。
- 能否推广到 prefill 或 batch 更大的计算受限场景，以及 Mirage superoptimizer 生成的 task 实现在更大模型上是否持平 cuBLAS。

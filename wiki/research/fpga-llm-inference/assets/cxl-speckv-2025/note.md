---
title: "CXL-SpecKV: A Disaggregated FPGA Speculative KV-Cache for Datacenter LLM Serving"
updated: 2026-10-09
---

# CXL-SpecKV: A Disaggregated FPGA Speculative KV-Cache for Datacenter LLM Serving

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（11 页，含参考文献；无附录）。图 1–6 只有轴标签和零散数字可读，柱状/曲线本身看不到；表格文本基本完整。

## Summary

问题：LLM 解码时 KV cache 占满 GPU 显存，限制 batch size 与吞吐。例如摘要给出 LLaMA-2 70B、batch 32、2048 tokens 需要 640GB (§1, §3.1)。

方法：把 KV cache 放到 FPGA 挂载的 CXL 2.0 Type-3 内存池（64–256GB），GPU 侧保留三层结构 (§3.3.1)：L1 本地缓存 8–16GB、L2 预取缓冲 2–4GB、L3 CXL 池（4KB 页）。三个部件：
- Speculative Prefetcher：FPGA 上的小型 2 层 LSTM（输入最近 16 个 token，声称 128K 参数），预测后续 k=4–8 个 token，据此发起 DMA 把对应 KV 页搬到 L2 (§3.4, Algorithm 1)。
- FPGA Cache Engine：地址翻译、INT8 量化 + delta 编码 + RLE 压缩/解压流水线（20 级，51.2 GB/s/实例，Agilex-7 上 812 MHz），Intel HLS 与 Verilog 混合实现 (§3.5, Table 1: ALM 30.5%, DSP 25.9%)。
- 自适应策略：页迁移阈值、UCB 选 k、带宽反馈控制 (§3.3.3, §3.6.3)；通过 5K 行 C++ allocator 插件接入 vLLM / TensorRT-LLM (§3.6.1)。

主要结果（8×A100 80GB + 4×Agilex-7 + CXL 2.0，22 个模型配置，4 类 workload，5 次重复）：
- 吞吐：相对 GPU-only 2.1–3.2×（平均 2.4×）；LLaMA-2 70B chatbot 487 -> 1,549 tok/s（batch 16 -> 64）(§4.2, Fig. 1)。摘要和结论写的 3.2× 是最大值。
- 延迟：LLaMA-2 70B，decode +8.2%，P99 +12.3%，TTFT +4.2% (Table 2)；无预取的 CXL-NoSpec decode 23.5 ms，CXL-SpecKV 19.8 ms，GPU-only 18.3 ms。
- 预取：top-4 准确率 94–97%（Fig. 2），hit rate 94.7%，precision 87.2%，有效平均访问延迟 383 ns，miss 时 1,850 ns (Table 3)。
- 容量：batch 上限 16 -> 128（含压缩 384）(Table 4)；压缩 3.21×，perplexity +1.2% (Table 9)。
- 成本/能耗：成本归一化后 cost-performance 1.75×（8 GPU 时 2.2×）(§4.4.2)；J/token 0.647 -> 0.340 (Table 7)。8 GPU 并行效率 87% (Fig. 5)。

## Evidence and Limits

- 所有数字来自作者自己的平台，没有第三方复现；正文说有开源仓库（github.com/FastLM/CXL-SpecKV），但文中没有说明仓库是否含 RTL 或评测脚本。
- 基线：vLLM GPU-only、FlexGen CPU offload、NVMe offload、GPU INT8 压缩、自家 CXL-NoSpec。没有和其他 KV offload/压缩系统（如 KIVI、H2O 的实际运行结果）做对比，只在 related work 中口头称“互补”。
- 核心机制说不通或未说明：解码每步 attention 要读取位置 [0, t-1] 的全部 KV (§3.1)，这些在上一步已经确定，不依赖未来 token；论文却通过预测未来 token 来“预取 KV”，并未解释被预取的具体是哪些页、与“被预测 token 的 KV 尚未产生”如何自洽。Table 3/8 的 hit rate 与 token 预测准确率之间的换算也没有给出。
- 内部数字不一致：640GB 的 KV 估算与 §3.1 自己的公式不符（按公式 L=80, d_h=8192, B=32, S=2048, FP16 约 172GB）；Eq.(1) 的 80 cycles 在 800 MHz 下约 100 ns，却写作 “<10 μs”；128K 参数对应 FP16 应为 256KB，文中写 512KB；Table 4 中 4×64GB FPGA 却写 320GB 并称 8×；摘要“压缩最高 4×”而实测平均 3.2×；cost-performance 一处 1.75×、结论写 2.3×；Table 1 的 ALM 占用 284,563/933,120 约 30.5%，与描述一致，但 FPGA HBM 1.6 TB/s 与 CXL 链路 64 GB/s 之间的数据路径（GPU 经 PCIe Gen4×16 连 FPGA）未讨论，GPU 与 FPGA 内存“cache-coherent 共享”的实现也未说明。
- 精度只报 WikiText-103 perplexity 与“99.5% accuracy preservation”（摘要），没有下游任务结果；LSTM 在 22 个模型间如何训练/迁移（词表不同）没有说明。
- 局限（作者自述）：未覆盖 32K–128K 长上下文、多租户 QoS、CXL 3.0 等，列为 future work (§5)。上下文最长仅 2048+256 左右。

## Open Questions

- 预取到底作用于哪部分 KV？token 预测命中如何转化为 L2 命中，top-k 预测错误时代价有多大（Table 8 的 hit rate 随 k 单调上升，但未给出 token 级准确率与页级命中的关系）？
- 摘要给出的 640GB、128K 参数/512KB、320GB 等数字相互矛盾，实际实验配置与测得的容量究竟是多少？
- 在没有真实 CXL 2.0 GPU 一致性路径的现有硬件上，GPU 如何直接读写 FPGA 的 CXL 内存？评测是真实硬件测量还是模型/仿真？文中未交代。

---
title: "SkipOPU: An FPGA-based Overlay Processor for Large Language Models with Dynamically Allocated Computation"
updated: 2026-10-09
---

# SkipOPU: An FPGA-based Overlay Processor for Large Language Models with Dynamically Allocated Computation

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文 + 参考文献，无附录）。图 1–9 只有标题，图中数据读不到；Table 3 的列对齐有错位（部分单元格并排），按上下文推断。

## Summary

问题：SkipGPT 类动态计算分配（每层 MHA/FFN 前加一个线性 router，按 token 跳过子模块，跳过 token 的 KV 复用最近执行层的 KV）在算法上省 FLOPs，但此前没有在真实硬件上验证。作者指出三个障碍（§1, Fig. 1）：Gumbel-Softmax 路由与非线性算子造成长延迟；INT4 权重 + FP16 激活的混合精度使 DSP PE 利用率低；跨层 KV 复用造成不规则的 HBM 访问，打碎 AXI burst。

方法（AMD Alveo U280 上的 overlay processor，SystemVerilog 实现）：
- 融合数据流（§3）：把 RMSNorm / Softmax 的 reduction 与逐元素部分拆开，reduction 与 router 线性计算或 QK^T 并行增量完成（Softmax 用 FlashAttention 的在线更新），归一化与后续矩阵乘流水重叠；注意力把多个 head 打包以聚合 KV 访问。配套 tile-wise NPE，覆盖 Softmax、RMSNorm、SwiGLU、RoPE（§4.3）。
- 混合精度 PE（§4.2）：在已有 DSP overpacking 基础上截断尾数、利用 DSP pre-adder 与 C 口同时做"消除污染项 + 恢复截断信息"，每个 DSP 同时做两个 FP16 尾数乘法；累加改为 BFP（共享指数的定点加）+ 一次 FP 重构。PE 阵列 4096 DSP，每周期 64×128 次 FP16×FP16 或 FP16×INT4 乘法。
- KV 内存系统（§4.4）：按 token 把 KV 整条放到单个 HBM 端口，各 token 轮询分布；再用 512 个 URAM 组成 KV invariance buffer，利用"被跳过 token 的 KV 在重新激活前跨层不变"且 routing bitmask 可提前一层得知，后台预取/保留复用 KV，使 HBM 只读当前层新生成的 KV；并利用注意力的置换不变性省掉 reorder buffer。

结果：
- PE 单元对照（Table 1）：与 64 个级联 FP MAC IP 相比，LUT 约省 57.2%，误差更低（如经验分布下 FP16×FP16 误差 0.116% vs 0.490%）。
- 资源（Table 2）：LUT 98.85%，FF 63.99%，DSP 51.17%，URAM 53.33%。
- MHA 融合数据流（§5.3, Fig. 8）：prefill 阶段 PartialSkip 约 1.14×、KV reuse 约 1.29×、加融合数据流约 1.40×；decode 阶段融合收益随长度增加减弱。
- KV 有效带宽（§5.4）：稠密 KV 408.7 GB/s（峰值的 88.7%）；KV reuse + 标准交织映射最差只有 55.8%；token 级映射恢复到 360.2 GB/s；加 invariance buffer 后等效 467.8 GB/s，超过 HBM 物理上限。KV reuse 使 KV 数据量减少约 25%。
- 端到端（Table 3）：U280 上 llama2-7b、[128,1024] 归一化吞吐 143.4 token/s，带宽效率 88.4%/89.1%（两列，推测对应 7B/13B），对比 vLLM(A100) 31.5%、FlightLLM 66%、ChatOPU 72%/66%、MCoreOPU 70%、Chen 等 23%、DFX 34%，摘要据此称带宽效率高 1.23×–3.83×。

## Evidence and Limits

- 设置：Llama-2（7B、13B），按 SkipGPT 剪枝，跳过概率约 25%；权重 GPTQ 4-bit，KV 与激活 FP16；batch size 1；prefill 128/256/512/1024，decode 512/1024；核心 225 MHz，HBM 450 MHz（§5.1）。
- 全文没有任何精度/困惑度/下游任务结果。剪枝模型的质量完全依赖 SkipGPT 原论文，本文未验证 4-bit 量化 + 剪枝 + KV 复用组合后的精度。
- Table 3 的比较并不同口径：对手的模型各异（opt-350m、gpt2-345m、llama2-7b），精度各异（HF16、W8、SparseW8），其吞吐被"归一化到 7B、稠密 4-bit 权重"，归一化方法只一句话描述，无公式。SkipOPU 的吞吐含 25% 跳过带来的计算量减少，而带宽效率分母是"设计频率下可达最大带宽"，不同设计的分母定义可能不同，摘要的"1.23×–3.83×"数字没有逐项推导。
- 摘要称 "outperforms GPU"，但 GPU 对比仅 vLLM 在 A100 一项，且 A100 的绝对吞吐（181.2 归一化）高于 SkipOPU（143.4/144.5）；优势只体现在带宽效率这一比值上。
- "467.8 GB/s 超过 HBM 物理上限"是把片上 URAM 命中的字节计入有效带宽，属于等效口径；该数字依赖连续层都做注意力的占比，文中称该情形"最常见"，但未给出跳过模式的统计。
- 摘要的"最多减少 25.4% KV 存储"在正文只出现为"约 25%"，没有按序列长度展开的表或图（图数据不可读）。
- Fig. 8 的数值只在文字中给出，没有误差线、没有与 GPU 上同样的 SkipGPT 实现对比（作者提到 GPU 对控制密集的路由效率低，但未测）。
- 未提供代码地址；没有复现信息，Vivado 2020.1 实现的频率、功耗未报告（功耗/能效未出现）。
- 作者自述局限：仅 batch 1 边缘场景；跳过 MHA 的非连续层情形下 invariance buffer 失效，带宽退回到 83.1% 物理利用率。

## Open Questions

- 在 GPU 上以同样 SkipGPT 路由、同等量化设置做对比，吞吐与能效差距有多大？目前的对比对象并非同一工作负载。
- 精度：25% 跳过 + W4 + KV 复用的联合损失多少？更高跳过率下非连续注意力层增多，invariance buffer 的收益如何衰减？
- 1024 token 的 KV 容量（512 URAM）限制了 buffer 覆盖长度；更长上下文下命中率与带宽收益如何变化，文中未说明。

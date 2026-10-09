---
title: "Allo: A Programming Model for Composable Accelerator Design"
updated: 2026-10-09
---

# Allo: A Programming Model for Composable Accelerator Design

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：正文全文（§1–§10）及参考文献前半部分；补充材料 A–D（类型定义、定理证明、完整示例、systolic array 的 HLS 代码）文中仅被引用、未读到。Fig. 12 的柱状图数值由文本抽取，Fig. 14 左图（延迟曲线）无数据，只有正文给出的汇总数字。

## Summary

问题：HLS 要靠大量源码重构才能出好性能，现有 ADL 多针对单 kernel，面对多 kernel 层次化设计时往往展平成一个整体，丢失模块边界（§1, §3）。§3 用 1024×1024 GEMM 举例：只加 pragma 不够，需把 j/k 循环交换成 row-wise product，延迟从 25074 ms 降到 112 ms，II=1（Fig. 2）；两个 GEMM 级联时，因函数接口的 partition 不一致，HLS 复制出两份 kernel，延迟 280 ms 而非预期 224 ms（Fig. 3）。

方法（Python 嵌入的 ADL + MLIR Allo dialect）：
- 把 compute / memory / communication / data type 的定制拆成 primitive（Table 2，如 split、reorder、buffer_at、reuse_at、partition、relay），每个 primitive 是一次 program rewrite，可逐步验证；验证用 CPU 仿真加等价性检查器（要求静态可解释控制流，§5.2）。
- 参数化 kernel 模板（§5.3）。
- `.compose()` 自底向上合并各子 schedule，做 schedule replay 并检测冲突（Algorithm 1）；保留函数边界的 hierarchical dataflow graph（§6.2）。
- 把数组 partition 方式建模成带子类型关系的格（lattice），在 dataflow graph 上用 worklist 做 partition 类型推断，声称 O(M) 终止（Algorithm 2, Theorem 6.1）；类型系统会拒绝 Fig. 3 那种接口不一致的调用。
- 按生产/消费速率公式推导 stage 之间的 FIFO 深度（§6.5）。
- 后端生成 HLS C++ 或 LLVM IR；PyTorch 前端（torch.compile）可直接导入 TorchVision / HuggingFace 模型（§7）。

结果（U280，Vitis HLS 2022.1，综合 300 MHz，上板 250 MHz，§8.1）：
- PolyBench：相对 Vitis HLS 基线最高 1099×；相对 ScaleHLS 最高 1478×，HeteroCL 34×，PyLog 837×，Merlin 775×，Dahlia 1405×（§8.2）。Table 3 选了 5 个 Allo 明显占优的 kernel，如 symm 延迟降 427.4×，DSP 用量升 201.3×。
- CNN：相对 ScaleHLS 加速 7.4×（VGG16）、8.3×（MobileNet）、12.7×（ResNet18），BRAM 为 0（Table 4）。
- GPT2（355M，W4A8）：相对 DFX 最高 2.80× 加速，DSP 1780 对 3533，BRAM 384 对 1192（Fig. 14）；输出序列较长时相对 A100 快 1.70×，相对 1080Ti 快 5.05×；实测功耗 30 W 对 96 W，能效 5.44×（§8.3.2）。定制代码少于 50 行。

## Evidence and Limits

- 论文主张 Allo 在单 kernel 与多 kernel 上都优于现有 HLS/ADL，并首次在 FPGA 上完整评测 LLM。PolyBench 与 CNN 对比有表有数，但 Allo 与 HeteroCL、PyLog、Dahlia 的方案是作者手写最优 schedule，ScaleHLS 用其自带 DSE，Merlin 自动插 pragma，对比并不对等，且 Allo 的数字含人工调优。Table 3 只挑了 Allo 大幅领先的 5 个 kernel。
- GPT2 上所有基线 ADL 都无法生成可用设计，因此只能与手写 SystemVerilog 的 DFX 比。DFX 用 fp16 且频率 200 MHz，Allo 用 W4A8 且 250 MHz，量化精度不同，文中只说"与 PyTorch 量化模型核对以保持精度"，未给精度数字，也未说明 DFX 数据是复现还是引用。
- GPU 对比：GPU 取最佳 fp16 性能而非低比特；单 batch 低延迟场景；输出序列短时 FPGA 明显落后（prefill 更适合 GPU），优势只在长输出序列。1.70× 与 5.44× 都是该有利区间的数字。功耗为 xbutil 实测板卡功耗，GPU 功耗的测法文中未说明。
- 文中承认的局限：大设计在 multi-die FPGA 上布线困难、频率受限；FIFO 尺寸算法只消除"生产快于消费"一类停顿；缺自动 schedule、自动 bufferization；FIFO 连接位置需用户指定；等价性检查要求静态控制流。
- 编译时间、代码行数只给了 Table 3 中 5 个 kernel，且对比 ScaleHLS 的编译时间只含 HLS 代码生成。

## Open Questions

- 手写 schedule 与自动 DSE 的比较中，Allo 的优势有多少来自 primitive 表达力，多少来自人工专家知识？论文没有给出同等人工投入下的对照。
- GPT2 上 Allo 与 DFX 的差距有多少来自量化（W4A8 对 fp16）而非编程模型本身？
- 长序列才优于 GPU 的结论能否推广到更大模型、更大 batch？文中只测了 355M 的 GPT2 与 batch=1。

---
title: "ScaleHLS: A New Scalable High-Level Synthesis Framework on Multi-Level Intermediate Representation"
updated: 2026-10-09
---

# ScaleHLS: A New Scalable High-Level Synthesis Framework on Multi-Level Intermediate Representation

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文、参考文献）；图（Fig. 7 的曲线、Fig. 8 的柱状图）只有图注，数值读不到；Table III 至 V 可读。

## Summary

问题：现有 HLS 工具基于 LLVM、C AST 等单层抽象，难以处理含大量子模块的大型设计。作者归纳出三点困难：表示（单层 IR）、优化（任务级并行、loop 变换靠手写改代码）、探索（各优化相互耦合，需要全局 DSE）(§I)。

方法：ScaleHLS 建在 MLIR 上，分三层 IR (§IV)。
- Graph-level：复用 ONNX-MLIR 的 onnx dialect。
- Loop-level：用 MLIR 内置的 affine/scf dialect。
- Directive-level：自定义 hlscpp dialect，用 attribute 表示 pipeline/dataflow/II，用 affine map 编码 array partition，用 memory space 表示 resource。

每层有对应的 pass 库 (§V, Table II)。
- Graph 层：legalize-dataflow（可选插入 copy 节点）、split-function（min-gran 控制粒度）。
- Loop 层：perfectization、loop order、remove-variable-bound、tiling、unroll。
- Directive 层：loop/function pipelining、基于访问下标距离的 array-partition。

另有一个解析式 QoR estimator（ALAP 调度，估计 latency 与资源），以及 5 步 neighbor-traversing DSE：随机采样、从 Pareto 前沿选点并提出最近邻、评估、更新前沿、选满足资源约束且 latency 最小的点 (§V-E)。作者依据 Fig. 6 的 PCA 观察，认为 Pareto 点在设计空间中成簇。前端是基于 Clang 的 HLS C 到 scf，再 raise 到 affine。后端是可综合 C++ emitter (§VI)。下游工具为 Vivado HLS 2019.1。

结果：
- PolyBench 六个 kernel，规模 4096，目标 XC7Z020。相对未优化原始 C 的加速为 41.7x（BICG）到 768.1x（GEMM）(Table III)。
- GEMM 案例：DSE 设计 1.610e9 cycles，作者称达到理论界的 0.97x（原文如此），比手工优化设计（2.684e9 cycles）快约 1.67x。DSE 用时数分钟，手工设计用了约 10 小时 (Table IV)。
- ResNet-18、VGG-16、MobileNet（CIFAR-10，PyTorch 输入）在 VU9P 的单个 SLR 上，相对"同样经 ScaleHLS 编译但不做多层优化"的基线，吞吐提升 1505.3x 到 3825.0x，优化耗时 37.3 到 60.8 秒 (Table V)。
- DSP 效率（OP/Cycle/DSP）为 0.744 到 1.343，TVM-VTA 为 0.296 到 0.468。
- 消融（Fig. 8，文字描述）：directive、loop、graph 优化平均分别贡献 1.8x、130.9x、10.3x。

## Evidence and Limits

- 所有数字来自 Vivado HLS 的综合报告（latency 与资源估计），没有上板实测，也没有 RTL 级仿真或布局布线后的频率。
- 加速比的基线都是"未优化"设计：PolyBench 原始 C，或 DNN 的未做多层优化版本。基线很弱，倍率主要说明优化管线有效，不能直接比较绝对性能。
- 与已有 DSE 工作（[17]–[19]）的比较只有文字：Comba [19] 在这六个 kernel 上要么生成无法综合的方案，要么耗时过长。没有表格或数字对比，也没有与 AutoDSE 等综合式方法的定量比较。
- 与 TVM-VTA 只比 DSP 效率，平台与量化精度不同，文中没有说明 DNN 的数据类型（kernel 为 32-bit float），可比性有限。DNN 只用了 CIFAR-10 规模的模型，没有给出精度、频率、绝对延迟。
- QoR estimator 的精度没有在正文中单独评估，仅说明"准确建模"。DSE 的 Step1 是随机采样，结果的随机性与方差没有报告。
- Table III 中 BICG 的 pipeline II 为 43，说明部分 kernel 受循环携带依赖限制，DSE 只能靠提高并行度换取加速。
- 作者自己列出的未来工作：IP 集成、更好的 DSE 算法、基于 ML 的 QoR 估计、MLIR 内直接生成 RTL。
- 代码已开源：https://github.com/hanchenye/scalehls（脚注），bib 中为 UIUC-ChenLab/scalehls。

## Open Questions

- 解析式 QoR estimator 与真实综合结果的偏差有多大，DSE 选出的"最优点"在实际综合后是否仍然最优？文中没有给出。
- 面对依赖复杂或访存不规则的程序（非 affine 循环）时，multi-level 流程能保留多少收益？文中只处理了 affine 为主的 kernel 与 CNN。
- DNN 结果缺少与强基线（手写或其他编译器生成的加速器）的绝对性能对比，DSP 效率优势是否能在同精度、同平台下成立，尚不清楚。

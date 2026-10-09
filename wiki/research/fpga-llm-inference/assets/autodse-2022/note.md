---
title: "AutoDSE: Enabling Software Programmers to Design Efficient FPGA Accelerators"
updated: 2026-10-09
---

# AutoDSE: Enabling Software Programmers to Design Efficient FPGA Accelerators

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文、参考文献、附录 A.1 代码清单与 A.2 说明）。图 5、6、7 只剩图注和坐标残片，柱状图数值读不到，只能用正文给出的几何平均数。

## Summary

问题：HLS 之后，软件程序员仍要手动改写代码并调 pragma 才能得到高性能 FPGA 设计；设计空间巨大（Code 1 的 CNN 仅 pipeline/unroll/array partition 就有约 10^20 个点），非单调，HLS 工具行为难以建模，单次综合 5–30 分钟（§1, §2）。

方法：把 HLS 工具当黑盒，后端用 Merlin Compiler（OpenMP 风格的 parallel / pipeline(cg|fg) / tiling 高层 pragma，自动做 burst、coalescing、double buffering），只搜索剩下的"最后一层"优化（§4.1）。核心是 bottleneck-guided coordinate optimizer（§5.2, Algorithm 1）：
- 利用 Merlin 把 HLS 周期报告回传到用户源码的能力，DFS 建层级路径并按延迟排序，判断瓶颈是访存还是计算，每轮只调与该语句对应的少数参数，而不是像普通 coordinate descent 那样每轮评估全部 K 个参数。
- 用 finite difference（式 5，面积项用 Σ 2^{1/(1-u)}，式 6）评价候选点，兼顾周期下降与资源消耗。
- 参数顺序启发式：计算瓶颈时 fg pipeline、parallel、cg pipeline；访存瓶颈时 cg pipeline 优先于 tiling（§5.3，Table 4）。
- 用 Python list comprehension 表示带互斥规则的网格设计空间（§5.4）；按 pipeline 模式做树形划分，再用 K-means 选出 t 个代表分区并行探索（§5.5）。

结果（AWS F1，VU9P）：
- MachSuite + Rodinia 的 11 个 kernel 加一层 AlexNet 卷积：相对单核 CPU 几何平均 19.9×，约为手工 Merlin pragma 设计的 0.93×，平均搜索 1.1 小时（§6.2）。相对无 pragma 的 Merlin 为 182.92×；原始 coordinate descent 为 13.52×，再加 list 表示与划分多 2.47×，瓶颈优化再多 5.5×。
- 与已有 DSE 同等时间比较：S2FA 3.6×、lattice-traversing 4.3×、GP-based Bayesian 17.9×（几何平均，各方法只覆盖部分 kernel，Table 5）。
- 33 个 Xilinx Vitis 视觉库 kernel：去掉六类优化 pragma（平均 14 个里去掉 13.47 个），AutoDSE 平均自动插入 3.2 个 Merlin pragma，性能为原手写库的 1.04×，pragma 减少 26.38×，平均 0.3 小时（§6.4, Table 6）。

## Evidence and Limits

- 论点"软件程序员可用"的证据是 pragma 数量减少，没有用户研究；"每个 kernel 少于 1 个 pragma"是因为保留了 DATAFLOW、STREAM、INTERFACE、LOOP_TRIPCOUNT，这些不在 Merlin 搜索范围内（§6.4）。
- 依赖 Merlin 的周期回传和 HLS 报告的周期精度。正文承认含 unbounded loop / while loop 的 kernel 周期估计不准，瓶颈分析会盯错参数，这是没追平手工设计的原因之一；Vitis 中 histEqualize、histogram、otsuthreshold 因 Merlin 无法设置 II 而落后。
- 以 HLS 综合结果而非 P&R 结果评价 QoR（结论部分），资源阈值固定 0.8；最终实现的频率与实际板上结果的关系没有展开。
- 摘要说"与手工设计相差 7%"，对应 0.93×；比较基线是作者自己用 Merlin pragma 手写的设计，不是独立专家设计。与他人方法的比较是复现或对方作者协助（致谢），且只覆盖部分 kernel；Lattice 方法只考虑 unroll 与 inline。
- 参数顺序（fg 先于 cg）自称为启发式，不能推广，依据只有 Table 4 的一个例子。
- 附录 A.1 的 CNN 例子：28 个 HLS pragma 手写版得 7,041×，Merlin 4 行 pragma 达到同等性能（§4.1）。
- 代码与 Merlin 在文中均称"将开源"。设计空间剪枝"平均 24.65×"出现在结论，正文未见推导。

## Open Questions

- Merlin 的高层 pragma 集合固定后，搜索空间已大幅缩小；有多少增益来自 Merlin 本身、多少来自 DSE，文中只在 Vitis 实验里拆分（Merlin 3.29× vs AutoDSE 9.04×），MachSuite 上的拆分有限。
- 搜索结果对 HLS 工具版本和 FPGA 型号的可移植性没有实验验证，只有论述。
- 对于周期报告不准的 kernel（动态循环边界），瓶颈分析会退化到什么程度，没有量化。

---
title: "Monomorphism-based CGRA Mapping via Space and Time Decoupling"
updated: 2026-10-09
---

# Monomorphism-based CGRA Mapping via Space and Time Decoupling

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（6 页会议论文，含参考文献）。图 2–5 为文本抽取，仅能看到节点标签；Table III 抽取基本完整，可读。无附录。

## Summary

问题：CGRA（粗粒度可重构阵列）上的 modulo scheduling 映射，即把循环的 DFG 的每个节点指派到某个 PE 和某个时间步，目标是最小的 II（Iteration Interval）。现有启发式方法和精确方法（ILP/SAT，如 SAT-MapIt）在大阵列上扩展性差（§I, §II）。

方法（§IV）：把时间和空间解耦，分两步。
- 时间：用 SMT（Z3）在 Kernel Mobility Schedule 上求调度。在 SAT-MapIt 的 modulo scheduling 约束之外新增两类约束：capacity（每个时间步上的节点数不超过 PE 数）和 connectivity（同一时间步上某节点的邻居数不超过 PE 连接度 D_M）。
- 空间：调度确定后，每个节点带有时间标签，在 MRRG（II 层 CGRA 堆叠图）中做 monomorphism（子图单射匹配，用 VF3 类算法 [29][30]）求 PE 放置。
- 理论（§IV-D）：证明只要时间解满足 capacity 与 connectivity 约束，MRRG 中必存在 monomorphism，即空间搜索不会因时间解而无解。

结果（§V, Table III）：2×2、5×5、10×10、20×20 四种 CGRA，17 个 MiBench/Rodinia 最内层循环，对比 SAT-MapIt，超时 4000 s。68 个实验中本方法求得 62 个解；其中 57 个与 SAT-MapIt 的 II 相同，5 个 SAT-MapIt 超时而本方法有解，1 个本方法空间搜索超时而对方不超时。平均编译时间加速（排除任一方超时的样例）依次为 30.85×、103.76×、887.84×、10288.89×。Fig. 5 显示 aes 上 SAT-MapIt 的编译时间随阵列增大而增长，本方法基本持平。

## Evidence and Limits

- 声称“映射质量与 SOTA 相当、编译速度显著更快”。证据主要是对 SAT-MapIt（同一组作者的前作）的单一对比，指标为 II 与编译时间。Table III 抽取后列对齐有些模糊（II 列究竟属于哪个工具文中未逐列说明），故 II 的逐样例结论以正文 57/5/1 的统计为准。
- 平均加速倍数是逐样例比值的平均，受 20×20 下极端样例（susan 35377.91×、gsm 18722.88×）拉高；超时样例（20×20 下 aes、backprop、heartwall、particlefilter、sha1 对方超时）被排除，故平均值低估了对方的失败情况，同时也无法反映本方法自身的超时。
- 小阵列下并非总是更快：2×2 的 basicmath、sha1 的编译时间差值为正（本方法更慢），nw、sha2 在 5×5 上空间搜索耗时数秒。
- 其他基线（CRIMSON、PathSeeker、HiMap 等）没有对比；理由是 SAT-MapIt 此前被证明优于同类，属于转述而非本文实验。
- 硬件假设（§V-3，作者明确承认）：每个 PE 都能读取邻居 PE 的寄存器文件。这一假设使解耦成立（证明依赖它），但增加硬件复杂度，适用范围受限。
- 实验平台：3.30 GHz Intel Core i9，256 GB 内存，Z3；基准只含无函数调用、无条件语句的最内层循环，DFG 规模 7–57 个节点。
- 代码：正文未给出代码地址。

## Open Questions

- 当 PE 不能直接读取邻居寄存器（需要显式路由节点）时，connectivity/capacity 约束是否仍足以保证 monomorphism 存在？论文仅列为未来工作。
- 解耦后时间解不一定是空间最优的；II 是否因此在更大或更复杂的 DFG（含条件分支、函数调用）上系统性劣于联合搜索，文中没有给出数据（Table III 只显示大阵列上对方超时而本方法有解的情形）。
- 20×20 下本方法的空间搜索仍可能耗时很长（如 particlefilter 的 Space 为 141.54 s、nw 在 10×10 为 10.25 s），monomorphism 搜索本身的复杂度随 DFG 与阵列规模的增长趋势未被分析。

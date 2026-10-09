---
title: "RankTuner: When Design Tool Parameter Tuning Meets Preference Bayesian Optimization"
updated: 2026-10-09
---

# RankTuner: When Design Tool Parameter Tuning Meets Preference Bayesian Optimization

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（7 页，含参考文献）。图 4 的坐标轴与曲线为乱码式提取，只能读到图例和少量刻度；表 2、3 数值完整可读。无附录。

## Summary

问题：EDA 工具（Genus、Innovus）的参数空间巨大（引言引用 [2] 称组合数可超过 10^70），现有方法把调参当作回归任务预测 QoR（功耗、性能、面积），样本少时回归不准，Pareto 支配关系容易判错（§1，图 1）。

方法：RankTuner 不回归绝对 QoR，而是直接学习两个参数配置之间的 Pareto 支配关系（§3）。
- Pairwise GP（§3.2）：沿用 Chu & Ghahramani 的 preference learning，假设潜函数 f 与真实支配关系之间有方差为 σ² 的高斯噪声，得到成对似然 Φ(z)，后验用 Laplace 近似，预测 p(x_r ⪰ x_s | D) = Φ((μ_r − μ_s)/σ*)。
- 采集函数 Duel-Thompson sampling（§3.3）：先用连续 Thompson 采样得到 f̃，选取 soft-winner 得分 ∫π(x,x')dx' 最大的 x_next（利用）；再选使 σ(f*) 方差最大的 x'（探索），组成下一对比较。
- 沿用 REMOTune [1] 的 random embedding + trust region 降维并支持并行搜索，另用前端（综合）QoR 做多保真过滤，再跑后端（图 2）。

实验（§4）：搜索空间约含综合 105、floorplan 7、global placement 10、detailed placement 3、routing 9 个参数（表 1）；基准为 RISCV32I（7.6k cells）和 Rocket（14.2k cells），TSMC 65nm；指标为 HV（参考点 [150,150,150]）及 MPI/MAI/MPPI/MPAI。对比 FIST、DAC'19、MLCAD'19、ICCAD'21、PTPT、REMOTune、DATE'24。
- RISCV32I（表 2）：HV 1.84e5，REMOTune 1.75e5，次优；文中称比最佳基线高 4.89%。
- Rocket（表 3）：HV 1.67e5，REMOTune 1.61e5；文中称高 3.59%。
- “最高 40.34% HV 提升”对应 Rocket 上对 DAC'19（1.19e5）的差距，并非对最强基线。
- 运行时间（图 4c）：比 REMOTune 慢 1.30×，比 PTPT 快 4.83×（归因于并行探索）。

## Evidence and Limits

- 只有两个 RISC-V 小设计、一个工艺节点，未见多次随机种子、方差或显著性检验；基线沿用 [1] 的环境与实现，但未说明每种方法的评估预算。
- 文中称“在所有基准上一致优于所有方法”，但表中并不成立：RISCV32I 上 MAI（5.12 vs REMOTune 7.45）、MPI2（5.04 vs 6.27）、HV1,2（3.00 vs 3.23）均不如 REMOTune；Rocket 上 MPI1（13.00 vs ICCAD'21 的 16.72）、HV0,2（3.06 vs 3.18）、MPPI、MPAI（6.68 vs 15.01）也落后。只有 HV 总量和部分子 HV 领先。
- 核心论点“排序模型比回归更能预测 Pareto 关系”仅由端到端 HV 间接支持，没有消融：未单独比较 pairwise GP 与回归 GP（同一套 random embedding/trust region/多保真），也未分离 Duel-Thompson 与其他采集函数的作用。因此提升可能来自与 REMOTune 共享组件之外的任何差异，无法判定。
- 图 1 的“低 MSE 但 Pareto 错误”只是示意图，不是实测。
- 文字不一致：正文出现“Rank-DSE”“architectures”等残留用词；公式 (4) 下 z_k 的定义印刷有误；参考文献 [15] 与 [21] 重复；Duel-Thompson 的细节（候选集如何离散化、积分如何数值计算、σ 如何估计、批大小、迭代次数、初始样本数）均未给出。
- 未提供代码链接，复现需自行重写。

## Open Questions

1. 在相同 random embedding/trust region/多保真框架下，pairwise GP 相对回归 GP 的 HV 增益是多少？
2. 成对比较的数量随样本数平方增长，Laplace 近似的 GP 在更多样本或更大设计上的开销和精度如何？
3. 不同随机种子下结果是否稳定？Rocket 上 MPAI、MPPI 落后是否说明对部分目标组合的偏向？

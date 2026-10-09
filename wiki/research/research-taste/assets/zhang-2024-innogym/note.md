---
title: "InnoGym: Benchmarking the Innovation Potential of AI Agents"
updated: 2026-10-09
---

# InnoGym: Benchmarking the Innovation Potential of AI Agents

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：正文全文及附录 A–G（局限、iGym、任务表、统计检验、novelty 度量验证、基准构建）；附录 H/I 的 prompt 文本仅浏览目录，未细读。图（Fig. 5/6）只有文字说明，具体曲线数值不可见。

## Summary

问题：现有 agent 基准只看答案是否正确，不看方法是否有新意。论文把任务形式化为 T=(P,S,V,D)，V(s)=C(s)·R(s)（可行性×目标得分），D 为解之间的方法距离，并定义两个指标（§2）：
- Performance gain G(s)=V(s)−V*_known，相对已知最优解的提升；
- Novelty N(s)=C(s)·min_{h∈S_known} D(s,h)，与已知解的最小距离，仅对可行解计算。
按 (G,N) 区域分为 breakthrough（高 G 高 N）、performance、conceptual（G≈0 高 N）三类创新；任务按 S_known 状态分为 solved / improvable / exploratory，iBench 只收 improvable。

基准 iBench：从 2018–2024 年竞赛与经典 NP-hard 问题的 197 项出发，经资源可得性与可负担性筛选剩 72 项，再经评估器验证与领域平衡得到 18 个任务（§3.1，Fig. 2）。每个任务补充任务说明、环境、validator、参考解（经 Codex 抽取成 summary 与伪代码）、归一化 evaluator（对 ROADEF 等相对分数做绝对化，要求与榜单 Pearson≥0.9、Kendall-τ≥0.8）、dev/eval 划分（§3.2）。iGym 是统一的 agent 执行 SDK，支持异步 Tool Dispatcher、断点恢复、并发（§3.5，附录 C）。

距离 D 的实现：Codex 抽取方法摘要，GPT-5 按六个维度各打 0–4 分，取平均后缩放到 0–100，对所有参考解取最小值（§4.1，附录 F.1）。

实验（§4）：10 个主任务，3 个 scaffold（MLAB、CodeAct、AIDE），骨干 DeepSeek-v3.1，每配置 12 小时上限、跑 3 次取有效提交中的最好值。Table 2 结果：没有任何 agent 超过人类 SOTA；CDML 和 PTTALC 上所有 agent 都无有效提交；平均 gain，MLAB −24.32、CodeAct −41.58、AIDE −42.68（各自只在有有效提交的任务上平均）；平均 novelty 56.55 / 54.86 / 46.67。作者据此得出"瓶颈是鲁棒性而非点子"（RCIC、TrojanDetection 上 novelty 中高但得分最低）。
Circle Packing 上的分析（§4.3）：AIDE 从 Gemini-2.5-Pro 初解出发迭代，G 上升、N 先升后降；随运行时间 G 增、N 降；换更强骨干分数更高（Gemini-2.5-Pro 2.49，GPT-5 2.44，DeepSeek-v3.1 2.40，AlphaEvolve 2.65）；温度 0.5–0.75 时性能与新颖度折中最好。

## Evidence and Limits

- 主结论"agent 与人类 SOTA 差距大"有 Table 2 支撑；但 Table 2 的平均值只覆盖有有效提交的任务，各 agent 的任务集合不同，不可直接比较。附录 E.2 用悲观填补（R=−1,N=0）重算：R 为 MLAB −0.62、CodeAct −0.81、AIDE −0.82（Table 4）；MLAB 在 R 上显著优于另两者（p=0.035、0.007），N 的差异均不显著（p=0.13–0.58，Table 5）。因此正文"MLab 在 gain 与 novelty 上均领先"中 novelty 部分只是描述性趋势。
- "鲁棒性比新颖度更重要"的推断较弱：novelty 是对最终提交打分，失败多为无有效提交（Table 6，多数任务成功率 0–33%），并未单独检验"有好点子但实现失败"；N 的置信区间很宽（如 MLAB 22–56）。
- 显式提示创新的实验（Table 7，仅 AIDE、3 个任务）：BEETL(Sleep) 与 CirclePacking 的 novelty 上升，但 OAG 从 70.83 降到 50.00，而文中说"改善了 novelty"；gain 三项均下降。基线 CirclePacking novelty 在 Table 7 为 35.33，Table 2 为 33.33，未解释。
- 新颖度度量依赖 LLM judge（Codex 抽取 + GPT-5 打分），验证规模很小：EquiBench 50 个三元组上均值 9.75 对 1.00，仅 8 个有人工标注（3 名研究生），与人一致 6/8；跨范式 3 个三元组各 1 名博士生，相关系数 1.00/0.99 在 n=3 下意义有限（附录 F，Table 8–12）。EquiBench 人工分的 (A,C) 全为 0 时相关系数未定义，已在表注说明。该度量只测"与已知解的距离"，S_known 有限（每任务 1–7 个，ROADEF 三项仅 1 个，Table 3），作者在附录 B 承认会带来偏差。
- 只在 18 个任务中的 10 个上评估，其余 8 个因算力与环境依赖未跑；每配置只 3 次，取最好值，且只用一个主骨干模型。Circle Packing 的骨干对比只有该任务。
- 文中把 GPT-5 称为"hypothetical"，疑为笔误；Fig. 6 数值只能从文字读到。
- "first benchmark"的说法未对 MLR-Bench、InnovatorBench 等做实质对比，Table 1 只列了是否评 novelty。
- 代码与数据：作者称已在 GitHub 开源（https://github.com/zjunlp/igym）；本文未复现。

## Open Questions

1. 方法距离由 LLM 在摘要上打分，是否对表述风格、摘要长度敏感？对 novelty 与"有效创新"（gain 为正）的相关性，论文没有给出直接验证。
2. 在多数配置只有 0–1 个有效提交的情况下，N 的跨 agent 比较是否有统计意义？更多 run 或把失败 run 的方法单独打分会否改变"鲁棒性是瓶颈"的结论？
3. 在 G 全为负的区间，(G,N) 分类中的"conceptual innovation"（G≈0）几乎无样本，该分类框架能否在当前 agent 上实际使用？

---
title: "Defining and Identifying Sleeping Beauties in Science"
updated: 2026-10-09
---

# Defining and Identifying Sleeping Beauties in Science

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文与 SI Appendix，共 40 页）。图中曲线与词云仅有提取出的坐标残片，Fig. S11 只有图注；表格基本可读。

## Summary

Sleeping Beauty (SB) 指长期沉睡后突然被大量引用的论文。此前的定义（van Raan 的睡眠长度/深度/唤醒强度，Glänzel 等，Redner 的 pre-1961、>250 引用、平均引用年龄比>0.7）都依赖人为阈值，数据集小或限于单一学科，因而得出"SB 很罕见"的结论。本文提出无参数指标 beauty coefficient B，并在 APS（384,649 篇有引用论文）和 WoS（22,379,244 篇）上统计。

方法 (§I)：设论文第 t 年引用数为 c_t，峰值在 t_m。参考线 ℓ_t 连接 (0, c_0) 与 (t_m, c_{t_m})，
B = Σ_{t=0}^{t_m} (ℓ_t − c_t) / max{1, c_t}（式 2）。早期引用被分母惩罚；c_t 沿直线增长时 B=0，凹增长时 B<0。唤醒年 t_a 取使 (t, c_t) 到参考线距离最大的 t（式 3）。

主要结果：
- APS 上 Redner 的 12 篇 revived classics 中 6 篇进入本文 top 10，其余 6 篇排名在 B 的第 45 到 218 位之间（§II.A, Table S1）。EPR 论文在 APS 与 WoS 中都靠前。
- B 的分布连续、跨多个数量级，无典型值，无天然分界；APS 尾部幂律拟合 α=2.35，B_min=22.27（Fig. 3）。APS 与 WoS 分布形状相近，仅截断不同。APS 4.68%、WoS 6.56% 的论文 B 为负。
- 两个基线模型，citation network randomization (NR，保持入/出度与时间顺序的链接交换) 和 preferential attachment (PA)，生成的 B 分布范围小得多，NR 最大 B=30（§II.C, Fig. 3, §S4）。
- WoS top 15 多为化学/物理，另有统计（Pearson 1901，Wilson 1927）。Table I 最高 B=11600（Freundlich 1906，2002 年唤醒）。社会科学也有大量 SB（Table S4，如 Stroop、Zachary、Garfield 1955）。
- 学科：top 0.1% 中占比最高的是 physics multidisciplinary 7.6%、chemistry multidisciplinary 7.5%、multidisciplinary sciences 7.4%（Fig. 4）。
- 唤醒触发：Garfield 1955 和 Zachary 1977 的案例中，唤醒与另一学科社群的发现相关（co-citation 分析，Fig. 5, S12）。top 1000 SB 中约 80% 有 ≥75% 的引用来自其他学科类别（Fig. 6）。
- 约 90% 的论文在峰值后引用迅速下降（SI S3），因此"年轻论文尚未来得及沉睡"不改变分布形状。

## Evidence and Limits

- 论文声称"SB 现象并不例外"。证据是 B 的分布连续且为重尾，这支持"没有天然分界"。但"不例外"在很大程度上是 B 的定义使然：B 对任何论文都有定义，连续谱不等于存在共同机制。"幂律暗示共同机制"在 Significance 中只是暗示，正文只做了 APS 一条曲线的拟合，未与其他分布做似然比较，也没给 WoS 的拟合。
- B 只看峰值之前的曲线，不看峰后衰减（作者在 Fig. 2C 说明）。作者承认跨学科、跨年代比较 B 可能有偏，没有做归一化。
- 基线模型只在 APS 上跑（每个 10 次平均），且 NR/PA 都没有 aging 或 fitness。作者明说 Wang et al. 2013 的模型是否与 SB 相容"有待观察"。"简单模型难以解释"的结论因此较弱。
- WoS 的分析限于 JCR 学科类别，用期刊学科推断被引论文的"外部引用"，粒度较粗。"跨学科"解释只有两个案例加一张分布图，是相关性，未检验因果。
- 数据：APS 论文只含 APS 内部引用，与 WoS 引用量不同，所以同一论文在两库的排名会变（如 3 篇 Phys. Rev. 论文）。数据截止 APS 2009、WoS 2011；WoS 需购买，APS 需申请。
- 文中 Table S1 的说明引用 [8] 为 Redner，SI 参考文献列表中为 [8]，主文为 [37]，编号不一致。文中未给代码，也没有说明 B 的计算是否开放。
- 未重现；所有数字取自文本。

## Open Questions

- B 对 c_0 与峰值年的依赖强，对噪声或单年爆发（如一次综述或方法论文引爆）是否稳健？未做敏感性分析。
- 幂律尾部是真实机制，还是 B 的定义加上引用量重尾共同造成的结果？NR/PA 以外的带 aging、fitness 的模型能否复现？
- 唤醒由"另一学科发现"触发，这一假说怎样与"本学科方法论被后来者重新采用"区分开？

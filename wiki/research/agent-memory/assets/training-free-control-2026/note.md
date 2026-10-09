---
title: "A Control Architecture for Training-Free Memory Use"
updated: 2026-10-09
---

# A Control Architecture for Training-Free Memory Use

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文 11 页加附录 A–E）。图 1、图 2 只有标题没有内容；表格可读。bib 只有 arXiv:2604.18206，无正式出处。

## Summary

问题：prompt 注入式记忆（规则、exemplar）不更新权重，但检索到的内容只在合适状态下才有用，所以"何时用、是否采纳"是控制问题，不只是检索问题（§1）。

方法 TAG（§3，Algorithm 1），四个耦合部件：
- 不确定性路由：基线答案置信度 c_t < τ 才检索并做第二遍解码。置信度用答案 token 平均 log-prob，agent 用动作文本的平均 log-prob。
- 守卫式接受：第二遍置信度须高出基线 margin m，且通过 format/valid/progress/contract 结构守卫，否则回滚到基线。
- 规则库与 exemplar 库的选择，含 rule→exemplar 级联、dual 等组合。
- 记忆治理：fit 阶段对每条记忆累积成对 utility，用 Hoeffding 上界 UCB 式规则，上界小于 0 即淘汰；阈值、margin、策略族、治理迭代都在 fit/dev 选定，test 前冻结。

主要结果（Qwen3-0.6B，多 seed 均值，Table 2）：SVAMP 74.0→81.0（+7.0，CI [+4.3,+9.8]，McNemar p=9.7e-7）；ASDiv 77.5→85.2（+7.7，p=3.8e-11）；MultiArith 87.8→89.1（+1.3，CI 跨 0，p=0.143，不显著）。算力匹配的 retry 完全无提升。与同底座的最强替代相比只高约 2 点：SVAMP 对 verifier 77.8 vs 75.7，ASDiv 对 always-retrieve 81.2 vs 79.2（Table 3）。

迁移（Qwen3-8B agent，各 3 seed 合并）：WebShop（n=900）acc +1.44 点，Help−Hurt +13，calls/query −0.55；ScienceWorld（n=600）acc +0.17 点（CI 下界 0），score +1.06，calls −0.91（Table 6）。QA（Table 5）：ARC-Easy 66.3→72.5，OpenBookQA 50.5→51.8，ARC-Challenge 25.5→27.8。第二个 checkpoint Qwen2.5-1.5B-Instruct：SVAMP 62.5→66.0（p=0.053），ASDiv 62.8→69.2（附录 C）。

机制分析（§5.6、§6）：低置信度区间收益最大（图 2）；第二遍置信度对规则库区分 helpful/harmful 的 AUC 为 0.79–0.85，MultiArith 的 exemplar 库仅 0.467（Table 8）；固定检索身份的 counterfactual replay 显示 repair 与 corrupt 的差异集中在检索集含被编辑条目的行（ASDiv 105 行，+5.7 点，14 help 对 8 hurt，p=0.0022）。

## Evidence and Limits

- 论文主张"收益来自控制架构而非原始记忆暴露或额外算力"。retry 持平、重排检索（bm25_rerank）几乎不动（+0.17 点）支持这一点；但对最强替代的优势只有约 2 点，且各表之间同一数据集的数字不一致（Table 2 的 SVAMP TAG 81.0，Table 3/12 的 gated 77.8，Table 13 的 dual 80.3，Table 19 的 governed 80.3），主文没有解释这些口径差别。
- 策略按数据集在 fit 集上挑选（SVAMP 用 dual、ASDiv 用 exemplar→rule、MultiArith 用保守规则策略），Oracle 列是上界。选择空间较大，报告的 test 数字含选择自由度，论文称已冻结但未给 fit/test 规模。
- 基线全是自己实现的同底座对照（no-memory、retry、固定预算、always-retrieve、反思、SC(3)、verifier）。没有与 Self-RAG、CRAG、FLARE 等真实系统比较，附录 C.1 承认只是部分类比。
- 模型很小：推理只用 Qwen3-0.6B，agent 用 Qwen3-8B；第二 checkpoint 仅 1.5B，只做算术。基线 SVAMP 74% 对 0.6B 本身已偏高，记忆库规模小（规则 50、exemplar 100）。
- 记忆库来自 train/fit 侧资源，构造方式在附录 A 说明有限；作者承认没有对库质量、噪声、构造成本做敏感性分析。
- 治理（淘汰）贡献有限且不稳：只在 SVAMP 明显（gap-close 0.70），ASDiv 回到基线附近（0.7850，Gap-close 0.046），低于一次性 multibank 策略（Table 13、19）。摘要把它列为四部件之一，实际主要增益来自路由、接受、选库。
- Table 4 显示 MultiArith 上 gate-only 比基线低 8.9 点，选库后才回升；置信度信号"因库而异"，不是通用修复。
- 置信度只用作门控信号，不是校准概率；Platt 后 ECE 在 MultiArith 反而变差（Table 11）。
- 反事实固定检索的 pooled 结果较弱：+1.33 点，CI [0, 2.67]，p=0.0768（附录 E）；显著的 +5.7 点是按"命中被编辑条目"事后划分的子集，且仅 ASDiv。
- QA 与 agent 的效果小；ScienceWorld 的 acc 增益 CI 下界为 0。固定预算检索在 WebShop 上 acc 更高（+2.8 对 +1.6 点），TAG 的优势在 harmful-acceptance 率、尾部风险和调用数（Table 15）。
- AIME24 对比每组仅 30 题（23/30 对 22/30），记忆是作者按 AIME24 自身正确 rollout 提炼的规则，存在泄漏风险，不能说明记忆质量优势。
- 作者自述的局限：明确的显著收益集中在算术；置信度可分性依赖库与基准；非学习式路由。

## Open Questions

- 策略族和阈值在小 fit 集上选择，换底座或换数据集后能否保持，论文只在算术上用 1.5B 做了一次方向性检查。
- 第二遍置信度高出基线 margin 为何能区分 help 与 hurt，这个信号在更强模型或更长推理链上是否仍然可分，尚未检验。
- 治理为何在 ASDiv 上无效、在 SVAMP 上有效，是库内容差异还是淘汰规则的统计功效问题，文中没有分析。

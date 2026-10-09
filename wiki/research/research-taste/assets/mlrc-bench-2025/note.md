---
title: "MLRC-Bench: Can Language Agents Solve Machine Learning Research Challenges?"
updated: 2026-10-09
---

# MLRC-Bench: Can Language Agents Solve Machine Learning Research Challenges?

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文、NeurIPS checklist、附录 A–F 及 prompt 部分）；图（雷达图、pass@k 曲线、饼图）只有坐标文字，数值细节读不到；附录 G（agent 生成代码）与 I、J 仅略读，未逐行阅读。

## Summary

- 问题：现有评测要么靠 LLM/人类打分看整篇论文（AI Scientist），主观且无可靠基线；要么是 Kaggle 式 ML 工程任务（MLE-Bench），很少需要方法创新。作者想客观衡量 agent “提出并实现新方法”的能力（§1）。
- 基准：从 ML 会议竞赛中选 7 个任务（LLM merging、backdoor trigger recovery、temporal action localisation、rainfall prediction、machine unlearning、next product recommendation、cross-domain meta learning；Table 1）。每个任务提供任务描述、重构后的 starter code（仓库级，agent 只能改 methods/ 目录，评测脚本只读，测试数据不可见）、可选的 human idea，并限定运行时间与显存（§3.1）。选题标准：需要方法创新、非平凡、可复现（§3.2）。
- 指标：Effectiveness（竞赛官方指标）、Efficiency（运行时间）、Simplicity（逻辑代码行数）。主榜指标为相对人类的提升：(s_agent − s_baseline)/(s_top_human − s_baseline)×100，baseline 为 0，竞赛第一名为 100（§3.3）。协议：按 dev 集最优快照在 test 集评一次（§3.4）。
- 主结果（Table 3）：以 MLAB 为 scaffold，每配置 8 次 trial 取最好，最佳是 gemini-exp-1206，7 任务平均仅 9.3；llama3.1-405b 6.3，gpt-4o 5.4，o3-mini 4.2，claude-3.5-sonnet-v2 为 −5.2（machine unlearning 上 −94.7）。多数任务接近 0 或为负；rainfall（gpt-4o 47.5）和 backdoor trigger 例外，作者解释为 U-Net 变体网上易得、baseline GCG 近似随机（§4.2）。
- 加 idea 不稳定提升：gpt-4o 下 Human Idea 平均 3.5、CoI-Agent(o1) idea 7.1，对比无 idea 的 5.4（Table 3，§4.1）。
- LLM-as-judge：用 o1 对实现出的方法按 5 个维度打 1–5 分，与客观指标做 Spearman 相关；innovativeness 与 effectiveness 相关 −0.06（带代码）/ −0.08（不带代码），整体相关弱（Fig. 3, 7，§4.3）。
- 过程分析：随迭代次数增加，runtime 和代码行数上升，性能不成比例上升（Fig. 4）。gemini 的 56 条轨迹中 11.5% 的步骤因工具参数错误，仅 17.2% 的执行错误被修复（§4.4）。成本分析中 llama-405b 性价比最优（Fig. 5）。
- pass@k（成功=缩小至少 5% 的差距）：给 idea 尤其是 human idea 提高多次尝试下的成功率；在固定预算下，分配给不同 idea 数与每 idea 的 trial 数差别不显著（Fig. 6）。16 trial 扩展实验中，machine unlearning 上 MLAB 单独 pass@16 = 0，Human Idea + MLAB pass@16 = 1.00（Table 5，C.2）。

## Evidence and Limits

- 设置：agent 在单卡 Quadro RTX 8000 48GB 或 V100 16GB 上运行；MLAB 每 trial 50 步/5 小时（rainfall 为 100 步/10 小时）；每配置 8 次 trial，因 API 预算限制（§4）。
- 主表报告的是 8 次中的最优值，没有误差棒或显著性检验（checklist 第 7 项明确答 No）。单次最佳的随机性可能很大，例如 claude 的 −94.7 与其它任务的差异无法区分是方法问题还是方差。
- “只填补 9.3% 的差距”是 7 个任务的平均，被 rainfall、backdoor 等 baseline 很弱的任务拉动；backdoor 的 baseline 近似随机，人类提升 621.3%，分母很大也使该归一化不均匀。Table 4 中人类提升 61.9%–621.3%，各任务尺度差异大。
- 只评了 MLAB 一种 scaffold；AIDE 等框架因仓库级设置不适配而未评（§4.1 脚注、Appendix D）。模型是 2024 年底—2025 年初的 gemini-exp-1206、gpt-4o、o3-mini 等，不含更强的推理 agent。ideation 实验只用 gpt-4o。
- “缺乏新颖方法”这一结论与“实现/调试能力不足”混在一起：agent 轨迹显示大量工具参数错误和低修复率，难以区分是创新不足还是工程能力不足。论文自己也承认 human idea 下仍然失败（§4.1）。
- LLM-judge 结论：只有 o1 一个 judge，一个 rubric，被评对象是 agent 自己加注释的代码经 o1 转述的“idea”，样本量未给；相关不显著不等于 judge 无效，但作者给出的“LLM 评测不可靠”的结论仅基于此设定。雷达图称 LLM 打分偏乐观，具体分数在文本中读不到。
- Simplicity 用代码行数，作者自称“imperfect”。数据污染的缓解仅靠“竞赛方案多为报告而非代码”的论断，没有实测。
- 8 个 trial 中多数任务零成功，pass@k 曲线对多数任务无信息（脚注 12），因此“探索 vs 利用无差别”的结论主要来自少数任务。
- 附录 F 的错误分类与修复标签由 GPT-4o-mini / GPT-4o 自动标注，未报告人工校验。
- 未复现任何结果；仅按文中描述阅读。

## Open Questions

- 8 次取最优、无方差估计的情况下，各模型/配置之间的排名差异（如 9.3 vs 6.3 vs 5.4）有多少是噪声？
- 失败主要来自“想不出有效的新方法”还是“实现与调试能力不足”？human idea 也无稳定增益，但没有把两者拆开的对照。
- LLM-judge 与客观效果几乎无相关，是 judge 本身的问题，还是被评的 idea 文本（由代码转述）信息不足、以及绝大多数方案效果接近 0 造成的范围受限？

---
title: "PaperBench: Evaluating AI's Ability to Replicate AI Research"
updated: 2026-10-09
---

# PaperBench: Evaluating AI's Ability to Replicate AI Research

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：正文与附录 A–H 前半（到 Appendix H 的 pruned rubric grading 开头）；之后的 prompt 图（Fig. 7–14）和剩余部分未读；图表为文本抽取，Fig. 2/3/5 只能看到标签。

## Summary

PaperBench 评测 AI agent 从零复现 ML 论文的能力：给定论文和 addendum，agent 要写出完整代码库，并提供 reproduce.sh；提交会在新的 Ubuntu 24.04 + A10 GPU 虚拟机上重新执行，再由 LLM judge 按 rubric 打分（§2）。

- 数据：20 篇 ICML 2024 Spotlight/Oral，经 8 项过滤（Appendix B）；联系 42 位作者，20 位同意合作写 rubric。禁止使用作者原代码和已有复现（blacklist）。
- Rubric 是加权树，叶节点二值判定，共 8,316 个叶节点；每个 rubric 与原作者共同制作，耗时数周（§3.1，Appendix C）。叶节点分三类：Code Development、Execution、Result Match，judge 能看到的文件不同（Table 1）。父节点得分为子节点加权平均，根节点即 Replication Score。
- Judge：SimpleJudge，每个叶节点单独判，文件过长时让模型排序后取前十个。另建 JudgeEval（5 篇论文的部分复现，人工逐叶打标）评估 judge。o3-mini-high 的 F1 为 0.83，每篇约 $66；o1 F1 0.84，约 $830；随机 0.49（Table 3）。
- 主结果（BasicAgent，12 小时，3 次/篇，Table 4）：Claude 3.5 Sonnet (New) 21.0±0.8，o1-high 13.2，DeepSeek-R1 6.0，GPT-4o 4.1，Gemini-2.0-flash 3.2，o3-mini-high 2.6。
- IterativeAgent（去掉提前结束的能力，prompt 要求逐步推进，Table 5）：o1-high 24.4，36 小时延长到 26.0；o3-mini 8.5；Claude 反而降到 16.1。
- 人类基线：8 位 ML PhD，4 篇论文每篇 3 次尝试取 best@3；在 3 篇子集上人类 48 小时 41.4%，o1 为 26.6%。o1 前几小时领先，约 1 小时后趋于平台，人类在 24 小时后反超（§5.4，Fig. 3）。
- PaperBench Code-Dev：只评 Code Development 节点，不跑 reproduce；o1 得 43.4；judge 成本降约 85%（约 $10/篇）。

## Evidence and Limits

- 评分依赖 LLM judge：JudgeEval 上 F1 0.83，Code Development 节点上仅 0.72（Table 8）；论文自己承认不如专家人类，且调用非确定。JudgeEval 只含 5 篇论文的部分复现，且其中部分基于作者原代码修改，分布与真实 agent 提交未必一致。
- 样本量小：20 篇论文，agent 每篇 3 次；人类基线只有 4 篇、每篇 3 人，best@3 对 agent 的 mean 比较并不对等（agent 报告的是平均，人类取最好）。论文也提到部分人类使用 A100 而非 A10。
- 模型对 scaffold 很敏感：同一模型在 BasicAgent 与 IterativeAgent 下排序翻转（Claude 21.0→16.1，o1 13.2→24.4）；IterativeAgent 的 prompt 是在 o 系列上调的。因此 Table 4 的模型排名只是特定 scaffold 下的初始基线，作者也如此声明。未评 Claude 3.7 Sonnet（API 限速）。
- Code-Dev 与完整版相关性弱（o1 上 Pearson r=0.48），只能作为粗略代理。
- Rubric 内部依赖用子节点顺序隐含表达，没有显式依赖图（Appendix A.1）。
- 规则合规靠事后日志文本搜索监控 blacklist URL，646 次运行中发现 10 次违规，得分记 0（§2.5）。
- 污染：几乎所有论文都有公开作者代码，预训练模型可能已记住；作者认为目前影响不大，未给检验。
- 成本：o1 IterativeAgent 12 小时每篇约 $400，整套约 $8000，加评分；rubric 制作每篇需专家数天，难以扩展。
- 未复现：未做独立复现；官方代码在 openai/frontier-evals（bib 记录）。

## Open Questions

- Judge 在对抗性或刻意迎合 rubric 的提交上是否稳健？论文只留作未来工作（Appendix A.3）。
- 模型排名随 scaffold 翻转，哪一部分差距来自模型能力，哪一部分来自 prompt 调优？
- 人类 vs agent 的曲线只在 3–4 篇论文上，结论（agent 约 1 小时后平台）能否推广到其余论文未知。

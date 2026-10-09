---
title: "SWE-bench Goes Live!"
updated: 2026-10-09
---

# SWE-bench Goes Live!

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文、附录 A–H，含 prompts 与 NeurIPS checklist）。图 4、5、7 的热力图/气泡图文字提取有乱码，只能依赖正文对图的描述；表 6 正常。

## Summary

问题：SWE-bench 及其变体（Multi-SWE-bench 等）是静态的，只覆盖 12 个仓库，实例与环境靠人工构建，存在污染、过拟合和扩展性问题（§1）。

方法：提出 SWE-bench-Live，一个可持续更新的 issue-resolving benchmark，任务定义与 SWE-bench 相同（附录 B）。构建分三步（§3, Fig. 1）：
- 抓取 issue-PR 对：GitHub 上 >1000 star 的 Python 仓库 8,577 个，经过 issue/PR 数、fork 数、Python 占比、许可证过滤后剩 2,609 个；沿用 SWE-bench 的抓取脚本并引入 SWE-Fixer 的启发式；要求 PR 含 test patch；只取 2024-01 之后创建的 issue（§3.1）。
- REPOLAUNCH：基于 LLM 的 ReAct 式 agent 为每个 base commit 自动搭建 Docker 环境。流程为相关文件识别、基础镜像选择、交互式 setup、verify agent 生成并运行逐用例输出的测试命令、提交为实例级镜像。另有 "time-machine"：把 pip 源改成只返回不晚于 base commit 时间的包版本，以避免依赖漂移（§3.2）。
- 验证：对比应用 gold patch 前后测试结果，要求至少一个 FAIL_TO_PASS；多次重复运行，仅保留结果一致的实例（§3.3）。

规模：首版 1,319 个实例，93 个仓库，创建时间 2024-01 至 2025-04-20；平均每个仓库 85k 行 Python，gold patch 平均 3.3 文件、102.6 行，F2P 平均 5.4 个、P2P 平均 2953 个（Table 2）。另有 300 个实例的 Lite 子集（2024-10 至 2025-03 每月 50 个）。计划每月更新。

结果（单次运行，temperature 0）：3 个 agent（OpenHands 60 轮、SWE-agent 100 次调用、Agentless 去掉 rerank）× 4 个模型（GPT-4o、GPT-4.1、Claude 3.7 Sonnet、DeepSeek V3）。Lite 上最高 resolved 17.67%（OpenHands 与 SWE-agent 搭 Claude 3.7）（Table 3）；Full 上最高为 OpenHands/Claude 3.7 的 19.25%（Table 4）。同一配置在 SWE-bench Verified 上重跑为 43.20%（§4.2）。来自原 SWE-bench 8 个仓库的 216 个实例 resolved 22.96%，其余 1,103 个为 18.89%（Table 5）。按季度看 resolved 率无明显趋势（§4.3）。patch 越大越难：单文件且少于 5 行约 48%，改 3 个以上文件或超过 100 行则低于 10%，7 个以上文件为 0（§4.4）。仓库越大越难（Fig. 7）。

## Evidence and Limits

- 核心结论"agent 对 SWE-bench 过拟合"证据偏弱。Live 与 Verified 在仓库、语言版本、难度分布、验证方式上都不同，Verified 经过人工筛选，Live 没有；差距可能来自实例质量与环境噪声而非记忆。论文没有做去污染对照（如同仓库同时间段的受控比较）。
- Table 5 的 22.96 对 18.89 是同一最佳配置下的单次结果，无置信区间；且论文自己说非 SWE-bench 仓库更小更简单，方向与"更简单应更易解"相反，但差值本身不大，样本量也不对等（216 对 1,103）。
- Live 全集的 resolved 率没有显著低于 Lite，且各季度之间基本持平，这只能说明难度稳定，不能直接说明"无污染"；论文没有测各模型的训练截止日期与实例日期的关系。
- 实例质量：未报告对自动生成实例的人工抽检（问题描述是否充分、测试是否过拟合 gold patch）、REPOLAUNCH 的成功率、各步成本。验证只保证 F2P 稳定，不保证任务描述足以推出该测试。P2P 允许"可容忍的失败"（§3.2）。
- 评测设置：Agentless 没有 rerank，只取单样本；轮数/调用次数上限较小，与榜单的高 rollout 设置不可比，论文自己也承认这点（§4.2）。所有实验单次运行，未重复（附录 F、checklist 第 7 项答 No）。
- 范围：仅 Python；仓库分类是人工完成的。仓库选择偏向 star 多的热门项目。
- 未复现：未运行任何代码，也未核对其 leaderboard/数据集页面。论文称代码、数据、Docker 镜像已发布。附录 G 的 prompt 完整给出。

## Open Questions

- 实例中有多大比例的 issue 描述与测试不匹配或可被"作弊"解决？没有类似 SWE-bench Verified 的人工审核。
- 随着每月更新，不同时间点的版本之间得分如何比较？论文只展示了季度间稳定，但未讨论版本迭代下的可比性与固定子集的维护。
- Live 与 Verified 的差距有多少来自污染/过拟合，多少来自实例分布和环境质量差异？需要受控实验分离。

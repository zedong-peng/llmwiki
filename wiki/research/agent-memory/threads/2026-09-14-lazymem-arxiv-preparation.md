---
title: LazyMem 既有实验论文的 arXiv 提交准备
domain: research
area: agent-memory
type: engineering
status: stable
updated: 2026-09-14
tags: [lazymem, paper, arxiv, negative-results, evidence-audit]
---

# LazyMem 既有实验论文的 arXiv 提交准备

用户要求把既有 LazyMem 论文整理成可以提交 arXiv 的形式，沿用现有 repo 组织。署名明确确认为 Zedong Peng，单作者，不列机构。没有上传 arXiv。

## 交付

- [11 页 PDF](</Users/pengzedong/Documents/Workspace/agent-memory/lazymem/paper/arxiv/lazymem.pdf>)
- [arXiv 源码提交包](</Users/pengzedong/Documents/Workspace/agent-memory/lazymem/paper/arxiv/lazymem-arxiv.tar.gz>)
- [仓库论文目录与使用说明](</Users/pengzedong/Documents/Workspace/agent-memory/lazymem/paper/README.md>)
- [验证记录](</Users/pengzedong/Documents/Workspace/agent-memory/lazymem/paper/VALIDATION.md>)

题目：**LazyMem: A Raw-Text Memory Baseline and a Negative Result on Query Compilation**。

## 科学定位

论文报告原始文本 BM25-window 与旧谓词 compiler 的既有 LoCoMo 开发集对照，保留负结果、题型差异和完整实验限制。旧稿的模型变强导致框架应变简单的论断改为未验证假设；不将后来 SDK 多轮检索的能力归因到历史单次检索分数。

1,540 个问题中，BM25 的 F1 为 0.5526、既有 judge 为 78.64%；compiler 为 0.5019、74.22%。生成 token 减少 14.93%。逐题净多正确 68，其中 single-hop +72，temporal +3，multi-hop −5，open-domain −2。新增离线配对/对话 cluster bootstrap 和 token 分解，不调用新模型。

原检索报告的 compiler ID 集在 1,032 题上与实际预测不一致；论文按真实预测与原始标注重算支持覆盖。保留缺失历史 protocol/source binding、后验开发集选择、judge 缺陷、图像字段遗漏等限制。未使用未经同协议绑定的外部产品分数拼接排名表。

## 可复查性

`paper/artifacts/` 发布 3,080 行数值记录和原输入 hashes；`evaluation/export_paper.py --from-release` 不依赖原始对话即可重算表格。原始 archive 保持不变。提交包包括 `.bbl`、矢量图与 ancillary 数值材料，解压至临时目录后完成独立编译和数值复算，无 TeX 警告/溢出。

原稿在 Git 和本地 ignored research history 中保留。生成的 `paper/arxiv/` 被 Git 忽略；可由 `make -C paper arxiv` 重建。本次未提交 Git、推送或发布。

另见 [[research/agent-memory/threads/2026-09-14-work-continuity-memory|长期 agent 记忆机制调查]]；这是不同的后续研究任务，不与现有论文主张混合。

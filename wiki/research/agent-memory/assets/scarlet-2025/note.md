---
title: SCARLet：用证据贡献来训练检索器
domain: research
area: agent-memory
type: paper
status: active
updated: '2026-09-22'
tags:
- rag
- evidence-utility
- related-work
---

## Archive Reading Record

- Historical reading status: read; migrated existing notes without extending the reading scope.
- Recorded source: tex.
- Recorded scope: main method, experiments, ablations, limitations; method and implementation appendices; bibliography not independently audited.
- Recorded reading paths: `paper-tex/extracted/2504.00573v2/acl_latex.tex`.
- Source versions, checksums, repository commits, and full historical metadata: [citation.bib](citation.bib).

# SCARLet：用证据贡献来训练检索器

## 论文与资产

Yilong Xu、Jinhua Gao、Xiaoming Yu、Yuanhai Xue、Baolong Bi、Huawei Shen、Xueqi Cheng。*Training a Utility-based Retriever Through Shared Context Attribution for Retrieval-Augmented Language Models*，EMNLP 2025，629–648；本次读取 **2504.00573v2**（2026-02-02 修订），年份目录保留 2025。

## 一句话

训练时反复拿走部分资料，看正确答案失去多少支持，再用这个信号教检索器以后优先找真正有用的资料。

## 方法：把效用变成训练标签

正文 Method 与归因附录：从种子实体及 Wikidata 一跳邻居检索 Wikipedia 段落，构建共享上下文；在同一批内容上合成问答、事实核查等不同任务，减少“语义领域不同”造成的混淆。六类任务各取 1,000 个种子，使用 gpt-4o-2024-11-20 合成、过滤，并注入“相关但无用”的干扰段落。

对上下文做 64 次随机遮蔽，每段保留概率 0.5；在给定标准答案条件下，计算答案 token 的 logits 之和，再用 ridge regression 拟合“哪些段落保留”与输出分数的关系。系数作为段落效用，按一维聚类分成正样本、中间舍弃、负样本，用于训练检索器。这是近似贡献归因，不是精确 Shapley 值，也不构成因果证明。

论文在 Contriever / BGE 检索器上报告结果。主要改动在离线合成、归因和训练，推理沿用检索流程并取 top-3；并非每次提问都在线执行 64 次遮蔽。

## 论文报告的实验

10 个数据集各取 1,000 测试样本，包含 6 个域内及 4 个域外任务。Llama3-8B 生成器下，BGE 的 NQ 得分 47.5→49.2，HotpotQA 41.6→47.0。这里 QA 指标是标准答案是否出现在输出中的 substring accuracy，不是 token F1。Qwen2.5-3B 下 NQ 46.8→44.9，说明并非所有搭配都提升；代码领域 BRIGHT 泛化也有退化。训练报告 A100、学习率 6e-5、1 epoch。均未本地复现。

## 代码核查与缺口

已检查 README、`src/attribution/attribute.py`、`src/training/sample.py`、`src/training/train.py`、`src/inference/downstream.py` 及归因/采样/训练脚本。

- 归因入口确实传入 `ground_truth_answer`、64 次 ablations，并保存 `utility`。但导入的 `src.attribution.context_attributor` 在缓存仓库中不存在，不能据此核实底层 ridge/logit 实现或宣称归因链可直接运行。
- `sample.py` 用 KMeans 三簇取最高簇为正、最低簇为负，并过滤若干异常样本。
- `train.py` 实际使用 query-passage 成对编码与 `AutoModelForSequenceClassification(num_labels=1)`，对候选 logits 做交叉熵。这与“可直接训练并部署独立向量的 dense retriever”的理解存在实现差距，不能将此脚本自动等同于论文整套检索流程。
- 论文提及 float32，归因入口加载模型使用 float16；下游代码确认 substring 匹配口径。

## 局限及与 Jev 的关系

依赖训练时标准答案、生成器 logits、较贵的多次遮蔽和高质量合成模型。换生成器或领域可能改变证据效用。它提供的是“怎样得到效用监督并训练检索”的方法，不是插一个 Jev 提示词即可等价替代的组件。

## 本地证据与阅读状态

- [arXiv](https://arxiv.org/abs/2504.00573v2) · [PDF](paper-pdf/2504.00573v2.pdf) · [TeX 主文件](paper-tex/extracted/2504.00573v2/acl_latex.tex) · [官方仓库缓存](github-repo/SCARLet) · [元数据](citation.bib)。
- 仓库 commit：`871c3756c98bf7e40d5e94c8fb6e4127a613fc9f`。
- 已阅读 TeX 方法、主要实验、消融与局限；相关附录按方法与实现细节核查；未逐一审核所有参考文献或独立复现实验。代码仅静态检查，未安装依赖、训练或调用模型。
- 对照解释：[[research/agent-memory/threads/jev-related-work|Jev 相关工作：四种不同层次]]；[[research/agent-memory/assets/jev-system-one-2026/note|Jev / System One]]。

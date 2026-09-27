---
title: OptiSet：选出互补的证据组合
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

# OptiSet：选出互补的证据组合

## 论文与资产

Yi Jiang、Sendong Zhao、Jianbo Li、Bairui Hu、Yanrui Du、Haochun Wang、Bing Qin。*OptiSet: Unified Optimizing Set Selection and Ranking for Retrieval-Augmented Generation*，arXiv **2601.05027v1**（2026-01-08）；未核实正式会议发表。

## 一句话

不要只挑单篇得分最高的几篇，而要挑一组能够互相补充、一起回答问题的资料。

## 两条方法路线

正文方法与算法区分 training-free 和 trained 两种方式。

无需训练的 Expand → Select → Refine：拆解原问题，列出信息需求；在给定候选文档 D 内为各子问题选证据；合并后用原问题再次筛选。实验输入是 Contriever 召回的 top-20。这里的“扩展”是扩展问题视角与候选证据组合，**不是自动重新搜索整个语料库**。

训练版先多次运行上述流程构造候选集合，每题 10 次，训练合成阶段可提供标准答案；20k 数据筛为 8k，每题 5 组候选并进行 3 次打乱。通过有无文档集合时标准答案 log-perplexity 的差值评价集合效用，以符号化 sigmoid 映射分数，结合最佳集合交叉熵及候选集合分布间 KL（λ=0.1）训练。它不是模型自由输出的预测熵，也不是在任意当前集合上逐条测量条件边际收益。

## 论文报告的实验

生成/选择基座 Llama3.1-8B；训练采用 LoRA rank 128、alpha 32、dropout 0.05，1 epoch、学习率 3e-5、2×A100。附录列 HotpotQA 500、Bamboogle 125、MuSiQue 2,417、TriviaQA 500；正文另提 2Wiki 子集，与表/附录不完全一致。

HotpotQA 答案 F1：Naive RAG 35.13、免训练版 41.72、训练版 43.30；平均入选文档数分别 3、2.20、2.34。Bamboogle 为 23.83→29.08→32.67。MuSiQue 训练版 15.49，低于 Rank1 15.84 和 SetR 16.16，不是全面领先。论文还报告包含式非严格 EM，应与 token F1 区分。

效率主要体现为最终选择文档更少，不能由此推断整条流水线的总时延或总费用更低。所有数字为论文报告，未复现。

## 代码可用性

官方 `liunian-Jay/OptiSet` 仓库截至本次缓存仅有 `README.md` 与 `assets/framework.png`。README 写有 “Details will be completed soon!” 和 TBD，没有选择、训练、评测实现。缓存仓库只用于核实发布状态，不视为可运行复现代码。

## 局限及与 Jev 的关系

受最初 top-20 的召回上限及模型上下文长度限制；动态集合大小不等于显式 token 预算优化。对某个生成器有用的集合不一定对另一个同样有用。

它已经覆盖“多视角扩展后再精选”与“集合互补优于单条排序”的方法空间。用 Jev 执行其中的判断可以是工程实现，但不能单凭替换底层模型声称上述概念的新颖性。

## 本地证据与阅读状态

- [arXiv](https://arxiv.org/abs/2601.05027v1) · [PDF](paper-pdf/2601.05027v1.pdf) · [TeX 主文件](paper-tex/extracted/2601.05027v1/Arxiv_submit.tex) · [官方仓库缓存](github-repo/OptiSet/) · [元数据](metadata.yaml)。
- 仓库 commit：`d4e37e0cd0aad4a9acbafc0e3406bcf9145b76cc`。
- 已阅读 TeX 方法、主要实验、消融与局限；相关附录按方法与实现细节核查；未逐一审核所有参考文献或独立复现实验。代码仅静态检查，未安装依赖、训练或调用模型。
- 对照解释：[[research/agent-memory/jev-related-work|Jev 相关工作：四种不同层次]]；[[research/agent-memory/assets/jev-system-one-2026/index|Jev / System One]]。

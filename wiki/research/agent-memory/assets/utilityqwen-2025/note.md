---
title: UtilityQwen：选择能帮助回答的段落
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
- Recorded reading paths: `paper-tex/extracted/2507.19102v2/main.tex`, `paper-tex/extracted/2507.19102v2/Sections/Method.tex`, `paper-tex/extracted/2507.19102v2/Sections/Experiments.tex`, `paper-tex/extracted/2507.19102v2/Sections/Futher_analyse.tex`, `paper-tex/extracted/2507.19102v2/Sections/Conclusion.tex`, `paper-tex/extracted/2507.19102v2/Sections/Related_work.tex`.
- Source versions, checksums, repository commits, and full historical metadata: [citation.bib](citation.bib).

# UtilityQwen：选择能帮助回答的段落

## 论文与资产

Hengran Zhang、Keping Bi、Jiafeng Guo、Jiaming Zhang、Shuaiqiang Wang、Dawei Yin、Xueqi Cheng。*Distilling a Small Utility-Based Passage Selector to Enhance Retrieval-Augmented Generation*，SIGIR-AP 2025；本次读取 arXiv **2507.19102v2**（2025-10-09）。

## 一句话

搜索先找来一堆资料，再让一个专门训练的小模型挑出“对回答真有帮助”的资料，而不只按“看起来相关”排序。

## 方法：相关不等于有用

Method 节将 Qwen3-32B 教师的伪答案生成与段落选择蒸馏到 Qwen3-1.7B。训练使用 100k MS MARCO 查询及每条查询的 BM25 top-20；学生同时学习形成答案与选择段落。伪答案不是已知正确答案，可能出错。

推理先由 BM25 或 BGE-base-en-v1.5 召回 top-100。以 20 条窗口处理，将上一轮最多 10 条入选内容带入后续窗口。输出数量可变，不必强行保留固定 top-k。适合放在 RAG 的“初步召回 → 最终回答”之间。

## 论文报告的实验

HotpotQA 7,405 条、NQ 2,255 条子集；生成器为 Llama3.1-8B-Instruct 或 Qwen2.5-7B-Instruct。BGE + Llama 设置下，主表 RankQwen top-5 答案 F1 为 49.68，UtilityQwen 为 53.56，后者证据 micro-F1 为 60.58。训练报告 8×A800 80GB、bf16、3 epochs、batch 64、学习率 5e-6。上述为论文数值，未复现。

原文有不一致：教师主体描述为 Qwen3-32B，但标注段落出现 Qwen2.5-32B；效率表答案 F1 为 53.36，与主表 53.56 不同；3.4h 对 11.2h 约减少 70%，正文另有“减少 30%”表述。保留差异，不将它们强行合成统一结论。

## 代码核查

已检查 README、`RelevanceRank_UtilitySelection/run_utility_selection.py` 和 `rank_llm/training/run.sh`。推理使用 vLLM、temperature 0、max_tokens 512、关闭 thinking；段落截到 300 words，输出伪答案和 `My selection` 编号列表。

窗口实现用 `last_selected = selected[:10]`，新加入数量取决于携带量，不是无条件固定步长 10。代码保留此前选中过且未重复的段落，即使后续窗口没有再次选中，也不一定删除；因此不能理解为严格的全局最小证据集合求解器。训练脚本为 generation objective，并包含本地模型路径；未安装或运行。

## 局限及与 Jev 的关系

选择只发生在已经召回的候选中，找不到候选池以外的遗漏事实；还要付出伪答案生成与选择成本。论文是通用 QA 评测，不能直接推断长期记忆任务有效。

这是“训练过的专门证据选择器”。Jev 可以用于实现某种选择决策，但替换模型本身不足以证明“按证据效用筛选”是新方法。

## 本地证据与阅读状态

- [arXiv](https://arxiv.org/abs/2507.19102v2) · [PDF](paper-pdf/2507.19102v2.pdf) · [TeX 主文件](paper-tex/extracted/2507.19102v2/main.tex) · [官方仓库缓存](github-repo/UtilitySelection) · [元数据](citation.bib)。
- 仓库 commit：`28f1f993c0369d03d3b572d153fadf32df93ea5d`。
- 已阅读 TeX 方法、主要实验、消融与局限；相关附录按方法与实现细节核查；未逐一审核所有参考文献或独立复现实验。代码仅静态检查，未安装依赖、训练或调用模型。
- 对照解释：[[research/agent-memory/threads/jev-related-work|Jev 相关工作：四种不同层次]]；[[research/agent-memory/assets/jev-system-one-2026/note|Jev / System One]]。

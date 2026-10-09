---
title: "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?"
updated: 2026-10-09
---

# SWE-bench: Can Language Models Resolve Real-World GitHub Issues?

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：正文与附录前半（A.1–A.7、B、C.1–C.2 及 Table 18 起始处）；文本读到约第 1600 行。Fig 4/5/9 的图像仅有文字残影；A.7（SWE-bench Lite 的筛选细节）文本被截断，正文 §2.4 也有一句话残缺；附录 D–F（prompt 与定性案例）未读到。

## Summary

问题：现有代码基准（如 HumanEval）多为几行代码的自包含题，无法反映真实软件工程。作者提出 SWE-bench：给定 issue 文本和完整代码库快照，模型需生成 patch，用仓库自带测试判定是否解决 (§1, §2.2)。

构建流程（§2.1, App. A）：从 12 个流行 Python 仓库抓取约 9 万个 PR（Table 10 为 93,139），三步过滤：(1) 已合并且链接 issue；(2) PR 修改了测试文件；(3) 执行过滤，要求安装/运行成功，且至少有一个 fail-to-pass 测试。最终得到 2,294 个实例。Table 1：平均 issue 195 词，代码库约 3,010 个文件、438K 行，gold patch 平均改 1.7 个文件、3.0 个函数、32.8 行。指标是 resolved 比例：所有 fail-to-pass 和 pass-to-pass 测试都通过才算解决 (A.4)。另给出 300 题的 SWE-bench Lite (§2.4) 和 225 题开发集 (A.6)。

SWE-Llama：用 19,000 条来自另外 37 个仓库的 issue-PR 对，在 CodeLlama-Python 7b/13b 上做 LoRA 微调（超过 30k token 的样本被剔除，剩约 10,000 条）(§3, App. B)。

结果：基线是 BM25 检索文件塞进上下文，一次生成 patch，没有 agent 交互。Claude 2 解决 1.96%（Table 2，13k 上下文）；Table 5 中 Claude 3 Opus 为 3.79%，GPT-4-turbo 1.31%，ChatGPT-3.5 0.17%，SWE-Llama 7b/13b 均为 0.70%。用 oracle 检索（只给 gold patch 改过的文件）时，Claude 2 为 4.80%，SWE-Llama 13b 为 3.97%（Table 18）。

分析 (§5)：上下文越长表现越差，BM25 最长上下文设置下几乎为 0（Table 2）；把 oracle 文件折叠到只剩修改处 ±15 行，Claude 2 从 4.8% 升到 5.93%，Claude 3 Opus 为 9.39%（Table 6）；生成 patch 优于整文件重写（Claude 2 为 4.8% 对 2.2%）；模型写出的 patch 更短，多只改单文件（Table 8）。

## Evidence and Limits

- 论文声称构建方式真实、可持续更新、评测稳健；数据与过滤统计（Table 10, 11）支持其规模和多样性。执行验证能保证任务可运行、测试可区分，但不保证 issue 描述足以唯一确定解法。
- 作者自己指出：测试通过不等于代码质量好，模型 patch 常更简单、不顾代码风格 (§5.1, §7)。
- 数据泄漏：Table 7 按 2023 年前后切分，多数模型差别不大，作者据此认为模型未靠记忆作答。但该切分粗糙，且 GPT-4 在此表只跑了 25% 子集，结论偏弱。
- 比较范围窄：只评估了 ChatGPT-3.5、GPT-4(-turbo)、Claude 2/3 Opus 和自训 SWE-Llama；GPT-4 因预算多处只跑 25% 随机子集，各设置的实例数不同，数字不完全可比 (Table 7, 14)。
- SWE-Llama 在 BM25 上表现很差，作者推测是训练用 oracle 上下文造成分布偏移 (§5)，没有做验证实验。
- 文中数字有不一致：摘要和 §5 称最佳为 Claude 2 的 1.96%，但 Table 5 里 Claude 3 Opus 为 3.79%；Claude 2 在 §1 写 1.96，Table 5 写 1.97。看起来是 v3 更新时未统一。
- 其余局限（作者所述）：仅 Python；只做了最简单的检索加单次生成基线，未探索 agent 或工具增强 (§7)。部分 issue 含图片，需多模态能力 (§5)。
- 补丁评测前会自动修复格式不合法的 patch (A.4)，Table 14 显示此类修复占已应用 patch 的 20%–69%，会影响 resolved 率的解读。

## Open Questions

- 低于 5% 的解决率中，有多少是 BM25 定位失败，有多少是真正的推理或编辑能力不足？oracle 与折叠实验只给出部分答案。
- issue 文本是否总能唯一确定可通过测试的实现？论文只排除了测试引用新命名的情况（ImportError/AttributeError），其余欠规格问题未量化。
- 微调模型对检索分布偏移的敏感性是否真因训练用 oracle 上下文，需要用 BM25 上下文训练来对照。

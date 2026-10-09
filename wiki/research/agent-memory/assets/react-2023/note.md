---
title: "ReAct: Synergizing Reasoning and Acting in Language Models"
updated: 2026-10-09
---

# ReAct: Synergizing Reasoning and Acting in Language Models

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文、参考文献、附录 A–E）。图 1、2、3、5 的文字被编码损坏，只能依据正文和图注；附录 C 的 prompt 与 D 的轨迹示例只浏览了结构，未逐条核对。

## Summary

问题：LLM 的推理（chain-of-thought）和行动（生成动作序列）此前被分开研究。CoT 不接触外部世界，容易 hallucination 和错误传播；纯 acting 缺少对目标的抽象推理和工作记忆。

方法：ReAct 把 agent 的动作空间扩展为 A ∪ L，L 为自然语言。"thought" 不影响环境、没有 observation，只是把推理写进 context，供后续推理和行动使用（§2）。主要设置是冻结的 PaLM-540B，加 1–6 个人工写的 few-shot 轨迹。知识类任务采用 thought-action-observation 稠密交替；决策类任务由模型自己决定 thought 稀疏出现的位置。

结果：
- HotpotQA / Fever（question-only，自建 Wikipedia API：search / lookup / finish），Table 1：Act 25.7 / 58.9，ReAct 27.4 / 60.9，CoT 29.4 / 56.3，CoT-SC 33.4 / 60.4。ReAct 在 Fever 上胜过 CoT，在 HotpotQA 上略低。
- ReAct 与 CoT-SC 互相 back off 的组合最好：ReAct→CoT-SC 在 HotpotQA 为 35.1，CoT-SC→ReAct 在 Fever 为 64.6。Figure 2 显示组合方法用 3–5 个 CoT-SC 样本就能达到 CoT-SC 21 样本的水平。
- 微调（§3.3，Figure 3）：用 3,000 条 ReAct 生成的正确轨迹微调 PaLM-8B/62B，ReAct 成为四种方法中最好；8B 微调后的 ReAct 超过 62B 的所有 prompting 方法。
- ALFWorld（134 个 unseen 游戏，Table 3）：ReAct best-of-6 为 71%，Act 45%，BUTLER 37%；ReAct 平均 57%。ReAct-IM（Inner Monologue 式稠密反馈）53%。
- WebShop（500 条测试指令，Table 4）：ReAct success rate 40.0，Act 30.1，IL 29.1，IL+RL 28.7，人类专家 59.6。
- 人工标注 HotpotQA 各 50 条轨迹（Table 2）：CoT 的成功样本中有 14% 是 hallucination（ReAct 为 6%），失败原因中 hallucination 占 56%；ReAct 失败主要是 reasoning error（47%，含重复循环）和 search result error（23%）。

## Evidence and Limits

- 摘要说 ALFWorld 和 WebShop 上"绝对提升 34% 和 10%"。34 来自 71 对 37 的 best-of-6 对 best-of-8 BUTLER；ReAct 平均值是 57，对比差距更小。WebShop 的 10 为 40.0 对 29.1。
- ALFWorld 的 6 个 prompt 来自 3 条标注轨迹中任取 2 条的排列，best-of-6 相当于在评测集上选 prompt。BUTLER 用 beam search，ReAct 用 greedy，并且 BUTLER 用的是 10^5 条专家轨迹训练。对比的是 few-shot prompting 和训练模型，设置不同。
- ReAct 与 Act 的对照在 ALFWorld 和 WebShop 上用的是同一批轨迹去掉 thought，较为干净。HotpotQA 上 ReAct 低于 CoT，作者用组合方法弥补，组合方法的启发式阈值（7/5 步、n/2 票）是作者设定，文中未给敏感性分析。
- Table 2 的人工分析每格 50 条，样本小，且为单一标注。
- 微调实验只在 HotpotQA 上做，微调样本来自模型自己生成的正确轨迹；所有 prompting 方法仍远低于监督 SoTA（67.5 EM / 89.5 Fever）。
- 主实验的 PaLM-540B 不公开；附录 A.1 用 GPT-3 (text-davinci-002) 复现，HotpotQA 子集（500 题）EM 30.8、ALFWorld 78.4，两个任务都高于 PaLM。
- Wikipedia API 故意做得很弱（只能按页面名取前 5 句），结论不一定外推到强检索器。
- 作者承认的限制：复杂任务需要更多示例，会超出 in-context 长度；ReAct 会陷入重复生成 thought/action 的循环（猜测与 greedy decoding 有关，脚注 4）；检索无信息时难以恢复。
- 可解释性、可诊断性、"thought editing" 人机协作（附录 A.3，图 5）只是个例展示，没有系统评估。
- 代码：正文给了匿名链接和项目页 react-lm.github.io，未给最终仓库地址。

## Open Questions

- ReAct 的收益有多少来自 thought 本身，有多少来自 few-shot 示例质量和 prompt 选择？ALFWorld 6 个 prompt 之间的方差很大（best 71 对 avg 57）。
- 重复循环和检索失败的问题在更好的解码或更强的检索工具下是否消失，文中没有实验。
- 微调结论只在 HotpotQA 与 8B/62B 上成立，能否推广到决策类任务以及更大数据量，文中未验证。

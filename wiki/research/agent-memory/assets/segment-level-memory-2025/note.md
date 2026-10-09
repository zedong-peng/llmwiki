---
title: "On Memory Construction and Retrieval for Personalized Conversational Agents (SeCom)"
updated: 2026-10-09
---

# On Memory Construction and Retrieval for Personalized Conversational Agents (SeCom)

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文、参考文献、附录 A.1–A.11 到 Table 11 与分割 prompt/rubric 的开头）。图中数值是从文本抽取的，坐标轴有些乱；附录后半的 case study 图（Fig. 13–16）、Fig. 9–10 rubric 全文、Fig. 12 评测 prompt 未细读。

## Summary

问题：长期开放域对话里，检索增强回复生成（RAG）的记忆单元粒度怎么选。turn 级太碎，相关信息分散在多轮里，关键词不一定出现在命中的 turn 中；session 级太粗，一个 session 常含多个话题，引入无关内容；摘要类方法丢细节（§1, Fig. 1, Fig. 2）。

方法 SeCom 由两部分组成：
1. 对话分割（§2.2）：用 GPT-4-0125 零样本把 session 一次性切成话题连贯的 segment，输出 JSONL 的起止 turn 编号；segment 直接拼接作为上下文，不做摘要。有少量标注时，用 LLM 自我反思从 WindowDiff 最差的 100 个样本中分 10 批提炼 10 条 rubric 和代表样例，作为 few-shot 指导（文中类比 prefix-tuning / SGD，是类比而非真实梯度）。
2. 压缩去噪（§2.3）：检索前用 LLMLingua-2（压缩率 75%，xlm-roberta-large）压缩每个记忆单元，认为自然语言冗余对检索是噪声（Fig. 3：压缩率较高时 recall 上升，相关/无关 segment 与 query 的相似度差拉大）。

设置：回复模型 GPT-3.5-Turbo（另测 Mistral-7B-Instruct-v0.3）；检索用 BM25 与 MPNet+FAISS；数据集 LOCOMO（平均 300 turn、约 9K token）和自建的 Long-MT-Bench+（把 5 个 MT-Bench+ 对话拼接，平均 65.45 turn、19,287 token）。指标 GPT4Score、BLEU、ROUGE、BERTScore。

主要结果（Table 1）：
- LOCOMO，4k token 预算：SeCom(BM25, GPT4-Seg) GPT4Score 71.57，SeCom(MPNet) 69.33；对比 Turn-Level BM25 65.58 / MPNet 57.99，Session-Level 63.16 / 51.18，MemoChat 65.10，ConditionMem 65.92，Full History 54.15。
- Long-MT-Bench+，1k token 预算：SeCom(MPNet) 88.81，BM25 86.67；Turn-Level 82.85 / 84.91，MemoChat 85.14，Full History 63.85。
- Turn/Session 级方法对检索器很敏感（BM25 与 MPNet 相差最高 11.98 / 7.89 分），SeCom 两种检索器下差距较小。
- 消融（Table 2）：去掉去噪，LOCOMO 69.33 到 59.87，Long-MT-Bench+ 88.81 到 87.51。
- 分割模型换小：Mistral-7B 分割 LOCOMO 66.37 / Long-MT-Bench+ 86.32；RoBERTa 分割 61.84 / 81.52（Table 1, 11）。
- 分割基准（Table 4）：DialSeg711、SuperDialSeg、TIAGE 上零样本 GPT-4 分割的 Pk/WD/F1 优于列出的无监督基线；带反思的版本在迁移设定下多数指标优于在源训练集上训练的 RoBERTa 等。例如 DialSeg711 零样本 F1 0.888，对比 CSM 0.610。
- 附录：官方 LOCOMO QA（Table 6）、CoQA（Table 8）、Persona-Chat（Table 9）、10 名标注者的人评（Table 10）上趋势一致；成本（Table 5）：SeCom 输入 1,722 token、延迟 2.61s，MemoChat 7,233 token、5.60s。

## Evidence and Limits

- 粒度对比有对照：同一检索器、同一预算下比 turn/session/segment，且 Fig. 5 给出了多个预算下的曲线，segment 级整体占优。这部分证据较扎实。
- 评测依赖 LLM：LOCOMO 的 QA 对（主实验）与 Long-MT-Bench+ 的测试问题都由 GPT-4 生成，打分和 pairwise 比较也用 GPT-4-0125；分割器同样是 GPT-4。存在生成器/评估器同源的风险，文中未讨论。官方 LOCOMO QA 作为补充（Table 6）。
- Long-MT-Bench+ 上 SeCom 与 Turn-Level(MPNet)、MemoChat 的差距较小（88.81 vs 84.91 / 85.14），无方差、种子或显著性检验的报告；pairwise 中 SeCom 对 Turn-Level 胜 45.19%、负 28.59%（Fig. 4）。
- 主表 SeCom 与 turn/session 基线都用了去噪（文中说明直接与"去噪增强"的基线比较），但摘要式基线和 MemoChat 未必同等对待；去噪对粒度的各自贡献在主表里不易拆分。
- 去噪机制的证据主要来自 Long-MT-Bench+ 上的 recall 和相似度曲线（Fig. 3，纵轴变化幅度很小，如相似度在 0.983–0.987 之间）；"冗余=检索噪声"的解释未做更直接的验证。
- 小模型分割下优势收窄：LOCOMO 上 Mistral-7B 分割 66.37，仅略高于 Turn-Level BM25 的 65.58；RoBERTa 分割 61.84 低于 BM25 的 turn/session 基线（Table 1）。
- 分割阶段的成本只在 Table 5 以单题延迟与 token 汇总，未分别列出；GPT-4 分割对长历史的开销没有单独分析。主实验分割为零样本、不使用 rubric。
- 分割基准比较里，部分基线数字引自其他论文（Table 4 脚注）；有监督基线与本方法的训练数据量设定不同（100 个难例 vs 完整训练集）。
- 论文只给出项目页 https://aka.ms/secom，未明确说明代码仓库；未复现。

## Open Questions

- 摘要、turn、segment 的比较是在不同上下文长度下进行的（Table 1 的 token 数不一致），摘要类方法的落后有多少来自预算差异而非信息丢失？
- 话题切分在话题交错、跨 session 回指、需要时间推理的问答上是否仍然有效？LOCOMO 的多跳/时序类问题未分类报告。
- 去噪带来的增益是否依赖具体检索器（BM25/MPNet）和 75% 压缩率，换更强的 dense retriever 后是否还成立？

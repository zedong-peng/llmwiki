---
title: "Eywa: Provenance-Grounded Long-Term Memory for AI Agents"
updated: 2026-10-09
---

# Eywa: Provenance-Grounded Long-Term Memory for AI Agents

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（29 页，含正文、参考文献、附录 A/B）。图 1–3 只有图注，没有图本身；表格文本基本完整。

## Summary

**问题。** 跨会话 agent 的记忆出错时，很难判断错在哪一层：证据缺失、抽取出了没有依据的事实、状态过期、检索丢失，还是回答模型的行为。端到端分数把这些混在一起（§1, Table 1 给出 8 类 failure taxonomy：coverage / grounding / revision / scope / temporal / retrieval / synthesis / measurement）。

**方法（§4）。** 原则是 "evidence before belief"。
- 写路径两层。Tier 0 把每条用户 turn 存为不可变 evidence，并用规则（regex + spaCy NER，不调 LLM）检测 typed signals（日期、实体、金额、版本、URL 等）。Tier 1 由 LLM 抽取候选事实，再用 V = V_support ∧ V_hard ∧ V_subject ∧ V_act 校验（来源文本重叠、硬值精确匹配、主语出现、否定/不确定性保留），通过的才写入 canonical fact，并保留指向 evidence 的 provenance link。
- 抽取只被当作 evidence 之上的可修订索引，不是记忆本身（§4.2）。
- 读路径零 LLM 调用。手写规则表的 query planner 按问题形状（精确、推荐、推理、计数、区间等）给 vector / FTS5-BM25 / temporal / entity-graph 四路加权，做 weighted RRF（k=20）。之后做 person demotion（δ=0.05）和 preservation floor（rank 25），再按 token budget 打包；另有 raw-episode rescue 和 inference support 两个辅助通道（§4.5）。
- 返回的 context 与 answer_instructions 分开，有 strict / balanced / advanced 三种回答策略（§4.6）。
- 实现为 SQLite（权威存储）+ LanceDB + RustworkX 图 + 本地 ONNX embedding，单进程 local-first（§4.3, 附录 B）。

**结果（§5）。**
- LoCoMo C1–C4（1,540 题，GPT-4o 作 judge）：write 与 QA 同模型族的对齐运行，Sonnet 4.6 为 90.19%，GPT-4o 为 88.77%，Kimi K2.5 为 84.09%（Table 5）。平均检索 context 约 4.3k tokens（Table 6）。
- LongMemEval-S（500 题，GPT-4o 兼任 write / QA / judge，3,200 token 预算）：retrieval-sufficiency 88.2%（Table 10）。剩余 59 个失败里，27 个是 fact not retrieved（Table 11）。
- BEAM（本文提出，35 段对话、700 题）：平均 nugget 分 81.45%，pass@0.5 为 597/700，Summarization 最弱（64.07%）（Table 12）。
- 检索延迟：在 6,320 facts 的 stress store 上，交互式检索约 200 ms，不含生成（Table 13）。
- Qwen3 32B 诊断：自写自答 69.09%，读 Sonnet 写的记忆库 79.68%（Table 7），C3 对回答模型最敏感（Table 8）。
- 另提出 refusal-aware F1：对非对抗类的拒答记 0 分（§5.5）。

## Evidence and Limits

- **比较是文献语境，不是对照。** Table 9 的外部行（Hindsight、Mem0、Zep 等）来自别人的论文或 MemOS 评测 artifact，抽取模型、回答模型、judge 提示和预算都不同；True Memory Pro 报 93.00%，高于 Eywa 的 90.19%，且无分项。作者自己也说不能当 leaderboard 读（§5.1, §7）。
- **没有消融。** "provenance""两层校验""零 LLM 读""answer policy 分离"各自的贡献都没有被单独测过（Limitation 7）。"This validates the design choice"（§5.6）更多是推断，证据只是同一检索层配了不同模型。
- **没有不确定性估计。** 无置信区间、显著性检验，LoCoMo 仅 10 段对话，错误会在对话内相关（§7）。
- **超参来自诊断运行。** 路由权重、k、δ_p、r_min 是"从诊断运行中选出的手写常数"，没有敏感性扫描（Limitation 8）。文中没说选参数用的数据是否与测试集分开。
- **Judge 与自评。** LoCoMo 用 GPT-4o judge；BEAM 的 QA 与 judge 都是 Claude Sonnet 4.6，没有多 judge 一致性或人工审计（Limitation 6）。BEAM 是作者自建，rubric 无人工验证、无外部 baseline，且发布仍是"intended"。
- **Qwen 行不可比。** Qwen3 32B 两行用的是 dashboard reviewed 的通过率，不是 GPT-4o judge，不能与 Table 5 并列。
- **校验审计很小。** 143 个样本的审计里 67.4% 的候选事实没有 hard anchor；11/132 被拒。LoCoMo observation 库中仅 59/2,541 条事实含 hard anchor（Limitation 12），说明硬锚点校验在对话数据上覆盖很窄。
- **未评测的声明。** 修订/supersession、删除（erasure）、多进程部署、C5 对抗题都没有测试（Limitations 13, 14, 16）。provenance 只证明"有来源支持"，不证明事实为真（§1）。
- 延迟只在一个 stress store 上测，且单进程。

## Open Questions

1. 各组件（两层校验、四路加权、person demotion、preservation floor、rescue 通道）分别贡献多少？超参是否在 LoCoMo 上调过，再在 LoCoMo 上报告？
2. 写入时的 supersession 在真实纠错场景下是否可靠？preservation floor 依赖"每个状态槽至多一条 active fact"的不变量，一旦漏检会保护过期事实。
3. 删除 evidence 之后，向量索引、图、trace 和备份是否真能完全清除？论文只把它写成架构要求。

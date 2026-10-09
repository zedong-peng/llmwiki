---
title: "Back to Basics: Let Conversational Agents Remember with Just Retrieval and Generation"
updated: 2026-10-09
---

# Back to Basics: Let Conversational Agents Remember with Just Retrieval and Generation

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文、参考文献、附录 A–E 全部读完）。图 2/3/6/7/12 的雷达图和柱状图只有零散数值，图 3(b) 的部分柱值和 Fig. 2(c) 曲线无法完整还原；表格基本完好。

## Summary

问题：长期对话记忆系统（分层摘要、图结构、RL 管理等）越做越复杂，作者认为瓶颈不在记忆结构，而在"信号稀疏"（Signal Sparsity Effect）。提出 Nano-Memory：原始对话历史直接追加，不做构建和更新，只靠检索 + 生成两步（§2）。

两个观察（均在 LoCoMo 上做统计，§3）：
- Decisive Evidence Sparsity：约一半 session 有 10 个以上 turn；对 session 做均值聚合的检索，Recall@3 随 session 变长从约 0.44 降到 <0.30（Fig. 2c）。
- Dual-Level Redundancy：多数问题只需 1 个 GT session（Fig. 3a），top-3 里其余 session 是噪声；GT session 共 29,705 个 turn，其中 18,360 个与答案 token 零重叠（Fig. 3c）。仅用命中 session 生成 F1 21.09，仅用未命中 session 为 5.26（Fig. 3b）。

方法两部分：
- TIR（Turn Isolation Retrieval）：session 得分 = 其中与 query 最相似 turn 的相似度（max 而非 mean），取 top-k session。
- QDP（Query-Driven Pruning）：把 top-k session 拼起来，让一个小 LLM 按 prompt 只抽取与问题相关的原文片段，再交给生成器。

主要结果（gpt-4o-mini 生成，Contriever 检索，k=3，Table 1/2）：
- LoCoMo：Recall@3 69.39（最强基线 MemGAS 56.85），F1 22.66（MemGAS 17.66），4o-J 48.84，平均生成 token 1,403（Contriever 基线 2,348）。
- LongMemEval-s：F1 21.06 vs MemGAS 20.74；LongMemEval-m：F1 18.09 vs 16.85；LongMTBench+：F1 42.40 vs 41.49。
- 消融（Table 4/11）：LoCoMo 上 F1 15.76 -> 19.62（+TIR）-> 22.66（+QDP）；token 2,685 -> 1,403。
- 时间（Table 3）：LoCoMo 总耗时 187.96s，MemGAS 361.78s，SeCom 316.17s；无离线构建。

## Evidence and Limits

- 设置：生成器 gpt-4o-mini-2024-07-18（temp 0），换 backbone 测了 Llama3.1-8B、Gemini-2.5-Flash、gpt-5.4-mini（Table 8）；检索器 Contriever/MPNet/MiniLM（Table 9/10）；QDP 过滤器测了 Qwen2.5-3B、Llama-3.2-3B、Phi-3-mini（Fig. 9）。4×RTX A6000。基线 10 个（MPNet、Contriever、MPC、RecurSum、SeCom、HippoRAG 2、RAPTOR、A-Mem、MemGAS、Full History）。数据集 LoCoMo、LongMTBench+、LongMemEval-s/m。
- 结论与证据有出入的地方：
  - "一致优于强基线"并不完全成立：4o-J 上 LongMTBench+ 为 64.15，低于 Full History 67.44 和 MemGAS 67.71；LongMemEval-s 为 57.20，低于 MemGAS 60.20。LongMemEval-s 的 Recall@3（77.23 vs 78.51）也低于 MemGAS。文中用 F1/ROUGE 等词面指标为主，LongMemEval-s 上 F1 只领先 0.3。
  - "总时间降 48.05%"实际是相对 MemGAS（361.78s）；相对更快的 SeCom（316.17s）约降 40%。"token 降 3–5×"与 Table 2 对比对象有关：对 SeCom（1,021 token）Nano-Memory 反而更多。
  - Table 8 中 Gemini-2.5-flash 的 SeCom 行（F1 21.97、BLEU 4.12 等）与 gpt-5.4-mini 的 SeCom 行数值相同，疑似复制错误。
  - 观察部分（Fig. 2/3）是 LoCoMo 单数据集上的统计；"latent knowledge manifold"是修辞性说法，没有流形层面的测量。GT turn 的"零重叠"用 token F1 衡量，会把语义相关但无答案词的 turn 也算作填充。
  - TIR 的对照是 mean-pooling 的 turn/session 级聚合，没有和"直接 turn 级检索再合并"之类更简单的基线单独比较（Table 6 只做定性对比）。
  - 基线选用 LoCoMo 为主；RAPTOR、A-Mem、HippoRAG 2 在 LongMemEval-m 缺失（算力原因），LongMTBench+ 无检索指标。
- 自述局限（§6, D.1）：被动、无结构，缺乏主动整合和自我演化；QDP 引入串行 LLM 推理延迟；隐私、可解释性问题。

## Open Questions

- QDP 多出一次 LLM 调用，但耗时表里生成时间反而更短；过滤器本身的 token 和延迟是否计入 Table 2/3 的 "Avg. Tokens" 与总时间，文中没有明说。
- 仅取每个 session 的单个最高分 turn 做排序，对多跳/需要聚合多处证据的问题（Fig. 3a 里占少数）是否会损失？分 query 类型的结果只以雷达图给出。
- 评测集规模较小（LoCoMo 10 段对话，LongMTBench+ 11 段），单次运行、无方差或显著性检验，提升幅度的稳定性未知。

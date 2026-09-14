---
title: 长期 agent 的工作状态、范围依赖与记忆失效
domain: research
area: agent-memory
type: synthesis
status: active
updated: 2026-09-14
tags: [agent-memory, lazymem, hindsight, incremental-computation, evidence-audit]
---

# 长期 agent 的工作状态、范围依赖与记忆失效

承接 GrepQA → 自进化检索 → LazyMem 工作区调查。用户明确选择不限定对话 QA，优先寻找长期 agent 真正需要的机制。没有运行新模型或训练实验。

## 当前判断

下一版的工程落点是保存可恢复的子问题状态：当前判断、原始依据、适用条件、实际检查范围，以及下一步从哪里继续。有变化时重新打开受影响的工作；对已验证的反复错误，将经验落实为未来行动中的检查。

“保存判断、按来源/范围变化刷新”不构成已建立的新贡献。查新宽主张为 **Level 2 — High Overlap**。尚可研究的是：实际工具读取范围及语义覆盖未知的记录，能否比手工标签、目录失效和普通工作文档更好地平衡旧结论误用与维护成本。收益未测量。

## 改变判断的源码证据

[[research/agent-memory/papers/hindsight-2025/index|Hindsight]] 的本地 checkout `f75251fc5c00bcbc01d12f5dc0dcb8eeb35ec6cb`，2026-04-18：

- `hindsight-api-slim/hindsight_api/engine/memory_engine.py:7450`，`compute_mental_model_is_stale` 按 bank、tags、fact types 和创建时间检查范围内新增记忆。新增项不必是旧引用的一部分。
- 同文件 `:6967`，`refresh_mental_model` 重跑 source_query；`:7120` 之后支持结构化文档局部修订。局部编辑前仍调用 reflect，不意味着检索/推理也已完全增量化。
- `engine/retain/fact_storage.py:227` 删除引用已移除事实的 observations，并重置剩余来源等待重新 consolidation。
- `engine/consolidation/consolidator.py:635` 在启用时调度已过期 mental models 的刷新。

这是源码复核，不能把所有产品实现细节追溯为 2025 年论文原始主张。也不能因未读到某机制就断言整个系统不存在它。

## 必须保留的区分

支持引用不等于完整依赖。“共有两次旅行”的旧两条引用不变，新增第三条记录仍会改变计数。否定、最新、排名与计数判断通常依赖检查范围。文件枚举和结构化查询可有确定范围；语义 top-k 的覆盖通常未知。字面搜索零命中不能推出语义不存在。

Hindsight 已有粗粒度范围刷新，因此“只有新方案能发现旧引用以外的新增证据”这一说法不成立。[[research/agent-memory/papers/byterover-2026/index|ByteRover]] 已有 agent 自行维护的文件记忆及缓存；[[research/agent-memory/papers/memoryarena-2026/index|MemoryArena]] 已有跨会话行动依赖评测；[[research/agent-memory/papers/temporal-semantic-memory-2026/index|TSM]] 已有时间有效性和分层刷新。DBSP 的增量视图维护是机制前驱，不能把增量计算换成认知术语就算新颖。

[[research/agent-memory/threads/2026-04-30-arm-proposal-overlap-analysis|早期 ARM 笔记]] 也已经讨论空结果的价值；其中独有性断言是历史判断，本次不作为查新结论。

## 对现有工作区的含义

LazyMem 的模型循环没有把已记录的搜索/operator trace 传入后续轮次，且每题重新创建状态；修复这一点是基线工作。Darwin 某处 success 使用进程退出码，不能充当答案正确性反馈。已保存 BM25/旧 compiler 对照净差主要来自 single-hop，不能压缩成“BM25 对所有任务更好”。

工程上先复用原始来源与检索边界，增加子问题状态和变化检查。只有在正常工具历史、工作文档、Hindsight 式标签范围刷新及目录失效都不能解释收益时，才继续捍卫更复杂机制。

## 调查产物

- [完整设计判断](</Users/pengzedong/Documents/Workspace/agent-memory/research-notes/2026-09-14-memory-investigation/SYNTHESIS.md>)
- [代码和既有结果审计](</Users/pengzedong/Documents/Workspace/agent-memory/research-notes/2026-09-14-memory-investigation/FINDINGS.md>)
- [29 条记录、七个候选的查新报告](</Users/pengzedong/Documents/Workspace/agent-memory/research-notes/2026-09-14-memory-investigation/long-agent-audit/REPORT.md>)

检索限制：arXiv 限流，DBLP 连接失败，Semantic Scholar 403，OpenReview 部分限流；24 条去重搜索记录补四篇 wiki 原文和一篇经典工作。七个候选中六个完成定点原文检查；Adapton 正文获取失败，仅书目核实。不能据此声称穷尽相关工作。

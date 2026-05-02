---
title: Misc Research Threads
domain: research
area: misc
type: overview
status: active
updated: 2026-04-25
tags: [research, misc, threads, sessions]
---
# Misc Research Threads

这里记录**对话驱动**的研究线程，和 `papers/` 里的正式论文笔记分开。

适合放进来的内容：
- 一次聊天里形成的研究判断
- benchmark 选择和实验路线
- 关键概念澄清
- paper positioning / novelty 风险分析
- 暂时还不值得升级成独立 area 的想法

不适合放进来的内容：
- 单篇论文正式笔记
- 只是一句待办，没有形成判断
- 纯聊天且没有后续研究价值的内容

## Naming Rule

- 文件名格式：`YYYY-MM-DD-topic-slug.md`
- `topic-slug` 用稳定小写短语，尽量聚焦一个线程
- 如果后续同一主题继续推进，优先更新原线程页，而不是不停新建碎片页

## Recommended Template

每个线程页优先包含：
- `Context`
- `Key Judgments`
- `Definitions / Clarifications`
- `References / Evidence`
- `Benchmarks / Papers Mentioned`
- `Next Steps`

## Citation Rule For Threads

- 线程页里的关键判断尽量带上**本地文献锚点**，优先链接到 `[[../papers/<slug>]]` 或同级相关页面。
- 尤其是以下类型的句子，不应只写结论，最好同时写出对应参考：
  - “这个方向已经有人做过”
  - “某类方法在某 benchmark 上有效 / 无效”
  - “某个 benchmark 的定位 / 局限”
  - “某种 framing 更适合某个 venue”
- 如果引用的论文还不在本地 wiki 里：
  - 先在当前线程里标注为“待 ingest”
  - 后续按 `paper-ingest-protocol.skills.md` 补齐正式 paper note
- 线程页不是正式 survey，但也不应该出现大段无出处的 literature claims。

## Current Threads

- [[2026-04-19-beir-related-paper-search]]
- [[2026-04-19-beir-current-sota-snapshot]]
- [[2026-04-19-compiled-lexical-retrieval-and-rag-benchmarks]]
- [[2026-04-19-cursor-blog-reading-notes]]
- [[2026-04-20-compiled-retrieval-nips-paper-plan]]
- [[2026-04-20-code-retrieval-benchmarks-survey]]
- [[2026-04-25-llm-leaderboard-resources]]

> Agent memory 线程已迁移至 [[../../agent-memory/threads/index]]

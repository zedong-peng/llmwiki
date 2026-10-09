---
title: Super Personal Wiki Index
domain: root
type: overview
status: active
updated: 2026-10-07
tags: [index]
---

# Super Personal Wiki Index

这是总入口。先按域进入，再通过每个域的 overview 找具体页面。

## Domains

| Domain   | Page                  | Purpose                 |
| -------- | --------------------- | ----------------------- |
| Personal | [[personal/overview]] | 学业经历、个人材料、长期目标、生活事件     |
| Research | [[research/index]]    | 研究主入口；先看这里，再进入具体 area   |
| Projects | [[projects/overview]] | GitHub 项目、工程经验、可复用技术记录  |
| Admin    | [[admin/overview]]    | 证件、合同、签证、财务、手续类材料的非敏感索引 |

## Recent Research References

- [[research/llm-inference/index|Qwen3.8-27B / RTX 4090]]：广泛工程与论文检索、固定资产、g4090 推理实验及 coding CLI 部署（2026-10-01）。

- [[research/agent-memory/threads/jev-related-work|Jev 相关工作通俗对照]]：LOTUS、UtilityQwen、SCARLet、OptiSet；原文、代码可用性与 RAG 接入位置（2026-09-22）。

- [[research/agent-memory/assets/jev-system-one-2026/note|Jev / System One]]：9 月 15 日发布博客、类型化概率决策、检索 cookbook、评测与局限（2026-09-22）。

- [[research/agent-memory/assets/mem0-2025/note|Mem0 2025 paper + official experiment code]]: paper citation and public RAG baseline; separate from the 2026 release (2026-09-20).

- [[research/agent-memory/assets/mem0-2026/note|Mem0 2026 software / technical release]]: SDK 2.1.0 and evaluation archive; platform-only features, changed judge, and shared 2025 evaluation protocol decision (2026-09-20).

- [[research/misc/assets/dream-rsi-2026/note|Dream-RSI]]：Google / DeepMind 历史树回放与探索策略自改进；misc 新增 self-improving agents 小分类（2026-09-17）。

- [[research/fpga-llm-inference/index#Paper-only competition audit (2026-09-15)|FPGA 仅论文竞争核查]]：IMAX、GDN 新增深读；WPU/纯仓库排除，五篇外围论文缓存待读。

- [[research/fpga-llm-inference/index#Model input and coverage audit (2026-09-15)|FPGA 模型输入与覆盖逐项核查]]：十篇论文及公开实现、模型绑定边界、源码证据与论文索引（2026-09-15）。

- [[research/llm-inference/index]]：LLM 推理关键论文地图；10篇TeX/PDF、vLLM/SGLang重点阅读、8篇定向阅读、8个官方仓库缓存（2026-09-14）。

- [[research/fpga-llm-inference/index]]：FPGA LLM 推理（U280 llama.cpp/GGML 主线、系统地图、评测协议、CODO 对照、VSTC 提案与失败审计；09-09 已折入证据矩阵/审计/复核/KV 边界；论文库见 assets/，原始 IdeaSpark 运行见 threads/）。
- [[research/fpga-llm-inference/index|FPGA LLM 证据复核]]：论文实验和交付证据复查（SECDA 集成边界、FlexLLM 精度、CODO 发表信息；2026-09-08）。
- [[research/fpga-llm-inference/index|FPGA backend 生态审计]]：对照准入、公开复现与替代边界（SECDA/Positron/Achronix/原生 backend）。
- [[research/fpga-llm-inference/index|FPGA LLM 证据矩阵]]：对照谓词与行判（New-model entry、Resident exec.、E2E、公开 artifact）。
- [[research/fpga-llm-inference/index|KV-cache 边界]]：K/V 计算、持久状态、KV 优化三层区分与执行对象决定指标。

## Operating Files

| File | Purpose |
|---|---|
| [[log]] | 追加式维护日志 |
| [[projects/karpathy-llm-wiki]] | 本库设计来源 |
| `AGENTS.md` | 维护规则 |
| `raw/` | 可安全纳入仓库的原始资料入口 |

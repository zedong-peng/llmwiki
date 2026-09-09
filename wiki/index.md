---
title: Super Personal Wiki Index
domain: root
type: overview
status: active
updated: 2026-09-07
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

- [[research/fpga-llm-inference/index]]：FPGA LLM 推理（U280 llama.cpp/GGML 主线、系统地图、评测协议、CODO 对照、VSTC 提案与失败审计；09-09 已折入证据矩阵/审计/复核/KV 边界；论文库见 papers/，原始 IdeaSpark 运行见 threads/）。
- [[research/fpga-llm-inference/index|FPGA LLM 证据复核]]：论文实验和交付证据复查（SECDA 集成边界、FlexLLM 精度、CODO 发表信息；2026-09-08）。
- [[research/fpga-llm-inference/index|FPGA backend 生态审计]]：对照准入、公开复现与替代边界（SECDA/Positron/Achronix/原生 backend）。
- [[research/fpga-llm-inference/index|FPGA LLM 证据矩阵]]：对照谓词与行判（New-model entry、Resident exec.、E2E、公开 artifact）。
- [[research/fpga-llm-inference/index|KV-cache 边界]]：K/V 计算、持久状态、KV 优化三层区分与执行对象决定指标。

## Operating Files

| File | Purpose |
|---|---|
| [[log]] | 追加式维护日志 |
| `sources/catalog.md` | 原始资料登记和敏感性分类 |
| `inbox/` | 临时放待处理笔记或待 ingest 清单 |
| `raw/` | 可安全纳入仓库的原始资料入口 |

## First Migration Targets

| Source | Target | Notes |
|---|---|---|
| Existing research map wiki | `wiki/research/` | core pages migrated on 2026-04-14; can continue incremental cleanup |
| `Documents/Personal Info` | `wiki/admin/` + `wiki/personal/` | 只建非敏感索引，不复制证件扫描件 |
| `Documents/SJTU_Master_CompSci` | `wiki/personal/education/` | 学业、成绩、学术报告、硕士手续 |
| `Documents/GitHub/*` | `wiki/projects/` + `wiki/research/` | 项目说明、实验记录、论文线索 |

## Open Questions

- 哪些页面未来会公开，哪些只在本地使用？
- Research wiki 是复制迁移，还是保留原仓库并在这里建立入口页？
- 个人材料是否需要按“申请/报销/签证/落户/实习”建立 checklist？

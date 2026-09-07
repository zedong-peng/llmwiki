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

- [[research/fpga-llm-inference/vitis-ai-dpu-finn-pynq]]：Vitis AI DPU、FINN 与 PYNQ/PINN 消歧，工具链架构、官方资料和 U280 LLM 部署边界。

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

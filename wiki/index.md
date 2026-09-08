---
title: Super Personal Wiki Index
domain: root
type: overview
status: active
updated: 2026-09-08
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

- [[research/fpga-llm-inference/manuscript-evidence-recheck-20260908]]：复查论文的实验和交付证据，区分 SECDA 初步集成、完整生成入口及固定图计时；纠正 FlexLLM 精度和 CODO 发表信息。

- [[research/fpga-llm-inference/backend-niche-and-baseline-audit]]：按实验数据、公开复现路径和发表记录筛选对照；核查 SECDA、Positron、Achronix 与原生 FPGA backend 的可替代性和公开价值。
- [[research/fpga-llm-inference/feature-level-evidence-matrix]]：九项实验工作加本地 FPGA backend；SECDA 转为正文集成先例，本地正确性未通过及公开 artifact 未核实均明确标注。

- [[research/fpga-llm-inference/vitis-ai-dpu-finn-pynq]]：Vitis AI DPU、FINN 与 PYNQ/PINN 消歧，工具链架构、官方资料和 U280 LLM 部署边界。
- [[research/fpga-llm-inference/kv-cache-runtime-boundary-comparison]]：区分 K/V 计算、持久 KV 状态、KV-specific 优化，以及 fixed-graph 与完整 runtime 的测量边界。

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

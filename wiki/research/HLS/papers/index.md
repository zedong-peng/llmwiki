---
title: HLS Papers Directory
domain: research
area: HLS
type: overview
status: active
updated: 2026-09-08
tags: [research, hls, papers, guide]
---

# HLS Papers Directory

`papers/` 下每个子目录对应一篇论文，均以 `index.md` 为入口。

## Conventions

- 目录名：`<slug>-<year>`，小写连字符。
- 每个 `index.md` 带 YAML frontmatter（`type: paper`，`status: processed`）。
- 已归档资产：论文 PDF、TeX source（`source/archives/` + `source/extracted/`）、官方代码（`repo/`，如有）。

## Papers

| Paper | Year | Venue | Assets |
|---|---|---|---|
| [Hierarchical GNN QoR](hierarchical-gnn-qor-2024/index.md) — 分层 GNN 从 C/C++ 源码直测 post-route QoR，支持 pragma | 2024 | arXiv | PDF + TeX source |
| [MPM-LLM4DSE](mpm-llm4dse-2026/index.md) — 图-文多模态 QoR 预测 + LLM-driven DSE | 2026 | DATE | PDF + TeX source + repo |

两篇共同主题：HLS 设计空间探索（DSE）的 QoR 预测。前者用纯 GNN 分层建模，后者加源码语义（CodeBERT）与 LLM 做优化器。

返回 [[research/HLS/index|HLS 总索引]]。

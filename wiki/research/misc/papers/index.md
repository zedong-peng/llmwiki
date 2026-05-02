---
title: Misc Papers Directory Guide
domain: research
area: misc
type: overview
status: active
updated: 2026-04-19
tags: [research, misc, papers, directory-guide, ingest]
---
# Misc Papers Directory Guide

这里解释 `wiki/research/misc/papers/` 的**目录组织方式**，和单篇论文目录内部的标准结构。

如果你只是想找某篇论文，先回到 [[../index]]。  
如果你想知道这里为什么这样排、每个文件夹里应该有什么，看本页。

## Purpose

`papers/` 存放的是**单篇论文或单个系统条目**的正式主笔记。

每个子目录对应一个稳定 slug，例如：
- `bright-2025`
- `coral-2024`
- `ragchecker-2024`

这些条目通常来自：
- arXiv 论文
- 官方工程博客 / 系统文章
- 官方代码仓库
- 少数 repo-first / source-collection 型系统条目

## Per-Paper Directory Layout

标准结构如下：

```text
wiki/research/misc/papers/<paper-slug>/
├── index.md
├── metadata.yaml
├── <downloaded>.pdf
├── source/
│   ├── archives/
│   └── extracted/
└── repo/<repository-name>/
```

### Required Files

- `index.md`
  正式主笔记。只有在读过 source / PDF 后才写。

- `metadata.yaml`
  记录：
  - arXiv / repo / PDF 链接
  - 下载状态
  - source 是否解压
  - 实际 reading source
  - ingest 状态

### Optional But Common

- `<downloaded>.pdf`
  保留原始下载文件名，方便追溯来源。

- `source/archives/`
  放原始 arXiv source / e-print 压缩包或原始 source 文件。

- `source/extracted/`
  放解压后的 TeX/source 文件；如果 `tex_available: true`，原则上这里应当存在可读内容。

- `repo/<repository-name>/`
  git clone 官方 GitHub 仓库；如果只是 placeholder README，也要在 `index.md` 里明确写清楚。

## Ingest Priority

本目录遵循当前 wiki 的论文 ingest 规则：

`arXiv TeX/source > official GitHub repo > PDF fallback`

也就是说：
- 只要有 source，就优先读 source
- 只把 source 下载下来但不解压，不算完成 ingest
- `index.md` 不是占位文件，而是读完后的正式摘要页

## Status Semantics

常见状态来自 `metadata.yaml`：

- `queued`
  只知道这篇论文，还没下载

- `downloaded`
  source / repo / PDF 至少有一项已下载

- `extracted`
  source 已解压到 `source/extracted/`

- `read`
  已读过 source 或 PDF

- `processed`
  已写完正式 `index.md`

## What `index.md` Should Contain

单篇论文页一般应覆盖：
- Paper Meta
- TL;DR
- Problem
- Method
- Benchmarks / Datasets
- Baselines
- Main Results
- Ablations / Analysis
- Implementation Clues
- Limitations
- Takeaways
- Open Questions

目标不是逐字转述论文，而是让几天后快速回看时仍然能抓住：
- 这篇论文在做什么
- 为什么和当前线程相关
- 哪些数字和实现细节值得记住

## What Belongs Here vs Elsewhere

适合放在 `papers/`：
- 单篇论文正式笔记
- 单个系统 / 博客 / repo 的正式条目

不适合放在 `papers/`：
- 会话总结
- brainstorming
- 多篇论文交叉比较但还没有沉淀成单篇条目

这些更适合放在：
- `[[../threads/index]]`

## Notes On Snapshot Counts

`[[../index]]` 里的 snapshot 指标主要统计：
- paper directories
- per-paper `index.md`
- `metadata.yaml`
- source / repo / PDF 覆盖率

本页本身是 `papers/` 目录说明，不属于某一个 paper slug，不应混入“paper directories”统计口径。

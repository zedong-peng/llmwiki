---
title: Agent Memory Papers Directory
domain: research
area: agent-memory
type: overview
status: active
updated: 2026-07-27
tags: [research, agent-memory, papers, guide]
---

# Agent Memory Papers Directory

`papers/` 下每个子目录对应一篇论文或一个语料库,均以 `index.md` 为入口。

## Conventions

- 目录名: `<slug>-<year>`,小写连字符;同名论文冲突时加区分词(如 `prism-memory-2026` vs `prism-2025`)。
- 每个 `index.md` 带 YAML frontmatter(`type: paper`,`status: stub | processed`)。
- `processed` 页面可附 `metadata.yaml`、`<arxiv-id>.pdf`、`source/`(TeX 源)、`repo/`(官方代码)。
- `stub` 页面仅含 Paper Meta、TL;DR、本地文件指针与研究关联。

## Special Directories

- [lazymem-related-work](lazymem-related-work/index.md) — 冻结的 45 篇 LazyMem 相关文献语料库(type: synthesis),内含 PDF/text/校验和;其成员论文各有独立 stub 页。

完整论文列表见 [Agent Memory 总索引](../index.md)。

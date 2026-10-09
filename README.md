# LLM Wiki

个人知识库：个人资料、科研、项目、行政材料放在同一个 markdown wiki 里，由 LLM agent 维护。设计来源见 [`wiki/projects/karpathy-llm-wiki.md`](wiki/projects/karpathy-llm-wiki.md)。

- 入口：[`wiki/index.md`](wiki/index.md)
- 维护规则：[`AGENTS.md`](AGENTS.md)
- 论文归档、查询、校验：[llmwiki-skill](https://github.com/zedong-peng/llmwiki-skill)
- `raw/` 只放可公开的原始资料，敏感文件留在原处

## 使用

查询使用 `llmwiki-query`，收录和校验使用 `llmwiki-collect`。归档采用 `citation.bib` 与实际阅读后的 `note.md`；未读线索保存在 topic 的 `threads/`。`wiki/research/dlm` 是独立研究项目子模块，参考资料采用同样的归档布局，活跃论文仍保留在 `paper/`。

维护后检查内部链接、引用 key、原文资产和阅读范围；旧的 `lint_wiki.py` / `fetch_assets.py` 已不再使用。

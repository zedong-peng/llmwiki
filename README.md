# LLM Wiki

个人知识库：个人资料、科研、项目、行政材料放在同一个 markdown wiki 里，由 LLM agent 维护。设计来源见 [`wiki/projects/karpathy-llm-wiki.md`](wiki/projects/karpathy-llm-wiki.md)。

- 入口：[`wiki/index.md`](wiki/index.md)
- 维护规则：[`AGENTS.md`](AGENTS.md)
- 论文归档、查询、校验：[llmwiki-skill](https://github.com/zedong-peng/llmwiki-skill)
- `raw/` 只放可公开的原始资料，敏感文件留在原处

## 检查

```sh
python3 /path/to/llmwiki-skill/skills/llmwiki/scripts/lint_wiki.py .
```

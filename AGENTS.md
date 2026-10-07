# Super Personal Wiki Schema

长期维护的个人 wiki，由 LLM agent 维护。论文归档、查询、校验的规则以 llmwiki skill 为准（<https://github.com/zedong-peng/llmwiki-skill>，`references/protocol.md` 是目录布局的唯一规范）。这里只写本库特有的约定。

## 维护位置

- 任意 clone 都可以改，GitHub origin 为准：先 pull，改完 push。
- 被 Git 忽略的缓存（`github-repo/`、`paper-tex/archives/`）只存在于下载它的那台机器，来源和哈希记在 `metadata.yaml`。
- 不在 FPGA 服务器上维护副本；远端实验结果回写到某个 clone 再推送。

## 目录

```text
AGENTS.md  README.md  raw/
wiki/
  index.md  log.md            # 总索引；唯一的追加式日志，新条目在最前
  personal/ admin/ projects/  # 各域 overview 与页面
  research/
    index.md                  # area 目录
    <topic>/
      index.md  threads/  assets/<ref_slug>/
```

`wiki/research/dlm` 是 git submodule（独立项目），不按论文归档处理。

## 隐私

- 证件、护照、银行卡、户口、成绩单、合同、体检、签证、recovery code 不进仓库，只写元数据页：是什么、存在哪、用途、有效期。
- 不写账号、证件号、电话、住址、API key。

## Frontmatter

```yaml
---
title: Page Title
domain: personal | research | projects | admin
area: optional-area-slug
type: overview | source | concept | paper | comparison | engineering | project | person | timeline | checklist | synthesis | note
status: seed | active | stable | stale
updated: YYYY-MM-DD
tags: []
---
```

`status` 只描述页面。论文的处理进度（queued → processed）只写在 `metadata.yaml`。

## 链接

- Obsidian 风格 `[[research/<topic>/assets/<slug>/index]]`；文件名小写加连字符；slug 全库唯一。
- 新页面必须能从 `wiki/index.md` 或所属 topic 的 `index.md` 到达。
- 保留历史 slug，不为统一而改名。

## 工作流

- 录入论文、校验、迁移：按 skill。
- 每次改动后运行 `python3 <skill>/scripts/lint_wiki.py .`，错误清零再提交。
- 回答问题：先读 `wiki/index.md`，再用 `rg` 找页面，引用本地路径；有长期价值的结论写回 wiki。

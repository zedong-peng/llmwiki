# LLM Wiki

个人知识库。查询使用 `llmwiki-query`，收录与归档校验使用 `llmwiki-collect`（<https://github.com/zedong-peng/llmwiki-skill>）。这里只补充本库约定，检索、阅读和整理方法按任务选择。

## 内容与目录

```text
wiki/
  index.md                    # 总入口
  log.md                      # 维护日志，新条目在前
  personal/ admin/ projects/
  research/
    index.md                  # 研究方向目录
    <topic>/
      index.md                # 主题索引
      threads/                # 想法、草稿、未读线索、工程与实验记录
      assets/<slug>/          # 外部参考文献及其原始资料
        citation.bib          # 引用 key 与 slug 一致
        note.md               # 实际阅读或源码核验记录，按需存在
        paper-pdf/
        paper-tex/
        github-repo/
```

- `assets/` 收录论文、博客、技术文档或外部开源项目等参考资料。本机部署、工具安装、benchmark 和运行日志放在 `threads/` 或 `wiki/projects/`，不包装成参考文献。
- `note.md` 如实记录阅读范围与证据；未读摘要放在 `threads/` 并标明未读。没有 note 表示没有阅读记录，下载或迁移不等于阅读。
- 保留既有 slug，全库唯一；跨主题引用同一份归档。页面从总索引或主题索引可达；链接可用 `[[research/<topic>/assets/<slug>/note]]` 或相对 Markdown 路径。
- 页面 frontmatter 保留 `title`、`updated`；其他字段按内容需要使用。
- `dlm` 是独立 Git 子模块，参考资料使用同样布局，`paper/` 保留活跃论文源码与产物；分别检查父库和子模块的改动。

## 检索与维护

- 检索限定到相关 topic、slug 或文件；不要从仓库根或 `wiki/` 递归扫描原文与代码缓存。全库统计用脚本汇总，只输出结果。
- 查询引用实际使用的证据，不自动写回。整理后更新相关索引与日志，检查内部链接、引用 key 和来源记录。
- Git 跟踪笔记、引用、PDF 和完整 TeX 解压目录。TeX 压缩包与官方代码缓存按 `.gitignore` 处理，可按 URL、版本、hash、commit 恢复。
- `citation.bib` 中旧 metadata 注释是迁移时保留的历史快照，不是当前资产状态；无需新建 `metadata.yaml`。缺失证据如实说明。
- 同步前核对未提交改动，保留其他会话的工作和已明确删除的内容。不在 FPGA 服务器维护副本，远端实验记录回写本地。
- 普通检索、下载、解压、解析工具可用；执行下载的研究代码及其安装或构建脚本需有任务授权。

## 隐私

证件、银行卡、合同、体检、签证、recovery code 等敏感原件不进仓库，只记录用途、有效期和存放位置。不写账号、证件号、电话、住址或 API key；`raw/` 只放可公开资料。

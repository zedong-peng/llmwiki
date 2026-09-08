理解和整理论文时，遵循这个最小协议。

## 核心原则

- 优先级固定：`arXiv TeX/source > 官方 GitHub repo > PDF fallback`
- 必须先下载、解压、阅读，再写 `index.md`
- 有 arXiv source / TeX 时必须读 source；不能只读 PDF
- source 只下载未解压、未阅读时，不算完成 ingest
- `index.md` 是正式论文笔记，不是占位文件
- 未读完时只能更新下载状态或 `metadata.yaml`，不能标记为 `processed`

## 工作流

1. 识别来源
   - arXiv abs、PDF、source / e-print
   - 官方 GitHub repo
   - 补充材料

2. 下载材料
   - 先下载 arXiv source / e-print
   - 再下载官方 repo 到 `repo/<repo-name>/`
   - 最后下载 PDF
   - 保留原始文件名，例如 `2405.14831.pdf`、`2405.14831-source.tar.gz`

3. 解压 source
   - 原始 source 放入 `source/archives/`
   - 解压到 `source/extracted/`
   - 支持 `tar.gz`、`zip`、`tar`、gzip tex、单个 `.tex` 等格式
   - 解压失败时，在 `metadata.yaml` 记录原因

4. 阅读 source
   - 优先读主 tex：`main.tex`、`paper.tex` 或会议模板入口
   - 继续读章节、附录、表格、ablation、implementation details
   - 读 `.bib` / `.bbl` 以理解相关工作和引用
   - 必须从内容中提取方法、实验、结论，而不只是确认文件存在

5. 阅读 repo
   - 读 `README.md`、入口脚本、训练/评测脚本、配置、数据处理和关键模块
   - 记录方法如何落地、运行入口、关键超参、数据格式、论文与代码是否一致

6. PDF fallback
   - 只有在没有 source、source 下载/解压失败且无法修复，或 source 严重缺失时才使用 PDF fallback
   - 必须在笔记和 metadata 中写明：`TeX unavailable, used PDF fallback.`

7. 写笔记和 metadata
   - 读完 source 或 fallback PDF 后，再写 `index.md`
   - `metadata.yaml` 记录链接、下载状态、解压状态、阅读来源和 ingest 状态

## 目录结构

```text
wiki/research/<topic>/papers/<paper_slug>/
  index.md
  metadata.yaml
  <original-filename>.pdf
  source/
    archives/
    extracted/
  repo/<original-repository-name>/
```

- `<topic>` 默认用 `misc`，除非用户指定或明显属于已有主题
- `index.md` 是正式主笔记
- `metadata.yaml` 记录来源和处理状态

## Cache 规则

- 本地已有文件即 cache，只用于避免重复下载
- 下载 PDF 前检查论文目录是否已有对应 PDF
- 下载 source 前检查 `source/archives/` 是否已有对应 archive
- 已有 source 仍必须继续解压和阅读
- cache 不代表已解压、已阅读或已 processed

## ingest 状态

- `queued`：只知道论文，尚未下载
- `downloaded`：PDF/source/repo 至少一项已下载
- `extracted`：source 已解压到 `source/extracted/`
- `read`：已读 source 或 PDF，并能提取主要信息
- `processed`：已完成正式 `index.md`

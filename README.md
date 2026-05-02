# LLM Wiki

这是一个“超级个人 wiki”的工作区：个人资料、科研地图、项目记录、行政材料、长期目标都可以逐步汇入同一个知识系统。

核心原则：

1. `wiki/` 是可阅读、可维护、可链接的 markdown 知识层。
2. `raw/` 是原始资料入口，只放可安全纳入仓库的材料或说明，不直接复制敏感证件、银行卡、护照、成绩单等文件。
3. `wiki/index.md` 是总索引，`wiki/log.md` 是按时间追加的操作日志。
4. 每次新增资料时，先进入 `inbox/` 或 `sources/catalog.md`，再由 LLM 归档到合适的 wiki 页面。
5. Research wiki 后续合并到 `wiki/research/`，不要和 personal/admin 材料混在同一层。

## Start Here

- 入口页：[`wiki/index.md`](wiki/index.md)
- 维护规则：[`AGENTS.md`](AGENTS.md)
- 资料登记：[`sources/catalog.md`](sources/catalog.md)
- 待处理区：[`inbox/README.md`](inbox/README.md)
- 原始资料说明：[`raw/README.md`](raw/README.md)

## 建议的第一阶段

1. 先把已有 research wiki 迁移到 `wiki/research/`，保留原来的 area 结构。
2. 给个人资料建立高层索引，不复制敏感文件，只记录“类型、用途、存放位置、有效期、注意事项”。
3. 每次只 ingest 一个小主题，例如“硕士材料”“CV/申请材料”“DiffHLS 论文线索”。
4. 每次 ingest 后更新 `wiki/index.md` 和 `wiki/log.md`，让这个库逐步变成你的长期记忆层。

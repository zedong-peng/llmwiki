---
title: "zvec-grep (zg)"
updated: 2026-10-09
---

# zvec-grep (zg)

开源工具，无对应论文。zvec-ai 组织发布（基于阿里 [zvec](https://github.com/alibaba/zvec) 向量库），Apache-2.0，npm 包 `@zvec/zvec-grep` 0.2.1。阅读范围：README、`docs/04-pipeline.md`、`docs/05-architecture.md`、`benchmarks/` 下三份 README，以及 `src/engine` 中的融合代码；commit `a09cd1236eee003feb699a17c5bf63d76f83f06c`（2026-10-09）。未运行代码。

## Summary

把 ripgrep、BM25 与向量检索放在同一个本地 CLI / MCP 接口后面，给人和 coding agent 共用。

- 两条检索路径：带索引的排序检索（BM25/FTS + 向量，RRF 融合），以及不需要索引、默认穷举的 managed ripgrep（`docs/05-architecture.md`）。
- 融合用 RRF，`k = 60`：`src/engine/pipeline/search/index.ts:77, 1154`；跨查询组的上下文合并另有一处同样的 RRF（`src/engine/service/zvec-grep.ts:2038`）。
- 索引按格式切分：C/C++、Go、Java、JS/TS、Python、Rust 用 tree-sitter 提取符号、签名和 breadcrumb；Markdown 按标题分节；其他文本按块切。PDF、Office 文档和压缩包不索引（`docs/04-pipeline.md`）。
- 默认本地 embedding（如 `local/potion-code-16m-v2`）；选远程 embedding 前需逐次或按工作区授权。索引存于 `<workspace>/.zvec-grep/`，结果标注 `fresh` / `possibly_stale`。
- agent 通过 `zg install --target <agent>` 接入本地 Streamable HTTP MCP，支持 Claude Code、Codex、Cursor、OpenCode 等。

## Evidence and Limits

以下是仓库自报的结果，未在本地复现。

- 评测方式是成对 A/B：同一 agent、模型、提示词和预算，treatment 只多出预建索引、zg 工具和通用使用说明；索引构建时间单列，不计入 agent 时间（`benchmarks/README.md`）。
- BrowseComp-Plus：100 题 × 3 次成对试验，Codex `gpt-5.6-sol`，embedding 用 Qwen3.7。准确率 98.67% → 99.00%，输入 token 1.68M → 1.05M，工具调用 25.42 → 14.36，agent 时间 259.4 s → 159.3 s。主 README 写 medium reasoning，benchmark README 写 `high`，两处不一致。
- SWE-QA-Bench：从 `peng-weihan/SWE-QA-Bench` 选出 20 道"检索密集"题，覆盖 11 个仓库；Claude Code 2.1.212 + Claude Opus 5（high），每题每组 3 次。结果只给图，没有数字表。题目是按适合检索挑的，不能代表一般编码任务。
- CI 的方差表显示，同一题多次运行之间分数波动很大（如 `conan:39` 基线 5–92、zg 5–100），单次运行的差异不可靠；仓库自己也建议看多次运行的均值。
- 结果依赖 agent 自己决定何时调用 zg；仓库说明称，第一次调用失败的话，agent 往往整轮放弃这个工具。

## Open Questions

- 只换 embedding 模型（本地 potion 对比 Qwen3.7）时，收益还剩多少？公开结果都用远程 Qwen3.7。
- 和 agent 自带 grep 的差距里，有多少来自排序检索本身，有多少来自更紧凑的输出格式？两者没有分开做消融。

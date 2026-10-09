---
title: "Agentless: Demystifying LLM-based Software Engineering Agents"
updated: 2026-10-09
---

# Agentless: Demystifying LLM-based Software Engineering Agents

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：PDF 全文文本的正文（§1–§8）；附录无，其后为参考文献（已略读）。图 1、5、7、8、9 的文字提取有乱码，只依据正文描述与表格数字；Table 2 中 multi-samples 行的数字有错位，未引用。

## Summary

问题：SWE-bench 上的主流方案都是让 LLM 自主选工具、决定下一步的 agent，设计复杂、难调试、自我反思能力弱。作者质疑是否真的需要 agent (§1)。

方法：AGENTLESS 固定为三阶段流水线，LLM 不决定后续动作，也不使用复杂工具 (§3)。
- 定位：先把 repo 转成类似 tree 的目录结构，让 LLM 选 top-N 可疑文件，再与 embedding 检索结果（先让 LLM 过滤无关目录，chunk 512）取交集合并；然后用只含类/函数声明的 skeleton 定位到类和函数，最后在这些代码上定位到具体 edit location (§3.1)。
- 修复：在 edit location 上下各 10 行的窗口内，让 LLM 生成 Search/Replace 形式的 diff；4 组 edit location，每组 1 个 greedy 加 9 个采样 patch，共 40 个 (§3.2, §4)。
- 验证：LLM 生成 40 个 reproduction test，只保留在原 repo 上输出 "Issue reproduced" 的，归一化后取出现次数最多的一个；回归测试集由现有通过测试减去 LLM 判定可能需要改动的测试得到。先按回归失败数最少筛选，再按 reproduction test 筛选，最后用 AST 归一化后的多数投票选 patch (§3.3)。

结果 (GPT-4o, SWE-bench Lite 300 题)：
- 解决 96 题 (32.00%)，平均 $0.70，78,166 tokens，是所有开源方法中最高 (Table 1)。表中更高的都是闭源或商业系统（如 CodeStory Aide 43.00%、MarsCode 39.33%）。
- 对比开源 agent：SWE-agent GPT-4o 18.33%/$2.53，Moatless Claude 3.5 S 26.67%/$0.17，AutoCodeRover-v2 30.67%。
- 消融：patch 选择只用多数投票为 77，加回归测试为 81，再加 reproduction test 为 96 (Table 4)；分层定位优于从文件直接到 edit location，skeleton 优于完整文件 (Table 2)；约 40 个采样后性能饱和，若 oracle 选 patch 可达 126 (42.0%) (§5.2.2)。
- 作者人工标注 SWE-bench Lite：4.3% 的题目描述里含完整 ground-truth patch，10.0% 信息不足，5.0% 含误导性解法 (§6.1)。剔除后得到 249 题的 Lite-S，各方法排名变化很小 (Table 5)。
- SWE-bench Verified 500 题上解决 194 题 (38.80%)，GPT-4o 方案中最高 (Table 6)。

## Evidence and Limits

- 主结论是"简单流水线可与 agent 竞争"，证据是单一模型 (gpt-4o-2024-05-13) 在单一基准族上的对比。结论支撑了"不必要复杂 agent"在该设定下成立，但没有受控地比较"同一模型、同一预算"下的 agent 与 non-agent。
- 基线数字直接取自排行榜或各自论文，LLM、采样预算、是否用 hidden test 等并不一致；多数闭源基线无轨迹，无法核验 (§4)。成本对比同样来自各方报告，且 Table 1 中很多基线没有成本。
- Agentless 每题采样 40 个 patch 和 40 个 reproduction test，成本未含的部分是推理次数大，$0.70 是均值。其自身的回归测试需要执行整个现有测试集，执行环境成本未计入。
- 作者没有使用 SWE-bench 提供的 PASS_TO_PASS，而是自行筛选回归测试；脚注称若直接使用则 Lite 成绩为 98（原文如此）。评测环境经修改以便执行任意测试。
- reproduction test 质量有限：300 题中 213 个能复现问题，但在 ground-truth patch 下只有 94 个输出 "Issue resolved" (§5.1.3)。
- 局限（作者自述）：无任何位置线索的题上，闭源 agent 优于 Agentless (§6.2)；可能存在 GPT-4o 训练数据泄漏，无法排除 (§7)；只评测 SWE-bench 系列，泛化未验证。
- 作者称 OpenAI 采用并"确认"了其思路（SWE-bench Verified），这是正文的自述，依据外部报告，并非本文实验。
- 文中 Lite 的 "exact patch / misleading / not enough info" 标注由作者人工完成，未报告标注者一致性。

## Open Questions

- 在同一底座模型和同等采样/成本预算下，agent 方案与固定流水线的差距有多大？表 1 的跨系统对比不能分离出"是否 agent"这一因素。
- 无位置线索的题目上 agent 更强，说明固定的层次定位在检索难题上受限；这类题的占比与 Agentless 失败的关系未量化。
- 采样 40 个 patch 的 oracle 上限 126 与实际 96 之间差距较大，更好的 patch 选择能否缩小，文中没有给出验证。

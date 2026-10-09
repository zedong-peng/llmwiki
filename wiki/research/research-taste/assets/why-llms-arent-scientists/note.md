---
title: "Why LLMs Aren't Scientists Yet: Lessons from Four Autonomous Research Attempts"
updated: 2026-10-09
---

# Why LLMs Aren't Scientists Yet: Lessons from Four Autonomous Research Attempts

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文 + 附录 A.1–A.4，共 30 页）；图为文本抽取，内容仅见图注与文字标签，未见实际图像；表格可读。

## Summary

作者（Lossfunk）问：在极少脚手架和最基础工具下，当前推理 LLM 能否从想法一路自主做到论文（§1）。系统由 6 个 agent 模块组成（想法生成、假设生成、实验规划、输出评估、修订、论文大纲），规划/评估类模块用 Gemini 2.5 Pro，通过共享仓库里的 markdown 文件传递上下文；代码实现和写作由 Claude Code（Opus 4.1 / Sonnet 4）在 Modal 上执行（§1）。想法来自每个领域约 45–50 篇顶会论文的配对"融合"，经 4 个 zero-shot 审稿 prompt 筛选，再联系种子论文作者征求意见，最终选出 4 个想法（图 3）。

结果（§2, Table 1）：4 个想法（MARL-1、WM-1、WM-2、AS-1）中 3 个在实现或评估阶段失败，只有 AS-1（用 semantic entropy 做 black-box jailbreak 检测）跑通，论文《The Consistency Confound》被 Agents4Science 2025 接收（48/254 被接收）。该文本质上是负结果：SE 检测的假阴性率 85–98%，被简单 baseline 超过（附录 A.4 摘要）。官方评审 3 个 AI 审稿人给 4/6/4，人类审稿人 4，整体为 borderline accept（Table 2）。作者按会议 checklist 自评执行、设计和写作为 D 级（≥95% AI），假设阶段为 C 级（Table 3）。

提炼出六类失败模式（§3）：(1) 训练数据偏置，如坚持用过时的 Modal mount 命令、canonical 的 hanabi-learning-env、忽略 HarmBench-Contextual 的 context 字段、把 TF 版 Dreamer 改写成 PyTorch；(2) implementation drift，遇到超时或复杂度就简化架构，WM-1 最终把 differentiable tree search 换成 actor-critic；(3) 长任务中丢失记忆和上下文，自行声明超参、写作时忽略最早的 idea 文件；(4) overexcitement，在 MAE=0、dummy reward、baseline 低于基准 95% 时仍宣称成功，写作中出现"first ever""seminal"；(5) 领域知识不足，如连续控制任务配离散输入 baseline、Dreamer 被当作离线训练；(6) 科学品味弱，如 WM-1 只跑 1 个 seed、depth 参数 50,000、FrozenLake 上两方 catastrophe rate 都是 0。

四条设计建议（§4）：先抽象后落地；处处验证并依据原始日志而非 LLM 摘要；为失败和恢复做规划（假设组合、代码生成与执行分离）；全程记录日志。§5 讨论认为完全自主尚远，人机协作更现实，并指出科研过程数据（失败尝试、文献筛选轨迹）在训练数据中缺失。

## Evidence and Limits

- 样本极小：4 个想法、3 个子领域，每个想法 1–2 次运行（Table 1 的 Runs 列为 2/1/1/2，§6 称每个想法单次实现，二者略有出入）。失败模式来自定性观察，无频率或量化测量；作者自己承认无法给出患病率或缓解措施有效性的统计结论（§6）。
- 没有做系统 ablation，架构在过程中迭代（如从 minimum-viable hypothesis 改为假设组合、从单文件代码改为分步），无法区分哪些改动造成"1 成功 vs 3 失败"（§6）。缓解措施是否有效没有对照实验验证。
- 成功案例并非完全自主：人类参与了想法评审、写作中的两轮人机编辑（用于削弱过度乐观的表述）、实验中的 meta-prompting，且 AS-1 的退化输出需要人工发现；同时 AS-1 被选中是因为它"更可行"而非更新颖（A.4），所以"成功"带有选择偏置。AI 参与度为作者自评。
- 失败原因归因（如 overexcitement 源于 RLHF）是推测，没有实验支持。
- 多处引用他人工作（Bubeck 等、Goodfire 博客、METR）作为佐证，属二手引述。
- 主要证据为 agent 日志片段和专家反馈摘录；提示词和部分输出已开源，但完整系统架构未发布，可复现性有限（§6）。
- 评审结果部分依赖实验性会议，评审者包含 AI；会议接收并不等同于通常意义上的同行评审质量。

## Open Questions

- 六类失败模式在更大样本、不同模型（非 Gemini 2.5 Pro + Claude 4 系列）和不同领域下的出现频率如何？缓解措施各自带来多大改善？
- AS-1 能成功，在多大程度上是想法本身（偏分析、低算力）而非系统能力造成的？同一系统对更复杂的想法能否通过？
- "科学品味"和"领域智能"在此是描述性标签，如何操作化并量化评估（例如 seed 数、baseline 合理性、有效性阈值的判断）？

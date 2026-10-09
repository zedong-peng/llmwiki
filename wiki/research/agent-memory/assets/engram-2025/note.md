---
title: "ENGRAM: Effective, Lightweight Memory Orchestration for Conversational Agents"
updated: 2026-10-09
---

# ENGRAM: Effective, Lightweight Memory Orchestration for Conversational Agents

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文 §1–7、附录 A–D，arXiv:2511.12960v2）。图 1、图 3 和附录 A.2 的曲线图只有提取出的文字标注，无法核对图形本身；表格数字清晰。

## Summary

问题：对话 agent 需要长程一致性，而现有记忆系统常用知识图谱、多阶段检索或 OS 式调度器，工程复杂、难复现（§1）。

方法：ENGRAM 把每个 user turn 经单个 router（LLM prompt 输出三位 mask）分配到 episodic / semantic / procedural 三类存储，各类有固定 schema（episodic: 标题、摘要、时间锚；semantic: 事实串；procedural: 标题与步骤），连同 embedding 存入 SQLite（§3.2–3.3）。查询时对三类各取 top-k（余弦相似度，dense-only），合并去重后截断到 K=25，按说话人分成两个 bank 拼进固定模板，交给回答模型（§3.4–3.5）。实现用 gpt-4o-mini 做抽取与回答，text-embedding-3-small 做 embedding（图 3）。

主要结果：
- LoCoMo（排除 adversarial 类）：LLM-as-Judge 总分 77.55，高于 memOS 72.99、mem0 64.73、langmem 55.28、openai 52.81、zep 42.29（Table 1）。分项：single hop 79.90，multi hop 79.79，open domain 72.92，temporal 70.79（低于 memOS 72.68）。平均记忆 token 916，memOS 为 1593，mem0 为 1177。
- 延迟：ENGRAM 总耗时 p50 1.487s / p95 1.819s，full-context 为 9.940s / 17.832s，J 分 72.60（Table 2）。mem0 更快（p50 0.718s）。
- LongMemEval_S（约 115K token/问，500 题）：沿用 LoCoMo 配置不重调，总分 71.40 对 full-context 56.20，输入约 1.0–1.2K 对 101K token（Table 3）。分项差异大：single-session-preference 93.33 对 23.33；knowledge-update 74.36 对 79.49，single-session-assistant 87.50 对 92.86，ENGRAM 反而更低。
- 消融（附录 A）：单一无类型 store 总分 46.56；只用 episodic 66.60、semantic 61.56、procedural 55.06（Table 4）。K 从 20 增到 60，J 从 75.65 升到 80.43，token 从 767 增到 4196；K=25 为性价比拐点（A.2）。

## Evidence and Limits

- 所有 LoCoMo 对比共用 gpt-4o-mini 骨干，并报告三次重复评测的 mean ± std，设置较公平。但 std 只反映 judge 随机性，不含数据划分或抽取的方差；LoCoMo 仅 10 段对话。
- 评分全靠 gpt-4o-mini 做 judge，作者自己承认存在 judge bias（§7）。ENGRAM 的 F1/B1 全面远低于基线（总体 F1 21.08 对 memOS 44.20，B1 13.31 对 36.75），作者解释为回答更长，但未给出长度统计或其他验证。
- 文字有不一致：§5.1 说"在所有类别领先"，同段又承认 temporal 低于 memOS；"token 减少 35% 以上、对几乎所有基线"与表不符（对 mem0 约少 22%，langmem 的 168 token 远少于 ENGRAM）。
- baseline 数字的来源和运行方式（自己重跑还是引用 mem0 论文）正文未说明；Table 1 的 Top-K 列写 20，而最终预算为 K=25（A.2 中 K=25 对应 77.55/916 token，K=20 对应 75.65/767），表述易混。
- K=25 是在 LoCoMo 上依据同一评测选的，存在对测试集调参的可能。LongMemEval 仅与 full-context 对比，没有和其他记忆系统比，所谓 state-of-the-art 只在 LoCoMo 成立；full-context 用 gpt-4o-mini 和 101K 上下文，对该小模型偏弱。
- 类型化的收益证据：无类型单 store 46.56 对 77.55，但该对照是"合并为一个 store"，没有分开"类型 schema"与"每类单独 top-k"的作用；也没有对比 router 去掉后三类全写的版本。
- 明说的局限：依赖 dense 检索质量，漏检会直接传导；router 太简单，跨类 utterance 可能处理不好；文本、英语；跨类交互建模不足（§7）。
- 代码：附录之外的 Reproducibility Statement 给出匿名仓库链接，未见正式仓库。

## Open Questions

- 三类类型的真实贡献是多少？单 store 的退化可能主要来自抽取 prompt 与 schema，而不是"分类型检索"本身，文中没有隔离。
- 延迟和 token 数是否包含写入阶段（每 turn 多次 LLM 抽取调用）的成本？Table 2 只测查询时间。
- 在 knowledge-update 与 single-session-assistant 上低于 full-context，是检索漏掉旧值/更新，还是 router 把 assistant 回复丢了？文中未分析。

---
title: "Recursive Language Models"
updated: 2026-10-09
---

# Recursive Language Models

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文、参考文献、附录 A–F，arXiv v3）。图（Fig. 1、3、4、7、9–16）只有标题和图注，曲线数值未提取；附录 C 的部分 prompt 和 D.1 的 OOLONG-Pairs 查询列表仅浏览。

## Summary

问题：LLM 的 context window 有限，且在窗口内也会 context rot；常用的 compaction 会丢掉早期细节，对需要密集访问全文的任务不够用。

方法（§2）：Recursive Language Model (RLM) 是包在基座模型 M 外的推理脚手架。用户 prompt P 不进模型上下文，而是作为变量放进持久的 Python REPL。root 模型每轮只看到 P 的元数据（长度、前缀等），写代码去 peek、切分、变换 P，并在代码里（可在循环中）调用 sub-LM / sub-RLM，中间结果存在变量里；stdout 只回传截断后的元数据；设置 Final 变量后返回。论文强调三点设计：prompt 是符号句柄而非塞进上下文；输出可由变量拼接，不受单次输出长度限制；递归调用由代码程序化发起，而不是模型逐条口述（Algorithm 1 vs 2）。

实验（§3–4）：模型为 GPT-5（medium reasoning，sub-call 用 GPT-5-mini）和 Qwen3-Coder-480B-A35B。任务按处理复杂度随长度的增长选取：S-NIAH（常数）、BrowseComp-Plus 1K 文档（6M–11M token，150 题）、OOLONG trec_coarse（线性，131K，50 题）、OOLONG-Pairs（二次，32K，20 题，作者自建）、LongBench-v2 CodeQA（23K–4.2M）。基线：base model、CodeAct（+BM25 / +sub-calls）、compaction agent、OpenCode、Claude Code（Opus 4.1）。
- Table 1，GPT-5：OOLONG-Pairs 上 base 0.1，compaction 0.1，CodeAct+sub-calls 28.4，RLM depth=1/2/3 为 58.0/65.5/76.0。BrowseComp+ 上 RLM depth=1 为 91.3（均价 $0.99），compaction 70.5，CodeAct+BM25 51.0，base 因超窗得 0；OpenCode 加 context offloading 为 94.0。OOLONG 上 base 44.0，RLM depth=1 56.0。
- Qwen3-Coder：OOLONG-Pairs 上 RLM depth=1 为 23.1，基线均接近 0；BrowseComp+ 上 depth=2/3 为 68.0/68.7，compaction 38.0。
- Table 2（LongCoT-mini）：GPT-5.2 base 38.7，RLM 50.6，加人工 decomposition hints 后 65.6。
- 训练（§4 Obs. 6、附录 A）：用 Qwen3-Coder 在 LongBenchPro 上的 RLM 轨迹，过滤后对 Qwen3-8B 做 SFT（约 1,000 条，48 H100 小时），RLM-Qwen3-8B 相对原 Qwen3-8B 的 RLM 在四个任务上中位提升 28.3%，且更省、更快（Fig. 3a、Fig. 6）。另在 MRCRv2 上用 RLVR 训练 Qwen3-4B-Instruct，从 64k/2-needle 泛化到 1M/8-needle（Fig. 3b，数值未提取）。

## Evidence and Limits

- 论文主张的核心是"REPL 外化 prompt 是处理超长输入的必要条件，递归 sub-call 对信息密集任务有额外收益"。Table 1 支持前半句：depth=0 的 RLM 与 OpenCode/Claude Code 加 offloading 在 BrowseComp+、CodeQA 上都大幅优于直接放入上下文的基线。后半句在 GPT-5 上成立（OOLONG-Pairs 随 depth 单调上升），在 Qwen3-Coder 上不稳：CodeQA 上 depth=0 反而最好（66.0），OOLONG 上 depth=2/3 低于 base（26.0/32.0 vs 36.0）。作者归因于 Qwen3-Coder 语法错误多且在 sub-RLM 中传播（§5、Fig. 4b）。
- OpenCode(+offloading) 与 Claude Code(+offloading) 在 BrowseComp+ 上（94.0 / 84.0）与 RLM 相当甚至更高，GPT-5 的 CodeQA 上 OpenCode 为 64.0，高于 RLM depth=1 的 62.0；摘要中"相对 Claude Code 中位提升 13%"是跨任务中位数，不是每项都赢。
- 对比不完全对等：GPT-5 RLM 的 sub-call 用 GPT-5-mini，compaction 基线用 GPT-5-nano 做摘要；Claude Code 用不同模型（Opus 4.1）；OpenCode / Claude Code 无成本数据（N/A）。
- 样本小：多数任务 20–150 个实例，未见置信区间或多次种子；成本方差大（如 OOLONG depth=2 为 $1.10 ± $3.25）。Fig. 11 与 Obs. 4 承认中位成本低于 base 但均值更高，尾部轨迹昂贵；"成本相当"主要指均值量级。运行时间因 sub-call 串行而很长，仅在附录 F.2 给出图。
- OOLONG-Pairs 为作者自建，20 个查询；LongCoT-mini 用另一套实现（Prime Intellect rlm-harness，附录 C.3），且 RLM 用了 decomposition hints，而 base 加 hints 反而变差（Table 3：38.7 到 28.6），所以 65.6 反映的是"hints + RLM"。
- 敏感性：prompt 不能跨模型直接复用，Qwen3-Coder 需额外加一句限制 sub-call，否则会对一切发起 sub-call、数量可达上千（附录 B、C.1）；first decomposition 对结果影响大，system prompt 里的无关示例也有明显提升（Fig. 4a）；FINAL / FINAL_VAR 判别脆弱；编码能力弱或输出 token 不足的模型表现差（Qwen3-8B、Qwen3-235B 思考型）。
- 训练部分是小规模探索：蒸馏数据来自 Qwen3-Coder 自身轨迹，并做了人工规则修补 FINAL 误用（16% 与 13% 的轮次）；摘要"approaches GPT-5"依赖 Fig. 3a，文本未给出具体数字。
- 作者自述的局限（§7、附录 B）：guardrail 机制、更自然的长上下文任务评测、sub-call 成本失控、同步调用导致慢，均未解决。

## Open Questions

- 增益里有多少来自 REPL 外化本身，多少来自更强的 sub-model（GPT-5-mini 作 sub-call）和对大量 chunk 的并行/重复覆盖？论文没有在相同 sub-model 预算下与其他 offloading 方案做更严格的消融。
- 递归深度的收益为何因模型而异（GPT-5 单调升，Qwen3-Coder 非单调）？是语法/指令遵循能力的问题，还是任务结构的问题，论文只给了相关性分析。
- 训练出来的 native RLM 能否在更大模型、更多数据和 on-policy RL 下继续提升，并摆脱 FINAL 标签与 prompt 依赖？目前只有 8B / 4B 的小规模证据。

---
title: Agent Memory Benchmark Comparison Thread
domain: research
area: agent-memory
type: synthesis
status: active
updated: 2026-04-26
tags: [research, agent-memory, benchmark, locomo, longmemeval, comparison, thread]
---

# Agent Memory Benchmark Comparison Thread

各论文在 LoCoMo / LongMemEval 上的对比设置汇总。重点记录：对比了哪些 baseline、用了哪些 benchmark、answer/judge 用的什么模型。

---

## 论文一览

| 论文                    | Baselines                                                                                      | Benchmarks                                | Answer Model                                                       | Judge Model                    | 备注                                                                          |
| --------------------- | ---------------------------------------------------------------------------------------------- | ----------------------------------------- | ------------------------------------------------------------------ | ------------------------------ | --------------------------------------------------------------------------- |
| Memory in the LLM Era | A-mem, memoryBank, MemGPT, mem0, mem0g, memochat, Zep, memtree, memoryOS, memos                | LoCoMo, LongMemEval                       | Qwen2.5-7B-Instruct (默认) / Qwen2.5-72B / LLaMA3.1-8B / GPT-4o-mini | —                              | 多模型对比                                                                       |
| MemOS                 | MIRIX, Zep, mem0, Memobase, Supermemory, memU                                                  | LoCoMo, LongMemEval, PreFEval, PersonaMem | GPT-4o-mini                                                        | GPT-4o-mini                    | 摘要提 GPT-4o-mini 为基座；正文未说明 LongMemEval judge 用什么模型                           |
| ByteRover             | Chronos†, Hindsight, Honcho, Memobase, OpenAI Memory, Mem0, SmartSearch†, Memora†, TiMem†, Zep | LoCoMo, LongMemEval                       | Gemini 3 Pro                                                       | Gemini 3 Flash                 | †= 仅引用论文数字，未在作者自己的 harness 中跑；两个 benchmark 用不同模型配置                          |
| EverMemOS             | Zep, Mem0, MemOS, MemoryOS, MemU                                                               | LoCoMo, LongMemEval, PersonaMem-v2        | GPT-4.1-mini / GPT-4o-mini                                         | GPT-4o-mini + auxiliary judges | LongMemEval baseline 引用 MemOS leaderboard；强调 MemCell/MemScene consolidation |
| Honcho                | Mem0, Zep                                                                                      | LoCoMo, LongMemEval, BEAM                 | Gemini 3 Pro                                                       | —                              |                                                                             |
| Supermemory           | Zep                                                                                            | —                                         | —                                                                  | —                              | 对比范围极小                                                                      |
| Hindsight             | Memobase, Zep, Mem0, LangMem, OpenAI Memory                                                    | —                                         | Gemini 3 Pro                                                       | —                              |                                                                             |
| mem0                  |                                                                                                |                                           | GPT-4o-mini                                                        | GPT-4o-mini                    |                                                                             |
| evermemos             |                                                                                                |                                           | GPT-4o-mini                                                        | GPT-4o-mini                    |                                                                             |
| zep                   |                                                                                                |                                           | GPT-4o-mini                                                        | GPT-4o-mini                    |                                                                             |

> **模型名注**：ByteRover / Honcho / Hindsight 原文写 "Gemini 3.1 Pro" / "Gemini 3 Flash" / "gemini3 pro"，推测对应 Gemini 2.5 Pro / Gemini 2 Flash（版本号待确认）。

---

## Benchmark 覆盖矩阵

| 论文 | LoCoMo | LongMemEval | BEAM | PreFEval | PersonaMem |
|---|:---:|:---:|:---:|:---:|:---:|
| Memory in the LLM Era | ✓ | ✓ | | | |
| MemOS | ✓ | ✓ | | ✓ | ✓ |
| ByteRover | ✓ | ✓ | | | |
| EverMemOS | ✓ | ✓ | | | ✓ |
| Honcho | ✓ | ✓ | ✓ | | |
| Supermemory | | | | | |
| Hindsight | | | | | |

---

## Baseline 出现频次

以下系统被多篇论文同时用作 baseline，是该领域的事实标准对比对象：

| System | 被引用次数 | 出现于 |
|---|:---:|---|
| Zep | 5 | Memory in the LLM Era, MemOS, ByteRover, Honcho, Hindsight, Supermemory |
| Mem0 | 4 | Memory in the LLM Era, MemOS, ByteRover, Honcho, Hindsight |
| Memobase | 3 | MemOS, ByteRover, Hindsight |
| Hindsight | 2 | ByteRover（作者自跑）, MemOS（间接） |
| Honcho | 2 | ByteRover（作者自跑） |
| OpenAI Memory | 2 | ByteRover, Hindsight |

---

## WizWand SOTA Snapshot 2026-04-26

Sources:
- LoCoMo: <https://www.wizwand.com/sota/long-term-memory-evaluation-on-locomo>
- LongMemEval: <https://www.wizwand.com/sota/long-context-memory-evaluation-on-longmemeval>

Important: WizWand aggregates entries from multiple report papers, dates, backbones, and judge setups. Treat the tables below as an external leaderboard snapshot, not as a controlled apples-to-apples comparison. The LoCoMo page's displayed primary metric is **Overall F1**; many paper notes in this wiki report **accuracy / LLM score**, so numbers are not interchangeable.

### LoCoMo External SOTA

Primary metric on page: **Overall F1**.

| Rank | Method | Score | Report Date | Config / Notes |
|---:|---|---:|---|---|
| 1 | EverMemOS | 92.3 | 2026-03-15 | page shows no config |
| 2 | Hindsight | 89.6 | 2026-03-15 | page shows no config |
| 3 | Zep v3 | 85.2 | 2026-03-15 | page shows no config |
| 4 | MemOS v2 | 80.8 | 2026-03-15 | page shows no config |
| 5 | SLM-V3 | 74.8 | 2026-03-15 | Mode A (Retrieval) |
| 6 | Governed Memory | 74.8 | 2026-03-18 | page shows no config |
| 7 | Mem0 | 64.2 | 2026-03-15 | page shows no config |
| 8 | OMNIMEM | 61.3 | 2026-04-01 | Backbone: GPT-5.1 |
| 9 | SLM-V3 | 60.4 | 2026-03-15 | Mode A (Raw) |
| 10 | OMNIMEM | 59.8 | 2026-04-01 | Backbone: GPT-4o |

### LongMemEval External SOTA

Primary metric on page: **Average Score**.

| Rank | Method | Score | Report Date | Config / Notes |
|---:|---|---:|---|---|
| 1 | Chronos High | 95.6 | 2026-03-17 | LLM Backbone: Advanced |
| 2 | Mastra | 92.8 | 2026-03-17 | page shows no config |
| 3 | Honcho | 92.6 | 2026-03-17 | page shows no config |
| 4 | Cognis | 92.4 | 2026-03-27 | Judge: GPT-4.1; answer: best across 8 models |
| 5 | Hindsight | 91.4 | 2026-03-17 | Judge: OSS-120B |
| 6 | MEMORA (P) | 87.4 | 2026-02-03 | Retriever: Policy; context 2.9k |
| 7 | Supermemory | 85.2 | 2026-03-17 | page shows no config |
| 8 | MEMORA (S) | 83.8 | 2026-02-03 | Retriever: Semantic; context 2.1k |
| 9 | EverMemOS | 83.0 | 2026-04-09 | page shows no config |
| 10 | MemReader-4B-GRPO | 83.0 | 2026-04-09 | Model size 4B; GRPO |

### Immediate Implications

**EverMemOS is the current LoCoMo headline on WizWand**, but the score is Overall F1 (92.3), not the EverMemOS paper's GPT-4.1-mini overall accuracy (93.05). Keep both numbers, with metric labels.

**LongMemEval has moved beyond MemOS-era baselines** on WizWand: Chronos High / Mastra / Honcho / Cognis / Hindsight all appear above 90 Average Score, while EverMemOS appears at 83.0. For any new LongMemEval claim, compare against both controlled paper baselines and this external moving leaderboard.

**Mem0 vendor/blog-era numbers remain hard to reconcile**: WizWand's visible Mem0 LongMemEval entries are 66.4 / 54.8 / 54.62 / 32.46 depending on report/config, not the much higher Mem0 blog claims. Keep vendor-reported and leaderboard-observed Mem0 numbers separated.

---

## 关键观察

**Baseline 选择差异大**：各论文对比的系统差异显著。ByteRover 覆盖最广（10 个 baseline），Supermemory 最窄（仅 Zep）。这使得跨论文直接比较数字存在风险。

**Judge model 不统一**：ByteRover 明确说明用 Gemini 2 Flash 做 judge；其他论文多数未说明 judge model，或与 answer model 混用。MemOS 正文甚至未说明 LongMemEval 的 judge 配置。

**†引用 vs 自跑**：ByteRover 区分了"引用论文数字"（†标注）和"作者自己 harness 跑出的数字"，这是目前各论文中最透明的做法。其他论文未做此区分。

**Gemini 版本模糊**：多篇论文写 "Gemini 3.x"，但当前公开版本为 Gemini 2.x 系列，版本对应关系需确认。

**Leaderboard 配置漂移**：WizWand 收录的 SOTA 页显示 2026 年 3-4 月大量新条目，但同一页面混合 Overall F1、Average Score、LLM Score、不同 backbone、不同 judge 和不同 report paper。它适合发现“当前强 baseline 候选”，不适合直接替代论文内 controlled comparison。

---

## LoCoMo Harness / Prompt Notes 2026-04-26

### Codex CLI Batch QA

Codex CLI 可以用 headless/non-interactive 方式批量调用：

```bash
codex exec --json "..."
```

适合测试 Codex agent 行为，而不是普通 LLM QA。1540 个 QA 不应手动逐条开启；应写脚本循环/并发调用 `codex exec`，但并发建议从 2-4 开始，避免 CLI session/rate-limit 问题。若 QA 不需要本地 repo 上下文，直接用模型 API 或 Batch API 更合适；若目标是测 Codex CLI agent 的行为，则 `codex exec` 是正确入口。

### Mem0 / Memobase / MemOS / GrepQA Prompt Difference

Mem0 和 Memobase 的 LoCoMo answer prompt 基本同源：长 prompt，强调 two-speaker memories、timestamps、contradiction 用 recent memory、relative time 转 absolute date，并要求答案少于 5-6 words；但同时包含 “Think step by step / show your work”，可能让答案变长或泄露推理。

MemOS 的 LoCoMo answer prompt 更宽松：允许 synthesize across entries，并允许用 general world knowledge 解释 memory 中的信息。这会影响 open-domain 和 implicit reference 题，不能和更严格的 prompt 直接视为同一 answerer。

GrepQA 是两段式：
- retrieval prompt：`grepqa_v21` 用 LLM 生成 3 个 question-side JSON predicates，是方法本身的一部分。
- answer prompt：`grepqa_v13` 是短 prompt，只允许基于 retrieved conversation turns 回答，要求用 session date 解析 relative time，并且不输出 full sentence / explanation。

结论：如果要做 NeurIPS-level harness，应把 **retrieval prompt** 视为方法组成部分保留，但统一 **answer prompt / answer model / scoring / category filtering**。否则 prompt 差异会混入 retrieval 方法比较。

推荐主表设置：

1. **Unified Answerer Harness**：所有方法只负责返回 retrieved context；统一 answer prompt、answer model、temperature、max tokens、F1、LLM judge。
2. **Native Prompt Appendix**：各方法按官方/论文 prompt 跑，用于说明和官方数字的可比性。

建议 canonical answer prompt 核心约束：

```text
Use only the provided context. Do not use outside knowledge.
Use timestamps to resolve relative time expressions.
If context uses event_time, treat it as the event occurrence time.
If multiple memories conflict, prefer the most recent relevant evidence.
Return only the final short answer. Do not explain.
```

### EverMemOS / EverOS

EverMemOS 需要作为 2026 年 5 月 NeurIPS 投稿的重要 baseline。其 repo 中 LoCoMo evaluation 明确报告 EverMemOS 在 LoCoMo 上约 92+ overall，并且 README 指向 2026 年初工作；审稿人很可能期待讨论或对比。

EverMemOS answer prompt 很强，不是普通短答 prompt。它要求结构化 CoT：
- relevant memories extraction
- key information identification
- cross-memory linking
- time reference calculation
- contradiction check
- detail verification checklist
- final answer extraction

代码会切出 `FINAL ANSWER:` 后面的内容作为最终答案。因此 native EverMemOS 数字不应直接和 GrepQA short-answer prompt 数字混用。

EverMemOS retrieval 也强依赖 agentic prompt：
- sufficiency check prompt：判断当前 docs 是否覆盖实体、start/end time、temporal relation。
- multi-query generation prompt：强制 temporal boundary decomposition，生成 2-3 个 query，并包含 HyDE-style declarative query。

这与 GrepQA v21 的 question-side multi-predicate 有相似动机，但 EverMemOS 是更重的 agentic multi-round retrieval。

### Zep LoCoMo Harness

Zep repo 的 LoCoMo harness 位于 `benchmarks/locomo`。它把 retrieval context 格式化成：

```text
FACTS:
- edge.fact (event_time: edge.valid_at)

ENTITIES:
- node.name: node.summary
```

Zep answer prompt 明确强调：timestamp / event_time 表示事件发生时间，不是事件被提到的时间。例如 “I went to the vet yesterday” 且 event_time 为 2023-03-15，则答案应按 2023-03-15 处理。这是 Zep 与普通 memory system 的关键语义差异。

默认 Zep config：
- `edge_limit=15`, `edge_reranker=cross_encoder`
- `node_limit=5`, `node_reranker=cross_encoder`
- response model `gpt-4o-mini`
- grader model `gpt-4o-mini`
- temperature 0

repo 内已有实验 config 使用更强 retrieval：`edge_limit=30`, `node_limit=30`。报告 Zep 结果时必须标清 limit/reranker/context tokens，否则数字不可比。

### F1 / Metric Consistency

Zep 官方 LoCoMo harness **不计算 F1、BLEU、ROUGE**。它的主指标是 LLM-judge accuracy，并额外报告 context completeness、latency、context token/char stats、category accuracy。因此表中如果出现 Zep F1，应该说明是用 saved `hypothesis` 和 `golden_answer` 后处理计算，不是 Zep 原 harness 原生指标。

GrepQA 当前使用 `mem0_old_compatible` token F1：
- lower-case
- punctuation 转空格
- split token set
- set overlap F1

Mem0/Memobase old evaluation 的 F1 也是 set-token 风格，但依赖其 `metrics/utils.py` 的实现；不同论文/leaderboard 可能把 LLM judge accuracy、Overall F1、Average Score 混写。统一 harness 应明确：

- `llm_judge_accuracy`: CORRECT/WRONG judge 平均
- `token_f1_mem0_compatible`: 统一后处理 F1
- `context_tokens`: answer prompt 中实际 context token
- `category 5`: 默认单独报告或排除，不能混入 overall

### EverMemOS Saved Results Re-Scoring

2026-04-26 inspection of `wiki/research/agent-memory/papers/evermemos-2026/repo/EverMemOS_Eval_Results`:

- The saved `answer_results.json` files contain `question`, `answer`, `golden_answer`, `category`, `conversation_id`, and formatted retrieved context. This is enough to recompute GrepQA-style token F1 and BLEU-1 without regenerating answers.
- The saved `eval_results.json` files contain three boolean LLM judgments per question and an aggregate accuracy. This is enough to report EverMemOS-native LLM-as-judge accuracy, but not to prove exact equivalence to a rerun with GrepQA's judge client.
- The judge prompts are effectively the same core prompt as GrepQA's `locomo/judge.py`: generous `CORRECT`/`WRONG` grading, same shell-necklace example, same relaxed date/time equivalence rule. Minor differences remain: EverMemOS uses a separate system prompt and asks for `{"label": ...}`, while GrepQA asks for JSON with `reasoning` and `label`.

Offline re-score with GrepQA `mem0_old_compatible` token F1 and BLEU-1 over 1540 LoCoMo questions, no category 5 present:

| Saved run | Native LLM judge accuracy | GrepQA token F1 | GrepQA BLEU-1 |
|---|---:|---:|---:|
| EverMemOS | 92.32 | 16.41 | 9.01 |
| Zep | 85.22 | 18.00 | 9.77 |
| MemOS | 80.76 | 40.02 | 32.47 |
| MemU | 66.67 | 45.47 | 39.18 |
| Mem0 | 64.20 | 41.31 | 34.87 |

Interpretation: direct post-hoc F1/BLEU is mechanically possible, but it is a harsh short-answer precision metric. Verbose answer prompts like EverMemOS and Zep get penalized despite high LLM-judge correctness. These numbers should be labeled "post-hoc token metrics on native generated answers," not treated as an apples-to-apples unified-answerer comparison.

### NeurIPS Harness Decision

主张用 “decoupled retrieval and answer generation” 表述：

> Each memory system constructs and retrieves its own memory context using its native retrieval mechanism. To avoid prompt-induced confounds, all retrieved contexts are passed to the same answer-generation prompt and evaluated with identical metrics.

同时保留 native-prompt appendix，解释 Zep event_time prompt、EverMemOS CoT answer prompt、MemOS world-knowledge permission 等官方设置与统一设置的差异。

---

## 相关论文

- [[../papers/memory-llm-era-2026]] — Memory in the LLM Era
- [[../papers/memos-2026]] — MemOS
- [[../papers/evermemos-2026]] — EverMemOS
- [[../papers/byterover-2026]] — ByteRover
- [[../papers/honcho-2025]] — Honcho
- [[../papers/hindsight-2025]] — Hindsight
- [[../papers/locomo-2024]] — LoCoMo benchmark
- [[../papers/longmemeval-2025]] — LongMemEval benchmark

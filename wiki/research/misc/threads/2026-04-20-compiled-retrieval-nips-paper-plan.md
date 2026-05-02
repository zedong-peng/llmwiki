---
title: "Compiled Retrieval: NeurIPS Paper Plan"
domain: research
area: misc
type: note
status: active
updated: 2026-04-20
tags: [research-thread, grepqa, compiled-retrieval, nips, paper-plan, code-retrieval, conversation-memory]
---
# Compiled Retrieval: NeurIPS Paper Plan

## Context

这个 thread 起源于 2026-04-20 的一次会话。起因：

1. `grepqa` 项目已经在 LoCoMo-10 上达到 F1=51.69（超过 Mem0⁺ +5.6pp），在 LongMemEval-S 上达到 65.2% accuracy
2. 已有 34 个版本的迭代历史、完整的 ablation study、RAG baseline 对比、详细的 failure mode analysis
3. 文献调研已覆盖 60+ 篇相关论文，包括 agent memory、retrieval optimization、RAG benchmarks 等方向
4. 目标：投 NeurIPS，做到最好，不考虑时间限制

## 为什么这么计划

### GrepQA 单独发的问题

1. **Novelty 压力**：BRIGHT 已经证明 "LLM-generated queries improve retrieval"，AutoBool 做了 boolean query generation。核心 idea 不算全新
   References: [[../papers/bright-2025]], [[../papers/autobool-2026]]

2. **Benchmark 单一**：主要在 LoCoMo-10 上（只有 10 个 conversation），LongMemEval 上表现一般（65.2% vs ByteRover 92.8%）
   References: [[../papers/locomo-2024]], [[../papers/longmemeval-2025]], [[../papers/byterover-2026]]

3. **方法相对简单**：100 行 Python，reviewer 可能觉得 technical contribution 不够

4. **Scope 窄**：只做了 conversational memory retrieval，没有在更广的 retrieval benchmark 上验证

### 选择 Idea 1+4 的理由

经过讨论，确定了 **Regime Map Paper + Code Retrieval** 的组合方向：

1. **两个 domain 互补性极好**
   - Conversation memory = 自然语言，vocabulary 共享度高，GrepQA 的 sweet spot
   - Code retrieval = 极端 lexical-faithful，变量名/函数名/API 完全精确匹配
   - 两个 domain 一起讲，regime map 的说服力远强于单 domain

2. **Story 自然**
   - "我们发现 LLM-compiled lexical search 在 lexical-faithful regime 下系统性地优于 dense retrieval"
   - Conversation 和 code 是这个 regime 的两个典型代表

3. **和工业实践直接呼应**
   - Cursor 的 regex search blog 是现成的 industrial evidence
   - Mem0/Zep 是 conversation memory 的工业 baseline
   References: [[2026-04-19-cursor-blog-reading-notes]]

4. **Code retrieval 是重要部分**
   - LLM 大量用于 code 场景
   - Coding agents 已经在用 grep（Cursor、Claude Code、Aider 等）
   - 但没有人系统研究过 LLM-compiled grep 作为 code retrieval 的效果
   - Code 是 lexical-faithful 的极端案例

## Paper Framing

### Title (Working)

**Compiled Retrieval: When LLM-Generated Search Programs Beat Dense Retrieval**

或

**Retrieval as Query Compilation: A Regime Study across Conversation and Code**

### Core Claim

Structured lexical query compilation（LLM 生成结构化的 keyword/boolean/typed predicates，然后用 exact matching 执行）is a distinct and useful retrieval representation that systematically outperforms dense retrieval in **lexical-faithful regimes** — where the query and the relevant document share vocabulary.

**不是说** "grep beats RAG"。
**而是说** "structured lexical query compilation is a distinct retrieval representation, and we characterize when it wins and when it loses."

### Contribution Structure

1. **Method**: Compiled Retrieval — LLM as query compiler, lexical/symbolic backend as retrieval executor
2. **Regime Map**: Systematic characterization of when compiled retrieval wins vs dense retrieval
3. **Cross-Domain Evaluation**: Conversation memory + code retrieval + reasoning-intensive retrieval
4. **Diagnostic Analysis**: RAGChecker-style separation of retrieval quality from generation quality

## Experiment Plan

### Domain 1: Conversation Memory (已有基础)

**Benchmarks:**
- LoCoMo-10 (1,540 QA pairs) — 已完成
- LongMemEval-S (500 questions, ~115k tokens/question) — 已完成
- LongMemEval-M (如果可获取) — 待做

**Methods to compare:**
| Method | Query Formulation | Retrieval Engine | Status |
|---|---|---|---|
| GrepQA v21/v34 | Structured keyword predicates | Exact match + scoring | ✅ 已完成 |
| BM25 baseline | Original question | BM25 | ✅ 已有代码 |
| Embedding RAG | Original question | Dense (text-embedding-3-small) | ✅ 已有代码 |
| Reasoning query + BM25 | Free-form reasoning trace | BM25 | ❌ 待做 |
| Reasoning query + Dense | Free-form reasoning trace | Dense | ❌ 待做 |
| Full context | N/A | N/A | ✅ 已完成 |
| No context | N/A | N/A | ✅ 已完成 |
| Oracle | N/A | N/A | ✅ 已完成 |

**Key experiments to add:**
1. Reasoning query baseline（BRIGHT-style，让 LLM 生成 reasoning trace 作为 query）
2. 用更好的 model（GPT-4o）跑 GrepQA，看 model scaling
3. Scaling analysis：conversation 长度从 10k → 100k → 500k tokens

### Domain 2: Code Retrieval (从零开始)

**Candidate Benchmarks:**

1. **SWE-bench file localization**
   - Task: 给定 GitHub issue，找到需要修改的文件
   - 为什么好：最接近 coding agent 的真实 retrieval 场景
   - 数据：SWE-bench Lite (300 instances) 或 SWE-bench Verified (500 instances)
   - 待 ingest

2. **CodeSearchNet**
   - Task: natural language → code function retrieval
   - 6 languages, ~6M functions
   - 经典但可能 dated
   - 待 ingest

3. **CoIR (Code Information Retrieval)**
   - Task: 多种 code retrieval 任务
   - 2024 年新 benchmark，和 MTEB 兼容
   - arXiv: 2407.02883
   - 待 ingest

4. **CrossCodeEval / RepoEval / RepoBench**
   - Repository-level code retrieval
   - 待调研

**Methods to compare (code domain):**
| Method | Query Formulation | Retrieval Engine |
|---|---|---|
| GrepQA-Code | Structured keyword predicates (function names, API calls, variable names) | Exact match + scoring |
| BM25 | Original query | BM25 |
| Code embedding | Original query | Dense (Voyage Code, CodeBERT, etc.) |
| Reasoning query + BM25 | Free-form reasoning trace | BM25 |
| Reasoning query + Dense | Free-form reasoning trace | Dense |

**GrepQA-Code 的 predicate generation 需要适配：**
- Code domain 的 keyword 不同于 conversation：function names, class names, API calls, error messages, file paths
- Speaker filter → language/file-type filter
- Window expansion → surrounding code context (function body, class body)
- 可能需要 code-aware tokenization

### Domain 3: Reasoning-Intensive Retrieval (BRIGHT)

**Benchmark:**
- BRIGHT (1,384 queries, 12 datasets)
- 已有详细论文笔记
References: [[../papers/bright-2025]]

**Methods to compare:**
| Method | Query Formulation | Retrieval Engine |
|---|---|---|
| GrepQA-style predicates | Structured keyword predicates | BM25 |
| BRIGHT reasoning query | Free-form reasoning trace | BM25 |
| BRIGHT reasoning query | Free-form reasoning trace | Dense |
| Original query | Original | BM25 |
| Original query | Original | Dense |

**预期：GrepQA 在 BRIGHT 上可能输给 reasoning query**，因为 BRIGHT 的 query-document 关系需要推理而不是 lexical match。这正是 regime map 的价值——展示 compiled retrieval 的边界。

### Domain 4 (Optional): Conversational RAG (CORAL)

**Benchmark:**
- CORAL (8,000 conversations, multi-turn)
References: [[../papers/coral-2024]]

**如果时间允许，作为 supplementary experiment。**

## Regime Map 设计

最终 paper 的核心 figure 应该是一个 **regime map**：

| Regime | Lexical Faithfulness | Example Domain | Predicted Winner |
|---|---|---|---|
| Lexical-faithful | High | Conversation memory, code search | Compiled retrieval |
| Paraphrastic | Low | General document retrieval | Dense retrieval |
| Reasoning-intensive | Low | BRIGHT-style tasks | Reasoning query + dense |
| Temporal/metadata-heavy | Medium | Temporal QA | Compiled retrieval + metadata filter |
| Compositional/multi-hop | Medium | Multi-hop QA | Hybrid or iterative |

## Diagnostic Analysis

使用 RAGChecker-style diagnostics 分离：
- Retrieval quality（precision, recall, nDCG）
- Generation quality（answer accuracy given retrieved context）
- 这样可以精确定位 compiled retrieval 的优势来源

References: [[../papers/ragchecker-2024]]

## Paper Outline

```
1. Introduction
   - LLMs are increasingly used as query compilers (cite BRIGHT, AutoBool, GrepQA)
   - But no systematic study of when this works vs when it fails
   - We introduce "compiled retrieval" and study it across conversation + code

2. Background & Related Work
   - Dense retrieval (BEIR, MTEB)
   - LLM-augmented retrieval (BRIGHT reasoning queries, HyDE, query rewriting)
   - Structured query generation (AutoBool, LOTUS)
   - Agent memory systems (Mem0, Zep, ByteRover)
   - Code retrieval (CodeSearchNet, SWE-bench, CoIR)

3. Compiled Retrieval
   - Definition: LLM generates structured search program, symbolic backend executes
   - Design space: keyword predicates, boolean queries, typed predicates
   - Implementation: GrepQA as instantiation

4. Experimental Setup
   - Benchmarks: LoCoMo, LongMemEval, SWE-bench/CoIR, BRIGHT
   - Methods: compiled retrieval vs dense vs reasoning query vs hybrid
   - Metrics: retrieval metrics + end-to-end task metrics

5. Results
   - Conversation memory: compiled retrieval wins
   - Code retrieval: compiled retrieval wins (especially for exact symbol lookup)
   - Reasoning-intensive: compiled retrieval loses to reasoning queries
   - Regime map: characterization of when each approach wins

6. Analysis
   - RAGChecker diagnostics
   - Failure mode taxonomy
   - Cost-accuracy tradeoffs
   - Scaling analysis (context length, model size)

7. Discussion
   - When to use compiled retrieval vs dense retrieval
   - Implications for agent design
   - Connection to industrial practice (Cursor, Claude Code)

8. Conclusion
```

## 待做清单

### 调研 (Research)
- [x] Ingest CoIR benchmark paper (queued, `papers/coir-2024`)
- [x] Ingest SWE-bench retrieval/localization related work (queued, `papers/swebench-2024`)
- [x] Ingest CodeSearchNet paper (queued, `papers/codesearchnet-2019`)
- [x] Ingest Agentless paper (queued, `papers/agentless-2024`)
- [ ] Ingest CrossCodeEval / RepoEval papers
- [ ] 调研 Voyage Code, CodeBERT 等 code embedding models
- [ ] 全部论文升级为 processed（需下载 TeX/PDF）

### 实验 (Experiments)
- [x] 实现 GrepQA-Code（`code_retrieval/grepqa_code.py`）
- [x] 实现 reasoning query baseline（`reasoning_baseline.py`）
- [x] SWE-bench experiment harness（`code_retrieval/run_swebench.py`）
- [x] BRIGHT experiment harness（`code_retrieval/run_bright.py`）
- [ ] 下载 SWE-bench Verified 数据 + checkout repos
- [ ] 下载 BRIGHT 数据（HuggingFace xlang-ai/BRIGHT）
- [ ] 在 SWE-bench 上跑 file localization 实验
- [ ] 在 CoIR 上跑 code retrieval 实验
- [ ] 在 BRIGHT 上跑 compiled retrieval vs reasoning query 实验
- [ ] 在 LoCoMo 上跑 reasoning_query baseline
- [ ] Scaling analysis（conversation length, model size）
- [ ] RAGChecker diagnostics
- [ ] Cost-accuracy Pareto frontier analysis

### 写作 (Writing)
- [ ] Paper draft
- [ ] Figures: regime map, comparison tables, Pareto frontier
- [ ] Appendix: full ablation tables, prompt templates

## References

### 已有论文笔记
- [[../papers/bright-2025]] — reasoning-intensive retrieval benchmark
- [[../papers/autobool-2026]] — boolean query generation
- [[../papers/coral-2024]] — conversational RAG benchmark
- [[../papers/byterover-2026]] — SOTA on LoCoMo and LongMemEval
- [[../papers/lotus-2025]] — declarative semantic operators
- [[../papers/mintlify-chromafs-2026]] — virtual filesystem for assistants
- [[../papers/ragchecker-2024]] — retrieval diagnostic framework
- [[../papers/locomo-2024]] — LoCoMo benchmark
- [[../papers/longmemeval-2025]] — LongMemEval benchmark
- [[../papers/mem0-2025]] — Mem0 memory system
- [[../papers/zep-2025]] — Zep memory system
- [[../papers/beir-2021]] — BEIR benchmark

### 待 ingest 论文
- ~~CoIR: A Comprehensive Benchmark for Code Information Retrieval (arXiv 2407.02883)~~ → `papers/coir-2024` (queued)
- ~~CodeSearchNet Challenge (Husain et al., 2019)~~ → `papers/codesearchnet-2019` (queued)
- ~~SWE-bench: Can Language Models Resolve Real-World GitHub Issues? (Jimenez et al., 2024)~~ → `papers/swebench-2024` (queued)
- ~~Agentless: Demystifying LLM-based Software Engineering Agents (Xia et al., 2024)~~ → `papers/agentless-2024` (queued)
- CrossCodeEval (Ding et al., 2024)
- RepoEval (Zhang et al., 2023)
- RepoBench (Liu et al., 2024)
- Voyage Code embeddings (technical report)

### 已有 threads
- [[2026-04-19-compiled-lexical-retrieval-and-rag-benchmarks]] — 前期 framing 讨论
- [[2026-04-19-beir-related-paper-search]] — BEIR 相关论文搜索
- [[2026-04-19-beir-current-sota-snapshot]] — BEIR SOTA 快照
- [[2026-04-19-cursor-blog-reading-notes]] — Cursor blog 阅读笔记

### GrepQA 项目
- 代码：`/Users/pengzedong/Documents/GitHub/grepqa`
- 当前最佳：v21 (F1=51.69 on LoCoMo-10), v34 (conditional answer routing)
- Blog post: `grepqa/blog_post.md`
- **新增代码（2026-04-20）：**
  - `code_retrieval/grepqa_code.py` — GrepQA-Code 核心实现
  - `code_retrieval/run_swebench.py` — SWE-bench file localization harness
  - `code_retrieval/run_bright.py` — BRIGHT experiment harness
  - `reasoning_baseline.py` — Reasoning query baseline for LoCoMo

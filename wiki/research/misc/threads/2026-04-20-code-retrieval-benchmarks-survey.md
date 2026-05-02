---
title: "Code Retrieval Benchmarks and Methods Survey"
domain: research
area: misc
type: note
status: active
updated: 2026-04-20
tags: [research-thread, code-retrieval, code-search, benchmarks, swe-bench, codesearchnet, coir]
---
# Code Retrieval Benchmarks and Methods Survey

## Context

为 Compiled Retrieval NeurIPS paper 做的 code retrieval 方向调研。目标是找到合适的 benchmark 来验证 LLM-compiled lexical search 在 code domain 的效果。

Related thread: [[2026-04-20-compiled-retrieval-nips-paper-plan]]

## Key Judgments

1. Code retrieval 是 lexical-faithful regime 的极端案例：变量名、函数名、API 调用、类名都是精确匹配的。这意味着 GrepQA-style 的 compiled retrieval 在 code domain 应该有天然优势。

2. 现有 coding agents（Cursor、Claude Code、Aider、SWE-agent）已经大量使用 grep/regex 作为核心检索工具，但没有人系统研究过 LLM-compiled grep 作为 code retrieval 的效果。
   References: [[2026-04-19-cursor-blog-reading-notes]]

3. Code retrieval 有多个层次，需要区分：
   - **File-level localization**: 给定 task/issue，找到需要修改的文件（SWE-bench 的核心子任务）
   - **Function-level retrieval**: 给定 NL query，找到相关函数（CodeSearchNet 的任务）
   - **Snippet-level retrieval**: 给定 context，找到相关代码片段（RepoBench、CrossCodeEval）
   - **Multi-granularity retrieval**: 混合以上层次（CoIR）

4. 对于 paper 来说，最有说服力的 code retrieval benchmark 应该满足：
   - 和真实 coding agent 场景接近
   - 有 dense retrieval baseline 可以对比
   - 数据规模足够
   - 社区认可度高

## Benchmark Survey

### SWE-bench File Localization

**概述：**
- 来源：Princeton NLP (Jimenez et al., 2024)
- Task：给定 GitHub issue description，找到需要修改的文件
- 数据：SWE-bench Lite (300 instances), SWE-bench Verified (500 instances)
- 每个 instance 是一个真实的 GitHub repo + issue + gold patch
- 文件数量从几十到几千不等

**为什么适合：**
- 最接近 coding agent 的真实 retrieval 场景
- Issue description 通常包含 error messages、function names、file paths 等 lexical-faithful 的线索
- 已有多种 retrieval 方法的对比（BM25、embedding、hybrid）
- 社区认可度极高

**已知的 retrieval 方法：**
| Method | Approach | Notes |
|---|---|---|
| Agentless | Hierarchical localization: repo structure → file → class/function | 不依赖 embedding |
| SWE-agent | Interactive grep/find in terminal | Agent-driven lexical search |
| AutoCodeRover | AST-based code search + spectrum-based fault localization | Structured search |
| Moatless Tools | Embedding-based retrieval with code-specific models | Dense retrieval |
| OpenHands | Hybrid approach | BM25 + embedding |

**GrepQA-Code 适配思路：**
- Input: issue description
- LLM generates predicates: `{"must_keywords": ["FileNotFoundError", "load_config"], "file_pattern": "*.py", "should_keywords": ["path", "config"]}`
- Retrieval: grep over repo files, score by keyword match
- Window expansion: surrounding code context (function body, class body)

**待 ingest：**
- SWE-bench paper: arXiv 2310.06770
- Agentless paper: arXiv 2407.01489
- AutoCodeRover paper: arXiv 2404.05427

### CodeSearchNet

**概述：**
- 来源：GitHub + Microsoft (Husain et al., 2019)
- Task：natural language query → code function retrieval
- 6 languages: Go, Java, JavaScript, PHP, Python, Ruby
- ~6M functions, ~2M with docstrings
- Metric: MRR (Mean Reciprocal Rank)

**为什么适合：**
- 经典 benchmark，广泛使用
- NL → code 的 retrieval 任务天然适合测试 compiled retrieval
- 有大量 dense retrieval baseline（CodeBERT, GraphCodeBERT, UniXcoder, StarCoder embeddings）

**局限：**
- 数据可能 dated（2019）
- 标注质量有争议（noisy relevance annotations）
- 主要是 function-level，不是 repo-level

**GrepQA-Code 适配思路：**
- Input: NL query (e.g., "sort a list of dictionaries by a specific key")
- LLM generates predicates: `{"must_keywords": ["sorted", "dict", "key"], "should_keywords": ["lambda", "sort", "list"]}`
- Retrieval: grep over function bodies + docstrings

**待 ingest：**
- CodeSearchNet Challenge paper: arXiv 1909.09436

### CoIR (Code Information Retrieval Benchmark)

**概述：**
- 来源：2024 年新 benchmark
- arXiv: 2407.02883
- Task：多种 code retrieval 任务的综合 benchmark
- 和 MTEB 兼容
- 覆盖多种 code retrieval 场景

**为什么适合：**
- 最新的综合性 code retrieval benchmark
- 多任务设计，可以测试 compiled retrieval 在不同 code retrieval 子任务上的表现
- MTEB 兼容，方便和 dense retrieval models 对比

**待 ingest：**
- CoIR paper: arXiv 2407.02883

### CrossCodeEval

**概述：**
- 来源：Ding et al., 2024
- Task：cross-file code completion，需要从其他文件检索相关代码
- 重点是 cross-file dependency retrieval

**为什么适合：**
- Cross-file retrieval 是 coding agent 的核心需求
- Import statements、function calls 等都是 lexical-faithful 的

**待 ingest：**
- CrossCodeEval paper

### RepoBench

**概述：**
- 来源：Liu et al., 2024
- Task：repository-level code completion
- 包含 retrieval 子任务：从 repo 中检索相关代码片段

**待 ingest：**
- RepoBench paper

## Code Embedding Models Survey

用于 dense retrieval baseline 对比：

| Model | Size | Type | Notes |
|---|---|---|---|
| Voyage Code 3 | API | Code-specific embedding | Voyage AI 的 code embedding model |
| CodeBERT | 125M | Encoder | Microsoft, 2020 |
| GraphCodeBERT | 125M | Encoder | Microsoft, 2021, 加入 data flow |
| UniXcoder | 125M | Encoder-Decoder | Microsoft, 2022 |
| StarCoder Embeddings | Various | Decoder-based | BigCode project |
| OpenAI text-embedding-3-small/large | API | General embedding | 也可用于 code |
| Jina Code v2 | 137M | Encoder | Code-specific |
| Nomic Embed Code | 137M | Encoder | Code-specific |

## Coding Agent Retrieval Methods

现有 coding agents 的 retrieval 策略，作为 industrial evidence：

### Cursor
- 自建 regex indexing engine
- Blog: "Fast regex search: indexing text for agent tools"
- Agent 大量使用 grep 作为核心工具
- 同时有 semantic search
References: [[2026-04-19-cursor-blog-reading-notes]]

### Claude Code
- 使用 Glob (file pattern matching) 和 Grep (ripgrep) 作为核心工具
- 没有 embedding-based retrieval
- Agent 通过 LLM 决定搜索什么关键词

### Aider
- 使用 tree-sitter 解析 AST
- 生成 repo map（文件结构 + 函数签名）
- 结合 grep-like 搜索

### SWE-agent
- 在 terminal 中使用 grep、find 等 UNIX 工具
- Agent 自主决定搜索策略
- 本质上是 LLM-compiled grep

### Agentless
- Hierarchical localization：先看 repo structure，再定位 file，再定位 class/function
- 不依赖 embedding
- 使用 LLM 直接推理

## GrepQA-Code Design

### Predicate Schema (Draft)

```json
{
  "must_keywords": ["error_keyword", "function_name"],
  "should_keywords": ["related_term", "synonym"],
  "file_pattern": "*.py",
  "language": "python",
  "scope": "function|class|file"
}
```

### Key Differences from Conversation GrepQA

| Aspect | Conversation GrepQA | GrepQA-Code |
|---|---|---|
| Retrieval unit | Conversation turn | File / function / code block |
| Speaker filter | Person name | N/A |
| File filter | N/A | File extension, path pattern |
| Window expansion | ±N turns | Function body, class body, or ±N lines |
| Keyword type | Natural language words | Identifiers, API names, error messages |
| Tokenization | Whitespace split | Code-aware tokenization (camelCase, snake_case splitting) |
| Scoring | OR-count per predicate | OR-count + possible IDF weighting |

### Code-Specific Challenges

1. **Identifier splitting**: `loadConfig` should match `load_config` and `LoadConfig`
2. **Import chains**: searching for `pandas` should also find `import pandas as pd`
3. **Multi-file context**: relevant code may span multiple files
4. **AST awareness**: function boundaries, class boundaries matter for window expansion

## Suggested Benchmark Selection for Paper

**Primary (必须做):**
1. **SWE-bench Verified** — file localization task, 500 instances
2. **CoIR** — comprehensive code retrieval benchmark

**Secondary (如果时间允许):**
3. **CodeSearchNet** — classic NL→code retrieval
4. **CrossCodeEval** — cross-file retrieval

**理由：**
- SWE-bench 是最有影响力的 coding benchmark，reviewer 一定认可
- CoIR 是最新的综合 benchmark，展示 breadth
- CodeSearchNet 和 CrossCodeEval 作为补充

## Open Questions

- GrepQA-Code 的 predicate generation prompt 应该如何设计？需要 code-specific examples
- Code domain 的 window expansion 应该用 AST-aware 的方式（function body）还是简单的 ±N lines？
- SWE-bench file localization 的 evaluation metric 是什么？Recall@K? Precision@K?
- 是否需要 code-aware tokenization（splitting camelCase/snake_case）？
- CoIR 的具体任务列表和 evaluation protocol 是什么？

## References

- [[2026-04-20-compiled-retrieval-nips-paper-plan]] — 总体 paper 计划
- [[2026-04-19-cursor-blog-reading-notes]] — Cursor blog 阅读笔记
- [[2026-04-19-compiled-lexical-retrieval-and-rag-benchmarks]] — 前期 framing 讨论
- [[../papers/bright-2025]] — BRIGHT benchmark
- [[../papers/mintlify-chromafs-2026]] — Mintlify virtual filesystem

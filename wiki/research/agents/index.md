---
title: Agents
domain: research
area: agents
type: overview
status: active
updated: 2026-10-09
tags: [research, agents, coding-agents, self-improvement, index]
---

# Agents

LLM agent 框架、编码 agent 与评测、自我改进与 harness 优化、test-time compute。由 `misc` 拆出（2026-10-09）；记忆相关见 [[research/agent-memory/index]]。

## Threads

- [Cursor Blog Reading Notes](threads/2026-04-19-cursor-blog-reading-notes.md)
- [Dream-RSI Search](threads/2026-09-17-dream-rsi-search.md)

## Agent Frameworks

| Paper | Year | Venue | Importance | Wiki Status |
|---|---:|---|---|---|
| [ReAct](assets/react-2022/note.md) | 2022 | ICLR | Reasoning-and-acting agent prompting | `processed` |
| [Recursive Language Models](assets/rlm-2026/note.md) | 2025 | Arxiv | Programmatic recursive calls over long context | `processed` |
| [LLM Test-Time Compute via Search Survey](assets/llm-inference-via-search-survey-2025/note.md) | 2025 | TMLR | Test-time search systems survey | `processed` |

## Coding Agents And Evaluation

| Paper | Year | Venue | Importance | Wiki Status |
|---|---:|---|---|---|
| [SWE-bench](assets/swebench-2024/note.md) | 2024 | ICLR | Real-world code issue benchmark | `agent-read` |
| [Agentless](assets/agentless-2024/note.md) | 2024 | Arxiv | Hierarchical code localization pipeline | `agent-read` |
| [Claude Code Lead Source Collection](assets/claude-code-lead-source-2026/note.md) | 2026 | Repo | Claude Code source meta-collection | `stable` |
| [CursorBench](assets/cursorbench-2026/note.md) | 2026 | Blog | Real-session coding benchmark design | `processed` |

## Self-Improving Agents And Harness Optimization

| Paper | Year | 改进对象 | Wiki Status |
|---|---:|---|---|
| [[assets/dream-rsi-2026/note|Dream-RSI]] | 2026 | 历史树回放优化 exploration-policy code；Google / DeepMind 等，arXiv v1 2026-09-14 | `processed` |
| [[assets/meta-harness/note|Meta-Harness]] | 2026 | 完整执行历史驱动 harness 代码搜索 | existing note |
| Experiential Reflective Learning | 2026 | 经验提炼与检索 heuristics（原归档已删除） | `processed` |

## Agentic Science

| Paper | Year | Venue | Importance | Wiki Status |
|---|---:|---|---|---|
| [EvoMaster](assets/evomaster-2025/note.md) | 2026 | Arxiv | Evolving agent framework for agentic science | `processed` |
| [SciMaster / X-Master](assets/scimaster-xmaster-2025/note.md) | 2025 | NeurIPS | General-purpose scientific agent | `processed` |

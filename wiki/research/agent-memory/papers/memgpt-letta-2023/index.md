---
title: "MemGPT: Towards LLMs as Operating Systems"
domain: research
area: misc
type: paper
status: processed
updated: 2026-04-18
tags: [paper, misc, memory, agents, retrieval, long-context]
---
# MemGPT: Towards LLMs as Operating Systems

## Paper Meta
- Title: MemGPT: Towards LLMs as Operating Systems
- Authors: Charles Packer, Sarah Wooders, Kevin Lin, Vivian Fang, Shishir G. Patil, Ion Stoica, Joseph E. Gonzalez
- Year: 2023
- Venue: not reported in extracted source
- Topic: misc
- Paper Slug: memgpt-letta-2023
- arXiv: https://arxiv.org/abs/2310.08560
- PDF: 2310.08560.pdf
- Code Repo: https://github.com/cpacker/MemGPT
- Reading Source: TeX source from `source/extracted/`; repo read from `repo/`; PDF fallback not used

## TL;DR
- MemGPT treats the LLM context window as a constrained memory hierarchy rather than a fixed prompt buffer.
- The system uses function calls to page information between main context and external storage, with queue eviction and recursive summaries to stay within limits.
- The strongest gains in the paper are on long-session conversation memory and multi-hop document retrieval, where fixed-context baselines collapse.

## Problem
- Fixed-context LLMs cannot hold long conversations or large document collections in prompt forever.
- The paper argues that simply scaling context is expensive and still imperfect: long-context models remain uneven in how they use tokens.
- The core question is whether an OS-style memory hierarchy can provide an effective illusion of longer context without changing the base model architecture.

## Method
- MemGPT splits memory into `main context` and `external context`.
- `main context` contains system instructions, working context, and a FIFO queue; `external context` contains recall storage and archival storage.
- A queue manager warns about memory pressure, flushes overflowing history, and rebuilds a recursive summary of evicted messages.
- A function executor lets the model read and write memory, search archival storage, and chain multiple function calls before returning to the user.
- The control flow is event driven: user messages, system warnings, scheduled events, and other triggers can all invoke inference.

## Benchmarks / Datasets
| Dataset / Benchmark | Task | Metric | Notes |
|---|---|---|---|
| Multi-Session Chat (MSC) | Deep memory retrieval | Accuracy, ROUGE-L recall | New session 6 added; tests recall across sessions 1-5 |
| MSC | Conversation opener | SIM-1, SIM-3, SIM-H | Measures whether the opener reflects persona memory |
| NaturalQuestions-Open + late-2018 Wikipedia | Document QA | LLM-judge correctness | 50 sampled questions; top-K retriever settings |
| Synthetic nested KV | Multi-hop key-value retrieval | Accuracy | 140 UUID pairs, 0-4 nesting levels, 30 orderings |

## Baselines
| Baseline | Type | Why Important | Notes |
|---|---|---|---|
| GPT-3.5 Turbo | Fixed-context LLM | Weakest context and function-calling baseline | Compared with and without MemGPT |
| GPT-4 | Fixed-context LLM | Stronger baseline for long-context tasks | Used for both conversation and document tasks |
| GPT-4 Turbo | Fixed-context LLM | Largest context among the paper's OpenAI baselines | Also paired with MemGPT |
| Human opener | Human reference | Upper bound for the opener task | SIM-H = 1.000 by definition |

## Main Results
| Dataset / Benchmark | Metric | Baseline | Ours | Gain / Delta | Notes |
|---|---|---|---|---|---|
| MSC deep memory retrieval | Accuracy | GPT-3.5 Turbo: 38.7% | GPT-3.5 Turbo + MemGPT: 66.9% | +28.2 pts | ROUGE-L R also rises from 0.394 to 0.629 |
| MSC deep memory retrieval | Accuracy | GPT-4: 32.1% | GPT-4 + MemGPT: 92.5% | +60.4 pts | ROUGE-L R rises from 0.296 to 0.814 |
| MSC deep memory retrieval | Accuracy | GPT-4 Turbo: 35.3% | GPT-4 Turbo + MemGPT: 93.4% | +58.1 pts | Best reported result in the paper |
| MSC conversation opener | SIM-H | Human: 1.000 | GPT-3.5 Turbo + MemGPT: 0.817 | not a direct gain metric | MemGPT can exceed the human opener on SIM-1/SIM-3 with stronger bases |
| MSC conversation opener | SIM-1 / SIM-3 | Human: 0.800 / 0.800 | GPT-4 + MemGPT: 0.868 / 0.843 | +0.068 / +0.043 vs human | Strongest opener scores in the table |
| Document QA | Accuracy curve | Fixed-context truncation degrades as K grows | MemGPT unaffected by increased context length | not reported numerically in extracted text | Figure claims GPT-4 and GPT-4 Turbo are equivalent here |
| Nested KV | Accuracy curve | GPT-3.5 hits 0% at 1 nesting; GPT-4 and GPT-4 Turbo hit 0% by 3 | MemGPT with GPT-4 remains effective across nesting levels | not reported numerically in extracted text | MemGPT with GPT-4 Turbo is worse than with GPT-4 |

## Ablations / Analysis
- GPT-4 is the strongest base model for MemGPT in this paper; GPT-3.5 Turbo suffers from weaker function-calling and degrades sharply on nested lookups.
- For document QA, the retriever is still a limiting factor: if the gold Wikipedia article is not surfaced, the fixed-context baselines cannot recover it.
- MemGPT can page through archival results iteratively, but the paper notes that it may stop before fully exhausting the retriever database.

## Implementation Clues
- The repo read is useful, but it is a later Letta codebase rather than a minimal paper artifact.
- `pyproject.toml` declares the package as `letta` version `0.16.7`, with `letta = "letta.main:app"` as the CLI entry point.
- `letta/main.py` registers `server` as the default command, so the CLI boots a server when run without a subcommand.
- `letta/agent.py` implements the memory-management loop: context overflow warnings, tool execution, message routing, and updates to memory blocks.
- `letta/config.py` shows archival, recall, and metadata storage defaults; sqlite is the default local storage path in the config object.

## Limitations
- The system depends on the underlying model's tool-use quality; GPT-3.5 Turbo is notably weaker than GPT-4 variants.
- Retrieval quality still matters: document QA performance is bounded by the retriever and can miss the gold article.
- The paper relies on LLM judges for both DMR and document QA, so the evaluation is not purely human-scored.
- Exact prompts and some implementation details are deferred to the project website rather than fully reproduced in the paper text.

## Takeaways
- The main contribution is not a new base model, but a memory and control-flow layer that lets an LLM behave as if it had a larger context.
- The strongest evidence is on tasks that require explicit recall and iterative retrieval, where fixed-context baselines fail hard.
- The OS analogy is operational, not just rhetorical: paging, summaries, warnings, and function chaining are all part of the system design.

## Open Questions
- How much of the gain comes from better retrieval policy versus the hierarchical memory abstraction itself?
- Would the same approach remain useful as base models get larger context windows and better native tool use?
- What policies best decide when to store, summarize, evict, or re-retrieve memory in practice?

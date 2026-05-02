---
title: "A Survey on LLM Test-Time Compute via Search: Tasks, LLM Profiling, Search Algorithms, and Relevant Frameworks"
domain: research
area: misc
type: paper
status: processed
updated: 2026-04-18
tags:
  - paper
  - survey
  - lis
  - llm-search
  - tmlr
---
# A Survey on LLM Test-Time Compute via Search: Tasks, LLM Profiling, Search Algorithms, and Relevant Frameworks

## Paper Meta
- Title: A Survey on LLM Test-Time Compute via Search: Tasks, LLM Profiling, Search Algorithms, and Relevant Frameworks
- Author: Xinzhe Li
- Year: 2025
- Venue: Transactions on Machine Learning Research (accepted TMLR style in source)
- arXiv: 2501.10069
- Source Read: TeX (`main.tex` + `sections/*` + `tables/*` + `main.bbl`)
- Repo Read: README placeholder only; no implementation code in local repo
- PDF Fallback: not used

## TL;DR
- The survey organizes "LLM inference via search" as sequential decision making: tasks are unified as MDP-like problems, LLM behavior is split into policy/value/transition roles, and reusable search procedures are factored out from framework-specific details.
- The main contribution is a comparison lens, not a new algorithm: it standardizes task definitions, clarifies how LLM priors are used inside search, and shows where LLM search departs from classical BFS/DFS, best-first search, A*, and MCTS.
- The paper covers 25+ related works in the core search sections and expands beyond them to world-model generation, meta-search, evolutionary search, fine-tuning for test-time compute, multimodal search, reranking, and sequential revision.

## Problem
The field had accumulated many search-based LLM systems, but they were hard to compare because each paper mixed together different task definitions, prompting/evaluation choices, and search-control logic. The survey says the main pain points are:
- task formulations that are not standardized across reasoning, planning, web navigation, graph traversal, code generation, and dialog
- LLM-side design choices that are described inconsistently
- search procedures that borrow names from classical algorithms but silently change their behavior
- limited visibility into how frameworks deviate from classical search assumptions such as fixed action spaces, clean transition models, and admissible heuristics

## Method
The survey uses three stacked abstractions.

### 1) Task unification as MDP-like problems
The task table in `tables/tasks.tex` maps LIS workloads into a common state/action/transition/reward view. The main families are:

| Task family | Core shape | Typical reward | Reversible? | Example benchmarks |
|---|---|---|---|---|
| Embodied tasks | discrete, state-dependent actions in physical environments | goal reached = 1 | maybe | VirtualHome, Jericho |
| Combinatorial tasks | discrete, constrained, state-dependent moves | default goal reward | maybe | Game of 24, Chess |
| Web navigation | constrained heterogeneous actions over pages | default goal reward | maybe | WebShop, WebArena |
| Graph traversal | homogeneous actions over finite graphs | 1 if goal node reached | maybe | GridMap |
| Reasoning via concatenation | thoughts are actions, state is concatenated trace | 1 if answer matches ground truth | yes | GSM8K, Math, HotpotQA, ToT-Writing |
| Reasoning via QAs | subquestions and answers become the evolving state | 1 if answer matches ground truth | yes | HotpotQA, GSM8K |
| Reasoning via concatenation + tools | thoughts plus tool calls | 1 if answer matches ground truth | maybe | HotpotQA |
| Reasoning over knowledge graph | entity-relation triplets plus open thoughts | 1 if answer matches ground truth | yes | WebQSP |
| Tool-based tasks | action sequences over external APIs | task completed = 1 | maybe | GSM8K, ToolBench |
| Code generation | token-level search over programs | pass rate of complete program | yes | MBPP, APPS |
| Goal-oriented dialog | intents plus agent/user utterances | conversational goal achieved | no | PersuasionForGood |

### 2) LLM-profiled roles
The survey factors LLM use into three agentic roles:
- `LMPP` for policy generation
- `LMPE` for evaluation/value estimation
- `LMPT` for transition modeling

Concrete implementations are summarized in the source tables:
- `LMPP`: deterministic, batch, and stochastic policies
- `LMPE`: binary/multi-class classification, logits, multi-choice QA, implicit continuation scoring, continuous scoring, and episode-level verbalization
- `LMPT`: generation of full states or partial observations, especially useful in dynamic environments

### 3) Reusable search procedures
The search-procedure section decomposes search into modular operations:
- LMPP sampling
- LMPE+ evaluation
- LMPT simulation
- multi-choice LMPE selection
- UCT / PUCT selection
- exhaustive action retrieval
- value-based top-k selection
- threshold selection
- expansion
- path simulation
- MCTS selection and backpropagation

This modular view is then used to compare frameworks by algorithm family rather than by paper-specific implementation details.

## Benchmarks / Datasets
The source does not report new experimental benchmarks; it surveys benchmarks used by prior work. The recurring ones are:

| Benchmark | Used for |
|---|---|
| GSM8K | reasoning, tool-based reasoning, alpha-MCTS variants |
| Math | reasoning via concatenation |
| HotpotQA | reasoning and tool-augmented reasoning |
| WebShop | web navigation |
| WebArena | web navigation |
| GridMap | graph traversal / path finding |
| Game of 24 | combinatorial search |
| Chess | combinatorial search |
| VirtualHome | embodied tasks |
| Jericho | embodied tasks |
| WebQSP | knowledge-graph reasoning |
| MBPP | code generation |
| APPS | code generation |
| ToolBench | tool-based tasks |
| PersuasionForGood | goal-oriented dialog |

## Baselines
The survey compares LIS frameworks against classical search families and nearby LLM inference methods.

| Family | Representative methods in the source | Main difference emphasized by the survey |
|---|---|---|
| Beam search | Beam-LLM, PathFinder, Think-on-Graph, Think-on-Graph 2.0 | beam search is often paired with LLM-based scoring rather than plain heuristic ranking |
| BFS / DFS | Tree-of-Thoughts | LLM priors make these searches more informed than classical uninformed search |
| Best-first search | Best-LLM | the heuristic is often an LLM-derived value estimate |
| A* | LLM-A*, Q*, ToolChain | LLM heuristics can violate admissibility; cost/value polarity is often inverted |
| MCTS | RAP, LATS, LLM-MCTS, rStar, MC-DML | rollout, selection, and backpropagation are modified with LLM sampling/evaluation |
| alpha-MCTS | PG-TD, GDP-ZERO, TS-LLM, ReST-MCTS* | search is entangled with training or preference optimization |

The paper also contrasts LIS with:
- ReAct, CoT, and Self-Consistency as components rather than full search frameworks
- reranking methods such as LEVER and DiVeRSe
- sequential revision methods such as Self-refine

## Main Results
This is a survey, so the main outputs are synthesis and coverage rather than benchmark scores.

| Survey-level claim | Source-backed detail |
|---|---|
| Broader coverage than earlier surveys | the comparison table says the survey covers 25+ papers, while earlier surveys cover 3-8 papers |
| More detailed task formalization | task definitions are unified explicitly under MDP-like notation |
| More detailed LLM profiling | the survey enumerates 8 policy implementations, 4 evaluator dimensions with 14 implementations, and 2 transition implementations |
| More explicit search analysis | the paper separately describes search procedures, framework families, deviations, applicability, performance, and efficiency |
| No new empirical gains are reported | not reported; the paper is comparative and taxonomic |

## Ablations / Analysis
No ablation study is reported by the survey itself. The analysis section instead focuses on failure modes and structural differences:
- classical BFS/DFS become heuristic-driven once LLM priors are inserted
- A* can lose optimality when the heuristic depends on policy-generated states
- MCTS can degenerate early if all candidates receive equal or zero scores
- LLM-based tree search can be slower than iterative refinement; the source cites 10-20x slower behavior in some settings when evaluators are weak
- caching, KV reuse, and tree-structured attention are presented as the main efficiency levers

## Implementation Clues
- `source/extracted/main.tex` is only the wrapper; the actual content lives in `sections/*` and `tables/*`
- `tables/tasks.tex` is the most useful anchor for task taxonomy and benchmark mapping
- `tables/lmpr_eval.tex` is the key reference for evaluator variants and how they map to `V` and `Q`
- `tables/frameworks.tex` is the main inventory of search-based frameworks and their algorithm families
- `tables/procedure_dependency.tex` shows which procedures depend on LMPP, LMPE, or LMPT
- `repo/README.md` is only a placeholder, so the local repo does not contribute implementation detail in this pass

## Limitations
- The survey itself says the MDP formalism can feel heavy for readers who only care about one framework.
- Many frameworks assume reversible actions or easy state restoration, which narrows applicability in irreversible environments.
- The survey focuses on sequential decision-making tasks; it explicitly separates out other LLM + search directions such as world-model generation, meta-search, evolutionary search, reranking, and sequential revision.
- Rapid field movement means the coverage is substantial but not exhaustive; some newer or under-review papers may be missing.

## Takeaways
- The most durable contribution is the abstraction layer: task -> LMPR -> search procedure -> framework.
- LLM search is not just classical search with a language model inserted; the model often changes the meaning of actions, values, transitions, and even search optimality assumptions.
- If you want to compare or implement a new LIS method, the most useful starting point is to specify:
  - the MDP-style task
  - the policy/evaluator/transition roles
  - whether the control loop is beam, DFS, best-first, A*, MCTS, or alpha-MCTS
  - whether actions are reversible and whether simulation happens in the environment, in a simulator, or via LMPT

## Open Questions
- How should we compare LIS methods when the LLM heuristic is not admissible or not calibrated?
- What is the right way to handle irreversible actions without relying on environment reset or backtracking tricks?
- When is exhaustive action retrieval cheaper and better than LLM sampling?
- Can we standardize evaluator calibration across binary, multi-class, and continuous scoring setups?
- Which tasks really benefit from tree search at test time versus sequential revision or reranking?

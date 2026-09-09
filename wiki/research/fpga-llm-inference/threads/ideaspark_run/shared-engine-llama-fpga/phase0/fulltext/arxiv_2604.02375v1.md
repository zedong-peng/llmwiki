# KAIJU: An Executive Kernel for Intent-Gated Execution of LLM Agents

paper_id: arxiv:2604.02375v1
tier: T3
source_used: html_arxiv
warning: none

## Intro

LLM-based agents that invoke external tools (APIs, shell commands, databases, web services) have become a dominant paradigm for grounding language models in real-world action. The foundational execution model is ReAct
(Yao
et al.
,
2023
)
: the model reasons about which tool to call, executes it, observes the result, and repeats. Modern implementations in production systems such as OpenAI’s Assistants API, Anthropic’s Claude Code, and OpenClaw extend this with native parallel function calling; the model can return multiple tool calls per turn, significantly reducing the number of reasoning round-trips. On straightforward queries, this approach is fast and effective.
Three problems emerge as task complexity grows. First, each reasoning turn still carries the full conversation history. Turn
i
i
transmits
c
+
i
​
k
c+ik
tokens, where
c
c
is the system context and
k
k
is the average tool result size. Total cost across
n
n
turns is
O
​
(
n
2
​
k
)
O(n^{2}k)
; for typical values of
k
≈
1
k\approx 1
K tokens, a 7-tool task transmits approximately 63K tokens; an 18-tool task approximately 250K. On multi-step computational queries, this cumulative context can exhaust the effective processing window, producing empty or degraded outputs. Second, the model retains unilateral authority over tool use at every turn. When a tool call fails or returns partial results, the model can abandon the task, defer to parametric knowledge, or ask the user for guidance; behaviour that is rational per-turn but undermines reliability across the full query. Prompt instructions to persist (“never give up, always retry”) partially mitigate this but cannot guarantee it; the model may comply or not on each turn. Third, tool safety is enforced via prompt instructions (“do not call destructive tools”), which the model can ignore through hallucination, prompt injection, or context overflow. There is no structural failsafe.
Nasr
et al.
(
2025
)
demonstrate that LLM-level defenses whether training-based, prompt-based, or filter-based are systematically defeated by adaptive adversaries who modify their attack strategy against the defense’s observable behaviour.
Prior systems address these problems partially. LLM Compiler
(Kim
et al.
,
2024
)
introduced parallel DAG execution but evaluates results only after the entire graph completes, with no mid-execution adaptation and no safety gating. LangGraph
(LangChain Inc.,
2024
; Biju,
2025
)
models workflows as state machines but keeps the LLM in the execution loop at every routing decision, with safety limited to human-in-the-loop breakpoints. Multi-agent frameworks (
CrewAI (
2024
)
, AgentArch
(Bogavelli
et al.
,
2026
)
) add coordination overhead that degrades both performance and reliability;
Bogavelli
et al.
(
2026
)
found that even the best configurations achieved only 35.3% success on complex enterprise tasks with 6.3% reproducibility. In each case, the model remains coupled to execution semantics.
We introduce KAIJU, with a strict execution abstraction consisting of two layers: a reasoning layer handling user interaction, and an execution layer responsible for dependency resolution, tool dispatch, failure recovery, safety enforcement, and result synthesis. In the execution layer the LLM is a stateless resource invoked at discrete points (to plan, to reflect, and to aggregate) with no visibility into execution mechanics. The execution layer invokes the reasoning model once to produce a dependency graph of tool calls, then schedules, gates, and dispatches tools independently, constituting the first graph node. At structured leaf nodes, a lightweight reflector evaluates the evidence gathered so far against the original query and decides whether to continue, conclude, or replan with targeted follow-up nodes. An execution gate (IGX) enforces authorisation via four independent variables (scope, intent, impact, and clearance), each governed by a separate authority outside the model.
The LLM does not observe gate decisions within the execution layer, removing the possibility of adaptive probing of the safety policy. In conversational loops (ReAct, LangGraph), blocked tool calls feed back into the model’s context, enabling adversarial probing; our architecture removes the feedback channel. Critically, data are only input to the execution layer from the reasoning layer at call time and fed back only at return time, creating a closed execution loop, except for preemption as described in Section
4.5
. The execution layer persists through tool failures via automatic replanning rather than deferring to the user. It does not ask for permission or silently substitute parametric knowledge; when a tool fails, the micro-planner retries with alternative approaches before the reflector evaluates whether sufficient evidence has been gathered. The graph is processed optimistically (execute first, adapt on failure via reflection checkpoints) across three adaptive modes.
A structured graph-based LLM workflow enables composable, verifiable execution units, providing a foundation for enforcing guarantees such as security and content policy and service level agreements. Nodes can be added or removed to improve or alter the graph mid-flight enabling custom and controlled outcomes. In our system, three execution modes provide progressively finer-grained mid-execution adaptation: structural phase boundaries (Reflect), periodic batch checkpoints (nReflect), and per-node observers (Orchestrator).
Contributions of IGX:
1.
Separation + bounded context
→
\rightarrow
reduced token scaling.
The planner and per-node observers operate on bounded context. Reflections see cumulative evidence within the execution layer but not the full conversational history. Token complexity reduces from
O
​
(
n
2
​
k
)
O(n^{2}k)
to
O
​
(
n
​
k
​
d
)
O(nkd)
in Reflect mode or
O
​
(
n
​
k
)
O(nk)
in Orchestrator mode, where
d
d
is dependency depth.
2.
Separation + parallelism
→
\rightarrow
schedulable.
The execution graph fires tools on dependency resolution, not LLM decision. Three adaptive modes (Reflect, nReflect, Orchestrator) reduce latency to
O
​
(
d
)
O(d)
where
d
d
is dependency depth, compared to
O
​
(
n
)
O(n)
for sequential dispatch or
O
​
(
t
)
O(t)
for parallel function calling (where
t
t
is reasoning turns,
t
≪
n
t\ll n
but structurally unbounded).
3.
Separation + enforcement
→
\rightarrow
structurally enforced safety.
A four-variable gate (scope, intent, impact, clearance) enforces authorisation deterministically in compiled code. Gate decisions do not reach the model; it does not distinguish a blocked tool from a failed one, preventing adaptive iteration against the policy.
4.
Separation + dataflow
→
\rightarrow
structural dependency injection.
A
param_refs
mechanism expresses data flow between steps at plan time; concrete values resolve at execution time from upstream outputs. This removes the need for a sequential reasoning loop to pass data between tool calls.
5.
Delegated resource clearance.
Resource-level authorisation delegates to external HTTP endpoints, enabling deployment across cybersecurity, robotics, enterprise, and healthcare environments without domain-specific logic in the agent.
The remainder of this paper is organised as follows. Section
2
surveys related work. Section
3
introduces an example illustrating key properties. Section
4
defines the system model and graph structure. Section
5
describes the three execution modes. Section
6
presents the execution gate. Section
7
reports experimental results. Section
8
concludes with limitations and future directions.

## Method

We illustrate with the following query:
“Check disk usage, list open ports, find git repos under /home, search for CVEs affecting our kernel version, and check environment variables for leaked secrets.”
This requires five independent data-gathering operations, a dependency chain (kernel version must be discovered before searching for CVEs), and cross-domain synthesis. Both queries were run through the same system instance with identical tools.
ReAct with parallel function calling — 9 turns, 14 tools, 64.5s.
turn 0: disk_usage, net_info, bash find,
turn 0:
uname, env_list
2K
turn 1: web_search CVE
4.3K
turn 2: web_fetch
4.5K
turn 3: web_search, bash
5.1K
turn 4--6: web_fetch, web_search, bash grep
5.9K
turn 7: bash
6.2K
turn 8: synthesise
→
\rightarrow
final report
6.2K
Modern parallel function calling batches 5 tools on turn 0, reducing the original 12-turn sequential baseline to 9 turns. However, each subsequent turn still carries the full conversation history; by turn 8 the context exceeds 6K tokens. The model decides per-turn whether to continue researching or conclude; turns 1–7 show it pursuing CVE details across multiple sequential search-fetch cycles. Total: 9 LLM calls, 14 tool executions, 64.5 seconds.
IGX (DAG, Reflect) — 4 LLM calls, 10 nodes, 41.8s.
planner (5s)
disk_usage
reflect #1: replan
need ports, git, kernel, env
net_info
bash find
bash uname
env_list
reflect #2: replan
need CVE search + secret scan
web_search CVE
bash grep secrets
reflect #3: conclude
The planner under-planned on this query, producing only one node initially. The reflection loop compensated: three reflections identified gaps and replanned with targeted follow-ups across two additional waves. Despite this, the DAG completed in 41.8 seconds versus ReAct’s 64.5 seconds because each wave executed tools in parallel and each reflection saw only the current wave’s results (bounded context) rather than the full conversation history. The CVE search in wave 3 used the kernel version discovered in wave 2. Total: 4 LLM calls (planner + 3 reflections), 10 tool executions, 41.8 seconds. The final reflection produced the verdict directly, skipping the aggregator.
The running example illustrates three key properties.
(1) Parallel execution within dependency waves reduces wall clock time even when the planner under-plans; the reflection loop compensates by identifying gaps and launching targeted follow-up waves. (2) Bounded context per LLM call: each reflection evaluates only the current wave’s evidence, not all prior tool results, avoiding the cumulative context growth visible in the ReAct trace (2K
→
\rightarrow
6.2K). (3) The execution layer persists through incomplete plans via structural replanning; the model cannot decide to stop early or defer to the user.

# Executing as You Generate: Hiding Execution Latency in LLM Code Interpreters

paper_id: arxiv:2604.00491v2
tier: T3
source_used: pdf_arxiv_pymupdf
warning: none

## Intro

Modern LLM systems increasingly act not by producing
text alone but by producing code that is run on the user’s
behalf. A growing class of systems hands the model a code
interpreter: the model writes a self-contained program, an
interpreter executes it, and the result is returned to the user or
fed back to the model for the next step. This pattern underlies
commercial tools such as Anthropic’s Claude code execution
tool [1] and OpenAI’s Code Interpreter [2], as well as research
systems such as CodeAct [3] and Open Interpreter [4], where
executable Python program is the unit of action. In these
settings the program is usually a short, single-file script that
runs a piece of data analysis or produces a plot, and the
user waits for the whole writing-and-running process to finish
before seeing a result.
This workflow is serial, where the model first generates the
complete program, and only after the final token is emitted
does execution begin. While the model is generating, the
∗These authors contributed equally to this research.
Serial
Generate
LLM
𝑇𝑔𝑒𝑛
𝑇𝑠𝑒𝑟𝑖𝑎𝑙
Idle
Executor
Execute
Idle
Generate
LLM
𝑇𝑝𝑎𝑟𝑎𝑙𝑙𝑒𝑙
Idle
Executor
Exec.
Idle
Saved
Parallel
Idle
Idle
Idle
Exec.
Exec.
Exec.
Time
Fig. 1: An illustrative example comparing Serial Execution and
Parallel Execution. For a code snippet with four chunks, Parallel
Execution overlaps the first three chunks with the generation process,
saving the corresponding waiting time.
interpreter sits idle. While the interpreter runs, the model has
nothing left to do. The user-perceived latency is therefore the
sum of two phases that run back to back, even though running
an early Python statement never requires the later code to be
generated first.
Our starting observation is a property of how these models
write code. A human developer revises constantly, jumping
back to edit earlier lines, so a program is only safe to run
once the developer decides it is done. A token-based language

## Method

decoding, it emits tokens from left to right and never rewrites a
token once it has been produced, so every prefix of the output
is already final. As soon as the model has emitted a complete
statement, that statement is exactly what will appear in the
finished program, and there is no reason to wait for the rest of
the code before running it. We call this idea parallel execution:
each statement is dispatched to the interpreter the moment it
is complete, so that execution of earlier statements overlaps
with generation of later ones. Figure 1 illustrates the effect.
Serial execution costs roughly Tgen + Texec, whereas parallel
execution costs roughly Tgen + Ttail, where Tgen, Texec, and
Ttail denote the generation time, the total execution time, and
the execution time of only the final chunk, respectively.
To the best of our knowledge, the parallel paradigm between
the execution and generation of LLM-produced code has not
yet been explored in the research community. Prior work has
arXiv:2604.00491v2  [cs.PL]  22 Jun 2026

proposed incremental execution strategies [4], [5], where a
model generates a few lines, executes them, and conditions
subsequent generation on the observed output. For example,
Open Interpreter [4] executes code in Jupyter-style cells and
feeds the output back to the model, and EG-CFG [6] integrates
real-time execution signals into the code generation process.
These approaches use execution feedback to improve code
quality by steering subsequent generation. However, they are
still fundamentally serial with respect to latency: the model
must pause generation while awaiting each execution result,
and the total wall-clock time includes both generation and
execution in full. In contrast, the parallel execution paradigm
we propose targets a complementary goal: reducing user-
perceived latency by overlapping generation and execution,
without altering the generated code. As a result, the following
question remains open: Is parallel execution of LLM-generated
code practically viable, and what are its benefits and costs?
To realize this paradigm, we present EAGER (Executing
As you GEneRate), a code execution framework to support
script-style code generation. We demonstrate this paradigm
for Python, the dominant language in LLM code generation,
though the principle applies to other interpreted languages. Its
core design follows a producer–consumer pipeline, where the
LLM acts as the producer and the executor as the consumer. As
the language model generates tokens, an AST-based chunker
incrementally identifies complete Python statements from the
token stream and enqueues each chunk into a buffer. Concur-
rently, an executor dequeues and runs available chunks within
a persistent interpreter session, preserving variable bindings
across successive batches. The executor employs a dynamic
batching strategy: when multiple chunks have accumulated in
the queue, it merges them into a single batch, thereby amor-
tizing the per-invocation setup overhead. Additionally, EAGER
features an optional early error interruption mechanism: since
chunks are executed as they are generated, a runtime error
in any chunk is detected immediately, at which point EAGER
terminates the LLM generation and returns the error along with
the partially generated code. This avoids wasting generation
time on code that depends on already-failed state.
We evaluate EAGER across four Python benchmarks, seven
LLMs, and three execution environments. The overlap mech-
anism hides most execution behind generation. It drives the
non-overlapped portion of execution time to near zero in most
settings and lowers end-to-end latency by up to 37.3% on
error-free runs, with the largest gains where generation is fast
relative to execution, so that execution makes up a larger share
of total latency. The optional early interruption avoids wasting
generation on already-failed code, and by handing the model
earlier and more focused error feedback it raises subsequent
repair success by up to 44.3 percentage points on data-centric
benchmarks. This prevents the model from being anchored by
the incorrect code generated after the error, giving it more
freedom to produce a corrected solution.
We open-source our artifacts at https://doi.org/10.6084/m9.
figshare.31869469. In summary, this paper makes the follow-
ing contributions:
• We formalize parallel execution for LLM code interpreters
and derive closed-form latency bounds that identify its
speedup potential and the regimes where it pays off, includ-
ing the condition under which it never regresses below serial
execution, namely when the cumulative per-chunk overhead
stays within the one-time serial setup cost.
• We present EAGER, a Python implementation featuring
AST-based chunking, gated dynamic batching, and early
error interruption.
• We evaluate EAGER on four benchmarks, seven LLMs, and
three environments, reporting the latency benefit of overlap
and the repair benefit of early interruption separately, along
with the conditions under which each applies.
II. PARALLEL EXECUTION
In this section, we introduce the general workflow of parallel
execution and theoretically analyze its latency.
A. Workflow
Current LLMs follow a strictly sequential paradigm for code
execution: the model first generates the entire program and
only then invokes the execution environment. This results in
a clear temporal separation between generation and execution,
leading to significant idle time on both sides.
We instead formulate the process as a streaming pipeline.
The LLM acts as a producer that autoregressively emits
tokens. A detection module continuously processes the token
stream to identify executable chunks, defined as minimal
syntactically complete and semantically executable units. Once
a chunk is detected, it is immediately dispatched to an execu-
tion engine, which maintains a persistent session to preserve
program state. This design enables temporal overlap across
all stages: while the LLM generates tokens for later chunks,
earlier chunks can already be detected and executed.
B. Theoretical Modeling
We model the system as a three-stage pipeline consisting
of generation, detection, and execution. The total latency is
determined by the critical path through these stages.
Notation. We define:
• L: total number of tokens,
• vgen: generation speed (tokens per second),
• TF T : time-to-first-token,
• N: number of executable chunks,
• li: length of chunk i, with PN
i=1 li = L,
• δi: residual detection delay for chunk i (the portion of
detection cost not hidden behind generation),
• Tsetup: per-chunk execution overhead,
• Texe,i: execution time of chunk i.
1) Serial Execution: In the serial paradigm, the model first
generates the complete program, after which the interpreter
executes it as a monolithic block. The total latency is therefore:
Tserial = TF T +
L
vgen
+ T (full)
setup + T (full)
exe ,
(1)

where T (full)
setup denotes the one-time execution setup cost for
the complete program, and T (full)
exe
denotes the execution time
of the full program.
For consistency with the chunked formulation, one may
approximate:
T (full)
exe
≈
N
X
i=1
Texe,i,
(2)
but importantly, the serial baseline does not incur repeated
per-chunk setup overhead or streaming detection overhead.
2) Parallel Execution: In the parallel paradigm, generation,
detection, and execution are overlapped. Let tg,i denote the
time when chunk i has been fully generated, and let te,i denote
the time when execution of chunk i completes.
Generation. The time at which chunk i has been fully
generated depends on the cumulative token length of all
preceding chunks:
tg,i = TF T +
Pi
j=1 lj
vgen
(3)
Detection. The detector processes the token stream online.
We write the chunk-ready time as:
td,i = tg,i + δi
(4)
where δi is the residual detection delay, i.e., the portion of
detection cost that is not hidden behind generation.
Execution. Chunk i can only start executing once it has
been detected from the generated code and the previous chunk
has finished executing:
te,i = max(td,i, te,i−1) + Tsetup + Texe,i
(5)
The overall parallel latency is the completion time of the final
chunk:
Tparallel = te,N
(6)
Closed-form characterization. Unrolling the recurrence
gives
Tparallel = max
1≤i≤N

tg,i + δi +
N
X
j=i
(Tsetup + Texe,j)


(7)
3) Latency Bounds: The closed-form expression of the
parallel execution allows us to derive upper and lower bounds
on the latency.
Upper bound. For any i ∈{1, . . . , N}, the generation
prefix satisfies Pi
j=1 lj ≤L, the detection residual satisfies
δi ≤¯δ ≜max1≤k≤N δk, and the execution tail satisfies
PN
j=i(Tsetup + Texe,j) ≤PN
j=1(Tsetup + Texe,j). Applying
these to every term inside the outer maximum yields
Tparallel ≤TF T +
L
vgen
+ ¯δ + N Tsetup +
N
X
j=1
Texe,j
(8)
This upper bound corresponds to a zero-overlap execution
in which every stage waits for its predecessor to complete
entirely. Compared with the serial baseline, the additional cost
is at most
Tparallel −Tserial ≤¯δ + N Tsetup −T (full)
setup
(9)
, which captures the overhead from (i) streaming detection
and (ii) repeated per-chunk setup. In practice ¯δ is on the
order of milliseconds because the detector operates on a
lightweight grammar, so the overhead is dominated by the
cumulative setup cost N Tsetup −T (full)
setup. When both ¯δ and
N Tsetup −T (full)
setup are negligible, the upper bound reduces
to Tserial, showing that the parallel scheme introduces no
regression under these conditions.
Lower bound. Two structural constraints yield complemen-
tary lower bounds.
1) Generation constraint (setting i = N). The system must
generate all tokens before the last chunk can complete:
Tparallel ≥TF T +
L
vgen
+ δN + Tsetup + Texe,N
(10)
2) Execution constraint (setting i = 1). The system must
execute all chunks in order after the first chunk becomes
available:
Tparallel ≥TF T + l1
vgen
+δ1+N Tsetup+
N
X
j=1
Texe,j (11)
Combining both gives the composite lower bound:
Tparallel ≥max







TF T +
L
vgen
+ δN + Tsetup + Texe,N,
TF T +
l1
vgen
+ δ1 + N Tsetup + PN
j=1 Texe,j







(12)
The first term dominates when generation is the bottleneck
(generation-dominated regime); the second dominates when
execution is the bottleneck (execution-dominated regime).
4) Speedup
Bounds:
Define
the
speedup
S
=
Tserial/Tparallel. From the lower bound (10) on Tparallel, the
speedup is at most:
S ≤
TF T +
L
vgen + T (full)
setup + T (full)
exe
TF T +
L
vgen + δN + Tsetup + Texe,N
(13)
when δN and Texe,N are small relative to L/vgen, which
simplifies to S ≲1+(T (full)
setup+T (full)
exe )/(TF T +L/vgen). This is
achieved when all execution is hidden behind generation. From
the upper bound (8), S ≥1 whenever T (full)
setup ≥¯δ + N Tsetup,
i.e., the one-time serial setup cost exceeds the cumulative
chunk overhead. Whether this condition holds depends on
the execution environment. In our experimental setup, where
chunks are dispatched to a persistent REPL session with per-
call overhead on the order of 1 ms, Tsetup and ¯δ are both
small enough for the condition to be satisfied comfortably.
However, in environments with heavier per-chunk orchestra-
tion costs (e.g., container cold starts or cross-process IPC), the
cumulative term N Tsetup may become non-negligible, and the
condition should be verified empirically.

5) Regime Analysis under Uniform Chunks: To obtain
sharper insight, we analyze the special case of uniform chunks:
li = L/N, Texe,i = τe, and δi = δ. Define the per-chunk
generation time α ≜L/(N vgen) and per-chunk execution
time β ≜Tsetup + τe. The inner term of the closed-form
expression becomes affine in i:
f(i) = TF T + δ + (N + 1)β
|
{z
}
constant
+i (α −β)
(14)
yielding the following three regimes:
R1: Generation-dominated (α > β). The maximum is at
i = N:
Tparallel = TF T +
L
vgen
+ δ + β
(15)
Execution of every chunk except the last is entirely hidden
behind generation.
R2: Execution-dominated (α < β). The maximum is at
i = 1:
Tparallel = TF T + α + δ + Nβ
(16)
Generation of every chunk except the first is hidden behind
execution.
R3: Balanced (α = β). The pipeline is perfectly paced.
Setting α = β, i.e., L/(N vgen) = Tsetup + T (full)
exe /N, and
solving for N gives the critical chunk count:
N ∗= L/vgen −T (full)
exe
Tsetup
(17)
which is positive whenever total generation time exceeds total
execution time, the common case for LLM code generation.
For N ≤N ∗additional chunks improve overlap; beyond N ∗
the cumulative setup overhead N Tsetup dominates and latency
degrades.
III. IMPLEMENTATION
Building on the theoretical framework in Section II-B, we
present EAGER, a concrete implementation of parallel execu-
tion for LLM code generation. EAGER instantiates the pipeline
with design choices aimed at minimizing the detection and
per-chunk setup overhead identified in Section II-B, without
affecting execution outcomes.
As illustrated in Figure 2, EAGER consists of a chunker
and an executor. Chunker accumulates the streaming tokens
generated by LLMs in a buffer and identifies complete Python
statements via AST parsing. Detected chunks are dispatched
to a pending queue, from which an executor dequeues, applies
gating and batching optimizations, and delegates execution to
a persistent session. If a runtime error is encountered, the
executor sends an interrupt signal back to terminate the LLM
generation immediately (the dashed path in Figure 2). We
describe each component in detail below.
A. Producer: AST-Based Chunker
The chunker operates on the streaming token output from
an LLM and identifies executable chunks incrementally. We
implement the chunker based on AST statement boundaries.
LLM
x
=
foo
()
\n
bar
Token Stream
Chunker
Collect
Buffer
x = foo()\nbar...
Lookahead disambiguation
Chunk detected
Results
Pending
Queue
Chunk 1
Chunk 2
Chunk 3
Interpreter
Persistent execution session
Dequeue
Interrupt
Error
Batching
Merge queued chunks
Gating
Defer/fall-back chunks
Fig. 2: Architecture of EAGER.
As each token arrives, it is appended to a code buffer, and
the chunker attempts to parse the buffer into a Python AST.
A chunk boundary is recognized when the buffer forms a
complete top-level statement (e.g., assignments, loops, or
function calls). A statement is considered complete when
it can be unambiguously determined that no further tokens
will be generated as part of it, i.e., the statement has no
remaining portions yet to be produced by the LLM. Once a
chunk is confirmed as complete, the corresponding statements
are removed from the buffer and dispatched to the executor,
while any remaining tokens stay in the buffer for subsequent
detection.
In many cases, syntactic completeness directly implies com-
pleteness. For example, upon receiving print("hi") fol-
lowed by a newline, the chunker can immediately confirm this
as a standalone statement and dispatch it. However, in other
cases, a syntactically valid statement may still have remaining
portions to be generated. Consider generating a function where
tokens arrive incrementally. After receiving the first line of the
function body, the parser can already yield syntactically valid
results. Yet the next line could continue the function body
with additional statements, in which case the definition is not
yet complete. To handle such ambiguities, EAGER employs
a lookahead strategy: when a statement parses successfully
but its completeness cannot be definitively confirmed from
syntax alone, the chunker waits for one additional token before
committing. If the next token rules out the possibility of the
current statement continuing (e.g., by beginning a new top-
level statement or indicating a dedent), the chunk is finalized
and dispatched; otherwise, the buffer continues to accumulate.

This mechanism ensures that dispatched chunks are both
syntactically complete and semantically independent.
B. Consumer: Gated Executor with Dynamic Batching
The executor acts as the consumer of the pipeline, receiving
chunks dispatched by the chunker. It interacts with a persistent
execution session, whether a local Python subprocess, a sand-
boxed environment, or a Docker container, that preserves all
imports, variable bindings, and function definitions across suc-
cessive chunk executions. This execution session is therefore
responsible for the execution of the chunks.
Confirmed chunks are placed into a pending queue. When
the executor becomes available, it merges all currently pending
chunks into a single big chunk, rather than executing them
one by one. This dynamic batching naturally adapts to the
pace difference between the chunker and the executor: when
execution is slower than detection, more chunks accumulate
and are batched together, reducing the effective number of ex-
ecutor invocations and thus the cumulative setup cost N Tsetup
in Equation 8. This also makes the speedup condition S ≥1
easier to satisfy, since the overhead term N Tsetup −T (full)
setup in
Equation 9 shrinks accordingly.
On top of batching, the executor applies a gating policy that
classifies each chunk before dispatch. The policy distinguishes
four categories. The first identifies chunks that are unprofitable
to execute eagerly and defers them within the pipeline. The
remaining three identify chunks whose EAGER execution
would be unsafe or would alter program semantics, and fall
back to serial execution for them.
• Low-yield chunks. Chunks whose execution time is negli-
gible compared to the per-invocation setup overhead yield
no useful overlap. Typical examples are function or class
declarations, which produce no observable computation
when executed in isolation. For such chunks, the setup cost
Tsetup dominates the actual execution time Texe,i ≈0,
so dispatching them individually only adds overhead. The
executor therefore defers these chunks: they remain in the
pending queue and are merged with the next non-deferred
chunk, at which point the declarations become available to
support subsequent code that depends on them.
• External-side-effect chunks. EAGER execution changes
when a statement runs relative to generation, not whether
it runs. For most statements this reordering is harmless,
but operations with irreversible, externally observable effects
must not be committed before the surrounding code has been
generated. For chunks invoking process creation, filesys-
tem mutation, network communication, or inter-process
operations (e.g., os, subprocess, shutil, socket,
multiprocessing), EAGER disables overlap and exe-
cutes the program serially, so that their side-effect timing
matches the serial baseline.
• Timing-sensitive chunks. Some statements have semantics
that depend on wall-clock timing or on the surrounding
execution schedule, such as sleeping, timers, clock reads,
signal delivery, and thread creation (e.g., time, signal,
threading). Executing such chunks ahead of generation
would perturb a program’s own timing or concurrency
assumptions, altering its observable behavior. EAGER there-
fore falls back to serial execution for these programs,
keeping such statements in program order and preserving
correctness for code that observes its own timing.
• Dynamic-execution
chunks. Dynamic execution entry
points (eval, exec, compile, __import__) make a
chunk’s behavior undeterminable from its surface syntax,
so the gating policy cannot reason about which of the cate-
gories above it belongs to. Rather than dispatch code whose
effects cannot be statically inspected, EAGER conservatively
falls back to serial execution.
The gate is applied as a static, name-based check over each
chunk’s parsed AST. Its default instance is a conservative
denylist of standard-library modules that commonly carry
external effects, and a deployer can extend this set for a given
workload.
C. Error Handling in the Pipeline
The preceding subsections describe the normal flow of the
pipeline: the chunker detects and dispatches chunks, and the
executor batches and executes them. We now describe how the
pipeline handle

---
title: Towards FPGA Backbone Idea Audit, July 2026
domain: research
area: fpga-llm-inference
type: synthesis
status: active
updated: 2026-07-24
tags: [fpga, llm-inference, llama-cpp, ggml, research-idea, idea-spark, falsification]
---

# Towards FPGA Backbone Idea Audit, July 2026

## Decision

对当前 **Towards a General FPGA Backbone for LLM Inference** 的判断是：

> 当前工作证明了 native GGML integration、strict no-fallback execution 和 evidence closure，但尚未形成可支撑强系统论文的 load-bearing research mechanism。现在不应以 general high-performance FPGA backbone 的主张投稿。

Microsoft ResearchStudio `idea-spark` 完整运行在 Phase 3 终止，没有生成 reviewer-defensible idea card。终止原因不是发现某篇论文直接 scoop 了候选，而是两个连续候选都未同时通过 mechanism coherence、novelty/recipe 和 falsification audit。

运行记录位于：

```text
ideaspark_run/towards-general-fpga-backbone/
```

最终状态见该目录的 `phase_3_failed.md`。

## What Is Already Established

当前证据仍然有明确价值，但价值边界必须写准：

| Established | Not established |
|---|---|
| 原生 `llama.cpp` / GGML FPGA backend | FPGA 相对 CPU/GPU 的 acceleration |
| accepted node 必须 FPGA execute 或 explicit fail | 自动模型编译或 graph lowering |
| Gemma 3 1B F16、U280、11 operator families | 多模型、多精度、多板卡 generality |
| 2,422/2,422 accepted dispatches、zero fallback | coarse-grained region execution |
| 可追踪 artifact identity 和 operator ABI | matched power/energy 或 model quality |
| `pp512` / `tg128` matched CPU-FPGA timing | competitive TTFT、TPOT 或 tokens/s |

当前 FPGA 路径比 matched CPU 慢 `228.5x` prefill 和 `12.54x` decode。`pp512` 的 1,626 个 GGML calls 展开成 224,936 个 XRT launches；`tg128` 的 104,877 个 calls 展开成 202,530 个 launches。这个结果足以证明 granularity mismatch 是首要研究对象，但不能证明任何候选 coarsening mechanism 会改善 downstream wall clock。

## IdeaSpark Bottleneck

Phase 1 给出的核心瓶颈成立：

> Individually valid FPGA admissions can compose into globally pathological execution when framework-visible graph progress is realized as fine-grained launches and waits. The unsolved part is reducing that amplification while preserving support decisions, explicit failure, tensor state, artifact identity, and zero fallback on the unchanged framework path.

因此，仅靠以下内容不足以支撑强系统论文：

- native backend registration；
- strict support contract；
- operator ABI；
- retained dispatch evidence；
- 更多单算子 HLS/RTL replacements。

这些是必要基础，不是当前结果中的性能机制。

## Literature Confidence

自动 Phase 0 检索只召回 10 篇 frontier items，而且多数是 `backend` 词面噪声；不能用它单独判断 novelty。运行另外注入了 DFX、FlightLLM、Spatial LLM、EdgeLLM、StreamTensor、CODO、TeLLMe、FAST-Prefill 和 FlexLLM 等 user anchors，并读取了可获得的公开全文。最终 collision retrieval 返回 98 个 signature/alias hits，没有发现直接 subsume RegionSeal contract 的论文。

这个结果只支持“尚未发现直接 collision”，不支持“已证明 novel”。检索对 execution-provider partitioning、alias-aware fusion、proof-carrying code、transactional accelerator runtime 和 XRT command scheduling 的历史覆盖仍不够完整。只有 mechanism 和 API 稳定后，才值得运行一次 focused scoop check；在此之前扩大检索不能修复候选本身的 falsification 缺陷。

## Attempt 1: Receipt-Carried Epochs

第一个候选尝试用 vector-descriptor operator wrappers、asynchronous graph epochs、tensor versions 和 copy-on-write KV state，把每个 accepted call 的内部 launches 压缩到一次，并把 host wait 推迟到 graph boundary。

该候选被放弃，原因是两个 load-bearing coherence failure：

1. Host-side `start()` 顺序不是 XRT completion dependency。producer fault 时，等待 input version 的 dependent wrapper 可能永远不退出，因此 first-error epoch commit 无法完成。
2. Tensor ID 不等于 canonical storage alias。没有 allocation/range/view relation 时，KV cache 的 copy-on-write versioning 可能读取 stale alias 或永久等待错误的 version。

补齐 device dependency、abort propagation、memory ordering、alias-safe MVCC 和 11 个 vector wrappers，已经不是小修，而是一个超出五个月可信范围的新 runtime subsystem。其 novelty-bearing 部分也容易被评价为 command batching 加 transaction machinery，而非清晰的新机制。

## Attempt 2: RegionSeal

第二个候选收窄为一个同步执行的 pure region：

```text
per-node strict admission
  -> canonical storage-range/effect check
  -> one exact recurring region
  -> one terminating U280 artifact
  -> one synchronous wait
  -> success-only device-residency publication
  -> remaining nodes stay on strict FPGA path
```

它明确排除 KV mutation、in-place writes、external aliases 和 host-visible state，只允许一个 unaliased terminal output。实际 backend source 也提供了可用的 publication point：

- backend commit: `2616bb6b0fabfe2974c00bf3a2d5be292a22e05e`；
- `ggml_fpga_residency_state::mirrors`；
- `ggml_fpga_residency_store` / `ggml_fpga_residency_get_input`；
- `ggml_fpga_wait_for_run` 的 timeout/abort path。

因此，region output 不需要虚构的 GGML tensor/BO rebinding。候选可限制为一个 output 和 same-group downstream consumers，在 successful wait 后发布 graph-local residency mirror；failed run 不发布，unconfirmed abort 则 quarantine run/BO 并禁用 backend，不宣称 reset 后可恢复执行。

### Why RegionSeal Is Still Not A Paper Idea

即使修复可实现性，独立审计仍指出三个问题：

1. **Novelty residue is weak.** Alias/effect analysis、subgraph fusion、delegate admission 和 residency publication 都是已有 building blocks。`digest-bound seal` 很容易被 reviewer 读成 ordinary effect-aware fusion 的 packaging。
2. **Pattern mechanism was initially bypassed.** 为满足 C13，retry 增加了 relation-typed effect graph 和固定点传播生成 `RTECC` certificate，但这仍需证明 certificate 相对 ordinary effect checker 提供了不可替代的安全或执行能力。
3. **Falsification was not executable enough.** Pre-synthesis `C_R` 无法独立测出尚未构建的 region artifact 的真实 launch/wait cost；decomposition-off、RTECC-off 和 ordinary fused-region controls 没有完全正交；30-pair bootstrap 规则也没有完整到可复现地证明 effect lower bound 大于 10%。

因此，RegionSeal 当前只能称为 **candidate engineering hypothesis**，不能称为 selected paper contribution。

## Required Go/No-Go Prototype

下一步不应直接实现完整 fused Transformer block。先做一个 calibrated region shell，用最小成本测出候选是否有足够的 end-to-end headroom。

### Stage A: Find One Eligible Region

从完整 `pp512` 和 `tg128` traces 中寻找长度 2 到 6 的 recurring contiguous region，并要求：

- 所有节点已经通过 strict FPGA support；
- F16 type/shape/stride 精确匹配；
- 无 KV update、in-place mutation 或 externally visible state；
- canonical allocation/range analysis 无 outside alias；
- exactly one terminal output；
- terminal output 的所有 downstream FPGA consumers 使用同一 XRT memory group；
- region occurrences 不重叠，wait/launch attribution 不重复计数。

如果不存在这样的 region，停止 RegionSeal 路线。

### Stage B: Build A Calibrated Shell

在实现完整 arithmetic 前，构建与候选 region 使用相同 BO count、memory group、argument ABI、status record 和 residency publication path 的 terminating shell。至少分别测量：

- seal/RTECC analysis time；
- region `run.start()` host cost；
- region `wait()` host-observed cost；
- device event duration；
- success-only mirror publication cost；
- manifest mismatch 和 failed-status path。

只有真实 shell 才能给出 one-region execution cost。用当前 per-node waits 减去 shell cost得到的只是 calibrated removable-control-time bound，不能用尚未实现的 region latency 猜测它。

### Stage C: Freeze Orthogonal Controls

所有 controls 必须使用同一 R* arithmetic artifact、输入、输出和 board clock：

| Arm | Certificate | Region substitution | Purpose |
|---|---:|---:|---|
| Strict baseline | no | no | 当前 per-node FPGA path |
| Certificate-only | yes | no | 隔离 analysis overhead |
| Ordinary effect-aware region | conventional checker | yes | 判断 RTECC 是否只是 packaging |
| RegionSeal | RTECC | yes | 完整候选 |
| Manifest-disabled | forced mismatch | no | 验证 exact artifact gate |

`RTECC-off` 不能通过换数据集或只挑 safe fixtures 实现，否则 artifact execution 和 admission population 同时改变，无法归因。

### Stage D: Pre-Register The Statistic

在正式 board run 前冻结：

- primary estimand，例如 paired per-run relative reduction
  `d_i = (T_baseline,i - T_region,i) / T_baseline,i`；
- run pairing、warmup、randomized/blocked order 和 board thermal policy；
- sample size，不能无依据固定为 30；
- bootstrap unit、resample count、random seed policy 和 interval type；
- `pp512` / `tg128` multiplicity correction；
- success threshold：adjusted one-sided lower confidence bound `> 0.10`，而不只是 point estimate `> 10%` 或 CI `> 0`；
- correctness、strictness、artifact identity、zero fallback 和 fault tests 均为 hard gate，任何失败都覆盖速度结果。

## Stop Conditions

满足任一条件就停止把 RegionSeal 作为论文主线：

1. 找不到满足 effect closure 和 same-group residency 的 recurring region。
2. Calibrated shell 表明可移除 control time 的保守上界不足以支持 10% full-path gain。
3. Region output 不能通过现有 residency mirror 被所有 downstream consumers 正确消费。
4. F16 outputs、tokens、support trace、artifact identity 或 zero-fallback 出现回归。
5. Ordinary effect-aware fused-region baseline 与 RTECC 在安全拒绝和执行能力上等价，说明 certificate 没有 research delta。
6. Full artifact 只改善 kernel/region event，却不能改善 `pp512` 或 `tg128` downstream wall clock。

## Publication Ladder

| Evidence reached | Defensible output |
|---|---|
| Current integration evidence only | engineering report、artifact/demo、workshop；不宣称 acceleration |
| Calibrated shell only | internal go/no-go result；不构成完整 systems paper |
| One R* passes correctness and >10% lower-bound gate | scoped Gemma 3 1B F16/U280 systems result |
| RTECC beats ordinary effect-aware baseline on a real safety/execution property | possible mechanism contribution |
| Second model and preferably second FPGA family/board | only then reconsider `general FPGA backbone` framing |

如果 RegionSeal 失败，但可以在多个模型、shape 和 backend configuration 上重复证明 admission-to-launch amplification，则可另行考虑一篇窄范围 characterization paper，例如 **The Granularity Gap in Framework-Native FPGA LLM Backends**。该路线也要求新增模型和系统样本，不能由当前单一 Gemma/U280 trace 支撑。

## Current Recommendation

1. 保留当前稿件作为系统与证据基线，不按 strong full-paper claim 投稿。
2. 先实现 calibrated single-output region shell，而不是完整 block compiler 或 persistent runtime。
3. Shell 通过 headroom gate 后，再实现一个 R* arithmetic artifact。
4. 将标题暂时收窄到 Gemma 3 1B F16/U280；在第二模型和第二硬件证据出现前，不使用 `General FPGA Backbone` 作为已证明主张。
5. 完成上述新证据后再重新运行 Idea Spark 和 focused scoop check，检索 `alias-aware graph fusion`、`effect-aware delegate partitioning`、`proof-carrying accelerator regions`、`transactional accelerator output commit` 和 XRT command-graph/runtime work。

## Related Pages

- [[research/fpga-llm-inference/project-status-2026-07]]
- [[research/fpga-llm-inference/end-to-end-evaluation]]
- [[research/fpga-llm-inference/system-landscape]]
- [[research/fpga-llm-inference/codo-2026]]

返回 [[research/fpga-llm-inference/index]]。

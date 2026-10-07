---
title: Mem0 New Algorithm Benchmark Decision
domain: research
area: misc
type: synthesis
status: active
updated: 2026-09-18
tags: [research, agent-memory, mem0, benchmark, locomo, longmemeval]
---
# Mem0 New Algorithm Benchmark Decision

## Update — 2026-09-18

The [2026 source archive](../assets/mem0-2026/index.md) now contains SDK 2.1.0 and the current public evaluation repository. ADD-only extraction and semantic/BM25/entity scoring are implemented publicly; graph memory and the platform temporal parameters remain platform features. The current article/README reports **92.5 / 94.4** on LoCoMo / LongMemEval, while the committed top-200 judgments still total **91.56 / 93.4**. The earlier values below preserve the April snapshot.

The current evaluator uses GPT-5 defaults and a permissive rubric for partial lists and approximate dates. The benchmark's old SDK-branch dependency and search API also need reconciliation before a new run. Sources were inspected and saved labels recounted; no inference was run. The recommendations below are historical planning context, not a completed matched comparison or a selected evaluator.

## Context

Mem0 published a post-paper algorithm update on 2026-04-16: "Introducing The Token-Efficient Memory Algorithm" at <https://mem0.ai/blog/mem0-the-token-efficient-memory-algorithm>.

This matters for local agent-memory research because Mem0 is already a close baseline in the paper library: [[research/agent-memory/assets/mem0-2025/index]]. The 2025 paper version uses two-pass extraction plus `ADD` / `UPDATE` / `DELETE` / `NOOP` memory reconciliation. The 2026 blog describes a materially different system: single-pass ADD-only extraction, agent-generated facts as first-class memories, entity linking, multi-signal retrieval, and keyword normalization.

## Key Judgment

For current agent-memory research, the new Mem0 algorithm should be treated as a **strong related benchmark that needs at least a small controlled evaluation**, not ignored in favor of only the old paper result.

The reason is not just that the reported score is higher. The new algorithm changes the failure modes that local work cares about:

- ADD-only extraction directly targets temporal change, contradiction, and provenance loss.
- Agent-generated fact storage directly targets assistant-memory questions, where old memory systems often miss facts produced by the agent rather than the user.
- Entity linking plus semantic / keyword / entity fusion overlaps with any retrieval-planning or symbolic-retrieval contribution.
- The blog reports large gains on LoCoMo and LongMemEval, which are the same benchmark family used by local agent-memory work.

## What Not To Do

Do not make the project depend entirely on reproducing Mem0's managed-platform numbers. The blog explicitly says the managed platform includes proprietary optimizations not necessarily present in the open-source SDK, so the reported 91.6 LoCoMo and 93.4 LongMemEval numbers should be cited as vendor-reported, not as directly comparable reproduced results.

Do not compare local micro-F1 numbers against Mem0's accuracy / judge numbers without metric normalization. The existing local wiki already warns that accuracy-based SOTA and micro-F1 are not comparable.

## Recommended Evaluation Strategy

Use a two-tier strategy:

1. **Main paper comparison:** keep the old Mem0 paper result in the related-work table because it is citable, archived, and methodologically specified.
2. **Current-system sanity check:** run the new open-source SDK or public evaluation harness on a small but representative slice, especially temporal, multi-hop, knowledge-update, and assistant-fact questions.
3. **Report both separately:** label them as "Mem0 paper baseline" and "Mem0 2026 SDK / blog-era baseline" rather than merging them.
4. **If compute is limited:** evaluate only the slices where the new algorithm claims the largest gains: LoCoMo temporal / multi-hop and LongMemEval temporal / assistant / knowledge-update.
5. **If writing soon:** include a short paragraph saying the post-paper Mem0 algorithm is an important moving baseline, and that any new method should report whether it beats the paper baseline, the current SDK, or both.

## Positioning Implication

If local work is framed as "better agent memory benchmark score," then testing the new Mem0 algorithm is almost mandatory because reviewers can object that the baseline is stale.

If local work is framed as "declarative / symbolic retrieval with no embedding index," then the new Mem0 algorithm is still important, but it becomes an ablation target rather than the central opponent. The paper can argue that Mem0 improves production memory under a compact context budget, while the local contribution studies executable retrieval programs, interpretability, and index-free search.

## WizWand Leaderboard Check 2026-04-26

WizWand's public SOTA pages currently do **not** make the Mem0 2026 blog-era claims look like a settled public baseline:

| Source | Metric shown by page | Mem0 entries observed | Strong visible entries |
|---|---|---|---|
| LoCoMo SOTA | Overall F1 | 64.2, 45.09, 42.4, 41.2, 39.7, 39.0, 36.4, 35.2 | EverMemOS 92.3, Hindsight 89.6, Zep v3 85.2, MemOS v2 80.8 |
| LongMemEval SOTA | Average Score | 66.4, 54.8, 54.62, 32.46 | Chronos High 95.6, Mastra 92.8, Honcho 92.6, Cognis 92.4, Hindsight 91.4 |

Interpretation: use Mem0 as both (1) the old paper baseline and (2) a moving production-system baseline, but do not cite the 2026 blog numbers as if they were the current public leaderboard state. If using WizWand as external evidence, cite the exact metric and page date, because entries are mixed across report papers and configurations.

## Next Steps

- Check whether the new algorithm is actually available in the open-source SDK and whether version pinning exposes it.
- Run a small LoCoMo slice with identical answer model, judge, and metric as the local system.
- Track tokens per query, latency, and retrieved context size, not only answer score.
- Keep the 2025 paper note unchanged as the paper baseline, but add this thread as the benchmark-decision note.

## References / Evidence

- Mem0 2026 blog: <https://mem0.ai/blog/mem0-the-token-efficient-memory-algorithm>
- WizWand LoCoMo SOTA snapshot: <https://www.wizwand.com/sota/long-term-memory-evaluation-on-locomo>
- WizWand LongMemEval SOTA snapshot: <https://www.wizwand.com/sota/long-context-memory-evaluation-on-longmemeval>
- Local paper note: [[research/agent-memory/assets/mem0-2025/index]]
- Related local warning: `wiki/research/log.md` notes that accuracy-based SOTA systems and local micro-F1 results are not directly comparable.

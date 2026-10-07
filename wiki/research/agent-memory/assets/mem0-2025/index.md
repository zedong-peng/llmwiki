---
title: "Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory"
domain: research
area: agent-memory
type: paper
status: active
updated: 2026-09-20
tags: [paper, misc, mem0, long-term-memory, conversational-memory, graph-memory]
---

# Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory

## Paper Meta
- Title: Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory
- Authors: Prateek Chhikara, Dev Khant, Saket Aryan, Taranjeet Singh, Deshraj Yadav
- Year: 2025
- Venue: not reported
- Topic: agent-memory
- Paper Slug: mem0-2025
- arXiv: https://arxiv.org/abs/2504.19413
- PDF: 2504.19413-mem0.pdf
- Code / project page: https://mem0.ai/research
- Reading Source: TeX only, no PDF fallback
- Official paper experiment code: [historical evaluation directory](repo/mem0/evaluation/) in `mem0ai/mem0`, pinned to `693e709389526b45cfadfd06d89a0e13af7c7345`. Its README explicitly identifies the 2025 paper. This later repository snapshot is not evidence of the exact revision used for the published runs.
- Legacy [memory-benchmarks cache](repo/memory-benchmarks/) belongs to the later evaluation lineage, documented under [Mem0 2026](../mem0-2026/index.md). Its existing location is retained for provenance; it is not the 2025 paper evaluator.

The [2026 algorithm and source archive](../mem0-2026/index.md) covers the later ADD-only/hybrid-retrieval release, SDK 2.1.0, changed evaluator, and the mismatch between current headline scores and committed result files. The results below remain the **2025 paper's reported results**.

## Citation identity and public RAG code

Use **Mem0 2025** for this paper and its reported results. Cite [arXiv:2504.19413](https://arxiv.org/abs/2504.19413); when describing the implementation, additionally cite the [pinned official experiment directory](https://github.com/mem0ai/mem0/tree/693e709389526b45cfadfd06d89a0e13af7c7345/evaluation). Reusable entries are in [citations.bib](citations.bib).

The official [README](repo/mem0/evaluation/README.md) identifies the paper and documents RAG. [src/rag.py](repo/mem0/evaluation/src/rag.py) implements timestamp-and-speaker text serialization, non-overlapping token chunks, embedding-based cosine retrieval, top-k concatenation, and short-answer generation. [run_experiments.py](repo/mem0/evaluation/run_experiments.py) exposes `--chunk_size` and `--num_chunks`; [the historical judge](repo/mem0/evaluation/metrics/llm_judge.py) is separate from the 2026 judge.

The paper's [experimental setup](paper-tex/extracted/legacy/sections/experiment_setup.tex) sweeps chunk sizes 128–8192 and k=1,2. Its [results](paper-tex/extracted/legacy/sections/result.tex) report the best RAG configuration as 256 tokens, k=2, Judge 60.97 ± 0.20%. The documented embedding API name is `text-embedding-3-small` (the paper spells it `text-embedding-small-3`).

```bash
python run_experiments.py --technique_type rag --chunk_size 256 --num_chunks 2
```

This is a documented invocation, not a run performed during this update. It requires dependencies, model credentials, and the expected `dataset/locomo10_rag.json` input. Changing the answer model or prompts yields a controlled rerun of this implementation, not verification of the original paper's numerical results.

## TL;DR
- Mem0 stores compact natural-language memories from dialogue turns and updates them with LLM-guided add, update, delete, and no-op operations.
- Mem0P extends the base system with graph memory, representing memories as directed labeled graphs for stronger relational and temporal reasoning.
- On LOCOMO, Mem0 is strongest on single-hop and multi-hop questions, while Mem0P is strongest on temporal questions and is close to the best open-domain result.
- The main trade-off is efficiency versus structure: Mem0 is faster and smaller, while Mem0P adds graph overhead but improves relational modeling.

## Problem
- Fixed context windows make long-horizon, multi-session conversations brittle.
- Without persistent memory, agents forget user preferences, repeat questions, and contradict prior facts.
- Long contexts do not solve the retrieval problem by themselves because relevant facts can be buried in many irrelevant tokens.

## Method

### Mem0
- Mem0 processes a message pair `(m_{t-1}, m_t)` and uses two context sources for extraction: a conversation summary `S` and a recent-message window of `m = 10` prior messages.
- An LLM (`GPT-4o-mini`) extracts salient candidate memories from this prompt and the system stores them in a vector database.
- The update phase retrieves the top `s = 10` semantically similar memories and lets the LLM choose one of four operations: `ADD`, `UPDATE`, `DELETE`, or `NOOP`.
- The update logic is meant to preserve consistency and avoid duplicate or contradictory memories without training a separate classifier.

### Mem0P
- Mem0P stores memories as a directed labeled graph `G = (V, E, L)` with entities as nodes, relations as edges, and labels as semantic types.
- Extraction is two-stage: an entity extractor identifies entities, and a relationship generator emits triplets such as `(v_s, r, v_d)`.
- New information is matched against existing nodes using embedding similarity; conflicts are resolved by an LLM-based update resolver that can mark relationships obsolete instead of deleting them.
- Retrieval has two modes: entity-centric graph expansion from anchor entities, and semantic triplet retrieval over embedded relation text.
- The implementation uses Neo4j as the graph database and `GPT-4o-mini` with function calling.

## Benchmarks / Datasets

### Dataset
- LOCOMO is the main benchmark.
- It contains 10 extended conversations, each with about 600 dialogues and about 26,000 tokens on average.
- Each conversation has about 200 questions with ground-truth answers.
- Question types used in the paper: single-hop, multi-hop, open-domain, and temporal.
- The adversarial category was excluded because ground-truth answers were unavailable.

### Metrics
- Quality metrics: F1, BLEU-1, and LLM-as-a-Judge.
- Deployment metrics: token consumption, search latency, and total latency.
- Judge scores were run 10 times per method and reported as mean plus/minus one standard deviation.
- Token counts were measured with `cl100k_base`.

## Baselines
- Established LOCOMO baselines: LoCoMo, ReadAgent, MemoryBank, MemGPT, and A-Mem.
- Open-source memory baseline: LangMem.
- Retrieval baseline: RAG with chunk sizes 128, 256, 512, 1024, 2048, 4096, and 8192 tokens, with `k = 1` or `2`.
- Full-context baseline: the entire conversation history in the prompt.
- Proprietary / platform baselines: OpenAI memory and Zep.

## Main Results

### Task Performance

| Question type | Best method in paper | Key result | What it means |
|---|---|---:|---|
| Single-hop | Mem0 | F1 38.72, BLEU-1 27.13, Judge 67.13 ± 0.65 | Dense textual memories are enough for direct factual recall. |
| Multi-hop | Mem0 | F1 28.64, Judge 51.15 ± 0.31 | Compact textual memory works well when facts are split across sessions. |
| Open-domain | Zep, with Mem0P close behind | Zep Judge 76.60 ± 0.13; Mem0P Judge 75.71 ± 0.21 | Structured memory helps, but Zep retains a narrow lead here. |
| Temporal | Mem0P | F1 51.55, Judge 58.13 ± 0.44 | Graph structure is most useful when order and event linkage matter. |

### Result Notes
- Mem0 is the strongest overall choice for single-hop and multi-hop questions.
- Mem0P does not improve single-hop or multi-hop over Mem0, so the graph layer is not universally beneficial.
- OpenAI memory is competitive on some categories but performs poorly on temporal questions because many generated memories miss timestamps.
- Zep is the strongest open-domain baseline and is also competitive on overall Judge score.

## Ablations / Analysis
### Efficiency and Overhead

| System | Memory / context size | Search p50 | Search p95 | Total p50 | Total p95 | Overall Judge |
|---|---:|---:|---:|---:|---:|---:|
| Mem0 | 1,764 tokens | 0.148 s | 0.200 s | 0.708 s | 1.440 s | 66.88 ± 0.15 |
| Mem0P | 3,616 tokens | 0.476 s | 0.657 s | 1.091 s | 2.590 s | 68.44 ± 0.17 |
| Best RAG variant | 256-token chunks, k = 2 | 0.255 s | 0.699 s | 0.802 s | 1.907 s | 60.97 ± 0.20 |
| Full context | 26,031 tokens | not reported | not reported | 9.870 s | 17.117 s | 72.90 ± 0.19 |
| Zep | 3,911 tokens | 0.513 s | 0.778 s | 1.292 s | 2.926 s | 65.99 ± 0.16 |

- Mem0 has the lowest search and total latency among the reported methods.
- Mem0P roughly doubles memory footprint versus Mem0 but remains much smaller than Zep’s reported graph footprint of more than 600k tokens.
- Full-context gives the best Judge score overall, but the p95 latency is an order of magnitude worse than the memory-based systems.
- The paper positions Mem0 and Mem0P as a practical trade-off between quality and deployability.

## Implementation Clues
- `GPT-4o-mini` is the core inference model throughout the paper.
- `text-embedding-small-3` is used for similarity search and RAG baselines.
- The Mem0 pipeline uses asynchronous summary refreshes so extraction can use a current conversation summary without blocking the main path.
- The RAG setup uses fixed chunk sizes from 128 to 8192 tokens and retrieves `k = 1` or `2` chunks.
- The OpenAI memory baseline was evaluated with privileged access to the full memory set for each conversation, because the paper did not have selective memory-retrieval API access.
- Mem0 graph construction is reported to complete in under a minute even in worst cases.

## Limitations
- Graph memory is not uniformly better; it helps most on temporal tasks and can be slower than the dense-memory variant.
- Open-domain performance is still slightly better for Zep.
- This note's paper results were read from TeX. Official repositories are now cached, but later SDK and evaluator changes do not establish reproduction of the 2025 experiments.

## Takeaways
- Mem0 is the more efficient default architecture when the goal is fast, compact long-term conversational memory.
- Mem0P is the better choice when explicit relational structure and temporal reasoning are important.
- The paper’s core message is that selective memory beats raw context extension for production agents.

## Open Questions
- How much of the gains transfer to datasets beyond LOCOMO?
- Can the graph layer in Mem0P be simplified without losing temporal gains?
- Could memory consolidation be made less asynchronous while keeping retrieval quality high?

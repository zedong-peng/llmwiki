---
title: "MemOS: A Memory OS for AI System"
domain: research
area: agent-memory
type: paper
status: processed
updated: 2026-04-25
tags: [paper, agent-memory, long-term-memory, memory-system, kv-cache, parameter-memory, personalization, memos]
---
# MemOS: A Memory OS for AI System

## Paper Meta
- Title: MemOS: A Memory OS for AI System
- Authors: Zhiyu Li, Chenyang Xi, Chunyu Li, Ding Chen, Boyu Chen, Shichao Song, Simin Niu, Hanyu Wang, Jiawei Yang, Chen Tang, Qingchen Yu, Jihao Zhao, Yezhaohui Wang, Peng Liu, Zehao Lin, Pengyuan Wang, Jiahao Huo, Tianyi Chen, Kai Chen, Kehang Li, Zhen Tao, Huayi Lai, Hao Wu, Bo Tang, Zhengren Wang, Zhaoxin Fan, Ningyu Zhang, Linfeng Zhang, Junchi Yan, Mingchuan Yang, Tong Xu, Wei Xu, Huajun Chen, Haofen Wang, Hongkang Yang, Wentao Zhang, Zhi-Qin John Xu, Siheng Chen, Feiyu Xiong
- Affiliation: MemTensor (Shanghai) Technology Co., Ltd.; Institute for Advanced Algorithms Research, Shanghai; Research Institute of China Telecom; Tongji University; Zhejiang University; USTC; Peking University; Renmin University of China; Beihang University; Shanghai Jiao Tong University
- Year: 2025 (arXiv July 2025)
- Venue: arXiv preprint
- Topic: agent-memory
- Paper Slug: memos-2026
- arXiv: https://arxiv.org/abs/2507.03724
- PDF: `2507.03724.pdf`
- Code Repo: https://github.com/MemTensor/MemOS
- Project Website: https://memos.openmem.net/
- Reading Source: TeX source under `source/extracted/`

## TL;DR
- MemOS proposes treating memory as a first-class, schedulable OS-level resource for LLMs, unifying three memory types—plaintext, activation (KV-cache), and parameter memory—under a single framework.
- The core abstraction is the **MemCube**, a standardized unit encapsulating memory content plus rich metadata (provenance, lifecycle state, access control, behavioral indicators).
- A three-layer architecture (Interface → Operation → Infrastructure) orchestrates memory through modules: MemReader, MemScheduler, MemOperator, MemLifecycle, MemGovernance, MemVault, MemStore.
- MemOS achieves state-of-the-art on LoCoMo, LongMemEval, PreFEval, and PersonaMem benchmarks, and demonstrates up to 91.4% TTFT reduction via KV-based memory injection.

## Problem
- LLMs rely on static parameter memory and short-lived context windows; they cannot maintain behavioral continuity, track user preferences, or update knowledge across sessions.
- RAG is a stateless workaround: it lacks lifecycle control, versioning, provenance, and permission-aware scheduling.
- No existing system treats memory as a manageable, schedulable resource with full lifecycle governance—analogous to how an OS manages CPU, RAM, and storage.
- Four concrete failure modes: (1) long-range dependency loss, (2) inability to track knowledge evolution, (3) no durable personalization across sessions, (4) memory silos preventing cross-platform migration.

## Memory Taxonomy
MemOS defines memory along two axes:

**By form:**
| Type | Description | Characteristics |
|---|---|---|
| Plaintext Memory | Retrieved passages, structured graphs, prompt templates injected at inference time | Editable, traceable, rapidly updatable; bypasses context window limits |
| Activation Memory | KV-cache and hidden states generated during inference | Short-term, dynamic, implicit; enables low-latency reuse of stable context |
| Parameter Memory | Knowledge encoded in model weights (FFN matrices, attention K/V matrices) | Long-term, high expressivity; high update cost, poor interpretability |

**By duration:** sensory (subsumed into short-term), short-term, long-term.

Cross-type transitions are a key design goal: plaintext → activation (hot content pre-cached as KV), plaintext/activation → parameter (distillation into capability modules), parameter → plaintext (cold/outdated weights offloaded).

## MemCube: Core Resource Unit
Each MemCube = **Memory Payload** + **Metadata**.

Metadata is grouped into three categories:
- **Descriptive Identifiers**: Timestamp, Origin Signature (inference extraction / user input / external retrieval / fine-tuning), Semantic Type (task prompt / fact / user preference)
- **Governance Attributes**: Access Control (read/write/share scope), Lifespan Policy (TTL or decay), Priority Level, Compliance & Traceability (sensitivity tags, watermarks, audit logs)
- **Behavioral Usage Indicators**: Access frequency/recency (hot vs. cold), Contextual Fingerprint (lightweight semantic signature for fast retrieval), Version Chain (modification history and derivation lineage)

Behavioral indicators drive **Policy-Aware Scheduling**: the system dynamically adjusts a memory block's tier and format based on usage, enabling layered memory evolution.

## Architecture: Three Layers

### Interface Layer
- **MemReader**: Parses natural language into structured `MemoryCall` objects (task intent, time scope, entity focus, memory type, contextual anchors). Handles coreference resolution and multi-turn slot filling.
- **Memory API**: Standardized suite—Provenance API (metadata embedding), Update API (version-aware append/merge/overwrite), LogQuery API (structured access to audit logs). All calls use MemCube as parameter carrier.
- **Memory Pipeline**: Declarative DSL or programmatic composition of memory operation chains (retrieve → augment → update → archive), with transactional consistency and rollback.

### Operation Layer
- **MemOperator**: Structures memory via tagging, knowledge-graph linking, and semantic layering (private / shared / global). Supports hybrid retrieval (symbolic rule-based + semantic embedding). Implements task-aligned routing via topic–concept–fact decomposition and `MemoryPathResolver`.
- **MemScheduler**: Central dispatcher. Selects memory type based on task semantics, window size, and resource constraints. Manages cross-type migration (e.g., hot plaintext → KV cache; stable templates → parameter modules; cold KV → plaintext archive). All decisions logged to MemCube.
- **MemLifecycle**: Finite state machine over five states: Generated → Activated → Merged → Archived → (Expired). Supports "Time Machine" (snapshot + rollback) and "Frozen" state for immutable critical memories.

### Infrastructure Layer
- **MemGovernance**: Ternary permission model (user identity × memory object × calling context). TTL enforcement, access-frequency-based GC, sensitive content detection, redaction, watermarking, audit export.
- **MemVault**: Central storage with namespaced repositories (user-private, expert knowledge, shared pipelines, contextual pools). Interfaces with vector stores, relational DBs, and blob storage via `MemoryAdapter`. Coordinates with MemScheduler for hot/cold tiering.
- **MemLoader / MemDumper**: Bi-directional cross-platform migration with provenance auto-fill and governance validation.
- **MemStore**: Publish-subscribe memory exchange across models, institutions, and networks. Supports push/pull, tag/semantic subscriptions, licensed access with contract-bound expiry.

## Evaluation

### Benchmarks
| Benchmark | What it tests |
|---|---|
| LoCoMo | Long-term multi-session dialogue QA (single-hop, multi-hop, temporal reasoning, open-domain) |
| LongMemEval | Long-term memory abilities (information extraction, multi-session reasoning, knowledge updates, temporal reasoning) |
| PreFEval | Personalized response rate (0-turn and 10-turn irrelevant context settings) |
| PersonaMem | Dynamic user profile and preference understanding (precision) |

### Baselines
MIRIX (6-component specialized memory), Mem0 (slot-based + top-k semantic search), Zep (time-aware knowledge graphs), Memobase (performance/cost/latency balance), Supermemory (Dynamic Knowledge Graph), MemU (multi-modal extraction + structured memory files). All run on GPT-4o-mini backbone.

### Main Results
| Benchmark | MemOS result | Key finding |
|---|---|---|
| LoCoMo | Best average across all sub-tasks | First or second in every category; strong on single-hop and multi-hop |
| LongMemEval | Best average across almost all sub-tasks | First or second in every category except knowledge updates |
| PreFEval | Best Personalized Response in both 0-turn and 10-turn settings | Lowest preference-unaware error; acceptable context length |
| PersonaMem | Best precision | Validates dynamic user profile handling |

### KV-Based Memory Acceleration
- Compared prompt-based injection vs. KV-cache injection across 3 context lengths × 3 query lengths on Qwen2.5-7B/72B and other models.
- KV injection yields identical outputs with substantially lower TTFT.
- Qwen2.5-72B: **91.4% TTFT reduction** under long-context, short-query conditions.
- MemOS achieves 100% success rate and lowest latency at up to 100 QPS (vs. Mem0, Memobase, Supermemory, MemU, Zep).

### Ablation: Chunk Size and Top-K
- Performance steadily improves as memory capacity (chunk size × Top-K) increases, especially for multi-hop and temporal reasoning.
- F1, ROUGE-L, BLEU all benefit from memory expansion. Cosine similarity remains stable throughout.

## Application Scenarios
1. **Multi-turn dialogue and cross-task continuity**: MemLink encodes salient elements per turn into structured conversation memory units; MemScheduler retrieves relevant history to prevent context drift.
2. **Knowledge evolution and continuous update**: Memory units have independent lifecycles; trusted new versions are prioritized at inference; obsolete entries archived without retraining.
3. **Personalization and multi-role modeling**: Per-user memory spaces; multiple roles (e.g., "parent" vs. "manager") coexist with separate memory streams; long-term interaction patterns encoded into personal memory units.
4. **Cross-platform memory migration**: Standardized portable MemCube format with encryption; breaks "memory silos" across mobile, cloud, and enterprise.

## Architectural Innovations
- **Memory-as-a-Service (Paid Memory)**: Domain experts publish structured memory via MemStore; consumers install via standardized loading interface with permission control and optional micropayment licensing.
- **Painless Memory Management**: Task-level Memory API abstracts away vector indexing, KV-caching, and context orchestration; hot-swapping and cache eviction are automatic.
- **Mem-training Paradigm**: Proposes continuous knowledge accumulation via explicit controllable memory units at runtime, extending beyond pretraining/fine-tuning to a society-scale distributed intelligence ecosystem.

## Future Directions
- **Cross-LLM Memory Sharing**: Memory Interchange Protocol (MIP) for standard formats, compatibility rules, and trust mechanisms across models and apps.
- **Self-Evolving MemBlocks**: Memory units that self-optimize and reconstruct based on usage feedback.
- **Scalable Memory Marketplace**: Decentralized mechanisms for memory exchange, asset-level transactions, and distributed evolution.

## Takeaways
- The OS analogy is productive and well-executed: MemOS maps classical OS components (CPU scheduler, virtual memory, filesystem, ACL) onto LLM memory management with concrete module designs.
- MemCube's three-part metadata (descriptive / governance / behavioral) is the key design that enables both governance and adaptive scheduling from a single abstraction.
- KV-based activation memory is underexplored in prior work; MemOS's controlled experiment showing 91% TTFT reduction is a strong practical result.
- The system is positioned as infrastructure for a future "memory marketplace" paradigm, not just a better RAG pipeline.

## Open Questions
- How does MemOS handle semantic drift when plaintext memory is promoted to KV or parameter form—can the compressed representation stay faithful over long horizons?
- The Memory Interchange Protocol (MIP) is mentioned as future work; what are the trust and alignment challenges when sharing parameter-level memory across heterogeneous models?
- Benchmarks (LoCoMo, LongMemEval) are static archives; how does the system behave in live, continuously evolving interaction streams?
- What are the failure modes of MemGovernance under adversarial memory injection or prompt injection attacks?

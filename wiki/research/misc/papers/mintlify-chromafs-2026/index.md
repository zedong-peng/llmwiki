---
title: How We Built a Virtual Filesystem for Our Assistant
domain: research
area: misc
type: paper
status: processed
updated: 2026-04-19
tags: [paper, misc, blog, systems, retrieval, filesystem, chroma]
---

# How We Built a Virtual Filesystem for Our Assistant

## Paper Meta
- Title: How We Built a Virtual Filesystem for Our Assistant
- Author: Dens Sumesh
- Date: March 24, 2026
- Venue: Mintlify Engineering blog
- Topic: misc
- Paper Slug: mintlify-chromafs-2026
- Canonical URL: https://www.mintlify.com/blog/how-we-built-a-virtual-filesystem-for-our-assistant
- Reading Source: official Mintlify blog post
- TeX/source: unavailable
- PDF fallback: not used

## TL;DR
- Mintlify replaced sandboxed document assistants with ChromaFs, a virtual filesystem layered on top of its existing Chroma-backed docs index.
- The assistant can navigate documentation with `grep`, `cat`, `ls`, `find`, and `cd`, which makes the interaction model closer to a codebase than to chunk-based RAG.
- The main operational win is latency and cost: session creation drops from about 46 seconds to about 100 milliseconds, and marginal per-conversation compute cost drops to zero.
- The system also preserves access control, read-only behavior, and cached reconstruction of full pages from embedded chunks.

## Problem
- The existing assistant could only retrieve chunks that matched a query, so it failed when answers were distributed across multiple pages or required exact syntax that did not land in the top-k results.
- Spinning up a real sandbox with a cloned repo would technically give the agent a filesystem, but the article says that approach was too slow for a user-facing assistant and too expensive at scale.
- The design goal was to let the assistant explore docs the way a developer explores a codebase, rather than forcing it to depend on single-shot retrieval.

## Method
- ChromaFs intercepts UNIX-style commands through `just-bash`, a TypeScript bash reimplementation that already knows how to parse `grep`, `cat`, `ls`, `find`, and `cd`.
- The documentation tree is stored as a gzipped JSON blob named `__path_tree__` inside the Chroma collection, then decompressed on startup into an in-memory `Set` of paths and a `Map` of directory children.
- Access control is enforced before tree construction by pruning slugs with the current user's session token, so inaccessible files never appear in the virtual filesystem.
- `cat` rebuilds pages by fetching all chunks for a page slug, sorting them by `chunk_index`, and joining them into a full document.
- Large documents can be represented as lazy file pointers, and write operations are rejected with `EROFS`, so the assistant can explore without mutating the docs corpus.
- `grep -r` is optimized as a two-stage pipeline: parse the request, translate it into a Chroma query, prefetch matching chunks into Redis, then run the final filter in memory.

## Benchmarks / Datasets
| Dataset / Benchmark | Task | Metric | Notes |
|---|---|---|---|
| Mintlify docs assistant | documentation navigation and QA | not reported | Production system, not a public academic benchmark |
| Sandbox baseline | session boot / filesystem access | p90 boot time | Reported as about 46 seconds including clone and setup |
| ChromaFs deployment | session boot / filesystem access | p90 boot time | Reported as about 100 milliseconds |

## Baselines
| Baseline | Type | Why Important | Notes |
|---|---|---|---|
| Full sandbox / micro-VM | system baseline | The obvious way to give an agent a filesystem | Too slow and too expensive for a front-end assistant |
| Chunk-only RAG | retrieval baseline | The prior behavior that the article says was insufficient | Breaks when answers span pages or require exact syntax |
| Naive networked grep | implementation baseline | The behavior ChromaFs avoids by reusing index metadata | Recursive search would otherwise be too slow over the network |

## Main Results
| Dataset / Benchmark | Metric | Baseline | Ours | Gain / Delta | Notes |
|---|---|---|---|---|---|
| Session creation | p90 boot time | about 46 s | about 100 ms | about 460x faster | The baseline includes GitHub clone and setup; the gain is inferred from the reported numbers |
| Per-conversation compute | marginal cost | about $0.0137 | about $0 | savings to zero | ChromaFs reuses the existing DB infrastructure |
| Annual infra estimate | compute cost at 850k conversations/month | north of $70k/year | not reported | not reported | Based on Daytona pricing and a minimal sandbox setup |
| Production usage | daily conversation volume | not reported | 30,000+ conversations/day | not reported | Described as the deployed docs assistant scale |

## Ablations / Analysis
- The article does not report a formal ablation study or accuracy benchmark suite.
- The strongest causal claim is architectural: reusing the existing Chroma index removes the sandbox bottleneck and avoids paying for fresh compute per session.
- The grep pipeline shows the main systems idea clearly: coarse candidate filtering in Chroma, then fine-grained in-memory filtering after prefetch.

## Implementation Clues
- `just-bash` is the shell interpreter layer; ChromaFs only has to provide the filesystem backend.
- `__path_tree__` is the bootstrap artifact that makes `ls`, `cd`, and `find` work without network calls after initialization.
- Access control is implemented by filtering the path tree up front, rather than by emulating Linux permissions inside a container.
- Redis is used as a cache for prefetched chunks matched during recursive grep workflows.
- The system is intentionally read-only, which simplifies isolation and prevents one agent from corrupting another agent's view.

## Limitations
- No public task-level accuracy metric is reported, so the article is primarily a systems post rather than an evaluation paper.
- The performance numbers are production-internal and depend on Mintlify's own documentation corpus, Chroma index, and cache layout.
- The approach assumes that the content is already indexed and structured as files and chunks; it is not a universal replacement for every retrieval workload.

## Takeaways
- Filesystem semantics are a strong interaction model for docs assistants when the corpus is already indexed and users need exact navigation.
- Reusing an existing vector store as the backing store for a virtual filesystem can shift the bottleneck from infrastructure to query translation.
- The article is a concrete production precursor to symbolic and filesystem-style retrieval ideas in the wiki's broader LLM retrieval notes.

## Open Questions
- How well would ChromaFs scale to much larger or more heterogeneous documentation trees?
- What answer-quality tradeoffs, if any, appear when filesystem semantics are approximated over a vector store?
- How much of the reported speedup comes from the architectural shift versus caching and pre-indexing?

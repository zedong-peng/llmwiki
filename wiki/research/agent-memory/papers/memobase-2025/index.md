---
title: "Memobase"
domain: research
area: misc
type: source
status: processed
updated: 2026-04-19
tags: [source, agent-memory, infrastructure, memobase, product]
---
# Memobase

## Source Meta
- Title: Memobase
- Author / Maintainer: memodb-io
- Year: 2025 snapshot
- Venue: official repository and product docs
- Topic: misc
- Source Slug: memobase-2025
- Repo: https://github.com/memodb-io/memobase
- Docs: https://docs.memobase.io
- Reading Source: official repo and docs; no paper or TeX source identified
- Repo Read: yes (`repo/memobase/readme.md`)
- PDF Fallback: not used

## TL;DR
- Memobase is a production-oriented memory system for personalized agents, not a research paper.
- Its main conceptual framing is user-profile memory plus an event timeline, with asynchronous processing over buffered interactions.
- The repo presents Memobase as a low-latency product stack with SDK, API, and MCP integration rather than a benchmark paper.

## What It Is
- Memobase stores and updates user memory in at least two forms:
  - profile-like structured memory
  - event / timeline memory
- The system emphasizes a background processing pipeline that converts interaction traces into durable memory representations.
- This is a product architecture choice: keep online latency low while maintaining richer memory than a flat chat history.

## Implementation Clues
- `repo/memobase/readme.md` describes the API and deployment model.
- The stack uses FastAPI, Postgres, and Redis, with SDK, API, and MCP-facing integration points.
- For the current wiki, Memobase is a valuable engineering comparison target for explicit memory products, especially against [[openai-memory-2024]] and [[hindsight-2025]].

## Why This Is Not A Paper
- I did not identify a canonical paper, TeX source, or conference venue in the official materials.
- The authoritative sources are the repo and docs.
- It should therefore be treated as a `source` note instead of a paper note.

## Takeaways
- Memobase is relevant because it makes concrete product decisions about what memory objects exist and when they are updated.
- It is useful for architecture comparison even without a benchmark paper, especially around profile memory, timeline memory, and asynchronous consolidation.

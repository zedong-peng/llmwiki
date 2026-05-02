---
title: "Honcho"
domain: research
area: misc
type: source
status: processed
updated: 2026-04-19
tags: [source, agent-memory, infrastructure, honcho, product]
---
# Honcho

## Source Meta
- Title: Honcho
- Author / Maintainer: Plastic Labs
- Year: 2025 snapshot
- Venue: official repository and product docs
- Topic: misc
- Source Slug: honcho-2025
- Repo: https://github.com/plastic-labs/honcho
- Docs: https://docs.honcho.dev
- Reading Source: official repo and docs; no paper or TeX source identified
- Repo Read: yes (`repo/honcho/README.md`)
- PDF Fallback: not used

## TL;DR
- Honcho is an open-source memory layer and managed-service stack for stateful agents, not a research paper.
- The system centers on agent memory operations such as storing conversations, building context, searching prior interactions, and maintaining peer or workspace-level state.
- Architecturally it looks like product infrastructure: FastAPI service, Postgres, and `pgvector`.

## What It Is
- Honcho exposes a developer-facing memory backend for agent applications.
- The repo surfaces abstractions around:
  - workspace
  - peers
  - sessions
  - messages
  - context
  - search
  - representation
  - chat
- The framing is operational and API-driven rather than benchmark-driven.

## Implementation Clues
- `repo/honcho/README.md` describes the deployment model and API surface.
- The stack uses FastAPI plus Postgres / `pgvector`, which makes it easy to compare against other memory-system products built around vector search plus structured state.
- This looks like a useful engineering reference if I want an opinionated memory backend for agents rather than a novel algorithm.

## Why This Is Not A Paper
- No arXiv paper, TeX source, or conference publication was identified from the official materials.
- The authoritative source is the public repository plus product documentation.
- It should therefore be stored in the wiki as a `source` note rather than a `paper` note.

## Takeaways
- Honcho is relevant as industry memory infrastructure, especially for API and storage design comparisons.
- It belongs in the memory-systems map alongside product or repo-backed systems such as [[openai-memory-2024]] and [[claude-mem-2026]], but it should not be confused with a peer-reviewed paper.

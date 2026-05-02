---
title: Claude-Mem
domain: research
area: misc
type: engineering
status: processed
updated: 2026-04-19
tags: [research, misc, repo, claude-code, plugin, memory, sqlite, chroma, coding-agents]
---

# Claude-Mem

## Source Meta
- Title: Claude-Mem
- Author: Alex Newman (`thedotmack`)
- Year: 2026
- Venue: GitHub repository
- Topic: misc
- Paper Slug: claude-mem-2026
- Canonical URL: https://github.com/thedotmack/claude-mem
- Reading Source: official GitHub repo
- TeX/source: unavailable
- PDF fallback: not used

## TL;DR
- Claude-Mem is an external persistent-memory plugin for Claude Code, not Claude Code's built-in memory system.
- It captures coding-session activity through lifecycle hooks, stores sessions / observations / summaries in SQLite, and adds semantic retrieval through Chroma.
- The repo wraps retrieval in a token-efficient workflow: search a compact index first, then expand only the small subset worth reading in detail.
- Operationally it behaves more like a sidecar memory service than an in-agent file-memory subsystem: local worker, local database, local web viewer, plugin hooks, and MCP search tools.

## Problem
- Claude Code sessions end, reconnect, and compact, so useful project history can disappear between working sessions.
- A practical coding-memory layer needs to preserve context automatically rather than relying on manual note-taking.
- It also needs search and selective reinjection, otherwise persistent memory just becomes another noisy transcript dump.

## Method

### System Shape
- Claude-Mem installs as a plugin and hooks into Claude Code's session lifecycle rather than modifying Claude Code's internal memory implementation.
- The repo describes a sidecar architecture with hook scripts, a worker service, a local database, local vector search, and user-facing search skills.
- Installation is designed to be one-command via `npx claude-mem install` or via the Claude Code plugin marketplace.

### Capture Path
- The repository describes 5 lifecycle stages: `SessionStart`, `UserPromptSubmit`, `PostToolUse`, `Stop`, and `SessionEnd`.
- Hook logic is implemented in `src/hooks/*.ts` and built into `plugin/scripts/*-hook.js`.
- The goal is to automatically capture observations from coding activity and summarize them into reusable memory without requiring manual user action.

### Storage And Retrieval
- The worker service runs as an Express API on port `37777` and handles asynchronous AI processing.
- Persistent structured data is stored in SQLite under `~/.claude-mem/claude-mem.db`.
- Semantic retrieval uses Chroma under `~/.claude-mem/chroma/`, so the system is not limited to exact keyword matching.
- The repo README describes the search stack as hybrid semantic plus keyword search.

### Search Workflow
- Claude-Mem exposes memory search through MCP tools and a `mem-search` skill.
- The documented workflow is explicitly progressive:
  1. `search` returns a compact index with IDs.
  2. `timeline` adds chronological neighborhood around a result or query.
  3. `get_observations` fetches full details only for filtered IDs.
- The README frames this as a token-efficiency tactic and claims about 10x token savings by filtering before fetching full details.

### Privacy And Control
- The repo supports `<private>...</private>` tags so users can mark content that should not be stored.
- The `CLAUDE.md` page says tag stripping happens at the hook layer before data reaches the worker or database.
- Settings are managed in `~/.claude-mem/settings.json`, covering model choice, port, data directory, log level, and context-injection behavior.

## Repo Structure Notes
| Path | Role |
|---|---|
| `src/hooks/` | lifecycle hook implementations |
| `src/services/worker-service.ts` | local worker / HTTP API |
| `src/services/sqlite/` | persistent storage layer |
| `src/services/sync/ChromaSync.ts` | vector sync and semantic retrieval |
| `plugin/skills/mem-search/` | memory search skill |
| `src/ui/viewer/` | local web viewer UI |
| `docs/` | architecture and usage docs |

## Concrete Technical Signals
- Worker service port: `37777`
- SQLite path: `~/.claude-mem/claude-mem.db`
- Chroma path: `~/.claude-mem/chroma/`
- Search interface: `search`, `timeline`, `get_observations`
- Viewer URL: `http://localhost:37777`
- Install path for plugin artifacts: `~/.claude/plugins/marketplaces/thedotmack/`

## Design Tradeoffs
- Compared with Claude Code's built-in file-based memory notes in [[research/claude-code-memory/overview]], Claude-Mem is an external plugin and service layer rather than an internal markdown-memory subsystem.
- Compared with lightweight local note systems, Claude-Mem adds more moving parts: hooks, worker process, SQLite, Chroma, viewer UI, and MCP search endpoints.
- Compared with purely semantic memory systems such as [[research/misc/papers/mem0-2025]], it leans harder into developer workflow tooling, operational plumbing, and search UX around stored observations.

## Why It Matters
- Claude-Mem is a strong example of the "memory engine as plugin" design point for coding agents.
- It shows a concrete architecture for cross-session continuity that is independent of Claude Code's own internal memory design.
- The progressive-disclosure retrieval pattern is also notable: retrieval quality is treated as a token-budgeting and workflow problem, not only as an embedding problem.

## Limitations
- This note is based on the public repository documentation and surfaced GitHub pages, not a line-by-line local code audit.
- The repository README mixes architecture, installation, and product claims, so some implementation details would need deeper source inspection to verify exhaustively.
- Claude-Mem is operationally heavier than simple markdown-memory approaches because it requires a worker, local databases, and plugin integration.

## Takeaways
- Claude-Mem should be categorized in `misc` as a repo-backed coding-agent memory system, not as Claude Code's native memory implementation.
- Its main systems idea is persistent capture plus progressive-disclosure retrieval: collect broadly, store locally, search cheaply, expand selectively.
- For future comparisons, it is useful as a bridge case between agent-memory research papers and production developer tooling.

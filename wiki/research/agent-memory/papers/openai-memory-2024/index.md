---
title: "OpenAI Memory (ChatGPT product feature)"
domain: research
area: misc
type: source
status: processed
updated: 2026-04-19
tags: [openai, chatgpt, memory, product-feature, help-center, personalization]
---
# OpenAI Memory (ChatGPT product feature)

## Source Meta
- Title: OpenAI Memory / Memory and new controls for ChatGPT
- Author: OpenAI
- Year: 2024 with 2025 product updates
- Venue: OpenAI product blog and Help Center
- Topic: misc
- Source Slug: openai-memory-2024
- Product Blog: https://openai.com/index/memory-and-new-controls-for-chatgpt/
- Help Center: https://help.openai.com/en/articles/8983136-what-is-memory
- Help Center FAQ: https://help.openai.com/en/articles/8590148-memory-faq
- Reading Source: official blog + Help Center; no arXiv source or TeX
- Repo Read: not applicable
- PDF Fallback: not used

## TL;DR
- OpenAI Memory is a ChatGPT product feature, not a research paper.
- The feature launched publicly in February 2024 and was materially expanded in 2025 to use both saved memories and chat history.
- The official docs frame memory as a personalization and convenience feature: ChatGPT can remember user preferences, recall prior chats when enabled, and use those signals to tailor responses and search query rewrites.
- The key design point is user control. OpenAI exposes toggles for saved memories, chat history reference, temporary chats, deletion, and training controls.

## What It Is
- ChatGPT memory works in two related ways:
  - **Saved memories**: explicit or auto-saved durable facts such as preferences, names, or goals.
  - **Chat history**: references to past conversations to improve future responses.
- The feature is intended to make ChatGPT more personalized and reduce repetition across sessions.
- The help center explicitly warns that memory is meant for high-level preferences and should not be treated as a verbatim store.
- ChatGPT can also use memory details when rewriting search queries for web search.

## Feature Timeline
| Date | Change | Source |
|---|---|---|
| 2024-02-13 | OpenAI announces "Memory and new controls for ChatGPT" | https://openai.com/index/memory-and-new-controls-for-chatgpt/ |
| 2024-09-05 | Memory becomes available to Free, Plus, Team, and Enterprise users | same OpenAI blog post |
| 2025-04-10 | Memory becomes more comprehensive and references all past conversations | same OpenAI blog post |
| 2025-06-03 | Memory improvements start rolling out for free users, with shorter-term continuity | same OpenAI blog post |
| 2026-04 (current docs) | Help Center presents current control and privacy details | https://help.openai.com/en/articles/8983136-what-is-memory |

## Controls And Privacy
- Users can turn memory off, delete specific memories, clear all memories, or use Temporary Chat so the conversation does not reference or update memory.
- The help center says turning off memory does not necessarily delete existing memories; deletion must be done explicitly.
- The FAQ says ChatGPT may use content from chats and memories to improve models if the user has the relevant data-control setting turned on.
- The feature raises privacy concerns, and OpenAI says it avoids proactively storing sensitive information unless explicitly asked.
- Enterprise and EDU controls are more restrictive, and availability varies by plan.

## Why This Is Not A Paper
- There is no arXiv abstract, TeX source, or code repository to ingest.
- The authoritative source is a product blog post plus Help Center documentation that is periodically updated.
- For wiki purposes, this should be treated as a product-source note, not a research paper note.

## Takeaways
- OpenAI Memory is best understood as a productized persistent-context layer, not as a published algorithmic contribution.
- The notable engineering choice is a two-tier memory model: durable saved facts plus recent-chat continuity.
- For memory-system comparisons, this is a useful baseline because it is explicitly controlled by product policy and exposes user-facing memory toggles.


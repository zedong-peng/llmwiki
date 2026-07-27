---
title: "Personalize Before Retrieve: User-Specific Query Expansion"
domain: research
area: agent-memory
type: paper
status: stub
updated: 2026-05-28
tags: [paper, retrieval, personalization, query-expansion, user-history]
---

# Personalize Before Retrieve: User-Specific Query Expansion

## Paper Meta
- Title: Personalize Before Retrieve: Personalized Query Expansion for Conversational Search
- Authors: —
- Year: 2025
- Venue: arXiv
- arXiv: https://arxiv.org/abs/2510.08935

## TL;DR
- User-specific query expansion injecting history, preferences, persona before retrieval.
- Conversation history = personalization signal for query generation.

## Method
- Extract user history, preferences, and persona from conversation.
- Inject these signals into query expansion before retrieval.
- Personalized queries better match user-specific information needs.

## Relevance to LAzyMem
Conversation history as personalization signal for query generation is directly applicable to LoCoMo. LAzyMem leverages this differently: rather than expanding queries, it uses the question to compile speaker-filtered boolean predicates, treating the conversation as a structured corpus rather than a personalization signal.

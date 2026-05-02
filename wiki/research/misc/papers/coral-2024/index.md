---
title: "CORAL: Benchmarking Multi-turn Conversational Retrieval-Augmentation Generation"
domain: research
area: misc
type: paper
status: processed
updated: 2026-04-19
tags: [paper, misc, rag, conversational-rag, benchmark, multi-turn]
---
# CORAL: Benchmarking Multi-turn Conversational Retrieval-Augmentation Generation

## Paper Meta
- Title: CORAL: Benchmarking Multi-turn Conversational Retrieval-Augmentation Generation
- Authors: Yiruo Cheng, Kelong Mao, Ziliang Zhao, Guanting Dong, Hongjin Qian, Yongkang Wu, Tetsuya Sakai, Ji-Rong Wen, Zhicheng Dou
- Year: 2024
- Venue: arXiv preprint; final venue not reported in the source
- Topic: misc
- Paper Slug: coral-2024
- arXiv: https://arxiv.org/abs/2410.23090
- PDF: 2410.23090.pdf
- Code Repo: https://github.com/Ariya12138/CORAL
- Reading Source: TeX source (`source/extracted/naacl25.tex`, `custom.bib`)
- Repo Read: `README.md` and `Constructing_Process/readme.md`
- PDF Fallback: not used

## TL;DR
- CORAL is a multi-turn conversational RAG benchmark built from Wikipedia and designed to evaluate three tasks jointly: passage retrieval, response generation, and citation labeling.
- The dataset contains 8,000 conversations and is explicitly built to include topic shifts, long-form responses, and source attribution, which makes it more aligned with deployed conversational RAG than single-turn QA benchmarks.
- For this repo's retrieval thread, CORAL is useful because it separates conversational retrieval quality from response generation and makes it possible to test whether generated lexical queries stay useful once topic shift and dialogue history enter the loop.
- The baseline results are mixed: conversational dense retrieval and query rewriting are fairly close, and fine-tuned open-source rewriting can match or beat GPT-3.5-based rewriting.

## Problem
- Most RAG evaluation work focuses on single-turn settings, while real assistants usually operate over multi-turn conversations.
- Multi-turn RAG adds coreference, omission, dialogue drift, topic shifts, and long noisy histories.
- Existing conversational search or QA datasets each miss something important for practical conversational RAG: open-domain scope, free-form answers, topic-shift handling, or citation labeling.

## Method
- CORAL is constructed from English Wikipedia pages using an HTML-tree-to-conversation pipeline.
- The paper treats Wikipedia titles and subtitles as question sources and the corresponding section text as high-quality grounded free-form responses.
- Four conversation-flow sampling strategies create different dialogue structures:
  - Linear Descent Sampling
  - Sibling-Inclusive Descent Sampling
  - Single-Tree Random Walk
  - Dual-Tree Random Walk
- GPT-4 is used to rewrite title-derived questions into more natural conversational turns with omission and coreference.
- The benchmark evaluates three tasks:
  - Conversational Passage Retrieval
  - Response Generation
  - Citation Labeling

## Benchmarks / Datasets
| Dataset / Benchmark | Task | Metric | Notes |
|---|---|---|---|
| CORAL | conversational passage retrieval | MRR, MAP, NDCG@3, Recall@20, Recall@100 | Multi-turn retrieval with dialogue history |
| CORAL | response generation | BLEU-1, ROUGE-L, RichRAG-style model evaluation | Long-form answer generation |
| CORAL | citation labeling | Citation Recall, Citation Precision | Uses ALCE-style citation metrics |

- Dataset statistics from the source and repo:
  - `8,000` conversations total
  - 4 structure types, `2,000` conversations each
  - README table reports train/test counts across LDS, SIDS, STRW, and DTRW
  - Test-set turns per conversation range roughly from `3.26` to `10.77`

## Baselines
| Baseline | Type | Why Important | Notes |
|---|---|---|---|
| Conv-ANCE-Q / Conv-ANCE-C | conversational dense retrieval | Main CDR baselines | Trained on QReCC or CORAL |
| KD-ANCE-Q / KD-ANCE-C | conversational dense retrieval | Stronger CDR reference | Uses golden-query distillation |
| LLM4CS (GPT-3.5) | conversational query rewriting | Closed-source CQR baseline | Rewrites before retrieval |
| Qwen2.5-1.5B | open rewrite model | Open-source CQR baseline | Raw open rewrite model |
| Qwen2.5-1.5B-SFT | fine-tuned open rewrite model | Strong open CQR baseline | Competitive with or better than GPT-3.5 rewrite |
| Raw Context / Last Response / Rewrite / LLM Summarization | generation-side history handling | Conversational compression strategies | Tested with multiple generators and SFT variants |

## Main Results
| Task | Best reported result | Notes |
|---|---|---|
| Retrieval | KD-ANCE-C gets `MRR 23.2`, `MAP 33.6`, `Recall@20 40.3`, `Recall@100 49.6` | Strongest CDR row in the main retrieval table |
| Retrieval | Qwen2.5-1.5B-SFT gets `NDCG@3 25.1` and `MAP 33.6` | Competitive CQR result; nearly matches or ties KD-ANCE-C |
| Generation | Raw Context + Qwen2.5-3B-SFT gets `BLEU-1 25.8` | Best BLEU-1 in the scaling table |
| Generation | Raw Context + Qwen2.5-7B-SFT gets `ROUGE-L 18.5` | Best ROUGE-L in the scaling table |
| Citation | LLM Summarization + Qwen2.5-3B-SFT gets `Citation Recall 14.6`, `Citation Precision 36.0` | Best citation row in the scaling table |

- The paper's interpretation:
  - CDR and CQR are broadly comparable.
  - Fine-tuned open-source rewriting (`Qwen2.5-1.5B-SFT`) surpasses raw Qwen2.5-1.5B and beats GPT-3.5-based LLM4CS on all retrieval metrics in the table.
  - Compressing conversation history can substantially reduce input length with only small generation losses, and sometimes improves citation behavior.

## Ablations / Analysis
- The paper analyzes four ways of modeling conversation history on the generation side:
  - Raw Context
  - Last Response
  - Rewrite
  - LLM Summarization
- A key observation is that stronger compression can preserve generation quality surprisingly well while improving citation labeling, suggesting that much history is noise.
- Scaling analysis with Qwen2.5 0.5B to 7B shows:
  - generation quality rises sharply from 0.5B to 1.5B
  - citation labeling improves more noticeably at larger sizes
- History-length analysis shows that more dialogue context is not monotonically better; after SFT, four to six turns can help, but very long histories introduce noise again.

## Implementation Clues
- The repo is relatively lightweight compared with the paper: it documents the dataset format, construction overview, and high-level framework, but does not include a large runnable training/evaluation stack in the checked-out files here.
- The README confirms the 8,000-conversation JSONL format with turn-level fields for question, response, and golden passages.
- `Constructing_Process/readme.md` records the four conversation-flow sampling strategies, which is the clearest implementation clue for how the benchmark's multi-turn structure is synthesized.
- The source specifies the retrieval stack used in evaluation:
  - KD-ANCE and Conv-ANCE for conversational dense retrieval
  - LLM4CS and open-source Qwen rewriting for conversational query rewriting
  - Faiss for dense retrieval

## Limitations
- The dataset is derived from Wikipedia, so there is contamination risk when using modern LLMs trained on overlapping corpora; the paper explicitly notes this.
- The conversation-compression strategies are fairly simple and mostly length-reduction-oriented.
- The local repo snapshot is dataset-centric and documentation-centric; it does not expose the full experimental pipeline in detail.

## Takeaways
- CORAL is one of the more useful "RAG-side" benchmarks for this wiki's retrieval thread because it moves beyond single-turn search and forces retrieval methods to cope with dialogue history and topic shift.
- It is a good testbed for asking whether generated lexical predicates or search programs still help once retrieval becomes conversational rather than static.
- The strong Qwen rewrite result is also a reminder that "LLM-generated intermediate retrieval queries" already has a foothold in conversational RAG, so a new method here needs to be more specific than just generic rewriting.

## Open Questions
- Can structured lexical programs outperform free-form query rewriting on CORAL retrieval?
- When topic shift is explicit, is generated-keyword search still competitive with conversational dense retrieval?
- Could citation labeling improve further if retrieval returned more structured evidence neighborhoods instead of flat top-k passages?

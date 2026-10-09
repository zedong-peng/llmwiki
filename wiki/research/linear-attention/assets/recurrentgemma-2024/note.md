---
title: "RecurrentGemma: Moving Past Transformers for Efficient Open Language Models"
domain: research
area: linear-attention
type: paper
status: active
updated: 2026-04-21
tags: [paper, misc, linear-attn, recurrentgemma, griffin, google-deepmind]
---

# RecurrentGemma: Moving Past Transformers for Efficient Open Language Models

> Status: fully ingested from local TeX and repo assets on 2026-04-21.

## Paper Meta
- Title: RecurrentGemma: Moving Past Transformers for Efficient Open Language Models
- Authors: Aleksandar Botev, Soham De, Samuel L. Smith, Anushan Fernando, George Cristian-Muraru, Ruba Haroun, Leonard Berrada, Razvan Pascanu, and others
- Year: 2024
- Venue: arXiv preprint / technical report
- Paper Slug: recurrentgemma-2024
- arXiv: https://arxiv.org/abs/2404.07839
- Official repo: https://github.com/google-deepmind/recurrentgemma

## TL;DR
- RecurrentGemma is Google DeepMind's open-weights implementation of the Griffin architecture: linear recurrences plus local attention, not global attention.
- The paper releases 2B and 9B variants, each in pre-trained and instruction-tuned form, and trains both sizes on 2T tokens.
- The main payoff is inference efficiency: the state is fixed-size, so long-sequence generation avoids the KV-cache growth that constrains standard transformers.

## Problem
- Transformer inference cost grows with sequence length because the KV cache must be stored and reloaded, which is especially painful for long generation.
- Local attention can reduce cache size, but it still keeps the attention-centric execution pattern and does not fully solve the memory-bound bottleneck.
- The paper asks whether an open language model can keep competitive quality while replacing global attention with a bounded recurrent state.

## Method
- RecurrentGemma uses the Griffin architecture, mixing linear recurrences with local attention. The recurrent state is fixed-size, while local attention handles short-range context.
- The release includes both JAX and PyTorch paths, with a specialized Pallas kernel for the linear recurrence in the TPU-oriented Flax implementation and a reference PyTorch implementation for portability.
- The paper makes a small architectural change relative to Griffin: input embeddings are multiplied by `sqrt(model width)`, with tied input/output embeddings and no output-side scaling.

## Results
- Both model sizes are trained on 2T tokens, compared with Gemma-2B on 3T tokens and Gemma-7B on 6T tokens.
- RecurrentGemma-2B is competitive with Gemma-2B on academic benchmarks despite using fewer tokens; RecurrentGemma-9B is competitive with Gemma-7B.
- Human evaluation shows RecurrentGemma-2B IT reaches a 43.7% win rate against Mistral 7B v0.2 Instruct on instruction-following prompts, while RecurrentGemma-9B IT reaches 59.3%.
- Throughput results show substantially higher sampling throughput than Gemma, especially for long sequences; prompt processing remains similar because both models parallelize that phase efficiently.

## Implementation Clues
- The repo README recommends the Flax implementation for best performance and keeps PyTorch as a less optimized reference path.
- The codebase is checkpoint-driven rather than training-first: users download Flax or PyTorch model archives from Kaggle and run sampling or fine-tuning examples locally.
- The release is TPU-friendly by design, and the README explicitly calls out the Pallas kernel used for the recurrent linear scan.

## Limitations
- This is not a pure linear-attention paper; it is a hybrid recurrent-plus-local-attention design, so its gains do not transfer directly to all linear-attention families.
- The strongest throughput claims are TPU-centric, and the repo itself warns that PyTorch and GPU paths are less optimized.
- The paper still relies on local attention, so the architecture does not eliminate all context-length-dependent computation.

## Takeaways
- RecurrentGemma is the practical open-model counterpart to Griffin: same design family, packaged as runnable checkpoints and optimized inference code.
- For the broader linear-attention thread, it is the clearest proof that fixed-state recurrent hybrids can preserve quality while improving long-sequence inference behavior.
- The most durable local references are the Griffin framing in `paper-tex/extracted/legacy/main.tex` and the implementation guidance in `github-repo/recurrentgemma/README.md`.

## Local Assets
- PDF: `paper-pdf/2404.07839.pdf`
- Source archive: `paper-tex/archives/2404.07839-source.tar.gz`
- Extracted source: `paper-tex/extracted/legacy/`
- Repo: `github-repo/recurrentgemma/`

## Source Notes
- Main TeX: `paper-tex/extracted/legacy/main.tex`
- Contributions section: `paper-tex/extracted/legacy/contributions.tex`
- Repo README: `github-repo/recurrentgemma/README.md`

## 迁移来源与阅读边界

本页保留历史实质阅读笔记；本次迁移没有重新阅读或执行研究代码。原归档的书目信息、版本、hash、仓库 commit 与 metadata 快照见 [citation.bib](citation.bib)。
旧 metadata 将 reading.status 记为 `not_started`，与上述历史笔记及来源描述不一致；保留两者作为历史记录，具体阅读范围以上述已记载内容为限，不补写未记录的范围。
仓库缓存的 commit 与检索日期保留在 citation.bib；恢复的当前缓存不证明历史阅读时所用 revision，原笔记未记录的历史 commit 仍未知。
书目字段来自旧记录，作者列表及发表信息尚未在本次迁移复核。原文下载版本未记录时，不根据 slug 或文件名猜测版本。

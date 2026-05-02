---
title: "Jamba: A Hybrid Transformer-Mamba Language Model"
domain: research
area: linear-attention
type: paper
status: processed
updated: 2026-04-21
tags: [paper, misc, linear-attn, jamba, hybrid-model, mamba]
---

# Jamba: A Hybrid Transformer-Mamba Language Model

> Status: processed from local TeX and PDF on 2026-04-21.

## Paper Meta
- Title: Jamba: A Hybrid Transformer-Mamba Language Model
- Authors: Opher Lieber, Barak Lenz, Hofit Bata, Gal Cohen, Jhonathan Osin, Itay Dalmedigos, Erez Safahi, Shaked Meirom, Yonatan Belinkov, Shai Shalev-Shwartz, Omri Abend, Raz Alon, Tomer Asida, Amir Bergman, Roman Glozman, Michael Gokhman, Avshalom Manevich, Nir Ratner, Noam Rozen, Erez Schwartz, Mor Zusman, Yoav Shoham
- Year: 2024
- Venue: arXiv preprint
- Paper Slug: jamba-2024
- Model release: AI21 Jamba-v0.1
- arXiv: https://arxiv.org/abs/2403.19887

## TL;DR
Jamba is a public base model that mixes Transformer layers, Mamba layers, and MoE in a single decoder stack. The key claim is not just quality, but the joint operating point: similar or better benchmark performance than comparable open models, materially lower KV-cache cost at long context, and better throughput on long sequences.

## Problem
The paper targets the tension between Transformer quality and long-context efficiency. Pure Transformers pay a large KV-cache and inference cost at long context, while pure SSMs or recurrent models can be efficient but may lose in-context-learning behavior and other capabilities. Jamba is presented as a large-scale hybrid intended to keep the best of both.

## Method
- The architecture interleaves Transformer and Mamba layers inside a repeated Jamba block.
- The released configuration uses a 1:7 attention-to-Mamba ratio, with MoE inserted every other layer and 16 experts total, top-2 routed per token.
- The model uses RMSNorm inside Mamba layers for stability, no explicit positional encoding in the main released configuration, and standard decoder components like GQA and SwiGLU.
- The design space is exposed as `l`, `a:m`, `e`, `n`, and `K`, which lets the architecture trade off quality, throughput, and memory footprint.

## Results
- On common academic benchmarks, Jamba is broadly competitive with Mixtral-8x7B and Llama-2 70B, while using 12B active parameters and 52B total parameters.
- The paper reports 256K-token support in the released model and training runs up to 1M context length.
- For long contexts, the KV cache is reported as 4GB at 256K tokens versus 32GB for Mixtral and 128GB for Llama-2 13B in the paper's comparison table.
- Throughput is reported as 3x Mixtral on two long-context settings: large batches on a single A100 80GB and 128K-token context on 4 A100s.

## Ablations
- Hybrid Attention-Mamba beats pure Attention and pure Mamba at 1.3B scale after 250B tokens.
- The paper reports no meaningful difference between 1:3 and 1:7 attention-to-Mamba ratios, so 1:7 was chosen for efficiency.
- Adding MoE improves the hybrid further: the 7B-scale hybrid with MoE outperforms the no-MoE variant across the reported OLLM, HellaSwag, WinoGrande, NQ, and log-prob metrics.
- Pure Mamba underperforms on tasks that require strict answer formatting and in-context learning, while the hybrid recovers much of the missing behavior.

## Implementation Clues
- The released model is intended to fit on a single 80GB GPU with int8 weights and a 140K-token input window.
- The paper notes loss spikes when scaling the Mamba stack to the largest run; adding RMSNorm to internal Mamba activations stabilizes training.
- The architecture appears to rely on the Mamba stack to carry implicit position information, because explicit positional encoding did not materially help in the reported comparison.
- The PDF and TeX source are consistent: the main TeX file is a self-contained NeurIPS-style paper with all core results in-line, no external repo required for this note.

## Limitations
- The released model is a base model, not aligned or instruction-tuned, and the paper explicitly warns against production use without additional adaptation.
- The paper is a hybrid architecture report, so some gains come from mixing inductive biases rather than from isolating a single clean mechanism.
- Benchmark results are strong but still mostly point-in-time evaluations; the authors themselves caution that benchmarks only partially reflect real deployment value.

## Takeaways
- Jamba is a concrete production-grade hybrid of attention and SSM, not just a conceptual bridge paper.
- The main engineering lesson is that attention-to-Mamba ratio and MoE placement are real design variables, not cosmetic choices.
- For the linear-attention reading queue, Jamba is important as an adoption reference: it shows a practical hybrid path where state-space layers handle most of the sequence while a smaller attention component preserves ICL behavior.

## Local Assets
- PDF: `2403.19887.pdf`
- Source archive: `source/archives/2403.19887-source.tar.gz`
- Extracted source: `source/extracted/`
- Repo: no official public training/inference repository identified during this import pass

## Open Questions
- How much of Jamba's advantage survives when the architecture is pushed into smaller or more latency-sensitive regimes?
- Which parts of the gain come from the Mamba layers themselves versus the MoE scaling strategy?
- Can the same hybrid recipe be simplified further without losing the long-context and throughput benefits?

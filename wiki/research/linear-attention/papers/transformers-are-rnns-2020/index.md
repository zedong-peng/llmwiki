---
title: "Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention"
domain: research
area: linear-attention
type: paper
status: processed
updated: 2026-04-21
tags: [paper, misc, linear-attn, linear-transformer, recurrent-formulation]
---

# Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention

> Status: fully read from local TeX/PDF/repo assets on 2026-04-21.

## Paper Meta
- Title: Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention
- Authors: Angelos Katharopoulos, Apoorv Vyas, Nikolaos Pappas, Francois Fleuret
- Year: 2020
- Venue: ICML 2020
- Paper Slug: transformers-are-rnns-2020
- arXiv: https://arxiv.org/abs/2006.16236
- Official repo: https://github.com/idiap/fast-transformers

## Local Assets
- PDF: `2006.16236.pdf`
- Source archive: `source/archives/2006.16236-source.tar.gz`
- Extracted source: `source/extracted/`
- Repo: `repo/fast-transformers/`

## TL;DR
- This paper is the canonical first-generation linear-attention result.
- The core move is to replace softmax attention with a positive feature-map dot product, then use associativity to turn causal attention into a recurrent state update.
- The paper is compelling because it gives both a theoretical story, `O(N)` scaling, and a concrete implementation path that runs much faster in autoregressive decoding.

## Problem
- Vanilla self-attention is quadratic in sequence length for both time and memory.
- That makes long-context training expensive and autoregressive inference especially slow, because each next token must re-attend to the entire prefix.
- The paper asks whether the attention mechanism itself can be rewritten so the model keeps transformer-like training parallelism but gets RNN-like inference.

## Method
- The attention kernel is linearized with a feature map `phi(x) = elu(x) + 1`, chosen because it stays positive and avoids zeroing gradients the way ReLU would.
- With that map, the attention output becomes a ratio of two prefix sums: `S_i = sum(phi(K_j) V_j^T)` and `Z_i = sum(phi(K_j))`.
- Causal masking then becomes a simple recurrence: update `S_i` and `Z_i` from the previous state in constant time, and compute the output from the current query against that state.
- This is the key conceptual step behind the title: a causal transformer layer can be written as an RNN with hidden state `(s, z)`.
- The supplementary derivation shows the backward pass can also be implemented with cumulative sums, so both forward and backward remain linear time and constant memory in sequence length.

## Experiments
- Synthetic copy task: linear attention matches softmax loss and converges more cleanly than Reformer because it does not introduce hashing noise.
- Memory/time benchmark on a GTX 1080 Ti: softmax becomes quadratic, while linear attention and Reformer scale linearly; linear is faster and uses less memory across all tested lengths.
- MNIST autoregressive generation: linear reaches `0.644` bits/dim versus `0.621` for softmax, with `142.8 images/sec` or `317x` throughput over softmax.
- CIFAR-10 autoregressive generation: linear gets `3.40` bits/dim and `17.85 images/sec`, versus `0.004` images/sec for softmax, which the paper describes as roughly `4,460x` throughput.
- WSJ speech recognition with CTC: linear reaches `8.08` PER and `824 s/epoch`, beating Reformer and the Bi-LSTM baseline on speed, though softmax still gets the best PER.

## Implementation Clues
- The repo README frames `fast-transformers` as a general research library for fast attention, not just a one-off paper artifact.
- The library exposes a builder API that can switch between full softmax attention and linear attention through `attention_type = "full"` versus `"linear"`.
- The paper states the constant-memory gradient path is implemented in about `200` lines of CUDA, which is a useful signal that the algorithm was meant to be practically deployable, not just mathematically neat.
- The repo also lists this paper as part of an internal research line, which makes it the implementation anchor for later follow-up work in the same codebase.

## Limitations
- The main approximation is the choice of feature map; exact softmax is not recovered, so quality depends on how well the chosen map behaves on the task.
- The paper’s speedups are strongest in autoregressive inference and long sequences; for shorter sequences the benefit is smaller and training can still favor conventional transformers.
- The reported experiments are mostly early-2020-era tasks and hardware, so the headline speedups should be read as a proof of concept rather than a modern hardware ceiling.

## Takeaways
- This is the paper that makes “linear attention” feel like a real algorithmic family rather than a loose approximation trick.
- The RNN equivalence is more than a metaphor: the state form `(s, z)` is the exact reason autoregressive decoding can be constant time per token.
- Later generations of linear attention, gated recurrence, and kernel/compiler work all sit downstream of the pattern established here.

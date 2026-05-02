---
title: "Gated Delta Networks: Improving Mamba2 with Delta Rule"
domain: research
area: linear-attention
type: paper
status: processed
updated: 2026-04-21
tags: [paper, misc, linear-attn, gated-deltanet, delta-rule, nvidia]
---

# Gated Delta Networks: Improving Mamba2 with Delta Rule

## Paper Meta
- Title: Gated Delta Networks: Improving Mamba2 with Delta Rule
- Authors: Songlin Yang, Jan Kautz, Ali Hatamizadeh
- Year: 2025
- Venue: ICLR 2025
- Paper Slug: gated-deltanet-2025
- arXiv: https://arxiv.org/abs/2412.06464
- Official repo: https://github.com/NVlabs/GatedDeltaNet

## TL;DR
- The paper argues that gating and the delta rule solve complementary memory problems in linear transformers: gating is good at rapid forgetting, while the delta rule is good at targeted updates.
- It introduces the gated delta rule and extends the earlier delta-rule parallelization into a chunkwise hardware-efficient training algorithm.
- Empirically, Gated DeltaNet improves over Mamba2 and DeltaNet on language modeling, commonsense reasoning, in-context retrieval, length extrapolation, and long-context understanding.
- The implementation story matters: the paper is not only a model proposal, but also a training algorithm plus hybrid model recipe.

## Problem
- Standard Transformers still dominate some retrieval-heavy and long-context settings, but quadratic attention is expensive.
- Linear attention variants reduce memory cost, yet they often underperform on exact retrieval because their fixed-size state collides when many associations accumulate.
- Mamba2-style decay improves forgetting, but it is coarse-grained: it suppresses all stored associations together rather than selectively editing one association.
- DeltaNet-style updates improve targeted memory replacement, but by themselves they cannot rapidly clear stale context when the input distribution shifts.

## Method
- The core update is the gated delta rule, which interpolates between rapid erasure and selective update by controlling the scalar decay term `alpha_t`.
- In the paper’s formulation, `alpha_t -> 0` behaves like memory reset, while `alpha_t -> 1` recovers the pure delta rule.
- The authors extend the WY-based parallel delta-rule algorithm from prior work to include gating terms, preserving chunkwise parallelism for hardware-efficient training.
- The base block follows a Llama-like macro design with token mixer plus SwiGLU MLP, and uses linear projections, short convolution, SiLU, L2 normalization on queries/keys, and output gating.
- Two hybrid variants are emphasized: `GatedDeltaNet-H1` combines Gated DeltaNet with sliding window attention, and `GatedDeltaNet-H2` stacks Mamba2, Gated DeltaNet, and SWA.

## Experiments
- Training is done at 1.3B parameters on 100B FineWeb-Edu tokens with a 4K training length and a 2K sliding window for the hybrid models.
- The benchmark suite covers commonsense reasoning, synthetic and real-world in-context retrieval, length extrapolation up to 20K tokens, long-context understanding, and training throughput.
- The paper’s S-NIAH case study is the cleanest proof of concept: Gated DeltaNet improves memory retention relative to Mamba2 and targeted replacement relative to DeltaNet.
- On real-world retrieval tasks, the gap is narrower than on synthetic retrieval, but Gated DeltaNet still improves over both DeltaNet and Mamba2.
- The hybrid variants are the strongest overall systems result: they preserve or improve throughput while improving downstream quality.

## Implementation Clues
- The repo explicitly says the Gated DeltaNet block is available from FLA and recommends FLA for faster varlen training and inference.
- The local NVLabs repo shows the block shape: `ShortConvolution` on q/k/v, `FusedRMSNormSwishGate`, and a chunked training-oriented implementation.
- The paper and repo together make clear that the practical deployment path is not a standalone model kernel, but a reusable block that can be embedded in a broader FLA stack.
- The repo README also points to optimized FLA kernels and Hugging Face conversion for evaluation, which is important if this thread later needs reproducible benchmarking.

## Main Results
- Gated DeltaNet is positioned as a better memory manager than DeltaNet and a more flexible update rule than Mamba2.
- The gated delta rule adds only marginal overhead relative to the original delta rule, so the accuracy gain is not bought by a large throughput penalty.
- The paper states that Gated DeltaNet is essentially as fast as DeltaNet and only slightly slower than Mamba2, while hybrid variants can recover or exceed throughput on practical sequence lengths.
- For long-context tasks, the hybrid design is the strongest evidence that mixing recurrent state with local attention is the right systems tradeoff.

## Limitations
- Fixed-size recurrent state remains the core bottleneck: even with better updates, exact retrieval still degrades when the stored association set grows too large.
- The strongest gains appear in synthetic retrieval and hybrid settings; real-world retrieval still shows smaller margins because task errors are partly dominated by instruction-following and repetition effects.
- The implementation is still a careful systems compromise rather than a universally best mixer: the best block depends on whether the workload is retrieval-heavy, local-context-heavy, or throughput-constrained.

## Takeaways
- Gated DeltaNet is the clearest “delta rule + gating” synthesis in the current linear-attention family.
- For this wiki thread, it is an important bridge between the algorithmic line (`Transformers are RNNs`, `DeltaNet`, `Mamba2`) and the implementation line (`FLA`, hybrid kernels, varlen support).
- The paper is especially valuable because it argues from both sides at once: memory semantics and efficient parallel execution.
- If this area keeps expanding, this page should stay as the canonical processed summary, while repo-specific kernel details can live in the related implementation notes.

## Local Assets
- PDF: `2412.06464.pdf`
- Source archive: `source/archives/2412.06464-source.tar.gz`
- Extracted source: `source/extracted/main.tex`, `source/extracted/main.bbl`
- Repo: `repo/GatedDeltaNet/`


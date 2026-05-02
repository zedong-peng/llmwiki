---
title: "Transformers are SSMs: Generalized Models and Efficient Algorithms Through Structured State Space Duality"
domain: research
area: linear-attention
type: paper
status: processed
updated: 2026-04-21
tags: [paper, misc, linear-attn, mamba-2, ssm-duality, state-space-duality, SSD]
---

# Transformers are SSMs: Generalized Models and Efficient Algorithms Through Structured State Space Duality

## Paper Meta
- Title: Transformers are SSMs: Generalized Models and Efficient Algorithms Through Structured State Space Duality
- Authors: Tri Dao, Albert Gu
- Year: 2024
- Venue: ICML 2024
- Paper Slug: mamba-2-2024
- arXiv: https://arxiv.org/abs/2405.21060
- Official repo: https://github.com/state-spaces/mamba

## TL;DR
- This paper is the cleanest formal bridge between Mamba-style selective SSMs and attention-like sequence models.
- The core contribution is SSD, a state-space duality framework based on semiseparable matrices, which yields both theory and a hardware-efficient algorithm.
- The practical result is Mamba-2: a block redesign that is more TP-friendly, easier to scale, and materially faster than the original Mamba implementation.

## Problem
- Prior work had a split ecosystem: Transformers had mature algorithmic and systems tooling, while SSMs were strong on sequence length but harder to optimize and reason about.
- The paper asks whether SSMs and attention can be placed into a shared algebraic framework so that implementations, parallelism, and architecture design can transfer across the two families.
- The answer matters for both modeling and systems: the goal is not just better asymptotics, but a sequence layer that actually maps well to GPU tensor cores and distributed training.

## Method
- SSD reframes structured SSMs as semiseparable matrices and shows that selective SSMs and structured masked attention occupy a large shared family of "state space dual" models.
- The main algorithm computes SSD by block-decomposing the semiseparable matrix and mixing the linear recurrent form with the quadratic dual form, which gives better hardware tradeoffs than a pure scan.
- Mamba-2 changes the block layout to make the layer parallel-friendly: it moves data-dependent projections to the front, introduces grouped-value attention style head structure, and makes tensor parallelism practical.

## Results
- The SSD implementation is reported to be 2-8x faster than the optimized selective scan implementation of Mamba for large state sizes, while also allowing much larger recurrent state.
- SSD is competitive with FlashAttention-2 and crosses over at sequence length 2K, becoming about 6x faster at 16K.
- On language modeling, Mamba-2 Pareto-dominates Mamba and Transformer++ in perplexity and wall-clock time in the paper's reported scaling setup.
- On downstream evaluation, Mamba-2 with 2.7B parameters trained on 300B Pile tokens outperforms Mamba-2.8B, Pythia-2.8B, and even Pythia-6.9B on the same data budget.
- On MQAR, larger state size matters materially: the paper shows that increasing the recurrent state improves recall performance, which supports the claim that SSD is not just a speed trick.

## Implementation Clues
- The local repo is the official `state-spaces/mamba` codebase and contains the practical Mamba-2 path, including `mamba_ssm/modules/mamba2.py`, `mamba_ssm/modules/mamba2_simple.py`, and the minimal SSD reference implementation.
- The README explicitly links both the original Mamba paper and this Mamba-2 paper, so the repository is the right code anchor for comparing Mamba-1 vs Mamba-2 behavior.
- The paper source is split into sections for SSD, efficient algorithms, architecture, systems, experiments, and appendix details, which makes the TeX tree a better reading source than the PDF alone.

## Limitations
- SSD is not a general replacement for softmax attention; the paper itself is explicit that the duality applies to structured attention families with finite feature maps, not arbitrary attention kernels.
- The Mamba-2 block is more parallel and hardware-friendly, but the paper still notes that a pure Transformer can be more efficient at some short sequence settings because it mixes attention and MLP layers differently.
- The strongest claims are about the SSD/Mamba-2 family, not about all possible linear-attention variants, so this paper should be treated as a framework paper rather than a universal benchmark winner.

## Takeaways
- SSD is the main conceptual artifact to carry forward: it is the common algebraic object that unifies selective SSMs and a structured attention family.
- Mamba-2 matters because it turns that theory into a block design that can use tensor parallelism, sequence parallelism, and matrix-multiply-heavy kernels.
- For the linear-attention/hardware thread, this is a foundational paper: it is where the SSM line becomes comparable to attention on both theory and systems grounds.

## Local Assets
- PDF: `2405.21060.pdf`
- Source archive: `source/archives/2405.21060-source.tar.gz`
- Extracted source: `source/extracted/`
- Repo: `repo/mamba/`

## Reading Notes
- The TeX source is the authoritative reading path here; the key sections are `abstract`, `intro`, `ssd`, `efficient`, `architecture`, `systems`, and `experiments`.
- The repo is useful for implementation context, especially the Mamba-2 block and the SSD minimal layer, but the paper's claims and definitions live in the source tree.

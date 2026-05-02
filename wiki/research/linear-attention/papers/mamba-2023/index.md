---
title: "Mamba: Linear-Time Sequence Modeling with Selective State Spaces"
domain: research
area: linear-attention
type: paper
status: processed
updated: 2026-04-21
tags: [paper, misc, linear-attn, mamba, ssm, selective-scan]
---

# Mamba: Linear-Time Sequence Modeling with Selective State Spaces

> Status: formally ingested from local TeX/PDF/repo assets on 2026-04-21.

## Paper Meta
- Title: Mamba: Linear-Time Sequence Modeling with Selective State Spaces
- Authors: Albert Gu, Tri Dao
- Year: 2023
- Venue: NeurIPS 2023
- Paper Slug: mamba-2023
- arXiv: https://arxiv.org/abs/2312.00752
- Official repo: https://github.com/state-spaces/mamba

## Local Assets
- PDF: `2312.00752.pdf`
- Source archive: `source/archives/2312.00752-source.tar.gz`
- Extracted source: `source/extracted/`
- Repo: `repo/mamba/`

## TL;DR
- Mamba turns structured state space models into a content-dependent sequence model by making the SSM parameters input-dependent, so the recurrence can selectively propagate or forget information.
- The paper's core technical move is a hardware-aware selective scan: compute the time-varying recurrence without materializing the full `(B, L, D, N)` state tensor in HBM, then fuse/recompute to keep memory use close to a strong Transformer implementation.
- Empirically, the result is a strong general sequence backbone: 5x higher inference throughput than Transformers, better scaling on long contexts, and state-of-the-art or best-in-class results on language, audio, and genomics.

## Problem
- Prior subquadratic architectures were either efficient but too rigid, or expressive enough only on continuous modalities.
- The paper identifies the missing capability as content-based selection: the model must decide, token by token, what to remember and what to discard.
- This is especially important for discrete, information-dense modalities such as text and DNA, where pure LTI SSMs underperform.

## Method
- The selective SSM layer keeps the state space backbone but makes `dt`, `B`, and `C` functions of the input, converting the recurrence from time-invariant to time-varying.
- The implementation replaces convolution with scan, because the parameters now vary by position; efficiency comes from kernel fusion, parallel scan, and recomputation.
- The final Mamba block simplifies older SSM stacks by folding the usual SSM block and MLP-style transformation into one homogeneous block repeated through the network.

## Results
- Synthetic copying: selective SSMs solve the task, while non-selective SSMs do not; Mamba reaches 99.8% on the strongest setting, while the non-selective baselines stay far lower.
- Induction heads: Mamba extrapolates to million-token lengths, far beyond the training length.
- Language modeling: on the Pile, Mamba-130M reaches 10.56 Pile ppl and 44.7 zero-shot average, Mamba-370M reaches 8.28 / 50.0, Mamba-790M reaches 7.33 / 57.1, Mamba-1.4B reaches 6.80 / 59.7, and Mamba-2.8B reaches 6.22 / 63.3.
- DNA classification: on Great Apes classification, Mamba-7M reaches 81.31% accuracy at sequence length `2^20`, versus 54.87% for HyenaDNA-1.4M.
- Audio generation: on SC09, Mamba-24.3M reaches FID 0.67, IS 7.33, and mIS 144.9, outperforming the SaShiMi baseline and the larger generative baselines listed in the paper.
- Efficiency: the selective scan is about 40x faster than a standard implementation and 20-40x faster than PyTorch scan; end-to-end inference is about 4-5x faster than a comparable Transformer.

## Implementation Notes
- The public repo exposes the exact code path the paper describes: `mamba_ssm/ops/selective_scan_interface.py` implements `selective_scan_fn` and the fused autograd path, while `mamba_ssm/modules/mamba_simple.py` implements the block.
- The fast path in `Mamba.forward()` uses the fused inner kernel (`mamba_inner_fn`) when the CUDA dependencies are available; otherwise it falls back to a slower explicit path.
- The repo README also documents Mamba-2 and Mamba-3, so this codebase is not just the paper artifact but the long-lived implementation family.

## Limitations
- The paper is explicit that selectivity is not a universal win: on continuous, smooth modalities such as audio waveforms, the LTI bias of earlier SSMs can be better.
- The main empirical study is still below the scale of the strongest open LLMs; the paper itself says larger-scale validation remains open.
- Performance is strongly implementation-dependent; the recurrence is only competitive because the authors carefully fuse and schedule it for GPU memory hierarchy.

## Takeaways
- Mamba is best read as a model-design paper plus a systems paper: the architecture idea only matters because the scan kernel makes it practical.
- For the linear-attention / SSM line, this paper is the key proof that input-dependent state updates can close the quality gap on discrete language tasks without giving up linear-time inference.
- The official repo is the implementation anchor for downstream work, especially `selective_scan_fn`, `mamba_inner_fn`, and the `Mamba` block used throughout the family.

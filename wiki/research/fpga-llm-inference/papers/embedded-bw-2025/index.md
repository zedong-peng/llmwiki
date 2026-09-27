---
title: "Pushing up to the Limit of Memory Bandwidth and Capacity Utilization for Efficient LLM Decoding on Embedded FPGA"
domain: research
area: fpga-llm-inference
type: paper
status: seed
updated: 2026-07-24
tags: [paper, fpga, llm-inference]
---

# Pushing up to the Limit of Memory Bandwidth and Capacity Utilization for Efficient LLM Decoding on Embedded FPGA

> Bibliographic record and local public asset cache. Full paper notes are pending.

## Paper Meta

- Authors: Jindong Li, Tenglong Li, Guobin Shen, Dongcheng Zhao, Qian Zhang, Yi Zeng
- Year: 2025
- Venue: 2025 Design, Automation and Test in Europe Conference
- BibTeX key: `embedded_bw`
- Related Work category: Embedded and low-bit LLM deployment
- Public record: [DOI](https://doi.org/10.23919/DATE64628.2025.10993087); [arXiv](https://arxiv.org/abs/2502.10659)

## Local Assets

- Paper PDF: [2502.10659.pdf](2502.10659.pdf) (7 pages; SHA-256 `56f87fc2a5c31e8ceddab7c4319d4fc44cff1d76f09b6b4877ed4423ab296072`)

## Ingest Status

- Metadata: verified against the manuscript bibliography.
- Paper PDF: `downloaded`.
- Reading note: seed; no unverified method or performance claims added.
- Source archive and code repository: not requested in this import pass.

Return to [[research/fpga-llm-inference/papers/index|FPGA LLM paper library]].

## Original-text verification (2026-09-27)

Checked against the original paper text or public code for the llama.cpp FPGA backend paper; supersedes earlier summaries where they differ.

- Code: github.com/adamgallas/llama-fpga (206 stars on 2026-09-27; also cited as ICCAD'25 follow-up).
- KV260 with 64-bit DDR4-2400 (19.2 GB/s); LLaMA2-7B AWQ 4-bit; about 5 token/s decode, 85% of the theoretical bandwidth limit; 300 MHz (PDF text lines 42-44, 96-99, 109).

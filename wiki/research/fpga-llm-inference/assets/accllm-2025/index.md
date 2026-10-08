---
title: "AccLLM: Accelerating Long-Context LLM Inference Via Algorithm-Hardware Co-Design"
domain: research
area: fpga-llm-inference
type: paper
status: seed
updated: 2026-07-24
tags: [paper, fpga, llm-inference]
---

# AccLLM: Accelerating Long-Context LLM Inference Via Algorithm-Hardware Co-Design

> Bibliographic record and local public asset cache. Full paper notes are pending.

## Paper Meta

- Authors: Yanbiao Liang, Huihong Shi, Haikuo Shao, Zhongfeng Wang
- Year: 2025
- Venue: arXiv preprint
- BibTeX key: `accllm`
- Related Work category: Long-context and phase-specialized acceleration
- Public record: [arXiv](https://arxiv.org/abs/2505.03745)

## Local Assets

- Paper PDF: [2505.03745.pdf](paper-pdf/2505.03745.pdf) (13 pages; SHA-256 `9d183689febd28655e39b0b35fddc464d32306e4138f8817d2c269f96f1c4aca`)

## Ingest Status

- Metadata: verified against the manuscript bibliography.
- Paper PDF: `downloaded`.
- Reading note: seed; no unverified method or performance claims added.
- Source archive and code repository: not requested in this import pass.

Return to [[research/fpga-llm-inference/index#Paper Library|FPGA LLM paper library]].

## Original-text verification (2026-09-27)

Checked against the original paper text or public code for the llama.cpp FPGA backend paper; supersedes earlier summaries where they differ.

- Published: IEEE Transactions on VLSI Systems, 2026, DOI 10.1109/TVLSI.2026.3658524 (Crossref).
- U280 at 225 MHz, Llama-2-7B with 2:4 pruning, Lambda-shaped attention and W2A8KV4; 164 token/s, 33 W, 4.96 token/J in Table VII - from a cycle-accurate simulator validated against RTL, not an on-board run.
- Table VII also lists FlightLLM U280 55 token/s (45 W), FlightLLM VHK158 92.5, EdgeLLM VCU128 ChatGLM2-6B 75 token/s at 125 MHz, A100 45 token/s.

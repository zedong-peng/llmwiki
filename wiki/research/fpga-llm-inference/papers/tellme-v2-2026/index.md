---
title: "TeLLMe: An Efficient End-to-End Ternary LLM Prefill and Decode Accelerator with Table-Lookup Matmul on Edge FPGAs"
domain: research
area: fpga-llm-inference
type: paper
status: seed
updated: 2026-09-15
tags: [paper, fpga, llm-inference]
---

# TeLLMe: An Efficient End-to-End Ternary LLM Prefill and Decode Accelerator with Table-Lookup Matmul on Edge FPGAs

> Bibliographic record and local public asset cache. Full paper notes are pending.

## Paper Meta

- Authors: Ye Qiao, Zhiheng Chen, Yifan Zhang, Yian Wang, Sitao Huang
- Year: 2026
- Venue: Proceedings of the 2026 ACM/SIGDA International Symposium on Field Programmable Gate Arrays
- BibTeX key: `tellme_v2`
- Related Work category: FPGA Transformer and LLM systems
- Public record: [DOI](https://doi.org/10.1145/3748173.3779191); [arXiv](https://arxiv.org/abs/2510.15926)

## Local Assets

- Paper PDF: [2510.15926.pdf](2510.15926.pdf) (11 pages; SHA-256 `510e249e529748795cf6544efe41473ee18bf0ffd943e37974f76afc3064f14d`)

## Ingest Status

- Metadata: verified against the manuscript bibliography.
- Paper PDF: `downloaded`.
- Reading note: seed; no unverified method or performance claims added.
- Source archive and code repository: not requested in this import pass.

Return to [[research/fpga-llm-inference/papers/index|FPGA LLM paper library]].

## Model input and coverage audit (2026-09-15)

**Classification: Model-specific implementation.** BitNet-0.73B ternary model.

chatbot.py ModelConfig fixes 24 layers, hidden=1536, FFN=4096, vocabulary=32002 and 16 heads of dimension 96, explicitly matching HLS configuration. The loader expects prepared .bin weights and checks array sizes. Changing the Python configuration alone does not demonstrate matching hardware or another architecture. This identifies the released model-specific implementation, not a proof the table-lookup method cannot be generalized.

Inspected code (pinned copies, not executed):

- [README.md](source/code-audit/README.md) — [upstream commit](https://github.com/UCI-CORSA/TeLLMe_FPGA_2026/blob/139ad882aba8485048e08993022872128bc00f51/README.md).
- [on_board_test/src/chatbot.py](source/code-audit/on_board_test/src/chatbot.py) — [upstream commit](https://github.com/UCI-CORSA/TeLLMe_FPGA_2026/blob/139ad882aba8485048e08993022872128bc00f51/on_board_test/src/chatbot.py).

[Audit receipt](source/model-coverage-audit.json). See [[research/fpga-llm-inference/index#Model input and coverage audit (2026-09-15)|cross-paper comparison]] for definitions and input formats. This dated section supersedes older coverage/placement summaries where they conflict.

---
title: "CODO: An Automated Compiler for Comprehensive Dataflow Optimization"
domain: research
area: fpga-llm-inference
type: paper
status: active
updated: 2026-09-08
tags: [paper, fpga, llm-inference]
---

# CODO: An Automated Compiler for Comprehensive Dataflow Optimization

CODO is an automated MLIR/dataflow compiler for fixed-shape FPGA graphs. Its GPT-2 result is an
important compiler reference, but its public artifact must be kept separate from a stateful
llama.cpp generation baseline.

## Paper Meta

- Authors: Weichuang Zhang, Yiquan Wang, Xinzhou Zhang, Chi Zhang, Yu Feng, Xiaofeng Hou, Chao Li, Jieru Zhao, Minyi Guo
- Year: 2026
- Venue: ISCA 2026, verified against the [official conference program](https://www.iscaconf.org/isca2026/program/) on 2026-09-08. The archived full text is the arXiv version; venue verification is separate from artifact reproduction.
- BibTeX key: `codo`
- Related Work category: FPGA Transformer and LLM systems
- Public record: [arXiv](https://arxiv.org/abs/2604.12618)

## Local Assets

- Paper PDF: [2604.12618.pdf](2604.12618.pdf) (17 pages; SHA-256 `b31c6872fc51bf5f779fc501952b78fbfa6d6233a71464c1e07e5b0ac8ec5b2e`)
- arXiv source archive: [2604.12618-source.tar.gz](source/archives/2604.12618-source.tar.gz); extracted TeX: [main.tex](source/extracted/main.tex)

## Read Notes

- The paper reports GPT-2 Medium on U280 at W4A8/300 MHz, including TTFT, decode speed and total latency. These figures are useful for understanding fixed graph/dataflow performance, but are not inserted into the current CPU/FPGA throughput table.
- The public `GPT2.py` forward computes current-input Q/K/V but has no `past_key_values` input/output. The Fig. 9 host statically binds HBM buffers and invokes one `main_graph` event; no token loop, cache position, append pointer or cross-launch state object is exposed.
- Therefore “CODO has no K/V” is inaccurate, while “the public artifact does not demonstrate persistent KV-cache management or KV-specific optimization” is supported. The author's clarification that the experiment measures one fixed-graph latency is recorded in the comparison note.
- Source-first read completed. Detailed artifact audit: [[research/fpga-llm-inference/codo-2026]].

## Public Artifact Recheck (2026-09-08)

- Official repository: [sjtu-zhao-lab/codo-artifact](https://github.com/sjtu-zhao-lab/codo-artifact). Local cache: [README.md](repo/codo-artifact/README.md), commit `130b12bc63e6e6daa31a1227b7e8391c5039148d`. Reused the committed objects from `/home/zdpeng/codo` after direct GitHub cloning timed out; GitHub's API independently confirmed the same current main SHA. The cache does not include that working tree's uncommitted changes or initialized dependency submodules.
- Re-read the complete main TeX, bibliography, artifact README, verification entry/data/config/helpers, GPT2 model, decode host, and synthesis runner. `gen_mlir_designs.py` instantiates the single block with random initialized parameters; `data.py` supplies seeded FP32 random input `[1,32,1024]`, hidden size 1024 and 16 heads. `utils.py` exports raw input/output `.bin` tensors as a functional oracle, not a text-generation workload. This verification example must be distinguished from the paper's W4A8 on-board figures.
- All four Fig. 9 host files expose one `enqueueTask` and event-start/end profiling. In the fully inspected decode host, output migration is commented out and `TEST PASSED` is printed without a result comparison. This is not a board-level model-correctness receipt.
- `experiments/run_all.sh` runs synthesis experiments for Fig. 11 and Tables II-IV, not the GPT generation loop. No `.xclbin` or `host.exe` appears in this committed repository snapshot. Dependencies, Docker contents and board execution were not reproduced here.
- Thus **public artifact available** is supported; **independently reproduced stateful generation** is not established by this inspection. Do not erase CODO's compiler-artifact credit when narrowing its generation boundary. The user's report of a private author conversation is corroborating context, not a public citation or proof of how every published number was derived.
- Feature-table definitions and cross-paper artifact discovery: [[research/fpga-llm-inference/feature-level-evidence-matrix]].

Return to [[research/fpga-llm-inference/papers/index|FPGA LLM paper library]].

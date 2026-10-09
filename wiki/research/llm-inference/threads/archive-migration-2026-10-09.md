---
title: LLM Inference 历史归档迁移与缺失证据
domain: research
area: llm-inference
type: note
status: active
updated: 2026-10-09
tags: [archive, migration]
---

# 历史归档迁移与缺失证据

后续清理：按用户要求删除两份本机工程记录的 assets 目录，它们不作为参考文献。当前保留 26 个引用、25 份阅读笔记；以下迁移计数及缺失路径清单记录删除前的历史状态。

本次只整理已有本地记录，没有重新阅读、核验科学结论、执行研究代码、连接远端或重跑实验。旧 metadata 全文作为历史快照保留在各 citation.bib 的 `%` 注释中；snapshot 的 downloaded/cached 等字段不代表当前文件存在。

28 个历史 slug 保留；27 个实际论文、源码或工程阅读记录迁至 note.md，1 个检索素材索引迁入 threads 并标明命中论文未读。作者、出版信息和固定 arXiv 版本依据已有来源记录，未从 slug 推断；软件归档日期只使用 urldate，不冒充发布日期。

迁移开始前本 topic 已删除 278 个被跟踪文件，多为 supplementary 实验/核验记录。下面逐项保留历史路径；本轮不恢复。工程笔记中的旧结果和服务状态仅代表记录日期，当前缺失资产使本地证据复查不完整。

## 预先删除路径

- `wiki/research/llm-inference/assets/beellama-cpp-2026/supplementary/github-api-commit.json`
- `wiki/research/llm-inference/assets/beellama-cpp-2026/supplementary/github-api-repository.json`
- `wiki/research/llm-inference/assets/beellama-cpp-2026/supplementary/web-extraction-2026-10-01.txt`
- `wiki/research/llm-inference/assets/cinference-4090-2026/supplementary/github-api-commit.json`
- `wiki/research/llm-inference/assets/cinference-4090-2026/supplementary/github-api-repository.json`
- `wiki/research/llm-inference/assets/exllamav3-2026/supplementary/github-api-commit.json`
- `wiki/research/llm-inference/assets/exllamav3-2026/supplementary/github-api-repository.json`
- `wiki/research/llm-inference/assets/exllamav3-2026/supplementary/mia-deployment-README.md`
- `wiki/research/llm-inference/assets/exllamav3-2026/supplementary/mia-engine-start.sh`
- `wiki/research/llm-inference/assets/exllamav3-2026/supplementary/r0b0tlab-ACCEPTANCE.md`
- `wiki/research/llm-inference/assets/exllamav3-2026/supplementary/r0b0tlab-ENV.md`
- `wiki/research/llm-inference/assets/exllamav3-2026/supplementary/r0b0tlab-deployment-README.md`
- `wiki/research/llm-inference/assets/exllamav3-2026/supplementary/turboderp-qwen38-model-README.md`
- `wiki/research/llm-inference/assets/exllamav3-2026/supplementary/turboderp-qwen38-model-info.json`
- `wiki/research/llm-inference/assets/g4090-agent-tools-2026/supplementary/agent_tools_install_20261001_retry.log`
- `wiki/research/llm-inference/assets/g4090-agent-tools-2026/supplementary/install-manifest.json`
- `wiki/research/llm-inference/assets/g4090-agent-tools-2026/supplementary/install_agent_tools.py`
- `wiki/research/llm-inference/assets/g4090-agent-tools-2026/supplementary/npm-package-manifest.json`
- `wiki/research/llm-inference/assets/g4090-agent-tools-2026/supplementary/smoke-results.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/Qwen3.8-27B-DFlash2-EXL3-4.00bpw-manifest.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/Qwen3.8-27B-EXL3-4.00bpw-manifest.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/archive-assets-qa.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/audit_benchmark_results.py`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/benchmark_exl3.py`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/benchmark_http.py`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/download_exl3_models.py`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-ar-dry-run.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/README.md`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/archive-manifest.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/benchmark_exl3_guarded.py`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/dflash2-config-pinned.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-ar-benchmark.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-ar-k0-cq4-cs4096/exl3-ar-k0-cq4-cs4096-code-0.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-ar-k0-cq4-cs4096/exl3-ar-k0-cq4-cs4096-code-0.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-ar-k0-cq4-cs4096/exl3-ar-k0-cq4-cs4096-code-1.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-ar-k0-cq4-cs4096/exl3-ar-k0-cq4-cs4096-code-1.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-ar-k0-cq4-cs4096/exl3-ar-k0-cq4-cs4096-code-2.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-ar-k0-cq4-cs4096/exl3-ar-k0-cq4-cs4096-code-2.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-ar-k0-cq4-cs4096/exl3-ar-k0-cq4-cs4096-json-0.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-ar-k0-cq4-cs4096/exl3-ar-k0-cq4-cs4096-json-0.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-ar-k0-cq4-cs4096/exl3-ar-k0-cq4-cs4096-json-1.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-ar-k0-cq4-cs4096/exl3-ar-k0-cq4-cs4096-json-1.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-ar-k0-cq4-cs4096/exl3-ar-k0-cq4-cs4096-json-2.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-ar-k0-cq4-cs4096/exl3-ar-k0-cq4-cs4096-json-2.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-ar-k0-cq4-cs4096/exl3-ar-k0-cq4-cs4096-prose-0.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-ar-k0-cq4-cs4096/exl3-ar-k0-cq4-cs4096-prose-0.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-ar-k0-cq4-cs4096/exl3-ar-k0-cq4-cs4096-prose-1.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-ar-k0-cq4-cs4096/exl3-ar-k0-cq4-cs4096-prose-1.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-ar-k0-cq4-cs4096/exl3-ar-k0-cq4-cs4096-prose-2.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-ar-k0-cq4-cs4096/exl3-ar-k0-cq4-cs4096-prose-2.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-ar-k0-cq4-cs4096/exl3-ar-k0-cq4-cs4096.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-ar-k0-cq4-cs4096/exl3-ar-k0-cq4-cs4096.summary.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-benchmark.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k15-benchmark.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k15-cq4-cs4096/exl3-dflash2-k15-cq4-cs4096-json-0.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k15-cq4-cs4096/exl3-dflash2-k15-cq4-cs4096.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k15-guard-check.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k7-cq4-cs4096/exl3-dflash2-k7-cq4-cs4096-code-0.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k7-cq4-cs4096/exl3-dflash2-k7-cq4-cs4096-code-0.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k7-cq4-cs4096/exl3-dflash2-k7-cq4-cs4096-code-1.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k7-cq4-cs4096/exl3-dflash2-k7-cq4-cs4096-code-1.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k7-cq4-cs4096/exl3-dflash2-k7-cq4-cs4096-code-2.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k7-cq4-cs4096/exl3-dflash2-k7-cq4-cs4096-code-2.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k7-cq4-cs4096/exl3-dflash2-k7-cq4-cs4096-json-0.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k7-cq4-cs4096/exl3-dflash2-k7-cq4-cs4096-json-0.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k7-cq4-cs4096/exl3-dflash2-k7-cq4-cs4096-json-1.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k7-cq4-cs4096/exl3-dflash2-k7-cq4-cs4096-json-1.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k7-cq4-cs4096/exl3-dflash2-k7-cq4-cs4096-json-2.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k7-cq4-cs4096/exl3-dflash2-k7-cq4-cs4096-json-2.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k7-cq4-cs4096/exl3-dflash2-k7-cq4-cs4096-prose-0.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k7-cq4-cs4096/exl3-dflash2-k7-cq4-cs4096-prose-0.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k7-cq4-cs4096/exl3-dflash2-k7-cq4-cs4096-prose-1.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k7-cq4-cs4096/exl3-dflash2-k7-cq4-cs4096-prose-1.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k7-cq4-cs4096/exl3-dflash2-k7-cq4-cs4096-prose-2.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k7-cq4-cs4096/exl3-dflash2-k7-cq4-cs4096-prose-2.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k7-cq4-cs4096/exl3-dflash2-k7-cq4-cs4096.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k7-cq4-cs4096/exl3-dflash2-k7-cq4-cs4096.summary.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-git-import-and-template.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-mtp-benchmark.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-mtp-k4-cq4-cs4096/exl3-mtp-k4-cq4-cs4096-code-0.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-mtp-k4-cq4-cs4096/exl3-mtp-k4-cq4-cs4096-code-0.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-mtp-k4-cq4-cs4096/exl3-mtp-k4-cq4-cs4096-code-1.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-mtp-k4-cq4-cs4096/exl3-mtp-k4-cq4-cs4096-code-1.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-mtp-k4-cq4-cs4096/exl3-mtp-k4-cq4-cs4096-code-2.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-mtp-k4-cq4-cs4096/exl3-mtp-k4-cq4-cs4096-code-2.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-mtp-k4-cq4-cs4096/exl3-mtp-k4-cq4-cs4096-json-0.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-mtp-k4-cq4-cs4096/exl3-mtp-k4-cq4-cs4096-json-0.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-mtp-k4-cq4-cs4096/exl3-mtp-k4-cq4-cs4096-json-1.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-mtp-k4-cq4-cs4096/exl3-mtp-k4-cq4-cs4096-json-1.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-mtp-k4-cq4-cs4096/exl3-mtp-k4-cq4-cs4096-json-2.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-mtp-k4-cq4-cs4096/exl3-mtp-k4-cq4-cs4096-json-2.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-mtp-k4-cq4-cs4096/exl3-mtp-k4-cq4-cs4096-prose-0.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-mtp-k4-cq4-cs4096/exl3-mtp-k4-cq4-cs4096-prose-0.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-mtp-k4-cq4-cs4096/exl3-mtp-k4-cq4-cs4096-prose-1.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-mtp-k4-cq4-cs4096/exl3-mtp-k4-cq4-cs4096-prose-1.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-mtp-k4-cq4-cs4096/exl3-mtp-k4-cq4-cs4096-prose-2.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-mtp-k4-cq4-cs4096/exl3-mtp-k4-cq4-cs4096-prose-2.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-mtp-k4-cq4-cs4096/exl3-mtp-k4-cq4-cs4096.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-mtp-k4-cq4-cs4096/exl3-mtp-k4-cq4-cs4096.summary.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-runner-before-gpu.py`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-runner-config-guard.diff`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-suite-summary.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/run_exl3_bench.sh`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-cpu-install.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-deployment-notes.md`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-git-import-and-template.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-model-downloads.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/exl3-pip-freeze.txt`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/git-clone-provenance-exl3-hyperqwen.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/install_exl3_cpu.sh`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/qwen38-cinference.service`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/qwen38-config.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/qwen38-model-api.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/build-env.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/cinference-benchmark-matched-k3-k7.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/cinference-benchmark-matched.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/cinference-benchmark.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/cinference-build.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/cinference-configure.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/cinference-service.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/cinference-service.requests.jsonl`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/cinference-unpack.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/gguf-download.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/gguf-mtp-download.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/llama-benchmark-matched.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/llama-build.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/llama-configure.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/llama-source-download.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/model-download-mirror.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/model-download.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/model-v3-conversion.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/ninfer-benchmark-matched-k5.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/ninfer-benchmark-matched.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/ninfer-build.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/ninfer-configure.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/primary-audit-current.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/primary-audit-final-http.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/runner-timewait-guard-test.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/service-verification-final.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/service-verification.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/zlib-install.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/build-env-explicit.txt`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/cinference-help.txt`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/cinference-server-help.txt`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/cmake-build-provenance.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/cuda-toolkit.txt`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/gguf-mtp-sha256.txt`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/gguf-sha256.txt`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/git-clone-provenance-exl3-hyperqwen.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/gpu-hardware.csv`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/cinference-int8-k0.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/cinference-int8-k0.requests.jsonl`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/cinference-int8-k0.runs.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/cinference-int8-k0.server.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/cinference-int8-k0.summary.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/cinference-int8-k3.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/cinference-int8-k3.requests.jsonl`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/cinference-int8-k3.server.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/cinference-int8-k3.summary.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/cinference-int8-k7.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/cinference-int8-k7.requests.jsonl`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/cinference-int8-k7.server.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/cinference-int8-k7.summary.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/cinference-int8.runs.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/llama-udq4-k0.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/llama-udq4-k0.server.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/llama-udq4-k0.summary.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/llama-udq4-k3.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/llama-udq4-k3.server.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/llama-udq4-k3.summary.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/llama-udq4-k7.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/llama-udq4-k7.server.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/llama-udq4-k7.summary.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/llama-udq4.runs.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/ninfer-erik-int8-k0-k3-k7.runs.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/ninfer-erik-int8-k0.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/ninfer-erik-int8-k0.requests.jsonl`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/ninfer-erik-int8-k0.server.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/ninfer-erik-int8-k0.summary.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/ninfer-erik-int8-k3.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/ninfer-erik-int8-k3.requests.jsonl`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/ninfer-erik-int8-k3.server.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/ninfer-erik-int8-k3.summary.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/ninfer-erik-int8-k5.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/ninfer-erik-int8-k5.requests.jsonl`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/ninfer-erik-int8-k5.server.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/ninfer-erik-int8-k5.summary.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/ninfer-erik-int8-k7.server.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/ninfer-erik-int8.runs.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench/cinference-int8-k0.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench/cinference-int8-k0.requests.jsonl`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench/cinference-int8-k0.server.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench/cinference-int8-k0.summary.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench/cinference-int8-k3.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench/cinference-int8-k3.requests.jsonl`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench/cinference-int8-k3.server.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench/cinference-int8-k3.summary.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench/cinference-int8-k7.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench/cinference-int8-k7.requests.jsonl`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench/cinference-int8-k7.server.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench/cinference-int8-k7.summary.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench/cinference-int8.runs.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/llama-bench-help.txt`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/llama-git-clone.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/llama-server-help.txt`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/ninfer-v2-sha256.txt`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/ninfer-v3-payload-verification.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/ninfer-v3-sha256.txt`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/official-commit-fetch-validation.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/official-commit-fetch-validation.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/primary-benchmark-audit.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/qwen38-cinference-4090-git-status-after-20260930T211550Z.txt`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/qwen38-cinference-4090-git-status-before-20260930T211550Z.txt`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/qwen38-cinference-4090-independent-git-clone-20260930T211550Z.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/qwen38-cinference-4090-removed-appledouble-20260930T211550Z.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/qwen38-ninfer-4090-git-status-after-20260930T211550Z.txt`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/qwen38-ninfer-4090-git-status-before-20260930T211550Z.txt`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/qwen38-ninfer-4090-independent-git-clone-20260930T211550Z.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/qwen38-ninfer-4090-removed-appledouble-20260930T211550Z.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/remote-git-clones-ninfer.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/service-verification/anthropic.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/service-verification/binary-and-unit.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/service-verification/code.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/service-verification/final-reconnect-and-cli.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/service-verification/final-systemd-state.txt`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/service-verification/json.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/service-verification/manager-state.txt`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/service-verification/responses-schema-correction.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/service-verification/responses.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/service-verification/stopped-at-user-request.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/service-verification/stream.sse`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/service-verification/summary.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/tabby-base-install.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/tabby-base-install.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/tabby-cpu-pycompile/backends_exllamav3_model.pyc`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/tabby-cpu-pycompile/common_args.pyc`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/tabby-cpu-pycompile/common_config_models.pyc`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/tabby-cpu-pycompile/main.pyc`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/tabby-dflash2-http-preparation.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/tabby-git-clone.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/tabby-git-clone.log`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/tabby-pip-freeze-after.txt`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/tabby-pip-freeze-before.txt`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/tabby-pip-plan.json`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/tabby-preserve-engine-constraints.txt`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/run_exl3_bench.sh`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/run_llama_modes.py`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/run_ninfer_modes.py`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/run_qwen38_service.sh`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/service_ctl.sh`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/tabby-http-preparation/README.md`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/tabby-http-preparation/dflash2-benchmark.yml`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/tabby-http-preparation/launch_dflash2_http.sh`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/verify_container_payload.py`
- `wiki/research/llm-inference/assets/g4090-qwen38-benchmark-2026/supplementary/verify_qwen38_service.py`
- `wiki/research/llm-inference/assets/hyperqwen-2026/supplementary/github-api-commit.json`
- `wiki/research/llm-inference/assets/hyperqwen-2026/supplementary/github-api-repository.json`
- `wiki/research/llm-inference/assets/ik-llama-cpp-2026/supplementary/github-api-commit.json`
- `wiki/research/llm-inference/assets/ik-llama-cpp-2026/supplementary/github-api-repository.json`
- `wiki/research/llm-inference/assets/llama-cpp-2026/supplementary/github-api-commit.json`
- `wiki/research/llm-inference/assets/llama-cpp-2026/supplementary/github-api-repository.json`
- `wiki/research/llm-inference/assets/ninfer-4090-2026/supplementary/github-api-commit.json`
- `wiki/research/llm-inference/assets/ninfer-4090-2026/supplementary/github-api-repository.json`
- `wiki/research/llm-inference/assets/ninfer-4090-2026/supplementary/landscape-github-observations.json`
- `wiki/research/llm-inference/assets/ninfer-4090-windows-2026/supplementary/github-api-commit.json`
- `wiki/research/llm-inference/assets/ninfer-4090-windows-2026/supplementary/github-api-repository.json`
- `wiki/research/llm-inference/assets/ninfer-4090-windows-2026/supplementary/jgamboa-model-README.md`
- `wiki/research/llm-inference/assets/ninfer-4090-windows-2026/supplementary/jgamboa-model-info.json`
- `wiki/research/llm-inference/assets/ninfer-all-2026/supplementary/github-api-commit.json`
- `wiki/research/llm-inference/assets/ninfer-all-2026/supplementary/github-api-repository.json`
- `wiki/research/llm-inference/assets/ninfer-all-2026/supplementary/wavecut-gsq-model-README.md`
- `wiki/research/llm-inference/assets/ninfer-all-2026/supplementary/wavecut-gsq-model-info.json`
- `wiki/research/llm-inference/assets/qwen38-4090-paper-search-2026/supplementary/qwen38-paper-search-installed.log`
- `wiki/research/llm-inference/assets/qwen38-4090-paper-search-2026/supplementary/qwen38-paper-search-researchstudio-py311.log`
- `wiki/research/llm-inference/assets/qwen38-4090-paper-search-2026/supplementary/qwen38-paper-search-researchstudio.log`
- `wiki/research/llm-inference/assets/tokenspeed-2026/supplementary/github-api-commit.json`
- `wiki/research/llm-inference/assets/tokenspeed-2026/supplementary/github-api-repository.json`
- `wiki/research/llm-inference/assets/tokenspeed-2026/supplementary/web-extraction-2026-10-01.txt`

## 历史 metadata 引用但本地缺失的路径

包括不由 wiki Git 保存的代码缓存和 TeX 压缩包；缺失不等于本轮删除。已失败下载路径未算作成功归档。

### beellama-cpp-2026

[[research/llm-inference/assets/beellama-cpp-2026/note]]；[来源快照](../assets/beellama-cpp-2026/citation.bib)。

- `assets/beellama-cpp-2026/supplementary/github-api-commit.json`
- `assets/beellama-cpp-2026/supplementary/github-api-repository.json`
- `assets/beellama-cpp-2026/supplementary/web-extraction-2026-10-01.txt`

### cinference-4090-2026

[[research/llm-inference/assets/cinference-4090-2026/note]]；[来源快照](../assets/cinference-4090-2026/citation.bib)。

- `assets/cinference-4090-2026/supplementary/github-api-commit.json`
- `assets/cinference-4090-2026/supplementary/github-api-repository.json`

### exllamav3-2026

[[research/llm-inference/assets/exllamav3-2026/note]]；[来源快照](../assets/exllamav3-2026/citation.bib)。

- `assets/exllamav3-2026/supplementary/github-api-commit.json`
- `assets/exllamav3-2026/supplementary/github-api-repository.json`
- `assets/exllamav3-2026/supplementary/mia-deployment-README.md`
- `assets/exllamav3-2026/supplementary/mia-engine-start.sh`
- `assets/exllamav3-2026/supplementary/r0b0tlab-ACCEPTANCE.md`
- `assets/exllamav3-2026/supplementary/r0b0tlab-ENV.md`
- `assets/exllamav3-2026/supplementary/r0b0tlab-deployment-README.md`
- `assets/exllamav3-2026/supplementary/turboderp-qwen38-model-README.md`
- `assets/exllamav3-2026/supplementary/turboderp-qwen38-model-info.json`

### g4090-agent-tools-2026

[[research/llm-inference/threads/2026-10-01-g4090-agent-tools]]；来源快照（引用目录已删除）。

- `assets/g4090-agent-tools-2026/supplementary/agent_tools_install_20261001_retry.log`
- `assets/g4090-agent-tools-2026/supplementary/install-manifest.json`
- `assets/g4090-agent-tools-2026/supplementary/install_agent_tools.py`
- `assets/g4090-agent-tools-2026/supplementary/npm-package-manifest.json`
- `assets/g4090-agent-tools-2026/supplementary/smoke-results.json`

### g4090-qwen38-benchmark-2026

[[research/llm-inference/threads/2026-10-01-g4090-qwen38-speed]]；来源快照（引用目录已删除）。

- `assets/g4090-qwen38-benchmark-2026/supplementary/Qwen3.8-27B-DFlash2-EXL3-4.00bpw-manifest.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/Qwen3.8-27B-EXL3-4.00bpw-manifest.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/archive-assets-qa.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/audit_benchmark_results.py`
- `assets/g4090-qwen38-benchmark-2026/supplementary/benchmark_exl3.py`
- `assets/g4090-qwen38-benchmark-2026/supplementary/benchmark_http.py`
- `assets/g4090-qwen38-benchmark-2026/supplementary/download_exl3_models.py`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-ar-dry-run.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/README.md`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/archive-manifest.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/benchmark_exl3_guarded.py`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/dflash2-config-pinned.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-ar-benchmark.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-ar-k0-cq4-cs4096/exl3-ar-k0-cq4-cs4096-code-0.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-ar-k0-cq4-cs4096/exl3-ar-k0-cq4-cs4096-code-0.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-ar-k0-cq4-cs4096/exl3-ar-k0-cq4-cs4096-code-1.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-ar-k0-cq4-cs4096/exl3-ar-k0-cq4-cs4096-code-1.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-ar-k0-cq4-cs4096/exl3-ar-k0-cq4-cs4096-code-2.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-ar-k0-cq4-cs4096/exl3-ar-k0-cq4-cs4096-code-2.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-ar-k0-cq4-cs4096/exl3-ar-k0-cq4-cs4096-json-0.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-ar-k0-cq4-cs4096/exl3-ar-k0-cq4-cs4096-json-0.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-ar-k0-cq4-cs4096/exl3-ar-k0-cq4-cs4096-json-1.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-ar-k0-cq4-cs4096/exl3-ar-k0-cq4-cs4096-json-1.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-ar-k0-cq4-cs4096/exl3-ar-k0-cq4-cs4096-json-2.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-ar-k0-cq4-cs4096/exl3-ar-k0-cq4-cs4096-json-2.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-ar-k0-cq4-cs4096/exl3-ar-k0-cq4-cs4096-prose-0.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-ar-k0-cq4-cs4096/exl3-ar-k0-cq4-cs4096-prose-0.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-ar-k0-cq4-cs4096/exl3-ar-k0-cq4-cs4096-prose-1.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-ar-k0-cq4-cs4096/exl3-ar-k0-cq4-cs4096-prose-1.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-ar-k0-cq4-cs4096/exl3-ar-k0-cq4-cs4096-prose-2.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-ar-k0-cq4-cs4096/exl3-ar-k0-cq4-cs4096-prose-2.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-ar-k0-cq4-cs4096/exl3-ar-k0-cq4-cs4096.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-ar-k0-cq4-cs4096/exl3-ar-k0-cq4-cs4096.summary.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-benchmark.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k15-benchmark.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k15-cq4-cs4096/exl3-dflash2-k15-cq4-cs4096-json-0.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k15-cq4-cs4096/exl3-dflash2-k15-cq4-cs4096.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k15-guard-check.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k7-cq4-cs4096/exl3-dflash2-k7-cq4-cs4096-code-0.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k7-cq4-cs4096/exl3-dflash2-k7-cq4-cs4096-code-0.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k7-cq4-cs4096/exl3-dflash2-k7-cq4-cs4096-code-1.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k7-cq4-cs4096/exl3-dflash2-k7-cq4-cs4096-code-1.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k7-cq4-cs4096/exl3-dflash2-k7-cq4-cs4096-code-2.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k7-cq4-cs4096/exl3-dflash2-k7-cq4-cs4096-code-2.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k7-cq4-cs4096/exl3-dflash2-k7-cq4-cs4096-json-0.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k7-cq4-cs4096/exl3-dflash2-k7-cq4-cs4096-json-0.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k7-cq4-cs4096/exl3-dflash2-k7-cq4-cs4096-json-1.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k7-cq4-cs4096/exl3-dflash2-k7-cq4-cs4096-json-1.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k7-cq4-cs4096/exl3-dflash2-k7-cq4-cs4096-json-2.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k7-cq4-cs4096/exl3-dflash2-k7-cq4-cs4096-json-2.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k7-cq4-cs4096/exl3-dflash2-k7-cq4-cs4096-prose-0.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k7-cq4-cs4096/exl3-dflash2-k7-cq4-cs4096-prose-0.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k7-cq4-cs4096/exl3-dflash2-k7-cq4-cs4096-prose-1.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k7-cq4-cs4096/exl3-dflash2-k7-cq4-cs4096-prose-1.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k7-cq4-cs4096/exl3-dflash2-k7-cq4-cs4096-prose-2.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k7-cq4-cs4096/exl3-dflash2-k7-cq4-cs4096-prose-2.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k7-cq4-cs4096/exl3-dflash2-k7-cq4-cs4096.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-dflash2-k7-cq4-cs4096/exl3-dflash2-k7-cq4-cs4096.summary.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-git-import-and-template.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-mtp-benchmark.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-mtp-k4-cq4-cs4096/exl3-mtp-k4-cq4-cs4096-code-0.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-mtp-k4-cq4-cs4096/exl3-mtp-k4-cq4-cs4096-code-0.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-mtp-k4-cq4-cs4096/exl3-mtp-k4-cq4-cs4096-code-1.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-mtp-k4-cq4-cs4096/exl3-mtp-k4-cq4-cs4096-code-1.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-mtp-k4-cq4-cs4096/exl3-mtp-k4-cq4-cs4096-code-2.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-mtp-k4-cq4-cs4096/exl3-mtp-k4-cq4-cs4096-code-2.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-mtp-k4-cq4-cs4096/exl3-mtp-k4-cq4-cs4096-json-0.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-mtp-k4-cq4-cs4096/exl3-mtp-k4-cq4-cs4096-json-0.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-mtp-k4-cq4-cs4096/exl3-mtp-k4-cq4-cs4096-json-1.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-mtp-k4-cq4-cs4096/exl3-mtp-k4-cq4-cs4096-json-1.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-mtp-k4-cq4-cs4096/exl3-mtp-k4-cq4-cs4096-json-2.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-mtp-k4-cq4-cs4096/exl3-mtp-k4-cq4-cs4096-json-2.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-mtp-k4-cq4-cs4096/exl3-mtp-k4-cq4-cs4096-prose-0.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-mtp-k4-cq4-cs4096/exl3-mtp-k4-cq4-cs4096-prose-0.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-mtp-k4-cq4-cs4096/exl3-mtp-k4-cq4-cs4096-prose-1.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-mtp-k4-cq4-cs4096/exl3-mtp-k4-cq4-cs4096-prose-1.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-mtp-k4-cq4-cs4096/exl3-mtp-k4-cq4-cs4096-prose-2.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-mtp-k4-cq4-cs4096/exl3-mtp-k4-cq4-cs4096-prose-2.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-mtp-k4-cq4-cs4096/exl3-mtp-k4-cq4-cs4096.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-mtp-k4-cq4-cs4096/exl3-mtp-k4-cq4-cs4096.summary.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-runner-before-gpu.py`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-runner-config-guard.diff`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/exl3-suite-summary.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-bench/run_exl3_bench.sh`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-cpu-install.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-deployment-notes.md`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-git-import-and-template.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-model-downloads.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/exl3-pip-freeze.txt`
- `assets/g4090-qwen38-benchmark-2026/supplementary/git-clone-provenance-exl3-hyperqwen.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/install_exl3_cpu.sh`
- `assets/g4090-qwen38-benchmark-2026/supplementary/qwen38-cinference.service`
- `assets/g4090-qwen38-benchmark-2026/supplementary/qwen38-config.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/qwen38-model-api.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/build-env.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/cinference-benchmark-matched-k3-k7.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/cinference-benchmark-matched.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/cinference-benchmark.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/cinference-build.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/cinference-configure.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/cinference-service.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/cinference-service.requests.jsonl`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/cinference-unpack.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/gguf-download.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/gguf-mtp-download.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/llama-benchmark-matched.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/llama-build.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/llama-configure.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/llama-source-download.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/model-download-mirror.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/model-download.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/model-v3-conversion.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/ninfer-benchmark-matched-k5.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/ninfer-benchmark-matched.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/ninfer-build.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/ninfer-configure.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/primary-audit-current.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/primary-audit-final-http.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/runner-timewait-guard-test.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/service-verification-final.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/service-verification.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/logs/zlib-install.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/build-env-explicit.txt`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/cinference-help.txt`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/cinference-server-help.txt`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/cmake-build-provenance.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/cuda-toolkit.txt`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/gguf-mtp-sha256.txt`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/gguf-sha256.txt`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/git-clone-provenance-exl3-hyperqwen.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/gpu-hardware.csv`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench/cinference-int8-k0.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench/cinference-int8-k0.requests.jsonl`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench/cinference-int8-k0.server.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench/cinference-int8-k0.summary.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench/cinference-int8-k3.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench/cinference-int8-k3.requests.jsonl`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench/cinference-int8-k3.server.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench/cinference-int8-k3.summary.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench/cinference-int8-k7.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench/cinference-int8-k7.requests.jsonl`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench/cinference-int8-k7.server.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench/cinference-int8-k7.summary.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench/cinference-int8.runs.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/cinference-int8-k0.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/cinference-int8-k0.requests.jsonl`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/cinference-int8-k0.runs.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/cinference-int8-k0.server.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/cinference-int8-k0.summary.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/cinference-int8-k3.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/cinference-int8-k3.requests.jsonl`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/cinference-int8-k3.server.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/cinference-int8-k3.summary.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/cinference-int8-k7.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/cinference-int8-k7.requests.jsonl`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/cinference-int8-k7.server.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/cinference-int8-k7.summary.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/cinference-int8.runs.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/llama-udq4-k0.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/llama-udq4-k0.server.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/llama-udq4-k0.summary.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/llama-udq4-k3.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/llama-udq4-k3.server.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/llama-udq4-k3.summary.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/llama-udq4-k7.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/llama-udq4-k7.server.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/llama-udq4-k7.summary.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/llama-udq4.runs.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/ninfer-erik-int8-k0-k3-k7.runs.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/ninfer-erik-int8-k0.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/ninfer-erik-int8-k0.requests.jsonl`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/ninfer-erik-int8-k0.server.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/ninfer-erik-int8-k0.summary.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/ninfer-erik-int8-k3.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/ninfer-erik-int8-k3.requests.jsonl`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/ninfer-erik-int8-k3.server.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/ninfer-erik-int8-k3.summary.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/ninfer-erik-int8-k5.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/ninfer-erik-int8-k5.requests.jsonl`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/ninfer-erik-int8-k5.server.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/ninfer-erik-int8-k5.summary.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/ninfer-erik-int8-k7.server.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/http-bench-matched/ninfer-erik-int8.runs.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/llama-bench-help.txt`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/llama-git-clone.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/llama-server-help.txt`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/ninfer-v2-sha256.txt`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/ninfer-v3-payload-verification.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/ninfer-v3-sha256.txt`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/official-commit-fetch-validation.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/official-commit-fetch-validation.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/primary-benchmark-audit.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/qwen38-cinference-4090-git-status-after-20260930T211550Z.txt`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/qwen38-cinference-4090-git-status-before-20260930T211550Z.txt`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/qwen38-cinference-4090-independent-git-clone-20260930T211550Z.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/qwen38-cinference-4090-removed-appledouble-20260930T211550Z.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/qwen38-ninfer-4090-git-status-after-20260930T211550Z.txt`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/qwen38-ninfer-4090-git-status-before-20260930T211550Z.txt`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/qwen38-ninfer-4090-independent-git-clone-20260930T211550Z.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/qwen38-ninfer-4090-removed-appledouble-20260930T211550Z.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/remote-git-clones-ninfer.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/service-verification/anthropic.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/service-verification/binary-and-unit.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/service-verification/code.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/service-verification/final-systemd-state.txt`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/service-verification/json.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/service-verification/manager-state.txt`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/service-verification/responses-schema-correction.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/service-verification/responses.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/service-verification/stream.sse`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/service-verification/summary.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/tabby-base-install.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/tabby-base-install.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/tabby-cpu-pycompile/backends_exllamav3_model.pyc`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/tabby-cpu-pycompile/common_args.pyc`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/tabby-cpu-pycompile/common_config_models.pyc`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/tabby-cpu-pycompile/main.pyc`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/tabby-dflash2-http-preparation.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/tabby-git-clone.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/tabby-git-clone.log`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/tabby-pip-freeze-after.txt`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/tabby-pip-freeze-before.txt`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/tabby-pip-plan.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/tabby-preserve-engine-constraints.txt`
- `assets/g4090-qwen38-benchmark-2026/supplementary/run_exl3_bench.sh`
- `assets/g4090-qwen38-benchmark-2026/supplementary/run_llama_modes.py`
- `assets/g4090-qwen38-benchmark-2026/supplementary/run_ninfer_modes.py`
- `assets/g4090-qwen38-benchmark-2026/supplementary/run_qwen38_service.sh`
- `assets/g4090-qwen38-benchmark-2026/supplementary/service_ctl.sh`
- `assets/g4090-qwen38-benchmark-2026/supplementary/tabby-http-preparation/README.md`
- `assets/g4090-qwen38-benchmark-2026/supplementary/tabby-http-preparation/dflash2-benchmark.yml`
- `assets/g4090-qwen38-benchmark-2026/supplementary/tabby-http-preparation/launch_dflash2_http.sh`
- `assets/g4090-qwen38-benchmark-2026/supplementary/verify_container_payload.py`
- `assets/g4090-qwen38-benchmark-2026/supplementary/verify_qwen38_service.py`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/service-verification/final-reconnect-and-cli.json`
- `assets/g4090-qwen38-benchmark-2026/supplementary/remote-evidence/results/service-verification/stopped-at-user-request.json`

### hyperqwen-2026

[[research/llm-inference/assets/hyperqwen-2026/note]]；[来源快照](../assets/hyperqwen-2026/citation.bib)。

- `assets/hyperqwen-2026/supplementary/github-api-commit.json`
- `assets/hyperqwen-2026/supplementary/github-api-repository.json`

### ik-llama-cpp-2026

[[research/llm-inference/assets/ik-llama-cpp-2026/note]]；[来源快照](../assets/ik-llama-cpp-2026/citation.bib)。

- `assets/ik-llama-cpp-2026/supplementary/github-api-commit.json`
- `assets/ik-llama-cpp-2026/supplementary/github-api-repository.json`

### llama-cpp-2026

[[research/llm-inference/assets/llama-cpp-2026/note]]；[来源快照](../assets/llama-cpp-2026/citation.bib)。

- `assets/llama-cpp-2026/supplementary/github-api-commit.json`
- `assets/llama-cpp-2026/supplementary/github-api-repository.json`

### ninfer-4090-2026

[[research/llm-inference/assets/ninfer-4090-2026/note]]；[来源快照](../assets/ninfer-4090-2026/citation.bib)。

- `assets/ninfer-4090-2026/supplementary/github-api-commit.json`
- `assets/ninfer-4090-2026/supplementary/github-api-repository.json`
- `assets/ninfer-4090-2026/supplementary/landscape-github-observations.json`

### ninfer-4090-windows-2026

[[research/llm-inference/assets/ninfer-4090-windows-2026/note]]；[来源快照](../assets/ninfer-4090-windows-2026/citation.bib)。

- `assets/ninfer-4090-windows-2026/supplementary/github-api-commit.json`
- `assets/ninfer-4090-windows-2026/supplementary/github-api-repository.json`
- `assets/ninfer-4090-windows-2026/supplementary/jgamboa-model-README.md`
- `assets/ninfer-4090-windows-2026/supplementary/jgamboa-model-info.json`

### ninfer-all-2026

[[research/llm-inference/assets/ninfer-all-2026/note]]；[来源快照](../assets/ninfer-all-2026/citation.bib)。

- `assets/ninfer-all-2026/supplementary/github-api-commit.json`
- `assets/ninfer-all-2026/supplementary/github-api-repository.json`
- `assets/ninfer-all-2026/supplementary/wavecut-gsq-model-README.md`
- `assets/ninfer-all-2026/supplementary/wavecut-gsq-model-info.json`

### qwen38-4090-paper-search-2026

[[research/llm-inference/threads/qwen38-4090-paper-search-2026]]；[来源快照](../assets/qwen38-4090-paper-search-2026/citation.bib)。

- `assets/qwen38-4090-paper-search-2026/supplementary/qwen38-paper-search-installed.log`
- `assets/qwen38-4090-paper-search-2026/supplementary/qwen38-paper-search-researchstudio.log`
- `assets/qwen38-4090-paper-search-2026/supplementary/qwen38-paper-search-researchstudio-py311.log`

### tokenspeed-2026

[[research/llm-inference/assets/tokenspeed-2026/note]]；[来源快照](../assets/tokenspeed-2026/citation.bib)。

- `assets/tokenspeed-2026/supplementary/github-api-commit.json`
- `assets/tokenspeed-2026/supplementary/github-api-repository.json`
- `assets/tokenspeed-2026/supplementary/web-extraction-2026-10-01.txt`

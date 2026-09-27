---
title: IMAX：Efficient Kernel Mapping and Comprehensive System Evaluation of LLM Acceleration
  on a CGLA
domain: research
area: fpga-llm-inference
type: paper
status: active
updated: '2026-09-15'
tags:
- paper
- fpga
- verified-arxiv
---

# IMAX：Efficient Kernel Mapping and Comprehensive System Evaluation of LLM Acceleration on a CGLA

## 论文身份与资产

Takuto Ando、Yu Eto、Ayumu Takeuchi、Yasuhiko Nakashima；2025。公开 [arXiv:2512.00335v1](https://arxiv.org/abs/2512.00335v1)，PDF 首页注明 IEEE Access DOI [10.1109/ACCESS.2025.3636266](https://doi.org/10.1109/ACCESS.2025.3636266)，received 2025-10-08 / accepted 2025-11-19。

[PDF（17 页）](paper-pdf/2512.00335v1.pdf) · [TeX 主文件](paper-tex/extracted/2512.00335v1/main.tex) · [元数据及哈希](metadata.yaml) · [官方仓库缓存](github-repo/IMAX3-LLM/README.md)。论文 Data Availability 明确链接 Takuto-Ando/IMAX3-LLM，仓库标题相符，身份匹配成立。

## 问题与方法

在通用线性粗粒度阵列 IMAX 上映射 llama.cpp 的 dot-product，兼顾量化解包、局部存储容量与 host/DMA 开销。CPU 负责分词、embedding、KV 管理、RMSNorm/RoPE/softmax，FPGA 承担线性层、attention/FFN 中的点积。它是实际框架集成先例，但不是完整模型和状态全部常驻 FPGA 的系统。

方法节 `proposed.tex`：FP16、Q8_0、Q3_K、Q6_K 映射；Q3_K 使用 CVT53 将 6-bit scale 近似转为 5-bit。相同 GGUF 文件不保证计算逐位等价；作者认为精度损失可忽略，尚不能替代独立模型质量实验。输入合并减少小 DMA，论文报告 LOAD 1.2×、DRAIN 4.8×（相对 naive）。LMM 容量决定可卸载的形状与比例。

## 论文实验与边界

实验节 `experiments_and_results.tex` 与讨论节：VPK180、145 MHz、双核 Cortex-A72、PetaLinux、Vivado 2024.1。硬件最多 8 lanes，主评测用 2 lanes；图中四板装置不等于每个结果均用四板。Qwen3 0.6B/1.7B/8B，Q8_0/Q3_K_S，54 workloads，输入/输出组合 [8:1] 到 [32:16]，每项 10 次，作者报告标准差低于 3%。仅证明同一模型家族多个规模。

讨论中 Qwen3-0.6B Q3_K_S [32:16] 的 FPGA 总时间 16.3 s：compute 4.47、CPU 5.43、load 5.31、drain 0.31、configuration 0.78 s。主机和搬运不能从请求指标里删掉。论文将 E2E 定义为 prompt 到首 token，却同时改变输出长度并讨论完整执行 breakdown；**TTFT 与整请求计时口径有歧义，不能直接换算 decode token/s**。

28 nm ASIC 的 840 MHz 为综合/时序投影，功耗采用 10% switching activity；GPU/CPU 使用 TDP。44.4× PDP、11.5× EDP 是 ASIC 投影结果，不是 FPGA 实测加速或实测整机能效。论文也报告 RTX 4090 在其 latency 比较中最快。

## 源码观察

官方仓库 main commit `ecf4b7590734b123d4004d16251979c66f6adcdf`，完整浅克隆，无 submodule。定向检查 README、`ggml/src/ggml-cpu/ggml-cpu.c`、`ggml/include/ggml-imax.h`、`imax.c`、backend registry / CMake。

`ggml-cpu.c` 的 `HANDLE_GGML_TYPE` 和 MatMul chunk 分支直接调用 `imax_compute_forward_mul_mat_one_chunk_*`；有 `s_use_cpu` 门控和 OTHER_ARM 分支。应标为 **CPU backend 内嵌 FPGA offload**，本次未发现独立 IMAX device/backend 注册。不能推成 zero fallback。头文件提供 DMA map 和线程参数。

README 提到的 `scripts/load_bitstream.sh` / `src/kernels/` 未在本次树中找到；`imax.c` 引用仓库外 `../../src/conv-c2d/emax7.h` 等依赖。未验证 README 构建命令可直接复现。README 的 44.4× 描述缺少论文的 ASIC 投影限定，应以正文为准。

## 对本项目的意义

和 [[research/fpga-llm-inference/papers/secda-llm-2024/index|SECDA]] 一起，否定“首次在 llama.cpp 内进行 FPGA 加速”的宽泛首创表述。可比较的是同正确性条件下逐算子卸载与整图执行、host-managed KV 与 device-resident KV 的搬运/调用/请求耗时；不能凭接口形式或未对齐 token/s 声称优势。

## 阅读与复现

已读 v1 全部 substantive TeX sections、讨论、结论和 bibliography；核验 PDF 首页身份，源码定向审查。没有构建、运行仓库、综合或板上复现。回到 [[research/fpga-llm-inference/index]]。

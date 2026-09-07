---
title: Vitis AI DPU、FINN 与 PYNQ：FPGA 推理工具链对照
domain: research
area: fpga-llm-inference
type: comparison
status: active
updated: 2026-09-07
tags: [fpga, vitis-ai, dpu, finn, pynq, quantization, overlay, dataflow]
---

# Vitis AI DPU、FINN 与 PYNQ

## 名称与范围

本页回应“Vitis 的 DPU 和 pinn 是否与 FPGA 推理相关”。用户所指的 `pinn` 尚未确认：结合 DPU 语境，**FINN** 和 **PYNQ** 都是合理候选；字面上的 **PINN** 则是另一类研究。这里保留歧义，分别登记。

| 名称 | 层次与含义 | 与本领域的关系 |
|---|---|---|
| Vitis / Vitis HLS | FPGA 软件开发、硬件综合与集成工具 | 当前 XRT kernel 路径与 FINN 都可能使用它们；使用 Vitis 不等于使用 DPU |
| Vitis AI | 包含模型量化、编译、IP、运行时和示例的推理工具链 | 本页重点核对其 v3.5 DPU 路线 |
| DPU | 此处是 Deep Learning Processing Unit，具有目标相关 ISA 的推理引擎 | shared-engine / 可编程 overlay 的产业参考 |
| FINN | AMD Research 的量化网络 FPGA 编译框架 | 为网络生成定制 streaming dataflow 硬件，是空间映射与层内时间复用的参考 |
| PYNQ | Python 驱动、硬件 overlay 与板卡软件生态 | 可以控制 DPU，也可以控制 FINN 生成的硬件；自身不定义神经网络计算架构 |
| PINN / PINNs | Physics-Informed Neural Networks，将物理方程约束纳入学习 | 属于模型/科学计算方法；不能由名称推断成 FPGA LLM 编译框架 |

DPU 与 FINN 的互补关系由 AMD 的 DPU 集成文档直接说明；PYNQ 与两者的连接分别可由 DPU-PYNQ 和 FINN 的生成驱动验证。[S1][S5][S8][S10][S11]

## Vitis AI DPU：复用硬件，编译模型指令

在核对的 v3.5 文档中，DPU 是带有自身 ISA 的微码处理器，内部包含面向不同任务的异构 processing engines。对兼容网络，更换模型主要是更换编译后的程序和权重，不需要为每个网络重新生成 bitstream。**这是一种受具体算子、形状和 ISA 约束的可编程性**；不意味着任意 GGML 节点都能执行。[S1]

```text
训练模型 -> 量化 -> 目标 arch.json + Vitis AI Compiler
                  -> XIR 图划分 + DPU 指令 -> .xmodel
                  -> VART 提交与完成 -> 已集成 DPU 的硬件平台
```

需要保留的工程事实：

- **编译目标是契约的一部分。** `arch.json` 描述特定 DPU 架构，编译产物与目标不匹配会导致运行时错误；不能只检查 `.xmodel` 文件存在。[S2]
- **量化器能力不等于 DPU 能力。** v3.5 文档描述的通用 CNN DPU 路线主要使用 INT8；量化工具列出的 FP16、BFP 或 matmul 支持不能单独证明目标 IP 支持相应模型。[S2][S4]
- **图划分必须可见。** Model Inspector 检查算子及其排列；WeGO/ONNX Runtime 路径可以把不适合 DPU 的子图交给 CPU。对当前 strict GGML 项目，必须分别审计原先接受的算子是否仍在设备执行，以及未支持部分如何处理。[S2]
- **异步接口是参考，实际 launch 数仍需测量。** VART 支持异步作业提交与回收、C++/Python 和多线程；一个高层作业对应多少底层提交，不能由 API 名称推断。[S3]
- **开源边界需要逐组件核对。** v3.5 文档明确说明编译器未提供源码；不能把 GitHub 仓库的 Apache-2.0 标识解释成整个工具链和所有 IP 均可修改。[S2]

### 目标板与版本边界

| 已核对对象 | 官方描述 | 对 U280 项目的含义 |
|---|---|---|
| DPUCZDX8G | Zynq UltraScale+ MPSoC / Kria K26 的 PL 推理 IP | KV260/ZCU104 的部署教程不是 U280 现成部署包 |
| DPUCV2DX8G | 面向带 AI-ML tiles 的 Versal，文档列出 VEK280、V70 等 | `VEK280` 与 `Alveo U280` 是不同平台，不能因编号相似混用 |
| Vitis AI v3.5 | 需按具体 IP 核对工具版本；release notes 给出 2023.1 的兼容说明，部分成熟 IP 没有更新参考设计 | 固定 IP、工具、platform 和 runtime 的完整组合，不能只写“最新版 Vitis AI” |

上述资料**没有建立 U280 上 Gemma 3 1B / GGML 的现成完整部署证据**。这是本轮证据的限制，不是对所有历史 DPU、第三方移植或未来产品的“不支持”断言。本页固定讨论 v3.5 文档，不把它描述成 2026 年所有 AMD AI 产品的最新功能清单。[S1][S4]

## FINN：定制 Dataflow 与层内 Folding

FINN 官方定位是实验性的量化网络 FPGA 框架，强调为各网络生成定制 dataflow 架构。当前文档给出的典型路径是：[S5][S6][S7][S8]

```text
Brevitas 量化模型 -> QONNX -> FINN-ONNX
    -> streamlining / HW layer 转换 / dataflow partition
    -> HLS 或 RTL 实现选择 + PE/SIMD folding
    -> DMA / 位宽转换 / FIFO / IP 拼接
    -> bitstream 与生成驱动 -> 板卡执行
```

它对 [[research/fpga-llm-inference/execution-architecture-taxonomy]] 的价值在于：网络层之间可以空间分配、通过 FIFO 连接，而每层内部仍用 folding 复用计算资源。**层内时间复用与层间空间 dataflow 可以同时存在**；FINN 不宜被简单标成“完全展开、无复用”。[S7][S8]

| 机制 | 可借鉴内容 | 对 LLM 的未解决问题 |
|---|---|---|
| QONNX / FINN-ONNX | 把量化语义、硬件转换与模型验证串联 | ONNX 输入不意味着任意 Transformer 可直接编译 |
| PE / SIMD folding | 用层内并行度换资源与吞吐，平衡流水级 | prefill 与 decode 的最优配置可能不同 |
| FIFO / DWC / DMA | 显式建模流间连接、位宽转换和外存入口 | 动态序列长度、KV cache 和 GGML 可观察边界仍需设计 |
| 参数 memory modes | 区分硬件内嵌常量、独立权重流和 external 参数流 | 外部权重端口不自动提供 U280 HBM bank 分配或完整 LLM 权重管理 |
| 生成 PYNQ driver | 把 tensor packing、数据搬运和执行形成可复现部署接口 | Python demo 的吞吐边界不同于原生 `llama-bench pp/tg` |

表中“可借鉴内容”来自官方设计文档，“未解决问题”是针对本项目的分析。[S6][S7][S8][S9]

几个容易误读的限制：

- **支持的硬件层与图模式有限。** FAQ 明确不支持把任意 ONNX Model Zoo 模型直接转成 FPGA accelerator；自定义层需要补实现。当前文档已有新增 HLS/RTL 层和目标限制，不能把历史上“FINN 只做二值 CNN”的描述当作完整现状。[S12]
- **避免给出统一位宽上限。** FAQ 同时保留“较高位宽/大网络资源代价高”的说明与 1–8 bit 建议；应核对具体层、backend、目标器件和综合结果，而不是宣称所有层均只能低于 4 bit。[S12]
- **网络定制不等于权重永远写死。** `internal_embedded` 将参数作为常量综合；`internal_decoupled` 分离权重存储和计算；`external` 可运行时输入参数，但 memory-mode 文档标记其为 experimental / limited support。能换兼容权重不等于能执行任意新拓扑。[S9]
- **示例支持与编译器可移植性分开。** 已核对的 `finn-examples` 预构建 Alveo 平台为 U250，同时提供 Zynq 示例；生成 IP 后可做其他板卡集成，但本轮没有实测 U280 部署，也未验证完整 Gemma 自回归推理。[S10]

基础论文已登记为阅读入口，本文未以其性能数字做跨模型比较：

1. [FINN: A Framework for Fast, Scalable Binarized Neural Network Inference](https://arxiv.org/abs/1612.07119)，FPGA 2017：早期二值网络到定制硬件的基础工作。
2. [FINN-R: An End-to-End Deep-Learning Framework for Fast Exploration of Quantized Neural Networks](https://arxiv.org/abs/1809.04570)，TRETS 2018：量化网络设计探索的后续框架。

题名、年份、出版入口通过官方 README 与 publication list 核对；本轮为官方工具链文档调研，未完成这两篇论文全文深读。[S5][S14]

## PYNQ 与字面上的 PINN

**PYNQ 是部署生态。** FINN 可生成使用 PYNQ API 的 Python driver；DPU-PYNQ 则把 Vitis AI DPU 放进 overlay，提供 `.bit`、`.hwh`、`.xclbin` 与 notebook 示例。因此 PYNQ 可以承载不同计算架构。PYNQ 文档中的 overlay 常指可加载的硬件设计包，不应自动等同于架构论文中的“可编程 overlay processor”。[S8][S10][S11]

**DPU-PYNQ 是历史参考。** 2026-09-07 核对时，官方 README 标记项目已归档、不再积极开发，GitHub API 的 `archived` 也为 `true`；README 对应 PYNQ 3.0 与 Vitis AI 2.5.0。它适合理解部署组件关系，不能把该版本组合直接套到 Vitis AI 3.5 或 U280。[S11]

**PINN 是模型方法。** 原作者项目用神经网络求解/发现偏微分方程，并把物理约束用于学习；基础论文为 Raissi、Perdikaris、Karniadakis 的 JCP 2019 工作。若用户实际指 PINN，需要另按具体 FPGA 论文核对训练、导数计算或前向推理的加速边界。本轮未确认一篇特定的 FPGA PINN 工作，暂不把它加入 LLM 系统性能表。[S13]

## 对当前 GGML / U280 主线的启发

以下是基于资料与 [[research/fpga-llm-inference/project-status-2026-07]] 的分析，并非新板卡测量：

1. **将 DPU 作为共享引擎的先例。** “一份硬件运行多份已编译网络程序”已有成熟先例。未来贡献必须解释 GGML support/failure contract、可观察边界或 HBM residency 的具体改进，不能仅以 shared engine 命名为创新。
2. **将 FINN 作为流式构建与验证的参考。** 优先读 folding、FIFO、参数流、生成驱动，研究它们如何支撑 coarse execution；这比直接把完整 Gemma F16 导入 FINN 更能回答当前 launch/wait 瓶颈。
3. **建立具体覆盖矩阵再讨论替换。** 对目标版本逐项检查 `MUL_MAT`、RMSNorm、RoPE、softmax、GLU、KV 读写、dtype 与 shape；记录实际编译分区、CPU 执行部分和 artifact identity。
4. **保留统一测量边界。** 若后续做原型，应分别记录编译/bitstream 成本、packing/DMA、设备计算、host wait 与完整 pp/tg 时间；不能把 CNN samples/s 当成 LLM token/s。

建议阅读顺序：DPU 架构与模型编译 [S1–S2] -> FINN 网络准备、构建、memory modes [S7–S9] -> VART 与 PYNQ 部署 [S3][S10–S11] -> 两篇 FINN 基础论文。与 [[research/fpga-llm-inference/system-landscape]] 中 DFX、StreamTensor、CODO 的 LLM 系统证据配合阅读。

## 一手资料与检索记录

访问日期：2026-09-07。搜索工具两次返回 HTTP 503，随后直接读取官方 GitHub raw 文档、项目 publication page 和 GitHub API。结论仅覆盖下列已读取资料，不宣称完成全网穷尽检索。FINN 文档核对时 `main` 的 commit 为 `38c42bf95abbdad493db0b0f5053060074698908`；以下 FINN 文档链接固定到该版本。未下载或验证 bitstream，未安装工具链，未运行板卡实验。

| ID | 官方资料 | 用途 / 核对范围 |
|---|---|---|
| S1 | [Vitis AI v3.5 DPU IP and System Integration](https://github.com/Xilinx/Vitis-AI/blob/v3.5/docsrc/source/docs/workflow-system-integration.rst) | ISA、硬件复用、FINN 对照和 IP/平台表 |
| S2 | [Vitis AI v3.5 Developing a Model](https://github.com/Xilinx/Vitis-AI/blob/v3.5/docsrc/source/docs/workflow-model-development.rst) | Inspector、INT8、XIR、arch.json、CPU 分区和编译器源码边界 |
| S3 | [Vitis AI v3.5 Deploying a Model](https://github.com/Xilinx/Vitis-AI/blob/v3.5/docsrc/source/docs/workflow-model-deployment.rst) | VART 异步作业、XRT、whole-application 边界 |
| S4 | [v3.5 Release Notes](https://github.com/Xilinx/Vitis-AI/blob/v3.5/docsrc/source/docs/reference/release_notes.rst)；[Version Compatibility](https://github.com/Xilinx/Vitis-AI/blob/v3.5/docsrc/source/docs/reference/version_compatibility.rst) | 工具版本与未更新的成熟 IP |
| S5 | [FINN README](https://github.com/Xilinx/finn/blob/38c42bf95abbdad493db0b0f5053060074698908/README.md) | 框架定位、Docker 与基础论文元数据 |
| S6 | [Brevitas Export](https://github.com/Xilinx/finn/blob/38c42bf95abbdad493db0b0f5053060074698908/docs/finn/brevitas_export.rst) | QONNX 到 FINN-ONNX |
| S7 | [Network Preparation](https://github.com/Xilinx/finn/blob/38c42bf95abbdad493db0b0f5053060074698908/docs/finn/nw_prep.rst) | streamlining、HW 分区、backend 选择与 folding |
| S8 | [Hardware Build and Deployment](https://github.com/Xilinx/finn/blob/38c42bf95abbdad493db0b0f5053060074698908/docs/finn/hw_build.rst) | driver、DMA、DWC、FIFO、硬件集成 |
| S9 | [Memory Modes](https://github.com/Xilinx/finn/blob/38c42bf95abbdad493db0b0f5053060074698908/docs/finn/reference/mem-modes.rst) | 参数流、常量、运行时权重与 external 限制 |
| S10 | [FINN Examples](https://github.com/Xilinx/finn-examples/blob/main/README.md) | PYNQ 驱动、U250/Zynq 示例与版本组合 |
| S11 | [PYNQ](https://github.com/Xilinx/PYNQ/blob/master/README.md)；[DPU-PYNQ](https://github.com/Xilinx/DPU-PYNQ/blob/master/README.md) | Python/overlay 生态、DPU-PYNQ 归档状态与 2.5.0 依赖 |
| S12 | [FINN FAQ](https://github.com/Xilinx/finn/blob/38c42bf95abbdad493db0b0f5053060074698908/docs/finn/faq.rst) | ONNX、位宽、层支持、FIFO sizing 与目标集成限制 |
| S13 | [PINNs 作者仓库](https://github.com/maziarraissi/PINNs/blob/master/README.md) | 名称消歧、物理方程问题与 JCP 2019 论文入口 |
| S14 | [FINN Publications](https://xilinx.github.io/finn/publications) | FINN / FINN-R 官方论文链接 |

返回 [[research/fpga-llm-inference/index]]。

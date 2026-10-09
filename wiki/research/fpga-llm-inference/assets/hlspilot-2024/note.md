---
title: "HLSPilot: LLM-based High-Level Synthesis"
updated: 2026-10-09
---

# HLSPilot: LLM-based High-Level Synthesis

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文 + 参考文献，约 7 页 arXiv 版）。Fig. 1–4 的文字内容被抽取成乱序文本，但可辨认；表格 I–IV 可读；无附录。

## Summary

问题：直接由自然语言生成 RTL 语义鸿沟大、只适用于小模块；而 HLS 代码质量依赖专家经验，pragma 参数空间大。HLSPilot 的思路是让 LLM 只做 C/C++ 到 HLS C 的转换，再由 HLS 工具产出 RTL，并把整个 CPU-FPGA 加速流程交给 LLM 驱动（§I, §III-A）。

流程五步（Fig. 1）：
1. 用 gprof 对 CPU 程序做 profiling，由 LLM 读报告选出耗时 kernel。
2. Program-tree-based task pipelining（Algorithm 1）：LLM 迭代地把 kernel 拆成子任务（非循环按语句功能拆；循环按最小可并行粒度拆），给了四类拆分示例（按迭代、按前后半段、按循环层级、多层循环合为一个任务），拆完后用 dataflow/stream 连接。重构后的代码对照原代码的输出做自底向上（从叶子节点开始）的正确性测试，多次失败则回退到父节点（§III-B）。
3. LLM-based HLS 优化（§III-C）：从 Xilinx 文档（UG902/UG1270/UG1399）抽取结构化策略库（简介、适用场景、参数说明、示例），用 RAG 式检索按代码内容选策略，再把描述和示例放进 prompt 做 in-context learning。
4. LLM 从 HLS 代码中提取参数，生成脚本调用外部 DSE 工具 GenHLSOptimizer 调 II、unroll factor、partition size。
5. 让 LLM 学习 XRT API，生成 host 代码并把 kernel 替换为 FPGA 调用。

实验（§IV）：默认 GPT-4，Vitis HLS，Alveo U280。基准由改造的 Rosetta（从 SDSoC 移植到 Vitis，并补写未优化版本）加若干手工收集的经典算法组成，共 9 个应用。Table I 给出 original / handcrafted / HLSPilot / HLSPilot+DSE 的运行时间（ms）。例如 Merge Sort 786.6 / 54.9 / 47.6 / 47.5；PageRank 1862 / 1255 / 1115 / 1051；BFS 5019 / 3974 / 4184 / 3830；Fir 0.413 / 0.279 / 0.245 / 0.227。在 Fir、Merge Sort、BFS(+DSE)、PageRank 上 HLSPilot 与人工相当或更快。

案例（§IV-D）：L-BFGS，cost calculation 占总时间 99.1%。Table III：CPU 总时间 18390 s，浮点设计 2365 s（7.78x），定点设计 1541 s（11.93x）；cost 部分 18237 s 降到 855 s / 31 s（21.33x / 588.29x）。Table IV 给出 kernel 资源：FXP 版 188294 LUT、624 DSP，单次 cost 计算 60.98 ms，CPU 为 38529 ms。

## Evidence and Limits

- 摘要称"comparable performance in general and can even outperform manual"。Table I 显示并非处处如此：Digit Recognition 手工 9.892 ms 对 HLSPilot 78.837 ms（+DSE 52.832）；Spam Filter 手工 37.3 ms 对 HLSPilot 8014 ms（+DSE 7519），几乎没有得到加速；Face Detection、Optical Flow 也慢于手工。文中解释为 task 划分不如专家合理、LLM 难以实现 LUT 化 sigmoid 这类场景特定优化（§IV-C），但没有定量分析。
- "超过手工"的结果限于少数应用，且多数含 DSE；手工版本是否同样经过 DSE 调参未说明，比较的公平性不清楚。
- 只有单次运行的运行时间，没有多次采样、成功率、LLM 调用失败/重试次数、生成 token 开销或人工介入程度的统计，"fully automate"的程度无法从证据判断。
- 没有消融：未单独评估 task pipelining、策略检索、DSE 各自的贡献；也未与其他 LLM 或无 RAG 的基线对比。
- Table II 只是定性列出手工与 HLSPilot 所用的优化类别，"基本覆盖专家所选策略"属于人工观察。
- 基准是作者自建的，未优化版本也是作者写的，规模为 9 个应用；L-BFGS 案例仅一个算法。案例中的 7.79x（正文）与 Table III 的 7.78x 略有出入。
- 摘要说 LLM 在 profiling、分区、代码生成、工具使用全程参与，但 profiling 工具、DSE 工具和正确性测试是外部固定组件；正确性仅靠输出对比测试，无形式化验证。
- 代码在 GitHub 公开（脚注 1）；论文未给出 prompt 全文、策略库规模和 GPT-4 具体版本，复现依赖仓库。

## Open Questions

- 在 Digit Recognition、Spam Filter 等落后明显的应用上，失败原因是任务拆分、策略选择还是数据类型/查表优化？论文没有给出诊断。
- 流程中 LLM 的随机性对结果的影响（同一 kernel 多次生成的方差、重构失败后回退到父节点的频率）未报告。
- 策略库和 in-context 示例是否会因基准与文档示例重合而偏乐观（例如 Rosetta 应用本身可能出现在 GPT-4 训练数据中）。

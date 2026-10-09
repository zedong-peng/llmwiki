---
title: "RTLRewriter: Methodologies for Large Models aided RTL Code Optimization"
updated: 2026-10-09
---

# RTLRewriter: Methodologies for Large Models aided RTL Code Optimization

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文 + 参考文献）。图表由文本提取，Figure 1–7 仅有零散文字；无附录。数据库构建细节论文自称因篇幅省略。

## Summary

论文提出 RTLRewriter，用大模型（GPT-4V，经 Poe 调用）对 RTL 代码做面向综合结果（wires/cells、area/delay）的优化重写，称为首个 LLM 辅助的 RTL 优化框架（§1）。框架由五部分组成：

- 电路划分（§3.1）：把设计解析成实例树，用 XGBoost 预测各模块综合时间，再按 min C = L + λE（综合时间加 edgecut 代价）做自顶向下的层次树划分，用 first-fit bin-packing 评估代价，使子电路可并行综合、并缩短 LLM 上下文。
- 多模态程序分析（§3.2）：输入电路图与 RTL，用 CoT 式提示让 LMM 输出优化模式和验证模式（组合/时序、算术等）。
- 检索引擎（§3.2, Table 1/2）：库中存图、代码、优化指令、算法；代码检索为 TF-IDF + LLM 嵌入的两阶段排序，第二阶段兼顾相关性与多样性（式 3、4）；图和算法用 join query。嵌入分别用 ViT、Llama3、DeepSeek。
- C-MCTS（§3.2）：根节点有 7 种检索内容组合，动作有 4 种提示（Table 3），选择式 a* = argmax(Q + λU + γC)，其中成本项 C 由验证通过率和 sigmoid 项构成，检索内容少的状态初始值更高。奖励：验证失败 0，等价但不优于原始 0.5，等价且更优 1。
- 快速验证（§3.3）：先用 fuzz 随机测试过滤明显不等价的重写，再按验证模式选 ABC（SAT，组合电路）或 egg（算术电路）做等价检查。

另提出两个基准：Small（初始 55 例，选 14 例报告）和 Large（5 个大设计：CPU、CNN、FFT、Huffman、VMachine），由资深 Verilog 工程师给出优化参考。

主要结果：
- Small（Table 4）：以 Yosys 为 1.00，RTLRewriter 的 wires/cells GeoMean 比为 0.69/0.77；Yosys+Egg 0.93/0.94，GPT-4 0.85/0.87，Claude3 0.88/0.89，VeriGen 1.00/1.00，RTLCoder 0.99/0.99。
- Large（Table 5，Vivado/ABC）：area 比 0.81，delay 比 0.96；Yosys+Egg 为 0.87/0.97；GPT-4、Claude3、VeriGen、RTLCoder 在 5 个大设计上与 Yosys 完全相同（无优化）。VMachine 与 Huffman 上 delay 反而变差。
- 划分消融（Table 6）：不划分综合时间约 10 倍，PPA 差异 0.99，重写性能 0.82（相对不划分 1.00，该列含义文中未解释）。
- 模式识别（Table 7/8）：优化模式 precision/recall 86.14%/83.12%（GPT-4 为 64.12%/72.15%）；验证模式 99.16%/97.24%（GPT-4 为 96.64%/92.23%）。
- 检索（Table 9）：H@1 1.00，H@5 0.68，MAP@3 0.76，MAP@5 0.88，高于 TF-IDF、BM25、XGB、RF。
- C-MCTS（Table 10）：PPA-ratio GPT4 1.0，GPT4-DFS 0.93，GPT4-MCTS 0.84，C-MCTS 0.81。
- 运行时间（Figure 7）：总时间 102 秒，文称显著低于各基线，主要来自 fuzz 过滤和求解器选择；ABC 与所提求解器在一个算术例子上为 4.66s 对 0.01s。

## Evidence and Limits

- 基准规模小：Small 仅报告 14 例（文字却写“16 cases”，前后不一致），Large 仅 5 例，且由作者团队自建；参考优化由工程师编写，未说明与基线是否隔离。
- LLM 基线是同一套“identical prompt engineering”下的 GPT-4/Claude3-Opus，经 Poe 网页接口访问，未说明采样次数和温度；而 RTLRewriter 每例生成约 10 次并搜索，投入的推理预算与基线不对等。Table 10 声称用相同选择次数公平比较，但仅在 Small 上测。
- Yosys+Egg 是作者自行实现并加了自定义算子的版本，细节未给。Yosys 用“标准优化命令”。
- 缺少统计信息：每例单次结果，无方差、无多次运行；Large 基准的整体收益主要来自几个设计，且 delay 在两个设计上变差，文中只说 area 与 delay 总体“优于”。
- 电路划分的 PPA 损失（0.99）与“重写性能 0.82”的定义不清；“PPA 损失可忽略”依据极少。
- 验证：fuzz 测试只能过滤不等价，不能证明等价；最终是否均经形式等价检查，文中说有但未给各例验证结果或通过率。图 7 的时间只给了一个总数。
- 检索库“需要大量人工”，构建细节省略；检索评测的数据集和标签来源未说明。优化模式提取依赖 GPT-4V，与同为 GPT-4 的基线对比的测试集规模未说明。
- 未说明闭源模型版本和成本（token、费用）；C-MCTS 声称降低推理成本，但未报告实际 API 调用次数或费用。
- 未验证：论文声称“first”，且声称 GPT-4 等“甚至超过 Yosys+Egg”，仅基于上述 14 例。

## Open Questions

- 在相同的采样次数与迭代预算下，纯 GPT-4 + 重复采样 + fuzz/等价检查能达到什么程度，即 C-MCTS、检索与多模态各自的净贡献在 Large 基准上是多少？
- Large 基准中 delay 变差的设计（Huffman、VMachine）如何被接受或拒绝，框架的目标函数如何在 area 与 delay 间取舍？
- 划分后各子电路单独重写的结果，如何保证拼回整体后仍功能等价和时序一致？

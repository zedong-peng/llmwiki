---
title: "Sanger: A Co-Design Framework for Enabling Sparse Attention using Reconfigurable Architecture"
updated: 2026-10-09
---

# Sanger: A Co-Design Framework for Enabling Sparse Attention using Reconfigurable Architecture

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文、附录 artifact description、参考文献）；图中数值（Fig. 8/9/10 坐标）和 Table 5 的 pattern 可视化为图像，文本中缺失，仅有文字描述和表中数字。

## Summary

问题：attention 的计算量随序列长度平方增长；静态稀疏（Longformer/BigBird）粒度粗、稀疏度低，动态非结构化稀疏（A3 等）则负载不均、解码开销大，硬件加速有限 (§1, §2.2, Table 1)。

方法（MICRO'21，PKU，软硬件协同）：
- 软件 (§4)：先把 Q、K 量化到 4-bit（对称线性量化，QAT + STE），算出近似 attention 并做 softmax，再用全局阈值 T 二值化得到 mask；随后对 mask 做 partition / packing（跳过全空子行）/ splitting（把非零过多的子行拆开），得到每行非零数相近的结构化 block，对应一次 systolic array 执行。低比特预测开销约为 16-bit 稠密 attention 的 1/16。
- 硬件 (§5, §6)：score-stationary 数据流，稀疏 score 常驻 PE，同一阵列统一 SDDMM（Q×K，原地累加）与 SpMM（S×V，向右转发累加），用 bubble 调整 PE 间延迟以免解码稀疏格式。RePE 中有 C1–C5 五个运行时可配置模块（Q/score 选择、K/V 选择、累加方式、加法器去向、输出延迟）。用 Chisel 实现，UMC 55nm、500MHz，面积 16.9 mm²、功耗 2.76 W (Table 2)。

结果：
- BERT 上稀疏度（非零比例）0.087–0.331，精度与稠密基线持平，计算节省 3.0–11.5X；SST-2、RTE 略高于基线 (§7.2, Table 3)。同设置下 Longformer/BigBird 精度更低，GLUE 短序列上几乎得不到稀疏。
- GPT-2、BART 在 0.5% 精度损失内稀疏度 0.15–0.35、0.23–0.54。
- 相对 V100：BERT/GPT-2/BART 平均加速 4.71X/6.45X/3.76X（FP32），4.64X/6.88X/3.94X（FP16）；相对 Threadripper 3970X 为 22.7X/13.3X/13.2X；能效为 GPU-FP32 48X、GPU-FP16 35X、CPU 113X (§7.3, Fig. 8)。
- 相对其他加速器（等比例缩放到 128 乘法器、1GHz）：A3 2.39X、SpAtten 1.47X、FTRANS 3.11X；有效吞吐 529 GOP/s 对 221/360/170 GOP/s (§7.4, Table 4)。
- 消融 (Fig. 9)：稠密阵列上跑稀疏模型吞吐降至 0.127X；score-stationary + 可重构带来 2.89X；pack&split 再 1.72X，合计比稠密基线 4.32X。pack&split 使 PE 利用率由 0.33–0.59 提到 0.56–0.74 (Table 5)。

## Evidence and Limits

- 模型与数据：BERT-base、GPT-2 small、BART-base；GLUE（去掉 WNLI）、SQuAD v1.1、CLOTH；序列长度最长 512，GLUE 多数 ≤128。没有大模型或长上下文（如 4K 以上）的评测，尽管动机里提到 16K。
- 硬件评估：Chisel RTL 经 DC 综合并用 Innovus 布局布线得到面积/功耗；性能来自自写的 cycle-accurate 模型，假设 128 GB/s HBM；没有流片或 FPGA 实测。
- 对比方式：A3/SpAtten/FTRANS 的数值是缩放到相同乘法器数和 1GHz 后的"有效吞吐 = 架构吞吐 × 计算节省"，工艺（40/55/16nm）和实现不同，A3/SpAtten 是否按各自论文设置复现正文未详述。FTRANS 的计算节省用 16/12=1.33X 估算而非实测。
- GPU/CPU 基线用 cuBLAS/MKL 跑稠密（稀疏模型也不用 cuSPARSE，理由是稀疏度仅约 0.1 且需动态转格式），所以 GPU 并未利用稀疏；GPU-FP16 在短序列上因 tensor core 利用不足反而慢于 FP32，会放大加速比。GPU 数据是 V100 PCIe 32GB（正文）与附录的 16GB 不一致。
- 阈值 T 是全局超参：SQuAD/CLOTH 用 2e-3，其余 GLUE 用 2e-2，需逐任务调。Sanger 需要用稀疏约束 fine-tune 模型；Longformer/BigBird 是缩小块大小后复现，且在 BERT 预训练数据上微调，可比性有限。
- 论文自述局限：稀疏度越高 PE 利用率越低，加速比不随稀疏度线性增长 (MNLI vs CoLA)；GPT-2/BART 的 decoder mask 掉一半，可压缩空间小。
- 附录给出代码与脚本（https://github.com/pku-liang/Sanger），声称可复现 Fig. 8、Fig. 10、Table 3、Table 5 的软件部分；硬件结果（Table 2、Table 4、Fig. 9）未在复现范围内，我也未验证。

## Open Questions

- 4-bit 预测 mask 在更长序列和更大模型（LLM、decoder-only 的自回归 decode 阶段）上是否仍能保持精度，预测本身的开销与带宽如何变化；论文只测了 encoder 类和小 GPT-2 的整句前向。
- 跨加速器对比依赖缩放和理论"有效吞吐"，在同工艺、同内存系统下的实测差距是否仍为 2.39X / 1.47X 未知。
- 全局阈值与 25% 每行非零约束对不同任务的敏感性，以及 pack/split 在线编码的硬件开销是否在 Table 2 的 pack&split 模块中被充分计入。

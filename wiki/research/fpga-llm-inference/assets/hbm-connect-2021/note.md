---
title: "HBM Connect: High-Performance HLS Interconnect for FPGA HBM"
updated: 2026-10-09
---

# HBM Connect: High-Performance HLS Interconnect for FPGA HBM

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文、参考文献）；图（Fig. 1–13）只有标题、无图像内容，Fig. 12 的代码和 Fig. 6–8 的曲线未能读到；Table 9/10 的加粗标注丢失，表格有轻微错位。

## Summary

问题：Alveo U280 的 HBM2 有 32 个 pseudo channel (PC)，理想带宽 460 GB/s，但当多个 PE 访问多个 PC 时有效带宽大幅下降。作者在 Vivado HLS 中实现四个访存密集应用（Table 1，16 个 PC）：MV 乘 211 GB/s、Stencil 206 GB/s，而 bucket sort 只有 65 GB/s、merge sort 只有 9.4 GB/s。后两者需要 PE 与 PC 的 all-to-all 通信，其中 bucket sort 的 PE 写多个 PC，merge sort 的 PE 读多个 PC。（§1, Table 1）

原因分析（§4）：(1) 单 PC 顺序访问约 12.9–13.1 GB/s，理想值 14.4；有效带宽按 BLEN/(BLEN/BWmax+LAT) 建模，读延迟 289 ns、写延迟 151 ns，因此需要较长 burst。(2) 内置 crossbar 只在相邻 4 个 PC 间全连接，跨区访问要经过 lateral connection，16x16 时 lateral 成为瓶颈。用二阶多项式拟合 many-to-many 最大带宽（R2=0.95–0.96）。(3) HLS 直接访问时，相邻 key 目标 PC 不同，AXI burst 长度被设为 1。

方法（§5–6）：
- 自定义 butterfly 多级 crossbar（CXBAR 取 0–4 级），由 2x2 开关组成，用于减少 lateral 流量。
- mux-demux switch：把 2x2 开关拆成 demux、FIFO 缓冲、mux，缓冲 16 时吞吐 1.93，普通开关 1.49；LUT 3748 对 3184，FF 2130 对 4135（Table 4）。并用 Markov chain 模型估计吞吐，缓冲 4/8/16 的估计 1.74/1.88/1.94，与实测 1.74/1.86/1.93 接近。
- HLS virtual buffer (HVB)：多个目标 PC 共享一块物理 FIFO，按虚拟通道划分，以满足 BRAM 最小深度 512 并实现按 PC 的 burst。FIFO-per-PC 方案在 burst 16/32/64 下 PnR 均失败，HVB 能布通（Table 5）。另提出 vfifo_read 类抽象语法（Fig. 13），称可由工具自动转换，文中未实现。

结果（§7–8）：用 BW^2/LUT、BW^2/FF、BW^2/BRAM 作指标，在 5 (CXBAR) x 9 (ABUF) = 45 个设计点上枚举。bucket sort 基线 65 GB/s；CXBAR=2、HVB 深度 64 时 180 GB/s，BW^2/LUT 等指标提升 5.8/8.0/5.2 倍；CXBAR=4（完全替换内置 crossbar、无需 HVB）达到 203 GB/s，接近 16 PC 顺序访问上限 206 GB/s，BW^2/BRAM 最佳（9.8）(Table 6, 9)。merge sort 的 BW^2/LUT 最优点在 CXBAR 1–4 且 burst 128–256，BW^2/BRAM 最优在 burst 64，因必须读 16 个地址空间，HVB 无法去掉 (Table 10, §8.3)。摘要和结论称整体指标改善 6.5X–211X（BW^2/LUT）和 9.8X–85X（BW^2/BRAM）。

## Evidence and Limits

- 全部实验在单一板卡 Alveo U280、Vitis/Vivado HLS 2019.2 上完成，只用 16 个 PC（PC 30/31 与 PCIe static region 重叠，32 PC 布线失败）。作者明确说明仅覆盖 U280，Intel 等其他板卡留作未来工作。
- 只有两个人工简化的 case study：key 固定 512 bit、key 分布已知并预置 splitter、不实现第二阶段排序。结论是否泛化到真实排序器或其他访存模式，文中未验证；结论里也承认还要"generalize beyond the two cases"。
- "6.5X–211X" 是自定义的 BW^2/资源指标相对基线（含 NA 项以外）的比值，指标对带宽取平方，是作者假设带宽比资源更重要；绝对带宽提升更小（bucket sort 65→203 GB/s）。资源统计只含 user logic，排除 static region、MC 与内置 crossbar；设计空间的资源数值是用单元资源乘数量估算的，非全部实测 (§7)。
- 表 6 显示 CXBAR=4 的频率只有 207 MHz，低于 CXBAR=2/3 的约 300 MHz；LUT 最高 189K。
- 部分 merge sort 带宽仅由模型估计，未逐点说明哪些是实测，哪些是模型值。设计空间表中有 NA 项（PnR 失败或不适用）。
- 文中没有与其他 HBM 互连方案或手写 RTL 的直接对比，基线只是作者自己的朴素 HLS 写法。代码、HVB 自动转换工具均未给出。
- 正文有一处重复段落（HVB 读操作描述出现两次），为排版问题。

## Open Questions

- HVB 的固定分区（每 PC 固定大小）在 PC 数量更多或访问分布不均时是否可扩展？32 PC 全用时布线问题如何解决？
- 完全 custom crossbar 的收益依赖于"多个 PE 的输出可写入同一内存空间"，对必须保序或写入不同地址的应用是否适用？
- Vitis/HLS 新版本是否改变了 burst 推断和内置 crossbar 的行为，从而改变基线？

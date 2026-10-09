---
title: "Shuhai: Benchmarking High Bandwidth Memory on FPGAs"
updated: 2026-10-09
---

# Shuhai: Benchmarking High Bandwidth Memory on FPGAs

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文与参考文献）；Fig. 5–8 为图，仅有坐标轴文字，曲线细节无法从文本读取；Fig. 6 各子图的具体数值缺失。

## Summary

Xilinx Alveo U280 带两个 HBM2 stack（8GB，32 个 AXI channel / 32 pseudo channel，理论 450 GB/s），另有两路 DDR4（32GB，理论 38.4 GB/s）。HBM 的实际性能特性（延迟、地址映射、内部 switch）缺乏公开说明。论文提出 Shuhai，一个在 FPGA 内部直接挂在 AXI channel 上的 benchmark 工具，用来测量这些特性（§I, §III）。

方法（§III）：
- 软件侧通过 PCIe 写运行时参数，访问模式为 Repetitive Sequential Traversal，地址 T[i] = A + (i×S)%W，参数为 N、B、W、S、A，因此换测试不用重新烧 FPGA。
- 硬件侧每个 AXI channel 一个 engine（Verilog，与 AXI 同频 450 MHz，无跨时钟 FIFO），分 write/read 模块；read 模块可串行发请求逐次测延迟，并有深度 1024 的 latency list。
- 32 个 engine 加 PCIe 等总计约 104K LUT、122K 寄存器，利用率低于 8%（Table III）。

主要结果（§V–VI）：
- 刷新：读延迟中周期性出现明显更长的事务，HBM 与 DDR4 都有，说明需要足够多的 in-flight 请求来摊销（Fig. 4）。
- 空闲延迟（Table IV）：HBM page hit / closed / miss 为 48 / 55 / 62 cycles（106.7 / 122.2 / 137.8 ns）；DDR4 为 22 / 27 / 32 cycles（73.3 / 89.9 / 106.6 ns）。同类别 HBM 约高 30 ns。
- 地址映射（Fig. 6）：默认策略 RGBCG 对所有 S、B 组合都最优；S=1024、B=32 时比 BRC 快近 10 倍；B 小或 S>8K 时吞吐很低；bank group 并行对 HBM 吞吐关键。
- 局部性（Fig. 7）：B=32、S=4K 时，W=8K 为 6.7 GB/s，W=256M 为 2.4 GB/s；S 小时局部性无提升（无 cache）。
- 总带宽（Table V）：单 channel 13.27 GB/s × 32 = 425 GB/s；DDR4 18 GB/s × 2 = 36 GB/s，约 10 倍。
- Switch（§VI, Table VI）：同一 mini-switch 内 4 个 AXI channel 访问同一目标延迟相同；跨 mini-switch 越远延迟越高，page hit 从 55 到 77 cycles（最多差 22 cycles）；switch 开启时比关闭多 7 cycles；吞吐与 AXI channel 位置基本无关（Fig. 8）。

## Evidence and Limits

- 全部数据来自单一板卡（U280）；声称可推广到其他 FPGA / HBM3 / DDR3，但文中没有实测。
- 425 GB/s 不是实测的 32 channel 同时运行结果，而是 channel 0 的 13.27 GB/s 乘以 32（脚注 11，理由是各 channel 无干扰）；跨 channel 同时访问时的真实聚合吞吐没有验证。
- 声称"FPGA benchmark 比 CPU/GPU 更准确"，论据是没有 cache 干扰、engine 与 AXI 同频；文中没有与 GPU 或 CPU 方法的对照实验。
- 延迟测量在空闲状态下进行，测量时 switch 关闭（延迟部分）；吞吐测量时 switch 开启。高负载或排队下的延迟没有测。
- 吞吐实验只覆盖顺序 / 带 stride 的读，写吞吐、读写混合和随机访问（真正的随机地址）未单独评估；论文仅由 stride 大推断随机访问吞吐低。
- Switch 吞吐实验只测了 8 个 mini-switch 中各一个 AXI channel 到 HBM channel 0/1，没有多 AXI channel 同时竞争同一 HBM channel 的结果。
- "可推广到 CPU/GPU 的 HBM"仅为信念陈述（§IV-D），未验证。
- 代码：文末给出 GitHub 地址，称会开源。DDR4 的资源开销因篇幅被省略（脚注 8）。

## Open Questions

- 32 个 AXI channel 全部同时运行、且经 switch 跨 channel 访问时，聚合带宽和竞争下的延迟是多少？
- 刷新间隔与 7.8 µs 的关系只做了定性观察，没有给出 HBM 实测的刷新周期和刷新开销数值。
- 结论在其他 HBM 容量 / 速度等级或其他厂商 FPGA 上是否仍成立？

---
title: "UNISON: A Co-Designed Near-Memory Scheduler of Session KV Residency for LLM Agents"
updated: 2026-10-09
---

# UNISON: A Co-Designed Near-Memory Scheduler of Session KV Residency for LLM Agents

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文、参考文献；无附录）。Fig. 4–8 的图内数据因字体编码乱码基本不可读，只能依赖正文描述；Table II/III 可读。

## Summary

问题：agent loop 在工具等待期间保留不断增长的 KV prefix，多个 session 共享 SRAM+HBM 两级池。LRU、timeout、按工具类型的到达表、基于角色/工作流的打分都没有利用 session 自身的 gap 历史和进度，会把“即将返回的等待”当成冷数据逐出（§I, §II）。

方法：一个事件驱动的 near-memory 调度 IP，由两部分共用一份 session 寄存器堆（§III）：
- SPEAR（驱逐）：score = g/σ(t) + (1−σ(t))·P。g 是 gap 的 EMA（α=0.3），σ(t) 由按 turn 统计的离散 hazard 查表得到（t 截断在 50），P 为可编程的完成惩罚；分数最高者被逐出。
- TIDE（分层）：gap_start 时用预计剩余等待时间乘 DMA 带宽得到迁移 token 预算，用同一个分数把 HBM 中分数最低的换进 SRAM、SRAM 中分数最高的换出。
- 硬件（§IV）：定点化（hazard 12 bit，gap 32 bit，μs 存储，score 64 bit 饱和），在 180 个格式点上选定；5 级流水线线性扫描，N=64 个 session 时 N+5 周期；28 nm CMOS 综合 0.169 mm²、13.6 mW、150 MHz（Table VII）；平均决策延迟 2.00 μs，最坏 3.14 μs；Zynq-7020 FPGA 原型（43 415 LUT，20 DSP）。

结果（§V，trace 驱动模拟器）：SWE-bench × GAIA × 三个模型（Qwen3-Coder-30B、Devstral-24B、Gemma4-E4B）共 6 条 trace，1 415 个 session、33 596 turn，6 种 SRAM/HBM 容量。
- Table II：UNISON 在所有 trace 上命中率和 AMAT 都是非 oracle 中最好；Bélády ratio 0.93；对 LRU 的 AMAT 在 36 个配对比较中全部更优，平均降低 34.8%。例：SWE/Qw3 命中率 LRU 20.7 → UNISON 43.8（oracle 43.9）。
- 摘要称命中率提升 0.3%–23.1%、AMAT 降低 22%–51%，长程 trace 上 TTFT 降低 58%–89%。
- 消融（Fig. 5）：单独 SPEAR 或单独 TIDE 都不如联合；没有 SPEAR 的迁移预取准确率仅 1.1%。leave-one-out（Fig. 6）显示 hazard 与 gap 都不可缺，elapsed idle 贡献最小（平均 1.55 pp），因此 RTL 去掉了它。
- 容量扫描（Table III）：各点相对 LRU 都为正，SRAM 占比越大收益越大（如 SRAM 40K 时 ΔHR +25.2 pp、ΔAMAT −38.0%）。
- 结构必要性（§IV-B, Table I, §VI-G）：双 IP + 周期同步的设计在每 8 个请求同步时命中率最多下降 5.4 pp，AMAT 变化符号不一致。
- 实现保真（§VI-F）：定点与浮点的 top-1 victim 一致率 0.9945，Kendall τ > 0.998，最坏命中率漂移 0.192 pp。

## Evidence and Limits

- 所有主结果来自自建的单 agent 回放语料和模拟器（Ollama + litellm 代理记录时间）。作者承认没有公开的多 agent session 级 trace，并发是通过回放构造的。AMAT 用 ts/th/tp 的每 token 成本模型，TTFT 用 trace 驱动的负载模型（4× 负载，p50），不是实测硬件时延。
- 对比基线较弱或不完全对等：CacheScout 只在一个 matched 两级 harness 的 Edge-Tight 点评估，其命中率很低（如 SWE/Qw3 为 2.6%）；AGSERVE 的 TTFT/LRU（0.63）略低于 UNISON（0.64），作者解释为命中率与延迟的取舍。Bélády oracle 在 AMAT/TTFT 上被 UNISON 超过或不如它（如 GAIA 的 AMAT 0.52 vs 0.67），说明 oracle 只最优化命中而非 AMAT。
- hazard LUT 在全 trace 上拟合；§V-F 用 5 折交叉验证（Table IV，held-out 偏差最多 0.85 pp）和在线冷启动收敛曲线（Fig. 7）来回应，但只在 SWE/Qwen3 上做交叉验证。
- vLLM 验证（Table V）只用 SPEAR，TIDE 因 block cache 无分层 API 未测；只有 GAIA/Qwen3，模型为 Qwen2.5-1.5B 时 TTFT 降 35%、p99 e2e 降 72%，换成 30B 原生模型只剩命中率 +1.6 pp、TTFT −1%。
- 自述退化：GAIA/Devstral 在缩小池+紧调度下，因工具 gap 短于 decode 时间，软件时间戳使 gap 信号反转，命中率降 6.6 pp；GAIA/Gemma4 只有 128 个 session，LUT 噪声大；SWE 的 Qwen3/Devstral 受 GPU 计算限制，策略不影响 TTFT。
- 硬件：功耗为 vectorless 估计，面积不含 HBM PHY、KV 阵列、prefix directory、router；FPGA 仅回放一条 trace（1 937 事件、845 决策）。“软件无法实现”的论点主要依据毫秒级时间戳粒度与 Python GIL 的推断，并未实测一个带精确事件钩子的软件实现。
- 文中数字不一致：Fig. 2 写 1,451 sessions，正文写 1 415。
- 无官方代码链接。

## Open Questions

- 在真实的多 agent、多租户并发（而非单 agent trace 回放）下，gap EMA 与 turn-indexed hazard 是否仍稳定，hazard 表在工作负载漂移时如何更新？
- “不能由软件实现”的必要性论证依赖毫秒级时间戳假设；若软件拿到精确的请求完成事件，收益还有多少只能靠硬件？论文没有给出这一对照。
- 命中率/AMAT 的提升在端到端 TTFT 上只在缓存受限的场景转化为收益（vLLM 30B 仅 −1%），代表性部署中这种场景占多大比例未说明。

---
title: "Combating the Memory Walls: Optimization Pathways for Long-Context Agentic LLM Inference (PLENA)"
updated: 2026-10-09
---

# Combating the Memory Walls: Optimization Pathways for Long-Context Agentic LLM Inference (PLENA)

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文、参考文献；无附录）。图（Fig. 1/2/11–14）只有图注，没有数据；表格基本可读。

## Summary

问题：agentic 推理（computer use、web use、tool call）上下文很长，单次推理 token 数比 chatbot 高约 100×，极端 1000×（Fig. 1a）。随上下文增长，计算重心从 FFN 移到 attention（LLaMA-3-70B 在约 19K 生成 token 处交叉，Fig. 1b），KV cache 超过权重成为显存主角（128k 下单 batch FP16 KV 约 39 GB）。作者把带宽与容量限制合称 "memory walls"，认为 batch 受容量限制而偏小，造成 M 维很小的"fat GEMM"，方阵 systolic array 利用率低（§I）。

方法：PLENA 是一套软硬件协同系统，含三条路径。
- Pathway 1，flattened systolic array：把阵列做成扁平形状，使 BLEN（对应 batch 维）远小于 MLEN（归约维），输出驻留（output-stationary）数据流，并用 result adder tree 和 MSUM 指令做跨子阵列求和；FlashAttention 时把阵列按 head 切成多个小核并行（§III-B）。
- Pathway 2，asymmetric quantization：激活保持较高精度，权重和 KV 用可配置的 MX 格式（MXINT/MXFP）。算法上提出 output-norm 引导的 block-wise clipping，嵌入 GPTQ 的误差传播（式 6–8），以及只在部分层对激活/KV 做在线 Hadamard 旋转的 selective rotation（式 9–10）（§IV）。
- Pathway 3，原生 FlashAttention：Matrix SRAM 支持 transpose-on-read，vector/scalar 单元做在线 softmax，ISA 支持 tile 级调度和预取（§III-C/E/F）。
- 配套：自定义 32 位 ISA（Table I 共 47 条指令）、PyTorch 到 ISA 的轻量编译器、Rust 事务级模拟器（接 Ramulator/DRAMSys）、基于 BoTorch 的精度/延迟/面积多目标 DSE、SystemVerilog RTL（Synopsys DC，7nm 预测 PDK，1 GHz）。

主要结果：
- 量化：W4A4KV16 下 LLaMA-3-8B WikiText-2 PPL 6.76（QuaRot 复现 8.00，FP16 6.13）；W4A4KV4 下 7.22（QuaRot 8.16，QuaRot-128G 7.36）（Table V）。LLaMA-3-70B W4A4KV4 为 4.77，QuaRot-128G 为 5.51。
- 消融（Table VI，LLaMA-3-8B）：MXFP4 一律差于 MXINT4；权重量化上旋转有害（MXINT4 6.83 到 6.98）；Erry clip 6.45 优于 Errw clip 6.53；全系统 RTN 8.28、加 Erry clip 7.60、再加 selective rotation 7.22。
- 下游：LLaMA-3-8B 4/4/4 平均 70.39（FP16 73.22，QuaRot 65.18）；LLaMA-3-70B 76.20（79.94，69.21）（Table VII）。Agentic 任务 4/4/4：HumanEval 84.1（基线 89.6），GSM8K 97.85（持平），BFCL-Web 24.0（27.0）（Table VIII）。
- 系统（Table XII）：同等乘法器数与 HBM 配置下，LLaMA-3.3-70B 的 (114k,5k) 负载 PLENA TPS 为 A100 的 2.23×，Tok/J 4.07×；(90k,8k) 为 2.21× / 4.04×。摘要中 4.70× 对 TPU v6e 是 2.21/0.47 的比值，表中没有直接列出。LLaMA-3.1-8B (90k,8k) 为 1.45×。Equal-batch 一栏收益缩小（70B 为 1.34×，8B 为 1.17×）。
- 硬件（Table XI）：4×1024 阵列面积 0.237 mm²，agentic 负载下 FLOPs/mm² 为 12.81，对比 MicroScopiQ 1.08、Olive 0.40、FIGNA 6.71；峰值 TOPs/mm² 34.49 低于 MicroScopiQ 的 59.45。
- 模拟器校准（Table II）：事务级模拟器相对 RTL 的延迟误差 4.17%，解析模型 11.32%。

## Evidence and Limits

- 吞吐优势主要来自 4-bit 量化带来的更大 batch（Table XII 中 PLENA batch 为 A100 的 4 倍；L-3.3-70B 为 16 比 4）。Equal Batch 一栏才是更接近硬件本身的对比，那里优势明显变小，L-3.1-8B 的 TTFT 也更差。摘要里的 2.23×/4.70× 是各 batch 取各自最大值的结果。
- PLENA、MicroScopiQ 的数字来自自家 7nm 模拟器（DeepScale 缩放），A100/H100/TPU 是实测（vLLM 0.10）。GPU/TPU 为 FP16（A100 另有 QuaRot 行），精度不同；"相同乘法器数"是近似对齐，不是按面积。对比者 MicroScopiQ、FIGNA、Olive 是作者重新实现后接入 PLENA 平台的，非原作者实现。
- 能耗数据（Tok/J）依赖综合功耗估计加缩放，没有流片或板级测量；TPU 能效记为 N/A。
- Table V 中 W4A16 设置下 PLENA 并不全面领先（LLaMA-3-70B 为 3.59，MicroScopiQ 3.25，QuaRot 3.53）；"W4A4KV16 全面优于相关工作" 的说法与表格基本一致，但 QuaRot 的部分数字是作者复现。PPL 只在 WikiText-2 上；GPT-OSS、Qwen3 只给了部分下游结果（Table IX）。
- 下游 agentic 评估只有 HumanEval、GSM8K、BFCL-Web，没有 OSWorld 等真正的长轨迹 agent 任务精度，OSWorld-L 仅作为 token 长度配置使用（Table XIII）。BFCL 样本量与方差未说明。
- GPT-OSS 20B 在 (1.4k,0.2k) 下 TTFT 为 13.41 s，A100 为 1.46 s；PLENA 的 TTFT 普遍较高，文中归因于 batch 更大。
- 代码和 RTL "将在论文接收后开源"，目前无法核对。解析模型功耗误差 23.81%；事务级模拟器不支持面积/功耗。DSE 只在 1B 和 8B 上跑（50 trials、5–9 seeds）。
- 量化过程需要 2–20 H100 GPU 小时；selective rotation 的层选择是逐模型搜索，成本和泛化性文中未展开。

## Open Questions

- 把 batch 受限于 HBM 容量作为前提，那么在权重/KV 量化后容量放宽时，flattened array 对 BLEN 的匹配是否仍是主要增益来源？文中缺少只开关阵列形状而保持量化和 batch 不变的消融（Fig. 13 的消融包含多项优化叠加）。
- 4-bit KV 在真正的多轮、长轨迹 agent 任务（误差会累积）上的成功率是否保持，现有 BFCL/HumanEval 证据较弱。
- 事务级模拟器只在单个 LLaMA-3-70B Transformer block 上对照过 RTL（Table II），整模型多卡、16 加速器系统的互联与同步开销如何建模，文中未说明。

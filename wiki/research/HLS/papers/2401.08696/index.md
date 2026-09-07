# Hierarchical Source-to-Post-Route QoR Prediction in High-Level Synthesis with GNNs

**Authors**: Mingzhe Gao, Jieru Zhao, Zhe Lin, Minyi Guo
**Affiliations**: Shanghai Jiao Tong University; Sun Yat-sen University
**Submitted**: 2024-01-14
**arXiv**: [2401.08696](https://arxiv.org/abs/2401.08696)
**Code**: https://github.com/sjtu-zhao-lab/hierarchical-gnn-for-hls

---

## 问题与动机

HLS（高层次综合）可以从 C/C++ 直接生成 FPGA 硬件，但 post-route QoR（延迟、资源利用率）的评估需要跑完整的 C-to-bitstream 流程（HLS + 逻辑综合 + 布局布线），耗时极长，严重拖慢 DSE（设计空间探索）。

现有方法的局限：
- 分析模型（HLScope+, COMBA）：精度高但只支持固定 pragma 子集，扩展性差
- ML 方法（Dai et al., Pyramid）：预测 post-route QoR，但特征来自 HLS 报告，仍需跑 HLS
- GNN 方法（GNN-DSE, Ferretti et al.）：从源码预测，但只预测 post-HLS 指标，与 post-route 偏差大
- Wu et al.（DAC 2022）：从 HLS IR 预测 post-route QoR，但需要跑 HLS，且不支持 pragma，代码结构简单

**本文目标**：直接从 C/C++ 源码预测 post-route QoR，支持多种 pragma 组合，无需调用任何 EDA 工具。

---

## 方法

### 总体流程

```
C/C++ 源码
  → LLVM IR（Clang 前端）
  → 图构建（CDFG + pragma 扩展）
  → 特征标注
  → 分层 GNN 训练与推理
  → post-route QoR 预测
```

训练阶段需要跑完整 C-to-bitstream 流程获取 ground truth；推理阶段完全不需要 EDA 工具。

### 图构建（Graph Construction）

基于 PrograML 扩展 CDFG，针对三种 pragma 做特殊处理：

| Pragma | 图构建策略 |
|--------|-----------|
| `#pragma HLS pipeline` | 图结构不变，通过额外特征（II、IL、TC）区分 |
| `#pragma HLS unroll` | 复制展开区域的逻辑节点，建立与前驱/后继的连接 |
| `#pragma HLS array_partition` | 添加 I/O port 节点；按分区因子拆分内存端口节点；通过 LLVM pass 分析访存索引确定连接关系 |

对于 k 维数组，分区因子为 u₁,...,uₖ，添加 ∏uᵢ 个内存端口节点。

### 特征标注

**节点特征**（9 维）：

| 特征 | 说明 |
|------|------|
| Optype | 操作类型（one-hot），如 add/mul/load/store |
| #invocation | 节点执行次数（tripcount / unroll factor） |
| In/Out degree | 入度/出度，间接反映 MUX 资源 |
| #cycle | 操作占用时钟周期数 |
| Delay | 操作延迟（ns），来自 micro-benchmark 库 |
| LUT/DSP/FF | 算术操作的资源用量，来自 micro-benchmark 库 |

**循环级特征**（用于流水线循环）：
- IL（iteration latency）：由 GNN 估计
- TC（tripcount）：从 LLVM IR 分析
- II（initiation interval）：解析计算下界

$$II_{min} = \max(II^{rec}, II^{res}) = \max\left(\max\left\{\left\lceil\frac{Delay_p}{Distance_p}\right\rceil\right\}, \max\left\{\left\lceil\frac{Access_m}{Ports_m}\right\rceil\right\}\right)$$

### 分层 GNN 建模

核心思想：按循环层次分而治之，从内到外逐层预测，而非对整图直接预测。

**内层（Inner Hierarchy）**：只含计算逻辑、无子循环的循环，包括：
1. 单层循环
2. 最外层 pipeline（内层全展开）
3. 完美嵌套循环 + flatten + pipeline（等价单层）
4. 内层全展开的嵌套循环

训练两个独立 GNN：
- **GNN_p**：流水线循环（pipelined）
- **GNN_np**：非流水线循环（non-pipelined）

预测完内层 QoR 后，将内层子图折叠为 **super node**，以预测的 QoR 作为 super node 特征。

**外层（Outer Hierarchy）**：其余逻辑和循环层次。super node 与外层节点组合成完整图，输入：
- **GNN_g**：全局模型，预测整个应用的最终 QoR

**分层训练**：先训练 GNN_p 和 GNN_np，冻结权重，再用其输出作为 super node 特征训练 GNN_g。

### GNN 架构

每个模型结构相同：
```
特征编码器 → 3层消息传递 → sum+max pooling → MLP
```

评估了 5 种消息传递层：GCN、GAT、GraphSAGE、TransformerConv、PNA。

延迟预测：内层 GNN 先预测 iteration latency，再结合循环级特征用 MLP 预测子循环延迟；外层 GNN_g 直接预测整体延迟。

---

## 实验

**平台**：AMD Ultrascale+ MPSoC ZCU102
**工具**：Vitis-HLS 2022.1 + Vivado 2022.1
**基准**：Polybench + MachSuite + CHStone（16 个应用，12 训练，4 DSE）
**数据集**：GNN_p 3102 个设计点，GNN_np 2300，GNN_g 6178；80/10/10 划分
**指标**：MAPE（平均绝对百分比误差）

### QoR 预测精度（GNN_g，最优结果）

| 指标 | 最优 GNN | MAPE |
|------|---------|------|
| Latency | TransformerConv | **8.54%** |
| DSP | GraphSAGE | **6.94%** |
| LUT | PNA | **9.65%** |
| FF | GraphSAGE | **9.99%** |

所有指标均 < 10%。

### 与 Wu et al. 对比

| 方法 | 配置 | Latency | DSP | LUT | FF |
|------|------|---------|-----|-----|----|
| Wu et al. | w/o pragma | N/A | 8.26% | 5.10% | 7.58% |
| Ours | w/o pragma | 5.54% | 6.71% | 6.78% | 7.91% |
| Wu et al. | w/ pragma | 35.81% | 57.31% | 27.14% | 29.03% |
| **Ours** | **w/ pragma** | **8.54%** | **6.94%** | **9.65%** | **9.99%** |

pragma 场景下提升极为显著（Wu et al. DSP 误差高达 57%）。

### DSE 结果

目标：找到 Pareto 最优 pragma 配置，用 ADRS 衡量近似质量。

| Kernel | #设计点 | Vivado 时间 | 本文时间 | Wu et al. ADRS | GNN-DSE ADRS | **本文 ADRS** |
|--------|---------|------------|---------|---------------|-------------|-------------|
| bicg | 2796 | 26天 | 12分钟 | 12.13% | 9.14% | **6.39%** |
| symm | 1972 | 44天 | 15分钟 | 13.15% | 11.50% | **5.45%** |
| mvt | 2116 | 25天 | 14分钟 | 16.01% | 12.17% | **9.31%** |
| syrk | 1972 | 40天 | 15分钟 | 14.45% | 11.03% | **6.49%** |
| **平均** | | | | 13.94% | 10.96% | **6.91%** |

DSE 时间从数十天缩短到十几分钟，ADRS 优于所有对比方法。

---

## 关键设计决策

1. **为何分离 GNN_p 和 GNN_np**：流水线与非流水线循环的硬件执行模型不同，分开训练精度更高（实验验证）。
2. **super node 机制**：将内层预测结果作为特征传递给外层，使全局模型能感知内层误差并做修正，避免误差累积过大。
3. **loop unrolling 显式展开节点**：在图中复制节点而非用特征编码，让 GNN 自然学习并行结构，降低预测难度。
4. **array_partition 用内存端口节点建模**：通过 LLVM pass 静态分析访存索引，精确建立 load/store 与内存端口的连接。

---

## 相关工作

| 方法 | 模型 | 输入 | 预测目标 | Pragma | 无需 HLS |
|------|------|------|---------|--------|---------|
| Zhong et al. | GBM | 源码 | Post-HLS | ✓ | ✓ |
| Dai et al. | XGB | HLS 报告 | Post-Route | ✗ | ✗ |
| GNN-DSE | GNN | 源码 | Post-HLS | ✓ | ✓ |
| Wu et al. | GNN | HLS IR | Post-Route | ✗ | ✗ |
| **本文** | **GNN** | **源码** | **Post-Route** | **✓** | **✓** |

---

## 局限与未来方向

- 分层结构目前只处理两层（inner/outer），更深嵌套需要扩展
- II 用解析下界估计，与实际综合 II 可能有偏差
- 数据集规模相对有限（16 个应用），泛化性有待验证
- 未考虑 dataflow pragma 等函数级优化

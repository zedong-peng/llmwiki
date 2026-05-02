# EvoMaster: A Foundational Evolving Agent Framework for Agentic Science at Scale

**Authors:** Xinyu Zhu, Yuzhu Cai, Zexi Liu et al. (SJTU / SciLand / DP Technology), Siheng Chen (corresponding)
**arXiv:** [2604.17406](https://arxiv.org/abs/2604.17406)
**Code:** https://github.com/sjtu-sai-agents/EvoMaster

---

## 一句话总结

EvoMaster 是 inference-time scaling 在 agentic 科学任务上的一种具体形态：把 compute 预算结构化地分配到不同认知角色（generate / critique / refine）和不同时间步（prefetch / draft / improve），让 LLM 逼近其知识边界，而不是停在单次调用的"懒惰平衡点"上。**没有任何训练。**

---

## 问题与动机

现有科学 agent 框架的两大缺陷：
1. **碎片化孤岛开发**：ChemCrow、MLAgentBench 等各搭各的 harness，跨领域不可复用，新领域边际开发成本极高。
2. **缺乏 evolution 机制**：现有框架单次执行即终止（single-pass），与科学研究本质上的假设-实验-修正迭代过程背道而驰。

---

## 方法

### 框架架构（3 层解耦）

```
Playground (Orchestration)   ← 多 agent 协作拓扑、领域 workflow
    └─ Exp (Experiment)       ← 单次实验生命周期、轨迹记录
        └─ Agent (Intelligence) ← 迭代推理 + 工具调用循环
```

### 4 大设计原则

1. **Modular Composability**：组件通过统一 Registry 注册，支持 MCP 协议和 Skill 规范，新领域 ~100 行代码接入。
2. **Experiment-Ready Harness**：YAML 配置驱动参数，Thread-safe JSON 轨迹系统记录每个 turn、工具调用和 token 统计。
3. **Iterative Self-Evolving**：Agent Engine 运行 `reason → tool → observe → self-critique` 多轮循环；Context Manager 用动态 LLM 摘要 + sliding window 防止长 horizon 上下文退化。
4. **Multi-Agent Collaborative Evolution**：通过 `AgentSlots` 声明式定义 solver/critic/rewriter 等角色，支持 sequential、parallel、peer-review 协作模式。

### Capability Layer

- **Tool System**：Action-Execution-Observation 模式，原生支持 MCP，外部工具自动转换。
- **Skill System**：层级注入，metadata 常驻上下文，详细指令按需加载（省 context）。
- **LLM Abstraction**：通过 LiteLLM 统一接口，支持 100+ 模型热插拔。

---

## Backbone Model

Paper 声称用 **GPT-5.4**，但代码里的 example config 默认是 **DeepSeek-V3.2**（本地 sglang 部署），同时支持 Claude (haiku-4-5-20251001)、OpenRouter、任意 OpenAI 兼容接口。模型通过 `${GPT_CHAT_MODEL}` 环境变量注入，LLM 抽象层（基于 LiteLLM）使所有 agent 无需改代码即可换模型。没有训练，没有 fine-tuning，所有"evolution"均为 inference-time 行为。

---

## 实验环境

- **硬件**：NVIDIA RTX 4090（仅用于本地工具执行和 API 调用，不做任何训练）
- **对比基线**：OpenClaw（通用 AI agent，支持 100+ 内置 skill）
- **约束**：MLE-Bench 限制 24 小时运行时

---

## 每个 Benchmark 的专门 Agent（非一招鲜）

EvoMaster 是共享 harness，但上层 agent 针对各领域深度定制，代码位于独立的 `playground/` 子目录：

| Benchmark | Agent | 代码路径 | Pipeline 设计 |
|---|---|---|---|
| **HLE** (41.1%, +202%) | X-Master | `playground/x_master/` | SolveExp → CritiqueExp → RewriteExp → SelectExp；多 solver 并行，best-of-N 选择 |
| **MLE-Bench Lite** (75.8%, +316%) | ML-Master 2.0 | `playground/ml_master_2/` | 7 角色：prefetch / draft / debug / improve / research / knowledge_promotion / wisdom_promotion；`wisdom.json` 跨 run 持久化 |
| **BrowseComp** (73.3%, +159%) | Browse-Master | `playground/browse_master/` | planner + executor 两角色；planner 制定检索计划，executor 执行 MCP web 工具 |
| **FrontierScience** (53.3%, +191%) | X-Master 2.0 | ❌ 未在 repo 中 | — |

每个 Playground 通过 `@register_playground("x_master")` 装饰器注册，互不干扰。

---

## "LLM 更新"的实质（代码验证）

**无参数更新**，全库搜索 `gradient / optimizer / loss / fine_tun` 零命中。"evolution" 全部是 inference-time 的 context engineering，核心在两个文件：

### `evomaster/agent/agent.py` — BaseAgent 主循环

```python
for turn in range(config.max_turns):
    dialog_for_query = context_manager.prepare_for_query(current_dialog)
    assistant_message = llm.query(dialog_for_query)        # 纯 inference
    for tool_call in assistant_message.tool_calls:
        observation = _execute_tool(tool_call)
        current_dialog.add_message(ToolMessage(observation))
    _append_trajectory_entry(...)                          # JSON 轨迹记录
```

### `evomaster/agent/context.py` — ContextManager：无限变长 prompt 的处理

这是回答"无限变长 prompt 怎么维护"的关键：

**两级溢出保护：**
1. **Proactive（80% token 占用）**：临时清除旧的 tool output（reversible）
2. **Aggressive（100% token 占用）**：永久截断 + LLM 摘要（irreversible）

**4 种截断策略（可配置）：**
- `LATEST_HALF`：保留最近一半历史
- `SLIDING_WINDOW`：保留最近 N 轮对话
- `SUMMARY`：调 LLM 对旧消息生成摘要后替换（摘要本身也消耗 token，但大幅压缩）
- `NONE`：不截断（依赖模型原生长窗口）

**应急恢复：**
```python
try:
    assistant_message = llm.query(dialog_for_query)
except ContextOverflowError:
    self.current_dialog = context_manager.truncate(current_dialog)
    assistant_message = llm.query(dialog_for_query)   # 压缩后重试
```

**跨 turn 记忆（ML-Master 2.0 特有）：**
- `wisdom.json`：把每轮 LLM 输出的洞察写入磁盘，下次 prefetch 阶段读回来注入 prompt
- 本质是"外部记忆"而非模型内部状态，规避了 context 长度限制
- 三级提升：round-level knowledge promotion → run-level wisdom promotion → 跨实验复用

**Skill 系统的懒加载：**
- Skill metadata 常驻上下文（少量 token）
- 详细指令按需加载（避免所有 skill 文档占满 context）

---

## 代码完整性（repo 核查）

| Agent | 对应 benchmark | repo 状态 |
|---|---|---|
| ML-Master 2.0 | MLE-Bench | ✅ `playground/ml_master_2/` |
| ML-Master 1.0 | MLE-Bench (旧版) | ✅ `playground/ml_master/` |
| X-Master | HLE | ✅ `playground/x_master/` |
| Browse-Master | BrowseComp | ✅ `playground/browse_master/` |
| Mat-Master | 材料科学 | ✅ `playground/mat_master/` |
| X-Master 2.0 | FrontierScience | ❌ 未在 repo 中 |
| PhysMaster | 物理 | ❌ Coming soon |
| EmboMaster | 具身智能 | ❌ Coming soon |

---

## SciMaster 生态

| Agent | 领域 | 开源状态 |
|---|---|---|
| ML-Master 2.0 | 自主机器学习 | 已开源 |
| ML-Master | 自主机器学习 | 已开源 |
| X-Master | 通用科学研究 | 已开源 |
| Browse-Master | Web 信息检索 | 已开源 |
| X-Master 2.0 | 前沿科学推理 | Coming soon |
| PhysMaster | 物理研究 | Coming soon |
| EmboMaster | 具身智能训练 | Coming soon |

---

## 范式意义：inference-time scaling 的 agentic 形态

CoT 被提出时也被质疑"只是用更多 token 换准确率"，但事后来看多步推理是能力涌现的载体，不是作弊。EvoMaster 类框架是同一逻辑在更大粒度上的延伸：

| 范式 | 计算展开的粒度 | 机制 |
|---|---|---|
| CoT | 单次 forward pass 内部 | 更长 decoding 序列 |
| Multi-agent iterative loop | 跨 API call | 角色分离 × 迭代次数 |

两者本质都是"用更多计算展开认知过程"，接受 CoT 为范式而拒绝后者在逻辑上不自洽。

**EvoMaster 的具体贡献**是把 inference-time compute 结构化：不是盲目多调几次，而是把 compute 分配到有意义的认知角色（solver/critic/rewriter）和时间阶段（prefetch/draft/improve/wisdom promotion）上，使 LLM 能在每个 pass 专注单一角色、避免单次 inference 同时处理生成和批判的角色冲突。

与 OpenClaw 的对比更应读作：**"结构化 inference-time scaling 远胜非结构化 inference-time scaling"**，而非"harness 好坏"的简单比较。

---

## 局限

- **FrontierScience agent 未开源**：X-Master 2.0 代码不在 repo 中，该 benchmark 结果无法复现
- 仅支持 in silico 计算工作流，不支持物理实验设备
- Context Manager 的摘要策略（SUMMARY）会丢失细节，长 horizon 任务存在信息损耗
- inference-time compute 开销大，API 成本未在论文中量化
- FrontierScience 仅单次 run，无统计显著性

---

## 关键引用

- OpenClaw (baseline): Steinberger et al. 2025
- MLE-Bench: Chan et al. 2024
- BrowseComp: Wei et al. 2025
- HLE: Humanity's Last Exam 2025
- FrontierScience: OpenAI 2026
- AI Scientist: Lu et al. 2024
- MCP: Anthropic 2025

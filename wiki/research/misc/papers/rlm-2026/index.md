# Recursive Language Models (RLM)

**Authors**: Alex L. Zhang, Tim Kraska, Omar Khattab (MIT CSAIL)
**Conference**: ICML 2026
**arXiv**: [2512.24601](https://arxiv.org/abs/2512.24601)
**Code**: [github.com/alexzhang13/rlm](https://github.com/alexzhang13/rlm)

## 核心思想

RLM 是一种通用的推理时范式，通过将长提示视为**外部环境**的一部分，允许 LLM **程序化地**检查、分解并**递归调用自身**来处理任意长度的输入。

关键洞察：不应将任意长的用户提示直接输入神经网络，而应将其视为 LLM 需要**符号化和递归交互**的环境的一部分。

## 方法

### 核心设计

RLM 将用户提示 $P$ 加载为 REPL 环境中的变量，LLM 可以：
1. 通过代码查看和分解 $P$
2. 在循环中程序化地调用子 RLM
3. 将中间结果存储在变量中
4. 构建最终响应而不受上下文窗口限制

### 三个关键设计选择

1. **符号化句柄 (Symbolic Handle)**: 给 LLM 提供对用户提示的符号化访问，而不是将其复制到上下文窗口
2. **变量输出 (Variable Output)**: 通过 REPL 变量构建输出，而非自回归生成，突破输出长度限制
3. **符号化递归 (Symbolic Recursion)**: 在 REPL 环境内程序化地调用 LLM，可在循环中处理 $\Omega(|P|)$ 甚至 $\Omega(|P|^2)$ 的子任务

## 实验结果

### 评测任务

- **S-NIAH**: 单针检索任务，$O(1)$ 复杂度
- **BrowseComp-Plus (1K docs)**: 多跳问答，需要推理多个文档
- **OOLONG**: 语义转换和聚合任务，线性复杂度
- **OOLONG-Pairs**: 配对聚合任务，二次复杂度
- **LongBench-v2 CodeQA**: 代码仓库理解任务

### 主要发现

1. **超长上下文处理**: RLM 可处理超出模型上下文窗口 2 个数量级的输入（10M+ tokens），在 BrowseComp-Plus (1K) 上比基线方法高出 29%

2. **信息密集任务优势**:
   - OOLONG: RLM(GPT-5) 和 RLM(Qwen3-Coder) 分别比基础模型高 28.4% 和 33.3%
   - OOLONG-Pairs: GPT-5 和 Qwen3-Coder 基础模型 F1 < 0.1%，而 RLM 达到 58.0% 和 23.1%

3. **性能退化更慢**: 随着输入长度和任务复杂度增加，基础 LLM 性能快速下降，而 RLM 保持稳定

4. **成本可控**: 中位数成本与基础模型相当甚至更低，比摘要代理便宜 3 倍

5. **可训练性**: RLM-Qwen3-8B 仅用 1000 个样本微调，在 4 个任务上平均提升 28.3%，接近 GPT-5 性能

### RLM 轨迹中的涌现模式

- **分块和递归调用**: 通过均匀分块或关键词搜索分解上下文
- **基于先验的过滤**: 使用 regex 等代码执行根据模型先验过滤输入
- **变量传递长输出**: 通过 REPL 变量拼接子调用输出，突破输出长度限制

## 实现

### 代码仓库结构

官方实现提供了可扩展的推理引擎，支持：
- 多种 REPL 环境：local、docker、modal、prime、daytona、e2b
- API 和本地 LLM 支持
- 轨迹可视化工具

安装：
```bash
pip install rlms
```

基本使用：
```python
from rlm import RLM

rlm = RLM(
    backend="openai",
    backend_kwargs={"model_name": "gpt-5-nano"},
    verbose=True
)

response = rlm.completion("Your prompt here")
```

## 相关工作对比

- **vs 上下文压缩**: RLM 不需要遗忘早期细节，适合需要密集访问整个提示的任务
- **vs 检索代理**: RLM 将提示本身作为环境，不受上下文窗口限制
- **vs 子代理委托**: RLM 通过程序化递归而非自回归生成子调用，突破输出长度限制

## 局限性

- 小规模模型（如 Qwen3-8B）作为 RLM 时表现较弱，需要微调
- 尾部成本方差较大，某些轨迹可能非常昂贵
- 在短上下文任务上，RLM 性能略低于基础 LLM

## 关键引用

```bibtex
@misc{zhang2025rlm,
  title={Recursive Language Models},
  author={Alex L. Zhang and Tim Kraska and Omar Khattab},
  year={2025},
  eprint={2512.24601},
  archivePrefix={arXiv}
}
```

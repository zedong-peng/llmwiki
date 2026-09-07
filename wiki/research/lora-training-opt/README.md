# LoRA Training Optimization Research

> 目标：在单卡 4090 / A100 上做出比 Unsloth 更快的 LoRA 训练框架

## 相关 Repo

- [unsloth](https://github.com/unslothai/unsloth) — `git clone --depth=1 https://github.com/unslothai/unsloth.git`
- [Liger-Kernel](https://github.com/linkedin/Liger-Kernel) — LinkedIn 出品的 Triton kernel 库
- [Chronicals](https://arxiv.org/abs/2601.02609) — 声称 3.51x over Unsloth 的新框架

## 文件索引

- [unsloth-internals.md](./unsloth-internals.md) — Unsloth 技术细节
- [landscape.md](./landscape.md) — 框架横向对比
- [bottlenecks.md](./bottlenecks.md) — LoRA 训练瓶颈分析
- [opportunities.md](./opportunities.md) — 可以超越 Unsloth 的方向
- [papers.md](./papers.md) — 相关论文

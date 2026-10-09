---
title: "InnoGym: Benchmarking the Innovation Potential of AI Agents"
domain: research
area: research-taste
type: note
status: active
updated: 2026-04-07
tags: [innovation, novelty, benchmark, research-agent, engineering]
arxiv: "2512.01822"
authors: [Jintian Zhang, Kewei Xu, Jingsheng Zheng, Zhuoyun Yu, Yuqi Zhu, Yujie Luo, Lanning Wei, Shuofei Qiao, Lun Du, Da Zheng, Shumin Deng, Huajun Chen, Ningyu Zhang]
venue: arXiv
year: 2024
---


> 未读资料：原页面来自网页检索摘要、会话引用或方案推演，未阅读论文原文，也没有代码核验记录。以下内容完整保留历史研究素材，数字、引文、方法归属和新颖性主张尚未核实；本次迁移不构成重新阅读或事实复核。
> 引用记录：[citation.bib](../assets/zhang-2024-innogym/citation.bib)。
> 元数据冲突：原页面 year=2024 与 arXiv 2512.01822 的编号年份不一致；保留原 frontmatter，引用年份暂不填写。
# InnoGym: Benchmarking the Innovation Potential of AI Agents

**arXiv:** https://arxiv.org/abs/2512.01822

## Abstract
True innovation depends not only on producing correct answers but also on the originality of the approach. InnoGym is the first benchmark and framework designed to systematically evaluate the innovation potential of AI agents, addressing the gap between creativity and effectiveness.

## Key Contributions
- First benchmark focused on **innovation potential** of AI agents
- Dual metrics: **performance gain** (does it work?) + **novelty** (is it different from prior approaches?)
- **iGym**: unified execution environment for reproducible, long-horizon evaluations
- 18 carefully curated tasks from real-world engineering and scientific domains

## Methodology
- Tasks span real-world engineering and scientific problems
- Novelty measured as methodological distance from prior approaches
- Performance gain measured against baselines
- Long-horizon evaluation: agents must sustain innovation over extended tasks

## Key Findings
- Separates "doing it correctly" from "doing it originally" — a crucial distinction
- Most AI agents can improve performance but struggle with genuine methodological novelty
- Highlights the gap between creativity and effectiveness in current AI systems

## Open Questions
- How do you objectively measure "methodological difference"? (Embedding distance? Human judges?)
- Is novelty-from-prior-work the right definition of innovation, or is novelty-to-the-world what matters?
- Can an agent be trained to be more innovative, or is this an emergent property?

## Connections
- [[research/research-taste/threads/research-ability-dimensions]] — novelty is one key dimension
- TastyBench（原引用条目已删除） — TastyBench measures impact prediction; InnoGym measures novelty generation
- [[research/research-taste/threads/benchmark-landscape]]

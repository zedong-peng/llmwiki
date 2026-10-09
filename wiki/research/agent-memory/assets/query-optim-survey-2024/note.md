---
title: "A Survey of Query Optimization in Large Language Models"
updated: 2026-10-09
---

# A Survey of Query Optimization in Large Language Models

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：正文 §1–§11 与 Limitations 已读完；参考文献只读到 Mo et al. 附近（约第 40 页），其余为引文列表，未逐条阅读。文本中图 1–6 只有提取出的文字标签，图形本身不可见；表格基本完整。BibTeX 记录标题为 "Survey on Query Optimization in LLMs"，arXiv:2412.17558（正文为 v3，2026-03）。

## Summary

作者（Tencent）综述 LLM / RAG 场景下的 query optimization（QO），核心问题是用户自然提问与检索器最优查询形式之间的语义鸿沟，以及 LLM 能答单个子问题却答不对组合问题的 compositionality gap（§1）。

贡献有三块：
- Query Optimization Lifecycle（QOL）：五阶段流程，即 Intent Recognition、Query Transformation、Retrieval Execution、Evidence Integration、Response Synthesis，加迭代反馈（§3.1，图 2）。
- Query Complexity Taxonomy：按证据类型（explicit/implicit）和证据数量（single/multiple）分四类，并把 Expansion、Decomposition、Disambiguation、Abstraction 四种原子操作映射到各类的主要策略（§3.2–3.3，图 3，Table 2）。例如 Class I 用 expansion，Class II 用 decomposition，Class III 用 disambiguation，Class IV 用 abstraction 加 decomposition。
- 四种操作的方法梳理（§4–§7，图 5 分类树，Table 3–6）：
  - Expansion 分 internal（Query2doc、HyDE、FLARE、Self-RAG、DeepRAG 等）和 external（DRAGIN、CSQE、RAG-DDR、REPLUG、RARE 等）。
  - Decomposition 分 sequential（Self-Ask、ReAct、IRCoT、CoRAG、RAG-Gym、Search-o1）和 parallel（Plan-and-Solve、Plan×RAG、RichRAG），另提到免分解的 GRITHopper。
  - Disambiguation 分 clarification（ToC、InfoCQR）和 feedback-driven（Rewrite-Retrieve-Read、AdaQR、MaFeRw、CRAG、Adaptive-RAG）。
  - Abstraction 分 conceptual（Step-Back、CoA、AoT）和 pattern-based（RuleRAG、GraphRAG、LightRAG、MemoRAG、TableRAG）。

§8 列出评测指标和数据集（NQ、TriviaQA、HotpotQA、2Wiki、MuSiQue、QReCC、TopiOCQA 等），并明确不提供跨论文的性能对比表，理由是模型、语料、指标、prompt 都不一致（§8.3）。§9 给出五条设计原则、四个跨方法趋势（reasoning-centric、process supervision、agentic 收敛、multi-modal）、决策流程图（图 6）和四个定性案例（Table 8、§9.4）。§10 的开放方向包括 query-centric process reward model、带中间标注的 benchmark、效率与质量权衡、多模态、个性化、理论基础。

## Evidence and Limits

- 这是纯文献综述，没有自己的实验、模型、硬件或基线。全文没有报告任何新的定量结果；各方法的效果描述只是转述原论文，多为"significantly""substantially"，没有数字。
- 检索范围：Semantic Scholar、DBLP、Google Scholar，限 ACL/EMNLP/NAACL/ICLR/NeurIPS/SIGIR/KDD/ECIR 等，2020 至 2026 年初；没有说明纳入/排除标准的细节，也没有统计纳入论文数量（§1）。许多被收录的方法是 arXiv 预印本（如 DMQR-RAG、RaFe、REAPER、QueryPlanner），与"premier venues"的说法不完全吻合。
- Taxonomy 到策略的映射（Table 2、图 3、图 6）没有实证检验，是作者的判断。案例（§9.4、Table 8）是示意性的，不是实测。
- 若干断言缺少证据：§6 称"analysis of real-world query logs"表明相当比例的歧义是真实的不确定性，但没有给出日志分析来源；§9.1 称组合操作的方法"consistently outperform"单操作方法，称 RAG-DDR、MaFeRw 的端到端信号"significantly outperform"启发式方法，也未给出对比数据；§4 的 "Semantic Signature Principle" 是对 HyDE 现象的解释性说法，没有验证。
- 分类边界较松：作者自己承认 CRAG、Adaptive-RAG、Speculative RAG、Think-then-Act 并非真正的 disambiguation（§6 Remark），GraphRAG 等被归入 abstraction 也是作者的重新定义（§7.2.3）。
- 自述局限（Limitations）：可能遗漏最新工作；只覆盖文本查询；缺少跨方法的计算成本实证比较。
- 与既有综述的对比（Table 1）只与三篇综述比较，且"只覆盖部分操作"的判断为作者主观标注。
- 正文未给出官方代码或资源库链接。

## Open Questions

- 四类查询的主策略映射是否在受控设置下成立？论文没有在同一 LLM、同一语料、同一检索器上比较各操作，无法判断映射是经验规律还是作者归纳。
- 方法间的收益能否分离？综述强调组合操作更好，但没有数据说明提升来自操作本身、更强的基座模型，还是额外的检索调用次数（效率指标在 §8 中被列出却没有被用于比较）。
- 作者提出的 query-centric PRM 与带中间标注的 benchmark 只是方向，没有给出可行的标注方案或原型，如何定义"好的中间查询"仍未解决。

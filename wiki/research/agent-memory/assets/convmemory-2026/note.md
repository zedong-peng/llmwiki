---
title: "ConvMemory: A Lightweight Learned Memory Reranker, a Negative Attribution Result, and a Research-Preview Conflict Editor"
updated: 2026-10-09
---

# ConvMemory: A Lightweight Learned Memory Reranker, a Negative Attribution Result, and a Research-Preview Conflict Editor

阅读者：Claude Sonnet 子 agent（2026-10-09），依据归档 PDF 的抽取文本；未经人工复核。

阅读范围：全文 PDF 文本（正文、附录 A、参考文献），共 15 页；无图，表格均可读，未见乱码。

## Summary

问题：对话式长期记忆检索中，cross-encoder 重排准确但在 top-500 候选上太慢；LLM-as-selector 成本随记忆量增长。论文问：一个很小的学习型 reranker 能多接近 cross-encoder，其增益来自什么机制（§1）。

方法：ConvMemory 约 3.6M 参数，在 dense 检索 top-500 候选上做重排。组件是对 dense 排序序列做滑动窗口 conv/mixer 编码（窗口 5、kernel 3）、query-候选的词法交互特征、一个可选 router 标量，以及 CE-lite 打分头（§3）。teacher 是 ms-marco-MiniLM-L-6-v2，损失为 pairwise ranking 加 first-rank 目标。候选侧 dense 向量与词法统计在写入时缓存，这是成本优势的来源（§3.4）。

主要结果：
- LongMemEval Clean500：Recall@10 为 0.9593，高于 BGE-large CE 的 0.8807（延迟低约 12.6 倍），比 mxbai-rerank-large-v1 的 0.9835 低 0.025（延迟低约 27.7 倍）（Table 2）。
- Stress1000（seed 23）：0.7386 对 BGE-large CE 0.6913，对 mxbai 0.8195；延迟比 mxbai 低约 117 倍。MRR 上两个 CE 都更好（Table 2，§4.1）。
- LoCoMo 5 seed：Recall@10 为 0.7798，高于 BGE-reranker-base 0.6967 和 large 0.7621，低于 mxbai 0.8080。MRR 0.5824 对 mxbai 0.6687（Table 3）。
- 换 BGE-large / E5-large 骨干（3 seed），Recall@10 相对 raw dense 提升 +0.1046 / +0.0892（Table 4）。

负结果（§5）：原先猜想滑动窗口隐式捕获时间结构。重训消融（3 seed）去掉词法特征降 0.089，去掉窗口降 0.035，router 约为 0（Table 5）。5 seed 配对 bootstrap 显示窗口增益在 HARD NON TEMPORAL（+0.0838）和 OTHER（+0.0868）上最大，在 T HOP 上不显著（+0.0096，CI 跨 0）（Table 6）。作者据此认为机制是融合 dense+词法空间里的廉价 CE 蒸馏，而不是时间结构。

CCGE-LA（§6）：在 ConvMemory 候选集上加一个小 transformer 编辑器，输入 18 个候选集特征，用 sigmoid gate（负偏置初始化）限制修正幅度，只用检索交叉熵训练。内部 5 seed 的 per-slice 最优变体在 FULL MRR 上 +0.0170，在 RESCUABLE STALE TOP1 上 +0.1019（Table 7）。发布的单 seed checkpoint 提升更小（Table 8）。

其他：从零训练的 GRU / transformer 流式 reranker 在 supersession 切片上低于 raw dense（T SUP R@10 0.28–0.31 对 0.50），说明在该规模下需要 teacher（§7，Table 9）。合成基准反复退化为 recency/位置等平凡基线可解（§8）。外部 OOD 检查中，QMSum 上有收益，MuSiQue 上低于 raw dense（Table 12）。

## Evidence and Limits

- 设置：骨干 all-mpnet-base-v2，单张 RTX 4080 SUPER，延迟只算重排阶段（不含 dense 检索与写入时缓存），CE 的 batch 大小按显存调到 32–128（§4.1，附录 A）。
- LongMemEval 数字是单次或单 seed（Stress1000 为 seed 23），无方差，作者自称只是 indicative；延迟也无方差条（附录 A）。
- 延迟优势部分依赖缓存词法统计的口径；高写入量场景需自行加上写入成本。CE 用原样 checkpoint，未做截断或蒸馏（附录 A）。
- LoCoMo 上的比较是 5 seed，证据较扎实；但 ConvMemory 在 LoCoMo 上训练、teacher 是小 CE，且仍不及 mxbai（Table 3）。
- 摘要说“在 BGE-large CE 之上”，Table 2 的 Clean500 里 BGE-large CE 的 Recall@10 低于 Raw MPNet（0.8807 对 0.9049），说明该 CE 作为基线本身偏弱。
- 负结果只针对 ConvMemory 的窗口与 LoCoMo，作者明确不外推；T SUP 切片上窗口增益显著，是否含时间信号仍未定论（§5）。
- Table 7 是各切片选最优变体后的“内部上界”，带选择偏差，不能当作单个模型的表现；发布的 checkpoint 为单 seed、单骨干、单任务（§6）。
- 无任何下游 QA 或端到端 agent 评测；单作者，未经独立审计（§10）。
- 代码与 checkpoint 公开，但 BGE/E5 版本未发布，逐题 CSV 与 embedding 缓存不提供（§12）。

## Open Questions

1. 检索阶段的 Recall@10 / MRR 优势能否转化为下游 QA 质量？论文没有测。
2. 窗口增益在 hard non-temporal 上最大，究竟是容量平滑，还是别的未识别结构？T SUP 上的显著增益如何归因？
3. 在 LongMemEval 上多 seed、多批大小设置下，延迟比与 Recall 差距是否稳定？

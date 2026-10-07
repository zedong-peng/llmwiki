# Step 4 - High-Potential Candidates

Timestamp: 2026-07-27

The following seven candidates were promoted after abstract triage. The cap is applied after considering the full combined broad + exact set.

1. **Predicting Retrieval Utility and Answer Quality in Retrieval-Augmented Generation** (Tian, Ganguly, Macdonald; ECIR 2026). The abstract defines utility as the with-context versus without-context performance gain, making it the closest semantic collision. Full chapter is subscription-gated.
2. **Distilling a Small Utility-Based Passage Selector to Enhance Retrieval-Augmented Generation** (Zhang et al.; SIGIR-AP 2025). Full PDF. It trains a small selector from LLM pseudo-answer/utility judgments and evaluates downstream answer EM/F1 and latency.
3. **Training a Utility-based Retriever Through Shared Context Attribution for Retrieval-Augmented Language Models** (Xu et al.; EMNLP 2025). Full ACL PDF. It estimates passage utility from downstream output changes under perturbation and trains a retriever.
4. **Retrieval as a Decision: Training-Free Adaptive Gating for Efficient RAG** (Wang, Wei, Ling; TMLR 2026). Full PDF. It gates retrieval using no-context reader uncertainty and explicitly analyzes paired with/without-RAG outcome differences.
5. **Cost-Aware Retrieval-Augmentation Reasoning Models with Adaptive Retrieval Depth** (Hashemi, Rühle, Rajmohan; arXiv preprint 2025). Full PDF. It trains dynamic retrieval depth with answer reward and memory/latency cost penalties.
6. **Learning to Rank for Multiple Retrieval-Augmented Models through Iterative Utility Maximization** (Salemi, Zamani; ICTIR 2025). Metadata/venue verified; ACM full text returned 403. The title and indexed record directly threaten utility-driven action selection among RAG branches.
7. **Consistent Estimators for Learning to Defer to an Expert** (Mozannar, Sontag; ICML 2020 / arXiv v3). Full PDF. It supplies the cost-sensitive action/defer formulation and warns that confidence-only deferral can be inconsistent with the joint system objective.

Adjacent but not promoted to the seven-paper deep dive: *Predict Responsibly* (NeurIPS 2018), *SelectiveNet* (ICML 2019), DeCCaF (TMLR 2024), *Stochastic RAG* (SIGIR 2024), and *Adaptive Retrieval Without Self-Knowledge?* (ACL 2025). They are included in the comparison and reading path where relevant.

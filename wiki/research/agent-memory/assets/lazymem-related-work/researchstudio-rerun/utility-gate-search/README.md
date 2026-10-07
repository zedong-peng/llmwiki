# Utility-Gated Retrieval Search

This folder is the narrow follow-up search for the question: what prior art already predicts or optimizes the downstream answer utility of an optional retrieval action, especially under explicit cost or deferral decisions?

## Search and evidence

- Broad Microsoft ResearchStudio search: four queries, 2015--2026, 137 unique records after 13 cross-source merges.
- Exact follow-up search: retrieval-utility prediction, iterative utility maximization, utility-based passage selection, and cost-sensitive deferral.
- Connectors queried: arXiv, DBLP, OpenAlex, OpenReview, Semantic Scholar, and Crossref.
- Full-text gate: official PDFs were downloaded and text-extracted for UtilityQwen, SCARLet, TARG, Cost-Aware Retrieval-Augmentation Reasoning, Consistent Estimators for Learning to Defer, Predict Responsibly, SelectiveNet, and cost-sensitive deferral; Tian et al. (ECIR 2026) is official abstract/metadata only; ICTIR utility ranking and Stochastic RAG metadata is verified but the ACM PDF returned HTTP 403.

`allinone.md` and `step3.md` contain the complete mechanically ranked search output and connector stderr. `step5.md` records the evidence-aware deep dive, and `step6.md`/`step7.md` are the conservative scoop assessment and proposed delta. The ranked tables are triage aids, not claims that every search hit is relevant; false positives from broad connector search are preserved for auditability.

## Main conclusion

The broad claim “use BM25 first and invoke semantic retrieval only when useful” is occupied by AgentIR and TARG-style adaptive gating. The closest direct utility collision is Tian, Ganguly, and Macdonald, whose abstract defines retrieval utility as with-context performance gain over no-context generation. UtilityQwen and SCARLet establish downstream utility as a training signal for passage selection/retriever learning, while action-aware deferral provides the formal cost-sensitive ancestor. A possible LazyMem delta therefore has to be narrower: a fixed BM25-versus-one-semantic intervention, matched reader/context/call budgets, a prespecified cost-adjusted answer-value lower bound, and a frozen cross-corpus falsification protocol. This remains a provisional high-overlap assessment until the ICTIR paper is obtained and the exact utility-prediction family is checked more deeply.

## Reproducibility

All connector output and errors are retained verbatim. Official full-text files are in `papers/`; the Springer abstract and landing page are retained separately because the chapter PDF was subscription-gated. No benchmark or model experiment was run as part of this search.

---
title: "HippoRAG: Neurobiologically Inspired Long-Term Memory for LLMs"
domain: research
area: misc
type: paper
status: processed
updated: 2026-04-18
tags: [paper, rag, graph, memory, retrieval, multi-hop]
---
# HippoRAG: Neurobiologically Inspired Long-Term Memory for LLMs

## Paper Meta
- Title: HippoRAG: Neurobiologically Inspired Long-Term Memory for LLMs
- Authors: Bernal Jiménez Gutiérrez, Yiheng Shu, Yu Gu, Michihiro Yasunaga, Yu Su
- Year: 2024
- Venue: NeurIPS 2024
- Topic: misc
- Paper Slug: hipporag-2024
- arXiv: https://arxiv.org/abs/2405.14831
- PDF: `2405.14831-hipporag.pdf`
- Code Repo: https://github.com/OSU-NLP-Group/HippoRAG
- Reading Source: TeX (`source/extracted/neurips_2024.tex` + `references.bib`)
- Repo Read: yes (`repo/main.py`, `repo/src/hipporag/HippoRAG.py`, `repo/src/hipporag/StandardRAG.py`)
- PDF Fallback: not used
- Legacy Note: [[agent-memory/papers/hipporag-2024]]

## TL;DR
- HippoRAG turns retrieval into a graph-search problem: it uses an LLM to extract OpenIE triples from passages, builds a schemaless KG, links query entities to KG nodes, and runs Personalized PageRank for single-step multi-hop retrieval.
- The method is strongest on knowledge-integration benchmarks. On the paper's 1,000-question dev subsets, it materially improves retrieval over BM25, Contriever, GTR, ColBERTv2, RAPTOR, Propositionizer, and IRCoT-style baselines.
- The main failure mode is a concept-context tradeoff. NER/OpenIE misses and graph-search errors dominate the error analysis, so the paper's gains come from structure, not end-to-end training.

## Problem
- Standard RAG encodes each passage in isolation, so it struggles when the answer requires stitching together facts across passage boundaries.
- This is especially visible in multi-hop QA and in the paper's "path-finding" cases, where a relevant passage is not lexically obvious from the query and must be recovered through associations.
- The paper frames long-term memory for LLMs as a continual indexing problem: new information should be absorbed without retraining the whole model.

## Method
- Offline indexing: an instruction-tuned LLM extracts named entities and OpenIE triples from each passage, producing a schemaless KG over the corpus. The KG acts as the paper's synthetic hippocampal index.
- Retrieval linking: the query is reduced to salient named entities, which are embedded and matched to KG nodes. Those nodes become seeds for Personalized PageRank.
- Graph completion: PPR spreads activation over the KG, letting the system recover relevant neighborhoods and rank passages by accumulated node probability.
- Node specificity: the paper adds an IDF-like local weighting term, defined as the reciprocal of the number of passages a node appears in, to downweight generic nodes without needing a global corpus aggregator.
- Neurobiology mapping: the paper explicitly maps neocortex to LLM-based extraction, parahippocampal regions to embedding-based linking, and hippocampus to KG + PPR retrieval.

## Benchmarks / Datasets
| Dataset | Dev questions | Passages | Unique nodes | Unique edges | Unique triples | Synonym edges |
|---|---:|---:|---:|---:|---:|---:|
| MuSiQue | 1,000 | 11,656 | 91,729 | 21,714 | 107,448 | 145,990 (Contriever) / 191,636 (ColBERTv2) |
| 2WikiMultiHopQA | 1,000 | 6,119 | 42,694 | 7,867 | 50,671 | 146,020 (Contriever) / 82,526 (ColBERTv2) |
| HotpotQA | 1,000 | 9,221 | 82,157 | 17,523 | 98,709 | 159,112 (Contriever) / 171,856 (ColBERTv2) |

## Baselines
| Baseline | Role | Notes |
|---|---|---|
| BM25 | Lexical retrieval | Strong classical sparse baseline. |
| Contriever | Dense retrieval | Main dense retriever in the paper. |
| GTR | Dense retrieval | Another strong dense retriever. |
| ColBERTv2 | Late-interaction retrieval | Best standalone dense baseline on HotpotQA. |
| Propositionizer | LLM-augmented retrieval | Rewrites passages into propositions. |
| RAPTOR | Hierarchical summary retrieval | Summarizes passages into summary nodes. |
| IRCoT | Iterative multi-step retrieval | Main iterative baseline; much slower and more expensive online. |

## Main Results
| Setting | Dataset | Metric | Baseline | HippoRAG | Delta |
|---|---|---:|---:|---:|---:|
| Single-step retrieval | MuSiQue | R@2 | ColBERTv2 37.9 | 40.9 | +3.0 |
| Single-step retrieval | MuSiQue | R@5 | ColBERTv2 49.2 | 51.9 | +2.7 |
| Single-step retrieval | 2Wiki | R@2 | ColBERTv2 59.2 | 70.7 | +11.5 |
| Single-step retrieval | 2Wiki | R@5 | ColBERTv2 68.2 | 89.1 | +20.9 |
| Single-step retrieval | HotpotQA | R@2 | ColBERTv2 64.7 | 60.5 | -4.2 |
| Single-step retrieval | HotpotQA | R@5 | ColBERTv2 79.3 | 77.7 | -1.6 |
| QA with ColBERTv2 retriever | MuSiQue | F1 | ColBERTv2 26.4 | 29.8 | +3.4 |
| QA with ColBERTv2 retriever | 2Wiki | F1 | ColBERTv2 43.3 | 59.5 | +16.2 |
| QA with ColBERTv2 retriever | HotpotQA | F1 | ColBERTv2 57.7 | 55.0 | -2.7 |
| IRCoT + HippoRAG | MuSiQue | R@5 | IRCoT + ColBERTv2 53.7 | 57.6 | +3.9 |
| IRCoT + HippoRAG | 2Wiki | R@5 | IRCoT + ColBERTv2 74.4 | 93.9 | +19.5 |
| IRCoT + HippoRAG | HotpotQA | R@5 | IRCoT + ColBERTv2 82.0 | 83.0 | +1.0 |

## Ablations / Analysis
- OpenIE matters a lot. REBEL produces far fewer nodes and edges than GPT-3.5 Turbo, and retrieval drops sharply when REBEL replaces the default extractor.
- Open-weight LLMs can work. Llama-3.1-8B is competitive on several settings, and Llama-3.1-70B is often close to or better than GPT-3.5 Turbo.
- PPR is doing real work. Replacing PPR with query nodes only, or query nodes plus direct neighbors, reduces retrieval substantially.
- Node specificity helps on MuSiQue and HotpotQA, while synonymy edges matter most on 2WikiMultiHopQA.
- Error analysis on 100 MuSiQue errors: NER limitation 48%, incorrect or missing OpenIE 28%, PPR 24%.
- OpenIE weakens on longer passages: CaRB F1 drops from 71.8 on the 10 shortest annotated passages to 53.9 on the 10 longest.
- Intrinsic OpenIE evaluation on 20 MuSiQue passages, 239 gold triples: GPT-3.5 Turbo AUC/Precision/Recall/F1 = 46.5/68.4/55.2/61.1; Llama-3.1-70B = 42.3/66.3/50.9/57.6; REBEL = 1.0/8.0/1.8/2.9.

## Implementation Clues
- The repo entry point is `repo/main.py`, which loads a corpus, indexes it, then runs retrieval and QA over all questions.
- The core class is `repo/src/hipporag/HippoRAG.py`. It wires together OpenIE, embedding stores, graph construction, and retrieval-time PPR.
- The repo also includes `repo/src/hipporag/StandardRAG.py`, which is a simpler dense-retrieval baseline, and `repo/main_dpr.py` uses that path.
- Default repo config differs from the paper experiments: `gpt-4o-mini` and `nvidia/NV-Embed-v2` are the code defaults, while the paper reports GPT-3.5 Turbo plus Contriever or ColBERTv2.
- Key config values in the code: `retrieval_top_k=200`, `linking_top_k=5`, `max_qa_steps=3`, `qa_top_k=5`, `graph_type=facts_and_sim_passage_node_unidirectional`, `openie_mode=online` by default.
- The codebase is organized for reproducible indexing: `EmbeddingStore` caches chunk/entity/fact embeddings, and `force_index_from_scratch` / `force_openie_from_scratch` control reuse.

## Limitations
- The method is not end-to-end trained. The paper explicitly leaves the extractor, encoder, and graph search components off-the-shelf.
- Most observed failures come from NER and OpenIE, which means the method is only as good as its query/entity extraction.
- HotpotQA is a weaker fit for the method because its distractors are less confounding, so the paper's gains there are smaller and sometimes negative.
- The paper's uncertainty ensemble can improve some settings, but it does not fix the concept-context tradeoff universally and can hurt 2WikiMultiHopQA.
- Scalability beyond the paper's benchmark sizes is still not validated.

## Takeaways
- HippoRAG is best read as a retrieval memory architecture, not just a QA trick.
- Its main contribution is to replace flat passage retrieval with graph-structured memory plus seeded diffusion.
- The strongest evidence is the 2Wiki gains and the complementary improvements when HippoRAG is plugged into IRCoT.
- The paper's "path-finding" examples show where graph associations matter more than literal lexical overlap.

## Open Questions
- How much of the benefit remains if OpenIE quality is reduced further or replaced with lighter extractors on larger corpora?
- Can relation-aware traversal beat plain PPR without adding too much latency or tuning complexity?
- Will the scheme still scale when the index grows far beyond the benchmark corpora used here?
- Can the concept-context tradeoff be solved without the uncertainty ensemble hurting some datasets?

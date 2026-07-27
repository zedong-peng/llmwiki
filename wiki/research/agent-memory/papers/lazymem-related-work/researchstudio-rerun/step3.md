# Step 3 - Abstract-Level Triage

Timestamp: 2026-07-27 (Asia/Shanghai)

Each record is compared with the four axes in [`step1.md`](step1.md). `Overlap` is the number of plausibly matching axes, not a final novelty verdict. `UA` means the connector supplied no usable abstract; those records are not dismissed when their title suggests mechanism overlap.

| ID | Title | Date | Problem framing | Core mechanism | Key insight | Domain | Overlap | Source |
|---|---|---|---|---|---|---|---:|---|
| A1 | Compress to Impress | 2024-02 | Long-term dialogue without retrieval DB | Compressive memory in one LM | Move work into compact memory | Chinese real-world dialogue | 2 | OpenAlex/arXiv |
| A2 | Beyond Retrieval: Embracing Compressive Memory | 2025 | Same work/repository record as A1 | Compressive memory | Compression replaces retrieval | Long-term dialogue | 2 | OpenAlex |
| A3 | Memory-augmented networks for context-aware dialogue | 2025-09 | Context-aware dialogue | Generic memory-augmented network | Persistent context helps responses | Dialogue systems | 1 | OpenAlex |
| A4 | Pre-Storage Reasoning for Episodic Memory | 2025-09 | Multi-session personalized dialogue | Extract typed fragments and cross-session relations at write time | Shift inference burden to storage | Personalized dialogue | 2 | OpenAlex/arXiv |
| A5 | Neural Cascade Decoding | 2024-11 | Decoding consistency | Cascade decoder | Multi-stage decoding | General LMs | 0 | OpenAlex |
| A6 | Hierarchical Aggregate Tree for RAG | 2024-06 | Long-conversation context selection | Conditional tree traversal over recursive aggregates | Hierarchy controls context breadth/depth | Long-form dialogue | 2 | OpenAlex/arXiv |
| A7 | Cognitive Ethical Memory Architecture | 2026-06 | Adaptive conversational memory | Cognitive/ethical architecture | Memory needs governance | Conversational AI | 1 | Crossref |
| A8 | Memory Fabric for Conversational AI Agents | unknown | Shared persistent agent memory | Cross-user memory fabric | Shared persistence | Conversational agents | 1 | Crossref |
| A9 | K-Lines Four-Memory Architecture | unknown | Persistent conversational memory | Four memory tiers | Cognitive specialization | Conversational AI | 1 | Crossref |
| A10 | Context and Time Sensitive Long-term Memory | 2024-05 | Ambiguous and temporal long-dialogue queries | Table-chain search, vector retrieval, query disambiguation | Conversational retrieval needs time and local context | Long-term dialogue QA | 2 | OpenAlex/arXiv |
| A11 | Comparative Analysis of Adaptive Memory Mechanisms | 2026-03 | Long-context conversational retrieval | UA; compares adaptive mechanisms | Adaptive memory may trade cost/quality | Conversational AI | 2 | Crossref |
| A12 | Eye movements and long-term memory retrieval | unknown | Human working memory | Eye-movement experiment | Attention and retrieval interact | Cognitive psychology | 0 | Crossref |
| A13 | Long-term retrieval does not bypass working memory | unknown | Human memory | Behavioral experiment | Retrieval still uses working memory | Cognitive psychology | 0 | Crossref |
| A14 | TA-Mem | 2026-03 | Long-term conversational QA | UA; tool-augmented autonomous retrieval | Retrieval can be delegated to tools | Conversational QA | 2 | Crossref |
| A15 | Hybrid Memory Architectures for Conversational AI | 2026 | Long-term context management | Vector DB plus RAG | Hybrid memory broadens coverage | Conversational AI | 2 | Crossref |
| A16 | Repetition Learning and Episodic Retrieval | unknown | Human learning | EEG experiment | Explicit episodic retrieval mediates repetition | Cognitive psychology | 0 | Crossref |
| A17 | In Prospect and Retrospect | 2025 | Long-term personalized dialogue | Reflective memory management | Prospective/retrospective reflection organizes memory | Dialogue agents | 2 | OpenAlex/ACL |
| A18 | Selective Prompting Tuning | 2024 | Personalized generation | Prompt tuning | Select prompts per user | Personalized dialogue | 1 | OpenAlex/ACL |
| A19 | Rewriting-Enhanced Inversion of Session Embedding | 2024 | Conversational dense retrieval interpretation | Query rewriting plus embedding inversion | Rewrites expose session embedding behavior | Conversational search | 1 | OpenAlex/ACL |
| A20 | DiSCo | 2025-07 | Efficient conversational search | Distill similarity scores into learned sparse retriever | Jointly distill context modeling and retrieval | Conversational search | 1 | OpenAlex/SIGIR |
| A21 | SHARE | 2025 | Shared-memory dialogue dataset | Dataset construction from movie scripts | Shared memories test dialogue grounding | Long-term dialogue | 1 | OpenAlex/ACL |
| A22 | Memorable Conversation Model with DPO | 2024-07 | Memorable conversation generation | DPO on a small LM | Preference tuning may retain context | Dialogue generation | 1 | OpenAlex/arXiv |
| A23 | Hybrid Memory in Healthcare | 2025 | Long-term assistant memory | Hybrid memory system | Domain memory needs scalable retrieval | Healthcare dialogue | 2 | OpenAlex |
| A24 | Efficient Selection for Dialogue State Tracking | 2024-06 | Select dialogue information for state tracking | Integrated-information selector | Selection reduces irrelevant history | Task dialogue | 1 | OpenAlex/IJCNN |
| A25 | Emotion-Tagged Graph Memory | unknown | Goal-aware long-term conversation | Emotion-tagged graph | Affect and goals guide recall | Conversational LMs | 1 | Crossref |
| A26 | Long-Term Memory Processes | 2025-03 | Human retrieval | Cognitive chapter | General account of retrieval | Cognitive psychology | 0 | Crossref |
| A27 | Efficient Memory Alignment for Conversational Information Seeking | 2026-07 | Long-term conversational search | UA; efficient memory alignment | Align memory to information need | Conversational search | 2 | Crossref/SIGIR |
| A28 | Telugu QA with BM25 and Dense Retrieval | 2026-05 | Multilingual document QA | Static BM25+dense hybrid | Sparse and dense signals complement | Telugu QA | 1 | Crossref |
| A29 | Connectivity-Adaptive Inference | unknown | Offline/online degradation | Connectivity router | Route compute by availability | General conversational AI | 0 | Crossref |
| A30 | Holistic Episodic Retrieval | unknown | Human episodic memory | Retrieval-practice experiment | Episodic retrieval is holistic | Cognitive psychology | 0 | Crossref |
| A31 | GRAIL-RAG | 2026-02 | Session-aware document QA | Multi-stage retrieval plus guardrails | Guard stages reduce unsupported answers | Document-grounded QA | 1 | Crossref |
| A32 | MERMAIDS | unknown | Multi-hop agentic RAG | Claim-evidence-source-time graph, evidence reuse cache, conflict-triggered re-retrieval | Reuse and conflict control stabilize multi-hop evidence | General multi-hop QA | 2 | Crossref |
| A33 | Evidence-Obligation Pool-Gated Retrieval | 2026-07 | Stable multi-cycle retrieval | LLM Warrant Judge plus turn-scoped evidence-obligation ledger | Similarity cannot decide semantic warrant; code should track obligation state | General agent retrieval | 3 | Crossref |
| A34 | ChatRetriever | 2024 | Robust conversational dense retrieval | Adapt an LLM as a dense retriever | LLM retrieval transfers across conversational search tasks | Conversational search | 1 | OpenAlex/EMNLP |
| A35 | Llama-2 Conversation Summarization | 2024-06 | Conversation summarization | Fine-tuning | Domain tuning improves summaries | Summarization | 0 | OpenAlex |
| A36 | Conversation Retrieval for DST | 2024 | Retrieve prior context for state tracking | Implicit text summaries | Summary representations improve retrieval efficiency | Task dialogue | 1 | OpenAlex/NAACL |
| A37 | Multi-pass Decoding for Document-Grounded Conversations | 2024-06 | Document-grounded response generation | Multi-pass decoder | Deliberation improves grounding | Document dialogue | 0 | OpenAlex |
| A38 | Adaptive Memory-Anchored Target Estimation | 2026-04 | Target tracking under false measurements | Event-triggered estimator | Adaptive observation processing | Sensors/control | 0 | Crossref |
| A39 | Iterative Cross-Fusion for Hash Retrieval | unknown | Cross-modal hashing | Multi-label fusion network | Iterative fusion aligns modalities | Cross-modal retrieval | 0 | Crossref |
| A40 | S2G-RAG | 2026 | Iterative retrieval QA | Structured sufficiency and gap judge | Retrieve against diagnosed missing evidence | General RAG QA | 3 | Crossref/ACL |
| A41 | Memory Updating after Episodic/Semantic Retrieval | unknown | Human memory updating | Behavioral experiment | Retrieval types share updating mechanisms | Cognitive psychology | 0 | Crossref |
| A42 | Iterative Retrieval for Multi-Modal Integration | unknown | Multi-modal generation | Iterative retrieval augmentation | Multiple cycles integrate modalities | Multi-modal RAG | 1 | Crossref |
| A43 | Financial Fraud Dialogue Network | 2024-12 | Fraud detection | Contrastive multimodal network | Calls contain fraud signals | Finance | 0 | OpenAlex |
| A44 | Conversational Text Extraction with RAG | 2024-12 | Text extraction | RAG pipeline | Retrieved text supports extraction | Information extraction | 0 | OpenAlex |
| A45 | Goal-oriented Document Dialogue with Evidence Generation | 2024-11 | Document-grounded dialogue | Evidence generation | Generate support before response | Document dialogue | 1 | OpenAlex |
| A46 | Dialogue Non-Quota Selection | 2025-04 | Dialogue-state sample selection | Loss-monitored multi-perspective selection | Training example quality matters | Dialogue state tracking | 0 | OpenAlex |
| A47 | Symbol-Rooted Cascade Propagation | 2025 | Contextual memory routing | UA; symbolic cascade | Structured roots may guide routes | General LMs | 2 | OpenAlex |
| A48 | Nonverbal Correlates of Conversation Memory | 2025-09 | Human conversation memory | Behavioral analysis | Nonverbal signals correlate with recall | Psychology | 0 | Crossref |
| A49 | Processing Level and Testing Effect | 2025-09 | Human learning | Behavioral experiment | Encoding/retrieval depth is asymmetric | Psychology | 0 | Crossref |
| A50 | Reasoning LMs for Dialogue Summarization | 2025-09 | Summarization evaluation | Model comparison | Reasoning may not help summaries | Summarization | 0 | OpenAlex |
| A51 | LLM-Guided Conversational Recommender | 2024 | Recommendation | Representation enhancement | LLM guidance improves recommendation | Recommenders | 0 | OpenAlex |
| A52 | Exemplar Selection against Catastrophic Forgetting | 2024 | Continual task dialogue | Exemplar selection | Rehearsal controls forgetting | Task dialogue training | 0 | OpenAlex |
| A53 | rbm25 Rust Wrapper | 2025-01 | Software package | BM25 wrapper | Implementation convenience | Software | 0 | Crossref |
| M1 | AgentIR | 2026-05 | Long-term conversational retrieval under latency | BM25 top-k-margin gate escalates to dense/RRF/recency | Dense has workload- and query-conditional value | LoCoMo, LongMemEval, BEIR | 4 | model-recall, verified arXiv PDF |
| M2 | Training-Free Lexical-Dense Fusion | 2026-06 | Conversational-memory retrieval | BM25 plus max-turn dense score fusion | Lexical/dense errors are category-dependent; fusion has a cross-corpus boundary | LoCoMo, LongMemEval-S | 3 | model-recall, verified arXiv PDF |
| M3 | SelRoute | 2026-04 | Long-term conversational retrieval | Deterministic query-type routing across lexical/semantic/hybrid/enriched paths | No single route wins across query types | LongMemEval and transfer datasets | 4 | model-recall, verified arXiv PDF |
| M4 | EviMem | 2026-04 | Long-term conversational evidence restoration | Sufficiency classifier diagnoses evidence gap and iteratively refines retrieval | Accumulated evidence, not score alone, should trigger repair | LoCoMo | 4 | model-recall, verified arXiv PDF |
| M5 | TierMem | 2026-02 | Cost-aware auditable memory QA | Summary-first sufficiency router escalates via provenance to immutable raw pages | Answer from the cheapest sufficient tier | LoCoMo, LongMemEval | 4 | model-recall, verified arXiv PDF |

## Triage observation

The API ranking itself is not a reliable novelty ranking: the five most dangerous works were absent because the high-signal connectors were rate-limited. The claim has at least four abstract-level full-axis collisions (M1, M3, M4, M5), while A33 and A40 introduce additional evidence-obligation and structured-gap formulations that warrant full-paper review.

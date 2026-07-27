# Step 4 - High-Potential Candidates

Timestamp: 2026-07-27 (Asia/Shanghai)

The candidate set is capped at seven papers. Selection prioritizes core-mechanism overlap, then same-domain recency and abstract ambiguity.

1. **AgentIR: A Workload-Adaptive Cascade Retrieval Substrate for Long-Term Conversational Memory**
   - Selected because it is the direct same-domain BM25-first confidence cascade: the lexical top-k margin decides whether dense retrieval is worth its cost.

2. **SelRoute: Query-Type-Aware Routing for Long-Term Conversational Memory Retrieval**
   - Selected because it routes among lexical, semantic, hybrid, and enriched pipelines using a cheap deterministic question-type signal.

3. **EviMem: Evidence-Gap-Driven Iterative Retrieval for Long-Term Conversational Memory**
   - Selected because it evaluates accumulated evidence sufficiency and triggers targeted retrieval repair in the same benchmark domain.

4. **From Lossy to Verified: A Provenance-Aware Tiered Memory for Agents (TierMem)**
   - Selected because it explicitly formulates cheapest-sufficient evidence routing and escalates through provenance to immutable raw logs.

5. **Training-Free Lexical-Dense Fusion for Conversational-Memory Retrieval**
   - Selected because it isolates the marginal value and cross-corpus boundary of the exact BM25/dense operation that a LazyMem cascade would gate.

6. **Evidence-Obligation Pool-Gated Retrieval: Stable Multi-Cycle Retrieval via Evidence Ledger and Warrant Judge**
   - Selected because its Warrant Judge and obligation lifecycle may subsume evidence-based fallback control even though the application domain is broader than conversational memory.

7. **S2G-RAG: Structured Sufficiency and Gap Judging for Iterative Retrieval-Augmented QA**
   - Selected because the title and accepted ACL 2026 metadata indicate direct mechanism overlap, but the API supplied no abstract; full text is required before assigning a verdict.

SmartSearch, Nano-Memory, DeferMem, MGRetrieval, and Fidelity Before Structure remain important related work, but they are not in this seven-paper deep-dive set because they overlap the raw-retrieval substrate or ranking stage more than the specific lexical-first marginal-utility gate.

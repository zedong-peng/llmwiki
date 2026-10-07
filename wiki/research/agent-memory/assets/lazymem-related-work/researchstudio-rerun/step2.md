# Step 2 - Search and Deduplicate

Timestamp: 2026-07-27 (Asia/Shanghai)

## Queries

1. Original problem: `budgeted long-term conversational memory raw dialogue retrieval`
2. Broad domain: `conversational memory BM25 dense adaptive cascade`
3. Method signature: `evidence sufficiency iterative retrieval multi-session dialogue memory`

## Search outcome

- Window: 2024-2026.
- Sources requested: arXiv, DBLP, OpenAlex, OpenReview, Semantic Scholar, Crossref.
- Raw source hits: OpenAlex 30, Crossref 30, all other sources 0 after connector errors.
- Deduplicated API set: 53 papers; 7 cross-source duplicate records merged.
- Abstracts available: 27 of 53.
- Filter: none. All records, including obvious off-topic results, were retained for transparent triage.

## Connector limitations

arXiv and Semantic Scholar exhausted their bounded retries with HTTP 429 errors. OpenReview returned rate-limit errors on two queries. The complete stderr is preserved in [`paper-search-errors.txt`](paper-search-errors.txt), and the structured OpenAlex/Crossref records are in [`paper-search-structured.json`](paper-search-structured.json).

## Memory-augmentation pass

Five non-overlapping papers were added from the already downloaded and full-text-verified official arXiv corpus:

1. AgentIR (arXiv:2605.25092)
2. Training-Free Lexical-Dense Fusion (arXiv:2606.04194)
3. SelRoute (arXiv:2604.02431)
4. EviMem (arXiv:2604.27695)
5. TierMem / From Lossy to Verified (arXiv:2602.17913)

The combined triage pool therefore contains 58 records. The complete ranked table, source provenance, model-knowledge additions, trends, frequencies, citation tables, and reading recommendations are preserved in [`allinone.md`](allinone.md).

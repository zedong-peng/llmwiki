# Step 2 - Search and Deduplicate

Timestamp: 2026-07-27

## Queries

Broad paper-search queries:

1. `retrieval augmented generation paired answer utility selective retrieval`
2. `cost sensitive adaptive retrieval learning to defer`
3. `retrieval gating downstream answer reward`
4. `selective retrieval distribution shift calibration`

Exact follow-up queries:

1. `Predicting Retrieval Utility and Answer Quality Retrieval-Augmented Generation`
2. `Learning to Rank Multiple Retrieval-Augmented Models Iterative Utility Maximization`
3. `Distilling Small Utility-Based Passage Selector`
4. `cost sensitive learning to defer expert`

## Search and deduplication results

- Broad pass: 137 cross-source-deduplicated records from arXiv (15), DBLP (0), OpenAlex (60), OpenReview (0), Semantic Scholar (15 in the formatted run; 8 in the structured rerun after rate limits), and Crossref (60); 13 cross-source duplicates were merged in the formatted run.
- Exact pass: 71 unique formatted records, with 14 cross-source duplicates merged.
- The complete broad report, exact output, structured JSON, ranked JSON, and connector stderr are in [`allinone.md`](allinone.md), `paper-search-structured.json`, `paper-search-ranked.json`, `exact-search-output.txt`, and the corresponding `*-errors.txt` files.
- Model-recall additions were limited to two verified papers: *Predict Responsibly* (official NeurIPS PDF) and *SelectiveNet* (official arXiv/ICML paper). No unverified model-recall paper is used as a blocking citation.

## Retrieval limitations

The arXiv connector hit 429/503/proxy errors after its first query; DBLP returned 500; OpenReview and Semantic Scholar returned rate-limit errors; OpenAlex returned 504 on some exact queries. These errors are retained verbatim. The full-text gate therefore uses official PDFs/HTML for the high-risk subset rather than treating connector coverage as exhaustive.

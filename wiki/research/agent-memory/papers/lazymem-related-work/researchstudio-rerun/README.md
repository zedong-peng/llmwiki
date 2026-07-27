# LazyMem ResearchStudio Rerun

This directory records the independent Microsoft ResearchStudio rerun performed on 2026-07-27. It supplements, but does not mutate, the parent frozen 45-paper arXiv corpus.

## Workflow outputs

- `allinone.md`: complete `paper-search` report with all 53 deduplicated API records, five separately verified core additions, trends, source errors, and reading order.
- `step1.md` through `step7.md`: the `scoop-check` novelty decomposition, abstract triage, high-risk selection, full-text deep dive, four-axis comparison, and final verdict.
- `paper-search-output.txt` and `paper-search-errors.txt`: raw human-readable connector output and failures.
- `paper-search-structured.json` and `paper-search-structured-errors.txt`: machine-readable search output and connector failures.
- `papers/`: official PDFs newly required by this rerun plus `pdftotext -layout` extractions.

## Newly downloaded papers

| File | Work | Official source | Evidence use |
|---|---|---|---|
| `papers/s2g-rag.pdf` | S2G-RAG, ACL 2026 | ACL Anthology, DOI `10.18653/v1/2026.acl-long.1185` | Full-text sufficiency/gap mechanism, matched ablation, calibration, and latency audit |
| `papers/targ.pdf` | Retrieval as a Decision (TARG), TMLR 2026 | arXiv `2511.09803` | Full-text uncertainty gate, paired retrieval-benefit model, error quadrants, and limitations audit |

AgentIR, SelRoute, EviMem, TierMem, and Training-Free Lexical--Dense Fusion already have verified official arXiv PDFs in the parent `pdfs/` directory, so they are not duplicated here.

PGR (`10.20944/preprints202607.1060.v1`) is not present as a PDF. Its official endpoint returned HTTP 403 after DOI resolution and bounded user-agent retries, and Crossref supplied no alternative official PDF. Every PGR statement in this rerun is therefore marked abstract-only.

## Search disclosure

The paper-search run requested arXiv, DBLP, OpenAlex, OpenReview, Semantic Scholar, and Crossref for three queries spanning budgeted conversational memory, lexical/dense routing, and evidence-sufficiency iteration. arXiv and Semantic Scholar rate-limited all three requests; two OpenReview requests were rate-limited; OpenAlex recovered from intermittent 504 responses; DBLP returned no matches. OpenAlex and Crossref yielded 60 source records and 53 unique records after seven duplicate merges. No returned record was silently removed from `allinone.md`.

IdeaSpark then ran a separate six-query map search through arXiv, OpenAlex, Semantic Scholar, and OpenReview. That run is preserved in the LazyMem repository under `ideaspark_run/lazymem-marginal-utility/`; its real-connector sentinel, 38-row literature table, 24-paper full-text cache, lineage, candidate, collision search, and final idea card remain separate from this Scoop audit.

## Verification

From this directory:

```bash
shasum -a 256 -c SHA256SUMS
pdfinfo papers/s2g-rag.pdf
pdfinfo papers/targ.pdf
wc -c papers/s2g-rag.txt papers/targ.txt
```

Cross-paper benchmark numbers are reported as each source states them. They are not directly comparable unless retrieval unit, corpus split, reader, prompt, context budget, call budget, judge, and abstention policy are matched.

# LazyMem Related-Work Corpus

This directory is a frozen literature corpus for evaluating the scientific position of LazyMem. It was assembled on 2026-07-27 from official arXiv records and PDFs. The corpus focuses on long-term conversational memory, raw-history retrieval, lexical and dense retrieval, query transformation, adaptive retrieval, evidence sufficiency, and evaluation methodology.

## Contents

- [`RELATED_WORK.md`](RELATED_WORK.md): detailed synthesis, novelty audit, and recommended experimental program.
- [`selection.tsv`](selection.tsv): 45-paper inclusion ledger with category, arXiv identifier, title, and inclusion rationale.
- [`arxiv_metadata.xml`](arxiv_metadata.xml): raw arXiv API metadata returned for the selected identifiers.
- [`pdfs/`](pdfs/): 45 official arXiv PDFs, named `<arxiv-id>-<slug>.pdf`.
- [`text/`](text/): `pdftotext -layout` extractions used for full-text checks.
- [`SHA256SUMS`](SHA256SUMS): checksums for the downloaded PDFs and source metadata.
- [`researchstudio-rerun/`](researchstudio-rerun/): independent Microsoft ResearchStudio rerun, including raw connector output, all-record abstract triage, seven-paper full-text scoop audit, S2G-RAG PDF/text, and the surviving-hypothesis falsification plan.
- [`researchstudio-rerun/utility-gate-search/`](researchstudio-rerun/utility-gate-search/): narrow follow-up on downstream answer utility, cost-aware retrieval, and learning-to-defer; includes 137-record search output, evidence-gated deep dive, and verified PDFs.

## Scope and selection rule

The collection is deliberately narrower than a general agent-memory survey. A work was included when it bears on at least one decision in LazyMem:

1. whether to preserve raw dialogue or write an abstraction;
2. what constitutes a credible lexical baseline;
3. whether dense retrieval, reranking, or query rewriting adds value beyond BM25;
4. when an expensive retrieval path should be invoked;
5. how to assemble sufficient multi-turn evidence under a context budget; or
6. how to compare memory systems without conflating retriever, reader, judge, and budget changes.

The set includes foundational IR and adaptive-RAG papers only where they define an essential control. It is not intended to cover every memory architecture or every RAG paper.

## Validation

At collection time:

- all 45 selected arXiv identifiers resolved;
- all 45 downloads were recognized as PDF files;
- every PDF had at least two pages;
- every PDF produced non-empty extracted text;
- title-token checks matched the arXiv metadata, with one small-caps extraction exception manually checked on the first page; and
- no partial download remained.

Several 2026 items are recent preprints. Their claims should be treated as reported evidence, not as settled results. Absolute benchmark scores should not be compared across papers unless the history subset, answer model, prompt, context budget, judge, and abstention policy match.

The ResearchStudio rerun is intentionally separate from the frozen 45-PDF arXiv set. Its ACL S2G-RAG and TMLR TARG artifacts plus API search logs are additional audit evidence, not retroactive members of `selection.tsv`; PGR remains metadata/abstract-only because its official PDF endpoint returned HTTP 403.

## Revalidation

From this directory:

```bash
shasum -a 256 -c SHA256SUMS
find pdfs -name '*.pdf' -exec pdfinfo {} \;
```

The first command verifies the frozen bytes. The second exposes document-level metadata and page counts for manual inspection.

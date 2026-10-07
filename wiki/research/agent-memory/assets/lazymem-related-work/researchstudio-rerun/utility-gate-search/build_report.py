#!/usr/bin/env python3
"""Build the complete paper-search and abstract-triage reports."""

from __future__ import annotations

import html
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
QUERIES = [
    "retrieval augmented generation paired answer utility selective retrieval",
    "cost sensitive adaptive retrieval learning to defer",
    "retrieval gating downstream answer reward",
    "selective retrieval distribution shift calibration",
]


def normalize_title(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def md(value: object) -> str:
    return clean(value).replace("|", "\\|")


def parse_cli(path: Path) -> list[dict]:
    records: list[dict] = []
    current: dict | None = None
    header = re.compile(r"^  \[(\d+)\] \(score (\d+)\)(?: \[survey\])? (.+)$")
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        match = header.match(line)
        if match:
            if current:
                records.append(current)
            current = {
                "rank": int(match.group(1)),
                "relevance_score": int(match.group(2)),
                "title": match.group(3).strip(),
                "authors": [],
                "year": None,
                "citation_count": 0,
                "venue": "",
                "found_in": [],
                "url": "",
                "abstract": "",
            }
            continue
        if not current:
            continue
        stripped = line.strip()
        if stripped.startswith("Authors:"):
            current["authors"] = [a.strip() for a in stripped[8:].replace("...", "").split(",") if a.strip()]
        elif stripped.startswith("Year:"):
            parsed = re.match(r"Year: (\S+)\s+Citations: (\d+)\s+Venue: ?(.*)", stripped)
            if parsed:
                current["year"] = None if parsed.group(1) == "None" else int(parsed.group(1))
                current["citation_count"] = int(parsed.group(2))
                current["venue"] = parsed.group(3).strip()
        elif stripped.startswith("Sources:"):
            current["found_in"] = stripped[8:].split()[0].split(",")
        elif stripped.startswith("URL:"):
            current["url"] = stripped[4:].strip()
    if current:
        records.append(current)
    return records


def infer_triage(record: dict) -> tuple[str, str, str, str, int]:
    title = clean(record.get("title"))
    abstract = clean(record.get("abstract"))
    text = f"{title} {abstract}".lower()

    if "retrieval-augmented" in text or "retrieval augmented" in text or " rag" in f" {text}":
        domain = "Retrieval-augmented generation or retrieval-augmented reasoning."
    elif "defer" in text or "reject option" in text or "selective prediction" in text:
        domain = "Selective prediction / learning-to-defer outside RAG."
    elif "retrieval" in text:
        domain = "Information retrieval outside the narrow RAG decision setting."
    else:
        domain = "Non-RAG result returned by broad lexical matching."

    framing = abstract[:360] if abstract else "Abstract unavailable; title-level triage only."
    mechanism = "Not recoverable safely from the available title/abstract."
    insight = "No narrow LazyMem claim inferred from metadata alone."
    score = 0

    utility_terms = any(term in text for term in ("retrieval utility", "answer quality", "downstream", "expected utility"))
    action_terms = any(term in text for term in ("gating", "gate", "adaptive retrieval", "defer", "routing", "retrieval depth"))
    cost_terms = any(term in text for term in ("cost-aware", "cost aware", "cost-sensitive", "latency", "budget"))
    shift_terms = any(term in text for term in ("distribution shift", "out-of-distribution", "calibration", "conformal"))

    if utility_terms:
        mechanism = "Uses or predicts downstream utility / answer-quality feedback for retrieval, selection, or evaluation."
        insight = "Topical relevance is not identical to a passage or retrieval action's downstream value."
        score = max(score, 2)
    if action_terms:
        mechanism = "Makes a conditional retrieval, routing, depth, or deferral decision."
        insight = "An expensive branch should be invoked selectively rather than uniformly."
        score = max(score, 2)
    if utility_terms and action_terms:
        score = 3
    if cost_terms:
        insight = "Decision quality must be evaluated jointly with the marginal resource or error cost."
        score = max(score, 2)
    if shift_terms and (action_terms or utility_terms):
        score = max(score, 2)
    if "retrieval as a decision" in text:
        score = 4
    if "predicting retrieval utility and answer quality" in text:
        score = 4

    return framing, mechanism, insight, domain, score


def render_table(records: list[dict]) -> list[str]:
    lines = [
        "| # | Title | Date | Venue | Citations | Score | Sources |",
        "|---:|---|---|---|---:|---:|---|",
    ]
    for index, record in enumerate(records, 1):
        title = md(record.get("title"))
        url = clean(record.get("url"))
        linked = f"[{title}]({url})" if url else title
        date = record.get("publication_date") or record.get("year") or "unknown"
        sources = ", ".join(record.get("found_in") or [record.get("source", "unknown")])
        lines.append(
            f"| {index} | {linked} | {md(date)} | {md(record.get('venue'))} | "
            f"{record.get('citation_count') or 0} | {record.get('relevance_score') or 0} | {md(sources)} |"
        )
    return lines


def main() -> None:
    structured_ranked = json.loads((ROOT / "paper-search-ranked.json").read_text(encoding="utf-8"))
    broad_cli = parse_cli(ROOT / "paper-search-output.txt")
    structured_by_title = {normalize_title(p.get("title", "")): p for p in structured_ranked}
    ranked = []
    for cli_record in broad_cli:
        structured = structured_by_title.get(normalize_title(cli_record.get("title", "")))
        if structured:
            structured["relevance_score"] = cli_record.get("relevance_score", structured.get("relevance_score", 0))
            ranked.append(structured)
        else:
            ranked.append(cli_record)
    exact = parse_cli(ROOT / "exact-search-output.txt")
    broad_titles = {normalize_title(p.get("title", "")) for p in ranked}
    exact_new = [p for p in exact if normalize_title(p.get("title", "")) not in broad_titles]
    combined = ranked + exact_new

    raw = json.loads((ROOT / "paper-search-structured.json").read_text(encoding="utf-8"))
    first_line = next(
        line for line in (ROOT / "paper-search-output.txt").read_text(encoding="utf-8").splitlines()
        if line.startswith("per-source hits:")
    )
    counts = {
        source: int(value)
        for source, value in re.findall(r"([a-z_]+)=(\d+)", first_line)
    }
    duplicate_count = sum(counts.values()) - len(ranked)

    tokens = re.findall(r"[a-z][a-z-]{3,}", " ".join(p.get("title", "") for p in ranked).lower())
    stop = {
        "with", "from", "using", "based", "under", "towards", "generation", "model", "models",
        "approach", "framework", "analysis", "prediction", "learning", "evaluation",
    }
    keywords = Counter(token for token in tokens if token not in stop).most_common(5)

    accepted = [
        p for p in ranked
        if clean(p.get("venue")) and not re.search(r"arxiv|ssrn|research square", clean(p.get("venue")), re.I)
    ]
    accepted.sort(key=lambda p: p.get("citation_count") or 0, reverse=True)

    by_author: dict[str, dict[str, int]] = defaultdict(lambda: {"papers": 0, "citations": 0})
    for paper in ranked:
        authors = paper.get("authors") or []
        if authors:
            by_author[authors[0]]["papers"] += 1
            by_author[authors[0]]["citations"] += paper.get("citation_count") or 0
    top_authors = sorted(by_author.items(), key=lambda item: item[1]["citations"], reverse=True)[:5]

    report = [
        "# Utility-Gated Retrieval Literature Search",
        "",
        "Generated from Microsoft ResearchStudio `paper-search`; no relevance cutoff was applied.",
        "",
        "## Search Configuration",
        "",
        f"- Year range: 2015--2026",
        f"- Broad queries: {'; '.join(QUERIES)}",
        "- Exact follow-up queries: retrieval-utility prediction, utility maximization across RAG models, utility-based passage selection, and cost-sensitive learning to defer.",
        "- Sources: arXiv, DBLP, OpenAlex, OpenReview, Semantic Scholar, Crossref, plus verified model recall.",
        "",
        "## Complete Broad Search Results",
        "",
        "Per-source hits: " + ", ".join(f"{key}={value}" for key, value in counts.items()) +
        f"; {len(ranked)} unique records; {duplicate_count} cross-source duplicates merged.",
        "",
        *render_table(ranked),
        "",
        "## Complete Exact-Query Follow-Up",
        "",
        f"The exact pass returned {len(exact)} unique ranked records. Records already present above remain visible here because this section preserves the exact-query output.",
        "",
        *render_table(exact),
        "",
        "## Model Knowledge (Verified Additions)",
        "",
        "| Title | Year | Venue | Verification | Relevance |",
        "|---|---:|---|---|---|",
        "| Predict Responsibly: Improving Fairness and Accuracy by Learning to Defer | 2018 | NeurIPS | Official proceedings PDF | Foundational action-aware deferral; confidence-only rejection is insufficient when the downstream decision-maker has heterogeneous skill. |",
        "| SelectiveNet: A Deep Neural Network with an Integrated Reject Option | 2019 | ICML | Official arXiv PDF / ICML paper | End-to-end risk--coverage optimization and post-training coverage calibration. |",
        "",
        "## Connector Errors (Verbatim)",
        "",
        "### Broad search",
        "",
        "```text",
        (ROOT / "paper-search-errors.txt").read_text(encoding="utf-8", errors="replace").rstrip(),
        "```",
        "",
        "### Structured rerun",
        "",
        "```text",
        (ROOT / "paper-search-structured-errors.txt").read_text(encoding="utf-8", errors="replace").rstrip(),
        "```",
        "",
        "### Exact follow-up",
        "",
        "```text",
        (ROOT / "exact-search-errors.txt").read_text(encoding="utf-8", errors="replace").rstrip(),
        "```",
        "",
        "## Summary",
        "",
        "### Overview",
        "",
        f"The broad pass yielded {len(ranked)} unique records and the exact pass yielded {len(exact)} records. The broad corpus is intentionally noisy; the exact pass and full-text gate identify the small set that actually bears on cost-adjusted retrieval decisions.",
        "",
        "### Trends",
        "",
        "The relevant line moves from generic reject-option and learning-to-defer objectives (2018--2020), to end-to-end downstream-utility retrieval training (2024--2025), and finally to explicit adaptive retrieval cost/benefit prediction and gating (2025--2026). Recent work increasingly separates relevance from downstream utility and reports answer-quality/cost frontiers rather than retrieval recall alone.",
        "",
        "### Key themes",
        "",
        "1. **Action-aware deferral:** optimize the joint system rather than threshold one model's confidence (Predict Responsibly; Consistent Estimators; DeCCaF).",
        "2. **Selective risk and calibration:** control coverage or deferral rate while minimizing retained risk (SelectiveNet and conformal descendants).",
        "3. **Utility-trained retrieval:** train retrievers/selectors from downstream generation changes rather than semantic relevance alone (Stochastic RAG, SCARLet, UtilityQwen).",
        "4. **Adaptive retrieval cost:** choose whether/how deeply to retrieve under token or latency cost (TARG and Dynamic Search-R1).",
        "5. **Direct utility prediction:** predict performance gain from with-context versus without-context generation (Tian et al., ECIR 2026).",
        "",
        "### Keywords Frequency",
        "",
        "| Keyword | Count |",
        "|---|---:|",
        *[f"| {word} | {count} |" for word, count in keywords],
        "",
        "### Most Cited by Accepted Paper",
        "",
        "This mechanical table spans the unfiltered broad set and therefore includes off-topic lexical matches.",
        "",
        "| Rank | Title | Year | Citations |",
        "|---:|---|---:|---:|",
        *[
            f"| {i} | {md(p.get('title'))} | {p.get('year') or 'unknown'} | {p.get('citation_count') or 0} |"
            for i, p in enumerate(accepted[:5], 1)
        ],
        "",
        "### Most Cited by First Author",
        "",
        "| Rank | Author | Papers in set | Total citations |",
        "|---:|---|---:|---:|",
        *[
            f"| {i} | {md(author)} | {stats['papers']} | {stats['citations']} |"
            for i, (author, stats) in enumerate(top_authors, 1)
        ],
        "",
        "### Recommendations for Reading",
        "",
        "1. *Predict Responsibly* (2018): foundational distinction between confidence rejection and action-aware deferral.",
        "2. *Consistent Estimators for Learning to Defer to an Expert* (2020): cost-sensitive formalization and consistency result.",
        "3. *Stochastic RAG* (2024): end-to-end expected-utility retrieval optimization.",
        "4. *Retrieval as a Decision* (2026): paired with/without-RAG benefit analysis and practical retrieve-or-skip gating.",
        "5. *Predicting Retrieval Utility and Answer Quality in RAG* (2026): the closest direct definition of utility as contextual performance gain.",
    ]
    (ROOT / "allinone.md").write_text("\n".join(report) + "\n", encoding="utf-8")

    triage = [
        "# Step 3 - Abstract-Level Triage",
        "",
        "Generated from all deduplicated broad-search records plus exact-query records not already present. Overlap scores are conservative metadata/abstract triage; only Step 5 full-text records support the final verdict.",
        "",
    ]
    for index, record in enumerate(combined, 1):
        framing, mechanism, insight, domain, score = infer_triage(record)
        source = record.get("url") or record.get("doi") or record.get("arxiv_id") or "unresolved"
        triage.extend([
            f"## {index}. {md(record.get('title'))}",
            "",
            f"- **Title:** {md(record.get('title'))}",
            f"- **Date:** {record.get('publication_date') or record.get('year') or 'unknown'}",
            f"- **Problem framing:** {md(framing)}",
            f"- **Core mechanism:** {md(mechanism)}",
            f"- **Key insight:** {md(insight)}",
            f"- **Application domain:** {md(domain)}",
            f"- **Overlap score:** {score}/4",
            f"- **Source:** {source}",
            "",
        ])
    (ROOT / "step3.md").write_text("\n".join(triage), encoding="utf-8")


if __name__ == "__main__":
    main()

# Super Personal Wiki Schema

This repository is a long-lived personal wiki maintained by LLM agents.

## Purpose

Build a persistent, interlinked knowledge base across:

- personal records and life administration
- research maps, papers, ideas, experiments, and project history
- career materials, CVs, internships, certificates, applications
- code/project notes from sibling GitHub repositories
- durable summaries extracted from raw documents

The wiki should compound over time. Do not merely answer a question in chat when the result is durable; file useful synthesis back into `wiki/`.

## Directory Structure

```text
llmwiki/
├── AGENTS.md
├── README.md
├── inbox/
│   └── README.md
├── raw/
│   └── README.md
├── sources/
│   └── catalog.md
└── wiki/
    ├── index.md
    ├── log.md
    ├── personal/
    │   └── overview.md
    ├── research/
    │   └── overview.md
    ├── projects/
    │   └── overview.md
    └── admin/
        └── overview.md
```

## Privacy Rules

- Never copy highly sensitive documents into this repo unless the user explicitly asks.
- Sensitive examples include ID cards, passport scans, bank cards, household registration, transcripts, contracts, medical records, recovery codes, and visa documents.
- For sensitive sources, create metadata pages only: what the document is, where it lives locally, what it is used for, dates, and caveats.
- Avoid exposing secret values, account numbers, government ID numbers, passport numbers, phone numbers, addresses, and API keys.
- Prefer references to local folder categories over exact sensitive filenames when a public-facing page would be risky.

## Page Frontmatter

Use YAML frontmatter for durable wiki pages:

```yaml
---
title: Page Title
domain: personal | research | projects | admin
area: optional-area-slug
type: overview | source | concept | paper | comparison | engineering | project | person | timeline | checklist | synthesis | note
status: seed | active | stable | stale
updated: YYYY-MM-DD
tags: []
---
```

Research pages commonly use:

- `type: paper` for paper notes
- `type: comparison` for landscape tables
- `type: engineering` for implementation analysis
- `type: note` for imported working notes or session transcripts

## Linking Conventions

- Use Obsidian-style links: `[[page-name]]` or `[[folder/page-name]]`.
- Prefer stable lowercase filenames with hyphens.
- Preserve existing historical slugs unless there is a concrete reason to rename them and update backlinks.
- Every new durable page should be reachable from `wiki/index.md`.
- Cross-domain links are encouraged when they represent real context, for example a research project linked to a CV item.

## Workflows

### Ingest a Source

1. Identify the source and classify sensitivity.
2. If sensitive, summarize metadata only unless explicitly instructed otherwise.
3. Create or update the relevant domain page under `wiki/`.
4. Update `wiki/index.md`.
5. Append one entry to `wiki/log.md`.

### Merge Existing Research Wiki

1. Preserve the existing research area names where possible.
2. Move or copy durable research pages under `wiki/research/`.
3. Update links to remain Obsidian-compatible.
4. Add cross-domain links only when useful, such as CV, publications, thesis, internships, and project pages.
5. Append the migration to `wiki/log.md`.

### Answer a Query

1. Read `wiki/index.md` first.
2. Search relevant pages with `rg`.
3. Answer from the wiki and cite local page paths.
4. If the answer is durable, offer or perform a wiki update.

### Lint

Check for orphan pages, broken links, stale pages, inconsistent frontmatter, duplicated concepts, sensitive information leakage, and missing index entries.

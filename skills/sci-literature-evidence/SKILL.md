---
name: sci-literature-evidence
description: >
  Build a verified literature and evidence base for scientific writing. Use to search and screen literature (OpenAlex, Crossref, Semantic Scholar, Unpaywall, Europe PMC), download open-access full texts with identity checks, and organise a local PDF library with Excel and CSV tables. Use to extract page-marked text, build page-cited evidence tables with verbatim quotes and evidence levels, and verify DOIs and metadata against Crossref. Use to audit a manuscript for mis-cited references, wrong numbers, or claims attributed to papers that do not contain them. 文献检索, 文献库整理, 证据表, 引文核查, DOI 核验, 数据溯源. Not for writing prose; hand results to sci-prose-style or sci-writing-orchestrator.
---

# Literature and Evidence

Every number and every attribution in a manuscript must be traceable to a page of a source that was actually read. This skill produces the materials that make that possible: a curated library, page-marked full texts, evidence tables with verbatim quotes, and a Crossref-verified reference database.

## Operating Rules

1. A claim is only as good as the page it comes from. Record the PDF page of every quote.
2. Quote verbatim. Only ligature repair, hyphen joining across line breaks, and whitespace collapse are allowed.
3. Label every value with its evidence level: `measured`, `simulated`, `projected`, `estimated`, `reported-survey` (a review restating another paper), or `abstract-only`.
4. Label every performance, cost or effect value with its accounting scope (the unit it is counted over: a component, a sample, a cohort, a site, a whole system), what is included and excluded, and the test conditions the source states (e.g. temperature, dose, dataset, sample size, model, region). [comparison-fairness.md](references/comparison-fairness.md) gives the scope ladder.
5. Verify every DOI against Crossref before it enters the reference list. A DOI that resolves to a different paper is removed, never cited.
6. A review that restates a primary result is cited as the review; the primary paper is cited only after its own text has been checked.
7. When a claim cannot be found in the attributed source, say so and remove or re-attribute it. Do not keep a citation that only looks plausible.
8. Never bypass paywalls or publisher verification. Record every download attempt.

## Workflow

### 1. Scope and search
Read [search-protocol.md](references/search-protocol.md). Write the query plan (topics × synonyms × date window × document type), run it against OpenAlex first (broad, free, abstracts as inverted index), then fill gaps with Crossref and Semantic Scholar. Keep raw API responses in `search_cache/`.

```bash
python3 scripts/search_openalex.py plan.json --out search/ --mailto you@uni.edu   # set OPENALEX_API_KEY if the shared quota is used up
```

It writes `search_results.json` and a `candidates.csv` screening sheet (UTF-8 BOM) with a `decision` column that the download script reads.

### 2. Screen and curate
Screen by title and abstract in `candidates.csv`: fill `decision` (include or exclude, with the reason in `note_zh` for exclusions), `category` and the Chinese positioning note `note_zh`. Then assign stable ids (R### review, P### primary, X### preprint) and category folders:

```bash
python3 scripts/build_library_tables.py assign search/candidates.csv --library <Topic>_Library/
```

This writes `library_plan.csv` and `selection_manifest.json`. Check the rows whose `kind_basis` ends in "(check)"; an optional `kind` column (R, P or X) in the candidates sheet overrides the guess. Ids already in the plan are kept on later runs. See [library-layout.md](references/library-layout.md) for the folder scheme and the deliverables.

### 3. Retrieve full texts

```bash
python3 scripts/fetch_open_access.py <Topic>_Library/library_plan.csv --out <Topic>_Library/ --email you@uni.edu
python3 scripts/build_library_tables.py tables --library <Topic>_Library/
```

The second command writes the Excel master table, the UTF-8-BOM CSVs of all, downloaded and not-downloaded papers, the catalogue, the entry-point list for papers without a PDF, the PDF integrity report and a README draft.

Sequential downloads only, through publisher open-access patterns, OpenAlex, Unpaywall, Crossref links, Europe PMC, Semantic Scholar, OpenAIRE and landing-page PDF links. A PDF is accepted only after identity checks (title fuzzy match ≥ 84, or DOI plus ≥ 75% title tokens; ≥ 2 pages; not supplementary; more text than an abstract; first and last pages render). Every attempt goes to `download_attempts.jsonl`. Bot-protection pages are logged and never bypassed; list those papers with their DOI for manual or library download. A missing PDF is not evidence that a paper is closed.

Before adapting any published figure, check its licence:

```bash
python3 scripts/license_check.py 10.1038/s41467-024-45670-9 10.1002/adma.202312783 --out licences.csv
```

CC BY content can be adapted with attribution; CC BY-NC/ND and publisher-licensed content usually needs permission (RightsLink) for a commercial journal.

### 4. Extract text

```bash
python3 scripts/extract_pdf_text.py LIBRARY_DIR --recursive --digest --out source_audit/
```

Produces `<id>.txt` with `=== PAGE n ===` markers, `<id>.digest.md` (headings, abstract, introduction opening, sample body paragraphs, all figure/table/box captions, closing section) and `manifest.json` with SHA-256, pages, DOI, publisher and type guess. Duplicates are skipped by hash.

### 5. Build evidence tables
Read [evidence-table-contract.md](references/evidence-table-contract.md). Fan out: one sub-agent per group of 5–10 sources, each writing `evidence_<group>.json`. Each record carries key, value, unit, metric, entity, paper, source_file, page, verbatim quote, evidence level, accounting scope, notes. Then run:

```bash
python3 scripts/verify_evidence_quotes.py source_audit/evidence_*.json --text-dir source_audit/
```

which re-finds every quote on its stated page and reports mismatches. Fix or delete every failing record before writing.

### 6. Verify references

```bash
python3 scripts/crossref_verify.py keys.json --out references_verified.json --emit-references references.json
```

`keys.json` maps citation keys to DOIs (optionally with the claimed title). The script records authors, container, year (print year first), volume, issue, pages or article number, and flags `title_match = mismatch` when the DOI points to a different paper. Conference papers, book chapters and preprints without Crossref records go in as `manual` entries transcribed from the PDF itself. Read [citation-audit.md](references/citation-audit.md) for the checks that follow (orphan and unused keys, attribution tests, year and venue corrections such as ISCA vs ASPLOS).

### 7. Audit an existing manuscript
For revisions, check before writing:
- each citation number against the list (off-by-one shifts are common after insertions);
- each attributed claim against the cited paper's text (search the `.txt`);
- each number against its source page, including what it measures (e.g. within-sample vs between-sample variation, a per-step vs a per-run value, a subgroup vs the whole cohort);
- each performance or cost value for its accounting scope and test conditions;
- simulated results presented as measured;
- numbers with no source at all (e.g. a percentage range that appears in no paper).

Report findings as a table: location, claim, source check, verdict, fix.

## Delegation

Fan-out pays off at this stage. Split the work by source group (target-subject primary papers, comparators, reviews) or by task (evidence extraction, DOI verification, manuscript audit). Give each sub-agent the exact output schema, the verbatim rule, the page rule, and the instruction to validate its own JSON and quotes before returning. Merge and re-verify centrally.

## Outputs

- `<Topic>_Library/` with category folders, `library_plan.csv`, `selection_manifest.json`, `download_attempts.jsonl`, master Excel and CSVs, catalogue, integrity report, README (from `build_library_tables.py`)
- `source_audit/` with page-marked texts, digests, `manifest.json`
- `evidence_*.json` (verified quotes), `references_verified.json`, `references.json`
- an audit table for revisions, and a short list of claims marked `[to verify]`

## References

- [search-protocol.md](references/search-protocol.md): query design, APIs, screening, deduplication
- [library-layout.md](references/library-layout.md): folders, ids, deliverables, integrity report
- [evidence-table-contract.md](references/evidence-table-contract.md): record schema, evidence levels, scope vocabulary
- [citation-audit.md](references/citation-audit.md): reference verification and manuscript attribution audit
- [comparison-fairness.md](references/comparison-fairness.md): comparing technologies without misleading the reader

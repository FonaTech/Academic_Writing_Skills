---
name: sci-literature-evidence
description: >
  Search and curate scientific literature, verify source identity and citations, and maintain claim-level evidence and provenance for literature, original data and derived quantities. 文献检索、证据表、引用核查、数据溯源。 Use for evidence work, not prose drafting or statistical analysis itself.
---

# Evidence and provenance

Build a checkable link from each substantive claim to the evidence that supports it. Bibliographic identity, quote accuracy, study validity and claim support are separate checks.

## Workflow
1. Define a query plan, dates, inclusion/exclusion criteria and sources suited to the field. Save raw searches and screening decisions. Seek contrary findings; do not select only evidence for a preferred conclusion.
2. Resolve source identity from title, authors and identifier. Use primary studies for primary results; a review is a secondary source until its cited original is actually checked. Register metadata through Crossref, DataCite or the appropriate archive; a real DOI is not proof of a correct claim. Check corrections/retractions and record the check date.
3. Retrieve legal full texts and extract page-marked text. Keep exact file identity, version and hash. OCR and table extraction require visual verification. Missing access is an unresolved limitation.
4. Create stable evidence records using [evidence-table-contract.md](references/evidence-table-contract.md). Literature has complete quotes and exact page ranges; original/derived results have file hashes, locators, methods/code and input records.
5. Re-find full quotes with `scripts/verify_evidence_quotes.py`. Decimals, signs, units and exponents are never discarded to obtain a match. Missing records and wrong pages fail. A repaired page must be reviewed.
6. Bind each quantitative manuscript claim to an individual evidence key, with value, unit, metric, object, method and an exact source-text anchor. Verify the scientific relationship manually; token matching alone cannot establish it.
7. Report coverage and remaining gaps. Do not mark an evidence record verified solely because an agent produced it.

Separate `result_method` (measured/simulated/estimated/projected/inferred; synthetic for labeled artificial test data), `source_role` (primary/secondary/original), `access_status` (full-text/abstract-only/raw-files) and `verification` (pending/verified). An abstract may describe measurements; a review may describe simulations.

Use [search-protocol.md](references/search-protocol.md) for general searching and [systematic-review-method.md](references/systematic-review-method.md) only for systematic/scoping work. [comparison-fairness.md](references/comparison-fairness.md) gives domain-specific metric examples; choose comparable populations, tasks, conditions and accounting scopes for the current field.

## Tools
Existing search, retrieval and library tools remain available. Their heuristics can miss or reject sources; inspect ambiguous results. `crossref_verify.py` is a Crossref-specific helper, not the only legitimate identifier route. Manual/non-Crossref entries need documented identity and metadata checks.

```bash
python3 scripts/extract_pdf_text.py LIBRARY_DIR --recursive --out source_audit/
python3 scripts/verify_evidence_quotes.py evidence/literature.json --text-dir source_audit/
python3 scripts/crossref_verify.py keys.json --out references_verified.json --emit-references references.json
```

Do not bypass access controls. Do not infer research quality from venue, citation count or successful download. If sources fan out, use scoped extraction and independent refutation when available, then verify the records centrally.

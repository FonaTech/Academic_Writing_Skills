# Library layout and deliverables

```text
<Topic>_Library/
  README.md                      scope, search date, counts, reading route, caveats
  01_综述与观点/<category>/        R###_<slug>.pdf   reviews and perspectives
  02_原始研究/<category>/          P###_<slug>.pdf   primary research
  03_预印本/<category>/            X###_<slug>.pdf   preprints (linked to published versions)
  <Topic>_文献库.xlsx             master table: category sheets, Chinese note, English abstract, DOI, local link
  全部文献.csv / 已下载文献.csv / 未下载文献.csv   UTF-8 with BOM so Excel opens Chinese correctly
  文献目录.md                      catalogue by category with one-line notes
  未下载文献_入口与摘要.md          closed papers: DOI, entry links, abstract
  PDF完整性报告.csv                title match score, pages, SHA-256, render check
  search_queries.json, search_cache/, search_results.json   reproducible search
  selection_manifest.json        screening decisions and categories
  library.json                   final metadata, local paths, download attempts, status
  download_attempts.jsonl        every retrieval attempt
  source_audit/                  page-marked texts, digests, evidence tables (extract_pdf_text.py)
```

## Producing the deliverables

`scripts/build_library_tables.py assign` gives included candidates their ids and folders (`library_plan.csv`, `selection_manifest.json`). `scripts/fetch_open_access.py` then downloads into those folders. `scripts/build_library_tables.py tables` writes the CSVs, the xlsx (an overview sheet, one sheet for all papers and one per type and category, with DOI and local-file links), `文献目录.md`, `未下载文献_入口与摘要.md`, `PDF完整性报告.csv`, `library.json` and `README_draft.md`. The draft is written only when no README.md exists; fill in scope, search date and reading route by hand. Entry points list the DOI, OpenAlex and open-access links and the download URLs tried; API calls, which carry the contact e-mail, are left out.

## README essentials
- counts by type (reviews, primary, preprints), downloaded vs not;
- a suggested reading route (foundational review → key primary papers → extensions);
- what the Chinese notes are based on (title and abstract, not a full quality review);
- that "not downloaded" does not mean closed, and that no paywall was bypassed;
- that citation counts are snapshots on the search date.

## Identifiers
R### reviews, P### primary, X### preprints, C### comparators (optional). Keep ids stable; manuscript evidence records refer to them.

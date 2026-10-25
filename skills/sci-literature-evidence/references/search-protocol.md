# Literature search protocol

## 1 Query plan
Write the plan before searching and keep it with the library (`search_queries.json`):

| Field | Example |
|---|---|
| topic groups | one group per section or question of the manuscript, e.g. "⟨subject⟩ for ⟨application A⟩", "⟨subject⟩ for ⟨application B⟩", "comparators for ⟨application A⟩" |
| synonyms per group | every name the community uses for the concept, including older and regional terms and abbreviations |
| subject anchors | the target subject's names, spellings and abbreviations, used as a must-match filter |
| date window | 2016–present for primary work; reviews 2020–present |
| document types | review, perspective, article, conference papers of the field's main meetings, preprints |
| exclusion rules | e.g. papers below the level a section discusses; languages not covered; duplicates of a preprint |

## 2 Sources, in order
1. **OpenAlex** (`api.openalex.org/works?search=...&filter=from_publication_date:...,type:...`): broad coverage, abstracts as inverted index, open-access locations, citation counts. Use a polite `mailto`. Page with `per-page=100`.
2. **Crossref** (`api.crossref.org/works?query.bibliographic=...`): metadata authority for DOIs, volumes, pages; weaker abstracts.
3. **Semantic Scholar** (`api.semanticscholar.org/graph/v1/paper/search`): good for conference papers and `openAccessPdf`.
4. **Europe PMC** and **PubMed** for life-science and clinical topics; field databases (for example ADS, INSPIRE, SSRN, RePEc, ERIC, dblp) where they exist; **arXiv** for preprints (record the published version when it exists).
5. Backward and forward citation chasing from the three to five most relevant reviews.

Cache raw responses (`search_cache/`); record query, date, count and API for each run.

## 3 Screening
- Title and abstract screening into `selection_manifest.json` with id, DOI, category, priority (core / extension), and a one-line Chinese positioning note.
- Keep excluded candidates with the reason; the final count is the curated list, not the raw hit count.
- Tag each paper by role: `review`, `primary`, `preprint`, `comparator` (non-target technology used for context), `method`.
- Link a preprint and its published version as one study.

## 4 Retrieval
- Concurrency 1. Try in order: publisher open-access PDF, OpenAlex `oa_url` and locations, Unpaywall `best_oa_location`, Europe PMC, Semantic Scholar `openAccessPdf`, OpenAIRE, institutional repositories.
- Accept a PDF only after identity checks: title fuzzy match ≥ 84 (or DOI plus ≥ 75% of title tokens), ≥ 2 pages, body text longer than an abstract, first and last pages render.
- Log every attempt (`download_attempts.jsonl`: time, DOI, URL, status, detail). Record SHA-256 and page count in `PDF完整性报告.csv` or equivalent.
- Do not bypass paywalls, captchas or publisher verification. For closed papers, list the DOI and the entry points in `未下载文献_入口与摘要.md` so the group can obtain them through the library.

## 5 Minimum coverage for a review section
- the two to four foundational papers for the mechanism or architecture;
- all target-subject papers at the level the section discusses;
- the strongest non-target comparators per application, with their accounting scope;
- the most recent reviews on the topic (to position the review and avoid duplicating them);
- benchmark, guideline or survey papers that define the metrics and their required values.

## 6 Reporting
State in a methods note or the cover letter only if the journal asks: the search date, databases, query groups and inclusion rules. Never narrate the screening in the review text itself (sci-writing-orchestrator, review-architecture.md, section 2). In the revision notes, list papers used at abstract level only.

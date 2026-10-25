# Evidence table contract

An evidence table is a JSON object mapping a stable key to one record. The manuscript may only state a number that some record supports.

```json
{
  "smith2024.metric_a.setting1": {
    "key": "smith2024.metric_a.setting1",
    "value": "12.3",
    "unit": "unit per event",
    "metric": "metric A at setting 1 (what is measured, in words)",
    "entity": "the system, sample, cohort or model the value belongs to",
    "paper": "smith2024",
    "source_file": "smith2024_short_title.txt",
    "page": 7,
    "quote": "verbatim sentence from page 7 that contains 12.3 ...",
    "exp_or_sim": "measured",
    "accounting_scope": "module level, including its interfaces; host excluded",
    "notes": "the same paper reports 4.1 at setting 3; the task-level result is simulated"
  }
}
```

## Fields
| Field | Rule |
|---|---|
| key | `<paper>.<metric group>.<metric>[.<qualifier>]`, lower case, stable |
| value | as printed in the source (keep significant figures); ranges as "59–405" |
| unit | as printed; normalise only in the manuscript |
| metric | what is measured, in words |
| entity | the unit, sample, cohort, system or model the value belongs to |
| paper | reference key used in the manuscript |
| source_file, page | page-marked text file and PDF page number from `=== PAGE n ===` |
| quote | verbatim sentence; ligature, hyphenation and whitespace repair only |
| exp_or_sim | measured, simulated, projected, estimated, reported-survey, abstract-only |
| accounting_scope | the level on the project's scope ladder (comparison-fairness.md, section 1) and what is included |
| notes | caveats, related values under stricter scope, inconsistencies inside the paper |

## Coverage per source
- primary papers: technology and node; scale and yield; task and dataset with accuracy; energy or efficiency with scope; speed or latency; converter strategy; the authors' stated limitations;
- reviews and surveys: every quantified statement used in the manuscript, attributed to the original source when the review names it;
- record both a headline value and any stricter-scope value the paper gives (e.g. system vs electronic-only efficiency).

## Workflow
1. Fan out extraction by source group; each agent writes one file and runs a self-check.
2. Run `verify_evidence_quotes.py` on all files; fix page numbers with `--fix-pages` after inspection; remove records whose quotes cannot be found.
3. Merge into `evidence/` of the manuscript project. Keep a `sources.md` that lists which records support which paragraph when a section is dense with numbers.

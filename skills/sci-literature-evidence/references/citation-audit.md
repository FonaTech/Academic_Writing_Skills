# Citation audit

## Reference-list checks
- **DOI identity**: give the claimed title for every key; without it the check is `unchecked`. Crossref title similarity ≥ 0.95 exact, 0.55–0.95 near (check subtitle and casing), below 0.55 mismatch (the DOI belongs to another paper; this happens in practice).
- **Year**: use the print (issue) year when it exists; online-first and print years often differ (published online in one year, in print the next). The year shown in table Year columns comes from the same reference record.
- **Venue**: conference DOIs name the proceedings; check the event (a DOI in `10.1145/3579371` is ISCA '23, not ASPLOS).
- **Volume, issue, pages or article number**: complete from Crossref; article numbers such as `e74633` for early-view papers.
- **Authors**: first six plus "et al." (Nature style) or the journal's rule; check author order against the PDF when Crossref and the PDF disagree.
- **Preprints**: cite the published version when it exists; keep the preprint only for material that is not in the published version.
- **Duplicates and unused entries**: every entry cited at least once; no two keys for the same DOI.

## Attribution checks
For each citation in the text:
1. Identify the claim the citation supports (the clause, not the whole sentence).
2. Search the cited paper's `.txt` for the claim's key terms and numbers.
3. Verdict: supported (quote and page), partly supported (what differs), unsupported (remove or re-attribute), secondary (the paper cites someone else; cite the original after checking it).

Common failures:
| Failure | Example pattern | Fix |
|---|---|---|
| number shift | [9] used for one paper while [9] is another | remap keys, rebuild numbering; check numbers baked into figure artwork |
| wrong review | a review of a neighbouring topic cited for results on the target subject | cite the primary source or remove |
| topic not in source | a named effect attributed to a review that never mentions it | find the right source or rephrase to what the review says |
| misread quantity | "about 100 items processed in 500 ns" for "about 100 states, each set with 500 ns pulses" | rewrite from the source sentence |
| scope dropped | a per-event value quoted as a system-level efficiency | add the scope or move the comparison |
| simulated as measured | "reached 97.92%" for a simulated network | "a network simulated with the measured states reached 97.92%" |
| number without source | "⟨component⟩ takes 60–80% of the ⟨cost⟩" found in no paper |
| quantifier dropped | source "up to 40%" written as "40%" | restore the quantifier and add the scope |
| per-paper fault-finding | "⟨A⟩ did not report the temperature" | state the reporting gap for the field, with citations | replace with sourced values and their scopes |

## Output
A table: location | cited key | claim | verdict | evidence (file, page, quote) | fix. Blocking items first.

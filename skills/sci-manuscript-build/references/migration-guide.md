# Migrating an existing manuscript into the kit

1. **Archive** the current files (`archive/vX.Y/`), including any generator script.
2. **Extract** paragraphs, headings, captions and tables from the `.docx` with python-docx, or read them from the old generator's data structures.
3. **Map citations.** Build `old_number → key` from the old reference list. Check every mapping against the claim it supports: insertions and deletions in the old list often shift numbers by one (the v1.4 review cited Molina-Lopez 2019 as [9] while reference 9 was Feng 2016).
4. **Verify references** with `crossref_verify.py`; correct years (print year), venues (e.g. ISCA, not ASPLOS), volumes and article numbers.
5. **Write blocks.** One `P()` per paragraph; keep ids stable (`s4.2-b`). Replace hand-typed numbers such as "Figure 3" with `{fig:key}` and "Eq. (5)" with `{eq:key}`.
6. **Move derivations** into boxes when the main text only needs the result.
7. **Remove duplication.** Old generators often held a "base" and an "advanced" version of the same section; merge them so each argument appears once.
8. **Rebuild and compare.** Diff the new English text against the old (`difflib` on paragraph lists) to confirm nothing was lost, then run the checker.
9. **Delete workarounds.** Remove image-patching code (white rectangles over wrong labels), placeholder paragraphs and dead assignments; regenerate figures properly.

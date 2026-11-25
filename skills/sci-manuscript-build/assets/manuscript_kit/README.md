# Declarative manuscript kit v2

Edit `content.json`, its ordered `sections/*.json` or referenced Markdown paragraph files, `floats.json`, evidence and references. Python assembles content; it does not write or certify the science.

Run `python3 pipeline.py --stage preview` during drafting. Review sources/data and render every final page. Record real review scope with `record_review.py` (identify an AI reviewer as AI), then run `python3 pipeline.py --stage release`. Any content/evidence/artwork change invalidates prior build and review state.

See the installed manuscript-build skill references for the source contract and evidence bindings. Legacy trusted Python projects are supported by `source.format = "python"`. Additional languages require labels and visual validation. Final author acceptance remains human.

2.2 drafting: prepare a sourced facts list, draft by the installed sci-prose-style references/human-line-of-thought.md guide, and run prose_lint.py before delivery. check_manuscript.py also runs the common English/Chinese chain diagnostics. These advisory diagnostics do not replace the existing evidence/freshness/release checks. Rebuilds invalidate prior reviews; the historical 2.1 demonstration keeps its original code and review scope.

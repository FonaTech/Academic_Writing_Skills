# Declarative manuscript kit v2

Edit `content.json`, its ordered `sections/*.json` or referenced Markdown paragraph files, `floats.json`, evidence and references. Python assembles content; it does not write or certify the science.

Run `python3 pipeline.py --stage preview` during drafting. Review sources/data and render every final page. Record real review scope with `record_review.py` (identify an AI reviewer as AI), then run `python3 pipeline.py --stage release`. Any content/evidence/artwork change invalidates prior build and review state.

See the installed manuscript-build skill references for the source contract and evidence bindings. Legacy trusted Python projects are supported by `source.format = "python"`. Additional languages require labels and visual validation. Final author acceptance remains human.

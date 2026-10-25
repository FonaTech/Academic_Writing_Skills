# Manuscript kit

Single-source, bilingual manuscript builder. Copy with `scripts/new_project.py` (preferred) or copy this folder by hand.

```bash
python3 build_manuscript.py            # EN with citations, EN without citations, ZH, references, equations JSON
python3 build_manuscript.py --en-only  # faster while drafting
python3 check_manuscript.py            # FAIL / WARN report
```

| File | Edit? | Purpose |
|---|---|---|
| manuscript.json | yes | titles, languages, fonts, paths, reference style, abbreviations; `style.overrides` changes a style rule by its label (a number sets a cap, null switches it off) |
| style_limits.json | no | caps, banned phrases and sentence targets shared with sci-prose-style's `prose_lint.py`; override per project in manuscript.json instead |
| style_limits.py | no | loads the limits and applies overrides (shared with sci-prose-style) |
| content.py | yes | ordered blocks: headings, paragraphs, display equations, boxes; `CHAPTER` numbers level-1 headings from that number (`None` leaves them unnumbered) |
| floats.py | yes | figures, tables, box bodies |
| references.json | generated | from `crossref_verify.py --emit-references` (sci-literature-evidence) |
| manuscript_core.py | rarely | markup parser, numbering helpers, rich-text runs, fonts |
| build_manuscript.py | rarely | two-pass builder |
| check_manuscript.py | rarely | consistency, evidence and style checks |

Markup summary: `[@key]` citations, `{fig:key|b}`, `{tab:key}`, `{eq:key}`, `{sec:id}`, `{box:name}`, `$...$` inline math, `CO~2~`, `cm^2 V^-1 s^-1`, `V_DS`, `**bold**`, `*italic*`. See the skill's `references/content-markup.md`.

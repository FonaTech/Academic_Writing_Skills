---
name: sci-manuscript-build
description: >
  Build manuscripts from a single structured source into Word documents with native equations, numbered citations, auto-placed figures and tables, boxes, and synchronized English and Chinese versions, then check and version them. Use to set up a new manuscript project, convert a hand-edited or script-generated draft into the kit, rebuild after edits, produce with-citation, no-citation, Chinese and reference-only variants, render pages to images for visual checks, and archive versioned snapshots. 论文构建, docx 生成, 公式 OMML, 中英双版本, 版本管理. Not for writing prose or verifying sources.
---

# Manuscript Build

A manuscript generated from one content source drifts far less: numbers, citations, figure references and both languages come from the same blocks, the checker compares the languages block by block, and every rebuild renumbers everything consistently. This skill packages such a build system as a reusable kit for papers, reviews, theses and proposals in any field.

## Operating Rules

1. Edit the source, never the generated `.docx`. If the user edits a `.docx` by hand, port the edits back into the source before rebuilding.
2. Before restructuring, archive the current source and outputs to `archive/<version>/` (or the project's `Drafts/Manuscript vX.Y/`).
3. Reference numbers follow first citation; figure and table numbers follow first mention; equation numbers follow display order; section and box numbers follow document order. Never number anything by hand.
4. A figure or table that is never cited is a build error. A citation key missing from `references.json` is a build error.
5. Equations are native Word equations (OMML via pandoc). Inline symbols use run-level subscripts and superscripts.
6. Every build is followed by `check_manuscript.py` and, before delivery, by a rendered-page check.
7. The no-citation variant removes citations cleanly: no empty brackets, no "ref." left behind, no doubled spaces before punctuation.
8. If another process or person is editing the same project, do not overwrite their files; work in a copy and report. Before writing a `.docx`, check for a Word lock file (`~$name.docx`) next to it; if one exists, ask the author to close the document or write to a new file name.
9. Years, numbers and labels that can be generated are generated. A table's Year column comes from `references.json` (`year_column`, `year_inline`), never typed into cells.
10. Length variants (for example 100 %, 50 % and 25 % versions) each have their own source folder. A correction made in one variant is applied to every variant and both languages in the same pass, then all variants are rebuilt and checked together.
11. After renumbering figures, check the labels baked into the artwork (panel letters, "Fig. 3" inside an image); the builder renumbers captions and text only.

## Kit Layout

```text
project/
  manuscript.json        titles, languages, fonts, paths, reference style, abbreviations, style.overrides
  style_limits.json      caps and banned phrases, identical to sci-prose-style's copy (do not edit here)
  content.py             CHAPTER, then BLOCKS: headings, paragraphs, display equations, boxes (both languages)
  floats.py              FIGURES, TABLES, BOXES
  references.json        verified reference database (sci-literature-evidence/crossref_verify.py)
  manuscript_core.py     markup parser, numbering, rich-text runs
  build_manuscript.py    two-pass builder
  check_manuscript.py    consistency, evidence and style checks (style_limits.py loads the limits)
  Figures/FigN_slug/     final/figure.png | final.png | final_nbp.png | layout_preview.png (sci-figure-design)
  evidence/              page-cited evidence JSON
  archive/               versioned snapshots
```

Create a project:

```bash
python3 <skill-dir>/scripts/new_project.py ~/Papers/MyPaper --slug MyPaper --type review --chapter 4 \
        --title-en "..." --title-zh "..."
cd ~/Papers/MyPaper && python3 build_manuscript.py && python3 check_manuscript.py
```

Document types: `review`, `article`, `letter`, `rebuttal`, `proposal`, `thesis-chapter`; each gets a skeleton.

## Markup

Read [content-markup.md](references/content-markup.md). In short:

| Markup | Meaning |
|---|---|
| `[@key; @key2]` | citation, numbered by first appearance, compressed to ranges |
| `{fig:key}`, `{fig:key|b}`, `{fig:key|c, d}` | figure or panel reference |
| `{tab:key}`, `{eq:key}`, `{sec:id}`, `{box:name}` | table, equation, section, box reference |
| `$G_{ij}V_i$` | inline math: subscripts, superscripts, Greek, italics |
| `CO~2~`, `mol L^-1 s^-1`, `T_m` | chemistry, units and symbol subscripts outside math |
| `**bold**`, `*italic*` | emphasis (captions: bold panel letters) |

## Build Pipeline

Read [build-pipeline.md](references/build-pipeline.md) for the internals. Pass 1 expands blocks in render order, queues each float at its first citation and releases it after the next complete paragraph (never between a sentence and its equation), then numbers floats, equations, sections, boxes and references. Pass 2 renders each language: with citations, without citations (authoritative language), reference list only, and an equation-source JSON.

```bash
python3 build_manuscript.py            # all variants
python3 build_manuscript.py --en-only  # authoritative language only, faster while drafting
python3 check_manuscript.py            # FAIL / WARN report, exit 1 on failure
python3 <skill-dir>/scripts/render_check.py *.docx --out render_check/   # PDF + page contact sheets
```

## Converting an Existing Manuscript

Read [migration-guide.md](references/migration-guide.md): extract paragraphs from the old `.docx` or script into blocks, map citation numbers to keys through the old reference list (and fix off-by-one shifts on the way), move figures and tables into `floats.py`, move derivations into boxes, then rebuild and diff the text against the old version.

## Length Variants

Read [versioning-delivery.md](references/versioning-delivery.md), section "Length variants". Each variant has its own content source and a per-section word budget. Tables, captions and boxes do not count toward the body budget, so full evidence tables stay in every variant and the text cites each table once without restating it. A correction log lists each fix with the variants and languages it reached.

## Versioning and Delivery

Read [versioning-delivery.md](references/versioning-delivery.md). Each delivered version gets a snapshot folder, a revision-notes document (changes, verified items, open items, abstract-only sources pending full-text checks, terminology table, journal-policy notes for AI images), and unchanged file names so collaborators' links keep working.

## Verification Before Delivery

- `check_manuscript.py`: 0 failures; warnings reviewed
- rendered pages: equations visible and numbered, tables within margins, figures after their first citation, captions below figures, no orphaned headings, Chinese fonts correct
- both languages: same numbers, citations and references block by block
- no-citation variant: no brackets, no "ref.", no stray spaces

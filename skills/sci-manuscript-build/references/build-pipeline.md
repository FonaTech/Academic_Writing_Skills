# Build pipeline internals

## Pass 1: expansion and numbering

1. **Expand** `content.BLOCKS` in order. For each paragraph or box, collect `{fig:}` and `{tab:}` markers; the first time a float is cited it is queued.
2. **Release** queued floats after the current block, unless the next block is a display equation (the paragraph leads into it), and always before the next heading or box. A float therefore never splits a sentence from its equation and never jumps into another section.
3. **Validate**: undefined floats, floats never cited, and citation keys missing from `references.json` stop the build with a message naming the block.
4. **Number** figures and tables in placement order, equations in display order (main text and boxes together), sections from `CHAPTER`, boxes in order, references by first appearance across paragraphs, box text, captions, table titles, cells and notes in render order.

## Pass 2: rendering

- Titles, headings and body text use the fonts in `manuscript.json` (Latin and East Asian separately).
- Paragraph text goes through the resolver (floats, then citations) and the rich-text renderer (math runs, chemistry subscripts, unit exponents, bold, italic).
- Display equations: LaTeX → pandoc (Markdown `$$...$$` → docx) → extract `m:oMath` → insert into a borderless two-cell table with the number right-aligned. Results are cached per equation key.
- Figures: the first existing file of `final.png`, `final.jpg`, `final_nbp.png`, `final_nbp.jpg`, `layout_preview.png`; a layout preview gets an orange "schematic panels pending" line.
- Tables: three-line style, header shading, repeated header row, 7.5 pt cells, note in 8.5 pt.
- Boxes: title in teal bold with "Box n |" prefix, indented body, equations numbered with the main sequence.
- References: Nature (default), ACS or IEEE formatting from `references.json`.

## Outputs

| File | Content |
|---|---|
| `<slug>_EN_WithCitations.docx` | authoritative language with numbered citations and reference list |
| `<slug>_EN_NoCitation.docx` | same text with citations removed (for word counts or proofreading) |
| `<slug>_ZH_WithCitations.docx` | second language, same numbering |
| `<slug>_References.docx` | reference list only |
| `<slug>_Equations.json` | equation number → key and LaTeX |
| `build_report.json` | numbering maps and unused references, read by the checker |

## Pandoc

The builder looks for pandoc in `paths.pandoc`, then `PATH`, then `pypandoc`, then bundled copies left by earlier projects. Install with `brew install pandoc` or `pip install pypandoc-binary` if none is found.

## Extending

- New inline markup: add a pattern in `manuscript_core._tokenize_plain` and a test sentence in `content.py`.
- New reference style: add a branch in `format_reference`.
- Journal templates: open the generated `.docx` in Word, apply the journal's template styles (Normal, Heading 1–3, Caption), save as `reference.docx`, and copy its styles in `render_document` if a project needs them.

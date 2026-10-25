---
name: sci-figure-design
description: >
  Plan and produce figures, tables and captions for scientific papers, and write prompts that make image models such as Nano Banana Pro (Gemini 3 Pro Image) draw correct schematics. Use for figure planning (what each figure argues, panel grids, print sizes), code-drawn data panels with sourced values, and layout specs. Use for per-panel and composite image-model prompts with label whitelists, text-free fallbacks and edit templates, and for redraw briefs and licence records. Use to compose final figures without altering data, verify that data panels survived, and write captions and three-line tables. 科研绘图, 示意图 prompt, Nano Banana Pro 提示词, 图注, 数据图, 拼图. Not for statistics or data analysis itself.
---

# Figure Design

A figure in a strong review or article makes one argument, shows its evidence at print size, and can be understood from the caption alone. Image models are good at clean schematics and bad at numbers, labels and physical detail; code is the reverse. This skill splits the work accordingly and never lets an image model touch data.

## Operating Rules

1. Each figure argues one point, written in one sentence as the `purpose` of its figure spec. If a figure needs two such sentences, it is two figures. The caption title names the object and the measurement in a noun phrase; a claim title is the minority form, used when every panel supports one finding.
2. Number figures by first mention in the text; place each after the paragraph that first cites it.
3. Schematics (mechanisms, structures and cross-sections, architectures, pipelines, application maps) may be drawn by an image model. Data (plots, benchmarks, distributions, maps with values) are drawn by code from a JSON file in which every value has a source, page and evidence level.
4. Every data panel shows its evidence level visibly: filled marks for measured values, open or hatched marks for simulated, projected or abstract-level values, grey for non-target comparators. Model curves say "model" in the title or legend.
5. Draw data panels at their final print size (use `figure_kit.py sizes`); never upsample a data panel.
6. Image-model prompts list every label in quotes, allow no other text, forbid numbers and equations, and describe geometry in physical terms. Few labels per panel (≤ 6–8), 1–3 words each.
7. Data panels always come from code. Schematic panels are redrawn by the author from image-model drafts (route D, the default) or, where the journal allows AI illustrations, taken from the image model with a caption disclosure (route A). The final figure is composed by code, and a model-made composite (route B) is accepted only after `figure_kit.py verify` and a visual check of every number.
8. Never ship artwork with misspelt labels, invented data, generic faces or robots, or patched-over errors. Regenerate the panel.
9. Check the target journal's AI-image policy before any rendering ([journal-ai-policies.md](references/journal-ai-policies.md)). By default, image-model output is a **draft** that the author redraws in standard software; an AI-drawn panel stays in a final figure only when the journal allows it, with a caption disclosure.
10. Reused published panels need a licence route: CC BY with an "Adapted from ref. X under a CC BY 4.0 licence" line, or permission (RightsLink). Record every reused or adapted panel in `sources.csv` (DOI, figure and panel, licence, route, credit line).

## Workflow

### 1. Plan the figure set
Read [figure-planning.md](references/figure-planning.md). For each figure write: argument (one sentence), placement (first citing paragraph), panel list with type (schematic | data | photo | table), what each panel proves, and data sources. A full review of 8,000–12,000 words typically carries 8–14 figures and 2–4 tables; an article carries 4–6 main figures with every panel referenced in Results. The target journal's author guide sets the binding limits. Comparison tables carry a Year column generated from reference metadata, are cited once and are not restated in the text.

### 2. Write the figure spec
One folder per figure with `figure_spec.json` (schema in [figure-spec-schema.md](references/figure-spec-schema.md)): title, purpose, placement, print width (180 mm double column, 88 mm single), aspect ratio, grid, slots, domain hints, per-panel scene, label whitelist, Chinese composition note, and captions in both languages.

### 3. Draw the data panels
Use `scripts/plot_style.py` for the shared palette, fonts and evidence semantics:

```python
from plot_style import apply_style, evidence_marker, save_panel
apply_style()
```

Write every plotted value, with source file, page, evidence level and scope, to `panels/panel_data.json`. Draw at the size printed by:

```bash
python3 scripts/figure_kit.py sizes FigN_slug
```

### 4. Layouts and prompts

```bash
python3 scripts/figure_kit.py layout  FigN_slug     # layout.json, layout_preview.png, layout_blocks.png
python3 scripts/figure_kit.py prompts FigN_slug     # prompt_NBP.md
```

`layout_preview.png` is annotated for humans and the Word placeholder. `layout_blocks.png` has no text at all: blue blocks mark schematic slots and orange blocks mark data slots. It is the only layout image that goes to the model, because a model tends to copy any text or dashed frames it sees.

`prompt_NBP.md` contains, per schematic panel: the prompt, the label whitelist, the Chinese note, a text-free fallback and edit templates; then the route-B composite prompt, both caption drafts and the QC checklist. Prompt construction rules and the domain hint library are in [image-model-prompting.md](references/image-model-prompting.md).

### 5. Render, redraw and compose
Route D (draft and redraw; default for journals that restrict AI images): render the schematic panels with the prompts, save them in `nbp/` as drafts, and redraw each panel in standard software using the draft, the label whitelist and the redraw brief in `prompt_NBP.md`. Save the redrawn panels as `final/panel_<letter>.png` (or the whole figure as `final/figure.png`); `compose` prefers `final/` over `nbp/`.

Route A (only when the journal allows AI illustrations): render each schematic panel alone in Nano Banana Pro at the stated ratio and save it as `nbp/panel_<letter>.png`. For either route, then run

```bash
python3 scripts/figure_kit.py compose FigN_slug     # final.png at print size + final_placements.json
python3 scripts/figure_kit.py verify  FigN_slug     # data panels must score SSIM >= 0.97
```

Route B: upload `layout_blocks.png` and all `panels/*.png` with the composite prompt; save the result as `final_nbp.png` and run `verify`. Model composites re-render every pixel and usually fail the strict threshold; inspect `verify/*.png` (figure | source | difference) number by number, or fall back to route A.

The manuscript builder embeds, in order of preference, `final/figure.png` (whole figure redrawn by the author), `final.png` (composed), `final_nbp.png` (model composite) and `layout_preview.png` (marked placeholder).

### 6. Captions and tables
Read [captions-and-tables.md](references/captions-and-tables.md): a noun-phrase title of 5–12 words that names the object and the measurement; bold panel letters with one sentence each; conditions and evidence levels; abbreviation definitions at the end; source and permission line for adapted panels. Tables are three-line tables with units in headers, "NR" for not reported (defined in the note), an Exp./Sim. column where results mix measurement and simulation, and a note that defines every abbreviation.

## QC Checklist (every figure)

- labels match the whitelist character by character; no extra, missing or repeated words
- no numbers, units, tick values or equations inside schematic panels
- geometry is physically plausible (layer order, contact positions, flow direction, arrow heads)
- colour semantics follow the palette roles; the same object has the same colour in every panel
- no faces, robots, brains, glow, gradients or photographic textures
- data panels identical to their sources: `figure_kit.py verify` reports SSIM ≥ 0.97 for composed figures
- panel letters bold lowercase at the top left, in caption order
- labels legible at print width (cap height about 2 mm, 6–8 pt)
- caption defines every abbreviation; `sources.csv` complete for every reused or adapted panel
- AI use disclosed in the caption when an image-model panel stays in the final figure

## References and scripts

| File | Use |
|---|---|
| [figure-planning.md](references/figure-planning.md) | figure set, types, budgets by genre and venue |
| [figure-spec-schema.md](references/figure-spec-schema.md) | `figure_spec.json` and `panel_data.json` fields |
| [image-model-prompting.md](references/image-model-prompting.md) | prompt anatomy, labels, edits, domain hints |
| [journal-ai-policies.md](references/journal-ai-policies.md) | Wiley, Springer Nature and AAAS rules; disclosure wording |
| [captions-and-tables.md](references/captions-and-tables.md) | caption structure, table templates |
| `scripts/figure_kit.py` | `sizes`, `layout`, `prompts`, `compose`, `verify`, `all` |
| `scripts/plot_style.py` | shared palette, fonts and evidence semantics for data panels |

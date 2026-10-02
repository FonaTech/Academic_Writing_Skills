---
name: sci-figure-design
description: >
  Plan scientific figures, tables and captions across disciplines; generate data panels by code from evidence/data, compose them deterministically and check integrity. 科研绘图、图注、数据图、示意图。 Image models may draft permitted schematics, never evidential data; this skill does not replace statistical analysis.
---

# Scientific figures and tables

Choose display items by the question they answer and the evidence they need, not a fixed number per paper. A coherent multipanel figure may support several related findings. A caption explains objects, methods, conditions, statistics, limitations and provenance sufficiently for its purpose.

## Workflow
1. Specify each figure's purpose, panels, placement, final size, data sources and caption needs. Respect the venue's dimensions rather than assuming a double column.
2. Save the panel data and their evidence keys or raw-data/code provenance. Compute statistics using the study's analysis method; this skill formats results and never manufactures them.
3. Draw data panels with plotting code. Choose scales, uncertainty display, colors and evidence distinctions suitable to the field and accessible at print size.
4. Draw schematics in standard software or, if useful and permitted, obtain independent image-model drafts. Keep physical geometry and labels checked. Journal-specific AI policies must be checked at submission; redraw/disclose as required.
5. Compose final panels by code. Data images must never be uploaded for an image-model composite. Prompts reserve data slots and do not request model reconstruction.
6. Verify asset hashes and compare exact RGB pixels against deterministic placement/resampling. A similarity score cannot certify data or labels. Inspect the rendered figure and check underlying plotted values separately.
7. Record reuse licenses, adapted panels and credits; keep captions and numbering aligned with the text.

```bash
python3 scripts/figure_kit.py sizes FIGURE_FOLDER
python3 scripts/figure_kit.py layout FIGURE_FOLDER
python3 scripts/figure_kit.py prompts FIGURE_FOLDER
python3 scripts/figure_kit.py compose FIGURE_FOLDER
python3 scripts/figure_kit.py verify FIGURE_FOLDER
```

A missing final, panel or composition record is a failed check. Final data figures use `final.png` with `final_placements.json`; externally assembled or vector figures need an explicit adapted verification method, not a silent bypass.

Read [figure-spec-schema.md](references/figure-spec-schema.md) for the tool format, [figure-planning.md](references/figure-planning.md) for general criteria and [journal-ai-policies.md](references/journal-ai-policies.md) for dated policy references. `plot_style.py` supplies an optional palette, not mandatory colors for all fields.

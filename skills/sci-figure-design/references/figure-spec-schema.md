# figure_spec.json

One file per figure folder. `figure_kit.py` reads it for layouts, sizes, prompts, composition and verification; the manuscript builder reads the caption from the float definition, so keep both captions identical or generate one from the other.

```json
{
  "title": "Tensor and convolution acceleration",
  "purpose": "One sentence: the argument this figure makes.",
  "placement": "Section 6.1, after the first paragraph that cites it",
  "print_width_mm": 180,
  "gutter_mm": 2.0,
  "letter_pt": 9,
  "ratio": "16:9",
  "domain": ["layers", "blocks", "flow"],
  "hints": {"my_object": "Project-specific hint sentence for a recurring object."},
  "grid": {"rows": 2, "cols": 2},
  "slots": [
    {
      "panel": "a", "row": 0, "col": 0, "col_span": 1, "row_span": 1,
      "kind": "schematic",
      "title": "Stages of the process and their inputs",
      "scene": "Physical layout, left to right, with counts, positions, colour roles and adjacency.",
      "labels": ["Input", "Stage 1", "Stage 2", "Output"],
      "domain": ["blocks"],
      "ratio": "4:3",
      "zh": "中文构图说明：对象、位置、配色含义。"
    },
    {
      "panel": "c", "row": 1, "col": 0,
      "kind": "data",
      "file": "panels/fig5_c_metric_scope.png",
      "title": "Metric and its scope"
    }
  ],
  "caption_en": "Noun-phrase title naming the object and the measurement. **a**, ... **b**, ... Abbreviations.",
  "caption_zh": "标题句。**a**，……缩写。"
}
```

| Field | Required | Notes |
|---|---|---|
| title | yes | used in previews and the prompt document, not drawn in the figure |
| purpose | yes | the figure's argument in one sentence |
| placement | yes | section and first citing paragraph |
| print_width_mm | no | 180 (default, full width); use the journal's widths, e.g. Nature 89 mm single and 183 mm double column; Wiley 80 mm small and 180 mm large figures (Wiley figure guidelines, 2016); check the journal's current guide |
| ratio | yes | whole-figure ratio; slot ratios follow from the grid unless given |
| domain | no | keys of the hint library (built-in primitives or project hints), applied to every schematic slot |
| hints | no | project-specific hint sentences, {key: sentence}; keys can then be used in `domain` |
| grid | yes | rows and columns of equal cells |
| slots[].kind | yes | `schematic` (image model) or `data` (code); `nbp` is accepted as an alias |
| slots[].file | data | path relative to the figure folder |
| slots[].scene | schematic | physical description; no numbers to draw |
| slots[].labels | schematic | the whitelist; ≤ 6–8 labels of 1–3 words |
| slots[].ratio | no | override when a slot must use a specific supported ratio |
| caption_en / caption_zh | yes | see captions-and-tables.md |

`panels/panel_data.json` accompanies the data panels:

```json
{"panels": [{"panel": "c", "file": "fig5_c_metric_scope.png", "values": [
  {"label": "Study A, condition 1", "value": 12.3, "unit": "unit per event", "exp_or_sim": "measured",
   "scope": "system including overheads", "source": "authorYYYY", "page": 7}]}]}
```

Evidence levels use one vocabulary everywhere (evidence tables, `panel_data.json`, plots): `measured`, `simulated`, `projected`, `estimated`, `reported-survey`, `abstract-only`; plots add `comparator` and `model`. The field name is `exp_or_sim`, as in the evidence-table contract.

# figure_spec.json and data provenance

One specification per figure folder. The raster helper reads slots for layout, sizes, schematic prompts and deterministic composition. Vector/externally assembled figures need their own explicit integrity method.

```json
{
  "title": "Workflow and comparison",
  "purpose": "Explain the design and compare the supported result",
  "print_width_mm": 170,
  "grid": {"rows": 1, "cols": 2},
  "slots": [
    {"panel": "a", "kind": "schematic", "row": 0, "col": 0,
     "scene": "Describe only the scientifically correct conceptual geometry", "labels": ["Input", "Output"]},
    {"panel": "b", "kind": "data", "row": 0, "col": 1, "file": "panels/comparison.png"}
  ]
}
```

Panel letters are unique; grid positions/spans must fit. Optional gutter_mm, letter_pt, ratio, domain and slot ratios configure the provided helper. Hardware domain hints and its palette are optional. Schematic finals under final/panel_a.png take precedence over model drafts under nbp/. Do not use an unreviewed model draft as a final unless the venue permits it and applicable disclosure/rights have been handled. The helper does not certify those decisions.

Store panels/panel_data.json with each plotted datum/series's evidence_key or raw-data/analysis provenance, exact value, unit, metric, object, conditions, result_method and accounting_scope where relevant. Use the literature v2 contract: result_method, source_role and access_status are different axes. Synthetic fixtures are explicitly synthetic, never mislabeled measured or simulated results.

Final composition is final.png plus final_placements.json. Missing slots fail composition. Each placement stores source_file, source_sha256 and box [x,y,width,height]. Verification compares exact RGB pixels after the same declared deterministic resize; it certifies that operation only. Scientific data correctness, plot semantics and permitted schematic use still require inspection.

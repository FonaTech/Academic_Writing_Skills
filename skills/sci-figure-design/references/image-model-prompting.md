# Prompting image models for scientific schematics

Written for Nano Banana Pro (Gemini 3 Pro Image) and applicable to similar models. The rules come from failures seen in real manuscript artwork and from published prompting guidance for this model family.

## What went wrong before (and why the rules exist)

| Failure seen in draft artwork | Cause | Rule |
|---|---|---|
| misspelt labels ("Netrwork", "Column Rine") and garbled strings | too much text requested in one image | ≤ 6–8 labels per panel, 1–3 words each, all quoted |
| repeated labels ("Layer Layer") | labels described loosely, model free to repeat | explicit whitelist plus "do not repeat any label" |
| invented confusion matrices and accuracy bars | data requested from the image model | data panels only from code |
| a generic human face, robot or brain | words such as "intelligent" or "vision" invite one | prohibit faces, robots, brains by name |
| labels overflowing panels, white patches pasted over errors | fixing by editing pixels | regenerate or edit with a one-change instruction |
| dashed guide frames and placeholder text copied into the figure | annotated layout image uploaded | upload only the text-free `layout_blocks.png` |

## Prompt anatomy

Write complete sentences in this order. `figure_kit.py prompts` assembles them from `figure_spec.json`.

1. **Frame**: "Create one panel of a scientific figure, aspect ratio 4:3, 2K resolution."
2. **Subject**: one sentence naming what the panel shows.
3. **Scene**: spatial layout left to right or top to bottom, each element with its shape, position, colour role and relation to its neighbours. Physical facts go here: layer order, which part is on top, flow direction, what touches what.
4. **Hints**: short fixed sentences for recurring objects (layers, sheets, tubes, grids, networks, blocks, light, pulses, molecules, cells or the project's own objects) so they look the same in every figure.
5. **Labels**: "Add exactly these text labels, each next to the element it names, with a thin leader line where needed, and no other text: 'Inlet', 'Reaction zone', 'Outlet'."
6. **Style**: flat vector, light isometric shading, thin uniform outlines, white background, palette with hex codes and roles, one sans-serif font, sentence case, legible.
7. **Prohibitions**: no title, no panel letters, no captions, no numbers, units, ticks or equations; no faces, robots, brains, glow, lens flares, photographic backgrounds; no labels beyond the list; no repeated labels.

Keep the scene description under about 120 words; with the fixed style and prohibition blocks a panel prompt then stays near 250–300 words. Longer scenes dilute the constraints that matter.

## Supported aspect ratios

1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9. `figure_kit.py` snaps each slot to the nearest supported ratio. Set the aspect ratio and the output size (2K for single panels, 4K for composites) in the app or through the API parameters (`aspect_ratio`, `image_size`); text in the prompt does not set them.

## Labels

- Quote every label exactly as it must appear, in single quotes.
- Sentence case, no trailing punctuation, no abbreviations the caption does not define.
- Prefer nouns: 'Input', 'Active layer', 'Readout'. Avoid verbs and full sentences.
- If text keeps failing, use the text-free fallback prompt and add labels in code or in a vector editor.

## Scene descriptions that work

- Name the viewpoint: "cross-section", "isometric view from the front left", "top view".
- Give counts: "a 4 by 4 grid", "three stacked layers", "five pulses".
- State adjacency: "the middle layer lies directly on the base; the top layer lies on the middle layer".
- Give colour by role, not by aesthetics: "the highlighted element in coral", "flow arrows in teal".
- Say what must be absent: "no packaging, no background grid, no decorative icons".

## Composite (route B) prompts

- Upload `layout_blocks.png` (text-free blocks) and every data panel PNG.
- Say which uploaded file goes into which grid position, and that it must be placed exactly as provided without redrawing, recolouring, cropping or retyping.
- Expect the model to re-render the data panels anyway. Always run `figure_kit.py verify` and compare every number; prefer route A for any figure whose data matter.

## Editing instead of regenerating

Generate once, then correct with short, single-purpose edits. Repeated full regeneration drifts in composition and colour.

- "Change only the label that should read 'Outlet' so that it reads exactly 'Outlet'; keep everything else identical."
- "Remove every piece of text that is not in this list and keep everything else identical: 'Inlet', 'Reaction zone', 'Outlet'."
- "Correct only the order of the layers: the base lies below the middle layer, not above it. Keep every other element identical."
- "Replace any glow, gradient or texture with flat colour on white; keep layout, colours and labels identical."

## Reference images

The model accepts reference images (up to 14 in current versions). Good references are a correct schematic from the authors' own slides, a previous panel whose style should be matched, and the palette swatch. Do not upload published figures from other groups as style references for figures that will be published.

## Hint library (from `figure_kit.py`)

`figure_kit.py` ships field-neutral visual primitives: `layers`, `sheets`, `tubes`, `grid`, `network`, `blocks`, `flow`, `optics`, `pulses`, `molecule`, `cell` and `map`. Each is one fixed sentence that keeps a recurring object looking the same in every panel.

Add hints for the project's own objects under `"hints"` in `figure_spec.json`, then list their keys under `"domain"`:

```json
"hints": {"my_object": "⟨Object⟩ is drawn as ⟨shape⟩ with ⟨feature⟩; never as ⟨common wrong rendering⟩."},
"domain": ["layers", "my_object"]
```

A good hint names the shape, the one feature that identifies the object, and the most common wrong rendering to avoid. Reuse the same hints across all figures of a manuscript.

## Journal policy

Publishers differ on generative-AI images and change their rules (see journal-ai-policies.md); treat renderings as drafts unless the target journal allows AI illustrations. Check the target journal before submission. When AI imagery is not allowed, use the rendered panels as a precise brief for a professional illustrator or redraw them in a vector editor.

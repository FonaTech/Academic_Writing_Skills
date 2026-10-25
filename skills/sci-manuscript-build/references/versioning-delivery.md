# Versioning and delivery

## Versions
- Semantic draft numbers: v1.0 first full draft, v1.x revisions, v2.0 after a structural change agreed with the supervisor.
- Before each version: copy source, outputs and figures to `Drafts/Manuscript vX.Y/` (or `archive/vX.Y/`). Never overwrite a delivered snapshot.
- Keep output file names stable across versions so shared links and comments keep working; the folder carries the version.

## Revision notes (deliver with every version)
1. What changed, by section (structure, text, figures, tables, references).
2. Corrections to facts and citations, each with the source page that justifies it.
3. New references, with the evidence level of each (full text read, abstract only).
4. Open items: claims marked `[to verify]`, abstract-only sources awaiting full text, figures still at the layout-preview stage.
5. Decisions taken and decisions needed from the supervisor.
6. Terminology table (English, abbreviation, Chinese).
7. Journal policy notes, e.g. restrictions on generative-AI images.

## Length variants
- One source folder per variant (e.g. `full_100/`, `half_50/`, `quarter_25/`), each built by the same builder. Never derive a shorter variant by editing the longer variant's output.
- Set a per-section word budget and a hard total cap for each variant; count body text only (tables, captions, boxes and references excluded). `check_manuscript.py` word counts are the reference; report them per section.
- Full evidence tables appear in every variant. Shorter variants shorten prose, not tables.
- A fix to a number, citation, wording rule or reviewer comment goes into every variant and both languages in one pass. Keep a correction log: fix, block ids touched per variant, languages, verified against which source page.
- Material that appears only in the longer variants is brought up to the same standard as the shortest, most-polished variant before delivery.
- Rebuild and check all variants together; deliver them in one snapshot folder.

## Before writing outputs
- Check for Word lock files (`~$<name>.docx`). An open document cannot be overwritten safely; write to a new name or ask the author to close it.
- After figure renumbering, open each figure and check labels inside the artwork.

## Delivery checklist
- `check_manuscript.py`: 0 failures
- `render_check.py`: every page inspected
- figure folders complete: panels, `panel_data.json`, layout images, `prompt_NBP.md`
- evidence and reference audits attached or referenced
- snapshot folder created
- for length variants: every variant rebuilt from its own source, word counts within budget, correction log complete

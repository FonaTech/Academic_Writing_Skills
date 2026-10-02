---
name: sci-manuscript-build
description: >
  Build repeatable scientific documents from declarative section content with references, figures, tables and native equations; support incremental previews, bilingual checks and reviewed release validation. 论文构建、文档生成、排版检查。 Preserve existing Word/Markdown/LaTeX workflows for small edits; this is not an evidence or prose-writing skill.
---

# Manuscript construction

Use staged authoring with deterministic assembly. Scientific content is written and reviewed in small units; the builder handles numbering, references, equations and layout. A one-click build is useful after content exists, not a substitute for deciding or verifying it.

## Choose the source
- New repeated or bilingual Word builds: section-based JSON content, independent float/reference/evidence files, stable Python builder. Long paragraph text may live in Markdown files referenced by a block.
- Existing author-edited DOCX: keep it authoritative for a small edit. Migrate to declarative source only when repeated generation justifies the cost; reconcile manual edits before rebuilding.
- Venue-required LaTeX: preserve the template and source. Use the host's native LaTeX editor/compiler when available; do not install a TeX system for it.
- A small plain draft can remain Markdown. Do not create a generator solely to make a short text edit.

See [build-pipeline.md](references/build-pipeline.md), [content-markup.md](references/content-markup.md) and the orchestrator's [authoring rationale](../sci-writing-orchestrator/references/ai-authoring-method.md).

## Default project
```text
manuscript.json        source, languages, fonts, paths and validation settings
content.json          ordered section list and heading-number policy
sections/*.json       stable blocks with text, status and evidence-bound claims
floats.json           figures, tables and optional boxes
references.json       checked bibliographic records
source_audit/         exact page-marked literature text
evidence/             literature, raw-data and derived-result records
data/ analysis/       original files and analysis code/results
build_manuscript.py   stable assembly engine
check_manuscript.py   draft/release consistency checks
review_record.json    actual reviewer, scope, limitations and inspected source state
```

```bash
python3 scripts/new_project.py PROJECT --slug Paper --type article --languages en zh
cd PROJECT
python3 pipeline.py --stage preview
# Review sources and figures; render the DOCX files and inspect every page.
python3 record_review.py --kind scientific_review --reviewed-by 'reviewer name and role' --notes 'actual scope and limits'
python3 record_review.py --kind visual_review --reviewed-by 'reviewer name and role' --notes 'which rendered pages were inspected'
python3 pipeline.py --stage release
```

Do not run the record commands before inspecting. They store an attestation, not proof that inspection happened. Identify an AI reviewer as AI. The final author acceptance and publication decision remain human.

## Gates
Preview permits labeled gaps; release rejects unresolved scaffolds, unsupported quantities, invalid evidence, missing outputs, incorrect language quantities/units, altered data panels and missing/stale review records. A source/evidence/artwork change invalidates prior build and review state. Release validation never silently treats a skipped check as passed.

Build incrementally during drafting. Once the argument and displays stabilize, refine page layout, render and inspect. Repair clipping, overflow, headings, captions, equations and fonts in the source/configuration and re-render. For immutable templates use their layout requirements.

Archive before restructuring, avoid simultaneous edits, and deliver only requested variants with validation limits. Legacy trusted Python sources are supported; external Python content executes on import and must not be treated as untrusted data.

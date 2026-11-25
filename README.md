# Academic Writing Skills

Version **2.3.1** — validator and method-study integration, 2026-11-25. Six reusable skills for evidence-traceable scientific writing across disciplines, with precise English and aligned Chinese when requested.

| Skill | Responsibility |
|---|---|
| sci-writing-orchestrator | Question, scope, roles, argument, mode routing and a living writing plan |
| sci-literature-evidence | Literature/search screening, source identity, page-cited evidence and raw/derived-data provenance |
| sci-prose-style | Incremental drafting, linked precise prose, terminology, quantitative wording and translation |
| sci-figure-design | Figure plans, sourced code-drawn panels, schematic prompts, captions and exact composition checks |
| sci-manuscript-build | Declarative/legacy sources, numbering, citations, native equations, years, variants and review freshness |
| sci-manuscript-review | Twelve review dimensions, source/method audits, review triage and point-by-point responses |

## Drafting-chain integration in 2.2

The supplied Academic_Writing_Skills_v1.3.0.zip matches all 103 scientific-skill files in the current local .codex installation. The GitHub base was 2.1.0. This release merges the 1.3 authoring method into that runtime rather than replacing either package wholesale.

Every prose-producing skill routes to [the facts-first drafting guide](skills/sci-prose-style/references/human-line-of-thought.md). Prepare the facts list, order sentences by the scientific argument and named actors, vary sentence lengths, use explanation connectives sparingly, avoid voiced questions/musings/template overviews, and end on the last relevant fact. Run prose_lint.py before delivery, including a task-local copy of chat-only prose. Preserve evidence, necessary qualifiers, terms and bilingual meaning. The English/Chinese functions are shared by the linter and the manuscript checker; other profiles do not silently disable them.

The precise default restores the full incoming style table: 42 banned-pattern entries, 7 capped entries and its Chinese/rhythm settings. The three alternative profiles and --known remain available. Diagnostics are editorial preferences; no finding automatically deletes a technical term or evidence qualifier, and no result establishes authorship or predicts detector scores.

Detailed prose guides, genre/agency scaffolds and all 16 method cases are available alongside the original 16 domain scenarios. The [case-bank index](skills/sci-writing-orchestrator/case-studies/INDEX.md) separates the two banks; the [detailed editorial preset index](skills/sci-writing-orchestrator/presets/editorial-1.3/INDEX.md) preserves the incoming scaffolds as optional examples subject to actual venue rules. Templates remain checklists rather than a fixed sentence sequence.

Raw/derived provenance, declarative and legacy builds, requested-language output, exact data-panel composition, Word-lock preflight, installer backups, release freshness, hidden metadata and checksums remain in place. See [the file-by-file merge record](MERGE_1.3.0.md) and [validation](VALIDATION.md). No global installation was performed.

## What is merged

The 2.1 base combined the functional Generic v2 implementation at commit `0457e77` with useful 1.1 editorial/build features in the installed skills and GitHub commit `b759d87`. It restores detailed review voice, article architecture, external-review triage and requested variant synchronization while retaining strict provenance, declarative sources and preview/release checks. It repairs the mixed-version upload, missing hidden plugin manifests, unsafe replacement installation and stale checksums. See [merge notes](MERGE_NOTES.md), [changelog](CHANGELOG.md) and [actual validation](VALIDATION.md).

The default precise style targets one principal claim per sentence, one coherent question per paragraph, topic sentence first, and a 16–20-word English median with a ceiling around 30. Keep necessary scientific qualifications and technical meanings. Compact, explanatory and generic profiles are opt-in; none relaxes evidence requirements or predicts AI detection. A narrative review synthesizes the field; systematic/scoping reviews retain their actual search, selection and appraisal reporting.

## Install

Use Python 3.10+ and install only the dependencies needed:

```bash
python3 -m pip install -r requirements-core.txt
python3 tools/install.py --status --targets codex
python3 tools/install.py --targets codex --no-inject
```

Use `--targets claude` or `--targets opencode` for those clients. Omit `--no-inject` only when intentionally updating the marked standing instructions. Existing skills are moved to timestamped backups; other discovery locations are reported and never silently deleted. The default no-argument installer remains compatible and targets all three clients. A project-local copy uses `--project DIR --no-inject`. Start a new client session and inspect the discovered skill list.

For Claude Code plugin installation with a supporting client:

```text
/plugin install academic-writing-skills --marketplace FonaTech/Academic_Writing_Skills
```

Client-specific details: [Codex](codex/INSTALL.md), [Claude Code](claude-plugin/INSTALL.md), [OpenCode](opencode/INSTALL.md). Existing user instructions always take priority over package defaults.

## Start a manuscript

```bash
python3 skills/sci-manuscript-build/scripts/new_project.py ./Paper --slug Paper --type article --languages en zh
cd Paper
# Edit manuscript.json, sections/*.json, floats.json, evidence/ and references.json from actual materials.
python3 pipeline.py --stage preview
```

The first requested language controls numbering; the program does not translate automatically. Defaults produce only requested primary outputs. Enable no-citation/reference-only variants in manuscript.json when needed. Trusted legacy Python sources remain supported; bounded Word/Markdown edits and venue-required LaTeX do not need migration.

Tables can derive `year_column` and `year_inline` from checked reference metadata. Standard inline functions such as `\ln` and `\exp` stay upright; display OMML equations require Pandoc. All planned DOCX destinations are checked for Word lock files before writes. See [source markup](skills/sci-manuscript-build/references/content-markup.md).

Render current documents with the build skill's render_check.py and inspect every final page. Only after actual scientific/visual reviews, record their identity, scope and limitations with record_review.py and run `python3 pipeline.py --stage release`. Hash freshness and a passed checker are not scientific certification or human author acceptance.

## Figures, sources and style tools

Data panels come from sourced values and code, with evidence records and units/conditions. An image model receives only schematic scenes or data-free layout blocks. Final composition is deterministic and checked by exact RGB/hash comparisons. Prompt helpers support label whitelists, text-free fallbacks and project-specific primitive hints.

Literature quantities have exact quotes/pages. Original/derived quantities have input hashes, locators and analysis provenance. Result method, source role and access state are separate. DOI-bearing references are checked against Crossref; non-DOI sources retain stable identifiers and an explicit manual-check path. Token or hash matches never replace source-based semantic review.

```bash
python3 skills/sci-prose-style/scripts/prose_lint.py draft.md --json --known DNA,RNA
python3 skills/sci-literature-evidence/scripts/verify_evidence_quotes.py evidence.json --text-dir source_audit
```

Style diagnostics are advisory. Acronym exceptions do not waive independent caption definitions. Optional research dependencies, offline transcription and native-equation requirements are documented in requirements-research.txt. The [16 teaching cases](skills/sci-writing-orchestrator/case-studies/INDEX.md) are hypothetical, with historical public-access records; they are not executed studies or an expert-quality benchmark.

## Validate and upload

```bash
python3 tools/sync_plugin_manifests.py
python3 tools/validate_skills.py
python3 -m unittest discover -s tests -v
python3 tools/checksums.py
```

The ZIP contains hidden `.claude-plugin/` and `.github/` files. Upload the directory contents at repository root, including hidden files, not the outer version folder. Visible `claude-plugin/*.json` mirrors support recovery after a browser upload: review them, then run `python3 tools/sync_plugin_manifests.py --write`. After intentional source edits, rerun checks and `python3 tools/checksums.py --write`.

See [upload instructions](UPLOAD_zh.md). The package includes a GitHub Actions configuration; its hosted execution is pending upload. [MIT license](LICENSE), retaining both source notices. [中文说明](README_zh.md).

## Selected 2.3 improvements in 2.3.1

This revision starts from 2.2.0 and integrates only the reviewed validator/index/organization improvements from the supplied 2.3.0 archive. Every profile's English and Chinese patterns and required diagnostic blocks are checked. Numbered method studies must have real links in their index; dangling numbered links fail. The method bank now lives under method-studies/, separately from the domain cases, with a compatibility redirect at its former index.

The full precise rule table, detailed editorial guides/scaffolds, occurrence-based connective statistics, short-question detection and figure-reference prose classification remain from 2.2.0. Evidence, build, backup and integrity engines are retained. See [integration details](MERGE_2.3.1.md) and [actual validation](VALIDATION.md). Original 2.3.0 is not installed or pushed wholesale.

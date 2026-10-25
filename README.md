# Academic Writing Skills

Evidence-traceable scientific writing for Claude Code, Codex and OpenCode: plan, research, draft, build, illustrate and review reviews, research articles, letters, rebuttals, theses and grant proposals in any field, in English and Chinese.

The suite was distilled from a multi-round rebuild of a bilingual review in three length variants, with supervisor, editor and external-reviewer feedback, and from an analysis of published expert reviews and research papers. It encodes what made that work hold up: audit before writing, page-cited evidence for every number, one content source for both languages, a review voice that narrates the field's progress, image models for schematics only, and adversarial review before delivery. The skills carry no field-specific content; examples use placeholders (⟨method⟩, ⟨metric⟩) or constructed cases.

## Skills

| Skill | Use it for |
|---|---|
| `sci-writing-orchestrator` | any manuscript project: mode routing, design brief, writing plan, milestones, delegation, definition of done |
| `sci-literature-evidence` | literature search (OpenAlex), library curation, PDF text extraction with page markers, evidence tables, quote re-finding, Crossref DOI verification, citation audits, fair-comparison rules |
| `sci-prose-style` | expert-journal English and aligned Chinese: house style, flow and review voice, no-hedging rules, revision passes, AI-flavour lexicon, section guides, terminology table, prose linter |
| `sci-figure-design` | figure plans, print-size data panels with evidence semantics, figure specs, Nano Banana Pro prompts, composition that never touches data pixels, integrity checks, captions and tables |
| `sci-manuscript-build` | single-source bilingual Word builds: numbered citations, auto-placed floats, native equations, boxes, section references, Year columns from reference metadata, length variants, no-citation and reference-only editions, checks, page rendering |
| `sci-manuscript-review` | twelve-dimension audits (including review voice and variant sync), refutation pass, readiness rubric, referee simulation, triage of external reviews and author rewrites, response letters |

## Install

```bash
python3 tools/install.py            # Claude Code + Codex + OpenCode, copies, global instructions injected
python3 tools/install.py --status   # what is installed where
python3 tools/install.py --mode symlink   # develop in the repo; installed skills follow edits
python3 tools/install.py --uninstall
```

What the installer does:

| Tool | Skills | Global instructions |
|---|---|---|
| Claude Code | `~/.claude/skills/<skill>` | marked block in `~/.claude/CLAUDE.md` |
| OpenCode | reads `~/.claude/skills` and `~/.claude/CLAUDE.md` natively; a separate copy in `~/.config/opencode/skills` is made only if Claude-compatibility is disabled | block added to `~/.config/opencode/AGENTS.md` only if that file already exists |
| Codex | `~/.codex/skills/<skill>` | marked block in `~/.codex/AGENTS.md` |

The instruction block is short: which skill to use for which task, and seven standing norms (no invented facts, Crossref-verified citations, sentence and paragraph discipline, bilingual parity, schematics-only image models, edit sources not outputs, report what was verified). Files are backed up once before the first change, and the block is replaced, not duplicated, on re-install.

Claude Code can also load the suite as a plugin: `claude plugin validate .` passes, and `.claude-plugin/marketplace.json` lists all six skills. See `claude-plugin/INSTALL.md`, `codex/INSTALL.md` and `opencode/INSTALL.md`.

## Start a project

```bash
python3 skills/sci-manuscript-build/scripts/new_project.py ~/Papers/MyReview --slug MyReview --type review --chapter 4
cd ~/Papers/MyReview && python3 build_manuscript.py && python3 check_manuscript.py
```

Then ask the agent, for example: "Use sci-writing-orchestrator to plan Sections 4–7 from the drafts in this folder and the literature in ../Library."

## Requirements
Python 3.9+, python-docx, lxml, PyMuPDF, Pillow, matplotlib, numpy, PyYAML, requests; openpyxl for the library workbook; rapidfuzz (optional, faster title matching); scikit-image for figure verification; pandoc (or pypandoc-binary) for equations; optional: transformers + torch + ffmpeg for offline meeting transcription; Microsoft Word or LibreOffice for page rendering. An OpenAlex API key (`OPENALEX_API_KEY`) avoids the shared anonymous quota.

## Validate

```bash
python3 tools/validate_skills.py
```

checks frontmatter against the Codex and OpenCode rules, folder–name agreement, every referenced file (including the files the orchestrator's mode router names), truncated files and unclosed code fences, agent metadata, script compilation and `--help`, the plugin manifests, and that the two copies of the shared style limits are identical.

## Style rules

Caps, banned phrases and sentence targets live in one file, `skills/sci-prose-style/assets/style_limits.json`. The prose linter and the manuscript kit's checker both read it; the kit carries an identical copy. Change a rule there (then copy it to `skills/sci-manuscript-build/assets/manuscript_kit/`), or override it for one project by label in `manuscript.json` under `style.overrides`.

## Layout

```text
skills/<skill>/SKILL.md         router: rules, workflow, which reference to load
skills/<skill>/references/      detailed guides, loaded only when needed
skills/<skill>/scripts/         tested command-line tools
skills/<skill>/assets/          templates and data (manuscript kit, style_limits.json)
skills/<skill>/agents/          Codex UI metadata
skills/sci-writing-orchestrator/presets/        defaults per document type
skills/sci-writing-orchestrator/case-studies/   worked cases
tools/                          installer, validator, global instruction block
provenance/                     source material the rules were distilled from (not installed, not in the release zip)
```

## Changes in 1.1.0

- All skills are field-neutral: domain examples were replaced by placeholders or constructed cases, and domain material moved to `provenance/`.
- Prose: flow (linked sentences, no staccato chains or orphan paragraphs), no defensive sentences, field-level gap statements, review voice, named-actor convention, quantifier and arithmetic checks, subsection endings, tables cited once.
- Build: `year_column` / `year_inline` table options filled from `references.json`; length-variant rules; Word lock-file check; upright function names (`\ln`, `\exp`) in inline math.
- Review: D11 voice and D12 variant-sync dimensions; triage table for external reviews and author rewrites.
- Linter: staccato runs, orphan paragraphs, defensive phrases, screening-report voice, "in a preprint", per-paper fault-finding; `--known` for a field's standard acronyms.

README in Chinese: [README_zh.md](README_zh.md).

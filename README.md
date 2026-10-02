# Academic Writing Skills

Evidence-traceable scientific writing for Claude Code, Codex and OpenCode: plan, research, draft, build, illustrate and review reviews, research articles, letters, rebuttals, theses and grant proposals, in English and Chinese.

The suite was distilled from a full rebuild of a review on carbon-nanotube devices for analog and neuromorphic computing (Hu group, 2026) and from an analysis of 137 papers in the group's literature library. It encodes what made that rebuild work: audit before writing, page-cited evidence for every number, one content source for both languages, image models for schematics only, and adversarial review before delivery.

## Skills

| Skill | Use it for |
|---|---|
| `sci-writing-orchestrator` | any manuscript project: mode routing, design brief, writing plan, milestones, delegation, definition of done |
| `sci-literature-evidence` | literature search (OpenAlex), library curation, PDF text extraction with page markers, evidence tables, quote re-finding, Crossref DOI verification, citation audits, fair-comparison rules |
| `sci-prose-style` | expert-journal English and aligned Chinese: house style, revision passes, AI-flavour lexicon, section guides with exemplar banks, terminology table, prose linter |
| `sci-figure-design` | figure plans, print-size data panels with evidence semantics, figure specs, Nano Banana Pro prompts, composition that never touches data pixels, integrity checks, captions and tables |
| `sci-manuscript-build` | single-source bilingual Word builds: numbered citations, auto-placed floats, native equations, boxes, section references, no-citation and reference-only variants, checks, page rendering |
| `sci-manuscript-review` | ten-dimension audits, refutation pass, readiness rubric, referee simulation, response letters |

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
skills/<skill>/assets/          templates and data (manuscript kit, style_limits.json, corpus_index.csv)
skills/<skill>/agents/          Codex UI metadata
skills/sci-writing-orchestrator/presets/        defaults per document type (review and article presets are corpus-based)
skills/sci-writing-orchestrator/case-studies/   worked cases
tools/                          installer, validator, global instruction block
provenance/craft-corpus/        how the corpus-based rules were made (not installed; review before publishing)
```

README in Chinese: [README_zh.md](README_zh.md).

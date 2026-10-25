---
name: sci-manuscript-review
description: >
  Audit and review scientific manuscripts before submission or after revision, and handle peer review. Use for adversarial checks of every number and citation against source pages, attribution tests, and evidence-level and accounting-scope checks. Use for style and terminology audits, figure and table integrity, bilingual consistency and structural gap analysis against reference reviews. Use for simulated referee reports, go/no-go readiness scores, and point-by-point responses to reviewers with tracked changes. 论文审查, 模拟审稿, 投稿前检查, 审稿意见回复, 数据核查. Not for first drafting; use sci-writing-orchestrator for that.
---

# Manuscript Review

A manuscript is ready when an expert referee can check any sentence and find it true, specific and sourced, and when the argument survives a hostile reading. This skill runs that check before the journal does.

## Operating Rules

1. Review against sources, not against memory. Every numeric or attributed claim is looked up in the evidence tables or the source text.
2. Separate findings by severity: **blocking** (wrong number, wrong attribution, simulated shown as measured, missing citation for a claim, data panel altered), **major** (unfair comparison, missing scope, structural gap, duplicated argument), **minor** (style, terminology, formatting).
3. Try to refute each finding before reporting it. A finding stays when the source supports it; an ambiguous finding is kept and marked "check", never dropped.
4. Report every fault with its fix: location, current text, evidence, proposed text.
5. Do not rewrite silently while reviewing; propose, then apply after the review is accepted.
6. Referee simulations are written in the voice of a demanding but fair expert. They are aids for revision, not predictions of the outcome.
7. Triage every external review (referee, colleague, AI tool) and every author rewrite point by point: adopted, partly adopted or rejected, each with its reason from the sources ([rebuttal-letters.md](references/rebuttal-letters.md), triage section).
8. Fixes reach every length variant and both languages; a fix found in one variant is searched for in all of them.
9. If the author asks for one continuous pass without sub-agents, run the dimensions sequentially yourself and keep the refutation step as a separate re-read.

## Review Dimensions

Run the dimensions as independent passes (in parallel sub-agents for long manuscripts). Each writes findings with location, claim, evidence, verdict and fix. Details and prompts are in [audit-dimensions.md](references/audit-dimensions.md).

| Dimension | Question |
|---|---|
| D1 Numbers | Does every number match its source page, unit, condition, scope and quantifier, and is every derived magnitude arithmetically right? |
| D2 Attribution | Does the cited paper actually say what the sentence attributes to it? |
| D3 Evidence level | Are measured, simulated, projected, estimated and abstract-only results labelled correctly? |
| D4 Comparison fairness | Are values compared only within the same scope, node, precision and dataset? |
| D5 Structure | Does each section make one argument? Are there gaps compared with the reference reviews? Duplicates? |
| D6 Style | Sentence profile, lexicon, hedging, meta-commentary (prose_lint.py) |
| D7 Terminology | Abbreviations defined once in text and again in captions; one spelling per term |
| D8 Floats | Figures and tables cited in order, placed after first mention, captions self-contained, data panels intact |
| D9 Bilingual | Same numbers, citations and references in both languages, block by block |
| D10 References | DOIs verified, metadata complete, no orphans, no unused entries, venue and year correct |
| D11 Voice | Does the text narrate the field's progress, without screening-report wording, per-paper fault-finding or defensive sentences? |
| D12 Variant sync | Is every fix present in every length variant and language, within budget, with full tables? |

## Workflow

1. **Inventory.** Build the manuscript and run `check_manuscript.py`; list the evidence files and reference database.
2. **Fan out.** One agent per dimension (D1 and D2 split by section for long texts). Each returns structured findings. The agent split, prompts and verification pass are in [parallel-audit-recipe.md](references/parallel-audit-recipe.md).
3. **Verify.** For each blocking or major finding, an independent agent tries to refute it against the source. Keep findings that survive.
4. **Synthesize.** Deduplicate, sort by severity, and write the review report with a readiness score ([readiness-rubric.md](references/readiness-rubric.md)).
5. **Referee simulation** (optional). Two or three referees with different expertise write reports ([referee-simulation.md](references/referee-simulation.md)).
6. **Apply.** After agreement, apply fixes in the source, rebuild, re-run the checks, and record every change in the revision notes.

```bash
# run from the project folder; <skills> is the folder holding the installed skills
python3 <skills>/sci-manuscript-review/scripts/audit_numbers.py content.py floats.py --evidence evidence/*.json   # D1
python3 <skills>/sci-prose-style/scripts/prose_lint.py <slug>_EN_WithCitations.docx                            # D6
```

## Responding to Reviewers

Read [rebuttal-letters.md](references/rebuttal-letters.md). Quote each comment verbatim, answer it directly, say what changed and where (page, line, figure), and thank without flattery. Disagree with evidence when the reviewer is wrong. Keep the response and the manuscript changes in step; every promised change must exist.

## Output

A review report with: summary verdict and readiness score; blocking findings; major findings; minor findings grouped by type; structural recommendations; a checklist of fixes with owners; and, when requested, referee reports and a draft response letter.

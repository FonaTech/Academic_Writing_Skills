---
name: sci-prose-style
description: >
  Write, rewrite and polish scientific English in any field to the standard of expert reviews and research papers in Nature-family, Science, Cell and leading society journals, and keep an English-Chinese pair in step. Use for drafting sections, deep polishing, removing AI flavour, hype and defensive hedging, fixing staccato or clause-heavy sentences, unifying terminology and abbreviations, writing captions, abstracts, titles, highlights and cover letters, syncing length variants, and translating between English and Chinese without drift. 英文润色, 去AI味, 去叠甲, 短句改写, 术语统一, 中英互译, 学术写作风格. Not for evidence gathering (sci-literature-evidence) or document building (sci-manuscript-build).
---

# Scientific Prose Style

Expert scientific prose reads fast because each sentence carries one claim, each paragraph answers one question, every number has a condition, and nothing is decorative or defensive. This skill turns drafts into that prose for any field and keeps the second language aligned.

## House Style in Fourteen Rules

1. **One claim per sentence.** Median 16–20 words; ceiling about 30. Split at the second verb clause, not in the middle of a noun phrase.
2. **Sentences link; they do not stack.** Join each sentence to the previous one by a shared subject or a light connective. No run of three bare short sentences; no one- or two-sentence orphan paragraphs.
3. **Paragraphs answer one question.** Topic sentence (naming a grouping or a trade-off) → evidence with numbers and conditions → one sentence on what it implies or what comes next. Put old information first and new information last.
4. **Numbers carry their conditions.** Value, unit, what was measured, at what scale, under which condition or protocol, and whether measured, simulated, projected or estimated. Keep the source's *about, up to, estimated, total* and its symbols.
5. **Name the actor.** "In ⟨year⟩, ⟨A⟩, ⟨B⟩ and colleagues measured …", then "The same team …". Use the passive only when the actor is irrelevant.
6. **Verbs, not nominalisations.** "reduces the error", not "achieves a reduction of the error".
7. **State what was done, then what follows.** No defensive sentences (so far, still, only, not yet, has not been shown, remains missing). A limitation is a fact with its scope that leads to the next step. Hedge only mechanisms and extrapolations, once.
8. **No hype, no stock phrases.** Delete adjectives a reviewer cannot check. Replace "plays a crucial role" with what the thing does.
9. **No meta-commentary and no screening voice.** The text never talks about itself, the drafting process or how the literature was screened, counted or graded. A review narrates the field's progress.
10. **Gaps belong to the field, not to one paper.** "⟨Metric⟩ is rarely reported with ⟨condition⟩ [refs]", not "⟨Author⟩ did not report ⟨condition⟩".
11. **Compare like with like.** Never write "N orders lower" across different accounting scopes; state each scope and ask for a common basis. Check every magnitude arithmetically.
12. **Terms and abbreviations are fixed.** Define each abbreviation at first use, again in each caption and table note, and use one spelling throughout.
13. **Cite as you claim.** The citation sits at the end of the clause it supports. A claim the source does not contain is removed or re-attributed. No "in a preprint" in running text.
14. **Every version says the same thing.** Both languages and every length variant carry the same numbers, citation keys and float references, block by block.

Read [style-rules.md](references/style-rules.md) for the full rule set with before/after pairs, and [ai-flavor-lexicon.md](references/ai-flavor-lexicon.md) for the phrases to remove and their replacements.

## Revision Protocol

Work in passes. Each pass has one purpose; do not mix them.

| Pass | Question | Output |
|---|---|---|
| 1 Argument | Does each section make one claim that the evidence supports? Does it read as the field's progress? | reordered or merged paragraphs, cut duplicates and repeated yardsticks |
| 2 Evidence | Does every number, quantifier, symbol and attribution match its source page? | corrected values, conditions, scopes, citations |
| 3 Paragraph | Topic sentence first? One question per paragraph? Ending a synthesis or bridge? | split or merged paragraphs, rewritten endings |
| 4 Sentence | One claim per sentence? Linked, not stacked? Actor and verb clear? | rewritten sentences |
| 5 Lexicon | Hype, defensive phrases, stock phrases, meta-commentary? | cleaned wording |
| 6 Consistency | Terms, abbreviations, units, symbols, float references? | unified terminology |
| 7 Second language and variants | Same content block by block, in every length variant? | aligned translation and synced variants |

Run the linter after passes 4–6:

```bash
python3 scripts/prose_lint.py draft.docx            # or .md / .txt; --json for machine output
python3 scripts/prose_lint.py draft.docx --limits manuscript.json   # apply a project's style.overrides
```

Caps, banned phrases and sentence targets come from `assets/style_limits.json`. The manuscript kit's checker reads an identical copy, so both tools apply the same rules. The linter reports every banned phrase and each cap that is exceeded (for example must above 3, therefore above 5, "rather than" and "X, not Y" above 4 together per 10,000 words). It also reports the sentence profile, overlong sentences, staccato runs, stacked clauses, defensive phrases, further lexicon with weights, hedging and intensifier density, nominalisations, flagged openers, repeated openers, meta-commentary, screening-report wording, number-hygiene problems and abbreviations used before definition. Treat it as a smoke detector: fix every weight-3 hit, review weight-2 hits, and use judgement on weight-1 hits. Flow, fairness and one-idea-per-sentence need a human pass.

## Section Guides

Load only the guide for the section being written.

- Titles, abstracts, key points, highlights, TOC text: [titles-abstracts.md](references/titles-abstracts.md)
- Introductions for reviews and articles: [introductions.md](references/introductions.md)
- Paragraph and sentence craft: [paragraph-sentence-craft.md](references/paragraph-sentence-craft.md)
- Quantitative reporting and fair comparison: [quantitative-reporting.md](references/quantitative-reporting.md)
- Section endings, outlook and conclusions: [outlook-conclusions.md](references/outlook-conclusions.md)
- Captions and table notes: see the sci-figure-design skill (its captions-and-tables reference)
- Chinese drafts, translation and length variants: [bilingual-consistency.md](references/bilingual-consistency.md)

Each guide gives rules, templates with placeholders, constructed before/after pairs and a checklist. The examples use placeholders (⟨method⟩, ⟨metric⟩, ⟨value⟩) so they fit any field; fill them only with sourced content.

## Terminology Table

Keep a table per project (English | abbreviation | Chinese | first-use location | notes) and apply it globally before the consistency pass. [terminology-template.md](references/terminology-template.md) gives the format and the rules for building it from the field's own nomenclature.

## Rewriting Examples

The examples are constructed; placeholders stand for sourced content.

**Hype and stock phrases.**
Before: "It is worth noting that ⟨approach⟩ plays a crucial role in ⟨field⟩, and its ⟨value⟩ ⟨metric⟩ is remarkable, which paves the way for next-generation systems."
After: "⟨Approach⟩ reached ⟨value⟩ ⟨metric⟩ per ⟨unit of account⟩, measured under ⟨condition⟩ without ⟨excluded component⟩ [11]."
Why: the importance phrase, the evaluation and the promise are removed; the number gains its condition and scope.

**Staccato chain.**
Before: "The sensor reads only positive values. The quantity changes sign. Two sensors are used. This doubles the cost."
After: "The sensor reads only positive values, but the quantity changes sign. Two sensors therefore record it as a difference, at the cost of twice the instruments and twice the calibration."
Why: four fragments become two linked sentences; the cost stays attached to the method.

**Defensive gap.**
Before: "So far, only small samples have been studied, and no work has yet measured ⟨endpoint⟩ at scale."
After: "Reported samples range from ⟨N1⟩ to ⟨N2⟩ [refs]. Measuring ⟨endpoint⟩ in a sample of ⟨N⟩ would show whether the effect holds at scale."
Why: the limitation stays as a fact with its scope and turns into the next step.

**Scope-mismatched comparison.**
Before: "⟨Method A⟩ uses about six orders of magnitude less energy than ⟨method B⟩."
After: "⟨Method A⟩ uses ⟨value⟩ per ⟨single operation⟩, whereas ⟨method B⟩ uses ⟨value⟩ per ⟨full task with overheads⟩ [refs]. A same-task measurement split into ⟨components⟩ would allow a direct comparison."
Why: the two values have different scopes, so no ratio is stated.

**Screening voice.**
Before: "Of the ⟨N⟩ studies in our library, ⟨n⟩ provide measured evidence, and we grade the rest as simulated."
After: "Measured results now cover ⟨scale⟩, and simulations extend the approach to ⟨larger scale⟩ [refs]."
Why: a review reports the field, not the authors' screening process; evidence labels stay attached to individual numbers.

**Simulated result reported as measured.**
Before: "The system achieved ⟨value⟩ accuracy on ⟨dataset⟩."
After: "A model simulated with the measured ⟨inputs⟩ reached ⟨value⟩ on a ⟨subset of dataset⟩ [12]."

More pairs, grouped by rule, are in [style-rules.md](references/style-rules.md) and [ai-flavor-lexicon.md](references/ai-flavor-lexicon.md).

## Final Human Pass

The author reads the whole text aloud once before submission. Automated checks cannot judge emphasis, fairness to other groups or the tone of a sentence, and journals hold the authors responsible for every AI-assisted sentence.

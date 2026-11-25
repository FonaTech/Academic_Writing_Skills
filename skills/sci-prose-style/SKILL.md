---
name: sci-prose-style
description: >
  Write, rewrite and polish scientific English in any field to the standard of expert reviews and research papers in Nature-family, Science, Cell and leading society journals, and keep an English-Chinese pair in step. Use for drafting new text in any genre that reads as expert human writing from the first draft, deep polishing, removing AI flavour, hype and defensive hedging, fixing staccato or clause-heavy sentences, unifying terminology and abbreviations, writing captions, abstracts, titles, highlights and cover letters, syncing length variants, and translating between English and Chinese without drift. 论文写作, 英文润色, 中文科研写作, 去AI味, 降AI率, 低AIGC率, 去叠甲, 短句改写, 术语统一, 中英互译, 学术写作风格. Not for evidence gathering (sci-literature-evidence) or document building (sci-manuscript-build).
---

# Scientific Prose Style

Expert scientific prose reads fast because each sentence carries one claim, each paragraph answers one question, every number has a condition, and nothing is decorative or defensive. This skill turns drafts into that prose for any field and keeps the second language aligned.

## Default Drafting Chain

This chain is the default for every request this skill handles, whatever its size and language: a section, a paragraph, an abstract, a caption or table note, a cover letter, a response to referees, a Chinese draft. Apply it from the first draft. These are author-requested editorial preferences; no detector result or expert quality is guaranteed.

1. **Load the guides.** Before writing or rewriting the first paragraph, read [human-line-of-thought.md](references/human-line-of-thought.md). Before writing Chinese, also read [bilingual-consistency.md](references/bilingual-consistency.md). Load the section guide for the part being written (Section Guides below).
2. **Fix the facts list.** Numbers with conditions and evidence labels, citation keys and float references, each from a source. The prose may not add a cause, a motive or a comparison that the sources do not state.
3. **Order by the private questions.** What the reader just learned and what it leaves open; who did what and why; what they saw; what it means and how far it reaches; what it left open. Follow the chain for the genre (guide, section 4). The questions never appear in the text.
4. **Write each paragraph in one go,** with named actors, the field's own terms, conditions in parentheses, and sentence lengths set by the content.
5. **Self-check every paragraph:**
   - no three bare number sentences in a row; each number has its comparison or meaning;
   - explanation connectives (so, because, since, then; 因此、从而、进而) near 8 per 100 sentences or fewer, with most links carried by sentence order and named actors;
   - sentence lengths vary within the paragraph;
   - no questions, embedded questions, musings, counted overviews, aphoristic verdicts, template phrases or promotional frames;
   - the paragraph ends on a fact, not on a forecast or a moral.
6. **Run the linter** when the text is in a file (`python3 scripts/prose_lint.py FILE`): fix weight-3 and weight-2 hits and review weight-1 hits by eye. For text delivered only in the conversation, save a task-local text copy and run the linter before delivery; the copy is a checking aid, not an extra requested deliverable.
7. **Write the second language** from the finished block: the same numbers, citation keys and float references, with its own natural rhythm.

For a light polish, follow section 7 of the guide and keep sentences that already read well. Tables, reference lists and abbreviation lists are formulaic by nature and are not rewritten for style. Worked examples are in the orchestrator skill's case studies 05, 06, 13 and 14.

## House Style in Seventeen Rules

1. **One claim per sentence.** Median 16–20 words; ceiling about 30. Split at the second verb clause, not in the middle of a noun phrase.
2. **Sentences link; they do not stack.** Join each sentence to the previous one by a shared subject or a light connective. No run of three bare short sentences; no one- or two-sentence orphan paragraphs.
3. **Paragraphs answer one question.** Topic sentence (naming a grouping or a trade-off) → evidence with numbers and conditions → the last relevant fact or supported implication. Put old information first and new information last.
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
15. **Write the paragraph as a researcher's line of thought.** Each sentence answers a need the previous one created: a cost, a gap or a consequence. Numbers sit inside reason or comparison clauses, and no three bare number sentences run in a row. The reasoning orders the text but is never voiced in it: no questions, embedded questions ("How much ⟨X⟩ matters depends on …"), musings or counted overviews. Let sentence order and named actors carry most links; a connective on every sentence (so, because, then) is a pattern of its own. Let content set sentence length, so that a paragraph mixes long and short sentences. See [human-line-of-thought.md](references/human-line-of-thought.md).
16. **Keep the author's voice and use the field's exact words.** When editing, keep the draft's terms, spelling variant, tense pattern, way of naming actors and citation style, and change only what a rule requires; sentences that already read well keep their wording. Name methods, materials and metrics as the cited papers do. Choose the verb that says what happened (measured, simulated, fitted, estimated, reported) and the quantity's own name. Do not rotate synonyms for variety: one concept keeps one term.
17. **Depth and correctness come before polish.** A paragraph explains why a result came out as it did, compares only at the same scope, keeps the conditions that change the answer, and mentions the strongest counter-case with its source. A smooth sentence built on a wrong number is worse than a plain one built on the right number (human-line-of-thought.md, section 9).

Read [style-rules.md](references/style-rules.md) for the full rule set with before/after pairs, and [ai-flavor-lexicon.md](references/ai-flavor-lexicon.md) for the phrases to remove and their replacements.

## Revision Protocol

Work in passes. Each pass has one purpose; do not mix them. For new text, first draft each paragraph by section 6 of [human-line-of-thought.md](references/human-line-of-thought.md), then run passes 2–7. For an existing draft, run all passes and follow section 7 of that guide when a paragraph has to be rewritten.

| Pass | Question | Output |
|---|---|---|
| 1 Argument | Does each section make one claim that the evidence supports? Does it read as the field's progress? | reordered or merged paragraphs, cut duplicates and repeated yardsticks |
| 2 Evidence | Does every number, quantifier, symbol and attribution match its source page? | corrected values, conditions, scopes, citations |
| 3 Paragraph | Topic sentence first? One question per paragraph? Does each sentence answer a need the previous one created (rule 15)? Is the paragraph free of the regularities in human-line-of-thought.md, section 1? Ending on a fact or a bridge? | split or merged paragraphs, reordered sentences, rewritten endings |
| 4 Sentence | One claim per sentence? Linked, not stacked? Actor and verb clear? | rewritten sentences |
| 5 Lexicon | Hype, defensive phrases, stock phrases, meta-commentary? | cleaned wording |
| 6 Consistency | Terms, abbreviations, units, symbols, float references? | unified terminology |
| 7 Second language and variants | Same content block by block, in every length variant? | aligned translation and synced variants |

Run the linter after passes 4–6:

```bash
python3 scripts/prose_lint.py draft.docx            # or .md / .txt; --json for machine output
python3 scripts/prose_lint.py draft.docx --limits manuscript.json   # apply a project's style.overrides
```

Caps, banned phrases and sentence targets come from `assets/style_limits.json`. The manuscript kit's checker reads an identical copy, so both tools apply the same rules. The linter reports every banned phrase and each cap that is exceeded (for example must above 3, therefore above 5, "rather than" and "X, not Y" above 4 together per 10,000 words). It also reports the sentence profile, overlong sentences, staccato runs, stacked clauses, defensive phrases, further lexicon with weights, hedging and intensifier density, nominalisations, flagged openers, repeated openers, meta-commentary, screening-report wording, number-hygiene problems and abbreviations used before definition. It also flags the line-of-thought patterns of rule 15: `number-run`, `question-voice` and `thinking-aloud` (weight 2), and `ordinal-enumeration` and `aphorism` (weight 1), plus an advisory when explanation connectives (so, because, since, then) exceed 40 per 10,000 words, and `uniform-rhythm` (weight 1) for a paragraph whose sentences are all about the same length. The sentence profile includes `explain_connectives_per_100_sentences`; keep it near 8 or below. Chinese paragraphs get `zh-template` and `zh-question` (weight 2) and `zh-connective`, `zh-ordinal` and `zh-uniform-rhythm` (weight 1), from the `zh` block of the limits file. Treat it as a smoke detector: fix every weight-3 hit, review weight-2 hits, and use judgement on weight-1 hits. Flow, fairness and one-idea-per-sentence need a human pass.

## Section Guides

Load only the guide for the section being written.

- Titles, abstracts, key points, highlights, TOC text: [titles-abstracts.md](references/titles-abstracts.md)
- Introductions for reviews and articles: [introductions.md](references/introductions.md)
- Paragraph and sentence craft: [paragraph-sentence-craft.md](references/paragraph-sentence-craft.md)
- Drafting and revising any paragraph so it reads as expert human prose: [human-line-of-thought.md](references/human-line-of-thought.md) (regularities to avoid, the private questions, page patterns, the chain for each genre, drafting and revising steps, section openings, depth)
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


## Integration with the 2.2 runtime
The eight standing norms and the default drafting chain apply in every requested genre/language. Read guides only as needed; templates are argument checklists rather than mandatory sentence patterns. For systematic/scoping reviews preserve the actual search, screening counts and appraisal in the appropriate methods/results. Preserve necessary uncertainty, exact technical terms, quotations and author meaning even when a style diagnostic flags them. Diagnostic weights trigger review, not automatic deletion of evidence or qualifiers.

The default precise profile retains the full 1.3 style-limit table and the broad advisory lexicon. Compact, explanatory and generic profiles remain available with --profile and --known; they do not disable the common English/Chinese drafting-chain checks. Captions independently define abbreviations. The manuscript builder uses the same shared diagnostic functions without replacing evidence, source-freshness or release checks.

# Audit dimensions and agent prompts

Each dimension runs as an independent pass. For manuscripts over about 5000 words, split D1 and D2 by section. Every finding uses this record:

```json
{"id": "D1-07", "dimension": "D1", "severity": "blocking|major|minor", "location": "s6.2-b",
 "claim": "exact text from the manuscript", "evidence": "source file, page, verbatim quote",
 "verdict": "what is wrong", "fix": "replacement text or action", "confidence": "high|medium|low"}
```

## D1 Numbers
For every number with a unit, percentage, ratio or count in paragraphs, captions, table cells and notes:
1. find the evidence record or the source page;
2. compare value, unit, rounding and significant figures;
3. check what the number measures: within-sample vs between-sample variation, a per-step vs a per-run value, a subgroup vs the whole cohort, a selected subset vs everything tested;
4. check the conditions the source states (temperature, dose, dataset, sample size, model, region, time window);
5. check that the source's quantifier survived: "about", "up to", "at least", "estimated", "total", "median" must not be dropped or added;
6. check every derived magnitude arithmetically ("three orders of magnitude", "a five-fold gain", "half the cost") against the two source values.
Blocking when the value, its meaning or its quantifier is wrong. `audit_numbers.py` lists quantities without matching evidence and is the starting list.

## D2 Attribution
For every citation, read the sentence it supports and search the cited paper's text for the claim. Typical failures:
- citation numbers shifted by one after an insertion (text cites [9] for work that is reference 10);
- a review cited for a statement it does not contain (e.g. a review of a neighbouring field cited for the target subject's results);
- a secondary source cited as if it were the primary paper;
- one citation covering a sentence with several independent claims;
- a mechanism, motive or purpose added that the source does not state ("to eliminate X", "because Y" where the paper reports only the result);
- the source's own symbol or term renamed (keep it and define it).
Blocking when the source does not support the sentence.

## D3 Evidence level
Label each result: measured, simulated, projected, estimated, restated by a review (reported-survey), abstract-only. Blocking when a simulated or projected result reads as measured; major when the label is missing. The label sits with the number; a separate disclaimer sentence is not needed (see D11).

## D4 Comparison fairness
Compare only values with the same accounting scope (component, sample, cohort, site, whole system), the same definition of the quantity, the same conditions or a stated normalisation, and the same dataset or population. Flag:
- rankings of values counted over different scopes;
- "N orders of magnitude better" claims across scopes (state each scope instead and name the same-task measurement that would settle the comparison);
- headline numbers whose stricter-scope value is omitted;
- comparisons with a baseline that the source did not use.
See sci-literature-evidence, comparison-fairness.md.

## D5 Structure
- Does each section and subsection make one argument that its first paragraph states?
- Is any argument made more than once? (Count restatements of the same point.)
- Compared with the reference reviews, which topics, comparisons or open problems are missing?
- For reviews: does each application or line of work explain which property or mechanism serves which function, with the strongest comparator?
- Are derivations in the main text that belong in boxes?
- Does each table appear once in the text, without its contents restated in prose?

## D6 Style
Run `prose_lint.py`. Report the sentence profile, weight-3 lexicon hits, meta-commentary, hedging stacks, repeated openers, staccato runs (several short bare sentences in a row) and orphan paragraphs (one or two sentences). Quote two or three representative sentences with rewrites; do not list every hit.

## D7 Terminology
- each abbreviation defined at first use in text, and again in each caption and table note;
- no abbreviation defined twice in the text; no abbreviation used once only;
- one spelling per term (pick one of the field's variants and keep it);
- units written one way throughout;
- second-language terms fixed by the terminology table.

## D8 Floats
- figures and tables numbered by first mention and placed after the first citing paragraph;
- every panel referenced in the text; captions self-contained with abbreviations defined;
- data panels: values in `panel_data.json`, evidence semantics visible, `figure_kit.py verify` passed;
- schematics: labels match the whitelist, no invented numbers, physically correct geometry;
- labels baked into artwork match the current figure numbers and panel letters;
- tables: one property per column, units in headers, "n.s." (not stated) defined in the note, evidence and scope columns where needed, a Year column generated from the reference metadata for evidence tables.

## D9 Bilingual
Block by block: numbers, citation keys, float references, section references. Numbers keep the same form in both languages. Then terminology and tone: the second language reads naturally, not as a calque; no fact, hedge or connective added or dropped in one language only.

## D10 References
DOIs resolve to the cited paper (Crossref title match), print year and volume correct, conference names correct, no duplicate entries, no unused entries, preprints linked to their published versions, abstract-only sources marked in the revision notes.

## D11 Voice
For reviews and Discussions:
- the text tells the field's progress (problem → idea → realisation → result), not the reviewer's screening of papers ("we found", "of the N papers examined", "none of the studies");
- reporting gaps are stated at field level with citations ("X is rarely reported with Y [@a; @b]"), never as per-paper fault-finding ("A et al. did not state…");
- no defensive or disclaimer sentences ("so far", "to date", "still", "not yet", "has not been shown", "remains missing"); each gap is turned into the next experiment or design implication;
- preprint status lives in the reference list, not in the sentence ("in a preprint");
- no internal codes (source ids, evidence-table row numbers) in text or notes;
- subsection endings synthesise and bridge forward; at most one numbered ending in the whole text.
Major when the voice reads as an audit report; minor for isolated phrases.

## D12 Variant and version sync
When the manuscript exists in several lengths or languages:
- every fix (number, citation, wording rule, reviewer comment) is present in every variant and both languages;
- material that appears only in the longer variants meets the same standard as the shortest one;
- each variant is within its word budget (body text only) and carries the full tables;
- the correction log lists each fix with the variants and blocks it reached.
Blocking when a corrected number survives uncorrected in any variant.

## Verification pass
For each blocking or major finding, a separate agent (or a separate pass by the same reviewer, if the author asked for no sub-agents) receives only the finding and the source paths and tries to refute it. Keep the finding if the refutation fails; downgrade to "check" if the evidence is ambiguous.

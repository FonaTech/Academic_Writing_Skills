---
name: sci-prose-style
description: >
  Draft, revise or translate scientific prose across disciplines while preserving evidence, conditions, uncertainty, terminology and author intent. 学术润色、科学写作、中英翻译、术语统一。 Use for prose; evidence gathering and document construction have separate skills.
---

# Scientific prose

Improve the argument and clarity while preserving what the evidence actually supports. Journal conventions and the author's requested style take priority over a house vocabulary list.

## Revision passes
1. Argument: define each section's question, contribution, supporting evidence and limits. Test alternatives and avoid duplication.
2. Evidence: check attributed claims, quantities, units, methods, scope and uncertainty against their individual records. Mark gaps instead of filling them.
3. Paragraphs: keep one coherent question per paragraph and put the topic sentence first in the default precise style. Make the connection to the paper clear; vary the remaining sentence structure with the argument.
4. Sentences: split when qualifications or clauses obscure meaning. Preserve causal distinctions, technical detail and necessary conditions. One principal claim per sentence is a useful default, not a rule against natural compound sentences.
5. Wording: remove unsupported praise and empty phrasing. Keep legitimate technical words and justified emphases; no ordinary word is globally forbidden.
6. Consistency: use stable terms, correct symbols/units and contextual abbreviation definitions. Choose conventions required by the venue.
7. Translation if requested: align blocks and scientific meaning, including quantities, units, polarity, comparison direction, uncertainty and evidence status. Matching numbers is insufficient.

## Style settings
`assets/style_limits.json` is the default precise profile: one main claim per sentence, topic sentence first, a 16–20-word English median and a ceiling around 30 words. Avoid formulaic AI flavor, hype and empty transitions. These are editorial targets; preserve scientific qualifiers and necessary technical meanings. Alternative profiles are opt-in.

Default precise style and compact, explanatory and generic alternatives are stored under assets/style_profiles/. They are editorial profiles, not scientific-quality laws.

Read [style-rules.md](references/style-rules.md) for general decision criteria and [bilingual-consistency.md](references/bilingual-consistency.md) for translation checks. Inspect prose diagnostics in context; never delete a qualifier or required technical term simply to obtain a clean report.

```bash
python3 scripts/prose_lint.py draft.md --json
```

The author retains scientific responsibility. Identify any AI-assisted review accurately and never present it as human expert approval.

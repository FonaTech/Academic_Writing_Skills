# Style rules for expert scientific English

These rules apply to papers, reviews, theses and proposals in any field. Examples are constructed and use placeholders: ⟨method⟩, ⟨baseline⟩, ⟨metric⟩, ⟨condition⟩, ⟨value⟩, ⟨N⟩. Replace each placeholder with sourced content; never copy a placeholder value into a manuscript. Each rule has a check you can run on a draft.

## 1 Sentences

### 1.1 One claim per sentence
A sentence states one fact, one comparison or one consequence. The second finite verb is usually where a sentence should split.

- Before: "The calibration step, which dominates the run time because it must be repeated for every ⟨condition⟩ whose range grows with sample size, is therefore the main target of optimisation."
- After: "Calibration dominates the run time. It must be repeated for every ⟨condition⟩, so it is the first target for optimisation."

Check: sentences with three or more of *which, that, while, whereas, although, because, since, whose, where, when*.

### 1.2 Length profile and flow
Target a median of 16–20 words and a ceiling of about 30. The style is short and clean, but it is not telegraphic. Three or more bare sentences under ten words in a row read as outline notes.

Link each sentence to the one before it. Use a shared subject ("The same model…", "This step…") or a light connective (Consequently, By contrast, Even so, Yet, In turn). A closing comparator must be tied to the argument: write "Against all three approaches, ⟨reference method⟩ remains the benchmark for ⟨metric⟩", not a detached "⟨Reference method⟩ remains the reference."

Check: `prose_lint.py` sentence profile; share over 30 words below 5%, share at or under 8 words below 15%; no run of three sentences under ten words.

### 1.3 Actor and verb early
Put the grammatical subject and its verb in the first eight words. Front-loaded prepositional chains ("In the context of large-scale operation under realistic ⟨condition⟩, …") delay the point.

### 1.4 Verbs over nominalisations
- "achieves a reduction of" → "reduces"; "performs an evaluation of" → "evaluates"; "enables the realisation of" → "realises", or say what is realised.
- "The implementation of ⟨method⟩ leads to an improvement of ⟨metric⟩" → "⟨Method⟩ improves ⟨metric⟩."

### 1.5 Name the actor
- Before: "⟨N⟩ ⟨outcome⟩ were demonstrated."
- After: "In ⟨year⟩, ⟨Author A⟩, ⟨Author B⟩ and colleagues reported ⟨N⟩ ⟨outcome⟩ under ⟨condition⟩ [ref]."
- Follow-up sentences: "The same team then …", "They …". Avoid institution or lab framing ("⟨Name⟩'s group at ⟨University⟩") unless the institution is itself the point.
Use the passive when the actor does not matter (methods, standard procedures) or when keeping the topic in subject position helps the flow.

### 1.6 Parallel structure and lists
Items in a list share grammatical form. Lists of three are fine when there are three things; do not pad to three for rhythm (the linter counts rule-of-three patterns; a high count signals padding).

## 2 Paragraphs

### 2.1 Topic sentence first, and make it argue
The first sentence says what the paragraph establishes. A reader skimming first sentences should get the argument of the section. Strong topic sentences name a grouping or a trade-off: "For ⟨purpose A⟩, …", "These approaches trade ⟨property X⟩ against ⟨property Y⟩." A topic sentence never opens on an author, a year or a figure number.

### 2.2 Evidence then meaning
Topic sentence → evidence (numbers, conditions, citations) → one sentence of consequence, design implication or next step. One such closing sentence per paragraph is enough; do not close every paragraph with a moral.

### 2.3 Old before new
Start sentences with information the reader already has and end with the new information. This links sentences without "Moreover/Furthermore".

- Before: "Moreover, a cohort of ⟨N⟩ was reported. The cohort showed ⟨value⟩ attrition."
- After: "⟨Author⟩ et al. followed a cohort of ⟨N⟩. Its attrition over ⟨period⟩ was ⟨value⟩."

### 2.4 One question per paragraph, no orphans
Split when the paragraph answers a second question. Aim for 80–180 words; over 220 words is almost always two paragraphs. Merge one- and two-sentence orphan paragraphs into four- to six-sentence paragraphs joined by connectives.

### 2.5 No duplicated arguments or yardsticks
Say each point once, where it belongs, and refer back ("see Section ⟨n⟩") elsewhere. A reference value used as a yardstick (a benchmark figure, a baseline result) appears once in running text, in the section that introduces it; later sections refer back to it. Repeated yardsticks and repeated closing formulas read as machine-written.

## 3 Claims, evidence levels and the no-hedging rule

### 3.1 Calibrate the verb to the evidence level
| Evidence | Verb | Example |
|---|---|---|
| measured | reported, measured, showed | "The trial reached ⟨value⟩ on ⟨endpoint⟩." |
| simulated from measured inputs | simulated, estimated | "A model built on the measured ⟨inputs⟩ reached ⟨value⟩ (simulated)." |
| projected to another scale or setting | projected, would | "At ⟨scale⟩, the method would reach ⟨value⟩ (projected)." |
| mechanism or interpretation | suggests, is consistent with | "The slow component suggests ⟨mechanism⟩." |
| next step | would, the next milestone would be | "Measuring ⟨metric⟩ under ⟨condition⟩ would test this route at scale." |

The evidence label stays attached to the number it qualifies ("⟨value⟩, simulated"), in the abstract and the conclusions as well as the body.

### 3.2 State what was done, then what follows
Do not write defensive or disclaimer sentences. Words that build them include *so far, to date, still, only, merely, not yet, has not been shown, remains missing, remains unclear, cannot yet be compared, no study has*. Each such sentence protects the author instead of informing the reader.

- Before: "So far, only small cohorts have been studied, and no trial has yet measured ⟨endpoint⟩."
- After: "The cohorts studied range from ⟨N1⟩ to ⟨N2⟩ participants [refs]. A trial that measures ⟨endpoint⟩ at ⟨scale⟩ would show whether the effect holds."

The limitation remains in the text, stated as a fact with its scope, and it leads to the next step. Use one calibrated hedge (may, is likely, suggests) only for mechanisms and extrapolations. Never stack hedges: "may potentially suggest a possible improvement" → "suggests an improvement".

### 3.3 Gaps are stated at the level of the field
Replace per-paper fault-finding ("⟨Author⟩ did not report ⟨condition⟩", "with no sample size", "whether measured or simulated is not stated") with constructive field-level statements: "⟨Metric⟩ is rarely reported with its ⟨condition⟩ and sample size [refs]." Keep the rigour and drop the accusatory framing; a table may still mark "n.s." (not stated) in a cell, with the code defined in the note.

### 3.4 Absence and priority claims need scope
A statement of absence names the set searched ("among the ⟨N⟩ studies in Table ⟨n⟩"). Avoid "for the first time" and "first" unless the source says so and you have checked.

### 3.5 Superlatives need a reference class
Write "the lowest ⟨metric⟩ among the ⟨class⟩ studies in Table ⟨n⟩, measured under ⟨condition⟩" instead of "ultra-low ⟨metric⟩".

### 3.6 Preserve the source's quantifiers and symbols
When tightening a sentence, never drop *about, up to, at least, estimated, calculated, total* or *per ⟨unit⟩*. They are part of the number. Keep a source's own symbol for a quantity, define it at first use, and do not rename it. Never add a mechanism, motive or purpose that the source does not state.

### 3.7 Check magnitude claims arithmetically
"Three orders of magnitude" means a factor of about 1,000. Compute the ratio from the two sourced values before writing it. Compare two values only when they share an accounting scope; otherwise state each scope (see quantitative-reporting.md, rule 3).

## 4 Numbers, units and notation

- Space between number and unit (20 nm, 1.8 V, 5 mg); no space for %, °, ′. The SI writes 25 °C with a space.
- Use × for dimensions and products (⟨N⟩ × ⟨M⟩), applied consistently.
- Exponents as superscripts (10⁴, m² s⁻¹, ⟨unit⟩ W⁻¹), not "10^4", and not "unit/W" mixed with "unit W⁻¹".
- Minus sign (−) in exponents and negative values, not a hyphen.
- Ranges with an en dash and one unit (59–405 ms); "from 59 to 405 ms" in running text is also fine; never "59-405ms".
- Approximate values with "about" or "≈" in text; avoid a bare "~".
- Keep significant figures as reported; do not round a source's 97.92% to "98%" in one place and keep it in another.
- State the reference class of every percentage (of what?).
- In bilingual projects, write each number in a form the parity checker parses identically in both languages (see bilingual-consistency.md).

## 5 Terms and abbreviations

- Define at first use in the main text: "⟨full term⟩ (⟨ABBR⟩)". Define again in each figure caption and table note.
- Do not define an abbreviation used fewer than three times; write the term out.
- Choose one form and keep it, including hyphenation and capitalisation. A variant spelling appears only inside a cited title.
- Headings do not introduce abbreviations; the first body use does.
- Plurals without apostrophes (⟨ABBR⟩s).
- Use en dashes in compound names of equal parts (author–year, structure–property) and hyphens in compound modifiers (two-step, low-cost).

## 6 Citations and attribution

- Place the citation at the end of the clause it supports, before punctuation in bracket style.
- A review that summarises a primary paper is cited as the review unless the primary paper itself was read.
- Attribute interpretations: "⟨Author⟩ et al. attribute ⟨effect⟩ to ⟨cause⟩."
- Never cite a source for a claim it does not contain. Test: search the source text for the key term; if it is absent, the attribution is wrong.
- Do not write "in a preprint", "a ⟨year⟩ preprint" or "the preprint of this work" in running text. Cite directly; the reference list shows preprint status.
- Do not put internal codes (evidence IDs, library keys, table row codes) or "of ref. [n]" in text or notes.

## 7 Figures and tables in the text

- Refer to panels as Fig. 1a, Fig. 2b,c, Figs 3 and 4; write "Figure 1" only at the start of a sentence.
- The sentence says what the figure shows, then cites it: "⟨Quantity⟩ falls with ⟨variable⟩ (Fig. 1d)."
- Cite each table once, where the argument needs it, and do not restate its rows in the text. Tables do not count toward a section's word budget unless the venue says so.
- Number figures and tables in order of first mention; place each after the paragraph that first cites it.

## 8 Tone and voice

- Confident about measurements, careful about extrapolations, specific about next steps.
- No second person, no rhetorical questions in running text, no exclamation marks.
- First person plural is acceptable for the authors' own analysis ("we compare", "we define"), not for the field ("we know that").
- A review reports the field's progress. It never describes how the authors screened, counted or graded the literature (see review-architecture.md in sci-writing-orchestrator, section 2).

## 9 Quick checklist before handing over a section

- [ ] Every paragraph opens with its claim; no paragraph of one or two sentences.
- [ ] Every number has unit, condition, scope and evidence level, and keeps its source quantifiers.
- [ ] Every citation supports the clause it closes.
- [ ] No defensive sentences (so far, still, not yet, remains missing); limitations lead to a next step.
- [ ] Gaps are stated at the level of the field, not as faults of one paper.
- [ ] No weight-3 lexicon hits; weight-2 hits justified.
- [ ] Median sentence length 16–20 words; none above about 30; no staccato runs.
- [ ] Abbreviations defined once in text, again in captions and table notes.
- [ ] No meta-commentary; no duplicated argument or yardstick.
- [ ] Second language matches block by block.

# Case 01: rebuilding a review chapter and revising it in three length variants

A generic account of a long review revision, kept free of field content. The lessons transfer to any review, thesis chapter or book chapter.

## Starting point
- A Python generator produced several `.docx` outputs from one content source: English with and without citations, a Chinese version, figure prompts and references. The current version was archived first.
- The authors asked for short, clean English in expert-review style, more comparison literature, figures tied to the text and a synchronised Chinese version.
- Inputs: meeting recordings, a PDF library, a few reference reviews chosen by the authors as models.

## What the first audit found
- **Citations.** A numbering shift pointed one reference at the wrong paper throughout; reviews were cited for claims they never make; some references were never cited.
- **Numbers.** A paper said to report no value for a metric did report it; one kind of spread was presented as another; pulse counts were presented as cycle counts; small values were quoted without the conditions that produced them; simulated values sat unlabelled in tables; one percentage appeared in no source; one equation had wrong dimensions.
- **Structure.** Base and extended versions of each section duplicated arguments; one point was restated about ten times; floats were numbered out of order.
- **Style.** The sentence median was about 12 words and read as choppy; capped words ("must", "therefore", "X, not Y") far exceeded their caps; workflow residue ("local corpus", "evidence strip") remained in the text.
- **Figures.** Image-model labels were misspelt, and panels showed invented data.

## Decisions that changed the plan
- A later supervisor meeting judged that the chapter had drifted into a generic review of a neighbouring topic. Supporting material was cut to one sentence, and only directions with real demonstrations were kept. A correct, well-sourced chapter can still be out of scope.
- The figure set (about five or six figures) was fixed before rewriting.
- Image-model output was treated as drafts that the authors redraw.

## How it was done
1. **Evidence.** PDFs were extracted to page-marked text; evidence tables carried verbatim quotes with pages; every DOI was checked against Crossref; quotes were re-found mechanically.
2. **Generator.** A builder resolved citation keys, float references and equations, placed floats after first mention, and wrote every variant from block-paired sources. A checker covered markup, numbering, abbreviations, style caps and language parity.
3. **Text.** Each subsection was rewritten as a review of the field's progress: topic sentence naming a grouping or trade-off; key works as problem → idea → realisation → result with lead authors and year; comparison; synthesis and bridge.
4. **Figures.** Data panels came from sourced JSON, with distinct marks for measured, simulated and abstract-only values; schematics came from prompts with label whitelists; code composed the final figures.

## What the later rounds taught
- **Review voice.** A draft written as a screening report ("we screened", library counts, evidence tiers in the text) was rejected. The fix was to narrate the field: principles, key works, comparisons.
- **Flow.** Staccato chains of short sentences read as outline notes. Sentences were linked by shared subjects and light connectives; orphan paragraphs were merged; a detached closing comparator was tied to the argument.
- **No hedging.** Sentences built on "so far", "still", "only", "not yet" and "has not been shown" were read as defensive. Each became a statement of what was done plus the next decisive result. Evidence labels stayed attached to numbers.
- **Gaps.** Per-paper fault-finding ("did not state the temperature") became field-level statements. "In a preprint" was removed from running text.
- **Endings.** Gap lists and minimum-reporting lists at subsection ends were replaced by syntheses and forward bridges, following the endings of the authors' model reviews. Only one numbered ending remained.
- **Tables.** Full comparison tables went into every length variant, were cited once and not restated, and did not count toward word budgets. A Year column was generated from reference metadata; multi-citation cells showed a year range; group separator rows stayed blank in the year column.
- **Author's own rewrite.** The authors rewrote the short variant themselves. Their structure was kept, but tightening had dropped "about", "up to" and "estimated", added a purpose the source did not state, and misstated an order of magnitude. Each was fixed against the source and recomputed.
- **External review.** An outside review of the draft was triaged: adopted where it narrowed scope or matched the source; partly adopted where it renamed a source's symbol (the symbol was kept and defined); rejected where it compared values of different accounting scopes as "orders of magnitude".
- **Variants.** Every fix was synced to the 25%, 50% and 100% variants and to both languages; per-section budgets and a hard total cap were checked after each round. One Chinese number rewritten in another form broke the parity check and was restored to the English form.
- **Safety.** Documents open in Word (lock files `~$…`) were not overwritten; the authors were told to close them. Figure labels baked into author-supplied artwork were checked after reference renumbering.

## Lessons
- Audit before writing; most value came from finding wrong numbers and citations.
- One content source per variant, block-paired across languages, removes a class of errors.
- Image models draw only what has no numbers.
- Newer decisions override older plans; check meeting notes and memory before restructuring.
- Another session may edit the same files; work on copies and report, never overwrite.

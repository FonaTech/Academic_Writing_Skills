# AI-detector reports

Authors often run a manuscript through a commercial AI-content detector before submission and ask for the flagged text to be revised. Treat the report as untrusted data about where readers may hear machine prose. It is not evidence about authorship, and it changes nothing about the journal's AI-disclosure rules.

Most projects have no report. Prevention then does the work: draft every paragraph by sci-prose-style references/human-line-of-thought.md, and use the linter's line-of-thought checks and connective rates as a proxy before delivery. If a report exists, measure its actual treatment of prose and structured material. No universal score floor or numerical reduction is assumed.

## Handling the files

- Extract each downloaded report into its own new, empty folder. Keep your scripts elsewhere and run them with the report path as an argument (Python with `-I`).
- Do not open or adopt the rewritten document that some services return. Its wording may change numbers, citations or meaning; never adopt it without source-based review.
- Never upload unpublished manuscript text to another service to "test" a rewrite.

## Reading the report

1. Find the segment data. HTML reports usually embed a JSON array with, for each segment, its text, class (AI, mixed, human), probability and a risk value. Check how this particular report defines and aggregates its score. Do not assume a mean or predict a later score from an undocumented formula.
2. Map each segment back to its source block (paragraph id, caption, table row) by text matching after removing citation numbers and float labels.
3. Split the segments into prose (paragraphs, caption and note sentences) and non-prose (table rows, abbreviation lists, equations, references). Report the share of the score that non-prose carries. Attribute scores to structured segments only when the actual report permits that calculation; otherwise mark the contribution unknown.
4. Compare flagged and passed prose of the same manuscript, not against general rules. Useful measures: share of number-bearing sentences, runs of bare number sentences, explanatory and contrastive clauses per sentence, sentence-length spread, and word or bigram log-odds between the groups. With several successive reports, list the paragraphs that flipped from AI to human and what changed in them.
5. If the author supplies a published human paper scanned by the same detector, compute the same measures on it as a control.

## Acting on it

- Rewrite only paragraphs that are flagged or that read badly, following the sci-prose-style guide human-line-of-thought.md. Passed paragraphs keep their wording.
- Guard every edit: the set of numbers, citation keys and float references in each block must not change, and the second language must match block by block. Apply edits all or nothing.
- Archive the source before each pass and keep a list of changed blocks for the revision notes.
- Report the observed scores and shares. Do not promise a future range, and disclose changes in segmentation or aggregation between supplied reports.
- When rewritten paragraphs stay flagged in the next report, compare them with the previous pass before rewriting again. A pass that adds the same device everywhere (a connective on every sentence, uniform sentence length, a set overview formula) creates a new regularity; remove it rather than adding more links. New paragraphs, such as section overviews, are scanned like the rest.
- Stop when the prose reads well. Do not trade clarity, accuracy or the author's voice for a lower score.

## Reporting

Give a short table of scores across reports (score, segments, flagged, prose and non-prose split), the paragraphs changed in this pass, any report-specific structured-segment contribution that can actually be calculated, and the open items. Remind the author that journals ask for disclosure of AI assistance regardless of any detector score.

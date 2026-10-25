# Architecture of a strong review

This guide covers how a review in any field is organised, from the primary axis to the outlook, and how it reads: as an expert's account of the field's progress. Examples use placeholders (⟨subject⟩, ⟨mechanism⟩, ⟨method⟩, ⟨metric⟩, ⟨value⟩). Prose-level rules are in the sci-prose-style skill.

## 1 Skeletons that work

- **Hierarchy review.** Runs up a ladder of levels in the field (for example mechanism → component → assembly → system → application; molecule → cell → tissue → organism; theory → method → validation → deployment). Each level has its own metrics and comparison table.
- **Mechanism-first review.** Runs from the underlying mechanism to its engineering or control, the routes that follow, and the application each route serves. Its outlook returns to the mechanisms.
- **Application-domain review.** Puts a constraint table up front (the requirements every application imposes) that every application section refers to. It fails without the shared table.
- **Problem–approach review.** Names a central problem and compares families of approaches against the same criteria.

Avoid the one-paper-per-section review and the purely chronological survey. Order only a history section by date.

## 2 Voice: a review of the field, not a screening report

A review tells the reader where the field stands, how it got there and what the key works showed. Each body subsection follows the logic of the work it describes: problem → idea → realisation → result → impact. It explains the principle or mechanism behind a result and compares routes against each other.

- Name the key works and their lead authors with the year: "In ⟨year⟩, ⟨A⟩, ⟨B⟩ and colleagues …", then "The same team …". Avoid institution or lab framing unless the institution is the point.
- Never describe how the literature was searched, screened, counted or graded in the text: no "our corpus", "we screened ⟨N⟩ papers", library counts, "evidence level" or tier tags in running text, audit tags or internal IDs. A methods box or the SI may describe the search if the venue asks.
- Evidence labels (measured, simulated, estimated, projected, abstract-only) stay attached to individual numbers; they are not a narrative device.
- State gaps at the level of the field ("⟨metric⟩ is rarely reported with ⟨condition⟩ [refs]"), never as faults of individual papers.
- Do not write defensive sentences (so far, still, not yet, remains missing). State what was achieved and the next decisive result.
- Do not mention preprint status in running text; the reference list shows it.

## 3 Scope discipline: the review is about its subject

A review of ⟨subject⟩ for ⟨application⟩ is judged on what it says about ⟨subject⟩. Supporting topics grow easily into chapters of their own; cut them back.

- Every section title and topic sentence names the target subject.
- Non-target comparators get one or two sentences per section to set the bar, and never a subsection of their own. Tie each comparator to the argument ("Against all three routes, ⟨comparator⟩ remains the reference for ⟨metric⟩").
- Generic background is cited to existing reviews and not rederived.
- Chapters written by co-authors are not repeated; cross-reference them. If the parent document has its own challenges chapter, a chapter's last section is a short synthesis.
- Applications keep only the directions with real demonstrations; thin directions go into one outlook paragraph or are dropped.
- Deep-read the few leading papers per direction; summarise the many homogeneous ones as a group.
- Decide the figure set before writing, because the figures define the story.
- Newer decisions (a meeting, a supervisor's note) override older plans; check them before restructuring.

## 4 Rules

### Frame and introduction

1. **Take the primary axis from the hierarchy or the mechanism.** Order top-level sections along a ladder of levels or a causal chain. Use classes of subject only inside those sections; a list of classes as the axis marks a catalogue.
2. **State the sorting criterion in one sentence before the first taxonomy section**, in the form "we divide ⟨X⟩ into ⟨A⟩ and ⟨B⟩ according to whether …".
3. **Give parallel units parallel labels and keep one order everywhere**: text, figures, tables and outlook.
4. **Say what earlier reviews covered and what this one adds.** Name two or three recent reviews and the dimension each leaves out (period, level, viewpoint). A field-level grand challenge is not a review gap.
5. **State the scope and inclusion rules, and end the introduction with a roadmap that names the axis.** Check every section number against the headings.
6. **Keep primers to what the later comparisons use.**
7. **State the evaluation criteria before the survey, then judge each case against them.** Give the figures of merit and their required values, each with its accounting scope.

### Body sections

8. **Write every body subsection as principle, key works with numbers, comparison and synthesis** (template 5.2). Non-target comparators take one or two sentences.
9. **Discuss three to eight works per subsection and narrate one to three in detail.** Put the rest in grouped citations or table rows, compared with each other.
10. **Open each paragraph on a concept that names a grouping or a trade-off**; named authors follow in the next sentence. Use one attribution convention throughout, and keep "we" for the review's own analysis.
11. **Attach level and status to every headline number.** Flag any value from a different scope or a simulation placed beside a measured one; never rank values of different scopes.
12. **One point, one place.** State a claim once with its evidence and refer back elsewhere. A yardstick value appears once in running text.
13. **Let transitions carry the argument.** The section opening frames the order of its subsections; each subsection ends on a hand-off to the next. Avoid templated endings that repeat across subsections.

### Figures, tables and boxes

14. **Draw one original frame figure and, where data allow, one original benchmark map.** The frame figure is a block diagram or taxonomy that later sections cite. The map plots metric against metric across works with stated normalisation.
15. **Reprint only panels that carry comparison evidence.** Credit each panel, remove the source's voice ("our", "proposed"), and reuse CC BY panels with attribution or request permission for the rest.
16. **Open every caption with a title that names what the figure shows** (sci-figure-design, captions reference). Close with the normalisation or data source.
17. **Give each comparison-table family one fixed column set,** including a Year column generated from reference metadata. Mark missing data with a defined code ("n.s."). Cite each table once in the text and do not restate its rows.
18. **Use boxes for derivations or accounting that would break the argument,** and key points for findings.

### Synthesis and outlook

19. **Place a synthesis between the survey and the outlook,** mapping classes to the applications they suit, with design rules.
20. **Order applications by what they demand, and map each back to the taxonomy.** Each application section states property → function → best demonstration with its level → strongest comparator → next decisive result.
21. **Re-slice the outlook along the body's axis and give targets numbers.** The outlook guide in sci-prose-style (references/outlook-conclusions.md) gives templates. End the review on a synthesis of what the field can now do.

## 5 Templates

### 5.1 Review skeleton (five to seven top-level sections)

| Section | Content |
|---|---|
| Introduction | stakes with one number → technical gap → earlier reviews and what they miss → scope → roadmap naming the axis and the frame figure |
| Frame section | frame figure, the sorting criterion in one sentence, figures of merit with required values (Table 1) |
| One section per level or route | subsections follow 5.2; tables and maps placed after first citation |
| Synthesis | which class suits which application, design rules |
| Outlook | present value (level, status), target and decisive next result, in the order of the body |

### 5.2 Subsection micro-structure

| Slot | Content |
|---|---|
| S1 | topic sentence naming the requirement, grouping or trade-off |
| S2–S4 | key works: problem → idea → realisation → result, each with lead authors and year, a number with its condition and level, and the citation at clause end |
| S5 | comparison with the alternative route or the Table 1 criterion, under the same accounting |
| S6 | synthesis or design implication, then the bridge to the next subsection |

Shape: *For ⟨purpose⟩, ⟨route A⟩ and ⟨route B⟩ trade ⟨property X⟩ against ⟨property Y⟩. In ⟨year⟩, ⟨A⟩, ⟨B⟩ and colleagues showed that ⟨mechanism⟩ gives ⟨value⟩ under ⟨condition⟩ [ref]. The same team then scaled the approach to ⟨scale⟩, reaching ⟨value⟩ [ref]. ⟨Route B⟩ avoids ⟨cost⟩ but ⟨penalty⟩ [refs]. Both routes therefore depend on ⟨shared property⟩, which Section ⟨n⟩ takes up.*

### 5.3 Key point and table note

| Element | Content |
|---|---|
| Key point | one finding of 20–35 words with its number, level and scope |
| Table columns | Ref.; Year (generated); subject or route; scale; conditions; metrics with units; level; status |
| Table note | defines every abbreviation and code ("n.s., not stated in the source; values extrapolated from shorter tests are marked a") |

## 6 Anti-patterns and fixes

| Pattern | Before (constructed) | After |
|---|---|---|
| The review's coverage as the gap | "This review addresses the need for a comprehensive understanding of ⟨topic⟩." | "Published studies of ⟨topic⟩ report ⟨metric⟩ under different ⟨conditions⟩, so they cannot be ranked; Section 5 sets out the common basis a comparison needs." |
| Spec-sheet praise | "⟨Subject⟩ is notable for its superior metrics: ⟨value 1⟩ [11], ⟨value 2⟩ [12], ⟨value 3⟩ [13]." | "Best values come from different studies [11–13]; a single ⟨unit⟩ meeting all three under one protocol would make ⟨subject⟩ a candidate for ⟨application⟩." |
| Simulation as proof | "Simulations prove the outstanding potential of this approach [refs]." | "Simulated ⟨models⟩ using measured ⟨inputs⟩ reach ⟨value range⟩ on ⟨task⟩ [refs]; a hardware or field test at ⟨scale⟩ would be the next decisive result." |
| Screening narrative | "We screened ⟨N⟩ papers; ⟨n⟩ provide measured evidence." | "Measured results now reach ⟨scale⟩ [refs], and simulations extend the approach to ⟨larger scale⟩ [refs]." |
| Paper-by-paper fault list | "⟨A⟩ did not report ⟨condition⟩; ⟨B⟩ gave no sample size." | "⟨Metric⟩ is rarely reported with ⟨condition⟩ and sample size [A; B]." |
| Gap-list ending | "Missing are: (i) …, (ii) …, (iii) …" at the end of every subsection | a synthesis sentence and a bridge; requirements move to the outlook |
| Detached comparator | "⟨Comparator⟩ remains the reference." | "Against all three routes, ⟨comparator⟩ remains the reference for ⟨metric⟩ because ⟨reason⟩." |
| Repeated yardstick | the same benchmark value restated in four sections | state it once; refer back ("the reference of Section ⟨n⟩") |

## 7 Venue differences

- Nature-family and Science reviews: shorter bodies, mostly unnumbered headings, Key points (Nature Reviews), strong framing, boxes for derivations.
- Society-journal reviews (ACS, RSC, Wiley, APS, Elsevier society titles): longer bodies, numbered headings, roadmaps, more benchmark maps and tables. Chemical Reviews adds a contents list.
- IEEE and engineering venues: reference-as-subject attribution, equations and normalised cross-work plots.
- Annual Reviews: strict length, a summary-points list and future-issues list at the end.
- Open-access mega-journals: formats vary; strong reviews there follow the same rules.

Aim for Nature-style framing with engineering-style comparison rigour, and follow the target journal's author guide.

## 8 Length, floats and apparatus

Take length, figure and table limits from the target journal's author guide and from two or three recent reviews in that journal; record them in the preset or the writing plan. Typical full reviews run 8,000–15,000 body words with about one figure per 800–1,000 words; mini-reviews and perspectives run shorter. Tables do not count toward body-word budgets unless the venue says so.

### Length variants

When the authors want several lengths (for example 25%, 50% and 100% of a full chapter):

- Keep one source per variant, with the same block schema and identifiers, so fixes can be synced block by block.
- Set a per-section word budget for each variant and a hard cap on the total; check both after every edit.
- Keep the full comparison tables in every variant; shorten prose, not evidence.
- The short variant keeps the frame, the topic sentences, the key works and the endings; it drops secondary works and repeated context.
- Sync every factual change to all variants and both languages in the same session; keep variant-specific extras.

## 9 Checklist

1. The text reads as the field's progress: no screening, counting or grading narrative, no defensive sentences, no per-paper fault-finding.
2. The introduction names earlier reviews, what this one adds, and the scope and inclusion rules.
3. The sorting criterion stands in one sentence before the taxonomy, and class labels keep one order throughout.
4. Every section title names the target subject, and non-target comparators take one or two sentences tied to the argument.
5. Each paragraph opens on a grouping or trade-off; key works are told as problem → idea → realisation → result.
6. Each subsection ends on a synthesis or design implication with a bridge; at most one numbered ending in the review.
7. Every headline number carries its level and status, and no sentence ranks values of different scopes.
8. Tables share one column set, carry a generated Year column and a defined missing-data code, and are cited once.
9. The outlook follows the body sections in order, with a measurable target for each, and the review ends on a synthesis.
10. Every length variant and both languages carry the same facts.

# Outlooks, conclusions and section endings

This guide covers how papers and sections end, from the challenges-and-outlook section of a review to the Discussion of a research article and the last sentence of any subsection. It applies to any field. Examples use placeholders (⟨layer⟩, ⟨metric⟩, ⟨value⟩, ⟨condition⟩, ⟨scale⟩).

## Rules

### Subsection endings in a review body

1. **End each subsection on a synthesis or a design implication, then a forward bridge.** The synthesis says what the works in the subsection add up to; the bridge names the question the next subsection takes up. Endings drawn from the strongest reviews in a field do this; endings that list gaps do not.
2. **Do not end a subsection on a list of gaps or a minimum-reporting list.** Reporting requirements belong in one place: the outlook, a box or a table note.
3. **Use at most one numbered "steps" ending per manuscript.** Every other ending is prose. Templated endings repeated across subsections read as machine-written.
4. **Let transitions carry the order of the argument.** Open a section by framing its order; end each subsection on the hand-off to the next ("as ⟨property⟩ fades, ⟨next topic⟩ takes over").

### Review outlooks

5. **Check whether the document already has a challenges chapter.** If a parent review or book carries its own Challenges and Outlook chapter, a chapter's last section becomes a short synthesis, and requirement lists move to that chapter.
6. **Organise the outlook along the axis of the body.** Use the layers of the body sections (for example, mechanism → component → system → application, or theory → method → validation) in the same order. The first sentence of each outlook paragraph names its layer.
7. **Write each challenge as status, requirement and next step, with a number on both sides.** Give the current value with its condition and reference, then the required value with its origin, then the experiment or analysis that would close the distance.
8. **Carry every threshold already stated in the body into the outlook.** Repeat each requirement with a pointer back to the section that derived it.
9. **Tie each target to what it buys and where it comes from.** Name the consequence (error, cost, yield, safety, time) and the source of the value, such as a roadmap, a model, a guideline or the Methods.
10. **Pair each challenge with a named remedy and its cost in the same paragraph.** The cost can be resources, time, complexity, lost precision or added risk; without it the remedy cannot be weighed.
11. **Name the single largest bottleneck and its layer.** A numbered list only sets an order of reading, so say in words which bottleneck blocks the others.
12. **With four or more challenges, add one target table or figure.** Use the columns layer, metric, best reported value (condition, reference), target (source), distance and decisive experiment, as in template T2.
13. **State open questions as the results that would settle them, and keep three to five.** Tie each to the measurement, dataset or model that would settle it. Phrase it forward ("would show", "the next key result would be"), not as an absence ("has not been shown").
14. **Ask for comparisons on a common accounting basis.** When the body contains values of different scopes, the outlook asks for one task measured with its components reported separately; it does not rank the values.
15. **End the review on a synthesis.** The last paragraph states what the field can now do, in concrete terms, and the decisive result that would move it to the next stage.

### Research-article Discussions and last sentences

16. **State one limitation in the Discussion with its size, cause and fix.** A limitation with its cause shows where the result stops holding.
17. **Label every forward number as measured, simulated or projected, with its condition and the place of its derivation.** A projection can be checked only when its derivation is given, in the Methods or a Supplementary Note.
18. **End on content: the decisive experiment, the remaining limit or the next measured target.** A slogan or a generic prospect names no next step that another group could check.

## Anti-patterns

General vocabulary (evaluative adjectives, stock importance phrases, attitude openers) is covered by [ai-flavor-lexicon.md](ai-flavor-lexicon.md) and checked by `scripts/prose_lint.py`. The entries below add what is specific to endings.

A1. **Replace stock closers with the next measurable step.** Search the last paragraph of every section for the lexicon's banned phrases and the phrases in the table below.
A2. **Replace evaluative adjectives with the compared number and its baseline in the same sentence.**
A3. **Give every priority claim a checkable scope, or delete it.** A claim of "first", "record" or "lowest known" needs the metric, the condition and the date of the search.
A4. **Compare like with like.** Keep the unit, accounting scope, workload and precision the same, report accuracy differences in percentage points, and never merge best values from different studies into one profile.
A5. **Mark every headline figure in an abstract or conclusion as measured, simulated or estimated.**
A6. **Cut sentences about the text itself.** Transitions, praise of the paper's own organisation and attitude openers carry no content.
A7. **Cut defensive closers.** "Much work remains to be done", "these results are still preliminary" and "further studies are needed" protect the author and inform no one. Name the next study instead.
A8. **Check every title word, abstract number and conclusion claim against a figure or table, then proofread in a separate pass.** The second pass covers agreement, articles and units, and re-checks any number taken from an AI-generated summary.

| Phrase | Replace with |
|---|---|
| open(s) a door, new horizon, new avenues, next frontier, vast potential | the decisive experiment |
| milestone | keep only when the sentence names the experiment ("The next milestone would be …") |
| superb, ideal, impactful | the number and its baseline |
| further studies are needed; remains to be explored | the named study and what it would show |
| first, record, lowest known | metric, condition and search date, or delete |

## Templates

Square brackets and ⟨ ⟩ mark slots for the author's sourced values.

### T1. Review "Challenges and outlook" skeleton

| Part | Content |
|---|---|
| Opening sentence | the verdict: which layer limits the field now |
| One paragraph per layer | status (value, condition, reference) → requirement (value, source) → remedy with its cost → decisive experiment |
| Priority paragraph | rank the bottlenecks; say which one blocks the others |
| Target table | template T2 |
| Closing paragraph | synthesis of what the field can do, then the decisive result for the top bottleneck |

Shape: *At the ⟨layer⟩ level, ⟨metric⟩ typically reaches ⟨value⟩ under ⟨condition⟩ [refs], whereas ⟨application⟩ needs ⟨target⟩ (⟨source⟩). ⟨Remedy⟩ narrows the distance at the cost of ⟨penalty⟩ [ref]. The decisive result would be ⟨experiment⟩ on ⟨scale⟩, reported with ⟨spread statistic⟩.*

### T2. Target-table row

| Layer | Metric | Best reported (condition, ref) | Target (source) | Distance | Decisive experiment |
|---|---|---|---|---|---|
| ⟨layer⟩ | ⟨metric⟩ | ⟨value⟩ (⟨condition⟩, [ref]) | ⟨target⟩ (⟨source⟩) | ⟨factor or difference⟩ | ⟨measurement on N units⟩ |

### T3. Research-article Discussion (four to six sentences)

Open with the result, its number and its condition, then give the closest competitor with its number and scope. Follow with the main limitation (size and cause), a projection with its condition and the location of its derivation, and the next bottleneck.

Shape: *The ⟨system⟩ reached ⟨value⟩ under ⟨condition⟩, including ⟨component⟩. The closest ⟨competitor⟩ reports ⟨value⟩ under ⟨different condition⟩ [ref]. ⟨Step⟩ was performed off-line, so the measured ⟨metric⟩ excludes it. Scaling to ⟨setting⟩ would improve ⟨metric⟩ by about ⟨factor⟩ (projected; Methods). The next bottleneck is ⟨named step⟩.*

### T4. Sentence slots

| Move | Slot |
|---|---|
| Challenge | "⟨Metric⟩ reaches ⟨value⟩ (⟨condition⟩, ⟨N⟩ samples [refs]), whereas ⟨application⟩ needs ⟨value⟩ (⟨source⟩); the distance comes from ⟨mechanism⟩." |
| Limitation | "⟨Result⟩ was limited to ⟨value⟩ by ⟨cause⟩; beyond ⟨threshold⟩, ⟨what failed⟩ (Supplementary Fig. ⟨n⟩)." |
| Synthesis ending | "Taken together, ⟨works⟩ show that ⟨capability⟩ under ⟨condition⟩; the same ⟨property⟩ sets the problem that Section ⟨n⟩ takes up." |
| Forward closing | "The next key result would be ⟨experiment⟩ at ⟨scale⟩, reported with ⟨metric and accounting scope⟩." |

## Venue differences

Nature-family reviews often end with a short outlook and a Key points or Box summary. Society-journal reviews more often carry a separate Challenges and Outlook section with a target table. Research-article Discussions in Nature-family journals are short and end on the limitation or the next measurement; IEEE and conference papers often end on a Conclusion that repeats the contribution, which should still state one limitation and one next step.

## Checklist

1. Each review subsection ends on a synthesis or design implication with a forward bridge, not on a gap list.
2. At most one numbered "steps" ending in the manuscript.
3. The outlook follows the axis of the body, and each challenge has status, requirement, remedy with cost and the decisive experiment.
4. Every threshold stated in the body reappears in the outlook with a pointer.
5. Open questions are phrased as the results that would settle them.
6. Comparisons across accounting scopes ask for a common basis instead of ranking.
7. Every forward number carries measured, simulated or projected and its derivation.
8. No stock closer, defensive closer or priority claim without scope.

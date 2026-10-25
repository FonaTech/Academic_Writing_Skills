# Quantitative reporting and fair comparison

This guide covers how to state a number with its conditions, name what a figure includes, keep measured, simulated and projected results apart, and compare methods, materials, treatments or systems fairly. It applies to any field: an efficiency, a cost, an effect size, a yield, an emission factor or an accuracy all need the same treatment. Examples use placeholders (⟨metric⟩, ⟨value⟩, ⟨condition⟩, ⟨scope⟩, ⟨baseline⟩, ⟨N⟩).

## Rules

### Evidence status and accounting

1. **Tag the evidence status of every number above the level of a single measurement.** Write "measured", "simulated from measured inputs", "projected", "estimated" or "extrapolated" in the number's own clause. Keep the tag when the number moves to the abstract, the conclusion or a comparison table. Abstract-only and reported-survey values (a review restating a primary result) carry their own labels in the evidence table.
2. **Name the accounting scope of every aggregate figure.** Say what is included (components, stages, overheads, populations, time window) and, in one clause, what is excluded. "Energy", "cost", "time", "emissions" and "efficiency" mean nothing without their boundary.
3. **Give the unit of account, and never compare across scopes as a ratio.** State it per event, per unit, per sample, per task, per participant or per year. Two values with different scopes are reported side by side with each scope named; they are never written as "N times lower" or "N orders of magnitude below". Ask instead for one task measured with its components reported separately.

### Conditions, baselines and comparison

4. **Tie every headline figure to its conditions.** Give the precision, dose, sample, temperature, dataset, setting or protocol that produced it, and the scale at which it was measured.
5. **Report every accuracy, effect or improvement against a baseline under the same task and data.** Name the baseline and give the difference in the natural unit (percentage points for accuracies, absolute and relative change for effects).
6. **Name the baseline of every ratio, and check the ratio against it.** Give its source and conditions, and whether it was measured or quoted from a vendor, a guideline or another review.
7. **Compare at matched conditions, or normalise and say how.** State the normalisation in the caption or table note. When numbers cannot be made comparable, leave them raw and say why.
8. **Separate peak from sustained and component from system figures.** State the operating fraction or the duty cycle when the figure was taken.
9. **Preserve the source's quantifiers.** "Up to", "about", "at least", "calculated", "estimated" and "total" are part of the number. If the source says "up to", keep it and add the scope. Never strengthen a number while shortening a sentence.
10. **Check every magnitude statement arithmetically.** Compute the ratio from the two sourced values; a factor of 10⁸ is eight orders of magnitude, not six.

### Statistics and setup

11. **Report distributions beside best cases.** Give the mean and standard deviation or the median with n, define the statistic, and state yield or success as successes over attempts. Put the best case next to the distribution.
12. **Never pool best-case values from different studies or samples without saying so.** This holds for one sentence and for one table row.
13. **Mark durability and lifetime values as measured or extrapolated, with the test duration and conditions.** Explain the extrapolation convention before the first extrapolated value.
14. **Disclose instrument and setup limits next to the number they affect.**
15. **Define each metric where it is first used, with its formula and extraction condition.** Keep the source's symbol and define it; do not rename it.
16. **Show the arithmetic of every worked example and state its assumptions.** Give each input value so that others can recompute the result.

### Claims, tables and consistency

17. **Replace priority and superlative words with the comparison itself.**
18. **Keep one column set and one unit per column in review comparison tables.** Put each test condition beside the metric it conditions. Mark evidence status and missing values ("n.s." for not stated, "n.r." for not reported), and define the codes in the note.
19. **Move accounting that would interrupt a review's argument into a box or table note.** Template F gives the slots.
20. **Make at least one outlook target numeric, tied to a consequence and set against the current value.**
21. **Reconcile every number that appears more than once before submission.** Check the abstract, introduction, results, conclusion, captions and tables against each other, and across every length variant and language version.
22. **Do not claim a property you did not measure.** When a paper reports no cost, energy or durability figure, drop the adjective or say what would measure it.

## Templates

Slots are placeholders for sourced values.

**A. Conditioned-number sentence.** Fill the slots in this order.

| 1 Evidence verb | 2 Metric, unit of account | 3 Value ± spread (n) | 4 Conditions | 5 Scope | 6 Baseline |
|---|---|---|---|---|---|
| measured, simulated, projected, estimated | ⟨metric⟩ per ⟨unit⟩ | median or mean with n | protocol, dose, setting, temperature, dataset | included and excluded parts | named, at matched conditions |

Shape: *Measured under ⟨condition⟩, the ⟨system⟩ reaches ⟨value⟩ ⟨unit⟩ per ⟨unit of account⟩ (median of ⟨N⟩). The figure includes ⟨components⟩ but not ⟨excluded part⟩, and it is ⟨factor⟩ times the best ⟨baseline⟩ under the same ⟨condition⟩ in Table ⟨n⟩.*

**B. Research-article abstract.** The moves are the need (one sentence), what exists and the missing combination (one or two), and "Here we" with the object and a scale number (one). Then come two to four headline numbers, each with its evidence tag, condition and baseline, and a closing sentence on scope or consequence. Typical length is 150–200 words; follow the journal limit.

**C. Review abstract with one quantified finding.** The moves are the problem, the organising axis, one quantified cross-study finding with its scope, one judgment and one numeric target.

Shape: *Across ⟨N⟩ ⟨studies⟩ reported since ⟨year⟩, ⟨metric⟩ rose about ⟨factor⟩, and ⟨n⟩ of them report ⟨full-scope metric⟩. Component-level figures and system-level figures therefore belong in separate comparisons. We set ⟨target⟩ under ⟨condition⟩, ⟨overheads⟩ included, as the next milestone.*

**D. Benchmark subsection in a review.** (1) Define the metric and its unit of account. (2) State the inclusion criterion and the normalisation. (3) Give the trend or ranking with numbers and n. (4) State what limits the comparison, such as the task, peak against sustained figures or best values from different studies. (5) Say what the comparison means for design or practice.

**E. Comparison table and caption.**

| Ref. | Year | Approach, setting | Scale or sample | Conditions | Metric, unit of account | Evidence status | Scope |
|---|---|---|---|---|---|---|---|

The Year column is generated from reference metadata by the builder, never typed by hand (sci-manuscript-build, content-markup.md). Footnote codes: a measured, b simulated from measured inputs, c projected, d extrapolated from ⟨duration⟩ under ⟨condition⟩, n.s. not stated. Caption: "Table n | ⟨What is compared⟩ for ⟨inclusion criterion⟩. Values are ⟨normalisation⟩; ⟨metric⟩ includes ⟨components⟩ unless marked. Letters mark evidence status."

**F. Accounting box.** Slots: the budget and its unit; the system and duration measured; what is counted; what is excluded and its likely size; per-unit values on both sides of the comparison; why a like-for-like task comparison is hard; and a bounded conclusion that asks for a common basis.

## Anti-patterns and fixes

| Pattern | Before (constructed) | After |
|---|---|---|
| Scope-mismatched ratio | "⟨Approach A⟩ uses three orders of magnitude less ⟨resource⟩ than ⟨B⟩." | "⟨A⟩ uses ⟨value⟩ per ⟨component-level event⟩, and ⟨B⟩ uses ⟨value⟩ per ⟨system-level task⟩ [refs]. A same-task measurement split into ⟨components⟩ would allow a direct comparison." |
| Dropped quantifier | Source: "up to 40%". Draft: "40%". | "up to 40% ⟨under condition⟩" |
| Simulated as measured | "The system achieved ⟨value⟩ accuracy." | "A simulation using measured ⟨inputs⟩ reached ⟨value⟩ [ref]." |
| Champion only | "The best sample reached ⟨value⟩." | "Across ⟨N⟩ samples, ⟨metric⟩ was ⟨median⟩ (IQR ⟨range⟩); the best reached ⟨value⟩." |
| Unnamed baseline | "a fivefold improvement" | "five times the ⟨named baseline⟩ under ⟨condition⟩ [ref]" |
| Renamed symbol | Source defines R_acc; draft writes "precision ε". | "the relative deviation from target, R_acc, of ⟨value⟩ [ref]" |
| Added motive | Source: "⟨A⟩ was integrated with ⟨B⟩." Draft: "⟨A⟩ was integrated with ⟨B⟩ to eliminate ⟨C⟩." | Keep the source's statement; add a purpose only if the source gives it. |

## Venue differences

Nature-family journals require reporting summaries and statistics (n, test, exact p or interval) for every quantitative claim. Engineering venues expect benchmark tables with normalised columns. Clinical and life-science journals follow reporting guidelines (for example CONSORT, STROBE, PRISMA, ARRIVE, MIAME); apply the one the venue names. In any venue, state the evidence status of each headline number.

## Checklist

1. Every aggregate number has its evidence status, conditions, unit of account and scope.
2. No ratio or "orders of magnitude" claim joins values of different scopes, and every magnitude is checked arithmetically.
3. Every accuracy or effect has a named baseline under the same task.
4. Distributions accompany best cases; pooled best values are flagged.
5. Source quantifiers (up to, about, estimated, total) and source symbols survive editing.
6. Tables have one unit per column, a generated Year column and defined missing-value codes.
7. Repeated numbers match across sections, variants and languages.

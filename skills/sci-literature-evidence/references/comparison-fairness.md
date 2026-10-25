# Fair comparison across papers

Most misleading statements in reviews come from comparing numbers that measure different things. Before two values appear in one sentence, one table row set or one plot, check the items below. They apply in any field; the examples use placeholders.

## 1 Accounting scope

Every aggregate value (energy, cost, time, emissions, yield, efficiency, effect size) belongs to a level and includes some parts and not others. Write a scope ladder for the project before extracting values, for example:

| Scope level | Includes | Example form |
|---|---|---|
| single event or unit | one operation, one reaction, one sample, one participant | ⟨value⟩ per event under ⟨condition⟩ |
| component | the unit plus its immediate support | ⟨value⟩ per ⟨component task⟩, ⟨support⟩ excluded |
| module or subsystem | components plus their interfaces and control | ⟨value⟩ at ⟨precision or setting⟩, ⟨overheads⟩ included |
| system | the module plus everything needed to run it | ⟨value⟩ per ⟨full task⟩, including ⟨inputs, transfer, host⟩ |
| deployment or population | the system in its real setting over time | ⟨value⟩ per year or per person, with ⟨usage profile⟩ |

Never compare across rows of this ladder without saying so, and never state a ratio or "N orders of magnitude" between values of different scopes. Report them side by side with each scope named, and ask for one task measured with its components reported separately. A per-event value is not an efficiency.

## 2 Unit, operation definition and precision

- State the precision, resolution or setting next to every efficiency or throughput value; such metrics often change steeply with it.
- Check how an operation, unit or event is counted; conventions differ between communities.
- Results at a coarse setting are not comparable with results at a fine setting without a stated normalisation.

## 3 Scale, node and projection

- Values projected to another scale, generation, site or population are labelled "projected" and kept apart from measured values at the original scale.
- Normalise with a stated rule only when all compared works allow it; otherwise present them unnormalised with the relevant condition in the table.

## 4 Measured, simulated, projected

- A model run on measured inputs is "simulated", even when the inputs are real.
- A demonstration on a subset of a dataset or cohort is not a full-dataset result; state the subset size.
- Say when best values come from different studies ("best values in this table come from different studies").

## 5 Task, dataset and protocol

Same dataset, same split, same preprocessing, same protocol, same model size, or say what differs. A two-class task and a ten-class task are not comparable; a pilot and a full trial are not comparable.

## 6 Conditions for unit-level metrics

- Durability or lifetime: conditions, test duration, and whether measured or extrapolated.
- Repetition counts: what was repeated (full cycles, partial cycles, read-outs) and under which load.
- Variation: within-unit vs between-unit vs between-batch; state n and the statistic.
- Per-event cost: the conditions and whether inputs (energy, reagents, preprocessing) are included.
- Ratios and windows: how they are defined and at what operating point.

## 7 Shares of a total

Quote shares (of cost, energy, area, time, variance) with their source and scope, and do not average shares from different systems. Show them as a table with one row per system and scope, or as dots and ranges in a figure, never as one pooled number.

## 8 Quantifiers and symbols

- Keep the source's quantifier: "up to", "about", "at least", "calculated", "estimated", "total".
- Keep the source's symbol for a quantity, define it, and do not rename it.
- Recompute every ratio and magnitude from the two sourced values before writing it.

## 9 Presentation

- Tables: a scope column and an evidence column whenever rows differ in either; a Year column generated from the references.
- Plots: marker fill encodes the evidence level; the caption states the normalisation and the scope.
- Text: comparisons within a sentence use values of the same scope; otherwise state each scope separately.

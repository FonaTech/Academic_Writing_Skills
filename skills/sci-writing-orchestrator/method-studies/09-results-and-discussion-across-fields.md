# Case 09: Results and Discussion paragraphs across fields

A method study for the two sections of a research article where depth is won or lost. The chain of reasoning is the same in every field; what counts as the control, the comparator and the condition differs. Placeholders stand for sourced content.

## The chain
**Results paragraph:** what we measured and why → what we saw, with the number and its condition → the control or comparison that rules out the obvious alternative → what this establishes → the measurement the next paragraph needs.

**Discussion paragraph:** the main finding stated as a claim → the mechanism and its evidence → the comparison with prior work at the same scope → the strongest counter-case or regime where the claim fails → the limit and the experiment that would remove it.

Before drafting, write the obvious alternative explanation for each result. If no panel or analysis rules it out, the paragraph is not ready, and no wording will fix it.

## What the slots mean in each field
| Field | Same-scope comparator | Conditions that change the answer | Typical obvious alternative | Evidence labels to keep apart |
|---|---|---|---|---|
| devices, materials, physical chemistry | the best prior device measured the same way (temperature, area, cycling protocol) | temperature, bias, sample size, cycle number, environment | contact or measurement artefact; sample-to-sample spread | measured, simulated, projected from models |
| synthesis and catalysis | the benchmark catalyst under the same loading, conversion and time | loading, temperature, pressure, conversion level | mass-transfer limits; a homogeneous leached species | isolated yield, NMR yield, calculated |
| cell and molecular biology | the matched control line or vehicle at the same passage and dose | dose, time point, cell line, passage, n per group | off-target effect; batch effect | in vitro, in vivo, in silico |
| clinical and epidemiology | the control arm with the same endpoint, follow-up and population | eligibility, follow-up length, adjustment set | confounding, selection bias, regression to the mean | trial, observational, modelled |
| ecology and earth science | the same site, season and sampling method in another year or region | season, scale, sampling effort, detection probability | sampling artefact; spatial autocorrelation | observed, reanalysis, modelled projection |
| computation and machine learning | the strongest baseline on the same dataset, split and compute budget | dataset version, split, seed, tuning budget | data leakage; tuning advantage | measured on held-out data, reported by others, estimated |
| quantitative social science | the same outcome in a comparison group with the same measure | sampling frame, period, instrument wording | selection, reverse causation | experimental, quasi-experimental, survey, simulated |

A ratio across scopes ("ten times better") is not stated. Both scopes are given, or the comparison waits for a common basis.

## Shapes
**Results, constructed:** "To test whether ⟨effect⟩ comes from ⟨cause⟩, we repeated the measurement with ⟨control⟩. The ⟨metric⟩ stayed at ⟨v⟩ (⟨condition⟩; ⟨n⟩ ⟨units⟩; Fig. 3b), against ⟨v′⟩ without ⟨control⟩ (Fig. 3a). ⟨Effect⟩ therefore requires ⟨cause⟩. The size of the effect at ⟨larger scale⟩ is the subject of Fig. 4."

The single "therefore" is the paragraph's one inference. The motive appears as the purpose of the test.

**Discussion, constructed:** "⟨Finding⟩ holds across ⟨range⟩ and follows from ⟨mechanism⟩, which the ⟨control⟩ experiment isolates. ⟨Prior study⟩ reported ⟨v″⟩ under ⟨their condition⟩ [ref]. Measured at that condition, our ⟨system⟩ gives ⟨v‴⟩ (Supplementary Fig. S5). The mechanism predicts no gain above ⟨threshold⟩, and ⟨other study⟩ saw none there [ref]. A test at ⟨untested condition⟩ would show whether ⟨limit⟩ is intrinsic."

## Failure modes and repairs
| Failure | Repair |
|---|---|
| Results restate the figure ("Fig. 2 shows …") | state what the panel establishes and cite it at the end of the clause |
| a Discussion that repeats the Results in the same order | restate the main finding once, then spend the paragraph on mechanism and comparison |
| every paragraph ends with "these results pave the way" | end on the limit and the test that would remove it |
| a limitations paragraph of defensive sentences | each limit is a fact with its scope and the experiment that addresses it |
| mixed evidence labels in one sentence | one label per number; simulated or modelled results say so in the clause |
| comparison with a weaker or older baseline only | name the strongest current comparator, even when the result is closer |

## Checks
- Every Results paragraph cites the panel that proves its claim; every panel is cited.
- Every comparison states both scopes.
- The Discussion names at least one counter-case or regime of failure, with its source.
- The abstract, the last Results paragraph and the conclusion carry the same number with the same qualifier.

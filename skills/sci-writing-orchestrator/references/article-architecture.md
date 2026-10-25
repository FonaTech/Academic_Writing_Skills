# Architecture of a strong research article or letter

This guide covers the structure of research articles, letters and conference papers in any experimental, computational or observational field. Examples use placeholders (⟨object⟩, ⟨mechanism⟩, ⟨metric⟩, ⟨value⟩, ⟨condition⟩). Prose-level rules are in the sci-prose-style skill.

## 1 The evidence ladder

Strong articles climb levels in one direction, and each Results subsection is one rung. The rungs differ by field; the logic does not.

| Field type | Typical ladder |
|---|---|
| Materials, devices, engineering | material or process → single unit with mechanism and control → statistics over many units → functional primitive → small system → scaled task or projection |
| Life sciences | molecular mechanism → cellular phenotype → tissue or organism → population or clinical relevance |
| Computational and theoretical work | model and assumptions → analytical or numerical result → validation against data or benchmarks → ablation or sensitivity → application |
| Observational, clinical and social sciences | data and design → main estimate → robustness and sensitivity → heterogeneity or mechanism → external validity |

The mechanism rung convinces only with a control that could have failed: a dependence that rules out an alternative, a with/without comparison, a knockout, a placebo, a falsification test or an out-of-sample check. A schematic alone is not a mechanism. Mark a projected or simulated rung as such.

## 2 Rules

### Introduction

1. **Give the need and the incumbents with numbers, then the evidenced gap.** Name the gap specifically ("not measured at ⟨scale⟩ for ⟨class⟩") within three short paragraphs. Keep the concept or claim as the grammatical subject; "⟨Author⟩ et al." is for landmark or disputed results.
2. **End the introduction with a "Here, we …" paragraph that previews Results.** Match each named deficiency to a quantified property and a Results subsection, and preview every headline number.

### Results

3. **Order Results as an evidence ladder in which each rung uses the one below.** Give each rung its own subsection. Letters and short papers keep the ladder with fewer headings.
4. **Settle the mechanism inside Results with a discriminating control.** List the candidate mechanisms, then test each under a condition that could rule it out.
5. **Use three to five Results subsections with short noun-phrase headings** of three to six words that name the object and its role. Keep evaluative adjectives out and mark simulated work ("Simulated ⟨large-scale task⟩").
6. **Give each subsection one main figure, cited in numerical order.** Walk the panels in reading order and keep each paragraph on one figure.
7. **Open each subsection with its purpose or requirement.** Then give the method, conditions, result with statistic and panel, any deviation with its cause, and a hand-off to the next rung.
8. **Tag every system- or population-level number as measured, simulated, projected or estimated.** Give its baseline: the ideal case, the standard method on the same task, or the configuration without the new element. The tag stays with the number in the abstract and the conclusion.
9. **State each limitation in the sentence after the number it qualifies, with its cause.** Keep only whole-claim limits for the Discussion.

### Figures, tables and SI

10. **Let the main figures carry the argument.** Move statistics, controls, repeats, derivations and extended benchmark tables to the Supplementary Information (SI) and cite each item where it is used. Never leave a headline number or its accounting scope only in the SI.
11. **Budget four to six main figures and at most one or two main-text tables,** or the venue's limit. The ladder sets the count.
12. **Build each caption from a title, panel clauses, conditions, statistics and abbreviations** (sci-figure-design, captions-and-tables reference).

### Discussion

13. **Build the Discussion from five moves, and add no new result.** Recap the ladder in Results order with tagged numbers. Then give a matched comparison (full table in the SI), the whole-claim limits, one projection with its condition and derivation, and one named next step.
14. **End on a specific sentence** that names the next step, a condition or a number.

### Methods and availability

15. **Place Methods where the venue expects it and organise it by process step.** Include the metric definitions, accounting scope, statistics, data split and preregistration or ethics approvals that Results relies on.
16. **Say where the data behind each figure live, preferably in a repository with a DOI.** Add a code statement whenever code produced a reported number.

### Title, abstract and consistency

17. **Scope the title and abstract to what the paper tests.** Every title word needs evidence in the paper ("flexible" needs bending data, "robust" needs a stress test).
18. **Keep every number identical across abstract, introduction, Results, captions and conclusion,** with its qualifier, and compute each difference once.

## 3 Letters and conference papers

A letter gives the gap and the result in the first paragraph and carries three to four figures, each with one claim. Methods go online, and the ladder stays with fewer headings.

A conference paper rests on the result and the comparison table. The table must normalise the conditions that drive the metric and state what each figure includes. Many engineering venues name sections after the analysis (design space, implementation, evaluation) and have no separate Methods. Follow the call for papers for page limits and anonymisation.

## 4 Templates

### 4.1 Article skeleton (Nature-family order)

```
Title        object or function noun phrase, "for" + target
Abstract     150-200 words: need, gap, "Here we" + object, 2-4 tagged numbers, scoped implication
Introduction unheaded, 4-6 paragraphs: need with a number, incumbents and failure modes,
             gap as a list of limits, contribution paragraph that previews Results and cites Fig. 1
Results      3-5 headed subsections in ladder order, one main figure each
Discussion   the five moves of rule 13
Methods      then Data availability and Code availability
```

Shape: *Here we report ⟨object⟩ built on ⟨enabling element⟩. We measure ⟨variation⟩ across ⟨N⟩ ⟨units⟩ (Fig. 2) and identify ⟨mechanism⟩ (Fig. 3). We then ⟨perform task⟩ (Fig. 4) and, in simulation, extend it to ⟨scale⟩ (Fig. 5).* Matching headings: "⟨Statistic⟩ across ⟨units⟩", "⟨Mechanism⟩ behind ⟨property⟩", "⟨Task⟩ with ⟨object⟩", "Simulated ⟨scale⟩ with measured ⟨inputs⟩".

### 4.2 Results subsection

```
[Heading: object + role or problem] -> [Purpose: what this rung must show] -> [Method and conditions, SI pointer]
-> [Result: number, statistic, n, panel] -> [Deviation and cause] -> [Hand-off]
```

### 4.3 Discussion

```
[Recap in Results order, tagged numbers] -> [Matched comparison] -> [Whole-claim limits]
-> [Projection, condition, where derived] -> [Named next step as last sentence]
```

### 4.4 Caption, Methods and availability

```
Fig. n | [Object or finding]. a, [what is plotted] under [condition]. b, ... [Shared conditions].
[Error bars: s.d. over n]. [Abbreviations].
Methods: materials or participants; preparation or design; measurement or data collection (instrument,
settings, averaging); analysis or simulation (dataset, split, model, baseline); accounting scope
(what is included); statistics; ethics or preregistration where applicable.
Availability: "Source data for Figs. 2-5 are provided with this paper; raw files are at ⟨repository⟩ (DOI).
Code for ⟨analysis⟩ is at ⟨host⟩ (link), archived at ⟨repository⟩ (DOI)."
```

## 5 Anti-patterns and fixes

| Pattern | Before (constructed) | After |
|---|---|---|
| Novelty as the gap | "⟨Object⟩ is studied here for the first time." | "Whether ⟨intervention⟩ changes ⟨metric⟩ at ⟨scale⟩ is untested; we test it across ⟨N⟩ ⟨units⟩." |
| Mechanism by schematic | "The band diagram explains the effect." | "The effect scales with ⟨variable⟩ (Fig. 3b), which rules out ⟨alternative⟩." |
| Simulation labelled as result | heading "Large-scale ⟨task⟩" | heading "Simulated large-scale ⟨task⟩" |
| Headline only in SI | accounting scope in Supplementary Note 4 only | scope stated in the main-text sentence; derivation in the SI |
| Stock closer | "This work paves the way for future ⟨applications⟩." | "The next step is ⟨experiment⟩ at ⟨scale⟩." |

## 6 Venue differences

- Nature-family and Science: unheaded introduction, "Here we" pivot, Results with headings, short Discussion, Methods at the end, reporting summary.
- Cell Press: Highlights, eTOC blurb, graphical abstract, STAR Methods with a key resources table.
- Society journals (ACS, RSC, Wiley, APS, Elsevier): Introduction, Results and Discussion often combined, Experimental section, SI.
- IEEE and conference venues: numbered sections, comparison table, no separate Methods, strict page limits.
- Clinical and life-science journals: structured abstracts and the reporting guideline the journal names (for example CONSORT, STROBE, ARRIVE).

## 7 Checks before submission

- Every abstract and conclusion number matches the body, with the same qualifier and evidence tag.
- Every title word is tested in the paper.
- Every gap named in the introduction is revisited in Results or Discussion.
- Simulated, projected and measured results are labelled where they appear, including headings and captions.
- Each Results subsection opens with its purpose and rests on one main figure, and figures are first cited in order.
- The mechanism rung has a control that could have failed.
- Each limitation sits next to the number it qualifies, and the last sentence names a next step, a condition or a number.
- Every SI item is cited where it is used, and the availability statements say where the data and code are.

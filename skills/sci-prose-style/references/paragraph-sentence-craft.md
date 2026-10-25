# Paragraph and sentence craft

This guide covers how a paragraph opens, where its evidence sits, how it closes and how long its sentences run. It applies to any field and adds detail to the house rules in style-rules.md without repeating them. Examples are constructed with placeholders (⟨method⟩, ⟨metric⟩, ⟨condition⟩, ⟨value⟩, ⟨N⟩); they show form, not literature values.

## Rules

The house paragraph runs from a topic sentence through quantitative evidence with its conditions to a one-sentence implication or next step (style-rules.md, sections 2.1 and 2.2). Rules 1–6 follow that order.

### Paragraph order

1. **Open on the idea, not the author.** The subject of the first sentence is a concept: a requirement, a mechanism, a class of methods, a trade-off or a claim. Names ("⟨Author⟩ et al.") and years ("In ⟨year⟩,") move to sentence two or later. A named chronological chain is acceptable after a concept sentence that frames it.

2. **Order the evidence inside the sentence.** Write the claim, value, statistic, population and condition, then the pointer in parentheses at the end. A figure-first opener ("As shown in Fig. 2", "Figure 2 shows") delays the claim.

3. **Give every Results paragraph a limiting move or a control.** A limiting move names a deviation's cause, a result's scope or a residual limit. A control is a same-setup baseline or variant.

4. **Explain each shortfall in one causal sentence.** Make the shortfall the subject and follow it with a cause verb ("is due to", "mainly results from", "is dominated by"), then the number or the pointer.

5. **Close on a synthesis, a design implication or a forward bridge.** The last sentence of a review subsection states what the evidence adds up to, what it implies for design or practice, or which question the next section takes up. A closer such as "highlights the potential" leaves nothing to test. Do not end on a list of gaps or a minimum-reporting list. Use at most one numbered "steps" ending per manuscript; every other ending is prose.

6. **Put given information before new.** Start a sentence with information already on the page, such as the method just named, "This" or the quantity just shown. End it on the new cause, number or comparison, and cite at the end of the clause the citation supports.

### Claims and calibration

7. **Calibrate; do not defend.** Remove boosters rather than adding hedges. A hedge belongs only on a mechanism, an interpretation or an extrapolation. A strong hedge names the competing explanation or the exact scope instead of adding "may". Defensive phrases (so far, to date, still, not yet, remains missing) are not hedges; delete them and state the scope (style-rules.md, section 3.2).

8. **Trade adjectives for numbers.** Give the value and its baseline, define the adjective by a criterion, or delete it.

9. **Let the verb carry the evidence status.** Use the verbs in the table below and keep "prove" for mathematics. The "simulated" or "estimated" label stays attached to the number in the abstract and the conclusions (style-rules.md, section 3.1).

10. **Retire default verbs.** Keep "exhibit" below about 0.5 per 1,000 words and delete "successfully".

11. **Prefer contrast to addition at sentence starts.** Use at most 3 additive openers per 100 sentences, and let each contrastive opener introduce a named cost or exception.

12. **Pair each advantage with its penalty.** Put the penalty in the same sentence or the next one, with a marker from the table below.

#### Word lists for rules 7, 9, 11 and 12

| List | Words and phrases |
|---|---|
| Hedges (mechanisms and extrapolations only) | may, might, could, likely, suggest, appear |
| Defensive phrases (delete) | so far, to date, still, only, merely, not yet, has not been, remains missing, remains unclear, cannot yet |
| Boosters | excellent, remarkable, outstanding, superior, tremendous, and the banned intensifiers in ai-flavor-lexicon.md |
| Evidence verbs | measured "shows"; simulated "simulations indicate"; projected "we project"; inferred "suggests" or "can be attributed to" |
| Additive openers | Moreover, In addition, Furthermore |
| Contrastive openers | However, Although, In contrast, By contrast, Yet |
| Trade-off markers | "at the expense of", "The trade-off is between", "at the cost of", "trades ⟨X⟩ against ⟨Y⟩" |

### Scope, limits and definitions

13. **Give scope and status a short sentence beside the result it limits.** Keep it to about 15 words, and join it to the result with a shared subject or a connective so it does not read as a fragment.

14. **Write a limitation as a fact with a magnitude and a cause.** Follow template T3 and set the shortfall against a requirement; "still in its infancy" is never the limitation.

15. **State an open problem as the next result that would settle it.** Name the experiment, analysis or dataset and what it would show: "Measuring ⟨metric⟩ on ⟨scale⟩ under ⟨condition⟩ would show whether ⟨claim⟩ holds." Do not phrase it as a negation ("has not been reported").

16. **Define each term where it first appears, in the same sentence and operationally.** Give the formula, the condition or the direction of goodness. For a term that readers misread, write "⟨term⟩ does not mean A; it means B." Keep new abbreviations to about 3 per 1,000 words in a review, and expand them in every caption.

17. **Use "we" for your own analysis.** A review benefits from at least one normalisation or calculation of its own, and one attribution convention for the whole manuscript.

### Length, flow and the last pass

18. **Hold the length profile and keep the conditions.** The house median is 16–20 words, with a ceiling of about 30. Extra length is acceptable when it carries conditions or comparisons; above about 30 words, move the condition into the next sentence and keep it. Also split two main clauses joined without punctuation, stacked purpose clauses and near-synonym repeats.

19. **Link, do not stack.** A run of short declaratives with no connective reads as an outline. Join sentences by a shared subject, a pronoun that points back, or a light connective. Merge orphan paragraphs of one or two sentences into their neighbours.

20. **Cut meta-commentary and emotive openers.** Delete openers such as "Obviously" and "Interestingly". Keep a plain "note that" for a caveat only.

21. **Check qualifiers, units and definitions in a separate pass.** A wrong qualifier survives a language edit because the sentence still reads well. Check every *about, up to, at least, estimated, total* and every unit against the source in the evidence pass of the revision protocol in SKILL.md.

## Templates

**T1. Review comparison paragraph, four to six sentences.** S1 names the requirement or the trade-off. S2 gives the criterion with its threshold and source. S3 and S4 set two or three works against the criterion, each with a value, a condition and a citation at the end of the clause. S5 states the trade-off, and S6 gives the design implication or the bridge to the next paragraph.

Shape: *⟨Application⟩ needs ⟨metric⟩ of at least ⟨threshold⟩ [ref]. ⟨Approach A⟩ reaches ⟨value range⟩ only with ⟨extra step⟩ [ref], whereas ⟨approach B⟩ reaches ⟨value⟩ under ⟨condition⟩ [ref]. The price of B is ⟨property⟩, because ⟨cause⟩ [ref]. For ⟨use case⟩, A therefore suits ⟨setting⟩, and B suits ⟨other setting⟩.*

**T2. Results paragraph, four or five sentences.** S1 states the purpose or claim with its pointer. S2 gives the condition, value, statistic and population, and S3 sets the result against a baseline or control. S4 names the cause of any deviation, and S5 states the scope.

**T3. Limitation sentence.** [Result, value] trails [requirement or baseline, value] by [gap], mainly because of [cause]; [remedy] would close most of the gap at the cost of [penalty].

**T4. Next-step sentence.** [Experiment or analysis] under [condition] would show whether [claim] holds at [scale], which [consequence for the field].

**T5. Definition sentence.** [Term] ([abbreviation]) is [operational definition with formula or condition]; [direction of goodness].

**T6. Named-work sentence pair.** In [year], [Author A], [Author B] and colleagues [did what] under [condition], reaching [value] [ref]. The same team then [next step], which [what it changed] [ref].

## Anti-patterns and fixes

| Pattern | Before (constructed) | After |
|---|---|---|
| Adjective judges a statistic | "Across ⟨N⟩ samples the variation was about ⟨value⟩, and the consistency was superb." | "Across ⟨N⟩ samples, the variation was about ⟨value⟩." |
| Simulated result hidden by the verb | "⟨Author⟩ et al. demonstrated a high accuracy of ⟨value⟩ [ref]." | "A simulation using the measured ⟨inputs⟩ gave ⟨value⟩ accuracy [ref]." |
| Run-on | "Most studies measured few samples and modelled the rest in software in such studies the link is weak." | "Most studies measured a few samples and modelled the rest [refs]. In such studies, the link between ⟨part A⟩ and ⟨part B⟩ is loose." |
| Untestable closer | "This capability paves the way for future applications." | "Operating ⟨N⟩ such units together under ⟨condition⟩ would show whether ⟨property⟩ survives at scale." |
| Defensive gap | "To date, no study has yet reported ⟨metric⟩." | "Reporting ⟨metric⟩ with ⟨condition⟩ would allow ⟨approaches⟩ to be compared directly." |
| Staccato chain | "⟨A⟩ is fast. ⟨B⟩ is stable. ⟨C⟩ is cheap. ⟨D⟩ is the reference." | "⟨A⟩ is fast but ⟨cost⟩, whereas ⟨B⟩ trades speed for stability. Against both, ⟨D⟩ remains the reference for ⟨metric⟩." |

## Venue differences

Venue predicts format more than sentence-level restraint. Nature- and Science-family research papers use "we" freely for the authors' own work and expect a limiting move or a control in Results. Society-journal reviews (for example ACS, RSC, Wiley, IEEE, APS, Elsevier society titles) tend to carry denser comparison tables and fewer boosters. Some engineering venues make the reference number the subject ("[7] proposes"); others forbid it. Follow the target journal's author guide and two recent reviews from that journal.

## Checklist

1. The first sentences of a section's paragraphs, read alone, state its argument, and none opens on an author, a year or a figure.
2. Every Results paragraph carries a limiting move or a control, and every review subsection ends on a synthesis, a design implication or a forward bridge.
3. Evidence sentences run claim, value, statistic, population and condition, with the pointer last and in parentheses.
4. No defensive phrases; hedges sit only on mechanisms and extrapolations.
5. Each claim verb matches its evidence status, and "simulated" survives into the abstract and the conclusions.
6. Each advantage has its penalty within one sentence, and each limitation has a magnitude and a cause.
7. Each new term is defined where it first appears, and each caption expands its abbreviations again.
8. `scripts/prose_lint.py` reports a median of 16–20 words, no sentence over about 30 words, no staccato run and no banned phrase.
9. A separate pass checks every qualifier and unit against its source.

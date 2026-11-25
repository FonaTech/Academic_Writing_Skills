# Introductions for reviews and research articles

This guide covers the introduction of a review or a research article, from the opening sentence to the roadmap or results preview. It applies to any field. Abstracts are in [titles-abstracts.md](titles-abstracts.md), sentence-level rules in [style-rules.md](style-rules.md), and the review body in the sci-writing-orchestrator review-architecture reference. Examples use placeholders (⟨field⟩, ⟨method⟩, ⟨metric⟩, ⟨value⟩, ⟨scale⟩).

## Rules

### Research articles

1. **State the gap by the end of paragraph 2.** Speed alone does not make a good introduction; the wording of the gap matters more (rule 2).
2. **Write the gap as a missing capability at a named scale or setting, or as named alternatives each with its limit.** Delete scarcity-only wording ("few researchers", "not fully explored", "for the first time"). If "seldom studied" is true, follow it at once with the reason and a narrower limit.
3. **Credit the cited work and state its limit in the same sentence.** Model form: "These studies established ⟨result⟩, but ⟨limit at named scale⟩."
4. **Build the gap by elimination, with one sentence, one named shortcoming and one citation per alternative.** Close the paragraph on what the field needs at a named scale. Answer the shortcomings in the same order in the contribution paragraph. Never end the list on "and other drawbacks".
5. **Pivot with "Here, we" or "In this Article, we", then the object, the enabling element and one number, in 20–35 words.** Put the pivot within about 150 words of the gap in an article and about 300 in a review.
6. **Close an article introduction with a results preview in Results order, and skip the roadmap.** Tag each number as measured, simulated or estimated and give its level or scope. Claim nothing in the introduction that the Results do not show.
7. **Replace priority claims ("first", "to the best of our knowledge") with a checkable comparison.** Enumerate contributions only when each item sits at a different level of abstraction.

### Reviews

8. **Reach the technical gap within about 500 words of the Introduction heading, and the scope sentence within about 750.** Spend a longer run on an evaluation lens (definitions, baselines, metrics) and keep any primer short.
9. **Justify the review with a limitation and its mechanism, a knowledge gap or a literature gap.** A generic grand challenge, a wish list of properties or "still preliminary" does not justify a review.
10. **Group earlier reviews by focus, with citations, and state the differentiator in one sentence.** Delegate out-of-scope material to cited reviews.
11. **Never call earlier reviews scarce without naming them and what they omit.** The defensible form cites a dated search with the engine, date and query.
12. **Give the scope sentence an organising rule (a thesis, a classification criterion, a sequence or an inclusion rule) and at least one justified exclusion with a pointer.** Drop "comprehensive".
13. **Keep the scope sentence in the introduction.**
14. **Fix the sorting terms and umbrella vocabulary in the introduction and reuse them as headings.**
15. **End a review introduction with a roadmap in body order, anchored to an overview figure, and check every section number against the final headings.** The roadmap frames the order of the argument ("from ⟨stage A⟩ to ⟨stage B⟩ to the problems they share"), not only the order of chapters.
16. **Write as the field's narrator, not as its auditor.** The introduction states what the field has achieved and where it is going. It never describes how the authors searched, screened, counted or graded papers; that belongs in a Methods box or the SI, if anywhere.

### Both

17. **Give the generic grand challenge one sentence at most.** Broad motivations that could open any paper in the field (a famous law, a market size, an analogy to nature) earn one sentence and must map onto a concrete requirement.
18. **Place one borrowed number, with its unit, condition and citation, where it does work.** At the gap it sets the constraint; in the opening it sets the stakes.
19. **When the application sets thresholds, list numbered requirements before judging prior work, then answer them in order.**

## Templates

Placeholders mark where sourced content goes. Never leave a placeholder value in a manuscript.

**T1. Research-article introduction (Nature-family style; unheaded, 3–5 paragraphs, about 450–650 words).**
- P1 context and constraint: the application demand, then one sourced number that sets the constraint.
- P2 alternatives: each prior route with its cited limit, closed by the capability the field needs at a named scale, or by numbered requirements.
- P3 (optional): why the candidate approach could close the gap, and where reports stop (small scale, partial system, simulated result).
- P4 pivot: "Here, we [report/demonstrate] [object] [enabling element] [scale number]", then one sentence per result in Results order, each number tagged measured or simulated.

Shape (P2 and P4): *In ⟨setting⟩, ⟨step A⟩ is cheap, but ⟨step B⟩ is costly: it takes up to ⟨value⟩ of ⟨resource⟩ [ref]. Sharing ⟨B⟩ cuts that cost but ⟨penalty 1⟩; lowering ⟨parameter⟩ saves ⟨resource⟩ but ⟨penalty 2⟩ [refs]. ⟨Candidate approach⟩ avoids ⟨limit⟩, but it has been evaluated with ⟨external component⟩, so its ⟨overhead⟩ is unmeasured. Here, we report ⟨object⟩ with ⟨enabling element⟩, measured on ⟨scale⟩.*

**T2. Review introduction (5–7 paragraphs; scope sentence within about 750 words).**
- P1 stakes, with one sourced number.
- P2 incumbent limits as mechanisms (the evaluation lens).
- P3 the candidate class, defined operationally, and the decisive result the field is working toward.
- P4 positioning: earlier reviews grouped by focus, what none of them does, and a one-sentence differentiator.
- P5 scope: organising rule, inclusion rule, exclusions with pointers, fixed vocabulary, anchor to Fig. 1.
- P6 roadmap in body order, framed by the argument.

Shape (P4–P6): *Earlier reviews covered ⟨focus A⟩ [refs] or ⟨focus B⟩ [refs]. None separates ⟨distinction⟩, which is where published claims diverge. This Review is organised by that distinction (Fig. 1). We cover work on ⟨scope⟩ since ⟨year⟩; ⟨excluded topic⟩ is reviewed in [refs]. Section 2 defines ⟨lens⟩, Sections 3–5 follow ⟨order⟩, and Section 6 turns to the problems they share.*

**T3. Gap paragraph by elimination (3–5 sentences).** State the requirement with a number. Give alternative A with its limit [ref] and alternative B with its limit [ref]. Close with the capability that would meet both conditions, and what it would enable.

Shape: *⟨Application⟩ needs ⟨property 1⟩ and ⟨property 2⟩ at ⟨scale⟩. ⟨Route A⟩ meets ⟨property 1⟩ but varies in ⟨property 2⟩ [refs]. ⟨Route B⟩ meets ⟨property 2⟩ but costs ⟨penalty⟩ [refs]. A route that meets both at ⟨scale⟩ would enable ⟨consequence⟩.*

**T4. Contribution sentence.** Here, we [verb] [object] that [enabling element], and [one quantitative result with evidence level and scope].

## Anti-patterns and fixes

| Pattern | Before (constructed) | After |
|---|---|---|
| Circular opening | "Building intelligent systems has long been a vision of the modern era." | "⟨Application⟩ must ⟨task⟩ within ⟨budget⟩ [refs]." |
| Contentless literature gap | "There are few comments on the latest progress." | "Reviews [a–c] cover ⟨focus A⟩ and ⟨focus B⟩. None compares ⟨approaches⟩ by ⟨criterion⟩, the organising axis of this Review." |
| The review's own coverage as the gap | "This review addresses the need for a comprehensive understanding of ⟨topic⟩." | "Published ⟨studies⟩ report ⟨metric⟩ under different ⟨conditions⟩ [refs], so they cannot be ranked. Section ⟨n⟩ normalises them to ⟨common basis⟩." |
| Uncheckable scope | "This study conducts a comprehensive review of various domains of ⟨topic⟩." | "We compare ⟨n⟩ named ⟨classes⟩ on ⟨metrics⟩ and trace ⟨trade-off⟩ to two levers, ⟨lever 1⟩ and ⟨lever 2⟩." |
| Novelty as the gap | "In this paper, ⟨material⟩ was studied for the first time." | "We test whether ⟨intervention⟩ narrows ⟨spread⟩ from ⟨baseline value⟩ [ref]." |
| Introduction claims more than Results | "The method supports up to eight levels." | "The method retains four levels under ⟨condition⟩; eight are reachable when ⟨tolerance⟩ is accepted." |
| Self-praise in the roadmap | "This paper is meticulously organised as follows…" | "Section 2 defines ⟨lens⟩, and Sections 3–4 cover ⟨topics⟩." |
| Screening narrative | "We screened ⟨N⟩ papers and graded each by evidence level." | "⟨Field⟩ has moved from ⟨stage A⟩ to ⟨stage B⟩ [refs]; this Review follows that path." |

## Venue differences

Venue predicts the template (heading, pivot formula, roadmap style) more reliably than quality.

- Nature-family articles: the introduction is usually unheaded, uses an explicit "Here, we" pivot and first person, and ends on a results preview.
- Nature-family reviews: first-person scope and a roadmap are common; Key points boxes and question headings appear in some titles.
- Society-journal reviews (ACS, RSC, Wiley, APS, Elsevier society titles): a roadmap is standard; the gap often comes later and is framed as a technology or knowledge gap. Chemical Reviews adds a contents list.
- IEEE and many engineering venues: a section-numbered roadmap ("The remainder of the paper is organised as follows. Section II …").
- Open-access mega-journals: scope sentences are often impersonal ("This paper reviews …"); positioning against named reviews strengthens them.

## Checklist

- Articles: the gap appears by the end of paragraph 2 and names a missing capability or alternatives with their limits.
- Articles: the pivot names the object, the enabling element and one number, within about 150 words of the gap.
- Articles: the introduction ends on a results preview with evidence labels and no roadmap.
- Reviews: the gap is a limitation with its mechanism, a knowledge gap or a literature gap, reached within about 500 words.
- Reviews: earlier reviews are grouped by focus with citations, and the differentiator is one sentence.
- Reviews: the scope sentence gives an organising rule and at least one exclusion with a pointer, inside the introduction.
- Reviews: the roadmap follows body order, and every section number matches a heading.
- Reviews: no screening, counting or grading narrative in the text.
- Generic grand challenges take one sentence at most.
- No "first", "to the best of our knowledge", "comprehensive" or "few reviews" without evidence.
- Sorting terms defined in the introduction reappear as headings.

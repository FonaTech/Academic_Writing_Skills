# Case 06: one set of facts, three drafts, four genres

A constructed teaching case. The same six facts are written as a parameter inventory, as an even causal chain and as a researcher's line of thought, and the third version is then carried into other genres and into Chinese. Placeholders stand for sourced content.

## The facts list (fixed before drafting)
| # | Fact | Evidence label | Source |
|---|---|---|---|
| F1 | ⟨A⟩ and colleagues (⟨year⟩) replaced ⟨X⟩ in ⟨system⟩ with ⟨Y⟩; ⟨Y⟩ avoids ⟨cost⟩ | measured | [1] |
| F2 | ⟨metric⟩ fell from ⟨v1⟩ to ⟨v2⟩ under ⟨protocol⟩ | measured | [1] |
| F3 | a ⟨control⟩ traced the gain to ⟨cause⟩ | measured | [1] |
| F4 | a ⟨baseline⟩ of the same size under the same protocol reached ⟨v3⟩ | measured | [2] |
| F5 | after ⟨n⟩ ⟨cycles⟩, ⟨metric⟩ drifted back to ⟨v4⟩ | measured | [1] |
| F6 | the same team simulated ⟨larger scale⟩ and obtained ⟨v5⟩, with drift left out of the model | simulated | [3] |

The list is the contract. A rewrite may reorder, merge or split sentences, but it may not add a cause, a motive or a comparison that the sources do not state.

## Draft A: parameter inventory
> ⟨A⟩ et al. used ⟨Y⟩ in ⟨system⟩ [1]. The ⟨metric⟩ was ⟨v2⟩. The original value was ⟨v1⟩. A ⟨baseline⟩ reached ⟨v3⟩ [2]. After ⟨n⟩ ⟨cycles⟩, the ⟨metric⟩ was ⟨v4⟩ [1]. A simulation at ⟨larger scale⟩ gave ⟨v5⟩ [3].

Diagnosis: five of six sentences report a bare value (linter `number-run`). The reason for ⟨Y⟩ (F1) and the mechanism (F3) are missing, so nothing says what the numbers show. The comparison with the baseline is not tied to anything, and the paragraph ends on a simulated number.

## Draft B: even causal chain
> ⟨X⟩ limits ⟨system⟩ because it ⟨causes cost⟩, so ⟨A⟩ et al. replaced it with ⟨Y⟩ [1]. The ⟨metric⟩ therefore fell from ⟨v1⟩ to ⟨v2⟩ because of ⟨cause⟩. Since a ⟨baseline⟩ of the same size reached only ⟨v3⟩ [2], ⟨Y⟩ is thus the better choice. Then, after ⟨n⟩ ⟨cycles⟩, the ⟨metric⟩ drifted to ⟨v4⟩ [1], so stability is the next problem. Because of this, the team then simulated ⟨larger scale⟩ and obtained ⟨v5⟩ [3], so scaling appears feasible.

Diagnosis: every sentence carries one or two explanation connectives, and all five sentences have about the same length (linter: connective rate far above 8 per 100 sentences, `uniform-rhythm`). The chain also damages correctness. "Because of this" invents a motive for the simulation that no source states. "The better choice" and "appears feasible" are verdicts the facts do not support, since the advantage drifted away (F5) and the scaling result is simulated without drift (F6).

## Draft C: the researcher's line of thought
> In ⟨year⟩, ⟨A⟩ and colleagues replaced ⟨X⟩ in ⟨system⟩ with ⟨Y⟩, which avoids ⟨cost⟩ [1]. The ⟨metric⟩ fell from ⟨v1⟩ to ⟨v2⟩ (⟨protocol⟩), and a ⟨control⟩ traced the gain to ⟨cause⟩. A ⟨baseline⟩ of the same size reached ⟨v3⟩ under the same protocol [2]. After ⟨n⟩ ⟨cycles⟩, however, the ⟨metric⟩ drifted back to ⟨v4⟩ [1]. A simulation by the same team puts it at ⟨v5⟩ for ⟨larger scale⟩, with the drift left out of the model [3].

Reasons it reads well:
- The private questions decided the order: what problem ⟨Y⟩ solves (F1), what it achieved and why (F2, F3), against what (F4), what it left open (F5), and how far the evidence reaches (F6).
- The actors carry the paragraph. "The same team" links F6 without a connective.
- One contrast word marks the only turn in the argument. No sentence uses so, because, since or then.
- Lengths vary with the content: the mechanism sentence is long and the baseline sentence short.
- The ending is a fact, the gap between simulation and drift, which the next paragraph can take up. No verdict or forecast is added.

## The same chain in other genres
**Article Results (the authors' own work).** "We replaced ⟨X⟩ with ⟨Y⟩ to avoid ⟨cost⟩ (Fig. 2a). The ⟨metric⟩ fell from ⟨v1⟩ to ⟨v2⟩ (⟨protocol⟩; ⟨N⟩ devices; Fig. 2b). Devices with ⟨control⟩ showed no change (Fig. 2c), which ties the gain to ⟨cause⟩." The control that rules out the obvious alternative takes the place that a citation takes in a review. The drift goes into the next Results paragraph or into the Discussion as a measured limit.

**Abstract.** One sentence carries F1 and F2 with the condition: "Replacing ⟨X⟩ with ⟨Y⟩ lowers ⟨metric⟩ from ⟨v1⟩ to ⟨v2⟩ under ⟨protocol⟩." F5 enters only when stability matters for the main claim.

**Proposal, preliminary evidence.** "Our devices with ⟨Y⟩ lowered ⟨metric⟩ from ⟨v1⟩ to ⟨v2⟩ [own ref], which makes Aim 1 feasible. They drifted back after ⟨n⟩ ⟨cycles⟩. Aim 2 tests ⟨stabilisation⟩ against this benchmark and falls back to ⟨alternative⟩ if ⟨criterion⟩ is not met." Here the open fact (F5) becomes the reason for an aim.

**Response to a referee.** "Drift was measured over ⟨n⟩ ⟨cycles⟩ and is now reported in Fig. 2d and Section 3.2 (lines ⟨a⟩–⟨b⟩)." The chain is point, change, location.

## Chinese version of draft C
> ⟨年份⟩年，⟨A⟩等用⟨Y⟩替换了⟨体系⟩中的⟨X⟩，以避开⟨代价⟩ [1]。⟨指标⟩由⟨v1⟩降至⟨v2⟩（⟨测试条件⟩），对照实验（⟨对照⟩）表明提升来自⟨原因⟩。同样尺寸的⟨基准⟩在相同条件下为⟨v3⟩ [2]。不过，经过⟨n⟩次⟨循环⟩后，⟨指标⟩回到⟨v4⟩ [1]。同一团队的仿真给出⟨更大规模⟩下的⟨v5⟩，模型中没有计入这种漂移 [3]。

The Chinese carries the same numbers, citation keys and evidence labels. It uses one contrast word (不过) and no 因此 or 从而, and its sentence lengths vary as the English ones do (sci-prose-style, bilingual-consistency.md).

## Section opening built from the same material
Weak: "This section first introduces ⟨Y⟩, then discusses its stability, and finally considers scaling." (a table-of-contents overview). Better: "⟨Y⟩ lowers ⟨metric⟩ by removing ⟨cost⟩ (Section ⟨n.1⟩). Its benefit fades with use, and models that leave the fade out predict ⟨metric⟩ at larger scale (Section ⟨n.2⟩)." Each sentence states a fact about the subject, and the section numbers sit in parentheses. The overview names the shared basis and how the subsections divide it, without describing the order of the text.

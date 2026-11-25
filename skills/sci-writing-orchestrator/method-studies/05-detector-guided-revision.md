# Case 05: revising a manuscript over successive AI-detector reports

A method study abstracted from several revision rounds of one long manuscript. Field content, scores and dates are left out. The steps and the failure modes transfer to any genre, language and detector.

## Situation
- After each revision the authors scanned the manuscript with a commercial detector and asked for the flagged text to be rewritten. Every number, citation, table and figure had to stay.
- Each report gave a verdict per segment (AI, mixed or human) and a risk value. The overall score was close to the mean segment risk, so the effect of a rewrite could be estimated before the next scan.
- The report gave no reasons beyond a fixed template, so every rule had to come from comparison.

## Method
1. **Decompose the score before rewriting anything.** Map each segment back to its source block. Split prose (body paragraphs, caption and note sentences) from non-prose (table rows, headers, abbreviation lists). Non-prose segments were flagged in every round whatever their wording, so they set a floor under the score. Tell the author the floor at once, because it decides whether the target is reachable.
2. **Compare flagged and passed prose within the same manuscript.** Word lists explained little. Three measures separated the groups: the share of sentences that carry a number (about three in five in flagged segments against two in five in passed ones), runs of bare number sentences, and, after one pass, the rate of explanation connectives. Sentence length and citation density did not separate them. Measure first; do not assume which feature matters.
3. **Scan a human control.** A published, human-written paper in the same field, scanned by the same detector, gave reference values for each measure. Its own nonzero score also calibrated what the authors could expect.
4. **Read the paragraphs that flipped.** Between two reports some paragraphs moved from AI to human. Listing what changed in them (concrete verbs instead of noun phrases, a study told in time order, a concession, one citation per study) gave the next rules.
5. **Test one hypothesis per pass.** Each pass changed one property of the flagged paragraphs and left passed paragraphs word for word, so the next report could test the change.
6. **Guard every edit** (case 07). No pass changed a number, a citation key or a float reference, and the second language followed block by block.
7. **Check each rewrite for a new regularity before delivery.** Compute the same measures on the rewritten paragraphs and compare them with the passed ones.

## What the rounds showed
| Pass | Change | Next report | Lesson |
|---|---|---|---|
| Vocabulary | flagged words and stock phrases replaced; a fixed reasoning template added | score rose slightly | detectors respond to organisation more than to words |
| Narrative | studies told as actor, action, finding; concrete verbs; concessions; one citation per study | large fall; the paragraphs that flipped to human shared these changes | narration by named actors reads as human |
| Explained numbers | each number put inside a clause that says what it shows; bare number runs broken | further fall | parameter inventories are the strongest single signal |
| Linked chain | every sentence made to answer the previous one with so, because or then | small fall; most rewritten paragraphs stayed flagged, now with a higher connective rate than passed ones | a remedy applied to every sentence becomes a regularity |
| Actor-led, low connective | causes carried by order and named actors, conditions in parentheses, mixed lengths, connective rate near the control | to be read from the next report | a pass is judged by the next report |

Explicit links helped while the paragraphs were inventories and hurt once every sentence had one. The dose matters more than the device.

## What a writer takes from it
- Avoid the regularities from the first draft (sci-prose-style, human-line-of-thought.md) instead of repairing them later. Most future projects will have no report at all.
- Use the linter's measures as a proxy: `number_sentence_share`, `explain_connectives_per_100_sentences`, `number-run` and `uniform-rhythm`. Compare them with a human paper from the target journal when one is at hand.
- Rewrite paragraphs as wholes when they are inventories, and leave passed paragraphs alone.
- Section overviews and other new paragraphs are scanned like the rest. Write them like body text.
- Stop when the prose reads well. A lower score is not worth a vaguer claim, a lost condition or a changed number.

## Reporting to the authors
Each round ended with a short table: score, segments, flagged prose, flagged non-prose and the estimated floor, then the paragraphs changed and the open items. When the target was below the floor, the report said so plainly and listed the choices that are the authors' to make, such as scanning without tables or moving tables to the supplement. The report also said that journals require disclosure of AI assistance whatever the score.

# Case 14: Chinese scientific prose, written first or paired with English

A method study for Chinese manuscripts, Chinese theses, 基金申请书 and Chinese versions of English papers. The rules are in sci-prose-style, bilingual-consistency.md; this case shows how they are applied.

## Two situations
- **Chinese written first** (a Chinese journal, a thesis, a national grant): the Chinese is the authoritative text. Write it from the facts list and the line of thought, as for English, then derive any English version from it.
- **Chinese paired with English** (a bilingual review or report): finish the English block, then write the Chinese from that block. Sentences may be split or merged, but each block keeps its numbers, citation keys and float references.

## What makes Chinese read as generated
| Regularity | Example | Repair |
|---|---|---|
| template openers and closers | 随着……的快速发展；值得注意的是；综上所述 | start from the problem or the fact; end on a fact |
| importance phrases | 发挥着重要作用；具有重要意义；应用前景广阔 | say what the thing does, for whom, under which condition |
| even causal chain | 因此……从而……进而……由此 on consecutive sentences | let the order of sentences carry the cause; keep one connective where the link would be missed |
| counted parallel lists | 首先……其次……最后 for items without an order | name each group by what separates it |
| English calques | 进行了……的研究；对……具有……的影响；实现了……的提升；作为……，; 一个 for "a" | the plain verb: 研究了；影响；提高了 |
| long attributive chains | 在……条件下由……制备的具有……特性的器件 | two sentences, or the condition in parentheses |
| uniform length | every sentence 35–45 characters | long sentences for mechanisms and conditions, short ones for plain results |

`prose_lint.py` reports `zh-template`, `zh-question`, `zh-connective`, `zh-ordinal` and `zh-uniform-rhythm`, and gives the connective rate per 100 sentences.

## Constructed example
Before: "随着⟨领域⟩的快速发展，⟨方法⟩引起了广泛关注。值得注意的是，⟨方法⟩在⟨应用⟩中发挥着重要作用。因此，研究人员对其进行了深入研究，从而使⟨指标⟩得到了显著提升。"

After: "⟨应用⟩受限于⟨代价⟩ [1]。⟨作者⟩等在⟨年份⟩用⟨方法⟩绕开了这一代价，⟨指标⟩由⟨v1⟩提高到⟨v2⟩（⟨条件⟩）[2]。这一提升只在⟨范围⟩内成立，超出后⟨指标⟩回落到⟨v3⟩ [2]。"

The first version has a template opener, an attention phrase, an importance phrase, an even 因此/从而 chain, a calque and an unsupported 显著. The second names the problem, the actor, the change with its condition and the range where it holds.

## In each Chinese genre
| Genre | What to watch |
|---|---|
| 期刊论文 | 摘要 and 结论 carry the same numbers as the body; 关键词 use the field's standard terms |
| 学位论文 | each chapter opens on the question the previous one left; 本章小结 states results |
| 基金申请书 | 立项依据 states the gap with numbers; 拟解决的关键科学问题 is a statement of what is unknown; 研究方案 gives the controls and the success criteria |
| 中英双语稿 | the Chinese adds no connective, inference or hedge that the English block lacks |

## Terms and numbers
- Use the field's established Chinese terms. If none exists, give the Chinese name with the English abbreviation at first use, then use one form throughout.
- Numbers, units and symbols keep the source form; write numbers so that the parity checker parses them the same in both languages.
- Full-width punctuation in Chinese text, half-width inside formulas, units and Latin-only phrases.

## Checks
- No template phrase, question or counted list in the body.
- The connective rate stays near 8 per 100 sentences or below; sentence lengths vary.
- Each block of a bilingual pair has the same numbers, citation keys and float references in both languages.

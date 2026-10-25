# AI-flavour and hype lexicon

Text generated or over-edited by language models has a recognisable surface. It shows promotional adjectives, stock importance phrases, symmetrical contrasts, rule-of-three lists, colon reveals, dash asides, stacked hedges and commentary about the text itself. Expert authors in every field use these rarely, and when they do the phrase carries information.

The hard rules live in one file, `assets/style_limits.json`. `scripts/prose_lint.py` reads it, and so does the manuscript kit's `check_manuscript.py`, which carries an identical copy. Entries marked `user` are the author's own rules; entries marked `kit` are house defaults. A project changes an entry by its label under `style.overrides` in manuscript.json. The tables below give the reason for each rule and the replacement. Where this page and the JSON file differ, the file applies; fix this page.

## Hard limits

Caps count matches in running text. They hold as written up to 10,000 words and grow in proportion above that, so a 20,000-word thesis chapter may use "therefore" ten times.

| Entry | Cap per 10,000 words | Source | Keep it when |
|---|---|---|---|
| must | 3 | user | a physical or logical necessity; advice to the field reads better as "needs" or "should" |
| therefore | 5 | user | a real inference from the previous sentence |
| thus, hence | 5 | kit | the same budget, so the cap cannot be met by swapping words |
| rather than, "X, not Y" | 4 together | user | the contrast is the finding |
| boundary | 3 | kit | the accounting scope is named once; then use the scope word itself |
| dash aside (—, --, spaced –) | 2 | user | almost never; use a comma pair, brackets or two sentences |
| "this review aims to" | 1 | kit | once, in the introduction |

Banned phrases are reported at every match, in body text, captions and table notes.

| Banned (user) | Replace with |
|---|---|
| useful | what it allows: "sets the read margin", "removes one calibration step" |
| credible | the evidence level and the condition: "measured on ⟨N⟩ samples under ⟨condition⟩" |
| decisive | the measured difference |
| This is why | one sentence with "because" or "so" |
| delve | analyse, compare, measure |
| pivotal | what it controls |
| underscore | shows, or delete |
| notably | delete; the content carries the weight |
| landscape | the field or the set of methods by name |
| intricate | the parts that interact |
| furthermore | delete; order sentences from known to new |
| not only … but also | two plain statements, or "both … and" |
| evaluative triplet ("fast, efficient and scalable") | only the property you then support with a number |
| colon reveal ("The answer is simple: …") | state the claim as the sentence |
| "In summary" / "To summarise" as an opener | end the section on its consequence |
| coined jargon (checked by hand) | the term the cited papers use; add accepted terms to the terminology table |

The kit also bans crucial, paramount, leverage, revolutionary, game-changing, pave the way, "plays a … role", holds promise, unprecedented, groundbreaking, realm, tapestry, paradigm shift, cutting-edge, state-of-the-art, seamless, "novel and unique", "it is worth noting" and "should be read as". Closing clichés are banned too: "opens new avenues", "the next frontier", "vast potential", superb, impactful, meticulous, "shaping the future" and "continues to evolve". The replacements are in the JSON file. Priority claims ("first", "record", "lowest known") are not banned; keep them only with the comparison and its date.

Several user bans are stricter than common practice: published papers use "furthermore" and "notably" often. The bans are house style, not a claim that expert papers never use these words. A project can relax an entry through `style.overrides` in its manuscript.json.

## Weight 3 in the linter: delete or rewrite every time

| Pattern | Why it fails | Replace with |
|---|---|---|
| embark on, navigate the complex, harness the power | narrative filler | the verb that names the action |
| ecosystem, journey (as metaphors) | decorative metaphor | the field or the set of methods by name |
| unlocks the potential, in the ever-evolving, ever-growing demand | unfalsifiable promise | the next measurable step: "would allow ⟨capability⟩ if ⟨spread⟩ falls below ⟨threshold⟩" |
| remarkable, outstanding, impressive, exceptional, excellent or superior performance | evaluation without data | the metric and value |
| a testament to, showcases, boasts | promotional register | reports, shows, reaches |
| synergy, holistic, multifaceted | marketing | the specific interaction |
| needless to say, in today's world | filler | delete |

## Weight 2: usually replace

| Pattern | Replace with |
|---|---|
| key (adjective) | main, or the reason |
| utilise, utilization | use |
| facilitate | allow, enable, or the verb for what happens |
| importantly, interestingly, remarkably, moreover, additionally (as openers) | delete; order sentences from known to new |
| comprehensive, robust, novel, innovative, promising | delete or give the evidence |
| significant(ly) outside statistics | large, substantial, or the number |
| various, numerous, a wide range of | the number or the list |
| in order to, due to the fact that | to, because |
| with respect to, in terms of | for, in, or rewrite |
| very, highly, extremely, greatly, dramatically, tremendously | the number |
| has emerged as, has attracted increasing attention | "is used for", or delete |

## Defensive and disclaimer phrases (advisory, weight 2)

These phrases protect the author instead of informing the reader. A review full of them reads as a list of what the field has failed to do. State what was done, with its scope, and then the implication or the next step. Evidence labels (simulated, estimated, projected) are not defensive; keep them attached to the number.

| Pattern | Replace with |
|---|---|
| so far, to date, up to now, until now | delete; give the year or the scope if it matters |
| still, yet, not yet | delete, or state the next step: "would require ⟨experiment⟩" |
| only, merely (minimising a result) | the number and its scope: "⟨N⟩ units" |
| has not been shown, has not been reported, remains missing, remains unclear | "⟨Experiment⟩ would show whether ⟨claim⟩ holds" |
| cannot yet be compared, no study has | "A same-task measurement of ⟨metric⟩ would allow a direct comparison" |
| further studies are needed, remains to be explored | the named study and what it would show |
| it should be emphasised that the results are preliminary | delete; the evidence label carries the status |

## Weight 1: check in context

| Pattern | When it is fine | When to change |
|---|---|---|
| however | a real contrast with the previous claim | opening consecutive paragraphs |
| framework | a named, defined model | an abstract noun doing no work |
| in conclusion, overall | once, at the end of a section | as a repeated paragraph opener |
| in recent years, with the rapid development of | never needed | delete; start with the fact |
| clearly, obviously, it is clear that | never needed | delete; show the evidence |
| note that | a plain "Note that" before a real caveat (acceptable once or twice per paper) | as a signpost; "it should be noted that" and "it is worth noting" are banned |

The linter also counts three-item lists without flagging them. Lists of measured quantities or materials ("Ti, Ni and Pd") are fine; only evaluative triplets are banned.

## Structural patterns

| Pattern | Example | Fix |
|---|---|---|
| Colon reveal (banned) | "The problem is clear: calibration dominates." | "Calibration dominates the run time." |
| Colon before a lowercase clause (advisory, more than 3 per 10,000 words outside captions) | "Two regimes appear: the first is linear." | keep lists; rewrite reveals |
| Dash aside (cap 2) | "The sample — which is small — responds." | fold into the sentence or cut |
| Symmetric contrast (cap 4 with "rather than") | "It is not a component problem, but a system problem." | state the positive claim: "The limit is set at the system level." |
| Evaluative triplet (banned) | "fast, efficient and scalable" | keep only the properties you then support |
| Stacked hedges | "may potentially suggest a possible" | one hedge: "suggests" |
| Meta-commentary | "This section aims to discuss …", "Figure 3 should be read as …", "as mentioned above" | delete; say what the section or figure shows |
| Moral at the end of every paragraph | "This highlights the importance of …" | end with the consequence only where it adds information |
| Cause signpost (banned) | "This is why calibration dominates." | "Calibration dominates because …" |
| Question headings and rhetorical questions | "Why does this matter?" | a noun-phrase heading that names the content |
| Emphatic typography | bold words in running text, ALL CAPS | none in body text |
| Workflow residue | "local corpus", "our library", "extracted record", "evidence strip", "not specified in abstract", internal IDs | delete; write "n.s." in tables with a note |
| Screening-report voice | "we screened ⟨N⟩ papers", "evidence level" or tier tags in running text, "of the ⟨N⟩ studies we graded" | write the field's progress; keep evidence labels attached to numbers only |
| Preprint mention | "in a preprint", "a ⟨year⟩ preprint" | cite directly; the reference list shows the status |
| "namely" in captions | "three routes, namely A, B and C" | a colon: "three routes: A, B and C" |
| Per-paper fault-finding | "⟨Author⟩ did not state ⟨condition⟩", "with no sample size" | a field-level statement: "⟨Metric⟩ is rarely reported with ⟨condition⟩ [refs]" |
| Coined jargon (banned, checked by hand) | "precision wall", "converter tax" | the term the cited papers use, or a plain description |

## Chinese counterparts (中文稿常见问题)

| 问题 | 例 | 改法 |
|---|---|---|
| 空泛拔高 | 具有重要意义、开辟了新途径、取得了突破性进展 | 说明具体提升了什么、多少 |
| 套话开头 | 随着……的快速发展、近年来、综上所述（段首） | 直接陈述事实 |
| 连接词堆叠 | 此外、同时、并且、进而 连用 | 按“旧信息→新信息”排句，删连接词 |
| 被动与“进行” | 对器件进行了测试 | 测试了器件 |
| 的字链 | 器件的阵列的读出电路的能耗 | 器件阵列读出电路的能耗 |
| 长定语 | 在……条件下由……制备的具有……特性的器件 | 拆成两句 |
| 中英混排不一 | ⟨unit⟩/W 与 ⟨unit⟩ W⁻¹ 混用；“图 1a”与“Fig. 1a” | 按术语表统一 |
| 叠甲句 | 目前仍、迄今尚未、仅、还没有、有待进一步研究 | 陈述已完成的工作，再写下一步（“若能……将可……”） |
| 逐篇挑错 | 某某未说明温度、未给出样本量 | 写成领域层面的陈述：“⟨指标⟩很少连同⟨条件⟩一起报道” |
| 中文独有连接词 | 英文没有对应的“因此”“由此可见” | 与英文逐块对应；英文无连接词时中文也不加 |
| 数字写法不一 | 英文 26.6 million，中文写成 2,660 万 | 写成检查器能同样解析的形式，如“26.6 百万” |

# Bilingual consistency (English ↔ Chinese)

## Principle
The two versions are one document in two languages. They share blocks, numbers, citation keys, float references and section structure. Only the language differs.

## Workflow
1. Finish the authoritative language (usually English) for a section, including captions and tables.
2. Translate block by block into the paired `zh` field. Do not translate from a rendered `.docx`; translate from the source block so markup (`[@key]`, `{fig:…}`, `$…$`) is kept.
3. Run the bilingual check: every block present; the same citation keys, float references and numbers in both.
4. Read the Chinese as Chinese: fix calques and long attributive chains; keep terminology from the table. Run `prose_lint.py` on the Chinese file and apply the native-prose rules below.
5. When a later English edit changes a fact, change the Chinese block in the same commit.

## Chinese style rules
- Short sentences; split long attributive chains ("在……条件下由……制备的具有……特性的器件" → two sentences).
- Active verbs: "测试了器件", not "对器件进行了测试".
- Remove empty intensifiers and slogans: 显著、极大地、重要意义、突破性进展、开辟了新途径.
- Connectors only where the logic needs them: 因此、然而 used sparingly; avoid 此外/同时/并且 chains.
- Full-width punctuation in Chinese text (，。；：（）“”); half-width inside formulas, units and Latin-only phrases.
- Numbers and units in Latin form with a space before the unit (6.5 ms, 20 nm); percentages without space (1.8%).
- Write each number in a form the parity checker parses identically in both languages. Keep the English mantissa and convert only the word: "26.6 million" → "26.6 百万", not "2,660 万"; "2 × 10^{6}" stays "2 × 10^{6}". Do not introduce a scientific-notation form in one language that the source does not use.
- Do not add connectives that the English block lacks (因此、由此可见、总之); a ZH-only inference is content drift.
- Captions: "即" is acceptable in Chinese where the English uses a colon.
- Figure and table references: 图1a、表2、式（3）；section references: 第 4 章、4.2 节.
- Terms: Chinese term with the abbreviation at first use, then the abbreviation or the Chinese term consistently.
- Keep the English sentence order where it helps alignment, but not at the cost of natural Chinese.

## Writing Chinese that reads as native expert prose
The Chinese version follows the same line of thought as the English (human-line-of-thought.md) and has its own regularities to avoid. Write it from the finished English block. Sentences may be split or merged, but each block keeps its numbers, citation keys and float references.

- **研究者作主语，按事情的先后叙述。** "⟨作者⟩等把⟨X⟩换成⟨Y⟩，以避开⟨代价⟩。⟨指标⟩由⟨v1⟩降至⟨v2⟩（⟨条件⟩）。"少用"研究表明""据报道""被证明"开头的无主语句。
- **连接词要少。** 因此、从而、进而、所以、由此、于是合计每 100 句约 8 次以内，因果主要靠句序承担。不要句句以"因此"开头或以"从而……"收尾。此外、同时、并且也不连用。`prose_lint.py` 报告 `zh-connective`（一段中超过四成的句子含这类词），并在统计中给出 `zh_connectives_per_100_sentences`。
- **句长有长有短。** 中位数约 25–35 字，单句不超过约 90 字。机理和条件写成长句，单纯的结果写成短句；一段中各句长度都相近时，检查脚本报告 `zh-uniform-rhythm`。
- **条件放进括号。** "（室温，100 次循环）"，不为每个条件另起一句。
- **去掉英文腔。** "进行了……的研究"改为"研究了"；"对……具有……的影响"改为"影响……"；"实现了……的提升"改为"提高了……"；"被"字句只在施事者无关时使用；不用"一个"对应英文的 a；"作为……，"和"基于……的"不作为句首套语反复出现；连续三个以上"的"的定语链拆开。
- **不写模板句。** 值得注意的是、综上所述、总而言之、随着……的发展、发挥着重要作用、引起了广泛关注、为……提供了新思路、奠定了基础、具有重要意义、应用前景广阔。检查脚本报告为 `zh-template`（权重 2），删去后直接写事实。
- **不写问句。** 设问、反问和"是否……取决于……""如何……是关键"一类的内嵌问句都改成陈述（`zh-question`）。
- **并列内容不计数。** 内容没有先后时，不用"首先……其次……最后""一方面……另一方面"，按区分各组的依据命名各组（`zh-ordinal`）。
- **段尾落在事实上。** 不以"具有重要意义""前景广阔"一类的评价句收尾，段尾是下一段要接着讲的事实或限制。
- **用领域中文文献的通行术语。** 没有通行译法时，首次出现写中文全称加英文缩写，此后统一用缩写。不为避免重复而换用近义词。

Constructed example. Before: "值得注意的是，⟨方法⟩在⟨领域⟩中发挥着重要作用。因此，研究人员对其进行了深入研究，从而使⟨指标⟩得到了显著提升，为⟨应用⟩提供了新思路。" After: "⟨作者⟩等在⟨年份⟩把⟨X⟩换成⟨Y⟩，以避开⟨代价⟩。⟨指标⟩由⟨v1⟩降至⟨v2⟩（⟨条件⟩），他们把这一变化归因于⟨原因⟩。" The template opener, the importance phrase, the even 因此/从而 chain and the promise are gone; the actor, the change and its condition carry the paragraph.

## Length variants and bilingual pairs
When a manuscript exists in several length variants (for example 25%, 50% and 100%), every variant is its own block-paired source. A factual fix in one variant is applied to the same block in every variant and in both languages in the same session. Keep variant-specific material (extra paragraphs in the long version, tighter wording in the short one); sync facts, numbers, citations and terminology. After a sync, run the checker on every variant.

## Common drift and how the checker catches it
| Drift | Check |
|---|---|
| a number updated in English only | number multiset per block differs |
| a citation added in one language | citation keys per block differ |
| a figure panel reference changed | float references per block differ |
| a paragraph added without its translation | block without `zh` text |
| different term for the same concept | terminology table review (manual) |
| number rewritten in another form in one language | number multiset per block differs; restore the source form |
| fix applied to one length variant only | run the checker on every variant; diff the block across variants |


## Runtime and scientific safeguards retained from 2.1

# Aligned scientific translation

Translate only requested languages. One may be authoritative, but both must preserve scientific meaning. Pair paragraph, caption, table cell and equation blocks with stable IDs.

Check: quantities including small integers, signs, exponents and units; object and method; qualifiers/uncertainty; negation and causal strength; comparison direction; measured/simulated/proposed status; reference and panel targets. Do not exchange table columns simply because a row contains the same number set.

The checker detects numeric/unit and reference inconsistencies. It cannot prove semantic equivalence; review paired text and terminology. A revised authoritative block invalidates its prior translation/review until checked. Unrequested second languages need not be created.

## Requested variants and external rewrites
Track each factual correction by stable block ID and apply it to every requested language/length variant that carries the claim. Check individual table cells, units, polarity, comparative direction, hedging and citation targets; equal sets of numbers are insufficient. A shorter variant may omit an argument but cannot retain a superseded fact. Maintain a project terminology table: English | abbreviation | Chinese | first-use location | meaning/spelling notes.

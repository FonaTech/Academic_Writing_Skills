# Bilingual consistency (English ↔ Chinese)

## Principle
The two versions are one document in two languages. They share blocks, numbers, citation keys, float references and section structure. Only the language differs.

## Workflow
1. Finish the authoritative language (usually English) for a section, including captions and tables.
2. Translate block by block into the paired `zh` field. Do not translate from a rendered `.docx`; translate from the source block so markup (`[@key]`, `{fig:…}`, `$…$`) is kept.
3. Run the bilingual check: every block present; the same citation keys, float references and numbers in both.
4. Read the Chinese as Chinese: fix calques and long attributive chains; keep terminology from the table.
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

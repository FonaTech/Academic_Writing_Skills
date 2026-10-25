# Content markup

## Blocks (content.py)

```python
CHAPTER = 4                      # headings without a leading number become 4, 4.1, 4.1.1
H('s4', 1, 'Measuring a first-order process', '一级过程的测量')
H('s4.1', 2, 'From the decay curve to the rate constant', '从衰减曲线到速率常数')
P('s4.1-a', '''English paragraph with [@smith2024] and {fig:decay|b}.''',
            '''中文段落，引用 [@smith2024] 与 {fig:decay|b}。''')
EQ('eq-decay', 'decay', r'y(t)=y_{0}\,e^{-kt}')
BOX('box1', 'fit')               # body defined in floats.BOXES['fit']
```

Block ids are stable handles for checks and cross-references; keep them when rewriting text. A heading can set `unnumbered=True` (for "Outlook" in some journals).

## Inline markup

| Write | Renders as | Notes |
|---|---|---|
| `[@a]`, `[@a; @b; @c]` | [1], [1–3] | Nature style; `citation_marker: superscript` for ACS-like superscripts |
| `{fig:key}` | Fig. 2 / 图2 | numbered by first mention in paragraphs and boxes |
| `{fig:key|b}`, `{fig:key|c, d}` | Fig. 2b, Fig. 2c,d | panel letters kept as written, spaces removed |
| `{tab:key}` | Table 1 / 表1 | |
| `{eq:key}` | equation (3) / 式3 | the equation must be displayed before it is cited |
| `{sec:id}` | Section 4.2 / 4.2 节; Chapter 4 / 第 4 章 | ids of headings |
| `{box:name}` | Box 1 / 专栏 1 | the box name used in `BOX()` |
| `$...$` | inline math | `_{}`, `^{}`, `\alpha`, `\mathrm{}`, `\mathbf{}` handled; no fractions |
| `CO~2~` | CO₂ | chemical subscripts outside math |
| `mol L^-1 s^-1`, `10^{-7}` | mol L⁻¹ s⁻¹, 10⁻⁷ | hyphen becomes a true minus |
| `T_m`, `k_obs` | T_m as subscript | only after a letter |
| `**a**`, `*Nature*` | bold, italic | |

Display equations go in `EQ()` or in a box item `{'type': 'eq', 'key', 'latex'}` and are converted to native Word equations.

## Floats (floats.py)

```python
FIGURES = {'decay': {'folder': 'Fig1_decay', 'caption_en': '...', 'caption_zh': '...'}}
TABLES = {'rates': {'title_en': '...', 'title_zh': '...', 'columns_en': [...], 'columns_zh': [...],
                    'rows_en': [[...]], 'rows_zh': [[...]], 'note_en': '...', 'note_zh': '...',
                    'widths': [1.2, 1.0, ...], 'year_column': True}}
BOXES = {'fit': {'title_en': 'Fitting window', 'title_zh': '拟合区间',
                 'items': [{'type': 'para', 'en': '...', 'zh': '...'},
                           {'type': 'eq', 'key': 'slope', 'latex': r'...'}]}}
```

Rows of a table carry the same numbers in both languages; only the text changes. Citations inside table cells and captions count for reference numbering at the position where the table or figure is placed.

### Year columns

- `'year_column': True` inserts a Year / 年份 column after the first column headed Ref., Refs., Source or 文献. Each cell shows the publication year of the works cited in that row's Ref. cell, taken from `references.json`; several works give a range (`2008–2024`). Separator rows (a group label in the first cell, all other cells empty) get a blank Year cell.
- `'year_inline': [2]` prefixes each citation group in column 2 with its year: `(2021) [@a]` in English, `（2021）[@a]` in Chinese.
- The no-citation edition keeps the years and drops a Ref. column that would otherwise be empty.
- Never type years into cells: a corrected reference then updates every table and every variant.

## Bilingual rules

- Every paragraph, heading, caption, table cell and box item has both languages before delivery.
- The same citation keys, float references and numbers must appear in both versions of a block; `check_manuscript.py` compares them.
- Write each number in the same form in both languages (digits, decimals and unit prefix unchanged), so the checker can match it. No connective, hedge or claim appears in one language only.
- Chinese uses full-width punctuation (，。；：（）) except inside math and around Latin-only expressions; units and symbols stay Latin.
- Keep the Chinese sentence order close to the English one so reviewers can align them, but write natural Chinese; do not calque English clause order.

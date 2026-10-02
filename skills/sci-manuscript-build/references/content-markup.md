# Declarative source and markup

`content.json` chooses ordered `sections` paths or inline `blocks`, never both. Each section is `{"blocks": [...]}`. Blocks have unique `id`, `type` (`heading`, `para`, `eq`, `box`), language text and optional `claims`. Heading levels follow the venue. Equations carry a `key` and `latex`; boxes can refer to a definition in `floats.json`.

Paragraph text is inline language fields, or `files: {"en": "sections/result.en.md", "zh": "sections/result.zh.md"}`. Do not define both inline text and file text for the same language. Markdown paragraph files support the kit's inline markup, not arbitrary multi-section Markdown or embedded HTML. Use one block for one coherent paragraph.

Supported markup: `[@key; @other]`; `{fig:key}` and `{fig:key|a}`; `{tab:key}`, `{eq:key}`, `{sec:id}`, `{box:name}`; `$inline_math$`; `**bold**`, `*italic*`; chemistry/unit subscript and superscript syntax retained from the legacy kit. Claims use exact source-text anchors including citation markup.

`floats.json` has `figures`, `tables`, `boxes`. Figures have folder, caption language fields and claims. Tables have title/column/row/note language fields and `cell_claims` indexed from zero. Numerical validation is cell-specific. Fields do not execute code.

Languages are opt-in and ordered; the first is authoritative for numbering. English and Chinese labels are built in; additional languages need project titles, translations and `labels` entries and visual testing. Selecting a second language does not automatically translate it.

Legacy `source.format = "python"` supports explicitly trusted `content.py`/`floats.py`; imports execute code. Archive and review such scripts before use or migration.

Numeric table cells inherit units only from explicit parentheses/brackets in the actual column heading. Bind each consequential numeric cell, including dimensionless counts, using cell_claims["row:column"]. Claims must carry conditions and accounting_scope whenever their evidence declares them. The metadata match does not prove that the prose expresses the condition; inspect it.

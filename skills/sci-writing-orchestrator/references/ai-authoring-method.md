# Choosing an AI authoring method

## Recommended hybrid
Use incremental evidence-led drafting plus repeatable construction. The default kit stores paragraphs/section blocks as data and leaves layout and numbering in stable code. This is an engineering choice for traceability and revision, not an experimentally established universal optimum.

1. Establish the question and provisional argument from actual evidence.
2. Draft a section in readable text. Review its claims, conditions, references and figure needs.
3. Store approved/marked-draft blocks in an ordered section file; use optional Markdown text files for long paragraphs. Keep claim IDs and evidence keys stable across edits.
4. Preview with `pipeline.py --stage preview` after meaningful changes. Early previews catch tables or equations that may require a different presentation.
5. Once the argument stabilizes, refine layout in configuration/renderer; avoid changing scientific wording to make a page fit.
6. Rebuild, render all requested variants, inspect every page, review sources and record actual review scope. `pipeline.py --stage release` checks file/evidence/record consistency.
7. Have the author accept scientific judgments and remaining limits.

## Why the alternatives are conditional
A single Python script embedding an entire new paper mixes reasoning, escaping, source content and formatting. It is hard to revise locally and cannot justify claims. It remains useful for a small, already verified report or a fixed data-driven template.

Writing the whole paper before ever rendering separates intellectual work from layout, but delays discovery of impossible tables, poor equation presentation or unreadable figures. Preview periodically; do detailed pagination later.

Structured content reduces context size, enables small diffs and avoids executing prose as code. It does not itself prevent hallucinations; the claim-to-evidence relationship and review are still required.

Keep a collaborator's Word source or a journal's LaTeX template when migration has no clear benefit. Citation-manager/native Word workflows and Markdown+Pandoc are valid alternatives. Native LaTeX editing should use the host compiler when available. The scientific method is separate from the renderer.

## Existing source migration
Archive source and outputs; map paragraphs, figures and references; build a text-equivalent prototype; compare omissions, equations and source claims; ask only about consequential ambiguities. Convert legacy Python evidence assumptions to explicit bindings before calling a build release-ready.

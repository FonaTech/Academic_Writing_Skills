# Case 07: rewriting many paragraphs without changing a fact

A method study for any large rewrite of an existing manuscript: a style pass, an AI-rate pass, a tone change requested by a supervisor, or a shortening. It was developed over several passes on a long bilingual manuscript built from a structured source, and it applies equally to LaTeX or Markdown sources.

## The risk
A fluent rewrite can drop a qualifier ("about", "up to", "estimated"), move a citation to the wrong clause, merge two conditions into one, or change a number while "smoothing" it. A reader cannot see these errors, because the new sentence reads well. Translating the rewrite into the second language doubles the chances.

## The method
1. **Archive first.** Copy every source file, the builder and the notes into a dated archive folder before the first edit of a pass.
2. **Write edits as data records.** Each edit is a record: block id, exact old text, new text, and the same pair for the second language. Small edits replace one sentence; a whole-paragraph rewrite uses a marker for "replace the block". Prefix and suffix markers rewrite only the opening or the closing of a block.
3. **Guard each block mechanically.** Before writing, compare the old and new block on:
   - the multiset of numbers (with their units and qualifiers where the checker can parse them);
   - the citation keys and their order of first appearance;
   - float references (figures, tables, equations, sections);
   - parity between the two languages: the same numbers, keys and references in each.
   A single mismatch rejects the whole batch, and nothing is written. All or nothing keeps the source consistent.
4. **Dry-run, then apply.** The dry run prints each guarded block and the reason for any rejection. Apply only after a clean dry run.
5. **Move applied edit files aside.** A file that has been applied goes into an `_applied/` folder, so that running the pass again cannot apply it twice.
6. **Rebuild and check.** Run the builder and the checker. Run the prose linter and compare its profile with the previous version: sentence count, median and maximum length, connective rate, number-sentence share.
7. **Render and look.** Export the built documents to PDF and inspect the pages that changed: headings, overviews, tables that continue across pages, equations.
8. **Record the pass.** The revision notes list the blocks changed, the tool files, the archive path, the before and after profile, and anything the guards caught.

## Failures the guards are built for
- A rewritten sentence that drops one of two citations.
- A number written as a word in one language ("two") and as a digit in the other.
- A merged sentence in which a condition moves from one value to another.
- A rewrite that splits one study's result over two sentences and cites only one of them.

Each of these survives a careful read. The guards do not catch everything: an abbreviation added to a note's definition list that the table never uses passes every number and key check, and only a read of the built table finds it.

## Edits that change facts
Some edits change facts on purpose: a correction against the source, a value read from a figure, a new citation. Make these in a separate, named edit set with the source page recorded, and never in the same batch as style edits. The revision notes report them as fact corrections, not as rewording.

## Transfer to other settings
| Setting | Block id | Guard |
|---|---|---|
| structured source (JSON, YAML) | paragraph key | as above |
| LaTeX | label or paragraph hash | numbers, `\cite` keys, `\ref` targets |
| Word document from co-authors | paragraph index after a frozen export | numbers and citation fields; compare tracked changes |
| rebuttal revision | comment id plus manuscript location | every promised change exists in the rebuilt text |
| length variants | the same block id in every variant | facts identical across variants, wording free |

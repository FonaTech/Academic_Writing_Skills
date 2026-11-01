# Migrating an existing manuscript

Migrate only when repeated generation or coordinated variants justify it. A small Word edit need not migrate.

1. Archive the current authoritative document, generator, figures and bibliography. Identify collaborators' edits and reconcile them.
2. Extract or copy paragraphs, headings, equations, tables and captions. Preserve order and stable block IDs in content.json and section files; optional paragraph Markdown files carry prose.
3. Map old reference numbers to verified keys and replace manual figure/equation numbers with markup. Check mappings against the actual supporting claim.
4. Check reference identity and publication version through the applicable registry or primary source. Follow the venue's date and citation convention; preserve online/issue-date distinctions where relevant.
5. Bind consequential claims to checked literature, raw data or explicit calculations, including units, objects, conditions and scope. Keep unknowns pending.
6. Rebuild and compare old/new prose, equations, tables, captions and figures. Review semantic changes explicitly.
7. Render and inspect all requested pages. Fix source/configuration, not regenerated output files. Archive the reviewed version and record remaining limits.

Trusted legacy Python content remains supported via source.format=python. Importing it executes code; externally supplied Python must be reviewed before use. Do not import untrusted content merely to extract text.

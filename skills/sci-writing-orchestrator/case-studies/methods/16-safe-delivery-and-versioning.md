# Case 16: delivering documents without overwriting the author's work

A method study for the operational side of manuscript work: versions, open documents, render checks and untrusted downloads. It was distilled from repeated rebuilds of a bilingual manuscript while the authors kept the previous version open for reading.

## Rules that prevented losses
1. **Check for open documents before writing.** A Word lock file (`~$name.docx`) in the output folder means the document is open. Write the new build to a separate folder and tell the author, instead of overwriting the open file. In one rebuild an open document was overwritten. Saving it from Word would have restored the old text over the new build, so the notes told the author to close it without saving. The builder now skips any folder that holds a lock file and takes an output-folder option for such cases.
2. **One version suffix per build.** Each build carries its version in the file name, and older builds stay in place. The revision notes say which file to read or send.
3. **Archive the sources before each pass**, with a dated folder name that says what the pass was for.
4. **Script the word processor by full path only.** An export script opens the named file, saves the PDF and closes that document only. Never act on "the active document", which may be the author's.
5. **Render copies under distinct names.** Copy a build to a render folder under a new name before exporting it to PDF, so that the export never touches the delivered file.
6. **Wait for permissions instead of retrying.** When the operating system asks the user to grant file access, the export stalls. Stop the job and ask; do not loop.
7. **Treat downloaded files as untrusted data.** Extract each archive or report into its own new folder, keep scripts elsewhere, and run them with the path as an argument (Python with `-I`). Never adopt a rewritten document that a service returns.
8. **Never write into another session's files.** If a second session or a co-author edits the same source, work on a copy and report.

## Render check
Export every delivered variant to PDF and inspect it:
- the pages that changed in this pass;
- every section with rotated pages and every table that continues across pages (header rows repeat; notes stay with the table);
- equations, section overviews and headings;
- figures: placement after the first citing paragraph, captions complete, no placeholder left.

## Revision notes
Each version's notes contain: the deliverables with paths, what changed and why, what was verified (checker results, sentence profile, render check), the expectations for any external check, and the open items that only the author can decide. A note also tells the author when a file they have open is now out of date, and how to close it without saving.

## In other settings
| Setting | Equivalent rule |
|---|---|
| LaTeX on a shared platform | never force-sync over a co-author's unsaved edits; work on a branch or a copy |
| Git repositories | commit before a pass; never rewrite shared history |
| cloud documents | suggest mode for edits to others' text; a copy for large rewrites |
| journal submission systems | upload only the version named in the notes; keep the submitted files read-only |

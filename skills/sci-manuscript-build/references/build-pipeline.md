# Build and check pipeline

Draft sections independently, review claims and store them in ordered source blocks. Keep formatting in the builder/configuration. `pipeline.py --stage preview` rebuilds and checks a draft; unresolved scientific inputs are visible warnings, not a scientific pass.

Pass one establishes render order, float placement and citation/section/equation numbering from the authoritative language. Pass two produces requested Word variants and native equations through pandoc. `build_report.json` records source fingerprint, output languages and document hashes. The builder does not generate scientific prose or analyze data.

After content and displays stabilize, render the documents using an available trusted converter, inspect every page and fix source/configuration. Record actual scientific and visual review with reviewer identity and limitations. `pipeline.py --stage release` reuses an unchanged inspected build; changed sources rebuild and invalidate review. It rejects missing/stale files, evidence and review states.

A review record is an auditable attestation, not an algorithmic proof or author submission approval. Scripts cannot detect a dishonest attestation. Interpret all checks by their scope. One-click release validation is valuable only after the scientific and visual work was performed.

Do not overwrite collaborator-owned files. Keep legacy outputs separate during migration, compare text/equations/figures and archive the accepted version.

For the shipped renderer: python3 scripts/render_check.py DOCUMENT.docx --out QA --dpi 140. On macOS it exposes existing system font directories to headless fontconfig locally. Use repeated --font-dir paths on other systems or to specify fonts. Confirm fonts exist; body and heading fonts come from manuscript.json. Conversion failure exits nonzero. The default renderer does not open Word; --allow-word-app explicitly enables that fallback. Inspect original-resolution pages even when contact sheets look acceptable.

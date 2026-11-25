# Case 08: adding published panels to existing figures when the author composes

A method study for reviews, theses and perspectives that adapt panels from published papers into figures the author has already drawn. The authors chose to compose the final artwork themselves, so the deliverable was captions, text references, crops and layout drafts, never finished images.

## Order of work
1. **Decide what each new panel proves.** Each candidate panel answered one sentence of the text: the result that a reader would otherwise have to take on trust. A panel that only decorated a section was dropped.
2. **Check the licence before cropping.** Open-access papers under CC BY allow adaptation with a credit line. When a PDF printed only "Creative Commons Attribution" without a version, the caption used the usual version and the open item asked the author to confirm it on the article page. Third-party material inside a figure (stock video frames, a dataset owner's images) falls outside the paper's licence and was cropped out. A preprint was flagged so that the published version could replace it later.
3. **Crop from a high-resolution render of the source page.** Render the PDF page at high resolution, locate panel edges by blank rows and columns, and keep neither the neighbouring panel's letter nor its tick labels. Record for each crop: source figure and panel, page, caption quote, licence, file name and any part left out.
4. **Write the caption before the artwork exists.** Each new panel got one sentence in the caption with its conditions and evidence level, and every new abbreviation was defined in that caption. Every number in the caption was checked against the source caption or text, with the page.
5. **Tie the text to the figure.** The first sentence that relies on the panel cites it. When a document exists in two copies (one with the new panels, one with the existing figures only), the builder keeps or removes panel references according to each copy's panel list, so neither copy cites a panel it lacks.
6. **Give layout drafts only.** A layout file lists each slot in millimetres from the top left, the crop it takes, and the original panel letters to remove. A low-resolution preview shows the arrangement, and a note marks anything the author must fix while composing.
7. **Leave the author's artwork alone.** Final figures sit in a folder that the tools read but never write. The builder embeds whatever the author places there.

## Consistency checks that found real problems
- **Text against figure.** A sentence quoted a value from a source's text that the source's own plot did not show. Once the plot appeared in the review, the sentence was changed to the values a reader can read from the plot, and the notes recorded the discrepancy and the choice for the author.
- **Note against built table.** A table note referred to a shaded row that the built document did not shade. The note was rewritten to name the row by its content (captions-and-tables.md, rule 21). The fix was to the words, because the author had not asked for shading.
- **Layout against artwork.** A draft placed new panels over a blank margin at the bottom of an existing figure. The overlap was harmless but visible, so the layout note told the author to crop the margin or extend the background.
- **Two values for one quantity.** A caption and a body sentence gave different drive conditions for what looked like the same measurement. The source showed two different experiments, so both stayed, each tied to its own figure.

## What generalises
- Captions and references come first; artwork comes last and belongs to the author.
- Every panel, caption number and licence line traces to a page.
- Once a figure shows the data, the text states what the figure shows.
- Notes and captions describe only what the built output contains.
- Check overlaps, removed letters and blank margins on the composed layout, not on the individual crops.

## In other genres
| Genre | What changes |
|---|---|
| research article | adapted panels are rare; reused published data need permission even when redrawn, and the caption says "Adapted from" or "Data from" |
| thesis | reuse of the candidate's own published figures follows the publisher's author-reuse terms and the university's rules |
| perspective or tutorial | schematic redraws dominate; the image-model route of the figure skill applies, with disclosure where the journal allows AI drafts |
| proposal | figures are evidence of feasibility; one composite figure of preliminary data beats several decorative ones |

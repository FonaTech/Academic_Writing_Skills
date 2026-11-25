# Case 02 (template): writing a new research article from data

Illustrative workflow; adapt to the project.

1. **Intake**: target journal and article type; the main claim in one sentence; available data (measurements, statistics, simulations, datasets); figures already drawn; co-author constraints.
2. **Claim–evidence map**: list each claim of the Results and the figure panel that proves it. Drop any claim without a panel; add a control experiment where the mechanism claim lacks one.
3. **Evidence ladder**: order the Results as an evidence ladder for the field (article-architecture.md, section 1): unit or model → mechanism with control → statistics → primitive or main estimate → system, population or task (simulation labelled).
4. **Figures first**: plan four to six main figures with `sci-figure-design`; draw data panels from the raw data at print size; schematics via image-model prompts; captions with conditions and statistics.
5. **Text**: Results paragraphs one per panel group; then Introduction (need → incumbents → gap → "Here, we" with numbers); then Discussion (recap, limitations, next step); Methods with the accounting scope of every aggregate number; abstract last.
6. **Checks**: numbers in abstract, conclusion and body identical with the same qualifier; every title word tested; `check_manuscript.py`; simulated referee reports; readiness rubric.
7. **Deliver**: manuscript, SI, cover letter, data availability statement, AI-use statement if the journal requires it.

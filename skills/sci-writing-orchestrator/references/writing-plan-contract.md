# Writing plan contract

The plan is the single authority for a writing project. It is written before drafting, updated when a decision changes, and read by every agent that works on the manuscript. Keep it in the project as `workflow/writing_plan.md`; if the agent tool keeps its own plan file (for example Claude Code plan mode), copy the approved plan into `workflow/writing_plan.md` and mark its status at the top: `draft`, `current`, `stale`, `superseded`.

## Required sections

1. **Context.** What the document is, who asked for what, which files produce it (source or generator), the current version and where it is archived.
2. **Requests.** The user's requirements in their own terms, numbered (e.g. "short sentences, no AI flavour", "applications expanded with comparisons", "figures drawable by Nano Banana Pro").
3. **Inputs.** Drafts, generator code, literature folders, recordings and the decisions extracted from them, reviewer comments, reference papers to emulate.
4. **Audit findings.** Grouped as citations and attribution, numbers and scopes, structure and duplication, terminology, style profile (with measured sentence statistics), figures and tables, code defects. Each finding says what will be done.
5. **Confirmed decisions.** Answers to the design brief (structure, second language, figure split, derivations, definition of done), with the date.
6. **Target structure.** Section tree; for each section its one-sentence argument, its evidence sources and the figures, tables, boxes and equations it hosts.
7. **Evidence plan.** Source groups, extraction agents, evidence files, verification rule, abstract-only sources and how they will be marked.
8. **Figure and table plan.** Per figure: argument, panels with type (schematic/data), data sources, print size; per table: columns and notes.
9. **Implementation architecture.** Content files, builder, checker, figure kit, reference database, archive locations.
10. **Milestones.** M0 evidence … M6 independent review, with what each produces and what it depends on.
11. **Style rules for this manuscript.** Sentence targets, banned patterns, terminology table location, attribution convention, citation style.
12. **Verification.** Commands to run, what "pass" means, the rendered-page check, and the independent audit.
13. **Open questions and risks.** What the author must decide or supply (journal, AI-image policy, missing PDFs), with a default if no answer arrives.

## Update rules
- A structural change (sections merged, figures added) sets the status to `stale` until sections 6–8 are updated.
- Every milestone ends by updating the plan: what was done, what changed, what is next.
- Do not overwrite a decision silently; record the new decision and why the old one was dropped.

## Size
Long enough to execute without asking again, short enough to scan: usually 150–300 lines. Put long lists (all audit findings, all references) in attached files and link them.

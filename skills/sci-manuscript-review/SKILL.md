---
name: sci-manuscript-review
description: >
  Review scientific manuscripts against evidence/data and applicable methods, test attributions and alternatives, inspect figures and bilingual meaning, and support referee responses. 论文审查、投稿检查、审稿回复。 Report findings and uncertainty; no numeric score predicts acceptance and AI review does not replace author responsibility.
---

# Scientific manuscript review

Review the actual source, data and draft; do not evaluate plausibility from memory. Separate factual consistency, evidential support, study validity, scientific interpretation and presentation.

## Passes
- Provenance: source identity/version, complete quote/page, original data/analysis and derived calculations.
- Attribution: whether the cited study actually supports the local claim, including qualifiers and contrary evidence.
- Methods: study-type reporting, controls, population, sampling, uncertainty, analysis choices and reproducibility. Writing polish cannot repair absent experimental evidence.
- Comparisons: units, metric definitions, objects, populations/tasks, conditions and accounting scopes.
- Argument: research question, alternatives, contribution, limits and section coherence.
- Figures: source data and plotting code, exact composition integrity, readable labels and self-contained captions.
- Languages: paired blocks/cells, quantities, units, polarity, uncertainty, evidence status and reference targets.
- Delivery: built files, numbering, equations, source freshness, rendered pages and requested variants.

Use separate passes. For substantial work, an independent reviewer/agent with exact raw sources should attempt to refute serious findings; if unavailable, disclose a self-review. Multiple agents of the same model are not guaranteed independent scientific judgments.

## Findings
Report location, claim, evidence, severity, proposed repair and uncertainty. Blocking: wrong value/attribution, changed evidential image, unsupported result or invalid method inference. Major: missing conditions, unfair comparison or structural gap. Minor: presentation and terminology. Ambiguous findings remain questions with their basis.

Fix authorized issues in the authoritative source, rebuild and review changed portions. If the user requested review only, provide findings without silently rewriting. Stop only for information/approval that materially constrains the authorized action.

Automated claim audits inspect declared bindings, not semantic entailment. Build checks inspect declared outputs, not research truth. Read [audit-dimensions.md](references/audit-dimensions.md) for review scope and [readiness-rubric.md](references/readiness-rubric.md) for a non-probabilistic internal decision rubric.

For reviewer responses, preserve each comment, answer directly and link every promised change to the actual revision. Scientific disagreement needs evidence; do not invent completed experiments or author commitments.

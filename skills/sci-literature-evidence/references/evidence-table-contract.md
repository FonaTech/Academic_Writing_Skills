# Evidence record and claim binding contract v2

Keep two different things: evidence that a source/data reports, and a local manuscript claim using it. A local claim must bind a specific evidence key; equal numbers elsewhere are irrelevant.

## Evidence
Common fields: `key`, `source_kind` (`literature`, `raw_data`, `derived`), `value` as source text, `unit` (empty string for dimensionless quantities), `metric`, `entity`, `conditions`, `result_method` (`measured`, `simulated`, `estimated`, `projected`, `inferred`, `synthetic`), `source_role` (`primary`, `secondary`, `original`), `access_status` (`full-text`, `abstract-only`, `raw-files`), `verification` (`pending`, `verified`). These axes are separate, not a quality ranking. Retain uncertainty, sample definition and accounting scope when relevant.

Literature also requires `paper` (reference key), exact `source_file`, `page` integer or consecutive `pages` list, and complete verbatim `quote`. Only safe PDF typography repair is allowed. Do not remove decimal points/signs or truncate the quote to get a match. Abstract-only evidence is labeled and does not establish details omitted from the abstract.

Original/derived evidence requires `provenance.artifacts` (`path` and SHA-256), `provenance.locator` (row/column, run/output field, etc.), and the actual method/code/environment. Derived evidence also has `provenance.formula` and `provenance.inputs` (evidence keys). Hashes prove file identity, not analytical correctness; rerun or inspect the analysis.

## Local claim
A paragraph/caption has `claims`; a table stores claims by `cell_claims["row:column"]`. Each claim contains `evidence_key`, `value`, `unit`, `metric`, `entity`, `result_method`, and `text` with an exact anchor for each requested language. The anchor includes the supported statement and its citation for literature. Every used condition/scope must be consistent with its evidence; reviewers check this semantic relationship.

```json
{
  "id": "p_result",
  "type": "para",
  "status": "reviewed",
  "en": "[verified result text with source citation]",
  "claims": [{
    "evidence_key": "study.metric.condition",
    "value": "<source value>",
    "unit": "<unit>",
    "metric": "<same metric as evidence>",
    "entity": "<same population/object as evidence>",
    "result_method": "measured",
    "text": {"en": "<exact local statement including its citation>"}
  }]
}
```

This is a format example, not a scientific result. Nonquantitative literature claims still require source review and can use qualitative claim records. Authors' interpretations must state premises, reasoning, limits and alternative explanations. No published source page is required for an original result with checkable raw-data provenance.

## Validation limits
Quote matching, identity and quantitative bindings are distinct. The scripts check complete quoted text, required fields, known artifacts and declared metadata. They cannot prove that a study is valid or a sentence entails the reported result. Record actual source/data review before setting verified. Legacy `exp_or_sim` records require migration into the separate axes before release validation.

Synthetic identifies artificial test/example data, not an experiment or a physical simulation. Label synthetic status prominently in the manuscript and provenance; do not reclassify it to make a release check pass. Claims repeat evidence conditions/accounting_scope when those fields are declared; exact anchor text plus review must confirm the wording carries those limits.

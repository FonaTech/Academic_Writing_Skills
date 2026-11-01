# Review dimensions

Verify local claims against exact sources, data and derived calculations. Separate wrong reported facts from weak scientific support. Examine study design, controls, sampling, uncertainty, alternative explanations and reproducibility using discipline-appropriate criteria. Do not infer these from journal reputation.

For comparisons check objects/populations, conditions, metric definitions, units and accounting scope. For displays inspect data, code, file integrity, meaningful scales/statistics and labels. For translations compare cells and blocks, including polarity and causal strength. For construction inspect source freshness, artifacts, citations, equations and rendered pages.

Automated quantitative binding pass:
```bash
python3 scripts/audit_numbers.py --project PROJECT --release --json
```

This checks declared relationships. An independent source-based semantic/methods review is still required. Report reviewer identity, coverage, limitations and unresolved findings.

## Twelve review dimensions
| Dimension | Check |
|---|---|
| D1 Quantities | Exact value, sign, precision, units, uncertainty, conditions and scope against the local record/source. |
| D2 Attribution | The cited source supports this claim; primary/secondary and access states are explicit. |
| D3 Evidence and methods | Study design, data/analysis provenance, controls, alternatives and reporting standards. |
| D4 Comparisons | Same metric, object/population, task, denominator and included overheads. |
| D5 Structure | Section questions, argument dependencies, synthesis and contribution. |
| D6 Prose | Linked precise sentences, justified qualifications, no hype or empty process commentary. |
| D7 Terms | Stable spelling, technical meaning, symbols and first-use/caption definitions. |
| D8 Figures and tables | Sourced values, appropriate scales, exact final-panel integrity, labels and permissions. |
| D9 Languages | Block/cell semantics, polarity, direction, quantities, units and citation parity. |
| D10 Build | Source freshness, requested outputs, equations, references, numbering and rendered pages. |
| D11 Voice | Field synthesis for narrative reviews; protocol/search/appraisal reporting for systematic/scoping work. |
| D12 Variants | Every requested variant contains the current facts, qualifiers, citations and matching artwork labels. |

Mark inapplicable dimensions explicitly. Findings include exact location, source basis, severity, repair and unresolved ambiguity. A completed checklist is not human expert endorsement or an acceptance probability.

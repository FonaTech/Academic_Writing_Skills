# Review dimensions

Verify local claims against exact sources, data and derived calculations. Separate wrong reported facts from weak scientific support. Examine study design, controls, sampling, uncertainty, alternative explanations and reproducibility using discipline-appropriate criteria. Do not infer these from journal reputation.

For comparisons check objects/populations, conditions, metric definitions, units and accounting scope. For displays inspect data, code, file integrity, meaningful scales/statistics and labels. For translations compare cells and blocks, including polarity and causal strength. For construction inspect source freshness, artifacts, citations, equations and rendered pages.

Automated quantitative binding pass:
```bash
python3 scripts/audit_numbers.py --project PROJECT --release --json
```

This checks declared relationships. An independent source-based semantic/methods review is still required. Report reviewer identity, coverage, limitations and unresolved findings.

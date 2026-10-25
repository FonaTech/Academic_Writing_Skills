# Parallel audit recipe

For long manuscripts, run the audit dimensions as parallel sub-agents, then verify every blocking and major finding with an independent refuter. This works with any agent tool that can spawn sub-agents (Claude Code Agent/Workflow tools, Codex sub-agents, OpenCode task agents). Where sub-agents are unavailable, run the same prompts one after another.

## 1 Inputs each agent receives
- manuscript source (`content.py`, `floats.py`) or the built `.docx`
- evidence files (`evidence/*.json`) and the page-marked source texts (`source_audit/*.txt`)
- `references.json` and `build_report.json`
- the dimension brief from `audit-dimensions.md`
- the finding schema:

```json
{"id": "", "dimension": "", "severity": "blocking|major|minor", "location": "", "claim": "",
 "evidence": "file, page, verbatim quote", "verdict": "", "fix": "", "confidence": "high|medium|low"}
```

## 2 Fan-out
| Agent | Scope |
|---|---|
| numbers-A, numbers-B | D1 for the first and second half of the sections |
| attribution-A, attribution-B | D2 for the same halves |
| levels-fairness | D3 and D4 across all tables, captions and comparison sentences |
| structure | D5 against the plan and the reference reviews |
| style-terms | D6 and D7 (runs `prose_lint.py`, reads the terminology table) |
| floats | D8 (runs `figure_kit.py verify`, reads captions and panel data) |
| bilingual | D9 block by block |
| references | D10 (reads `references_verified.json`, checks unused and duplicate keys) |
| voice | D11 screening wording, per-paper fault-finding, defensive sentences, endings |
| variants | D12 every fix in every length variant and language; budgets; full tables |

## 3 Verification
For each blocking or major finding, spawn a refuter with only the finding and the source paths: "Try to show this finding is wrong, citing the source." Keep findings the refuter cannot refute; keep ambiguous ones and mark them "check".

## 4 Synthesis
Deduplicate by location and claim, sort by severity, attach the fix, and compute the readiness score (`readiness-rubric.md`). Report the counts per dimension and anything that was not checked (for example sources without full text).

## 5 Apply
After the user accepts the report: edit the source, rebuild, re-run `check_manuscript.py`, `audit_numbers.py` and `prose_lint.py`, and record every change in the revision notes.

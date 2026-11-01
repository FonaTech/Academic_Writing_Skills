# Synthetic smoke demonstration for 2.1.0

This is a complete runnable test project rebuilt with the 2.1.0 kit from packaged artificial CSV records. It is not empirical research and was not supplied as a real dataset in this user task. EN/ZH output files and a current source/document-bound review record are included. The review identifies the AI maintainer and its sequential self-review; no independent human or expert approval occurred. Human author acceptance remains pending.

The means, counts, difference, raw-file hashes and explicit claim bindings were inspected. Each final EN/ZH document was rendered to one PDF page and the final page PNGs were opened; Chinese fonts required system font discovery in the validation environment. No visual clipping/overlap was observed in the final pages.

To check this snapshot, run python3 pipeline.py --stage release inside this directory with core dependencies. To rebuild, run python3 analysis/summarize.py, python3 analysis/provenance.py and python3 pipeline.py --stage preview. Then render and inspect the new documents and record actual fresh reviews before release. A new build can invalidate the prior DOCX hashes even if the text looks unchanged.

WithCitations is the standard output variant name; this artificial example has zero references, no scientific citations, no figures and no display equations. The data support descriptive arithmetic only, no causal effect, real-world conclusion or inferential significance. The sixteen case-bank scenarios remain hypothetical and unexecuted.

#!/usr/bin/env python3
"""Re-find every evidence quote on its stated page and check that the value is in the quote.

Usage
  verify_evidence_quotes.py EVIDENCE.json [EVIDENCE2.json ...] --text-dir source_audit/ [--fix-pages] [--strict]

Evidence files are either {key: record} or [record, ...]. A record needs
  quote, source_file (or text / paper), page (or page_reported), and ideally value.

Matching normalises ligatures, soft hyphens, line-break hyphenation, dashes, quotes,
control characters and whitespace. A quote found on a different page is reported with
the correct page (and fixed with --fix-pages). Exit code 1 if any quote is missing.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

LIG = {'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl', 'ﬃ': 'ffi', 'ﬄ': 'ffl', '­': '',
       '‐': '-', '‑': '-', '‒': '-', '–': '-', '—': '-', '−': '-',
       '‘': "'", '’': "'", '“': '"', '”': '"', ' ': ' ', ' ': ' ',
       ' ': ' ', '×': 'x', 'µ': 'u', 'μ': 'u'}


def norm(text: str) -> str:
    text = text or ''
    text = re.sub(r'\u00ad\s*', '', text)                     # soft hyphen at a line break
    for a, b in LIG.items():
        text = text.replace(a, b)
    text = re.sub(r'[\x00-\x08\x0b-\x1f]', ' ', text)
    text = re.sub(r'(\w)-\s*\n\s*(\w)', r'\1\2', text)      # line-break hyphenation
    text = re.sub(r'(\w)- (\w)', r'\1\2', text)                # already-collapsed hyphenation
    return re.sub(r'\s+', ' ', text).strip().lower()


def squash(text: str) -> str:
    """Letters and digits only: tolerant of hyphenation, spacing and punctuation, strict on words and numbers."""
    return re.sub(r'[^0-9a-z]+', '', text)


def pages_of(path: Path) -> dict[int, str]:
    raw = path.read_text(encoding='utf-8', errors='replace')
    parts = re.split(r'=== PAGE (\d+) ===', raw)
    pages = {}
    for i in range(1, len(parts) - 1, 2):
        pages[int(parts[i])] = norm(parts[i + 1])
    if not pages:
        pages[1] = norm(raw)
    return pages


def records(data):
    if isinstance(data, dict):
        if 'papers' in data and isinstance(data['papers'], list):     # mining batch format
            for paper in data['papers']:
                for ex in paper.get('exemplars', []) + paper.get('antipatterns', []):
                    rec = dict(ex)
                    rec.setdefault('source_file', paper.get('text') or paper.get('id'))
                    rec.setdefault('key', f"{paper.get('id')}:{ex.get('category', 'anti')}:{ex.get('page')}")
                    yield rec['key'], rec
            return
        for key, rec in data.items():
            if isinstance(rec, dict):
                yield key, rec
    elif isinstance(data, list):
        for i, rec in enumerate(data):
            yield rec.get('key', str(i)), rec


def resolve_text(rec, text_dir: Path):
    for field in ('source_file', 'text', 'paper', 'id'):
        name = rec.get(field)
        if not name:
            continue
        for cand in (Path(name), text_dir / name, text_dir / f'{name}.txt'):
            if cand.exists() and cand.is_file():
                return cand
        hits = sorted(text_dir.glob(f'{Path(str(name)).stem}*.txt'))
        if hits:
            return hits[0]
    return None


def value_tokens(value) -> list[str]:
    if value is None:
        return []
    toks = re.findall(r'\d+(?:[.,]\d+)?', str(value))
    return [t.replace(',', '.') for t in toks][:3]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('files', nargs='+')
    ap.add_argument('--text-dir', default='source_audit')
    ap.add_argument('--fix-pages', action='store_true', help='rewrite page numbers that were off')
    ap.add_argument('--strict', action='store_true', help='also fail when the value is not in the quote')
    args = ap.parse_args(argv)
    text_dir = Path(args.text_dir)
    cache: dict[Path, dict[int, str]] = {}
    totals = dict(ok=0, moved=0, missing=0, novalue=0, nosource=0)
    failed = False
    for file in args.files:
        path = Path(file)
        data = json.loads(path.read_text(encoding='utf-8'))
        changed = False
        for key, rec in records(data):
            quote = rec.get('quote')
            if not quote:
                continue
            src = resolve_text(rec, text_dir)
            if src is None:
                totals['nosource'] += 1
                print(f'NOSOURCE {path.name}:{key}')
                failed = True
                continue
            pages = cache.setdefault(src, pages_of(src))
            q = norm(quote)
            probe = q if len(q) < 160 else q[:160]
            page = rec.get('page', rec.get('page_reported'))
            try:
                page = int(page) if page is not None else None
            except (TypeError, ValueError):
                page = None
            found = [p for p, t in pages.items() if probe in t]
            if not found:
                sq = squash(probe)
                found = [p for p, t in pages.items() if sq and sq in squash(t)]
            if not found:
                # tolerate a quote that runs over a page break
                joined = squash(' '.join(pages[p] for p in sorted(pages)))
                found = [None] if squash(probe) in joined else []
            if not found:
                totals['missing'] += 1
                failed = True
                print(f'MISSING  {path.name}:{key}  (p{page})  "{quote[:90]}"')
                continue
            if page is not None and found[0] is not None and page not in found:
                totals['moved'] += 1
                print(f'PAGE     {path.name}:{key}  stated p{page}, found p{found[0]}')
                if args.fix_pages:
                    rec['page' if 'page' in rec else 'page_reported'] = found[0]
                    changed = True
            else:
                totals['ok'] += 1
            vals = value_tokens(rec.get('value'))
            if vals and not any(v in q.replace(',', '.') for v in vals):
                totals['novalue'] += 1
                print(f'VALUE    {path.name}:{key}  value {rec.get("value")!r} not in quote')
                if args.strict:
                    failed = True
        if changed:
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
            print(f'rewrote page numbers in {path}')
    print('\n' + ', '.join(f'{k} {v}' for k, v in totals.items()))
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
"""List numbers in manuscript text that no evidence record supports.

Usage
  audit_numbers.py content.py [floats.py] --evidence evidence/*.json [--json]
  audit_numbers.py draft.docx --evidence source_audit/evidence_*.json

For every paragraph (or table cell and caption) the script extracts quantitative tokens
(numbers with units, percentages, ranges, multipliers, scientific notation) and looks for
each value in the 'value' and 'quote' fields of the evidence files. Values found nowhere
are reported with their paragraph id and the sentence around them, so a reviewer can check
them first. Model constants, section numbers, years and small integers are ignored.
"""
from __future__ import annotations

import argparse
import glob
import importlib.util
import json
import re
import sys
from pathlib import Path

QTY = re.compile(
    r'(?<![\w.])(?:\d+(?:\.\d+)?\s?[×x]\s?10\s?\^?\{?[−-]?\d+\}?|\d+(?:\.\d+)?(?:\s?[–-]\s?\d+(?:\.\d+)?)?)'
    r'(?:\s?(?:%|×|fold|[kMGTPµunpfa]?(?:mol|min|ppm|ppb|bits?|OPS|eV|Hz|Pa|Gy|Bq|dB|°C|yr|m|g|L|M|V|A|W|J|s|h|d|Ω|S|F|b|B|K)(?:\s?[−-]?\d)?'
    r'(?:\s?(?:W|L|g|kg|mm|cm|µm|m|s|h|V|mol)\s?\^?[−-]?\d?)?))?')
SKIP_CONTEXT = re.compile(r'(Section|Chapter|Fig\.|Figure|Table|Box|equation|eq\.|ref\.|refs)\s*$', re.I)


def norm_num(tok: str) -> str:
    t = tok.replace('−', '-').replace(' ', '').replace(',', '')
    m = re.match(r'(\d+(?:\.\d+)?)', t)
    return m.group(1) if m else t


def load_evidence(patterns):
    values, quotes = set(), []
    for pat in patterns:
        for f in glob.glob(pat):
            data = json.loads(Path(f).read_text(encoding='utf-8'))
            items = data.values() if isinstance(data, dict) else data
            for rec in items:
                if not isinstance(rec, dict):
                    continue
                for field in ('value', 'quote', 'notes'):
                    text = str(rec.get(field, ''))
                    quotes.append(text)
                    for m in re.finditer(r'\d+(?:\.\d+)?', text.replace(',', '')):
                        values.add(m.group(0))
    return values, ' '.join(quotes)


def load_text(path: Path):
    """Yield (location, text) from content.py/floats.py modules or a .docx file."""
    if path.suffix == '.docx':
        from docx import Document
        doc = Document(path)
        for i, p in enumerate(doc.paragraphs, 1):
            if p.text.strip():
                yield f'¶{i}', p.text
        for ti, t in enumerate(doc.tables, 1):
            for ri, row in enumerate(t.rows):
                for ci, cell in enumerate(row.cells):
                    yield f'T{ti}r{ri}c{ci}', cell.text
        return
    sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    for b in getattr(mod, 'BLOCKS', []):
        if b.get('type') == 'para':
            yield b['id'], b.get('en', '')
        elif b.get('type') == 'box':
            for i, it in enumerate(b.get('items', [])):
                if it.get('type') == 'para':
                    yield f"{b['id']}.{i}", it.get('en', '')
    for key, fig in getattr(mod, 'FIGURES', {}).items():
        yield f'fig:{key}', fig.get('caption_en', '')
    for key, tab in getattr(mod, 'TABLES', {}).items():
        for ri, row in enumerate(tab.get('rows_en', [])):
            for ci, cell in enumerate(row):
                yield f'tab:{key}:r{ri}c{ci}', str(cell)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('sources', nargs='+', help='content.py, floats.py or .docx')
    ap.add_argument('--evidence', nargs='+', required=True)
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args(argv)
    values, _ = load_evidence(args.evidence)
    unsupported, seen = [], set()
    for src in args.sources:
        for loc, text in load_text(Path(src)):
            clean = re.sub(r'\[@[^\]]+\]|\{(fig|tab|eq|sec|box):[^}]+\}|\$[^$]*\$', ' ', text)
            for m in QTY.finditer(clean):
                tok = m.group(0).strip()
                num = norm_num(tok)
                if not num or not re.search(r'\d', num):
                    continue
                try:
                    val = float(num)
                except ValueError:
                    continue
                before = clean[max(0, m.start() - 12):m.start()]
                if SKIP_CONTEXT.search(before) or (val.is_integer() and val < 10 and not re.search(r'[%a-zA-Zµ×]', tok[len(num):])):
                    continue
                if 1900 <= val <= 2100 and val.is_integer():
                    continue
                if num in values or num.rstrip('0').rstrip('.') in values:
                    continue
                cut = max(clean.rfind('. ', 0, m.start()), clean.rfind('; ', 0, m.start()))
                s = cut + 2 if cut != -1 else 0
                e = clean.find('. ', m.end())
                sentence = clean[s:e + 1 if e != -1 else None].strip()
                if (loc, tok) in seen:
                    continue
                seen.add((loc, tok))
                unsupported.append({'where': loc, 'value': tok, 'sentence': ' '.join(sentence.split())[:220]})
    if args.json:
        print(json.dumps(unsupported, ensure_ascii=False, indent=2))
    else:
        for u in unsupported:
            print(f"{u['where']:22s} {u['value']:>14s}   {u['sentence']}")
        print(f'\n{len(unsupported)} quantities without a matching evidence value '
              f'(check each: model constant, derived value, or missing source).')
    return 0


if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
"""Validate full evidence quotes on stated PDF pages; fail on absent fields or mismatches.

No punctuation-stripping fallback is used. --strict is accepted for compatibility;
value checks are always enabled. --fix-pages repairs only a uniquely located full quote.
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from evidence_tools import norm, pages_of, iter_records, resolve_text, verify_quote

# Legacy provenance helpers now retain numerical punctuation.
squash = norm
records = iter_records

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('files', nargs='+')
    ap.add_argument('--text-dir', default='source_audit')
    ap.add_argument('--strict', action='store_true', help='compatibility option; checks are strict by default')
    ap.add_argument('--fix-pages', action='store_true')
    args = ap.parse_args(argv)
    checked, failed = 0, 0
    for filename in args.files:
        path = Path(filename)
        data = json.loads(path.read_text(encoding='utf-8'))
        changed = False
        for key, rec in iter_records(data):
            checked += 1
            errors = verify_quote(rec, args.text_dir)
            if errors and args.fix_pages and rec.get('quote'):
                src = resolve_text(rec, args.text_dir)
                found = [p for p, t in pages_of(src).items() if norm(rec['quote']) in t] if src else []
                if len(found) == 1 and not ('papers' in data if isinstance(data, dict) else False):
                    rec['page'] = found[0]
                    rec.pop('pages', None)
                    rec.pop('page_reported', None)
                    errors = verify_quote(rec, args.text_dir)
                    changed = True
                    print(f'REPAIRED {key}: page {found[0]} (review this edit)')
            if errors:
                failed += 1
                print(f'FAIL {path.name}:{key}: ' + '; '.join(errors))
            else:
                print(f'OK {path.name}:{key}')
        if changed:
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'{checked} records checked, {failed} failed')
    return 1 if failed or checked == 0 else 0

if __name__ == '__main__':
    sys.exit(main())

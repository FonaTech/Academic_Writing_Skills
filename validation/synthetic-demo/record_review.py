#!/usr/bin/env python3
"""Record an actual review, its reviewer and limits; this does not perform the review."""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from project_source import fingerprint
from evidence_tools import sha256

HERE = Path(__file__).resolve().parent

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--kind', choices=['scientific_review','visual_review'], required=True)
    ap.add_argument('--reviewed-by', required=True, help='name/role; identify an AI reviewer as AI')
    ap.add_argument('--notes', required=True, help='what was inspected and what remains outside that check')
    args = ap.parse_args(argv)
    cfg = json.loads((HERE/'manuscript.json').read_text(encoding='utf-8'))
    report = json.loads((HERE/'build_report.json').read_text(encoding='utf-8'))
    current = fingerprint(HERE,cfg)
    if report.get('source_fingerprint') != current or not report.get('documents'):
        ap.error('build is absent or stale; rebuild and inspect first')
    for name,digest in report['documents'].items():
        if not (HERE/name).is_file() or sha256(HERE/name) != digest:
            ap.error('documents changed or are missing; rebuild and inspect first')
    path = HERE/'review_record.json'
    data = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
    if data.get('source_fingerprint') != current or data.get('documents') != report['documents']:
        data = {}
    data.update(source_fingerprint=current,documents=report['documents'])
    data[args.kind] = dict(status='passed',reviewed_by=args.reviewed_by,notes=args.notes)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Review scope recorded. Author responsibility and submission approval remain with the author.')
    return 0

if __name__ == '__main__':
    sys.exit(main())

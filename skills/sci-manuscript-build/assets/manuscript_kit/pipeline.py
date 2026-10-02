#!/usr/bin/env python3
"""Build previews or validate an already inspected release; never auto-attest review."""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from pathlib import Path
from project_source import fingerprint

HERE = Path(__file__).resolve().parent

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--stage', choices=['preview','release'], default='preview')
    args = ap.parse_args(argv)
    cfg = json.loads((HERE/'manuscript.json').read_text(encoding='utf-8'))
    report_path = HERE/'build_report.json'
    fresh = report_path.exists() and json.loads(report_path.read_text()).get('source_fingerprint') == fingerprint(HERE,cfg)
    if args.stage == 'preview' or not fresh:
        result = subprocess.run([sys.executable,str(HERE/'build_manuscript.py')],cwd=HERE)
        if result.returncode:
            return result.returncode
    command = [sys.executable,str(HERE/'check_manuscript.py')]
    if args.stage == 'release':
        command.append('--release')
    return subprocess.run(command,cwd=HERE).returncode

if __name__ == '__main__':
    sys.exit(main())

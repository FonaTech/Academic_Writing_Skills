#!/usr/bin/env python3
"""Check plugin metadata mirrors, or restore hidden metadata after a browser upload."""
from __future__ import annotations
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='copy visible metadata into .claude-plugin/')
    args = parser.parse_args(argv)
    issues = []
    for name in ('plugin.json', 'marketplace.json'):
        visible = ROOT/'claude-plugin'/name
        hidden = ROOT/'.claude-plugin'/name
        if args.write:
            hidden.parent.mkdir(exist_ok=True)
            hidden.write_bytes(visible.read_bytes())
        if not hidden.is_file() or hidden.read_bytes() != visible.read_bytes():
            issues.append(name)
    if issues:
        print('Plugin metadata missing or out of sync: '+', '.join(issues))
        print('Review claude-plugin/*.json, then run this script with --write.')
        return 1
    print('Hidden plugin metadata matches visible upload mirrors.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())

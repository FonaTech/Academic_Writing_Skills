#!/usr/bin/env python3
"""Write/check a complete release SHA256 manifest, including hidden plugin metadata."""
from __future__ import annotations
import argparse
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = 'SHA256SUMS.txt'

def release_files(root):
    for path in sorted(root.rglob('*')):
        relative = path.relative_to(root)
        if relative.parts[0] in {'.git','work','outputs','provenance'}:
            continue
        if any(part in {'__pycache__','.pytest_cache','.academic-writing-backups','.DS_Store'} for part in relative.parts):
            continue
        if path.name == '.installed-from' or path.suffix == '.pyc' or '.bak' in path.name:
            continue
        if path.is_file() and relative.as_posix() != MANIFEST:
            yield relative.as_posix(), path

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='rewrite the manifest after intentional release changes')
    args = parser.parse_args(argv)
    actual = {name:hashlib.sha256(path.read_bytes()).hexdigest() for name,path in release_files(ROOT)}
    manifest = ROOT/MANIFEST
    if args.write:
        manifest.write_text(''.join(f'{digest}  {name}\n' for name,digest in actual.items()), encoding='utf-8')
        print(f'Wrote {len(actual)} file hashes.')
        return 0
    if not manifest.is_file():
        print('SHA256SUMS.txt is missing.');return 1
    expected = {}
    for line in manifest.read_text(encoding='utf-8').splitlines():
        digest,name = line.split('  ',1)
        expected[name]=digest
    missing = sorted(expected.keys()-actual.keys())
    extra = sorted(actual.keys()-expected.keys())
    changed = sorted(name for name in expected.keys()&actual.keys() if expected[name]!=actual[name])
    for label,names in [('MISSING',missing),('UNLISTED',extra),('CHANGED',changed)]:
        for name in names: print(label,name)
    print(f'{len(actual)} files checked: {len(missing)+len(extra)+len(changed)} integrity issues.')
    return int(bool(missing or extra or changed))

if __name__ == '__main__':
    raise SystemExit(main())

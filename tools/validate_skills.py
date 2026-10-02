#!/usr/bin/env python3
"""Validate the skill suite for Claude Code, Codex and OpenCode.

Checks
  - SKILL.md frontmatter: only name, description, license, allowed-tools, metadata; name is hyphen-case,
    <= 64 chars and equals the folder name (OpenCode requires this); description <= 1024 chars, no angle brackets
  - every relative link and every `references/`, `scripts/`, `presets/`, `case-studies/`, `assets/` path named
    in SKILL.md and in reference files exists
  - agents/openai.yaml: display_name, short_description (25-64 chars), default_prompt mentioning $skill-name
  - every Python script compiles; scripts with a main() answer --help without error
  - plugin manifests list every skill
Exit code 1 on any error.
"""
from __future__ import annotations

import json
import py_compile
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
SKILLS = REPO / 'skills'
ALLOWED = {'name', 'description', 'license', 'allowed-tools', 'metadata'}
errors, warnings = [], []


def check_frontmatter(skill: Path):
    text = (skill / 'SKILL.md').read_text(encoding='utf-8')
    m = re.match(r'^---\n(.*?)\n---\n', text, re.S)
    if not m:
        errors.append(f'{skill.name}: SKILL.md has no frontmatter')
        return text
    fm = yaml.safe_load(m.group(1))
    extra = set(fm) - ALLOWED
    if extra:
        errors.append(f'{skill.name}: unexpected frontmatter keys {sorted(extra)}')
    name, desc = fm.get('name', ''), fm.get('description', '')
    if name != skill.name:
        errors.append(f'{skill.name}: name "{name}" differs from folder name')
    if not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', name or '') or len(name) > 64:
        errors.append(f'{skill.name}: name is not hyphen-case or too long')
    if not desc or len(desc) > 1024 or '<' in desc or '>' in desc:
        errors.append(f'{skill.name}: description missing, over 1024 chars or contains angle brackets')
    lines = text.count('\n')
    if lines > 500:
        warnings.append(f'{skill.name}: SKILL.md has {lines} lines; move detail into references')
    return text


def check_integrity(skill: Path):
    """Every Markdown file: no truncation markers, balanced code fences, relative links resolve."""
    for md in sorted(skill.rglob('*.md')):
        text = md.read_text(encoding='utf-8')
        rel = md.relative_to(skill)
        if re.search(r'\[truncated \d+ chars\]', text):
            errors.append(f'{skill.name}: {rel} contains a truncation marker')
        if text.count('```') % 2:
            errors.append(f'{skill.name}: {rel} has an unclosed code fence')
        if md.name != 'SKILL.md' and md.parent.name != 'references':
            check_paths(skill, text, str(rel))


def check_paths(skill: Path, text: str, origin: str):
    for link in re.findall(r'\]\(([^)#\s]+)\)', text):
        if link.startswith(('http', 'mailto:')):
            continue
        if not (skill / link).exists() and not (skill / Path(origin).parent / link).exists():
            errors.append(f'{skill.name}: {origin} links to missing {link}')
    for rel in re.findall(r'`((?:references|scripts|presets|case-studies|assets|agents)/[A-Za-z0-9_./-]+)`', text):
        rel = rel.rstrip('/.')
        if '<' in rel or '*' in rel:
            continue
        if not (skill / rel).exists():
            errors.append(f'{skill.name}: {origin} names missing path {rel}')


def check_agents(skill: Path):
    path = skill / 'agents' / 'openai.yaml'
    if not path.exists():
        warnings.append(f'{skill.name}: no agents/openai.yaml')
        return
    data = yaml.safe_load(path.read_text(encoding='utf-8')) or {}
    ui = data.get('interface', {})
    for key in ('display_name', 'short_description', 'default_prompt'):
        if not ui.get(key):
            errors.append(f'{skill.name}: openai.yaml lacks interface.{key}')
    if ui.get('short_description') and not 25 <= len(ui['short_description']) <= 64:
        errors.append(f'{skill.name}: short_description must be 25-64 chars')
    if ui.get('default_prompt') and f'${skill.name}' not in ui['default_prompt']:
        errors.append(f'{skill.name}: default_prompt must mention ${skill.name}')


def check_scripts(skill: Path):
    for py in sorted(skill.rglob('*.py')):
        if '__pycache__' in py.parts:
            continue
        try:
            with tempfile.TemporaryDirectory() as td:
                py_compile.compile(str(py), doraise=True, cfile=str(Path(td) / 'x.pyc'))
        except py_compile.PyCompileError as exc:
            errors.append(f'{skill.name}: {py.relative_to(skill)} does not compile: {exc.msg}')
            continue
        src = py.read_text(encoding='utf-8')
        if 'argparse' in src and "__name__ == '__main__'" in src and 'scripts' in py.parts:
            r = subprocess.run([sys.executable, str(py), '--help'], capture_output=True, text=True, timeout=60,
                               cwd=str(py.parent))
            if r.returncode not in (0, 2) or 'Traceback' in r.stderr:
                errors.append(f'{skill.name}: {py.name} --help failed: {r.stderr.strip()[-200:]}')


def check_manifests(names):
    for manifest in (REPO / '.claude-plugin' / 'marketplace.json',):
        if not manifest.exists():
            errors.append(f'missing {manifest.relative_to(REPO)}')
            continue
        listed = {Path(s).name for p in json.loads(manifest.read_text())['plugins'] for s in p.get('skills', [])}
        missing = set(names) - listed
        if missing:
            errors.append(f'{manifest.relative_to(REPO)} does not list {sorted(missing)}')


# Files that two skills each carry so that either works alone; the copies must match byte for byte.
SHARED_COPIES = [
    ('sci-literature-evidence/scripts/evidence_tools.py', 'sci-manuscript-build/assets/manuscript_kit/evidence_tools.py'),
    ('sci-prose-style/assets/style_limits.json', 'sci-manuscript-build/assets/manuscript_kit/style_limits.json'),
    ('sci-prose-style/scripts/style_limits.py', 'sci-manuscript-build/assets/manuscript_kit/style_limits.py'),
]
SHARED_COPIES += [('sci-prose-style/assets/style_profiles/'+name+'.json', 'sci-manuscript-build/assets/manuscript_kit/style_profiles/'+name+'.json') for name in ('precise','generic','explanatory','compact')]


def check_shared():
    for a, b in SHARED_COPIES:
        pa, pb = SKILLS / a, SKILLS / b
        if not (pa.exists() and pb.exists()):
            errors.append(f'shared file missing: {a if not pa.exists() else b}')
            continue
        if pa.read_bytes() != pb.read_bytes():
            errors.append(f'shared copies differ: {a} and {b} (edit one, copy it over the other)')
    path = SKILLS / 'sci-prose-style/assets/style_limits.json'
    if path.exists():
        limits = json.loads(path.read_text(encoding='utf-8'))
        for group in ('caps', 'banned', 'banned_openers', 'advisory'):
            labels = [e['label'] for e in limits.get(group, [])]
            if len(labels) != len(set(labels)):
                errors.append(f'style_limits.json: duplicate labels in {group}')
            for entry in limits.get(group, []):
                try:
                    re.compile(entry['pattern'])
                except re.error as exc:
                    errors.append(f'style_limits.json: {group} "{entry["label"]}" does not compile: {exc}')


def check_router():
    """Files named in the orchestrator's mode router exist; a bare name resolves in the skill named before it."""
    router = SKILLS / 'sci-writing-orchestrator' / 'references' / 'writing-mode-router.md'
    if not router.exists():
        return
    skills = {p.name for p in SKILLS.iterdir() if (p / 'SKILL.md').exists()}
    for line in router.read_text(encoding='utf-8').splitlines():
        if not line.startswith('|'):
            continue
        for cell in line.split('|'):
            skill = 'sci-writing-orchestrator'
            for token in re.findall(r'[A-Za-z0-9_./-]+', cell):
                if token in skills:
                    skill = token
                elif re.search(r'\.(md|json)$', token):
                    base = SKILLS / skill
                    if not any((base / sub / token).exists() for sub in ('', 'references', 'presets')):
                        errors.append(f'writing-mode-router.md names {token} in {skill}, which does not exist')


def main():
    names = []
    check_shared()
    check_router()
    for skill in sorted(p for p in SKILLS.iterdir() if (p / 'SKILL.md').exists()):
        names.append(skill.name)
        text = check_frontmatter(skill)
        check_paths(skill, text, 'SKILL.md')
        for ref in sorted((skill / 'references').glob('*.md')):
            check_paths(skill, ref.read_text(encoding='utf-8'), f'references/{ref.name}')
        check_integrity(skill)
        check_agents(skill)
        check_scripts(skill)
    check_manifests(names)
    for w in warnings:
        print('WARN ', w)
    for e in errors:
        print('ERROR', e)
    print(f'{len(names)} skills checked: {len(errors)} errors, {len(warnings)} warnings')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())

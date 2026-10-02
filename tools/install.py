#!/usr/bin/env python3
"""Install the Academic Writing Skills for Claude Code, Codex and OpenCode.

Usage
  python3 tools/install.py                       install skills + inject global instructions (all tools)
  python3 tools/install.py --targets claude codex
  python3 tools/install.py --mode symlink        link instead of copy (edits in the repo apply at once)
  python3 tools/install.py --project DIR --no-inject   install into DIR/.claude/skills and DIR/.agents/skills
                                                 instead of the user folders (a repository that carries its own copy)
  python3 tools/install.py --no-inject           skills only, leave global instruction files alone
  python3 tools/install.py --status              show what is installed where
  python3 tools/install.py --uninstall           remove skills and the injected instruction blocks

Where things go
  claude    ~/.claude/skills/<skill>        read by Claude Code; OpenCode also reads this folder
  codex     $CODEX_HOME/skills/<skill>      Codex (some hosts discover both ~/.codex/skills and ~/.agents/skills;
                                            one copy is enough, and the installer uses ~/.codex/skills)
  opencode  ~/.config/opencode/skills/<skill>  only when OpenCode cannot see ~/.claude/skills
            (OPENCODE_DISABLE_CLAUDE_CODE[_SKILLS] set); otherwise skipped to avoid duplicates
  agents    ~/.agents/skills/<skill>        for other Agent-Skills tools; do not combine with codex
                                            (Codex would list every skill twice)

Global instructions (a marked block, replaced on re-install, removed on uninstall)
  ~/.claude/CLAUDE.md                   Claude Code; OpenCode falls back to it
  ~/.codex/AGENTS.md                    Codex
  ~/.config/opencode/AGENTS.md          if it already exists (it shadows CLAUDE.md in OpenCode), or when
                                        OPENCODE_DISABLE_CLAUDE_CODE[_PROMPT] stops OpenCode reading CLAUDE.md
Existing files are backed up once to <file>.bak-academic-writing before the first change.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO / 'skills'
HOME = Path.home()
MARK_BEGIN = '<!-- BEGIN academic-writing-skills -->'
MARK_END = '<!-- END academic-writing-skills -->'
IGNORE = shutil.ignore_patterns('__pycache__', '*.pyc', '.DS_Store', '*.bak*')


def skill_names():
    return sorted(p.parent.name for p in SKILLS_DIR.glob('*/SKILL.md'))


def version():
    try:
        return json.loads((REPO / '.claude-plugin' / 'plugin.json').read_text(encoding='utf-8'))['version']
    except Exception:
        return 'dev'


def _flag(name):
    return os.environ.get(name, '').lower() in ('1', 'true', 'yes')


def opencode_sees_claude():
    return not (_flag('OPENCODE_DISABLE_CLAUDE_CODE') or _flag('OPENCODE_DISABLE_CLAUDE_CODE_SKILLS'))


def opencode_reads_claude_md():
    return not (_flag('OPENCODE_DISABLE_CLAUDE_CODE') or _flag('OPENCODE_DISABLE_CLAUDE_CODE_PROMPT'))


def skill_roots(targets, project=None):
    """User-level roots, or project roots only when --project is given (both would duplicate skills)."""
    roots = {}
    if project:
        p = Path(project).expanduser().resolve()
        if 'claude' in targets or 'opencode' in targets:
            roots['project-claude'] = p / '.claude' / 'skills'      # Claude Code and OpenCode
        if 'codex' in targets or 'agents' in targets:
            roots['project-agents'] = p / '.agents' / 'skills'      # Codex repo skills
        return roots
    if 'claude' in targets:
        roots['claude'] = HOME / '.claude' / 'skills'
    if 'codex' in targets:
        roots['codex'] = Path(os.environ.get('CODEX_HOME', HOME / '.codex')) / 'skills'
    if 'opencode' in targets and not ('claude' in targets and opencode_sees_claude()):
        roots['opencode'] = HOME / '.config' / 'opencode' / 'skills'
    if 'agents' in targets:
        roots['agents'] = HOME / '.agents' / 'skills'
    return roots


def place(src: Path, dst: Path, mode: str):
    import uuid
    dst.parent.mkdir(parents=True, exist_ok=True)
    token = datetime.now().strftime('%Y%m%d-%H%M%S') + '-' + uuid.uuid4().hex[:8]
    staged = dst.with_name('.' + dst.name + '-' + token)
    if mode == 'symlink':
        staged.symlink_to(src.resolve(), target_is_directory=True)
    else:
        shutil.copytree(src, staged, ignore=IGNORE)
        (staged/'.installed-from').write_text(f'{src}\nversion {version()}\n', encoding='utf-8')
    if dst.exists() or dst.is_symlink():
        backup = dst.parent/'.academic-writing-backups'/token/dst.name
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(dst), str(backup))
        print(f'  previous skill saved: {backup}')
    staged.replace(dst)


def instruction_block():
    body = (REPO / 'tools' / 'global_instructions.md').read_text(encoding='utf-8').strip()
    return f'{MARK_BEGIN}\n{body}\n{MARK_END}\n'


def backup_once(path: Path):
    bak = path.with_name(path.name + '.bak-academic-writing')
    if path.exists() and not bak.exists():
        shutil.copy2(path, bak)


def inject(path: Path, create: bool):
    if not path.exists() and not create:
        return 'skipped (file absent)'
    text = path.read_text(encoding='utf-8') if path.exists() else ''
    block = instruction_block()
    pattern = re.compile(re.escape(MARK_BEGIN) + r'.*?' + re.escape(MARK_END) + r'\n?', re.S)
    if pattern.search(text):
        new = pattern.sub(lambda _: block, text)
        action = 'updated'
    else:
        new = (text.rstrip() + '\n\n' if text.strip() else '') + block
        action = 'created' if not text else 'appended'
    if new != text:
        backup_once(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(new, encoding='utf-8')
    else:
        action = 'unchanged'
    return action


def remove_block(path: Path):
    if not path.exists():
        return 'absent'
    text = path.read_text(encoding='utf-8')
    pattern = re.compile(r'\n*' + re.escape(MARK_BEGIN) + r'.*?' + re.escape(MARK_END) + r'\n?', re.S)
    new = pattern.sub('\n', text).strip()
    if new == text.strip():
        return 'no block'
    if new:
        path.write_text(new + '\n', encoding='utf-8')
        return 'block removed'
    path.unlink()
    return 'file removed (it held only the block)'


def instruction_files(targets):
    files = []
    if 'claude' in targets or ('opencode' in targets and opencode_reads_claude_md()):
        files.append((HOME / '.claude' / 'CLAUDE.md', True))
    if 'codex' in targets:
        files.append((Path(os.environ.get('CODEX_HOME', HOME / '.codex')) / 'AGENTS.md', True))
    if 'opencode' in targets:
        files.append((HOME / '.config' / 'opencode' / 'AGENTS.md', not opencode_reads_claude_md()))
    return files


def status(targets, project):
    names = skill_names()
    print(f'Academic Writing Skills {version()} in {REPO}')
    for label, root in skill_roots(targets, project).items():
        present = [n for n in names if (root / n / 'SKILL.md').exists()]
        kind = 'symlink' if present and (root / present[0]).is_symlink() else 'copy' if present else '-'
        print(f'  {label:15s} {root}: {len(present)}/{len(names)} skills ({kind})')
    if 'codex' in targets and not project:
        alternate=HOME/'.agents'/'skills'
        primary=Path(os.environ.get('CODEX_HOME',HOME/'.codex'))/'skills'
        duplicate=[n for n in names if (alternate/n/'SKILL.md').is_file() and (primary/n/'SKILL.md').is_file()]
        if duplicate:
            print('  duplicate discovery copies: '+', '.join(duplicate))
            print('  Inspect both copies and choose one location; no alternate directory is removed automatically.')
    for path, _ in instruction_files(targets):
        has = path.exists() and MARK_BEGIN in path.read_text(encoding='utf-8')
        print(f'  instructions    {path}: {"block present" if has else "no block" if path.exists() else "absent"}')
    if 'opencode' in targets and opencode_sees_claude():
        print('  opencode        reads ~/.claude/skills and ~/.claude/CLAUDE.md (no separate copy needed)')


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--targets', nargs='+', default=['claude', 'codex', 'opencode'],
                    choices=['claude', 'codex', 'opencode', 'agents'])
    ap.add_argument('--mode', choices=['copy', 'symlink'], default='copy')
    ap.add_argument('--project')
    ap.add_argument('--no-inject', action='store_true')
    ap.add_argument('--status', action='store_true')
    ap.add_argument('--uninstall', action='store_true')
    args = ap.parse_args(argv)
    names = skill_names()
    if not names:
        sys.exit(f'no skills found in {SKILLS_DIR}')
    if args.status:
        status(args.targets, args.project)
        return 0
    if 'agents' in args.targets and 'codex' in args.targets:
        sys.exit('--targets agents and codex together would make Codex list every skill twice; choose one.')
    roots = skill_roots(args.targets, args.project)
    if args.uninstall:
        for label, root in roots.items():
            for n in names:
                d = root / n
                if d.is_symlink() or d.is_file():
                    d.unlink()
                elif d.exists():
                    shutil.rmtree(d)
            print(f'removed {len(names)} skills from {root}')
        for path, _ in instruction_files(args.targets):
            print(f'{path}: {remove_block(path)}')
        return 0
    for label, root in roots.items():
        for n in names:
            place(SKILLS_DIR / n, root / n, args.mode)
        print(f'{label:15s} {len(names)} skills -> {root} ({args.mode})')
    if 'opencode' in args.targets and 'opencode' not in roots and not args.project:
        print('opencode        uses ~/.claude/skills (Claude-compatible discovery); no duplicate copy made')
    if not args.no_inject:
        for path, create in instruction_files(args.targets):
            print(f'instructions    {path}: {inject(path, create)}')
    print('Restart Claude Code, Codex and OpenCode sessions to load the skills.')
    return 0


if __name__ == '__main__':
    sys.exit(main())

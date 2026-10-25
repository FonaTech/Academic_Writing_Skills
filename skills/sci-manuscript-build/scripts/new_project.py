#!/usr/bin/env python3
"""Create a new manuscript project from the kit.

Usage
  new_project.py TARGET_DIR --slug Name --type review|article|letter|rebuttal|proposal|thesis-chapter
                 [--title-en "..."] [--title-zh "..."] [--languages en zh] [--chapter N]

Copies assets/manuscript_kit into TARGET_DIR (never over an existing manuscript.json),
fills manuscript.json, writes a skeleton content.py for the document type, creates
Figures/, evidence/ and archive/, and records the kit version. Then:

  cd TARGET_DIR
  python3 build_manuscript.py && python3 check_manuscript.py
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import date
from pathlib import Path

KIT = Path(__file__).resolve().parents[1] / 'assets' / 'manuscript_kit'
KIT_VERSION = '1.1.0'

SKELETONS = {
    'review': [
        ('h', 1, 'Introduction', '引言'),
        ('p', 'State the field-level problem in one sentence, then the progress that makes a review timely, '
              'then what this review covers and how it is organised.',
              '一句话陈述领域问题，再说明哪些进展使综述适时，最后说明本综述覆盖什么、如何组织。'),
        ('h', 1, 'Principles: the mechanism or concept the field builds on', '原理：领域赖以发展的机制或概念'),
        ('h', 1, 'First line of progress (named by its idea, not by paper)', '第一条进展主线（以思路命名，而非按文献）'),
        ('h', 1, 'Second line of progress', '第二条进展主线'),
        ('h', 1, 'Shared challenges across the lines', '各主线共同面对的挑战'),
        ('h', 1, 'Outlook', '展望'),
    ],
    'article': [
        ('h', 1, 'Introduction', '引言'),
        ('p', 'Context in two sentences; the specific gap; what we show, with the headline numbers.',
              '两句背景；具体空白；本文展示了什么，给出关键数字。'),
        ('h', 1, 'Results', '结果'),
        ('h', 2, 'Declarative heading that states the first finding', '陈述第一项发现的标题'),
        ('h', 2, 'Declarative heading that states the second finding', '陈述第二项发现的标题'),
        ('h', 1, 'Discussion', '讨论'),
        ('h', 1, 'Methods', '方法'),
    ],
    'letter': [
        ('h', 1, 'Main text', '正文'),
        ('p', 'Gap and result in the first paragraph; one figure per claim.', '第一段给出空白与结果；每个结论对应一张图。'),
        ('h', 1, 'Methods', '方法'),
    ],
    'rebuttal': [
        ('h', 1, 'Summary of changes', '修改概述'),
        ('h', 1, 'Reviewer 1', '审稿人 1'),
        ('p', 'Comment 1.1 (quoted verbatim). Response. Change made, with location.',
              '意见 1.1（原文引用）。回复。所做修改及位置。'),
        ('h', 1, 'Reviewer 2', '审稿人 2'),
    ],
    'proposal': [
        ('h', 1, 'Aims and significance', '研究目标与意义'),
        ('h', 1, 'Background and preliminary results', '研究基础与前期结果'),
        ('h', 1, 'Research plan', '研究方案'),
        ('h', 1, 'Risks and alternatives', '风险与备选方案'),
        ('h', 1, 'Timeline and deliverables', '进度与成果'),
    ],
    'thesis-chapter': [
        ('h', 1, 'Chapter title', '章标题'),
        ('p', 'Chapter aim and how it connects to the previous chapter.', '本章目标及与上一章的衔接。'),
        ('h', 2, 'Methods', '方法'),
        ('h', 2, 'Results', '结果'),
        ('h', 2, 'Summary', '小结'),
    ],
}


def skeleton(doc_type: str, chapter) -> str:
    lines = ['"""Manuscript text. See the kit README for the markup."""', 'from floats import BOXES', '',
             f'CHAPTER = {chapter!r}', 'BLOCKS = []', '', '',
             "def H(id, level, en, zh=''):",
             "    BLOCKS.append(dict(id=id, type='heading', level=level, en=en, zh=zh))", '', '',
             "def P(id, en, zh=''):",
             "    BLOCKS.append(dict(id=id, type='para', en=' '.join(en.split()), zh=' '.join(zh.split()) if zh else ''))",
             '', '',
             'def EQ(id, key, latex):',
             "    BLOCKS.append(dict(id=id, type='eq', key=key, latex=latex))", '', '',
             'def BOX(id, name):',
             '    box = BOXES[name]',
             "    BLOCKS.append(dict(id=id, type='box', name=name, title_en=box['title_en'],",
             "                       title_zh=box['title_zh'], items=box['items']))", '', '']
    n = 0
    for item in SKELETONS[doc_type]:
        n += 1
        if item[0] == 'h':
            _, level, en, zh = item
            lines.append(f"H('h{n}', {level}, {en!r}, {zh!r})")
        else:
            _, en, zh = item
            lines.append(f"P('p{n}', {en!r}, {zh!r})")
    return '\n'.join(lines) + '\n'


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('target')
    ap.add_argument('--slug', required=True)
    ap.add_argument('--type', default='review', choices=sorted(SKELETONS))
    ap.add_argument('--title-en', default='Working title')
    ap.add_argument('--title-zh', default='暂定题目')
    ap.add_argument('--languages', nargs='+', default=['en', 'zh'])
    ap.add_argument('--chapter', type=int, default=None,
                    help='number of the first level-1 heading (default 1 for review and thesis-chapter; '
                         'other types are unnumbered unless given)')
    args = ap.parse_args(argv)
    if args.chapter is None and args.type in ('review', 'thesis-chapter'):
        args.chapter = 1
    target = Path(args.target)
    if (target / 'manuscript.json').exists():
        sys.exit(f'{target} already holds a manuscript project; not overwriting.')
    target.mkdir(parents=True, exist_ok=True)
    for f in KIT.iterdir():
        if f.is_file() and f.suffix in ('.py', '.json', '.md'):
            shutil.copy2(f, target / f.name)
    cfg = json.loads((target / 'manuscript.json').read_text(encoding='utf-8'))
    cfg['project'].update(slug=args.slug, doc_type=args.type, title_en=args.title_en, title_zh=args.title_zh)
    cfg['output']['languages'] = args.languages
    cfg['kit_version'] = KIT_VERSION
    cfg['created'] = date.today().isoformat()
    (target / 'manuscript.json').write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding='utf-8')
    (target / 'content.py').write_text(skeleton(args.type, args.chapter), encoding='utf-8')
    (target / 'floats.py').write_text('FIGURES = {}\nTABLES = {}\nBOXES = {}\n', encoding='utf-8')
    (target / 'references.json').write_text('{}\n', encoding='utf-8')
    for sub in ('Figures', 'evidence', 'archive', 'source_audit'):
        (target / sub).mkdir(exist_ok=True)
    print(f'Created {args.type} project "{args.slug}" in {target}')
    if args.chapter is None:
        print('Headings are unnumbered (CHAPTER = None in content.py); {sec:} references need a number.')
    elif args.type == 'thesis-chapter':
        print(f'Headings start at chapter {args.chapter}; pass --chapter N for the chapter\'s place in the thesis.')
    print('Next: python3 build_manuscript.py && python3 check_manuscript.py')


if __name__ == '__main__':
    sys.exit(main())

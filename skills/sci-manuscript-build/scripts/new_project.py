#!/usr/bin/env python3
"""Create a generic declarative manuscript project; never overwrite a nonempty directory."""
from __future__ import annotations
import argparse
import json
import shutil
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parents[1] / 'assets/manuscript_kit'
KIT_VERSION = '2.0.0'
SKELETONS = {
    'review': ['Introduction', 'Organizing framework', 'Evidence synthesis', 'Limitations and open questions', 'Conclusions'],
    'narrative-review': ['Introduction', 'Scope and approach', 'Thematic synthesis', 'Limitations and open questions', 'Conclusions'],
    'systematic-review': ['Introduction', 'Methods', 'Results', 'Discussion', 'Data and code availability'],
    'scoping-review': ['Introduction', 'Methods', 'Evidence map', 'Gaps and limitations', 'Conclusions'],
    'article': ['Introduction', 'Methods', 'Results', 'Discussion', 'Data and code availability'],
    'letter': ['Main text', 'Methods', 'Data and code availability'],
    'rebuttal': ['Summary of revisions', 'Reviewer comments and responses'],
    'proposal': ['Research question and significance', 'Current evidence', 'Aims and approach', 'Risks and alternatives', 'Schedule and resources'],
    'thesis-chapter': ['Chapter question', 'Methods or approach', 'Findings or synthesis', 'Discussion and connection to the thesis'],
}
ZH = {'Introduction':'引言','Organizing framework':'组织框架','Evidence synthesis':'证据综合',
      'Limitations and open questions':'局限与开放问题','Conclusions':'结论','Scope and approach':'范围与方法',
      'Thematic synthesis':'主题综合','Methods':'方法','Results':'结果','Discussion':'讨论',
      'Data and code availability':'数据与代码可用性','Evidence map':'证据图谱','Gaps and limitations':'空白与局限',
      'Main text':'正文','Summary of revisions':'修改概述','Reviewer comments and responses':'审稿意见与回复',
      'Research question and significance':'研究问题与意义','Current evidence':'现有证据','Aims and approach':'目标与方法',
      'Risks and alternatives':'风险与备选方案','Schedule and resources':'进度与资源','Chapter question':'本章问题',
      'Methods or approach':'方法或途径','Findings or synthesis':'发现或综合','Discussion and connection to the thesis':'讨论及与全文的联系'}

def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('target')
    ap.add_argument('--slug', required=True)
    ap.add_argument('--type', choices=sorted(SKELETONS), default='article')
    ap.add_argument('--languages', nargs='+', default=['en'])
    ap.add_argument('--title-en', default='Working title')
    ap.add_argument('--title-zh', default='暂定题目')
    ap.add_argument('--chapter', type=int)
    ap.add_argument('--field',default='unspecified')
    ap.add_argument('--style',choices=['precise','compact','explanatory','generic'],default='precise')
    args = ap.parse_args(argv)
    if not args.languages or len(args.languages) != len(set(args.languages)):
        ap.error('languages must be nonempty and unique')
    if not args.slug or any(c in args.slug for c in '/\\'):
        ap.error('slug must be a filename component')
    target = Path(args.target)
    if target.exists() and any(target.iterdir()):
        ap.error('target directory is not empty; use a new directory')
    target.mkdir(parents=True, exist_ok=True)
    for file in KIT.iterdir():
        if file.is_file() and file.suffix in ('.py','.json','.md'):
            shutil.copy2(file, target/file.name)
    shutil.copytree(KIT/'style_profiles',target/'style_profiles')
    cfg = json.loads((target/'manuscript.json').read_text(encoding='utf-8'))
    cfg['project'].update(slug=args.slug, doc_type=args.type, title_en=args.title_en, title_zh=args.title_zh)
    cfg['source'] = dict(format='json', manifest='content.json', floats='floats.json')
    cfg['output']['languages'] = args.languages
    cfg['style']['profile'] = args.style
    cfg['writing_context'] = dict(field=args.field,study_type=args.type,perspectives=['domain researcher','scientific editor'],reader='to specify',current_task='planning and drafting')
    if sys.platform == 'darwin':
        cfg['fonts'].update(east_asian_body='Songti SC', east_asian_heading='Heiti SC')
    elif sys.platform == 'win32':
        cfg['fonts'].update(east_asian_body='SimSun', east_asian_heading='SimHei')
    else:
        cfg['fonts'].update(east_asian_body='Noto Serif CJK SC', east_asian_heading='Noto Sans CJK SC')
    cfg['kit_version'] = KIT_VERSION
    write(target/'manuscript.json', cfg)
    for name in ('sections','Figures','evidence','archive','source_audit','data','analysis'):
        (target/name).mkdir(exist_ok=True)
    sections = []
    for index, heading in enumerate(SKELETONS[args.type],1):
        filename = f'sections/{index:02d}.json'
        sections.append(filename)
        blocks = [dict(id=f'h{index}',type='heading',level=1,en=heading,zh=ZH.get(heading, heading)),
                  dict(id=f'p{index}',type='para',status='draft',claims=[],en='[to verify] Draft this section from its evidence and argument plan.',
                       zh='[to verify] 根据本节证据与论证计划起草。')]
        write(target/filename, {'blocks':blocks})
    write(target/'content.json', {'schema_version':2,'chapter':args.chapter,'sections':sections})
    write(target/'floats.json', {'figures':{},'tables':{},'boxes':{}})
    write(target/'references.json', {})
    (target/'content.py').unlink(missing_ok=True)
    (target/'floats.py').unlink(missing_ok=True)
    print(f'Created {args.type} project at {target}')
    print('Edit the ordered sections/*.json; scaffold text is not submission-ready.')
    print('Preview: python3 pipeline.py --stage preview')
    print('Validate final files: python3 pipeline.py --stage release')
    return 0

if __name__ == '__main__':
    sys.exit(main())

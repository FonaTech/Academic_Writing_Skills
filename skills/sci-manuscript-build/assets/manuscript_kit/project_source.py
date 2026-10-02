"""Load declarative chapter files or an explicitly trusted legacy Python project."""
from __future__ import annotations
import hashlib
import importlib
import json
from pathlib import Path
from types import SimpleNamespace

def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def source_paths(root, cfg):
    root = Path(root)
    source = cfg.get('source', {'format': 'python'})
    if source.get('format') == 'python':
        return [root/'content.py', root/'floats.py']
    manifest = root/source.get('manifest', 'content.json')
    data = read(manifest)
    paths = [manifest, root/source.get('floats', 'floats.json')] + [root/f for f in data.get('sections', [])]
    blocks = list(data.get('blocks', []))
    for file in data.get('sections', []):
        part = read(root/file)
        blocks += part if isinstance(part,list) else part['blocks']
    for block in blocks:
        paths += [root/f for f in block.get('files', {}).values()]
    return paths

def load_project(root, cfg):
    root = Path(root)
    if cfg.get('source', {}).get('format', 'python') == 'python':
        return importlib.import_module('content'), importlib.import_module('floats')
    source = cfg['source']
    manifest = read(root/source.get('manifest', 'content.json'))
    if manifest.get('blocks') and manifest.get('sections'):
        raise ValueError('choose manifest.blocks or manifest.sections, not both')
    blocks = manifest.get('blocks', [])
    for name in manifest.get('sections', []):
        part = read(root/name)
        blocks += part if isinstance(part, list) else part['blocks']
    f = read(root/source.get('floats', 'floats.json'))
    floats = SimpleNamespace(FIGURES=f.get('figures', {}), TABLES=f.get('tables', {}), BOXES=f.get('boxes', {}))
    primary = cfg['output'].get('languages', ['en'])[0]
    ids = set()
    for block in blocks:
        if not isinstance(block, dict) or not block.get('id') or block['id'] in ids:
            raise ValueError('every content block requires a unique id')
        ids.add(block['id'])
        for lang, filename in block.get('files', {}).items():
            if lang in block:
                raise ValueError(f'{block["id"]}: choose inline text or files.{lang}, not both')
            block[lang] = (root/filename).read_text(encoding='utf-8').strip()
        if block.get('type') not in ('para', 'heading', 'eq', 'box'):
            raise ValueError(f"{block['id']}: unsupported block type")
        if block['type'] == 'box' and 'items' not in block:
            definition = floats.BOXES[block['name']]
            block.update(definition)
        if block['type'] in ('para', 'heading') and primary not in block:
            raise ValueError(f"{block['id']}: missing authoritative language {primary}")
    return SimpleNamespace(BLOCKS=blocks, CHAPTER=manifest.get('chapter')), floats

def fingerprint(root, cfg):
    """Bind checks/reviews to the source and declared evidence/artifact state."""
    root = Path(root)
    paths = [root/'manuscript.json', root/cfg['paths']['references'], root/'style_limits.json',root/'style_limits.py'] + source_paths(root, cfg)
    paths += sorted((root/'style_profiles').glob('*.json'))
    for name in ('build_manuscript.py', 'check_manuscript.py', 'project_source.py', 'evidence_tools.py', 'manuscript_core.py'):
        paths.append(root/name)
    folder = root/cfg['paths'].get('evidence', 'evidence')
    for file in sorted(folder.glob('*.json')):
        paths.append(file)
        data = read(file)
        records = data.values() if isinstance(data, dict) else data
        for rec in records:
            if not isinstance(rec, dict):
                continue
            for artifact in rec.get('provenance', {}).get('artifacts', []):
                paths.append(root/artifact.get('path', ''))
            if rec.get('source_file'):
                src = Path(rec['source_file'])
                paths.append(src if src.is_absolute() else root/cfg['paths'].get('source_audit', 'source_audit')/src)
    figures = root/cfg['paths']['figures']
    if figures.exists():
        paths += [p for p in figures.rglob('*') if p.is_file() and 'verify' not in p.parts]
    digest = hashlib.sha256()
    for path in sorted(set(paths), key=str):
        name = str(path.relative_to(root)) if path.is_relative_to(root) else str(path)
        digest.update(name.encode())
        digest.update(path.read_bytes() if path.is_file() else b'[missing]')
    return digest.hexdigest()

def audit_blocks(content, floats, languages):
    for block in content.BLOCKS:
        if block['type'] == 'para':
            yield block['id'], block, {l: block.get(l, '') for l in languages}
        elif block['type'] == 'box':
            for i, item in enumerate(block.get('items', [])):
                if item['type'] == 'para':
                    yield f"{block['id']}.{i}", item, {l: item.get(l, '') for l in languages}
    for key, fig in floats.FIGURES.items():
        yield 'fig:'+key, fig, {l: fig.get('caption_'+l, '') for l in languages}
    for key, table in floats.TABLES.items():
        for ri, row in enumerate(table.get('rows_'+languages[0], [])):
            for ci, _ in enumerate(row):
                cell = dict(table.get('cell_claims', {}).get(f'{ri}:{ci}', {}))
                cell['table_cell'] = True
                cell['unit_context'] = {lang: str(table.get('columns_'+lang, [])[ci])
                    if ci < len(table.get('columns_'+lang, [])) else '' for lang in languages}
                texts = {}
                for lang in languages:
                    rows = table.get('rows_'+lang, [])
                    texts[lang] = str(rows[ri][ci]) if ri < len(rows) and ci < len(rows[ri]) else ''
                yield f'tab:{key}:{ri}:{ci}', cell, texts
        yield 'tab:'+key+':note', table, {l: table.get('note_'+l, '') for l in languages}

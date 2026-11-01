"""Evidence and quantity checks. These detect inconsistencies, not semantic truth."""
from __future__ import annotations
import hashlib
import json
import re
from decimal import Decimal, InvalidOperation
from pathlib import Path

LIGATURES = {'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl', 'ﬃ': 'ffi', 'ﬄ': 'ffl', '\u00ad': ''}
NUMBER = r'[+−-]?(?:\d+(?:\.\d+)?|\.\d+)(?:[eE][+−-]?\d+)?'
NUM_RE = re.compile(r'(?<![\w.])' + NUMBER)
BASE_UNIT = r'(?:TOPS|GOPS|OPS|[kMGTPmunpfµμ]?(?:Hz|Pa|eV|Ω|ohm|mol|bits?|m|V|A|W|J|s|S|F|g|L)|%|K|°C|ppm|dB|伏|毫伏|焦耳|秒|米|帕|摄氏度)'
UNIT = BASE_UNIT + r'(?:[²³]|\^[-−]?\d+)?(?:\s*(?:/|[·⋅])\s*' + BASE_UNIT + r'(?:[²³]|\^[-−]?\d+)?)*'
QUANTITY_RE = re.compile(r'(?<![\w.])(' + NUMBER + r'(?:\s*[–—]\s*' + NUMBER + r')?)\s*(' + UNIT + r')(?![A-Za-z])')

def scientific_notation(text):
    text = str(text)
    superscript = str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻','0123456789+-')
    text = re.sub(r'(\d)([⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻]+)', lambda m:m[1]+'^'+m[2].translate(superscript), text)
    pattern = re.compile(r'(?<![\w.])(?:(('+NUMBER+r')\s*(?:×|x|\\times)\s*)?10\s*\^\s*\{?([+−-]?\d+)\}?)')
    def convert(match):
        mantissa = match.group(2) or '1'
        exponent = int(match.group(3).replace('−','-'))
        if abs(exponent)>10000:
            return match.group()
        return str(Decimal(mantissa.replace('−','-')) * Decimal(10)**exponent)
    text = pattern.sub(convert,text)
    return re.sub(r'(?<=\d)-(?=\d)', '–', text)

def norm(text):
    """Safe PDF typography normalization: never remove decimal points or signs."""
    text = str(text or '')
    for before, after in LIGATURES.items():
        text = text.replace(before, after)
    text = re.sub(r'([A-Za-z])-\s*\n\s*([A-Za-z])', r'\1\2', text)
    return re.sub(r'\s+', ' ', text).strip()

def numeric(value):
    try:
        return str(Decimal(str(value).replace('−', '-')).normalize())
    except InvalidOperation:
        return str(value)

def numeric_tokens(text):
    # Preserve signs and exponents; ignore citation/float markup, not scientific numbers.
    text = re.sub(r'\[@[^\]]*\]|\{(?:fig|tab|eq|sec|box):[^}]*\}', '', str(text))
    return [numeric(m.group()) for m in NUM_RE.finditer(scientific_notation(text))]

def unit(text):
    text = str(text or '').replace('μ', 'µ').replace(' ', '').replace('²','^2').replace('³','^3')
    return {'伏': 'V', '毫伏': 'mV', '焦耳': 'J', '秒': 's', '米': 'm', '帕': 'Pa',
            '摄氏度': '°C', 'TOPSW^-1': 'TOPS/W', 'TOPSW-1': 'TOPS/W', 'TOPSW⁻¹': 'TOPS/W'}.get(text, text)

def quantities(text):
    clean = re.sub(r'\[@[^\]]*\]|\{(?:fig|tab|eq|sec|box):[^}]*\}', '', str(text))
    return [(n, unit(m.group(2))) for m in QUANTITY_RE.finditer(scientific_notation(clean)) for n in numeric_tokens(m.group(1))]

def header_units(header):
    """Only explicit parenthesized/bracketed column units, never arbitrary metadata."""
    candidates = re.findall(r'[（(\[]([^）)\]]+)[）)\]]', str(header))
    return {unit(c) for c in candidates if c.strip() and len(c)<80}

def declared_quantities(text, known_units):
    """Extend common-unit detection with exact units declared by this project."""
    found = quantities(text)
    clean = scientific_notation(re.sub(r'\[@[^\]]*\]|\{(?:fig|tab|eq|sec|box):[^}]*\}', '', str(text)))
    for declared in known_units:
        if not declared:
            continue
        spellings = {declared,declared.replace('µ','μ'),declared.replace('^2','²').replace('^3','³')}
        for spelling in spellings:
            pattern = r'(?<![\w.])('+NUMBER+r'(?:\s*[–—]\s*'+NUMBER+r')?)\s*'+re.escape(spelling)+r'(?![A-Za-z])'
            for match in re.finditer(pattern,clean):
                for n in numeric_tokens(match[1]):
                    pair=(n,unit(declared))
                    if pair not in found:
                        found.append(pair)
    return found

def pages_of(path):
    raw = Path(path).read_text(encoding='utf-8')
    parts = re.split(r'=== PAGE (\d+) ===', raw)
    return {int(parts[i]): norm(parts[i+1]) for i in range(1, len(parts)-1, 2)} or {1: norm(raw)}

def iter_records(data):
    if isinstance(data, dict) and isinstance(data.get('papers'), list):
        for paper in data['papers']:
            for i, item in enumerate(paper.get('exemplars', []) + paper.get('antipatterns', [])):
                rec = dict(item)
                rec.setdefault('source_file', paper.get('text') or paper.get('id'))
                yield f"{paper.get('id')}:{i}", rec
    elif isinstance(data, dict):
        for key, rec in data.items():
            if not isinstance(rec, dict):
                raise ValueError(f'evidence {key} is not an object')
            yield key, rec
    elif isinstance(data, list):
        for i, rec in enumerate(data):
            if not isinstance(rec, dict):
                raise ValueError(f'evidence item {i} is not an object')
            yield rec.get('key', str(i)), rec
    else:
        raise ValueError('evidence must be an object or array')

def resolve_text(rec, text_dir):
    names = [rec.get(k) for k in ('source_file', 'text', 'paper', 'id') if rec.get(k)]
    candidates = []
    for name in names:
        for candidate in (Path(name), Path(text_dir)/name, Path(text_dir)/(str(name)+'.txt')):
            if candidate.is_file() and candidate.suffix == '.txt':
                candidates.append(candidate.resolve())
    candidates = list(dict.fromkeys(candidates))
    if len(candidates) > 1:
        raise ValueError('ambiguous text source; use its exact path')
    return candidates[0] if candidates else None

def verify_quote(rec, text_dir, check_value=True):
    errors = []
    if not rec.get('quote'):
        return ['missing quote']
    try:
        src = resolve_text(rec, text_dir)
    except ValueError as exc:
        return [str(exc)]
    if src is None:
        return ['text source missing (use an exact .txt path)']
    page_list = rec.get('pages', [rec.get('page', rec.get('page_reported'))])
    if not isinstance(page_list, list) or not page_list or any(type(p) is not int or p < 1 for p in page_list):
        return ['missing/invalid PDF page or pages']
    if page_list != list(range(page_list[0], page_list[-1]+1)):
        return ['cross-page quotes require consecutive pages']
    pages = pages_of(src)
    if any(p not in pages for p in page_list):
        return ['stated page does not exist']
    quote = norm(rec['quote'])
    if quote not in norm(' '.join(pages[p] for p in page_list)):
        found = [p for p, text in pages.items() if quote in text]
        errors.append('full quote not on stated page(s)' + (f'; found on {found}' if found else ''))
    if check_value and rec.get('value') is not None:
        expected, actual = numeric_tokens(rec['value']), numeric_tokens(quote)
        if any(expected.count(n) > actual.count(n) for n in set(expected)):
            errors.append('value is not present in quote as complete numeric token(s)')
    return errors

def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def verify_record(rec, root, text_dir, release=False):
    kind = rec.get('source_kind', 'literature')
    errors = []
    if kind == 'literature':
        errors += verify_quote(rec, text_dir)
    elif kind in ('raw_data', 'derived'):
        provenance = rec.get('provenance', {})
        artifacts = provenance.get('artifacts', [])
        if not artifacts:
            errors.append('raw/derived evidence requires provenance.artifacts')
        for artifact in artifacts:
            path = Path(root)/artifact.get('path', '')
            if not path.is_file():
                errors.append(f'provenance file missing: {artifact.get("path")}')
            elif not artifact.get('sha256') or artifact['sha256'] != sha256(path):
                errors.append(f'provenance hash missing/mismatched: {artifact.get("path")}')
        if kind == 'derived' and (not provenance.get('formula') or not provenance.get('inputs')):
            errors.append('derived evidence requires formula and input evidence keys')
        if not provenance.get('locator'):
            errors.append('raw/derived evidence requires a row, column, run or output locator')
    else:
        errors.append(f'unknown source_kind {kind}')
    if release:
        fields = ('entity', 'result_method', 'source_role', 'access_status') if rec.get('claim_type') == 'qualitative' else ('value', 'unit', 'metric', 'entity', 'result_method', 'source_role', 'access_status')
        for field in fields:
            if field not in rec or rec[field] is None or (field != 'unit' and rec[field] == ''):
                errors.append(f'missing evidence field {field}')
        if rec.get('result_method') not in ('measured','simulated','estimated','projected','inferred','synthetic'):
            errors.append('invalid result_method')
        if rec.get('source_role') not in ('primary','secondary','original'):
            errors.append('invalid source_role')
        if rec.get('access_status') not in ('full-text','abstract-only','raw-files'):
            errors.append('invalid access_status')
        if rec.get('verification') != 'verified':
            errors.append('evidence is not verified; do not set verified before checking the source/data')
        if kind == 'literature' and not rec.get('paper'):
            errors.append('literature evidence requires reference key paper')
    return errors

def load_evidence(folder):
    records = {}
    for file in sorted(Path(folder).glob('*.json')):
        for key, rec in iter_records(json.loads(file.read_text(encoding='utf-8'))):
            if key in records:
                raise ValueError(f'duplicate evidence key {key}')
            records[key] = rec
    return records

def audit_bindings(blocks, records, languages=('en',), release=False):
    errors, notices, checked = [], [], 0
    known_units = {unit(r.get('unit','')) for r in records.values()}
    for location, block, texts in blocks:
        claims = block.get('claims', [])
        covered = {lang: [] for lang in languages}
        for claim in claims:
            key = claim.get('evidence_key')
            if key not in records:
                errors.append(f'{location}: unknown evidence_key {key}')
                continue
            rec = records[key]
            checked += 1
            fields = ('entity', 'result_method') if claim.get('claim_type') == 'qualitative' else ('value', 'unit', 'metric', 'entity', 'result_method')
            for field in fields:
                if field not in claim:
                    errors.append(f'{location}/{key}: claim lacks {field}')
                    continue
                a, b = claim[field], rec.get(field)
                same = numeric_tokens(a) == numeric_tokens(b) if field == 'value' else (
                    unit(a) == unit(b) if field == 'unit' else a == b)
                if not same:
                    errors.append(f'{location}/{key}: {field} differs from its evidence record')
            for field in ('conditions', 'accounting_scope'):
                if rec.get(field) and claim.get(field) != rec[field]:
                    errors.append(f'{location}/{key}: {field} missing or differs from evidence')
            for lang in languages:
                text = texts.get(lang, '')
                anchor = claim.get('text', {}).get(lang, '')
                if not anchor:
                    errors.append(f'{location}/{key}: claim needs an exact text anchor for {lang}')
                    continue
                if anchor not in text:
                    errors.append(f'{location}/{key}: {lang} claim anchor absent from source text')
                expected = [(n, unit(claim.get('unit'))) for n in numeric_tokens(claim.get('value', ''))]
                actual = declared_quantities(anchor, known_units) if unit(claim.get('unit')) else [(n, '') for n in numeric_tokens(anchor)]
                # Numeric cells inherit an explicit unit from their real column header.
                numeric_cell = re.fullmatch(r'\s*'+NUMBER+r'(?:\s*[–—]\s*'+NUMBER+r')?\s*', scientific_notation(anchor))
                if block.get('table_cell') and numeric_cell and unit(claim.get('unit')) in header_units(block.get('unit_context', {}).get(lang, '')):
                    actual += [(n, unit(claim['unit'])) for n in numeric_tokens(anchor)]
                if any(q not in actual for q in expected):
                    errors.append(f'{location}/{key}: {lang} anchored value/unit differs from claim')
                covered[lang] += expected
                paper = rec.get('paper')
                if rec.get('source_kind', 'literature') == 'literature' and paper:
                    cited = re.findall(r'@([A-Za-z0-9_.:-]+)', anchor)
                    if paper not in cited:
                        errors.append(f'{location}/{key}: {lang} anchor lacks citation @{paper}')
        for lang, text in texts.items():
            if lang not in covered:
                continue
            found = declared_quantities(text, known_units)
            if block.get('table_cell') and re.fullmatch(r'\s*'+NUMBER+r'\s*', scientific_notation(text)):
                units = header_units(block.get('unit_context', {}).get(lang, ''))
                if len(units) <= 1:
                    found += [(n, next(iter(units), '')) for n in numeric_tokens(text)]
            unmatched = [q for q in found if q not in covered[lang]]
            if unmatched:
                message = f'{location}: {lang} quantities without bound evidence: {unmatched}'
                (errors if release else notices).append(message)
    return errors, notices, checked

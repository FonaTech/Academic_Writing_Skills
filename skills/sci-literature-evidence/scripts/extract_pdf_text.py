#!/usr/bin/env python3
"""Extract page-marked text and a reading digest from scientific PDFs.

Usage
  extract_pdf_text.py PDF_OR_DIR [PDF_OR_DIR ...] --out DIR [--digest] [--recursive]

For every unique PDF (duplicates are detected by SHA-256) this writes
  DIR/<id>.txt          full text with '=== PAGE n ===' markers (PDF page numbers, 1-based)
  DIR/<id>.digest.md    title, DOI, publisher, type guess, headings, abstract, opening of the
                        introduction, figure/table/box captions and the closing section (--digest)
  DIR/manifest.json     one record per PDF: id, path, sha256, pages, doi, publisher, type_guess

Quotes cited in evidence tables must come from the .txt file and carry the page marker in
which they appear. Ligatures are normalised; nothing else in the wording is changed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:  # pragma: no cover
    sys.exit('PyMuPDF is required: pip install pymupdf')

fitz.TOOLS.mupdf_display_errors(False)
try:
    fitz.TOOLS.mupdf_display_warnings(False)
except AttributeError:
    pass

LIGATURES = {'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl', 'ﬃ': 'ffi', 'ﬄ': 'ffl',
             'ﬅ': 'st', 'ﬆ': 'st', '­': '', '‐': '-', '‑': '-'}
DOI_RE = re.compile(r'\b(10\.\d{4,9}/[^\s"<>,;]+)', re.I)
PUBLISHERS = {
    '10.1038': 'Nature Portfolio', '10.1126': 'Science/AAAS', '10.1002': 'Wiley', '10.1021': 'ACS',
    '10.1109': 'IEEE', '10.3390': 'MDPI', '10.1039': 'RSC', '10.1016': 'Elsevier', '10.1088': 'IOP',
    '10.1007': 'Springer', '10.1080': 'Taylor & Francis', '10.1063': 'AIP', '10.1103': 'APS',
    '10.1145': 'ACM', '10.3389': 'Frontiers', '10.1186': 'BMC', '10.1371': 'PLOS', '10.1073': 'PNAS',
    '10.21203': 'Research Square', '10.48550': 'arXiv', '10.1117': 'SPIE', '10.1364': 'Optica',
    '10.35848': 'JSAP', '10.1049': 'IET', '10.34133': 'Science Partner Journals', '10.1515': 'De Gruyter',
}
REVIEW_RE = re.compile(r'\b(Review(?: Article)?|REVIEW|Perspective|PERSPECTIVE|Progress Report|Survey|Tutorial|Roadmap|Outlook)\b')
ARTICLE_RE = re.compile(r'\b(Article|ARTICLE|Letter|LETTER|Communication|Research Paper)\b')
CAPTION_RE = re.compile(r'^\s*((Fig(?:ure)?s?\.?|FIG\.?|FIGURE)\s*S?\d+|Table\s*S?\d+|TABLE\s*S?\d+|Box\s*\d+|BOX\s*\d+)\b')
CLOSING_RE = re.compile(r'^(\d+(\.\d+)*\.?\s*)?(Conclusions?|Outlook|Perspectives?|Summary|Concluding remarks|'
                        r'Discussion|Summary and outlook|Conclusions? and (outlook|perspectives?|prospects)|'
                        r'Challenges and (outlook|perspectives?|opportunities)|Future (directions|perspectives|outlook))\b', re.I)
INTRO_RE = re.compile(r'^(\d+(\.\d+)*\.?\s*)?(Introduction|INTRODUCTION|Background)\b')
REFS_RE = re.compile(r'^(References|REFERENCES|Bibliography|Reference)\s*$')


def clean(text: str) -> str:
    for a, b in LIGATURES.items():
        text = text.replace(a, b)
    return text


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def slug(text: str, limit: int = 60) -> str:
    return re.sub(r'[^A-Za-z0-9]+', '_', text).strip('_')[:limit] or 'doc'


def spans(page):
    try:
        data = page.get_text('dict')
    except Exception:
        return []
    out = []
    for block in data.get('blocks', []):
        for line in block.get('lines', []):
            text = ''.join(s.get('text', '') for s in line.get('spans', []))
            if not text.strip():
                continue
            sizes = [s.get('size', 0) for s in line.get('spans', []) if s.get('text', '').strip()]
            bold = any((s.get('flags', 0) & 16) or 'Bold' in s.get('font', '') for s in line.get('spans', []))
            out.append((clean(text).strip(), max(sizes) if sizes else 0, bold))
    return out


def detect_headings(doc, max_pages=60):
    lines = []
    for pno in range(min(len(doc), max_pages)):
        for text, size, bold in spans(doc[pno]):
            lines.append((pno + 1, text, round(size, 1), bold))
    if not lines:
        return []
    weights = Counter()
    for _, text, size, _ in lines:
        weights[size] += len(text)
    body = weights.most_common(1)[0][0]
    heads, seen = [], set()
    for pno, text, size, bold in lines:
        words = text.split()
        if not (1 <= len(words) <= 14) or len(text) < 3:
            continue
        if text.endswith(('.', ',', ';', '-', ':')) or CAPTION_RE.match(text):
            continue
        if text[0].islower() or re.search(r'[a-z]\d|\d,|&|@|\*', text):
            continue  # paragraph continuations and author/affiliation lines
        letters = sum(c.isalpha() for c in text)
        if letters < 0.6 * len(text.replace(' ', '')):
            continue
        if pno == 1 and not (INTRO_RE.match(text) or re.match(r'^(Abstract|ABSTRACT)$', text)):
            continue  # page 1 carries title, authors and abstract, not section headings
        if size >= body + 1.0 or (bold and size >= body - 0.2 and len(words) <= 10):
            key = text.lower()
            if key in seen:
                continue
            seen.add(key)
            heads.append({'page': pno, 'text': text, 'size': size, 'bold': bold})
    return heads[:120]


def page_texts(doc):
    return [clean(p.get_text('text')) for p in doc]


def blocks_text(page):
    try:
        return [clean(b[4]).strip() for b in page.get_text('blocks') if b[4].strip()]
    except Exception:
        return []


def words_after(text: str, anchor_re: re.Pattern, n_words: int):
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if anchor_re.match(line.strip()):
            chunk = ' '.join(lines[i + 1:i + 400])
            return ' '.join(chunk.split()[:n_words])
    return ''


AFFIL_RE = re.compile(r'\b(University|Universit[àäé]|Institute|Department|Laboratory|School of|College|'
                      r'Academy|Correspondence|e-mail|E-mail|Received|Accepted|Published|Copyright|©)\b')


def is_front_matter(flat: str) -> bool:
    """Author lists, affiliations and publication metadata rather than prose."""
    words = flat.split()
    if not words:
        return True
    if len(AFFIL_RE.findall(flat)) >= 2:
        return True
    tagged = sum(1 for w in words if re.search(r'[A-Za-z]\d|\d,\d|^\d+,?$|[*†‡§]', w))
    if tagged / len(words) > 0.12:
        return True
    if flat.count(',') > 0.2 * len(words) and sum(w[:1].isupper() for w in words) > 0.55 * len(words):
        return True
    return False


def prose_blocks(doc, first_page=1, last_page=None, min_words=60):
    """Paragraph-like text blocks (page, text), skipping captions, front matter and reference lists."""
    out = []
    last_page = last_page or len(doc)
    for pno in range(max(1, first_page), min(len(doc), last_page) + 1):
        for block in blocks_text(doc[pno - 1]):
            flat = ' '.join(block.replace('-\n', '').split())
            if len(flat.split()) < min_words or CAPTION_RE.match(flat) or is_front_matter(flat):
                continue
            if len(re.findall(r'\(\d{4}\)|\b\d{4};|doi\.org|et al\.', flat)) >= 3:
                continue  # reference-list block
            out.append((pno, flat))
    return out


def guess_abstract(doc, texts):
    first = '\n'.join(texts[:2])
    m = re.search(r'\b(Abstract|ABSTRACT)\b[:.\s]*(.+)', first, re.S)
    if m:
        return ' '.join(m.group(2).split()[:260]), None
    blocks = prose_blocks(doc, 1, min(2, len(doc)), min_words=80)
    if blocks:
        return ' '.join(blocks[0][1].split()[:260]), blocks[0][1]
    return '', None


def digest(doc, texts, rec):
    heads = detect_headings(doc)
    captions = []
    for pno, page in enumerate(doc, start=1):
        for block in blocks_text(page):
            if CAPTION_RE.match(block):
                captions.append({'page': pno, 'text': ' '.join(block.split())[:900]})
    full = '\n'.join(f'=== PAGE {i} ===\n{t}' for i, t in enumerate(texts, start=1))
    abstract, abstract_block = guess_abstract(doc, texts)
    intro = words_after(full, INTRO_RE, 450)
    if not intro:
        blocks = prose_blocks(doc, 1, min(3, len(doc)))
        after = [b for _, b in blocks if b != abstract_block]
        intro = ' '.join(' '.join(after).split()[:450])
    body = prose_blocks(doc, min(len(doc), max(1, len(doc) // 4)), min(len(doc), max(1, (3 * len(doc)) // 4)), min_words=110)
    samples = body[::max(1, len(body) // 4)][:4] if body else []
    closing, closing_head = '', ''
    for h in reversed(heads):
        if CLOSING_RE.match(h['text']):
            closing_head = h['text']
            closing = words_after(full, re.compile(re.escape(h['text'])), 650)
            break
    out = [f"# {rec['title_guess']}", '',
           f"- id: `{rec['id']}`", f"- file: `{rec['path']}`", f"- pages: {rec['pages']}",
           f"- DOI: {rec['doi'] or 'not found'}", f"- publisher: {rec['publisher']}",
           f"- type guess: {rec['type_guess']}", '']
    out += ['## Headings (page)', ''] + [f"- p{h['page']}: {h['text']}" for h in heads] + ['']
    out += ['## Abstract (first 260 words)', '', abstract or '(not detected)', '']
    out += ['## Introduction opening (450 words)', '', intro or '(not detected)', '']
    out += ['## Sample body paragraphs (middle half of the document)', '']
    out += [f'- p{p}: {t[:1600]}' for p, t in samples] or ['(none detected)']
    out += ['']
    out += ['## Figure, table and box captions', ''] + [f"- p{c['page']}: {c['text']}" for c in captions] + ['']
    out += [f'## Closing section: {closing_head or "(not detected)"} (650 words)', '', closing or '(not detected)', '']
    return '\n'.join(out), heads, captions


def title_guess(doc, texts):
    meta = (doc.metadata or {}).get('title') or ''
    if len(meta.split()) >= 4 and not meta.lower().endswith(('.pdf', '.doc', '.docx')):
        return clean(meta).strip()
    best, best_size = '', 0
    for text, size, _ in spans(doc[0]) if len(doc) else []:
        if len(text.split()) >= 3 and size > best_size:
            best, best_size = text, size
    return best or 'untitled'


def process(pdf: Path, out: Path, want_digest: bool, seen: dict):
    digest_hash = sha256(pdf)
    if digest_hash in seen:
        return None
    try:
        doc = fitz.open(pdf)
    except Exception as exc:
        return {'path': str(pdf), 'error': repr(exc)}
    texts = page_texts(doc)
    head = '\n'.join(texts[:2])
    m = DOI_RE.search(head)
    doi = m.group(1).rstrip('.)]') if m else ''
    prefix = doi.split('/')[0] if doi else ''
    rec = {
        'id': f"{slug(pdf.stem, 48)}_{digest_hash[:6]}",
        'path': str(pdf), 'sha256': digest_hash, 'pages': len(doc), 'doi': doi,
        'publisher': PUBLISHERS.get(prefix, 'unknown'),
        'type_guess': 'review' if REVIEW_RE.search(head[:3000]) else ('article' if ARTICLE_RE.search(head[:3000]) else 'unknown'),
        'title_guess': title_guess(doc, texts),
        'words': sum(len(t.split()) for t in texts),
    }
    seen[digest_hash] = rec['id']
    (out / f"{rec['id']}.txt").write_text(
        ''.join(f'\n=== PAGE {i} ===\n{t}' for i, t in enumerate(texts, start=1)), encoding='utf-8')
    if want_digest:
        md, heads, captions = digest(doc, texts, rec)
        (out / f"{rec['id']}.digest.md").write_text(md, encoding='utf-8')
        rec['headings'] = len(heads)
        rec['captions'] = len(captions)
    doc.close()
    return rec


def iter_pdfs(inputs, recursive):
    for item in inputs:
        p = Path(item).expanduser()
        if p.is_dir():
            yield from sorted(p.rglob('*.pdf') if recursive else p.glob('*.pdf'))
        elif p.suffix.lower() == '.pdf':
            yield p


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('inputs', nargs='+')
    ap.add_argument('--out', required=True)
    ap.add_argument('--digest', action='store_true')
    ap.add_argument('--recursive', action='store_true')
    args = ap.parse_args(argv)
    out = Path(args.out).expanduser()
    out.mkdir(parents=True, exist_ok=True)
    manifest_path = out / 'manifest.json'
    records = json.loads(manifest_path.read_text()) if manifest_path.exists() else []
    seen = {r['sha256']: r['id'] for r in records if 'sha256' in r}
    added = 0
    for pdf in iter_pdfs(args.inputs, args.recursive):
        rec = process(pdf, out, args.digest, seen)
        if rec:
            records.append(rec)
            added += 1
    manifest_path.write_text(json.dumps(records, ensure_ascii=False, indent=1), encoding='utf-8')
    errors = [r for r in records if 'error' in r]
    print(f'{added} new PDFs extracted; {len(records)} in manifest; {len(errors)} unreadable -> {out}')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())

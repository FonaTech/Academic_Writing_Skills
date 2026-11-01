#!/usr/bin/env python3
"""Verify and complete bibliographic records against Crossref.

Usage
  crossref_verify.py KEYS.json --out references_verified.json [--cache DIR] [--mailto ADDRESS]
  crossref_verify.py KEYS.json --out references_verified.json --emit-references references.json

KEYS.json maps a citation key to either a DOI string or a dict:
  {"pei2024": "10.1002/adma.202312783",
   "wu2018": {"doi": "10.1109/ISSCC.2018.8310399", "title": "Brain-inspired computing ..."},
   "farmer2021": {"manual": {"authors": "...", "year": 2021, "title": "...", "journal": "...", "doi": "..."}}}

For each key the script queries https://api.crossref.org/works/<DOI> (one request per
second, cached), records authors ("Surname AB"), title, container, year (print, else
online), volume, issue, pages or article number, and compares the returned title with the
claimed title (title_match = exact | near | mismatch). A DOI that resolves to a different
paper is flagged; the script then searches Crossref by title and proposes candidates.
Records with a "manual" entry are passed through and marked verified="manual".

--emit-references writes the database consumed by build_manuscript.py:
  {key: {authors, year, title, journal, volume, issue, pages, article_number, doi, verified}}
with authors condensed to six names plus "et al.".
Nothing is invented: missing fields stay empty and are listed in the report.
"""
from __future__ import annotations

import argparse
import difflib
import html
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

API = 'https://api.crossref.org/works/'
SEARCH = 'https://api.crossref.org/works?'


def norm_title(text):
    text = html.unescape(text or '')
    text = re.sub(r'<[^>]+>', '', text)
    return re.sub(r'[\W_]+', ' ', text.lower()).strip()


def similarity(a, b):
    if not a or not b:
        return 0.0
    return difflib.SequenceMatcher(None, norm_title(a), norm_title(b)).ratio()


def fetch(url, cache_dir: Path, mailto: str, pause: float):
    key = re.sub(r'[^A-Za-z0-9]+', '_', url)[-180:]
    path = cache_dir / f'{key}.json'
    if path.exists():
        return json.loads(path.read_text(encoding='utf-8'))
    req = urllib.request.Request(url, headers={'User-Agent': f'sci-literature-evidence/1.0 (mailto:{mailto})'})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode('utf-8'))
            path.write_text(json.dumps(data), encoding='utf-8')
            time.sleep(pause)
            return data
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                return None
            time.sleep(2 + 3 * attempt)
        except Exception:
            time.sleep(2 + 3 * attempt)
    return None


def clean(text):
    if not text:
        return None
    text = html.unescape(re.sub(r'<[^>]+>', '', text))
    return re.sub(r'\s+', ' ', text.replace('‐', '-').replace('‑', '-')).strip()


def author_name(a):
    family = a.get('family') or a.get('name') or ''
    given = a.get('given') or ''
    initials = ''.join(part[0] for part in re.split(r'[\s\-.]+', given) if part)
    return f'{family} {initials}'.strip()


def parse(msg):
    issued = (msg.get('published-print') or msg.get('published-online') or msg.get('issued') or {})
    year = (issued.get('date-parts') or [[None]])[0][0]
    pages = msg.get('page')
    number = msg.get('article-number')
    return dict(
        doi=msg.get('DOI'),
        title=clean((msg.get('title') or [''])[0]),
        authors=[author_name(a) for a in msg.get('author', [])],
        journal=clean((msg.get('container-title') or [''])[0]) or clean((msg.get('event') or {}).get('name')),
        year=year, volume=msg.get('volume'), issue=msg.get('issue'),
        pages=clean(pages.replace('-', '–')) if pages else None,
        article_number=clean(number) if number else None,
        type=msg.get('type'),
        post_publication_updates=msg.get('update-to', []),
        relations=msg.get('relation', {}),
        integrity_status='pending',
    )


def condense(authors, limit=6):
    if not authors:
        return ''
    return ', '.join(authors) if len(authors) <= limit else ', '.join(authors[:limit]) + ', et al.'


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('keys')
    ap.add_argument('--out', required=True)
    ap.add_argument('--emit-references')
    ap.add_argument('--cache', default='.crossref_cache')
    ap.add_argument('--mailto', default='research@example.org')
    ap.add_argument('--pause', type=float, default=1.0)
    args = ap.parse_args(argv)

    keys = json.loads(Path(args.keys).read_text(encoding='utf-8'))
    cache = Path(args.cache)
    cache.mkdir(parents=True, exist_ok=True)
    verified, report = {}, {'mismatch': [], 'unresolved': [], 'missing_fields': {}, 'manual': []}
    for key, spec in keys.items():
        spec = {'doi': spec} if isinstance(spec, str) else dict(spec)
        if 'manual' in spec:
            rec = dict(spec['manual'])
            rec['verified'] = 'manual'
            verified[key] = rec
            report['manual'].append(key)
            continue
        doi = spec.get('doi')
        data = fetch(API + urllib.parse.quote(doi, safe='/'), cache, args.mailto, args.pause) if doi else None
        if not data:
            report['unresolved'].append(key)
            verified[key] = {'doi': doi, 'verified': 'unresolved', 'claimed_title': spec.get('title')}
            continue
        rec = parse(data['message'])
        claimed = spec.get('title')
        sim = similarity(rec['title'], claimed) if claimed else None
        rec['title_similarity'] = round(sim, 3) if sim is not None else None
        rec['title_match'] = ('unchecked' if sim is None else 'exact' if norm_title(rec['title']) == norm_title(claimed) else 'near' if sim >= 0.55 else 'mismatch')
        rec['verified'] = 'crossref' if claimed and rec['title_match'] == 'exact' else 'identity-review-needed'
        if rec['title_match'] == 'mismatch':
            q = SEARCH + urllib.parse.urlencode({'query.bibliographic': claimed, 'rows': 5})
            found = fetch(q, cache, args.mailto, args.pause)
            cands = [parse(it) for it in ((found or {}).get('message', {}).get('items', []))]
            rec['candidates'] = [{'doi': c['doi'], 'title': c['title'], 'year': c['year'],
                                  'similarity': round(similarity(c['title'], claimed), 3)} for c in cands]
            report['mismatch'].append(key)
        missing = [f for f in ('authors', 'title', 'journal', 'year') if not rec.get(f)]
        if not (rec.get('pages') or rec.get('article_number')):
            missing.append('pages/article_number')
        if missing:
            report['missing_fields'][key] = missing
        verified[key] = rec
        print(f"{key:24s} {rec['title_match']:8s} {rec.get('year')} {rec.get('journal') or ''}"[:120])
    Path(args.out).write_text(json.dumps(verified, ensure_ascii=False, indent=2), encoding='utf-8')
    if args.emit_references:
        refs = {}
        for key, rec in verified.items():
            if rec.get('verified') == 'unresolved' or rec.get('title_match') == 'mismatch':
                continue  # never cite an unresolved or wrong-paper DOI; fix it in KEYS.json first
            authors = rec.get('authors')
            refs[key] = {k: v for k, v in dict(
                authors=condense(authors) if isinstance(authors, list) else authors,
                year=rec.get('year'), title=rec.get('title'), journal=rec.get('journal'),
                volume=rec.get('volume'), issue=rec.get('issue'), pages=rec.get('pages'),
                article_number=rec.get('article_number'), doi=rec.get('doi'),
                verified=rec.get('verified'),integrity_status=rec.get('integrity_status'),
                post_publication_updates=rec.get('post_publication_updates'),relations=rec.get('relations')).items() if v not in (None, '')}
        Path(args.emit_references).write_text(json.dumps(refs, ensure_ascii=False, indent=2), encoding='utf-8')
    print('\nmismatch:', report['mismatch'] or 'none')
    print('unresolved:', report['unresolved'] or 'none')
    print('manual:', report['manual'] or 'none')
    if report['missing_fields']:
        print('missing fields:', json.dumps(report['missing_fields'], ensure_ascii=False))
    pending = [key for key,rec in verified.items() if rec.get('verified') not in ('crossref','manual-checked')]
    if pending:
        print('identity review needed:', pending)
    return 1 if report['mismatch'] or report['unresolved'] or pending else 0


if __name__ == '__main__':
    sys.exit(main())

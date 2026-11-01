#!/usr/bin/env python3
"""Retrieve open-access full texts with identity checks and a persistent attempt log.

Usage
  fetch_open_access.py LIST.csv|LIST.json --out library/ [--email you@uni.edu] [--max-urls 10] [--only ID ...]

LIST rows need: id, title (optional: doi, year, venue, folder). Rows without DOI remain
visible as manual-required; this helper does not query DOI services with empty identifiers.
CSV may be the screening
sheet written by search_openalex.py (rows with decision = include are used when that column
is filled). Downloads run one at a time. Routes, in order: publisher open-access patterns,
OpenAlex locations, Unpaywall, Crossref full-text links, Europe PMC, Semantic Scholar, OpenAIRE,
and PDF links found on landing pages. A file is accepted only if
  - its normalized complete title is present, or a nonempty matching DOI accompanies
    fuzzy title ratio >= 84 and >= 75% title-token coverage (a candidate identity check, not final certification),
  - it is not supplementary material, has >= 2 pages, is not encrypted, has > 2500 characters of text,
  - its first and last pages render.
Every attempt is appended to OUT/download_attempts.jsonl; results go to OUT/library_status.csv
(UTF-8 BOM). Paywalls, captchas and publisher verification are never bypassed; closed papers are
listed with their entry points for library access.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import time
import unicodedata
from pathlib import Path
from urllib.parse import urljoin, quote

import fitz
import requests

try:
    from rapidfuzz.fuzz import partial_ratio
except ImportError:  # pragma: no cover
    from difflib import SequenceMatcher

    def partial_ratio(a, b):
        return 100 * max((SequenceMatcher(None, a, b[i:i + len(a)]).ratio() for i in range(0, max(1, len(b) - len(a) + 1), max(1, len(a) // 2))), default=0)

fitz.TOOLS.mupdf_display_errors(False)
UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126 Safari/537.36',
      'Accept': 'application/pdf,text/html,application/json,*/*'}
S = requests.Session()
S.headers.update(UA)


def norm(s):
    return ''.join(c for c in unicodedata.normalize('NFKC', s or '').casefold() if c.isalnum())


def slug(s, n=80):
    return re.sub(r'[^A-Za-z0-9]+', '_', s or '').strip('_')[:n]


def validate(path: Path, row):
    try:
        with fitz.open(path) as doc:
            if doc.page_count < 2 or doc.needs_pass:
                return False, 'fewer than 2 pages or encrypted'
            texts = [p.get_text() for p in doc]
            front = ' '.join(texts[:2])
            title_norm = norm(row.get('title', ''))
            if not title_norm:
                return False, 'missing title; manual identity check required'
            ratio = partial_ratio(title_norm, norm(front[:14000]))
            doi_norm = norm(row.get('doi', ''))
            doi_hit = bool(doi_norm) and doi_norm in norm(front)
            tokens = set(re.findall(r'[a-z]{4,}', row['title'].lower())) - {'with', 'from', 'based', 'using', 'review'}
            coverage = sum(t in front.lower().replace('-\n', '') for t in tokens) / max(1, len(tokens))
            exact_title = title_norm in norm(front[:14000])
            if not exact_title and not (doi_hit and ratio >= 84 and coverage >= 0.75):
                return False, f'title mismatch (fuzzy {ratio:.0f}, tokens {coverage:.2f}, DOI {doi_hit})'
            lead = ' '.join(texts[0].split())[:800].lower()
            if re.search(r'^(?:electronic )?supporting information|^supplementary|^electronic supplementary', lead):
                return False, 'supplementary material'
            if len(''.join(texts)) < 2500:
                return False, 'too little text (abstract page or scan)'
            for i in sorted({0, doc.page_count - 1}):
                if not doc[i].get_pixmap(matrix=fitz.Matrix(0.12, 0.12), alpha=False).samples:
                    return False, f'page {i + 1} does not render'
            return True, f'title match {ratio:.0f}; DOI {doi_hit}; {doc.page_count} pages'
    except Exception as exc:
        return False, f'invalid PDF: {str(exc)[:120]}'


def publisher_urls(row):
    d, urls = row['doi'], []
    if d.startswith('10.1038/'):
        urls.append(f'https://www.nature.com/articles/{d.split("/", 1)[1]}.pdf')
    elif d.startswith(('10.1007/', '10.1186/')):
        urls.append(f'https://link.springer.com/content/pdf/{d}.pdf')
    elif d.startswith('10.1021/'):
        urls.append(f'https://pubs.acs.org/doi/pdf/{d}')
    elif d.startswith('10.1002/'):
        urls.append(f'https://onlinelibrary.wiley.com/doi/pdfdirect/{d}')
    elif d.startswith('10.1039/'):
        urls.append(f'https://pubs.rsc.org/en/content/articlepdf/{row.get("year", "")}/{d.split("/")[-1]}')
    elif d.startswith('10.1088/'):
        urls.append(f'https://iopscience.iop.org/article/{d}/pdf')
    elif d.startswith('10.3390/'):
        urls.append(f'https://www.mdpi.com/{d}/pdf')
    elif d.startswith('10.1126/'):
        urls.append(f'https://www.science.org/doi/pdf/{d}')
    return urls


def api_json(url, params=None, log=None):
    try:
        r = S.get(url, params=params, timeout=25)
        if log is not None:
            log.append(dict(url=r.url[:300], status=r.status_code, kind='api'))
        return r.json() if r.ok else {}
    except Exception as exc:
        if log is not None:
            log.append(dict(url=url[:300], status=type(exc).__name__, kind='api'))
        return {}


def repository_urls(row, email, log):
    d, urls = row['doi'], []
    j = api_json('https://api.openalex.org/works/https://doi.org/' + d, log=log)
    for loc in j.get('locations', []) or []:
        urls += [loc.get('pdf_url'), loc.get('landing_page_url')]
    j = api_json(f'https://api.unpaywall.org/v2/{d}', {'email': email}, log)
    for loc in [j.get('best_oa_location')] + (j.get('oa_locations') or []):
        if loc:
            urls += [loc.get('url_for_pdf'), loc.get('url')]
    j = api_json('https://api.crossref.org/works/' + quote(d, safe='/'), log=log)
    urls += [ln.get('URL') for ln in (j.get('message') or {}).get('link', [])]
    j = api_json('https://www.ebi.ac.uk/europepmc/webservices/rest/search',
                 {'query': f'DOI:"{d}"', 'format': 'json', 'pageSize': 3}, log)
    for r in (j.get('resultList') or {}).get('result', []):
        if r.get('pmcid'):
            urls += [f'https://europepmc.org/articles/{r["pmcid"]}?pdf=render',
                     f'https://pmc.ncbi.nlm.nih.gov/articles/{r["pmcid"]}/pdf/']
    j = api_json('https://api.semanticscholar.org/graph/v1/paper/DOI:' + d, {'fields': 'openAccessPdf'}, log)
    urls.append((j.get('openAccessPdf') or {}).get('url'))
    return [u for u in dict.fromkeys(u for u in urls if isinstance(u, str) and u.startswith('http'))]


def html_pdf_links(text, base):
    urls = re.findall(r'<meta[^>]+name="citation_pdf_url"[^>]+content="([^"]+)"', text)
    for href in re.findall(r'href="([^"]+)"', text):
        if re.search(r'supplement|supporting|/suppl|esm|_si_', href, re.I):
            continue
        if '.pdf' in href.lower() or '/pdf/' in href.lower() or 'pdfdirect' in href.lower():
            urls.append(urljoin(base, href))
    return list(dict.fromkeys(urls))[:6]


def try_url(url, dest: Path, row, log):
    try:
        r = S.get(url, timeout=45, allow_redirects=True)
    except Exception as exc:
        log.append(dict(url=url[:300], status=type(exc).__name__, kind='download'))
        return False, []
    log.append(dict(url=url[:300], status=r.status_code, kind='download', ctype=r.headers.get('content-type', '')[:40]))
    if not r.ok:
        return False, []
    if r.content[:5] == b'%PDF-':
        tmp = dest.with_suffix('.part')
        tmp.write_bytes(r.content)
        ok, msg = validate(tmp, row)
        log[-1]['validation'] = msg
        if ok:
            tmp.replace(dest)
            return True, []
        tmp.unlink(missing_ok=True)
        return False, []
    if 'html' in r.headers.get('content-type', ''):
        head = r.text[:4000].lower()
        if re.search(r'captcha|challenge|cf-chl|verify you are human|proof.of.work|enable javascript|access denied', head):
            log[-1]['validation'] = 'bot-protection page (not bypassed); fetch this one by hand or through the library'
            return False, []
        return False, html_pdf_links(r.text, r.url)
    log[-1]['validation'] = 'not a PDF'
    return False, []


def load_rows(path: Path):
    if path.suffix == '.json':
        data = json.loads(path.read_text(encoding='utf-8'))
        rows = data if isinstance(data, list) else list(data.values())
    else:
        with path.open(encoding='utf-8-sig', newline='') as fh:
            rows = list(csv.DictReader(fh))
        if rows and 'decision' in rows[0] and any(r.get('decision') for r in rows):
            rows = [r for r in rows if (r.get('decision') or '').lower() in ('include', 'yes', 'y', '1', '纳入')]
    return [r for r in rows if r.get('title')]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('list')
    ap.add_argument('--out', default='library')
    ap.add_argument('--email', default='research@example.org', help='contact address for Unpaywall and polite API use')
    ap.add_argument('--max-urls', type=int, default=10)
    ap.add_argument('--pause', type=float, default=1.0)
    ap.add_argument('--only', nargs='*', help='ids to process')
    args = ap.parse_args(argv)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    rows = load_rows(Path(args.list))
    if args.only:
        rows = [r for r in rows if r.get('id') in set(args.only)]
    attempts = (out / 'download_attempts.jsonl').open('a', encoding='utf-8')
    status = []
    for i, row in enumerate(rows, 1):
        rid = row.get('id') or f'D{i:04d}'
        row['doi'] = re.sub(r'^https?://(?:dx\.)?doi\.org/', '', row.get('doi', '').strip(), flags=re.I).lower()
        if not row['doi']:
            status.append(dict(id=rid, doi='', title=row['title'], status='manual-required', file='',
                               note='No DOI; retrieve and verify the appropriate source manually. Record is retained.'))
            print(f'{rid:8s} --  no DOI; manual retrieval/identity check required')
            continue
        folder = out / (row.get('folder') or '')
        folder.mkdir(parents=True, exist_ok=True)
        dest = folder / f'{rid}_{slug(row["title"])}.pdf'
        if dest.exists() and validate(dest, row)[0]:
            status.append(dict(id=rid, doi=row['doi'], title=row['title'], status='present', file=str(dest), note=''))
            continue
        log, queue, tried, got = [], publisher_urls(row), set(), False
        queue += repository_urls(row, args.email, log)
        while queue and len(tried) < args.max_urls and not got:
            url = queue.pop(0)
            if url in tried:
                continue
            tried.add(url)
            got, found = try_url(url, dest, row, log)
            queue += [u for u in found if u not in tried]
            time.sleep(args.pause)
        for entry in log:
            attempts.write(json.dumps(dict(id=rid, doi=row['doi'], time=time.strftime('%Y-%m-%d %H:%M:%S'), **entry),
                                      ensure_ascii=False) + '\n')
        note = '' if got else f'{len(tried)} entry points tried; request via library: https://doi.org/{row["doi"]}'
        status.append(dict(id=rid, doi=row['doi'], title=row['title'], status='downloaded' if got else 'not retrieved',
                           file=str(dest) if got else '', note=note))
        print(f'{rid:8s} {"OK " if got else "-- "} {row["title"][:70]}')
    attempts.close()
    with (out / 'library_status.csv').open('w', encoding='utf-8-sig', newline='') as fh:
        wr = csv.DictWriter(fh, fieldnames=['id', 'doi', 'title', 'status', 'file', 'note'])
        wr.writeheader()
        wr.writerows(status)
    ok = sum(s['status'] in ('downloaded', 'present') for s in status)
    print(f'{ok}/{len(status)} full texts available -> {out}/library_status.csv')


if __name__ == '__main__':
    main()

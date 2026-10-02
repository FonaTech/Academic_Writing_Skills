#!/usr/bin/env python3
"""Run a query plan against OpenAlex and write a de-duplicated candidate list for screening.

Usage
  search_openalex.py PLAN.json --out search/ [--mailto you@uni.edu] [--per-query 100] [--api-key KEY]

OpenAlex now meters anonymous use per IP address; set OPENALEX_API_KEY (free key from
https://openalex.org) or pass --api-key when the shared budget is exhausted (HTTP 429).

PLAN.json
  {"from": "2018-01-01", "to": "2026-12-31",
   "types": ["review", "article"],                      # optional OpenAlex work types
   "must_any": ["urban biodiversity", "species richness"], # optional title/abstract filter
   "groups": {"urban_ecology": ["urban biodiversity monitoring", "urban species richness"],
              "methods": ["biodiversity sampling methods", "ecological observation bias"]}}

Outputs (in --out)
  search_cache/*.json     raw API pages (re-used on re-runs)
  search_results.json     unique works with groups hit, query ranks, abstract, OA links, citations
  candidates.csv          UTF-8-BOM table for screening in Excel (id, title, year, venue, type, DOI,
                          cited_by, groups, is_oa, oa_url, abstract)
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = 'https://api.openalex.org/works'


def fetch(params, cache: Path, mailto: str, api_key: str = ''):
    cache_params = {k: v for k, v in params.items() if k != 'api_key'}
    key = re.sub(r'[^A-Za-z0-9]+', '_', urllib.parse.urlencode(cache_params))[-200:]
    path = cache / f'{key}.json'
    if path.exists():
        return json.loads(path.read_text(encoding='utf-8'))
    if api_key:
        params = dict(params, api_key=api_key)
    url = API + '?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={'User-Agent': f'sci-literature-evidence/1.0 (mailto:{mailto})'})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=40) as resp:
                data = json.loads(resp.read().decode('utf-8'))
            path.write_text(json.dumps(data), encoding='utf-8')
            time.sleep(0.35)
            return data
        except urllib.error.HTTPError as exc:
            body = exc.read().decode('utf-8', 'replace')
            if exc.code == 429:
                try:
                    info = json.loads(body)
                except ValueError:
                    info = {}
                if 'budget' in info.get('message', '').lower():
                    raise SystemExit('OpenAlex: anonymous daily budget exhausted for this IP. Set OPENALEX_API_KEY '
                                     'or pass --api-key (free at https://openalex.org), or retry after midnight UTC.')
                time.sleep(int(info.get('retryAfter', 10)) + 2)
                continue
            print(f'  HTTP {exc.code}: {body[:200]}')
            time.sleep(2 + 4 * attempt)
        except Exception as exc:
            print(f'  {type(exc).__name__}: {exc}')
            time.sleep(2 + 4 * attempt)
    print(f'  failed after retries: {url[:140]}')
    return {'results': []}


def abstract(inv):
    if not inv:
        return ''
    words = [(p, w) for w, ps in inv.items() for p in ps]
    return ' '.join(w for _, w in sorted(words))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('plan')
    ap.add_argument('--out', default='search')
    ap.add_argument('--mailto', default='research@example.org')
    ap.add_argument('--per-query', type=int, default=100)
    ap.add_argument('--api-key', default=os.environ.get('OPENALEX_API_KEY', ''))
    ap.add_argument('--field', choices=['all', 'title_and_abstract', 'title'], default='title_and_abstract',
                    help='title_and_abstract (default) matches only titles and abstracts; all searches full text too')
    args = ap.parse_args(argv)
    plan = json.loads(Path(args.plan).read_text(encoding='utf-8'))
    out = Path(args.out)
    cache = out / 'search_cache'
    cache.mkdir(parents=True, exist_ok=True)
    filters = [f"from_publication_date:{plan.get('from', '2000-01-01')}",
               f"to_publication_date:{plan.get('to', '2100-12-31')}"]
    if plan.get('types'):
        filters.append('type:' + '|'.join(plan['types']))
    must = [m.lower() for m in plan.get('must_any', [])]
    works = {}
    for group, queries in plan['groups'].items():
        for q in queries:
            params = {'per-page': min(200, args.per_query), 'sort': 'relevance_score:desc', 'mailto': args.mailto}
            if args.field == 'all':
                params.update(search=q, filter=','.join(filters))
            else:
                safe_q = re.sub(r'[,|:;]+', ' ', q).strip()   # commas and pipes are filter separators
                params['filter'] = ','.join(filters + [f'{args.field}.search:{safe_q}'])
            data = fetch(params, cache, args.mailto, args.api_key)
            for rank, w in enumerate(data.get('results', []), 1):
                title = w.get('title') or ''
                abs_text = abstract(w.get('abstract_inverted_index'))
                if must and not any(m in (title + ' ' + abs_text).lower() for m in must):
                    continue
                doi = (w.get('doi') or '').replace('https://doi.org/', '').lower()
                key = doi or re.sub(r'\W+', '', title.lower())[:120]
                loc = w.get('primary_location') or {}
                src = loc.get('source') or {}
                oa = w.get('open_access') or {}
                rec = works.setdefault(key, dict(
                    doi=doi, title=title, year=w.get('publication_year'), venue=src.get('display_name', ''),
                    type=w.get('type', ''), cited_by=w.get('cited_by_count', 0), is_oa=oa.get('is_oa', False),
                    oa_url=oa.get('oa_url') or '', openalex=w.get('id', ''), abstract=abs_text,
                    authors='; '.join(a['author'].get('display_name', '') for a in w.get('authorships', [])
                                      if a.get('author')), groups=[], hits=[]))
                if group not in rec['groups']:
                    rec['groups'].append(group)
                rec['hits'].append([q, rank])
            print(f'{group:24s} {q[:60]:60s} total {len(works)}')
    rows = sorted(works.values(), key=lambda r: (-len(r['groups']), -(r['cited_by'] or 0)))
    for i, r in enumerate(rows, 1):
        r['id'] = f'S{i:04d}'   # S = search candidate; C### is reserved for comparators
    (out / 'search_results.json').write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding='utf-8')
    with (out / 'candidates.csv').open('w', encoding='utf-8-sig', newline='') as fh:
        wr = csv.writer(fh)
        wr.writerow(['id', 'title', 'year', 'venue', 'type', 'doi', 'cited_by', 'groups', 'is_oa', 'oa_url',
                     'decision', 'category', 'note_zh', 'abstract'])
        for r in rows:
            wr.writerow([r['id'], r['title'], r['year'], r['venue'], r['type'], r['doi'], r['cited_by'],
                         '|'.join(r['groups']), r['is_oa'], r['oa_url'], '', '', '', r['abstract'][:1500]])
    print(f'{len(rows)} unique works -> {out}/search_results.json, candidates.csv')


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Look up the reuse licence of papers whose figures you want to adapt.

Usage
  license_check.py DOI [DOI ...] [--out licences.csv] [--email you@uni.edu]
  license_check.py --from-sources Figures/*/sources.csv [--out licences.csv]

For each DOI the script reads licence URLs from Crossref (`license` field), the open-access
status and licence from Unpaywall, and the licence from Europe PMC when the paper is in PMC,
then proposes a reuse route:
  CC BY / CC BY-SA           reuse with attribution: "Adapted from ref. N under a CC BY 4.0 licence"
  CC BY-NC / NC-ND / ND      check the target journal: commercial publishers usually need permission
  publisher licence, closed  request permission (RightsLink or the publisher's permissions page)
  unknown                    check the article page by hand
The result is advice for the author, not legal advice; the article page is authoritative.
"""
from __future__ import annotations

import argparse
import csv
import glob
import re
import time
from urllib.parse import quote

import requests

S = requests.Session()
S.headers.update({'User-Agent': 'sci-literature-evidence/1.0'})


def classify(urls, oa_license):
    text = ' '.join(u.lower() for u in urls if u) + ' ' + (oa_license or '').lower()
    if re.search(r'by-nc-nd|by-nc|by-nd|cc-by-nc|cc-by-nd', text):
        return 'CC BY-NC/ND', 'check journal policy; permission is often needed for reuse in a commercial journal'
    if re.search(r'creativecommons\.org/licenses/by(-sa)?/|cc-by(-sa)?(\b|$)|\bcc by\b', text):
        return 'CC BY', 'reuse with attribution: "Adapted from ref. N under a CC BY 4.0 licence"'
    if re.search(r'publisher|tdm|elsevier\.com/tdm|springer\.com/tdm|wiley.*termsandconditions|acs\.org', text):
        return 'publisher', 'request permission (RightsLink or the publisher permissions page)'
    return 'unknown', 'check the article page by hand'


def lookup(doi, email):
    urls, oa = [], ''
    try:
        r = S.get('https://api.crossref.org/works/' + quote(doi, safe='/'), timeout=25)
        if r.ok:
            urls += [lic.get('URL', '') for lic in r.json()['message'].get('license', [])]
    except Exception:
        pass
    try:
        r = S.get(f'https://api.unpaywall.org/v2/{doi}', params={'email': email}, timeout=25)
        if r.ok:
            best = r.json().get('best_oa_location') or {}
            oa = best.get('license') or ''
    except Exception:
        pass
    try:
        r = S.get('https://www.ebi.ac.uk/europepmc/webservices/rest/search',
                  params={'query': f'DOI:"{doi}"', 'format': 'json', 'resultType': 'core', 'pageSize': 1}, timeout=25)
        if r.ok:
            for res in r.json().get('resultList', {}).get('result', []):
                oa = oa or res.get('license', '')
    except Exception:
        pass
    time.sleep(0.5)
    return urls, oa


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('dois', nargs='*')
    ap.add_argument('--from-sources', nargs='*', default=[])
    ap.add_argument('--out', default='licences.csv')
    ap.add_argument('--email', default='research@example.org')
    args = ap.parse_args(argv)
    dois = list(args.dois)
    for pattern in args.from_sources:
        for f in glob.glob(pattern):
            with open(f, encoding='utf-8-sig') as fh:
                dois += [r['doi'] for r in csv.DictReader(fh) if r.get('doi')]
    dois = list(dict.fromkeys(d.strip() for d in dois if d.strip()))
    rows = []
    for d in dois:
        urls, oa = lookup(d, args.email)
        label, route = classify(urls, oa)
        rows.append(dict(doi=d, licence=label, crossref_licence=' | '.join(u for u in urls if u), unpaywall_or_pmc=oa, route=route))
        print(f'{d:40s} {label:12s} {route}')
    with open(args.out, 'w', encoding='utf-8-sig', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]) if rows else ['doi'])
        w.writeheader()
        w.writerows(rows)
    print(f'{len(rows)} DOIs -> {args.out}')


if __name__ == '__main__':
    main()

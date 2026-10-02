#!/usr/bin/env python3
"""Lint scientific English (and basic Chinese) prose for expert-journal style.

Usage
  prose_lint.py FILE [FILE ...] [--json] [--limits FILE] [--max-words N] [--quiet]

FILE may be .txt, .md or .docx. Markdown code blocks, tables, block quotes, headings and reference
lists are skipped, and each list item is read as its own paragraph; for .docx the body paragraphs
are read and reference lists are skipped.

Caps, banned phrases and sentence targets come from ../assets/style_limits.json, the file the
manuscript kit's check_manuscript.py also reads. --limits takes another style_limits.json, a
manuscript.json (its style.overrides apply) or a {label: cap} map.

Reports
  - sentence-length profile (median, mean, share over the limit, share of very short sentences)
  - overlong sentences and paragraphs, stacked clauses (>= 3 of which/that/while/whereas ...)
  - banned phrases and capped words from style_limits.json, with the cap scaled to the text length
  - further vocabulary that reads as generated or promotional (see references/ai-flavor-lexicon.md)
  - hedging stacks, empty intensifiers, nominalisations, passive clusters, flagged openers,
    colons before a lowercase clause outside captions, sentence openers that repeat
  - meta-commentary about the manuscript itself
  - number hygiene: missing space before units, hyphen for minus in exponents, "10^-7" plain text,
    ranges written with "to" and a dash mixed, bare "~" approximations
  - abbreviation use before definition (first use without "(ABBR)")
  - Chinese: mixed half-/full-width punctuation, spaces missing between Chinese and Latin numbers
    are not flagged (house style allows both), repeated 的的, overlong Chinese sentences
Exit code is 0; this is an advisory tool. Use --json for machine-readable output.
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import style_limits as sl  # noqa: E402

DEFAULT_LIMITS = HERE.parent / 'assets' / 'style_limits.json'

# ----------------------------------------------------------------------------- lexicon
# Phrases that style_limits.json bans or caps are not repeated here. Weights follow
# references/ai-flavor-lexicon.md. All findings require context; vocabulary does not identify AI authorship.
LEGACY_LEXICON = {
    3: [r'\bin the ever[- ]evolving\b', r'\bunlock(s|ed|ing)? the (full )?potential\b', r'\ba testament to\b',
        r'\bnavigat(e|es|ing) the complex\b', r'\bmultifaceted\b', r'\bever[- ]growing demand\b', r'\bneedless to say\b',
        r'\bin today\'?s (world|era)\b', r'\bembark(s|ed|ing)? on\b', r'\bharness(es|ed|ing)? the power\b',
        r'\bsynerg(y|ies|istic)\b', r'\bholistic\b', r'\bboasts?\b', r'\bshowcas(e|es|ed|ing)\b', r'\bremarkabl[ey]\b',
        r'\bsuperior performance\b', r'\bexcellent performance\b', r'\boutstanding\b', r'\bimpressive(ly)?\b',
        r'\bexceptional(ly)?\b', r'\becosystems?\b', r'\bjourney\b'],
    2: [r'\butili[sz](e|es|ed|ing|ation)\b', r'\bfacilitat\w+', r'\bcomprehensive(ly)?\b', r'\brobust\b', r'\bnovel\b',
        r'\binnovative\b', r'\bpromising\b', r'\bsignificant(ly)?\b(?! (difference|at|p\s*<))', r'\bvarious\b',
        r'\bnumerous\b', r'\ba (wide|broad) (range|variety|spectrum) of\b', r'\bin order to\b', r'\bdue to the fact that\b',
        r'\bwith respect to\b', r'\bin terms of\b', r'\bat the same time\b', r'\bmoreover\b', r'\badditionally\b',
        r'\bin addition\b', r'\bconsequently\b', r'\bultimately\b', r'\bessentially\b', r'\bfundamentally\b',
        r'\binherently\b', r'\bvery\b', r'\bhighly\b', r'\bextremely\b', r'\bgreatly\b', r'\bdramatically\b',
        r'\btremendous(ly)?\b', r'\bemerg(ed|ing) as\b', r'\bgain(ed|ing)? (increasing|significant|considerable) attention\b',
        r'\battract(ed|ing)? (increasing|much|considerable|extensive) (attention|interest)\b', r'\bkey\b'],
    1: [r'\bhowever\b', r'\bin particular\b', r'\bindeed\b', r'\bclearly\b', r'\bobviously\b', r'\bof course\b',
        r'\bcan be seen\b', r'\bit is (clear|evident|obvious) that\b', r'\bin conclusion\b', r'\boverall\b',
        r'\bto (be|this) end\b', r'\bin recent years\b', r'\bwith the (rapid )?development of\b', r'\bframework\b',
        r'\bstep change\b'],
}
LEXICON = {1: [], 2: [], 3: []}
META = [r'\bas (mentioned|discussed|noted|stated) (above|earlier|previously|before)\b',
        r'\bin this (section|chapter|subsection), we (will )?(discuss|describe|present|introduce)\b',
        r'\bthe (following|next) (section|subsection)s? (will )?(discuss|describe|present)\b',
        r'\bit is (important|essential|necessary) to (note|mention|emphasi[sz]e)\b',
        r'\blet us\b', r'\bwe (would like|want) to\b', r'\bthe reader\b', r'\bhere(in)?, we (briefly )?(summari[sz]e|review)\b',
        r'\blocal (corpus|library)\b', r'\bextracted (record|text)\b']
HEDGE = re.compile(r'\b(may|might|could|possibly|potentially|perhaps|likely|appears? to|seems? to|suggests?|to some extent|somewhat|relatively)\b', re.I)
INTENSIFIER = re.compile(r'\b(very|highly|extremely|greatly|significantly|substantially|considerably|dramatically|remarkably|incredibly|truly|really)\b', re.I)
NOMINAL = re.compile(r'\b(the )?(implementation|utili[sz]ation|realization|realisation|enhancement|optimization|optimisation|improvement|investigation|examination|determination|evaluation|achievement|reduction|demonstration) of\b', re.I)
PASSIVE = re.compile(r'\b(is|are|was|were|be|been|being)\s+(\w+ly\s+)?\w+(ed|en)\b', re.I)
CLAUSE = re.compile(r'\b(which|that|while|whereas|although|because|since|whose|where|when)\b', re.I)
LIST3 = re.compile(r'\b\w+(?:\s\w+)?, \w+(?:\s\w+)?,? and \w+(?:\s\w+)?\b')   # counted only; lists of facts are fine
CAPTION = re.compile(r'^(Supplementary\s+)?(Fig(ure)?s?\.?|Table|Box|图|表|专栏)\s*S?\d+', re.I)
UNITS = r'(nm|µm|um|mm|cm|m|ns|µs|us|ms|s|Hz|kHz|MHz|GHz|THz|V|mV|µV|A|mA|µA|nA|pA|W|mW|µW|nW|pW|J|mJ|µJ|nJ|pJ|fJ|aJ|Ω|kΩ|MΩ|S|mS|µS|K|°C|eV|meV|dB|bit|bits|b|TOPS|GOPS|%|F|pF|fF|nF)'
NUM_UNIT = re.compile(rf'\b\d+(?:\.\d+)?{UNITS}\b')
PLAIN_EXP = re.compile(r'\b10\^-?\d+|\b10\^\{?-')
TILDE = re.compile(r'(?<!\S)~\s?\d')
ABBR_DEF = re.compile(r'\(([A-Z][A-Za-z0-9\-/]{1,9}s?)\)')
# caption and table-note convention: 'ADC, analog-to-digital converter;'
ABBR_DEF_NOTE = re.compile(r'(?:^|[;.]\s)([A-Z][A-Za-z0-9\-/]{1,9}), [a-z][a-z\- ]{3,80}(?=[;.])')
ABBR_USE = re.compile(r'(?<![\w\-/])([A-Z][A-Z0-9]{1,7}s?)(?![\w\-/])')
ABBR_SKIP = {'EN','ZH','CN','I','II','III','IV','V','VI','VII','VIII','IX','X','PDF','ID','SI','OK','PhD','MSc','BSc','US','UK','EU','USA','Hz','kHz','MHz','GHz','THz'}


def read(path: Path) -> list[str]:
    if path.suffix.lower() == '.docx':
        from docx import Document
        paras, in_refs = [], False
        for p in Document(path).paragraphs:
            t = p.text.strip()
            if not t:
                continue
            if p.style.name.lower().startswith('heading'):
                in_refs = t.lower() in ('references', 'bibliography', '参考文献')
                continue
            if not in_refs:
                paras.append(t)
        return paras
    text = path.read_text(encoding='utf-8', errors='replace')
    text = re.sub(r'```.*?```', '', text, flags=re.S)
    paras, buf, in_refs = [], [], False
    for line in text.splitlines():
        s = line.strip()
        if s.startswith('#'):
            in_refs = bool(re.match(r'#+\s*(references|bibliography|参考文献)', s, re.I))
            if buf:
                paras.append(' '.join(buf)); buf = []
            continue
        if not s or s.startswith('|') or s.startswith('>'):
            if buf:
                paras.append(' '.join(buf)); buf = []
            continue
        item = re.match(r'(?:[-*+]|\d+[.)])\s+', s)
        if item:                                    # each list item is its own unit
            if buf:
                paras.append(' '.join(buf)); buf = []
            s = s[item.end():]
        if not in_refs:
            buf.append(s)
    if buf:
        paras.append(' '.join(buf))
    return paras


def is_chinese(text: str) -> bool:
    han = len(re.findall(r'[一-鿿]', text))
    return han > 0.3 * max(1, len(re.sub(r'\s', '', text)))


def clean(text: str) -> str:
    text = re.sub(r'\[\s*\d+(?:\s*[,–-]\s*\d+)*\s*\]', '', text)      # numeric citations
    text = re.sub(r'\[@[^\]]+\]', '', text)
    text = re.sub(r'\{(fig|tab|eq|sec|box):[^}]+\}', 'Fig. 1', text)
    text = re.sub(r'\$[^$]*\$', 'X', text)
    return re.sub(r'\s+', ' ', text).strip()


def sentences_en(text: str) -> list[str]:
    protected = re.sub(r'\b(et al|e\.g|i\.e|Fig|Figs|Eq|Eqs|Ref|Refs|vs|approx|ca|cf|No|no|Vol|vol|pp|p|'
                       r'Nat|Commun|Rev|Chem|Phys|Mater|Appl|Lett|Adv|Electron|Photon|Sci|Soc|Proc|Technol|Eng|Bull)\.',
                       lambda m: m.group(0).replace('.', '§'), text)
    protected = re.sub(r'(\d)\.(\d)', r'\1§\2', protected)
    parts = re.split(r'(?<=[.!?\]])\s+(?=[A-Z0-9(“"\[])', protected)   # a bracketed note after a sentence starts a new one
    return [p.replace('§', '.').strip() for p in parts if len(p.split()) >= 3]


def sentences_zh(text: str) -> list[str]:
    return [s for s in re.split(r'(?<=[。！？；])', text) if len(s.strip()) > 4]


def read_limits(arg=None, profile=None):
    """style_limits.json by default; --limits may name another one, a manuscript.json or a {label: cap} map."""
    if not arg:
        return sl.load(sl.profile_path(DEFAULT_LIMITS.parent,profile or 'precise'))
    data = json.loads(Path(arg).read_text(encoding='utf-8'))
    if 'caps' in data or 'banned' in data:
        return sl.apply_overrides(data, {})
    if 'style' in data:
        name = profile or data['style'].get('profile','precise')
        local = Path(arg).resolve().parent
        folder = local if (local/'style_profiles').is_dir() else DEFAULT_LIMITS.parent
        return sl.load(sl.profile_path(folder,name), data['style'].get('overrides', {}))
    return sl.load(DEFAULT_LIMITS, data)


def lint(paths, max_words=None, limits=None):
    limits = limits or read_limits()
    target = limits['sentence']
    max_words = max_words or target['max_words']
    findings, lengths, openers = [], [], Counter()
    abbr_defined, abbr_first = set(), {}
    counts, capped, advisory = Counter(), {}, {}
    zh_lengths, en_words = [], 0
    for path in paths:
        for pi, para in enumerate(read(Path(path)), start=1):
            loc = f'{Path(path).name}:¶{pi}'
            if is_chinese(para):
                for s in sentences_zh(clean(para)):
                    n = len(re.sub(r'\s', '', s))
                    zh_lengths.append(n)
                    if n > 90:
                        findings.append((2, loc, 'zh-long-sentence', f'{n} characters: {s[:60]}…'))
                if re.search(r'[一-鿿][,;:?!](?=[一-鿿])', para):
                    findings.append((1, loc, 'zh-halfwidth-punct', 'half-width punctuation between Chinese characters'))
                if '的的' in para:
                    findings.append((2, loc, 'zh-repeat', '的的'))
                continue
            text = clean(para)
            words = len(text.split())
            en_words += words
            if words > target['paragraph_max_words']:
                findings.append((2, loc, 'long-paragraph', f'{words} words; split where the topic changes'))
            banned_spans = []
            for entry, m in sl.banned_hits(limits, text):
                banned_spans.append((m.start(), m.end()))
                findings.append((3, loc, 'banned', f'"{m.group(0)}" ({entry["label"]}): {entry["fix"]}'))
            for entry, m in sl.find(limits.get('caps', []), text):
                capped.setdefault(entry['label'], [entry, []])[1].append(loc)
            if not CAPTION.match(para):
                for entry, m in sl.find(limits.get('advisory', []), text):
                    advisory.setdefault(entry['label'], [entry, []])[1].append(loc)
            for d in ABBR_DEF.findall(text) + ABBR_DEF_NOTE.findall(text):
                for part in d.split('/'):
                    abbr_defined.add(part.rstrip('s'))
            for u in ABBR_USE.findall(text):
                base = u.rstrip('s')
                if base in ABBR_SKIP or len(base) < 2:
                    continue
                if base not in abbr_defined and base not in abbr_first:
                    abbr_first[base] = loc
            for s in sentences_en(text):
                n = len(s.split())
                lengths.append(n)
                first = s.split()[0].rstrip(',')
                openers[first] += 1
                if n > max_words:
                    findings.append((2, loc, 'long-sentence', f'{n} words: {s[:100]}…'))
                clauses = len(CLAUSE.findall(s))
                if clauses >= 3:
                    findings.append((2, loc, 'stacked-clauses', f'{clauses} subordinators: {s[:100]}…'))
                if len(HEDGE.findall(s)) >= 2:
                    findings.append((1, loc, 'hedge-stack', s[:110]))
                if len(PASSIVE.findall(s)) >= 3:
                    findings.append((1, loc, 'passive-cluster', s[:110]))
                hit = sl.opener_hits(limits, s)
                if hit:
                    weight, label, fix = hit
                    findings.append((weight, loc, 'opener', f'{label}: {fix}'))
            for weight, pats in LEXICON.items():
                for pat in pats:
                    for m in re.finditer(pat, text, flags=re.I):
                        if any(a <= m.start() < b for a, b in banned_spans):
                            continue
                        counts[m.group(0).lower()] += 1
                        if weight >= 2:
                            findings.append((weight, loc, 'lexicon', f'"{m.group(0)}"'))
            for pat in META:
                for m in re.finditer(pat, text, flags=re.I):
                    findings.append((3, loc, 'meta-commentary', f'"{m.group(0)}"'))
            counts['nominalisation'] += len(NOMINAL.findall(text))
            counts['intensifier'] += len(INTENSIFIER.findall(text))
            counts['three-item list'] += len(LIST3.findall(text))
            for m in NUM_UNIT.finditer(text):
                findings.append((1, loc, 'unit-spacing', f'"{m.group(0)}" needs a space before the unit'))
            for m in PLAIN_EXP.finditer(text):
                findings.append((1, loc, 'plain-exponent', f'"{m.group(0)}" should be a superscript with a minus sign'))
            for m in TILDE.finditer(text):
                findings.append((1, loc, 'tilde', f'"{m.group(0)}" use "about" or "≈"'))
    stats = {}
    if lengths:
        stats = dict(sentences=len(lengths), median=statistics.median(lengths),
                     mean=round(statistics.mean(lengths), 1), max=max(lengths),
                     over_limit=sum(n > max_words for n in lengths),
                     short_le8=sum(n <= 8 for n in lengths),
                     share_over_limit=round(sum(n > max_words for n in lengths) / len(lengths), 3),
                     share_short=round(sum(n <= 8 for n in lengths) / len(lengths), 3))
    if zh_lengths:
        stats['zh_sentences'] = len(zh_lengths)
        stats['zh_median_chars'] = statistics.median(zh_lengths)
    if len(lengths) >= 20 and not target['median_min'] <= stats['median'] <= target['median_max']:
        findings.append((2, 'all', 'median-length',
                         f'median {stats["median"]} words; target {target["median_min"]}-{target["median_max"]}'))
    for word, n in openers.most_common(8):
        if n >= 5 and word not in ('The', 'A', 'An', 'This', 'These', 'In', 'For', 'Its', 'Each', 'We'):
            findings.append((1, 'all', 'repeated-opener', f'{n} sentences start with "{word}"'))
    ref = limits.get('reference_words', 10000)
    for weight, group in ((2, capped), (1, advisory)):
        for label, (entry, locs) in group.items():
            counts[label] = len(locs)
            cap = sl.scaled_cap(entry, en_words, ref)
            if len(locs) > cap:
                where = ', '.join(dict.fromkeys(locs))
                findings.append((weight, 'all', 'cap' if weight == 2 else 'advisory',
                                 f'{label} ×{len(locs)} (cap {cap:g} for {en_words} words): {entry["fix"]}; at {where[:160]}'))
    stats['english_words'] = en_words
    undefined = {a: loc for a, loc in abbr_first.items()}
    return stats, findings, counts, undefined


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('files', nargs='+')
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--limits', help='style_limits.json, manuscript.json or {label: cap} map (default: '
                                     '../assets/style_limits.json)')
    ap.add_argument('--max-words', type=int, default=None, help='sentence ceiling (default from the limits file)')
    ap.add_argument('--profile',choices=['precise','generic','explanatory','compact'],help='precise is the default; override a project profile')
    ap.add_argument('--quiet', action='store_true', help='summary only')
    args = ap.parse_args(argv)
    stats, findings, counts, undefined = lint(args.files, args.max_words, read_limits(args.limits,args.profile))
    if args.json:
        print(json.dumps(dict(stats=stats, findings=[dict(weight=w, where=l, kind=k, detail=d) for w, l, k, d in findings],
                              counts=counts, abbreviations_without_definition=undefined), ensure_ascii=False, indent=2))
        return 0
    print('Sentence profile:', ', '.join(f'{k} {v}' for k, v in stats.items()))
    score = sum(w for w, *_ in findings)
    print(f'Findings: {len(findings)} (weighted {score})')
    if not args.quiet:
        for w, loc, kind, detail in sorted(findings, key=lambda f: (-f[0], f[1])):
            print(f'  [{w}] {loc:18s} {kind:18s} {detail}')
    top = [f'{k} ×{v}' for k, v in counts.most_common(15) if v]
    if top:
        print('Most frequent flagged items:', '; '.join(top))
    if undefined:
        print('Abbreviations used before a definition "(ABBR)" (names of chips, products and datasets need none):',
              ', '.join(f'{a} ({loc})' for a, loc in list(undefined.items())[:25]))
    return 0


if __name__ == '__main__':
    sys.exit(main())

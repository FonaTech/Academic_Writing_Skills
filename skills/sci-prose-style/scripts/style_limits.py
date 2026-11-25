"""Shared style limits: load style_limits.json, apply project overrides, count caps and banned phrases.

prose_lint.py (sci-prose-style) and check_manuscript.py (manuscript kit) both import this module.
The two copies of this file and of style_limits.json must stay identical; tools/validate_skills.py
checks that.

Overrides are keyed by entry label. A number sets the cap of a capped or advisory entry, null
switches an entry off, and the sentence keys median_min, median_max, max_words and
paragraph_max_words replace the sentence targets. A key that matches no label is read as a
legacy {regex: cap} pair and added as a cap.
"""
from __future__ import annotations

import copy
import json
import re
from pathlib import Path

GROUPS = ('caps', 'banned', 'banned_openers', 'advisory')
SENTENCE_KEYS = ('median_min', 'median_max', 'max_words', 'paragraph_max_words')


def profile_path(folder, name='precise'):
    name = {'group':'precise'}.get(name,name)  # compatibility alias
    if name not in ('precise','generic','explanatory','compact'):
        raise ValueError('unknown style profile: '+str(name))
    selected = Path(folder)/'style_profiles'/f'{name}.json'
    if selected.is_file():
        return selected
    if name == 'precise':
        return Path(folder)/'style_limits.json'
    raise FileNotFoundError(selected)


def load(path, overrides=None):
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    return apply_overrides(data, overrides or {})


def apply_overrides(limits, overrides):
    out = copy.deepcopy(limits)
    for key, value in overrides.items():
        if key in SENTENCE_KEYS:
            out['sentence'][key] = value
            continue
        hit = False
        for group in GROUPS:
            for entry in list(out.get(group, [])):
                if entry['label'] != key:
                    continue
                hit = True
                if value is None:
                    out[group].remove(entry)
                elif 'max' in entry:
                    entry['max'] = value
        if not hit and value is not None:
            re.compile(key)
            out.setdefault('caps', []).append(dict(label=key, pattern=key, max=value, source='project', fix=''))
    return out


def scaled_cap(entry, words, reference_words):
    """Caps hold unchanged up to reference_words and grow in proportion above it (rounded down)."""
    return int(entry['max'] * max(1.0, words / max(1, reference_words)))


def find(entries, text):
    """Yield (entry, match) for every match of every entry in text."""
    for entry in entries:
        for m in re.finditer(entry['pattern'], text, flags=re.I):
            yield entry, m


def banned_hits(limits, text):
    """Banned matches in text; a match inside a longer one ('crucial' in 'plays a crucial role') is dropped."""
    hits = sorted(find(limits.get('banned', []), text), key=lambda h: (h[1].start(), h[1].start() - h[1].end()))
    kept, end = [], -1
    for entry, m in hits:
        if m.end() <= end:
            continue
        kept.append((entry, m))
        end = m.end()
    return kept


def opener_hits(limits, sentence):
    """(weight, label, fix) for a banned opener (3) or a flagged opener (2) at the start of sentence."""
    for entry in limits.get('banned_openers', []):
        if re.match(entry['pattern'], sentence, flags=re.I):
            return 3, entry['label'], entry['fix']
    for word in limits.get('flagged_openers', []):
        if re.match(rf'{re.escape(word)}\b', sentence):
            return 2, f'"{word}" opener', 'start with the subject; the content should carry the weight'
    return None


# ------------------------------------------------------------------ line of thought
# Regularities that make prose read as generated (sci-prose-style references/human-line-of-thought.md).
# The writer's reasoning orders the paragraph; the text does not voice it, and no device repeats on every sentence.
EMBEDDED_Q = re.compile(r'^(How|Why|What|Whether|Which|Where)\b', re.I)
THINK_ALOUD = re.compile(r'\b(the (open |real |key |central )?question (is|was|here|remains)|the answer (is|lies)|'
                         r'what matters (here |most )?is|it remains to be seen|one (may|might|could) ask|'
                         r'we (may|might) ask|the key (is|lies)|the catch is|the point is)\b', re.I)
ORDINAL_ENUM = re.compile(r'^(In the (first|second|third|fourth)\b|The (remaining|other) (two|three|four)\b|'
                          r'(Two|Three|Four) of (them|these)\b)', re.I)
EXPLAIN = re.compile(r'\b(because|since|so|which|that|therefore|thus|hence|as a result|owing to|due to|'
                     r'however|but|whereas|although|though|while|yet|instead|compared|than|attribut\w*|traced|'
                     r'means?|meaning|explain\w*|caus\w*|so that|until|unless|when|if|once|as long as|provided)\b', re.I)
EXPLAIN_CONN = re.compile(r'\bso\b(?!-called)|\bbecause\b|\bsince\b|\bthen\b|\btherefore\b|\bthus\b|\bhence\b', re.I)
FLOAT_REF = re.compile(r'\b(Figs?\.|Fig(ure)?s?|Table|Section|Box|[Ee]quation|Eq\.)\s*\(?\d+[a-z]?\)?(\.\d+)*')


def has_number(sentence):
    return bool(re.search(r'\d', FLOAT_REF.sub('', sentence)))


def number_runs(sents, run=3):
    """Runs of `run` or more sentences that each carry a number and no explanatory or contrastive word."""
    out, cur = [], []
    for s in sents:
        if has_number(s) and not EXPLAIN.search(s):
            cur.append(s)
            continue
        if len(cur) >= run:
            out.append(cur)
        cur = []
    if len(cur) >= run:
        out.append(cur)
    return out


def uniform(rhythm, lens, key):
    """True when a paragraph has enough sentences and all their lengths sit within the rhythm range."""
    n = rhythm.get('min_sentences', 5)
    return bool(rhythm) and len(lens) >= n and max(lens) - min(lens) <= rhythm.get(key, 8)


def sentences_zh(text):
    return [s for s in re.split(r'(?<=[。！？；?])', text) if re.search(r'[一-鿿A-Za-z0-9]', s)]


def line_of_thought_en(limits, sents):
    """(weight, kind, detail) for one English body paragraph, given its sentences."""
    out, rhythm = [], limits.get('rhythm', {})
    if uniform(rhythm, [len(s.split()) for s in sents], 'max_range'):
        out.append((1, 'uniform-rhythm', f'{len(sents)} sentences of nearly equal length; {rhythm.get("fix", "")}'))
    for r in number_runs(sents):
        out.append((2, 'number-run', f'{len(r)} number sentences in a row with no reason or comparison; say what the '
                                     f'numbers show or move some to a table: {" ".join(r)[:100]}…'))
    for s in sents:
        if s.rstrip().endswith('?') or EMBEDDED_Q.match(s):
            out.append((2, 'question-voice', f'question or embedded question; state the finding directly: {s[:100]}…'))
        hit = THINK_ALOUD.search(s)
        if hit:
            out.append((2, 'thinking-aloud', f'"{hit.group(0)}"; give the content, not the reasoning step'))
        hit = ORDINAL_ENUM.match(s)
        if hit:
            out.append((1, 'ordinal-enumeration', f'counted list ("{hit.group(0)}"); name the groups by what separates '
                                                  f'them: {s[:80]}…'))
        if len(s.split()) <= 5 and not re.search(r'\d', s) and len(sents) > 2:
            out.append((1, 'aphorism', f'short verdict sentence "{s}"; attach the judgement to its evidence'))
    return out


def line_of_thought_zh(limits, para, sents):
    """(weight, kind, detail, matched text or None) for one Chinese body paragraph."""
    conf, rhythm, out = limits.get('zh', {}), limits.get('rhythm', {}), []
    lens = [len(re.sub(r'\s', '', s)) for s in sents]
    for entry in conf.get('template', []):
        for m in re.finditer(entry['pattern'], para):
            out.append((2, 'zh-template', f'"{m.group(0)}"（{entry["label"]}）：{entry["fix"]}', m.group(0)))
    conn = conf.get('connective')
    if conn and len(sents) >= conn.get('min_sentences', 4):
        hit = [s for s in sents if re.search(conn['pattern'], s)]
        if len(hit) / len(sents) > conn.get('max_share', 0.4):
            out.append((1, 'zh-connective', f'{len(hit)}/{len(sents)} 句含因此、从而、进而一类连接词：{conn["fix"]}', None))
    if conf.get('question'):
        for s in sents:
            if re.search(conf['question'], s.strip().rstrip('。；')):
                out.append((2, 'zh-question', f'{conf.get("question_fix", "")}：{s.strip()[:50]}…', None))
    if conf.get('ordinal') and re.search(conf['ordinal'], para):
        out.append((1, 'zh-ordinal', conf.get('ordinal_fix', ''), None))
    if uniform(rhythm, lens, 'max_range_zh'):
        out.append((1, 'zh-uniform-rhythm', f'{len(sents)} 句长度相近（{min(lens)}–{max(lens)} 字）；'
                                             f'机理与条件用长句，单纯的结果用短句', None))
    return out


def zh_connective_hits(limits, sents):
    pattern = limits.get('zh', {}).get('connective', {}).get('pattern')
    return sum(1 for s in sents if pattern and re.search(pattern, s))


def explanation_count(text):
    """Count occurrences, not just sentences containing a connective."""
    return len(EXPLAIN_CONN.findall(text))


def zh_explanation_count(limits, text):
    pattern = limits.get('zh', {}).get('connective', {}).get('pattern')
    return len(re.findall(pattern, text)) if pattern else 0

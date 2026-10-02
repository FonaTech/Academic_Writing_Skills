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

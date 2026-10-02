"""Rendering core for repeatable scientific Word construction.

Markup parsing, citation and float resolution, rich-text runs and document defaults.
Numbering and rendering live in build_manuscript.py.

Content lives in content.py (blocks) and floats.py (figures, tables, boxes) and uses a small markup:
  [@cite_key; @other_key]   citation
  {fig:key}  {fig:key|b}    figure or panel reference
  {tab:key}                 table reference
  {eq:key}                  equation reference
  {sec:id}  {box:name}      section or box reference (numbered automatically)
  $G_{ij}$                  inline math: _{...} subscript, ^{...} superscript,
                            single asterisks for italic, \alpha and friends for
                            Greek symbols
  **bold**  *italic*        emphasis outside math
"""
from __future__ import annotations

import re
from pathlib import Path

from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt, RGBColor
from docx.oxml.ns import qn

# --------------------------------------------------------------------------
# Greek and symbol table for inline math
# --------------------------------------------------------------------------
SYMBOLS = {
    r'\alpha': 'α', r'\beta': 'β', r'\gamma': 'γ', r'\Gamma': 'Γ', r'\delta': 'δ',
    r'\Delta': 'Δ', r'\epsilon': 'ε', r'\varepsilon': 'ε', r'\zeta': 'ζ', r'\eta': 'η',
    r'\theta': 'θ', r'\Theta': 'Θ', r'\iota': 'ι', r'\kappa': 'κ', r'\lambda': 'λ',
    r'\Lambda': 'Λ', r'\mu': 'μ', r'\nu': 'ν', r'\xi': 'ξ', r'\pi': 'π', r'\Pi': 'Π',
    r'\rho': 'ρ', r'\sigma': 'σ', r'\Sigma': 'Σ', r'\tau': 'τ', r'\upsilon': 'υ',
    r'\phi': r'\varphi' and 'φ', r'\Phi': 'Φ', r'\chi': 'χ', r'\psi': 'ψ', r'\Psi': 'Ψ',
    r'\omega': 'ω', r'\Omega': 'Ω',
    r'\times': '×', r'\approx': '≈', r'\sim': '∼', r'\ge': '≥', r'\geq': '≥',
    r'\le': '≤', r'\leq': '≤', r'\ne': '≠', r'\pm': '±', r'\propto': '∝',
    r'\sum': 'Σ', r'\int': '∫', r'\infty': '∞', r'\partial': '∂', r'\cdot': '·',
    r'\rightarrow': '→', r'\to': '→', r'\S': '§', r'\circ': '°', r'\degree': '°',
}
SYMBOLS[r'\phi'] = 'φ'
SYMBOLS[r'\varphi'] = 'φ'


# --------------------------------------------------------------------------
# Citation handling
# --------------------------------------------------------------------------
CITE_RE = re.compile(r'\[@([^\]]+)\]')


def parse_cite_keys(text: str) -> list[str]:
    keys: list[str] = []
    for group in CITE_RE.findall(text):
        for key in group.split(';'):
            key = key.strip().lstrip('@').strip()
            if key:
                keys.append(key)
    return keys


def _compress(nums: list[int]) -> str:
    nums = sorted(set(nums))
    parts, start, prev = [], nums[0], nums[0]
    for n in nums[1:]:
        if n == prev + 1:
            prev = n
            continue
        parts.append(f'{start}–{prev}' if prev > start + 1 else
                     ','.join(str(x) for x in range(start, prev + 1)))
        start = prev = n
    parts.append(f'{start}–{prev}' if prev > start + 1 else
                 ','.join(str(x) for x in range(start, prev + 1)))
    return ','.join(parts)


def resolve_citations(text: str, order: dict[str, int], citations: bool,
                      style: str = 'bracket') -> str:
    """Replace [@key] groups with plain reference markers (or nothing)."""
    def repl(match: re.Match) -> str:
        keys = [k.strip().lstrip('@') for k in match.group(1).split(';')]
        keys = [k for k in keys if k]
        if not citations:
            return ''
        label = _compress([order[k] for k in keys])
        if style == 'superscript':
            return '^{' + label + '}'
        return f'[{label}]'

    out = CITE_RE.sub(repl, text)
    if citations and style == 'superscript':
        out = re.sub(r'\s+(\^\{[^}]*\})', r'\1', out)          # superscripts touch the preceding word
    if not citations:
        out = re.sub(r'\s+([.,;:)])', r'\1', out)
        out = re.sub(r'\(\s*\)', '', out)
        out = re.sub(r'\s{2,}', ' ', out)
    return out.strip()


# --------------------------------------------------------------------------
# Float and equation references
# --------------------------------------------------------------------------
FLOAT_RE = re.compile(r'\{(fig|tab|eq|sec|box):([A-Za-z0-9_.\-]+)(?:\|([a-z](?:\s*[,–-]\s*[a-z])*))?\}')


def resolve_floats(text: str, fig_no: dict, tab_no: dict, eq_no: dict, zh: bool,
                   sec_no: dict | None = None, box_no: dict | None = None) -> str:
    """Resolve {fig|tab|eq|sec|box:key} markers. Section numbers are strings such as '4.1.2'."""
    def repl(match: re.Match) -> str:
        kind, key, panel = match.groups()
        table = {'fig': fig_no, 'tab': tab_no, 'eq': eq_no, 'sec': sec_no or {}, 'box': box_no or {}}[kind]
        if key not in table:
            raise KeyError(f'reference to undefined {kind}:{key}')
        n = table[key]
        if kind == 'sec' and n is None:
            raise KeyError(f'{{sec:{key}}} points to a heading without a number; set CHAPTER in content.py '
                           f'(1 numbers the first level-1 heading as 1), start the heading text with its '
                           f'number, or refer to it by name')
        if kind == 'sec':
            if zh:
                return f'第 {n} 章' if '.' not in str(n) else f'{n} 节'
            return f'Chapter {n}' if '.' not in str(n) else f'Section {n}'
        if kind == 'box':
            return f'专栏 {n}' if zh else f'Box {n}'
        if zh:
            prefix = {'fig': '图', 'tab': '表', 'eq': '式'}[kind]
            sep = '' if kind == 'eq' else ''
            out = f'{prefix}{n}'
        else:
            prefix = {'fig': 'Fig.', 'tab': 'Table', 'eq': 'equation'}[kind]
            out = f'equation ({n})' if kind == 'eq' else f'{prefix} {n}'
        if panel and kind in ('fig', 'tab'):
            out += re.sub(r'\s+', '', panel)
        return out
    return FLOAT_RE.sub(repl, text)


# --------------------------------------------------------------------------
# Inline markup
# --------------------------------------------------------------------------
MATH_RE = re.compile(r'\$(.+?)\$')
SUB_RE = re.compile(r'_(?:\{([^}]*)\}|(\w))')
SUP_RE = re.compile(r'\^(?:\{([^}]*)\}|([\w+\-−]+))')


def _tokenize_plain(text: str) -> list[tuple[str, str]]:
    """Split plain text into (text, style) runs.

    Styles: '' plain, 'bold', 'italic', 'sub', 'sup'. Outside math, chemical
    subscripts use ~x~ (MoS~2~), unit exponents use ^ (cm^2, s^-1, 10^{4}) and
    symbol subscripts use _ after a letter (V_DS, I_on).
    """
    out, i = [], 0
    pattern = re.compile(
        r'\*\*(?P<b>.+?)\*\*'
        r'|(?<![\w*])\*(?P<i>[^*\s][^*]*?)\*(?![\w*])'
        r'|~(?P<sub>[^~\s]+)~'
        r'|\^\{(?P<supb>[^}]*)\}'
        r'|\^(?P<sup>[-−+]?[0-9A-Za-z.]+)'
        r'|(?<=[A-Za-z])_\{(?P<subb>[^}]*)\}'
        r'|(?<=[A-Za-z])_(?P<sub2>[A-Za-z0-9]+)')
    for match in pattern.finditer(text):
        if match.start() > i:
            out.append((text[i:match.start()], ''))
        kind = match.lastgroup
        body = match.group(kind)
        style = {'b': 'bold', 'i': 'italic', 'sub': 'sub', 'supb': 'sup', 'sup': 'sup',
                 'subb': 'sub', 'sub2': 'sub'}[kind]
        if style == 'sup':
            body = body.replace('-', '−')
        out.append((body, style))
        i = match.end()
    if i < len(text):
        out.append((text[i:], ''))
    return [(t, s) for t, s in out if t]


def _tokenize_math(expr: str) -> list[tuple[str, str]]:
    """Convert one inline-math expression into (text, style) runs.

    Runs are emitted as (text, script) where script is one of
    '' plain, 'sub', 'sup', 'it', 'it_sub', 'it_sup'.
    """
    expr = re.sub(r'\\math(?:bf|rm|it|sf)\{([^}]*)\}', r'\1', expr)
    expr = expr.replace(r'\!', '').replace(r'\left', '').replace(r'\right', '')
    for name, char in sorted(SYMBOLS.items(), key=lambda kv: -len(kv[0])):
        expr = expr.replace(name, char)
    expr = expr.replace(r'\,', ' ').replace(r'\;', ' ').replace('~', ' ')
    runs: list[tuple[str, str]] = []
    i = 0
    while i < len(expr):
        char = expr[i]
        if char in '_^' and i + 1 < len(expr):
            script = 'sub' if char == '_' else 'sup'
            if expr[i + 1] == '{':
                end = expr.find('}', i + 2)
                body = expr[i + 2:end]
                i = end + 1
            else:
                body = expr[i + 1]
                i += 2
            runs.append((body, script))
            continue
        if char.isspace():
            runs.append((' ', ''))
            i += 1
            continue
        # gather a literal token: digits stay upright, letters become italic
        if char.isdigit() or char in '+-−=<>/.,()':
            j = i
            while j < len(expr) and (expr[j].isdigit() or expr[j] in '+-−=<>/.,()'):
                j += 1
            runs.append((expr[i:j], ''))
            i = j
            continue
        j = i
        while j < len(expr) and (expr[j].isalpha() or expr[j] in "'"):
            j += 1
        if j == i:
            runs.append((char, ''))
            i += 1
        else:
            runs.append((expr[i:j], 'it'))
            i = j
    # merge adjacent runs of the same style
    merged: list[tuple[str, str]] = []
    for text, style in runs:
        if merged and merged[-1][1] == style:
            merged[-1] = (merged[-1][0] + text, style)
        else:
            merged.append((text, style))
    # trailing space inside a math run is never wanted
    if merged and merged[-1][0].endswith(' '):
        merged[-1] = (merged[-1][0].rstrip(), merged[-1][1])
    return [(t, s) for t, s in merged if t]


def _add_plain(paragraph, text):
    for body, style in _tokenize_plain(text):
        run = paragraph.add_run(body)
        run.bold = style == 'bold'
        run.italic = style == 'italic'
        if style == 'sub':
            run.font.subscript = True
        elif style == 'sup':
            run.font.superscript = True


def add_rich_text(paragraph, text: str):
    """Add plain text, inline math and emphasis to one paragraph."""
    pos = 0
    for match in MATH_RE.finditer(text):
        if match.start() > pos:
            _add_plain(paragraph, text[pos:match.start()])
        for body, style in _tokenize_math(match.group(1)):
            if style == 'sup':
                body = body.replace('-', '−')
            run = paragraph.add_run(body)
            if style in ('sub', 'it_sub'):
                run.font.subscript = True
            if style in ('sup', 'it_sup'):
                run.font.superscript = True
            if style.startswith('it'):
                run.italic = True
        pos = match.end()
    if pos < len(text):
        _add_plain(paragraph, text[pos:])


# --------------------------------------------------------------------------
# Document styling
# --------------------------------------------------------------------------
NAVY = '153B50'
TEAL = '18757E'
SLATE = '425A64'


def set_doc_defaults(doc, fonts=None):
    sec = doc.sections[0]
    sec.top_margin = Inches(0.85)
    sec.bottom_margin = Inches(0.85)
    sec.left_margin = Inches(0.9)
    sec.right_margin = Inches(0.9)
    styles = doc.styles
    normal = styles['Normal']
    fonts = fonts or {}
    normal.font.name = fonts.get('latin', 'Times New Roman')
    normal._element.rPr.rFonts.set(qn('w:eastAsia'), fonts.get('east_asian_body', 'Songti SC'))
    normal.font.size = Pt(fonts.get('body_pt', 12))
    normal.paragraph_format.line_spacing = fonts.get('line_spacing', 1.5)
    normal.paragraph_format.space_after = Pt(6)
    for name, size, bold, color in [('Title', 16, True, NAVY),
                                    ('Heading 1', 14, True, NAVY),
                                    ('Heading 2', 12, True, TEAL),
                                    ('Heading 3', 12, True, SLATE)]:
        st = styles[name]
        st.font.name = fonts.get('latin', 'Times New Roman')
        st._element.rPr.rFonts.set(qn('w:eastAsia'), fonts.get('east_asian_heading', 'Heiti SC'))
        st.font.size = Pt(size)
        st.font.bold = bold
        st.font.color.rgb = RGBColor.from_string(fonts.get('heading_color', '000000'))
        st.paragraph_format.keep_with_next = True
        # Word's built-in Title can carry a decorative bottom rule.
        ppr = st._element.find(qn('w:pPr'))
        if ppr is not None:
            borders = ppr.find(qn('w:pBdr'))
            if borders is not None:
                ppr.remove(borders)


def add_title(doc, title, subtitle=None):
    p = doc.add_paragraph(style='Title')
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run(title)
    if subtitle:
        q = doc.add_paragraph()
        q.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = q.add_run(subtitle)
        r.italic = True
        r.font.size = Pt(10)


def add_body(doc, text, indent=True):
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Inches(0.25) if indent else Inches(0)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    add_rich_text(p, text)
    return p


def add_box(doc, title, paragraphs, level=1):
    """A bordered box: title line then indented paragraphs."""
    head = doc.add_paragraph()
    head.paragraph_format.space_before = Pt(8)
    head.paragraph_format.space_after = Pt(2)
    run = head.add_run(title)
    run.bold = True
    run.font.size = Pt(11)
    run.font.color.rgb = RGBColor.from_string(TEAL)
    for text in paragraphs:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.space_after = Pt(4)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        add_rich_text(p, text)


def add_placeholder(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text)
    r.bold = True
    r.font.color.rgb = RGBColor.from_string('B4501E')

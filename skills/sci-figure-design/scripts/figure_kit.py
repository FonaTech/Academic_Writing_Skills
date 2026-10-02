#!/usr/bin/env python3
"""Figure kit: layouts, image-model prompts, composition and integrity checks.

One folder per figure, driven by figure_spec.json (see references/figure-spec-schema.md):

  FigN_<slug>/
    figure_spec.json      grid, slots (schematic | data), labels, scenes, captions
    panels/*.png          data panels drawn by code (never by the image model)
    panels/panel_data.json  every plotted value with source, page and evidence level
    nbp/panel_<x>.png     schematic panels returned by the image model (route A)
    layout.json           derived grid description
    layout_preview.png    annotated wireframe for humans and for the docx placeholder
    layout_blocks.png     text-free colour blocks, the only layout image given to the model
    prompt_NBP.md         per-panel schematic prompts, text-free fallbacks and layout-draft guidance
    final.png             deterministic composition; model composites are not accepted data finals

Usage
  figure_kit.py layout  FOLDER [FOLDER ...]
  figure_kit.py prompts FOLDER [...]
  figure_kit.py compose FOLDER [...]
  figure_kit.py verify  FOLDER [...]     compare RGB pixels and source hashes in final.png
  figure_kit.py sizes   FOLDER [...]     print size of every slot (use it as the matplotlib figsize)
  figure_kit.py all     FOLDER [...]     layout + prompts (+ compose when nbp panels exist)
"""
from __future__ import annotations

import json
import hashlib
import sys
from pathlib import Path

PALETTE = {
    'navy': '#153B50', 'cyan': '#2C78A0', 'coral': '#D98262', 'teal': '#18757E',
    'gold': '#C9A227', 'lgrey': '#C9CFD4', 'pale': '#F2F6F8', 'green': '#6E9C75', 'purple': '#7B6A9B',
}
ROLES = {
    'navy': 'structures and text', 'cyan': 'primary object or positive branch',
    'coral': 'trapped charge, negative branch, highlighted value', 'teal': 'arrows and signal flow',
    'gold': 'metal electrodes', 'lgrey': 'substrate, inactive parts, non-target comparators',
}
STYLE = (
    'Clear scientific conceptual schematic with uniform outlines, a plain background and legible labels. '
    'Use consistent accessible colors for scientific roles specified in the scene. Depict only the objects '
    'required by this discipline and question. Keep the geometry and relationships explicit.'
)
PROHIBIT = (
    'Do not add a figure title, panel letters, captions, references, logos or watermarks. Do not write any numbers, '
    'units, axis tick values or equations; add verified numeric labels later in deterministic software. '
    'Do not invent data, realistic evidence images or unrelated decorations. Depict anatomical or other '
    'domain objects only when explicitly required by the scene. Do not invent labels beyond the quoted list.'
)
DOMAIN_HINTS = {
    'flow': 'Show the declared inputs, operations and outputs with unambiguous directed connections.',
    'biology': 'Draw only the supplied conceptual biological structures and relationships; no invented evidence images.',
    'environment': 'Keep the supplied spatial or temporal relationships explicit and distinguish observed from conceptual elements.',
    'chemistry': 'Use the supplied chemically valid relationships; add verified formulas and numeric labels separately.',
    'statistics': 'Depict sampling or analysis steps conceptually; never invent a plot or distribution.',
}

QC = [
    'Every label matches the whitelist character by character; no extra, missing or repeated words.',
    'No numbers, units, tick values or equations inside schematic panels.',
    'Geometry is physically plausible: layer order, electrode positions, current directions and arrow heads.',
    'Colour semantics follow the palette roles; the same object has the same colour in every panel.',
    'Objects and geometry fit the actual discipline; no invented data or decorative additions.',
    'Data panels match deterministic code composition and source hashes; verify their data separately.',
    'Panel letters are bold lowercase at the top-left of each panel and match the caption order.',
    'Text remains legible at the specified final width and meets the actual venue requirements.',
]


def load_spec(folder: Path) -> dict:
    spec = json.loads((folder / 'figure_spec.json').read_text(encoding='utf-8'))
    rows, cols = spec['grid']['rows'], spec['grid']['cols']
    if type(rows) is not int or type(cols) is not int or min(rows,cols)<1 or not spec['slots']:
        raise ValueError('figure needs a positive grid and at least one slot')
    names, occupied = set(), set()
    for slot in spec['slots']:
        if slot.get('kind') == 'nbp':
            slot['kind'] = 'schematic'
        slot.setdefault('col_span', 1)
        slot.setdefault('row_span', 1)
        if slot.get('kind') not in ('data','schematic') or slot.get('panel') in names:
            raise ValueError('slots require a supported kind and unique panel letters')
        names.add(slot['panel'])
        cells = {(r,c) for r in range(slot['row'],slot['row']+slot['row_span']) for c in range(slot['col'],slot['col']+slot['col_span'])}
        if not cells or any(r<0 or r>=rows or c<0 or c>=cols for r,c in cells) or occupied.intersection(cells):
            raise ValueError('panel grid spans overlap or exceed the grid')
        occupied.update(cells)
    return spec


def cell_ratio(spec) -> float:
    w, h = (float(x) for x in spec.get('ratio', '16:9').split(':'))
    rows, cols = spec['grid']['rows'], spec['grid']['cols']
    return (w / cols) / (h / rows)


# --------------------------------------------------------------------------
# Layout images
# --------------------------------------------------------------------------
def write_layout(folder: Path):
    from PIL import Image, ImageDraw
    spec = load_spec(folder)
    rows, cols = spec['grid']['rows'], spec['grid']['cols']
    ratio = cell_ratio(spec)
    layout = {k: spec[k] for k in ('title', 'ratio', 'grid') if k in spec}
    layout['slots'] = [{k: v for k, v in s.items() if k in ('panel', 'row', 'col', 'col_span', 'row_span', 'kind', 'file', 'title')}
                       for s in spec['slots']]
    (folder / 'layout.json').write_text(json.dumps(layout, ensure_ascii=False, indent=2), encoding='utf-8')
    for annotated in (True, False):
        cw, ch = 800, round(800/ratio)
        canvas = Image.new('RGB',(cols*cw,rows*ch),'white')
        draw = ImageDraw.Draw(canvas)
        for slot in spec['slots']:
            x, y = slot['col']*cw, slot['row']*ch
            w, h = slot['col_span']*cw, slot['row_span']*ch
            schematic = slot['kind'] == 'schematic'
            face = (PALETTE['pale'] if annotated else '#DCEBF2') if schematic else ('white' if annotated else '#F4DCCF')
            draw.rectangle((x+10,y+10,x+w-10,y+h-10),fill=face)
            if not annotated:
                # A model layout input must contain blocks only, never evidence/data panels.
                continue
            draw.text((x+20,y+20),slot['panel'],fill=PALETTE['navy'])
            if schematic:
                draw.text((x+20,y+45),slot.get('title','schematic'),fill=PALETTE['navy'])
            elif (folder / slot['file']).exists():
                panel=Image.open(folder/slot['file']).convert('RGB')
                panel.thumbnail((w-40,h-80),Image.Resampling.LANCZOS)
                canvas.paste(panel,(x+(w-panel.width)//2,y+60+(h-80-panel.height)//2))
            else:
                draw.text((x+20,y+60),f"missing {slot['file']}",fill='#B4501E')
        name = 'layout_preview.png' if annotated else 'layout_blocks.png'
        canvas.save(folder/name,dpi=(200,200))
    print(f'{folder.name}: layout.json, layout_preview.png, layout_blocks.png')


# --------------------------------------------------------------------------
# Prompts
# --------------------------------------------------------------------------
SUPPORTED_RATIOS = ['1:1', '2:3', '3:2', '3:4', '4:3', '4:5', '5:4', '9:16', '16:9', '21:9']


def nearest_ratio(value: float) -> str:
    def as_float(r):
        a, b = r.split(':')
        return float(a) / float(b)
    return min(SUPPORTED_RATIOS, key=lambda r: abs(as_float(r) - value))


def slot_ratio(spec, slot) -> str:
    if slot.get('ratio'):
        return slot['ratio']
    return nearest_ratio(cell_ratio(spec) * slot['col_span'] / slot['row_span'])


def hints(spec, slot):
    keys = list(dict.fromkeys(spec.get('domain', []) + slot.get('domain', [])))
    return ' '.join(DOMAIN_HINTS[k] for k in keys if k in DOMAIN_HINTS)


def panel_prompt(spec, slot):
    labels = ', '.join(f"'{l}'" for l in slot.get('labels', []))
    label_rule = (f'Add exactly these text labels, each next to the element it names, with a thin leader line where '
                  f'needed, and no other text: {labels}.') if labels else 'Do not add any text.'
    return (f"Create one panel of a scientific figure, aspect ratio {slot_ratio(spec, slot)}. "
            f"Subject: {slot.get('title','conceptual schematic')}. {slot['scene']} {hints(spec, slot)} {label_rule} {spec.get('style_prompt',STYLE)} {PROHIBIT}")


def textfree_prompt(spec, slot):
    return (f"Create the same scientific schematic with no text at all, aspect ratio {slot_ratio(spec, slot)}. "
            f"Subject: {slot.get('title','conceptual schematic')}. {slot['scene']} {hints(spec, slot)} Leave clear white space next "
            f"to each element so labels can be added later. {spec.get('style_prompt',STYLE)} Do not write any letters, words, numbers or "
            f"symbols. " + PROHIBIT.split('. ', 1)[1])


def edit_templates(slot):
    labels = slot.get('labels') or ['label']
    whitelist = ', '.join(f"'{l}'" for l in labels)
    return [
        f"Change only the label that should read '{labels[0]}' so that it reads exactly '{labels[0]}' in the same "
        f"font and size; keep everything else identical.",
        f"Remove every piece of text that is not in this list and keep everything else identical: {whitelist}.",
        "Make all outlines the same thin weight and replace any glow, gradient or texture with flat colour on white; "
        "keep layout, colours and labels identical.",
        "Correct only the geometry of <element>: <one physical fact, e.g. the gate lies below the dielectric>. "
        "Keep every other element, colour and label identical.",
    ]


def composite_prompt(spec):
    return ('Draft only schematic layout ideas. Do not upload, draw, reconstruct or include any data panel. '
            'Leave data positions blank. Final composition is performed by code, never by an image model. ' + STYLE)


def ensure_sources(folder: Path):
    """Create sources.csv for reused or adapted panels if it does not exist."""
    path = folder / 'sources.csv'
    if not path.exists():
        path.write_text('panel,doi,source_figure,licence,route,credit_line\n', encoding='utf-8-sig')


def write_prompts(folder: Path):
    spec = load_spec(folder)
    ensure_sources(folder)
    L = [f"# {folder.name}: {spec.get('title', '')}", '',
         f"- Purpose: {spec.get('purpose', '')}", f"- Placement: {spec.get('placement', '')}",
         f"- Figure aspect ratio: {spec.get('ratio', '16:9')}; grid {spec['grid']['rows']} × {spec['grid']['cols']}",
         '- Route D (default): render each schematic panel alone as a draft in `nbp/`, redraw it in standard software '
         'from the draft and the redraw brief, save it as `final/panel_<letter>.png`, then run `figure_kit.py compose '
         '<folder>`. Data panels stay untouched.',
         '- Route A (only if the journal allows AI illustrations, with a caption disclosure): use the rendered '
         'panels in `nbp/` directly, then `compose`.',
         '- Set supported dimensions/resolution through the selected tool when available; syntax is provider-specific.',
         '- Layout drafts: provide only text-free blocks from `layout_blocks.png`; keep data slots empty. '
         'Never upload data panels for model composition. The legacy filename prompt_NBP.md is provider-neutral guidance.', '']
    for slot in spec['slots']:
        if slot['kind'] == 'data':
            L += [f"## Panel {slot['panel']} (data, drawn by code)", '',
                  f"- File: `{slot['file']}`; {slot.get('title', '')}",
                  f"- Values and sources: `panels/panel_data.json`. Never regenerate this panel with an image model.", '']
            continue
        L += [f"## Panel {slot['panel']}: {slot.get('title','conceptual schematic')} (schematic, aspect {slot_ratio(spec, slot)})", '',
              '### Prompt', '', '```text', panel_prompt(spec, slot), '```', '',
              '### Label whitelist', '', ' | '.join(slot.get('labels', [])) or '(none)', '']
        if slot.get('zh'):
            L += ['### 中文构图说明', '', slot['zh'], '']
        L += ['### Text-free fallback', '', '```text', textfree_prompt(spec, slot), '```', '',
              '### Edit templates', ''] + [f'- {t}' for t in edit_templates(slot)] + ['']
    L += ['## Redraw brief (route D)', '',
          'Use the rendered draft only as a layout reference. Redraw in standard software at the print size given by '
          '`figure_kit.py sizes`, with the chosen role colors, readable venue-compliant labels and the label whitelist verbatim. '
          'Check the geometry against the scene description and sources. '
          'Save as `final/panel_<letter>.png` (or the full figure as `final/figure.png`).', '']
    L += ['## Schematic layout draft only', '', '```text', composite_prompt(spec), '```', '',
          '## Caption drafts', '', f"**EN** {spec.get('caption_en', '')}", '', f"**ZH** {spec.get('caption_zh', '')}", '',
          '## QC checklist', ''] + [f'- [ ] {q}' for q in QC] + ['']
    (folder / 'prompt_NBP.md').write_text('\n'.join(L), encoding='utf-8')
    print(f'{folder.name}: prompt_NBP.md')


# --------------------------------------------------------------------------
# Composition and verification
# --------------------------------------------------------------------------
def geometry(spec, dpi=300):
    """Print geometry: total width from print_width_mm (default 180 mm, a double column)."""
    rows, cols = spec['grid']['rows'], spec['grid']['cols']
    total_w = round(spec.get('print_width_mm', 180) / 25.4 * dpi)
    gutter = round(spec.get('gutter_mm', 2.0) / 25.4 * dpi)
    cell_w = (total_w - (cols + 1) * gutter) / cols
    cell_h = cell_w / cell_ratio(spec)
    letter = round(spec.get('letter_pt', 9) / 72 * dpi)
    return dict(rows=rows, cols=cols, total_w=total_w, gutter=gutter, cell_w=cell_w, cell_h=cell_h,
                letter=letter, top=letter + round(0.6 / 25.4 * dpi), dpi=dpi)


def slot_box(g, slot):
    x0 = g['gutter'] + slot['col'] * (g['cell_w'] + g['gutter'])
    y0 = g['gutter'] + slot['row'] * (g['cell_h'] + g['gutter'])
    w = slot['col_span'] * g['cell_w'] + (slot['col_span'] - 1) * g['gutter']
    h = slot['row_span'] * g['cell_h'] + (slot['row_span'] - 1) * g['gutter']
    return round(x0), round(y0), round(w), round(h)


def sizes(folder: Path):
    """Print size of every slot, so data panels can be drawn at their final size."""
    spec = load_spec(folder)
    g = geometry(spec)
    print(f"{folder.name}: figure {spec.get('print_width_mm', 180)} mm wide, {g['rows']}×{g['cols']} grid")
    for slot in spec['slots']:
        _, _, w, h = slot_box(g, slot)
        h -= g['top']
        wi, hi = w / g['dpi'], h / g['dpi']
        print(f"  panel {slot['panel']} ({slot['kind']}): {wi * 25.4:.0f} × {hi * 25.4:.0f} mm; "
              f"matplotlib figsize=({wi:.2f}, {hi:.2f}); {w} × {h} px at {g['dpi']} dpi")


def compose(folder: Path):
    """Route A: paste schematic panels and untouched data panels into the print-size canvas."""
    from PIL import Image, ImageDraw, ImageFont
    spec = load_spec(folder)
    g = geometry(spec)
    height = round(g['rows'] * g['cell_h'] + (g['rows'] + 1) * g['gutter'])
    canvas = Image.new('RGB', (g['total_w'], height), 'white')
    draw = ImageDraw.Draw(canvas)
    font = None
    for path in ('/System/Library/Fonts/Supplemental/Arial Bold.ttf', '/System/Library/Fonts/Helvetica.ttc',
                 '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 'C:/Windows/Fonts/arialbd.ttf'):
        if Path(path).exists():
            font = ImageFont.truetype(path, g['letter'])
            break
    font = font or ImageFont.load_default()
    missing, placements = [], {}
    for slot in spec['slots']:
        x0, y0, w, h = slot_box(g, slot)
        if slot['kind'] == 'data':
            src = folder / slot['file']
        else:
            # redrawn finals (route D) take precedence over image-model drafts (route A)
            src = next((p for d in ('final', 'nbp') for p in (folder / d / f"panel_{slot['panel']}.{e}"
                                    for e in ('png', 'jpg', 'jpeg', 'webp', 'tif', 'tiff')) if p.exists()), None)
        avail_w, avail_h = w, h - g['top']
        if src and src.exists():
            img = Image.open(src).convert('RGB')
            scale = min(avail_w / img.width, avail_h / img.height)
            if slot['kind'] == 'data':
                scale = min(scale, 1.0)  # never upsample a data panel; draw it at print size instead
            img = img.resize((max(1, round(img.width * scale)), max(1, round(img.height * scale))), Image.LANCZOS)
            px = x0 + (avail_w - img.width) // 2
            py = y0 + g['top'] + (avail_h - img.height) // 2
            canvas.paste(img, (px, py))
            placements[slot['panel']] = dict(box=[px,py,img.width,img.height],
                source_file=str(src.relative_to(folder)),source_sha256=hashlib.sha256(src.read_bytes()).hexdigest())
        else:
            missing.append(slot['panel'])
            draw.rectangle((x0, y0 + g['top'], x0 + w, y0 + h), outline='#9AAAB2', width=3)
        draw.text((x0, y0), slot['panel'], fill='black', font=font)
    if missing:
        raise ValueError('cannot produce a final with missing panels: '+', '.join(missing))
    canvas.save(folder / 'final.png', dpi=(g['dpi'], g['dpi']))
    (folder / 'final_placements.json').write_text(json.dumps(placements, indent=2), encoding='utf-8')
    print(f"{folder.name}: final.png ({g['total_w']} × {height} px, {spec.get('print_width_mm', 180)} mm)"
          + (f"; schematic panels still missing: {', '.join(missing)}" if missing else ''))
    return missing


def verify(folder: Path):
    """Verify exact RGB pixels and source hashes after deterministic composition."""
    from PIL import Image
    spec = load_spec(folder)
    data = [s for s in spec['slots'] if s['kind'] == 'data']
    if not data:
        good = any((folder/name).is_file() for name in ('final.png','final/figure.png'))
        print(f'{folder.name}: schematic final ' + ('exists; geometry still needs review' if good else 'MISSING'))
        return good
    final, placement = folder/'final.png', folder/'final_placements.json'
    if not final.is_file() or not placement.is_file():
        print(f'{folder.name}: FAIL missing code-composed final/placement records')
        return False
    placed = json.loads(placement.read_text(encoding='utf-8'))
    if set(placed) != {s['panel'] for s in spec['slots']}:
        print(f'{folder.name}: FAIL missing or extra panels in final composition')
        return False
    big = Image.open(final).convert('RGB')
    ok = True
    for slot in data:
        source, item = folder/slot['file'], placed.get(slot['panel'])
        if not source.is_file() or not isinstance(item, dict):
            print(f'{slot["panel"]}: FAIL missing source/placement')
            ok = False
            continue
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        if digest != item.get('source_sha256'):
            print(f'{slot["panel"]}: FAIL source changed after composition')
            ok = False
            continue
        x,y,w,h = item['box']
        expected = Image.open(source).convert('RGB').resize((w,h), Image.Resampling.LANCZOS)
        identical = big.crop((x,y,x+w,y+h)).tobytes() == expected.tobytes()
        print(f'{slot["panel"]}: ' + ('OK exact RGB composition' if identical else 'FAIL pixels altered'))
        ok = ok and identical
    print(f'{len(data)} data panels checked; underlying values and physical meaning require separate review')
    return ok


def main(argv):
    if len(argv) < 2 or argv[0] not in ('layout', 'prompts', 'compose', 'verify', 'sizes', 'all'):
        print(__doc__)
        return 2
    cmd, folders = argv[0], [Path(a) for a in argv[1:]]
    status = 0
    for folder in folders:
        if cmd == 'sizes':
            sizes(folder)
        if cmd in ('layout', 'all'):
            write_layout(folder)
        if cmd in ('prompts', 'all'):
            write_prompts(folder)
        if cmd == 'compose' or (cmd == 'all' and (folder / 'nbp').exists()):
            compose(folder)
        if cmd == 'verify' and not verify(folder):
            status = 1
    return status


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

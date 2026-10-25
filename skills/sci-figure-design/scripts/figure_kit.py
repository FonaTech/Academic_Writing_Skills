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
    prompt_NBP.md         route A per-panel prompts, text-free fallbacks, edit templates,
                          route B composite prompt, captions and QC checklist
    final.png             composed figure (route A)      final_nbp.png  model composite (route B)

Usage
  figure_kit.py layout  FOLDER [FOLDER ...]
  figure_kit.py prompts FOLDER [...]
  figure_kit.py compose FOLDER [...]
  figure_kit.py verify  FOLDER [...]     locate data panels in final*.png and score their fidelity
  figure_kit.py sizes   FOLDER [...]     print size of every slot (use it as the matplotlib figsize)
  figure_kit.py all     FOLDER [...]     layout + prompts (+ compose when nbp panels exist)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

PALETTE = {
    'navy': '#153B50', 'cyan': '#2C78A0', 'coral': '#D98262', 'teal': '#18757E',
    'gold': '#C9A227', 'lgrey': '#C9CFD4', 'pale': '#F2F6F8', 'green': '#6E9C75', 'purple': '#7B6A9B',
}
ROLES = {
    'navy': 'structures and text', 'cyan': 'primary object, positive branch, measured data',
    'coral': 'highlighted element, negative branch, highlighted value', 'teal': 'arrows, flows and signal paths',
    'gold': 'contacts, interfaces or key components', 'lgrey': 'background, inactive parts, non-target comparators',
}
STYLE = (
    'Clean scientific schematic in the style of a Nature Reviews figure panel. Flat vector illustration with light '
    'isometric shading, thin dark outlines of uniform weight, white background, generous white space, and a '
    'restrained palette: navy #153B50 for structures and text, cyan #2C78A0 for the primary object and positive '
    'signals, coral #D98262 for highlighted elements and negative signals, teal #18757E for arrows and flows, gold '
    '#C9A227 for contacts, interfaces or key components, light grey #C9CFD4 for backgrounds and inactive parts. All '
    'text in a plain sans-serif font such as Helvetica, sentence case, one size for all labels, perfectly spelled and '
    'fully legible.'
)
PROHIBIT = (
    'Do not add a figure title, panel letters, captions, references, logos or watermarks. Do not write any numbers, '
    'units, axis tick values or equations. Do not draw human faces, robots, brains, glowing effects, lens flares or '
    'photographic backgrounds. Do not invent labels beyond the quoted list and do not repeat any label.'
)
# Field-neutral visual primitives. Add project-specific hints in figure_spec.json ("hints": {...}) rather than here.
DOMAIN_HINTS = {
    'layers': 'Stacked layers are flat slabs of distinct colours seen at a shallow isometric angle, with thin gaps '
              'between them and the order exactly as described.',
    'sheets': 'Thin sheets are single flat planes with a faint regular lattice seen at a shallow angle; stacks show '
              'distinct sheets with small gaps.',
    'tubes': 'Cylindrical objects (fibres, tubes, filaments or vessels) are thin seamless cylinders drawn as aligned '
             'rods or a sparse random network; never ropes, springs or helices unless described.',
    'grid': 'A grid is a square array of parallel row lines crossing parallel column lines, with one small identical '
            'unit at each crossing; keep every row and column straight and evenly spaced.',
    'network': 'A network is a set of round nodes joined by straight thin edges, with no crossing clutter; node size '
               'and colour follow the palette roles.',
    'blocks': 'Process or system blocks are rounded rectangles connected by straight orthogonal connectors with small '
              'arrowheads; no decorative packages or icons.',
    'flow': 'Flows are smooth arrows of one width in teal, following the described path, without glow or motion blur.',
    'optics': 'Light is shown as a few straight rays or a soft cone in a single hue, not as rainbows or glow.',
    'pulses': 'Pulse trains and events are drawn as short vertical ticks on a thin baseline, not as noisy waveforms.',
    'molecule': 'Molecules are ball-and-stick models with flat-shaded spheres and uniform bonds, no reflections.',
    'cell': 'Cells and tissue are simple pale cross-sections with clean outlines and few organelles, not photographic.',
    'map': 'Geographic areas are flat shapes with thin borders and no terrain texture; no real map tiles.',
}
QC = [
    'Every label matches the whitelist character by character; no extra, missing or repeated words.',
    'No numbers, units, tick values or equations inside schematic panels.',
    'Geometry is physically plausible: layer order, contact positions, flow directions and arrow heads.',
    'Colour semantics follow the palette roles; the same object has the same colour in every panel.',
    'No faces, robots, brains, glow, gradients, photographic textures or decorative packages.',
    'Data panels in final images are pixel-identical to panels/*.png (route A) or pass figure_kit.py verify (route B).',
    'Panel letters are bold lowercase at the top-left of each panel and match the caption order.',
    'Text remains legible at the printed width (180 mm): minimum label height about 2 mm.',
]


def load_spec(folder: Path) -> dict:
    spec = json.loads((folder / 'figure_spec.json').read_text(encoding='utf-8'))
    for slot in spec['slots']:
        if slot.get('kind') == 'nbp':
            slot['kind'] = 'schematic'
        slot.setdefault('col_span', 1)
        slot.setdefault('row_span', 1)
    return spec


def cell_ratio(spec) -> float:
    w, h = (float(x) for x in spec.get('ratio', '16:9').split(':'))
    rows, cols = spec['grid']['rows'], spec['grid']['cols']
    return (w / cols) / (h / rows)


# --------------------------------------------------------------------------
# Layout images
# --------------------------------------------------------------------------
def write_layout(folder: Path):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    spec = load_spec(folder)
    rows, cols = spec['grid']['rows'], spec['grid']['cols']
    ratio = cell_ratio(spec)
    layout = {k: spec[k] for k in ('title', 'ratio', 'grid') if k in spec}
    layout['slots'] = [{k: v for k, v in s.items() if k in ('panel', 'row', 'col', 'col_span', 'row_span', 'kind', 'file', 'title')}
                       for s in spec['slots']]
    (folder / 'layout.json').write_text(json.dumps(layout, ensure_ascii=False, indent=2), encoding='utf-8')
    for annotated in (True, False):
        cw, ch = 4.0, 4.0 / ratio
        fig, ax = plt.subplots(figsize=(cols * cw, rows * ch))
        ax.set_xlim(0, cols); ax.set_ylim(0, rows); ax.axis('off')
        if annotated:
            ax.set_title(spec.get('title', folder.name), fontsize=11, color=PALETTE['navy'], pad=8)
        for slot in spec['slots']:
            x, w, h = slot['col'], slot['col_span'], slot['row_span']
            y = rows - slot['row'] - h
            schematic = slot['kind'] == 'schematic'
            face = (PALETTE['pale'] if annotated else '#DCEBF2') if schematic else ('white' if annotated else '#F4DCCF')
            ax.add_patch(Rectangle((x + 0.02, y + 0.03), w - 0.04, h - 0.06, facecolor=face,
                                   edgecolor=(PALETTE['teal'] if schematic else '#B8C0C8') if annotated else face,
                                   linewidth=1.2, linestyle='--' if schematic else '-'))
            if not annotated:
                if not schematic and (folder / slot['file']).exists():
                    _place(ax, plt.imread(folder / slot['file']), x, y, w, h, cw, ch)
                continue
            ax.text(x + 0.06, y + h - 0.1, slot['panel'], fontsize=11, fontweight='bold', color=PALETTE['navy'], va='top')
            if schematic:
                ax.text(x + w / 2, y + h / 2, slot.get('title', ''), fontsize=7.5, color=PALETTE['navy'],
                        ha='center', va='center', wrap=True, style='italic')
                ax.text(x + w / 2, y + 0.1, 'schematic: image model', fontsize=6.5, color=PALETTE['teal'], ha='center')
            elif (folder / slot['file']).exists():
                _place(ax, plt.imread(folder / slot['file']), x, y, w, h, cw, ch)
            else:
                ax.text(x + w / 2, y + h / 2, f"missing {slot['file']}", fontsize=7, color='#B4501E', ha='center')
        name = 'layout_preview.png' if annotated else 'layout_blocks.png'
        fig.savefig(folder / name, dpi=200, bbox_inches='tight', facecolor='white', pad_inches=0.08)
        plt.close(fig)
    print(f'{folder.name}: layout.json, layout_preview.png, layout_blocks.png')


def _place(ax, img, x, y, w, h, cw, ch):
    box_w, box_h = w - 0.14, h - 0.24
    ih, iw = img.shape[0], img.shape[1]
    scale = min(box_w * cw / iw, box_h * ch / ih)
    dw, dh = iw * scale / cw, ih * scale / ch
    x0, y0 = x + 0.07 + (box_w - dw) / 2, y + 0.08 + (box_h - dh) / 2
    ax.imshow(img, extent=(x0, x0 + dw, y0, y0 + dh), aspect='auto', zorder=2)


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


def hint_table(spec):
    """Built-in primitives plus project hints from figure_spec.json ("hints": {key: sentence})."""
    table = dict(DOMAIN_HINTS)
    table.update(spec.get('hints', {}))
    return table


def hints(spec, slot):
    keys = list(dict.fromkeys(spec.get('domain', []) + slot.get('domain', [])))
    table = hint_table(spec)
    unknown = [k for k in keys if k not in table]
    if unknown:
        print(f"warning: no hint for domain key(s) {unknown}; add them under \"hints\" in figure_spec.json",
              file=sys.stderr)
    return ' '.join(table[k] for k in keys if k in table)


def panel_prompt(spec, slot):
    labels = ', '.join(f"'{l}'" for l in slot.get('labels', []))
    label_rule = (f'Add exactly these text labels, each next to the element it names, with a thin leader line where '
                  f'needed, and no other text: {labels}.') if labels else 'Do not add any text.'
    return (f"Create one panel of a scientific figure, aspect ratio {slot_ratio(spec, slot)}. "
            f"Subject: {slot['title']}. {slot['scene']} {hints(spec, slot)} {label_rule} {STYLE} {PROHIBIT}")


def textfree_prompt(spec, slot):
    return (f"Create the same scientific schematic with no text at all, aspect ratio {slot_ratio(spec, slot)}. "
            f"Subject: {slot['title']}. {slot['scene']} {hints(spec, slot)} Leave clear white space next "
            f"to each element so labels can be added later. {STYLE} Do not write any letters, words, numbers or "
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
        "Correct only the geometry of <element>: <one physical fact, e.g. the base layer lies below the middle layer>. "
        "Keep every other element, colour and label identical.",
    ]


def composite_prompt(spec):
    grid = spec['grid']
    parts = []
    for slot in spec['slots']:
        pos = f"row {slot['row'] + 1}, column {slot['col'] + 1}"
        if slot['col_span'] > 1 or slot['row_span'] > 1:
            pos += f", spanning {slot['col_span']} columns and {slot['row_span']} rows"
        if slot['kind'] == 'data':
            parts.append(f"Panel {slot['panel']} ({pos}): place the uploaded image '{Path(slot['file']).name}' "
                         f"exactly as provided. Do not redraw, recolour, crop, sharpen or retype any text, number, "
                         f"tick or data point in it.")
        else:
            labels = ', '.join(f"'{l}'" for l in slot.get('labels', []))
            parts.append(f"Panel {slot['panel']} ({pos}): {slot['title']}. {slot['scene']} "
                         f"Labels for this panel only: {labels}.")
    return (f"Create a complete multi-panel scientific figure, aspect ratio {spec.get('ratio', '16:9')}, on a "
            f"white background. The uploaded image 'layout_blocks.png' shows only where each panel "
            f"goes ({grid['rows']} rows by {grid['cols']} columns, even gutters); blue blocks are schematic panels "
            f"to draw and orange blocks hold the uploaded data images. Do not reproduce the blocks themselves. Put a "
            f"bold lowercase panel letter at the top-left corner of each panel. " + ' '.join(parts) + f" "
            f"{' '.join(hint_table(spec)[k] for k in spec.get('domain', []) if k in hint_table(spec))} {STYLE} "
            "Do not add a figure title, captions, references, logos or watermarks. Do not write numbers, units or "
            "equations inside the schematic panels. Do not draw faces, robots, brains or glow effects.")


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
         '- Set the aspect ratio and the output resolution (2K for panels, 4K for composites) in the app or the '
         'API (`image_size`); writing them in the prompt text does not set them.',
         '- Route B: upload `layout_blocks.png` and every file in `panels/` with the composite prompt; save the result '
         'as `final_nbp.png` and run `figure_kit.py verify <folder>`.', '']
    for slot in spec['slots']:
        if slot['kind'] == 'data':
            L += [f"## Panel {slot['panel']} (data, drawn by code)", '',
                  f"- File: `{slot['file']}`; {slot.get('title', '')}",
                  f"- Values and sources: `panels/panel_data.json`. Never regenerate this panel with an image model.", '']
            continue
        L += [f"## Panel {slot['panel']}: {slot['title']} (schematic, aspect {slot_ratio(spec, slot)})", '',
              '### Prompt', '', '```text', panel_prompt(spec, slot), '```', '',
              '### Label whitelist', '', ' | '.join(slot.get('labels', [])) or '(none)', '']
        if slot.get('zh'):
            L += ['### 中文构图说明', '', slot['zh'], '']
        L += ['### Text-free fallback', '', '```text', textfree_prompt(spec, slot), '```', '',
              '### Edit templates', ''] + [f'- {t}' for t in edit_templates(slot)] + ['']
    L += ['## Redraw brief (route D)', '',
          'Use the rendered draft only as a layout reference. Redraw in standard software at the print size given by '
          '`figure_kit.py sizes`, with the palette hex codes, one sans-serif font at 7-8 pt, the label whitelist verbatim, '
          'uniform 0.5-0.75 pt outlines and no effects. Check the geometry against the scene description and the source papers. '
          'Save as `final/panel_<letter>.png` (or the full figure as `final/figure.png`).', '']
    L += ['## Route B composite prompt', '', '```text', composite_prompt(spec), '```', '',
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
            placements[slot['panel']] = [px, py, img.width, img.height]
        else:
            missing.append(slot['panel'])
            draw.rectangle((x0, y0 + g['top'], x0 + w, y0 + h), outline='#9AAAB2', width=3)
        draw.text((x0, y0), slot['panel'], fill='black', font=font)
    canvas.save(folder / 'final.png', dpi=(g['dpi'], g['dpi']))
    (folder / 'final_placements.json').write_text(json.dumps(placements, indent=2), encoding='utf-8')
    print(f"{folder.name}: final.png ({g['total_w']} × {height} px, {spec.get('print_width_mm', 180)} mm)"
          + (f"; schematic panels still missing: {', '.join(missing)}" if missing else ''))
    return missing


def _match(region, ref, fracs):
    """Best normalised cross-correlation of ref inside region over a set of width fractions."""
    import numpy as np
    from skimage.feature import match_template
    best = (-1.0, None, None, None)
    reg = np.asarray(region, dtype=float) / 255.0
    for frac in fracs:
        tw = int(round(frac * region.width))
        th = int(round(tw * ref.height / ref.width))
        if tw < 16 or th < 16 or th > region.height or tw > region.width:
            continue
        tpl = np.asarray(ref.resize((tw, th)), dtype=float) / 255.0
        res = match_template(reg, tpl)
        idx = np.unravel_index(int(np.argmax(res)), res.shape)
        if res[idx] > best[0]:
            best = (float(res[idx]), frac, (int(idx[1]), int(idx[0])), (tw, th))
    return best


def verify(folder: Path, files=('final.png', 'final_nbp.png', 'final/figure.png')):
    """Locate every data panel in the final figure and measure how faithfully it survived.

    Image models re-render every pixel, so a route-B composite will rarely score as identical;
    the side-by-side images written to verify/ must then be checked by eye for every number,
    tick label and data point. Route A (compose) keeps the pixels and should score >= 0.97.
    """
    import numpy as np
    from PIL import Image
    try:
        from skimage.metrics import structural_similarity
    except ImportError:
        print('verify needs scikit-image: pip install scikit-image')
        return False
    spec = load_spec(folder)
    ok = True
    out_dir = folder / 'verify'
    for name in files:
        final = folder / name
        if not final.exists():
            continue
        out_dir.mkdir(exist_ok=True)
        big = Image.open(final).convert('L')
        cw, ch = big.width / spec['grid']['cols'], big.height / spec['grid']['rows']
        placed = {}
        if name == 'final.png' and (folder / 'final_placements.json').exists():
            placed = json.loads((folder / 'final_placements.json').read_text(encoding='utf-8'))
        for slot in spec['slots']:
            if slot['kind'] != 'data':
                continue
            if slot['panel'] in placed:
                # route A: compare at the recorded position with the same resampling as compose()
                px, py, tw, th = placed[slot['panel']]
                crop = np.asarray(big.crop((px, py, px + tw, py + th)), dtype=float)
                ref_r = np.asarray(Image.open(folder / slot['file']).convert('RGB')
                                   .resize((tw, th), Image.LANCZOS).convert('L'), dtype=float)
                ssim = float(structural_similarity(crop, ref_r, data_range=255))
                ok &= ssim >= 0.97
                print(f'{folder.name}/{name}: panel {slot["panel"]} SSIM {ssim:.3f} at recorded position -> '
                      f'{"identical" if ssim >= 0.97 else "CHANGED after composition"}')
                continue
            ref = Image.open(folder / slot['file']).convert('L')
            m = 0.15
            box = (max(0, int((slot['col'] - m) * cw)), max(0, int((slot['row'] - m) * ch)),
                   min(big.width, int((slot['col'] + slot['col_span'] + m) * cw)),
                   min(big.height, int((slot['row'] + slot['row_span'] + m) * ch)))
            region = big.crop(box)
            f = min(1.0, 420 / region.width)
            small = region.resize((max(1, int(region.width * f)), max(1, int(region.height * f))))
            score, frac, pos, _ = _match(small, ref, np.linspace(0.35, 1.0, 27))
            if frac is None:
                print(f'{folder.name}/{name}: panel {slot["panel"]} not found')
                ok = False
                continue
            step = 0.0025
            score, frac, pos, (tw, th) = _match(region, ref, frac + step * np.arange(-10, 11))
            crop = np.asarray(region.crop((pos[0], pos[1], pos[0] + tw, pos[1] + th)), dtype=float)
            ref_r = np.asarray(ref.resize((tw, th), Image.LANCZOS), dtype=float)
            ssim = float(structural_similarity(crop, ref_r, data_range=255))
            status = ('identical' if ssim >= 0.97 else 'altered: inspect every number and mark' if ssim >= 0.75
                      else 'redrawn or replaced')
            ok &= ssim >= 0.97
            side = Image.new('L', (tw * 3 + 20, th), 255)
            side.paste(Image.fromarray(crop.astype('uint8')), (0, 0))
            side.paste(Image.fromarray(ref_r.astype('uint8')), (tw + 10, 0))
            side.paste(Image.fromarray((255 - np.abs(crop - ref_r)).clip(0, 255).astype('uint8')), (2 * tw + 20, 0))
            side.save(out_dir / f'{Path(name).stem}_panel_{slot["panel"]}.png')
            print(f'{folder.name}/{name}: panel {slot["panel"]} NCC {score:.2f}, SSIM {ssim:.3f} -> {status}')
    if not ok:
        print('  Compare the side-by-side images in verify/ (figure | source | difference). '
              'Use route A (compose) whenever data integrity matters.')
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

"""Shared matplotlib style for code-drawn data panels.

    from plot_style import apply_style, PALETTE, evidence_marker, save_panel, model_label
    apply_style()
    fig, ax = plt.subplots(figsize=size_for('FigN_slug', 'c'))   # print size from figure_spec.json

Result methods are measured, simulated, projected, estimated, inferred and synthetic.
Source role and access status are separate keyword arguments. Marker/hatch differences are
optional presentation conventions, not evidence quality ranks. Legends/captions retain the
actual method, source role and access limits; estimated results are never relabeled simulated.

evidence_marker() returns keyword arguments for ax.scatter; evidence_line() for ax.plot markers.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402

PALETTE = {
    'navy': '#153B50', 'teal': '#18757E', 'cyan': '#2C78A0', 'coral': '#D98262', 'green': '#6E9C75',
    'purple': '#7B6A9B', 'gold': '#C9A227', 'grey': '#8A8F98', 'lgrey': '#C9CFD4', 'pale': '#F2F6F8',
    # grey = secondary text and axes; lgrey = substrates, inactive parts and comparators (as in figure_kit)
}
SERIES = [PALETTE[k] for k in ('cyan', 'coral', 'green', 'purple', 'gold', 'navy')]
DPI = 300


def apply_style(font='DejaVu Sans', base=7.5):
    """Optional print panel defaults; set fonts/sizes and venue requirements for this figure."""
    plt.rcParams.update({
        'font.family': font, 'font.size': base, 'axes.titlesize': base + 1, 'axes.titleweight': 'bold',
        'axes.labelsize': base, 'xtick.labelsize': base - 0.5, 'ytick.labelsize': base - 0.5,
        'legend.fontsize': base - 1, 'legend.frameon': False,
        'axes.edgecolor': '#4A5560', 'axes.labelcolor': PALETTE['navy'], 'axes.titlecolor': PALETTE['navy'],
        'xtick.color': '#4A5560', 'ytick.color': '#4A5560', 'axes.linewidth': 0.6,
        'xtick.major.width': 0.6, 'ytick.major.width': 0.6, 'xtick.major.size': 2.5, 'ytick.major.size': 2.5,
        'axes.spines.top': False, 'axes.spines.right': False,
        'axes.grid': True, 'grid.color': '#E1E7EB', 'grid.linewidth': 0.5,
        'lines.linewidth': 1.3, 'lines.markersize': 4.5,
        'figure.dpi': DPI, 'savefig.dpi': DPI, 'savefig.facecolor': 'white',
        'pdf.fonttype': 42, 'ps.fonttype': 42, 'svg.fonttype': 'none',
    })


LEVELS = ('measured', 'simulated', 'projected', 'estimated', 'inferred', 'synthetic')


def _level(level):
    if level not in LEVELS:
        raise ValueError('Supply an explicit v2 result_method; source role/access state are separate fields')
    return level


def _metadata(source_role, access_status):
    if source_role not in ('primary','secondary','original') or access_status not in ('full-text','abstract-only','raw-files'):
        raise ValueError('Invalid source_role/access_status')


def evidence_line(level: str, colour: str, *, source_role='primary', access_status='full-text', comparator=False) -> dict:
    """Optional plot convention; legend retains the actual method and access/source fields."""
    level = _level(level); _metadata(source_role,access_status)
    colour = PALETTE['lgrey'] if comparator else colour
    style = dict(color=colour,markerfacecolor=colour if level=='measured' else 'white',markeredgecolor=colour)
    if level=='projected': style['linestyle']='--'
    if level=='synthetic': style['linestyle']=':'
    if access_status=='abstract-only': style['alpha']=0.7
    return style


def evidence_marker(level: str, colour: str, *, source_role='primary', access_status='full-text', comparator=False) -> dict:
    level = _level(level); _metadata(source_role,access_status)
    colour = PALETTE['lgrey'] if comparator else colour
    style = dict(facecolors=colour if level=='measured' else 'white',edgecolors=colour,linewidths=0.8)
    if access_status=='abstract-only': style['alpha']=0.7
    return style


def evidence_bar(level: str, colour: str, *, source_role='primary', access_status='full-text', comparator=False) -> dict:
    level = _level(level); _metadata(source_role,access_status)
    colour = PALETTE['lgrey'] if comparator else colour
    style = dict(color=colour if level=='measured' else 'white',edgecolor=colour,linewidth=0.8)
    if level!='measured': style['hatch']={'simulated':'////','estimated':'\\','inferred':'..','projected':'xx','synthetic':'++'}[level]
    if access_status=='abstract-only': style['alpha']=0.7
    return style


def model_label(text: str) -> str:
    return text if 'model' in text.lower() else f'{text} (model)'


def size_for(figure_folder, panel, spec_name='figure_spec.json'):
    """(width, height) in inches of a slot at print size, from the figure spec."""
    import importlib.util
    here = Path(__file__).resolve().parent
    spec_mod = importlib.util.spec_from_file_location('figure_kit', here / 'figure_kit.py')
    kit = importlib.util.module_from_spec(spec_mod)
    spec_mod.loader.exec_module(kit)
    spec = kit.load_spec(Path(figure_folder))
    g = kit.geometry(spec)
    for slot in spec['slots']:
        if slot['panel'] == panel:
            _, _, w, h = kit.slot_box(g, slot)
            return w / g['dpi'], (h - g['top']) / g['dpi']
    raise KeyError(f'panel {panel} not in {figure_folder}')


def save_panel(fig, path, records=None, data_json=None, panel=None):
    """Save a panel at 300 dpi and append its plotted values to panel_data.json."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=DPI, bbox_inches='tight', pad_inches=0.02, facecolor='white')
    plt.close(fig)
    if records is not None:
        data_json = Path(data_json or path.parent / 'panel_data.json')
        store = json.loads(data_json.read_text(encoding='utf-8')) if data_json.exists() else {'panels': []}
        store['panels'] = [p for p in store['panels'] if p.get('panel') != panel]
        store['panels'].append({'panel': panel, 'file': path.name, 'values': records})
        data_json.write_text(json.dumps(store, ensure_ascii=False, indent=2), encoding='utf-8')
    return path

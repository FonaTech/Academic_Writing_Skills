"""Figures, tables and boxes. Keys are cited in content.py as {fig:key}, {tab:key}.

FIGURES[key]
  folder        Figures/<folder>/ holds final.png (composed), final_nbp.png (image-model
                composite) or layout_preview.png; the first one found is embedded
  caption_en    first sentence = figure title; then **a**, ... panel descriptions;
  caption_zh    abbreviations defined again at the end of the caption
TABLES[key]
  title_*, columns_*, rows_* (one list per language; numbers identical), note_*, widths (inches)
  year_column   True: insert a Year column after the Ref./Source column, filled from references.json
  year_inline   [column indices]: prefix each citation group in those columns with its year
  A separator row holds only a group label in its first cell; its Year cell stays blank.
BOXES[name]
  title_*, items: [{'type': 'para', 'en', 'zh'} | {'type': 'eq', 'key', 'latex'}]
"""

FIGURES = {
    'decay': {
        'folder': 'Fig1_decay',
        'caption_en': 'First-order decay and its rate constant. '
                      '**a**, Normalized quantity versus time for three rate constants (model). '
                      '**b**, The same curves on a logarithmic axis, where the slope equals −*k*.',
        'caption_zh': '一级衰减及其速率常数。**a**，三个速率常数下归一化物理量随时间的变化（模型）。'
                      '**b**，同一组曲线的对数坐标图，斜率等于 −*k*。',
    },
}

TABLES = {
    'rates': {
        'title_en': 'Reported rate constants and their conditions',
        'title_zh': '已报道的速率常数及其条件',
        'columns_en': ['System', 'Conditions', 'k (s^-1)', 'Basis', 'Ref.'],
        'columns_zh': ['体系', '条件', 'k (s^-1)', '依据', '文献'],
        'rows_en': [['Example system', '25 °C, 0.1 mol L^-1', '0.05', 'Meas.', '[@example2024]']],
        'rows_zh': [['示例体系', '25 °C，0.1 mol L^-1', '0.05', '实测', '[@example2024]']],
        'note_en': 'Meas., measured; Sim., simulated; Est., estimated from reported parameters.',
        'note_zh': '实测：实验测得；仿真：模拟计算；估算：由已报道参数估算。',
        'widths': [1.5, 1.7, 0.9, 0.8, 0.9],
        'year_column': True,
    },
}

BOXES = {
    'fit': {
        'title_en': 'Fitting window',
        'title_zh': '拟合区间',
        'items': [
            {'type': 'para',
             'en': 'A linear fit of the logarithm over $n$ points gives $k$ as the negative slope,',
             'zh': '在 $n$ 个数据点上对对数作线性拟合，$k$ 即为斜率的相反数，'},
            {'type': 'eq', 'key': 'slope',
             'latex': r'k=-\frac{\sum_{i=1}^{n}(t_i-\bar{t})(\ln y_i-\overline{\ln y})}{\sum_{i=1}^{n}(t_i-\bar{t})^{2}}'},
        ],
    },
}

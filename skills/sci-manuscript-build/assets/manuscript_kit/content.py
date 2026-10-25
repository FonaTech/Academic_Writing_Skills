"""Manuscript text: ordered blocks, each carrying every language.

Markup (see manuscript_core.py)
  [@key; @key2]      citation, numbered by first appearance
  {fig:key|b}        figure (panel) reference, numbered by first mention
  {tab:key}          table reference
  {eq:key}           equation reference (equations are numbered by display order)
  $G_{ij}V_i$        inline math: subscripts, superscripts, Greek, italics
  CO~2~  mol L^-1  s^-1  T_m   chemistry, units and symbol subscripts outside math
  **bold**  *italic*

Rules enforced by check_manuscript.py
  - every block has every language listed in manuscript.json
  - citation keys, float references and numbers match between languages block by block
  - every figure and table is cited in a paragraph before it is placed
  - abbreviations in manuscript.json are defined at first use in running text
"""
from floats import BOXES

CHAPTER = 1          # headings without a leading number are numbered 1, 1.1, 1.1.1
BLOCKS = []


def H(id, level, en, zh=''):
    BLOCKS.append(dict(id=id, type='heading', level=level, en=en, zh=zh))


def P(id, en, zh=''):
    BLOCKS.append(dict(id=id, type='para', en=' '.join(en.split()), zh=' '.join(zh.split()) if zh else ''))


def EQ(id, key, latex):
    BLOCKS.append(dict(id=id, type='eq', key=key, latex=latex))


def BOX(id, name):
    box = BOXES[name]
    BLOCKS.append(dict(id=id, type='box', name=name, title_en=box['title_en'], title_zh=box['title_zh'],
                       items=box['items']))


# ---------------------------------------------------------------- example section
# Replace with the manuscript's own sections. The example exercises every markup type once.
H('s1', 1, 'Measuring a first-order process', '一级过程的测量')
H('s1.1', 2, 'From the decay curve to the rate constant', '从衰减曲线到速率常数')

P('s1-a', '''
Many processes in physics, chemistry and biology follow first-order kinetics, in which the rate is
proportional to the remaining quantity. The quantity $y$ then decays with a rate constant $k$
from its initial value $y_{0}$ ({fig:decay|a}):
''', '''
物理、化学和生物中的许多过程遵循一级动力学，即速率与剩余量成正比。此时物理量 $y$ 以速率常数 $k$ 从初值 $y_{0}$ 衰减（{fig:decay|a}）：
''')
EQ('eq-decay', 'decay', r'y(t)=y_{0}\,e^{-kt}')

P('s1-b', '''
A half-life $t_{1/2}=\ln 2/k$ follows from {eq:decay}, so one fitted constant summarizes the whole
curve [@example2024]. Reported constants differ with temperature, concentration (mol L^-1) and
fitting window, so each value in {tab:rates} carries its conditions ({box:fit}).
''', '''
由 {eq:decay} 可得半衰期 $t_{1/2}=\ln 2/k$，因此一个拟合常数即可概括整条曲线 [@example2024]。已报道的常数随温度、浓度（mol L^-1）和拟合区间而变化，因此 {tab:rates} 中每个数值都附有其条件（{box:fit}）。
''')

BOX('box1', 'fit')

"""Behavioral checks for merged features. All inputs/years/references here are synthetic fixtures."""
from __future__ import annotations
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT/'skills/sci-manuscript-build/assets/manuscript_kit'

def write(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')

def run(path, *args, cwd=None):
    return subprocess.run([sys.executable, str(path), *map(str, args)], cwd=cwd,
                          capture_output=True, text=True, timeout=30)

class MergedBuildTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.project = Path(self.temp.name)/'fixture'
        result = run(ROOT/'skills/sci-manuscript-build/scripts/new_project.py', self.project,
                     '--slug', 'MergeFixture', '--languages', 'en', 'zh')
        self.assertEqual(result.returncode, 0, result.stderr)
        write(self.project/'content.json', {'blocks':[{'id':'p', 'type':'para',
              'en':'The synthetic fixture is shown in {tab:t}.', 'zh':'人工合成测试见 {tab:t}。'}]})
        self.table = dict(title_en='Synthetic metadata fixture', title_zh='合成元数据测试',
                         columns_en=['Source','Description'], columns_zh=['来源','描述'],
                         rows_en=[['[@fixture]','Synthetic reference [@fixture]']],
                         rows_zh=[['[@fixture]','合成参考记录 [@fixture]']], year_column=True)
        write(self.project/'references.json', {'fixture':dict(title='Synthetic fixture; not a real publication',
              authors='Fixture Author', year=2024, journal='Test fixture only', verification='synthetic')})

    def tearDown(self):
        self.temp.cleanup()

    def build(self, success=True):
        write(self.project/'floats.json', dict(figures={}, boxes={}, tables={'t':self.table}))
        result = run(self.project/'build_manuscript.py', cwd=self.project)
        self.assertEqual(result.returncode == 0, success, result.stdout+result.stderr)
        return result

    def document(self, suffix='EN_WithCitations'):
        from docx import Document
        return Document(self.project/f'MergeFixture_{suffix}.docx')

    def test_year_column_both_languages_and_no_citation(self):
        cfg = json.loads((self.project/'manuscript.json').read_text())
        cfg['output']['no_citation_variant'] = True
        write(self.project/'manuscript.json', cfg)
        self.build()
        for lang, label in [('EN','Year'),('ZH','年份')]:
            table = self.document(lang+'_WithCitations').tables[0]
            self.assertEqual([c.text for c in table.rows[0].cells][1], label)
            self.assertEqual(table.cell(1,1).text, '2024')
        no_cite = self.document('EN_NoCitation').tables[0]
        self.assertEqual(no_cite.cell(1,1).text, '2024')
        self.assertNotIn('[1]', ' '.join(c.text for row in no_cite.rows for c in row.cells))

    def test_inline_year_indices_refer_to_original_columns(self):
        self.table['year_inline'] = [1]
        self.build()
        table = self.document().tables[0]
        self.assertEqual(table.cell(1,1).text, '2024')
        self.assertIn('(2024)', table.cell(1,2).text)
        zh = self.document('ZH_WithCitations').tables[0]
        self.assertIn('（2024）', zh.cell(1,2).text)

    def test_missing_reference_year_fails(self):
        write(self.project/'references.json', {'fixture':dict(title='Synthetic fixture', year='')})
        result = self.build(success=False)
        self.assertIn('year metadata missing', result.stderr)

    def test_word_lock_preserves_existing_outputs(self):
        self.build()
        doc = self.project/'MergeFixture_EN_WithCitations.docx'
        before = doc.read_bytes()
        (self.project/('~$'+doc.name)).write_text('synthetic lock file')
        result = self.build(success=False)
        self.assertIn('Word lock file found', result.stderr)
        self.assertEqual(doc.read_bytes(), before)

    def test_legacy_python_source_keeps_year_generation(self):
        cfg = json.loads((self.project/'manuscript.json').read_text())
        cfg['source'] = {'format':'python'}
        write(self.project/'manuscript.json',cfg)
        (self.project/'content.py').write_text("CHAPTER = None\nBLOCKS = [{'id':'p','type':'para','en':'Synthetic fixture {tab:t}.','zh':'合成测试 {tab:t}。'}]\n")
        (self.project/'floats.py').write_text('FIGURES = {}\nBOXES = {}\nTABLES = '+repr({'t':self.table})+'\n')
        self.build()
        self.assertEqual(self.document().tables[0].cell(1,1).text, '2024')

    def test_inline_function_names_are_upright(self):
        write(self.project/'content.json', {'blocks':[{'id':'p','type':'para',
              'en':r'Synthetic expression $y=\ln(x)+\exp(z)$ accompanies {tab:t}.', 'zh':r'合成表达式 $y=\ln(x)+\exp(z)$ 对应 {tab:t}。'}]})
        self.build()
        runs = [r for p in self.document().paragraphs for r in p.runs]
        self.assertTrue(any('ln' in r.text and not r.italic for r in runs))
        self.assertTrue(any('exp' in r.text and not r.italic for r in runs))
        self.assertTrue(any(r.text == 'x' and r.italic for r in runs))

    def test_unclosed_inline_math_group_fails_promptly(self):
        write(self.project/'content.json', {'blocks':[{'id':'p','type':'para',
              'en':r'Synthetic malformed expression $x_{ab$ accompanies {tab:t}.', 'zh':r'合成错误表达式 $x_{ab$ 对应 {tab:t}。'}]})
        result = self.build(success=False)
        self.assertIn('unclosed inline math', result.stderr)

class MergedToolTests(unittest.TestCase):
    def test_release_checksums_detect_changes_and_unlisted_files(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root/'tools').mkdir()
            shutil.copy2(ROOT/'tools/checksums.py',root/'tools')
            (root/'.claude-plugin').mkdir()
            meta = root/'.claude-plugin/plugin.json'
            meta.write_text('{"fixture": true}')
            tool = root/'tools/checksums.py'
            self.assertEqual(run(tool,'--write').returncode,0)
            self.assertEqual(run(tool).returncode,0)
            meta.write_text('{"fixture": false}')
            self.assertNotEqual(run(tool).returncode,0)
            self.assertEqual(run(tool,'--write').returncode,0)
            (root/'unexpected.txt').write_text('unlisted fixture')
            self.assertNotEqual(run(tool).returncode,0)

    def test_known_acronyms_and_profile_coexist(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td)/'draft.md'
            path.write_text('The LLM test fixture preserves the declared method and its limits.')
            tool = ROOT/'skills/sci-prose-style/scripts/prose_lint.py'
            result = run(tool, path, '--json', '--known', 'LLM', '--profile', 'generic')
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertNotIn('LLM',json.loads(result.stdout)['abbreviations_without_definition'])
            without = run(tool,path,'--json')
            self.assertIn('LLM',json.loads(without.stdout)['abbreviations_without_definition'])

    def test_staccato_diagnostic_is_advisory(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td)/'draft.md'
            path.write_text('The sample was collected. The temperature was recorded. The reading was stored.')
            result = run(ROOT/'skills/sci-prose-style/scripts/prose_lint.py',path,'--json')
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertIn('staccato-run',[f['kind'] for f in json.loads(result.stdout)['findings']])

    def test_project_schematic_hints_override_defaults(self):
        spec = importlib.util.spec_from_file_location('merge_figure_kit',ROOT/'skills/sci-figure-design/scripts/figure_kit.py')
        module = importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        prompt = module.panel_prompt(dict(grid={'rows':1,'cols':1},domain=['layers'],
                    hints={'layers':'Synthetic project-specific layer order.'}),
                    dict(title='Synthetic schematic',scene='Conceptual sequence.',labels=[],col_span=1,row_span=1))
        self.assertIn('Synthetic project-specific layer order.', prompt)
        self.assertNotIn('Stacked layers are flat slabs',prompt)

    def test_browser_upload_metadata_can_be_restored(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root/'tools').mkdir()
            shutil.copy2(ROOT/'tools/sync_plugin_manifests.py',root/'tools')
            shutil.copytree(ROOT/'claude-plugin',root/'claude-plugin')
            self.assertNotEqual(run(root/'tools/sync_plugin_manifests.py').returncode,0)
            self.assertEqual(run(root/'tools/sync_plugin_manifests.py','--write').returncode,0)
            self.assertEqual((root/'.claude-plugin/plugin.json').read_bytes(),(root/'claude-plugin/plugin.json').read_bytes())

if __name__ == '__main__':
    unittest.main()

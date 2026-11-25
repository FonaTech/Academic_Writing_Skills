"""Synthetic prose fixtures test observable diagnostics, not authorship or detector efficacy."""
from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
LINTER=ROOT/'skills/sci-prose-style/scripts/prose_lint.py'

class DraftingChainTests(unittest.TestCase):
    def lint(self,text,*args):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'fixture.md';path.write_text(text,encoding='utf-8')
            before=path.read_bytes()
            p=subprocess.run([sys.executable,str(LINTER),str(path),'--json',*args],capture_output=True,text=True,timeout=30)
            self.assertEqual(p.returncode,0,p.stdout+p.stderr)
            self.assertEqual(path.read_bytes(),before,'Diagnostics must not rewrite evidence-bearing text')
            return json.loads(p.stdout)

    @staticmethod
    def kinds(result):return {hit['kind'] for hit in result['findings']}

    def test_number_inventory_is_flagged(self):
        result=self.lint('The synthetic voltage was 2 V. The synthetic current was 3 A. The synthetic duration was 4 s.')
        self.assertIn('number-run',self.kinds(result))

    def test_short_english_questions_are_not_dropped(self):
        self.assertIn('question-voice',self.kinds(self.lint('Why? What next?')))

    def test_short_chinese_questions_are_not_dropped(self):
        self.assertIn('zh-question',self.kinds(self.lint('为何？为什么？')))

    def test_thinking_aloud_and_counted_overview(self):
        result=self.lint('The question is whether the fixture changes. In the first group, the samples remain unchanged.')
        self.assertTrue({'thinking-aloud','ordinal-enumeration'}<=self.kinds(result))

    def test_chinese_templates_are_detected(self):
        result=self.lint('值得注意的是，所列记录只是人工测试数据。综上所述，实际研究需要另行验证。')
        self.assertIn('zh-template',self.kinds(result))

    def test_uniform_english_rhythm(self):
        result=self.lint('The first synthetic sample preserves the specified shape. The second synthetic sample preserves the specified shape. The third synthetic sample preserves the specified shape. The fourth synthetic sample preserves the specified shape. The fifth synthetic sample preserves the specified shape.')
        self.assertIn('uniform-rhythm',self.kinds(result))
        self.assertEqual(result['stats']['paragraph_length_cv_median'],0)

    def test_uniform_chinese_rhythm_and_connective_chain(self):
        result=self.lint('因此，样本保持相同形状。因此，样本保持相同形状。因此，样本保持相同形状。因此，样本保持相同形状。因此，样本保持相同形状。')
        self.assertTrue({'zh-connective','zh-uniform-rhythm'}<=self.kinds(result))
        self.assertEqual(result['stats']['zh_connectives_per_100_sentences'],100)

    def test_connective_rate_counts_occurrences(self):
        result=self.lint('Because the synthetic fixture was repeated, the record was checked and then stored.')
        self.assertEqual(result['stats']['explain_connectives_per_100_sentences'],200)
        self.assertIn('explanation-connective-rate',self.kinds(result))

    def test_chinese_connective_rate_counts_occurrences(self):
        result=self.lint('因此记录被保留，所以核查仍有依据。')
        self.assertEqual(result['stats']['zh_connectives_per_100_sentences'],200)

    def test_all_profiles_keep_common_english_and_chinese_checks(self):
        for profile in ('precise','compact','explanatory','generic'):
            with self.subTest(profile=profile):
                result=self.lint('Why?\n\n为何？','--profile',profile)
                self.assertTrue({'question-voice','zh-question'}<=self.kinds(result))

    def test_markdown_data_and_references_are_not_rewritten_as_prose(self):
        result=self.lint('| Value | Unit |\n|---|---|\n| 2 | V |\n| 3 | V |\n| 4 | V |\n\n# References\n\nWhy? Synthetic reference title.')
        self.assertFalse({'number-run','question-voice'}&self.kinds(result))

    def test_number_profile_and_float_references(self):
        result=self.lint('Figure 1 shows the synthetic arrangement. The fixture was repeated under the declared conditions. The synthetic voltage was 2 V. The same fixture retained the original shape after the repeat.')
        self.assertEqual(result['stats']['number_sentence_share'],0.25)

    def test_full_incoming_style_rules_remain_available(self):
        result=self.lint('The useful fixture made the comparison credible and decisive.')
        details=' '.join(hit['detail'] for hit in result['findings'] if hit['kind']=='banned')
        for word in ['useful','credible','decisive']:self.assertIn(word,details)

    def test_builder_uses_chain_diagnostics_for_json_and_markdown(self):
        with tempfile.TemporaryDirectory() as td:
            project=Path(td)/'fixture'
            new=ROOT/'skills/sci-manuscript-build/scripts/new_project.py'
            p=subprocess.run([sys.executable,str(new),str(project),'--slug','ChainFixture','--languages','en','zh'],capture_output=True,text=True)
            self.assertEqual(p.returncode,0,p.stderr)
            (project/'paragraph.md').write_text('Why? The question is whether the synthetic fixture changes.')
            content={'blocks':[{'id':'p','type':'para','files':{'en':'paragraph.md'},'zh':'为何？值得注意的是，所列值只是合成测试数据。'}]}
            (project/'content.json').write_text(json.dumps(content,ensure_ascii=False))
            p=subprocess.run([sys.executable,'check_manuscript.py','--style'],cwd=project,capture_output=True,text=True)
            self.assertEqual(p.returncode,0,p.stdout+p.stderr)
            for kind in ['question-voice','thinking-aloud','zh-question','zh-template']:self.assertIn(kind,p.stdout)
            self.assertFalse((project/'ChainFixture_EN_WithCitations.docx').exists())

if __name__=='__main__':unittest.main()

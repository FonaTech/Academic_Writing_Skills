"""Negative fixtures validate profile/index failure detection without changing real skills."""
from pathlib import Path
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ValidatorImprovementTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name)/'repo'
        for name in ('tools', 'skills', '.claude-plugin', 'claude-plugin'):
            shutil.copytree(ROOT/name, self.repo/name, ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
        shutil.copy2(ROOT/'VERSION', self.repo/'VERSION')
        spec = importlib.util.spec_from_file_location('validator_fixture', self.repo/'tools/validate_skills.py')
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)

    def tearDown(self):
        self.temp.cleanup()

    def write_both(self, relative, change):
        paths = [self.repo/'skills/sci-prose-style/assets'/relative,
                 self.repo/'skills/sci-manuscript-build/assets/manuscript_kit'/relative]
        original = [path.read_bytes() for path in paths]
        data = json.loads(original[0]);change(data)
        text = json.dumps(data, ensure_ascii=False)
        for path in paths:path.write_text(text)
        return paths, original

    def restore(self, paths, original):
        for path, content in zip(paths, original):path.write_bytes(content)
        self.module.errors.clear()

    def test_all_english_profiles_reject_invalid_regexes(self):
        for profile in ('precise','compact','explanatory','generic'):
            with self.subTest(profile=profile):
                paths, original = self.write_both(Path('style_profiles')/(profile+'.json'),
                    lambda data:data.setdefault('banned',[]).append({'label':'synthetic invalid regex','pattern':'[','fix':'fixture'}))
                self.module.check_shared()
                self.assertTrue(any(profile+'.json' in e and 'does not compile' in e for e in self.module.errors), self.module.errors)
                self.assertFalse(any('copies differ' in e for e in self.module.errors))
                self.restore(paths,original)

    def test_all_chinese_profiles_reject_invalid_regexes(self):
        for profile in ('precise','compact','explanatory','generic'):
            with self.subTest(profile=profile):
                paths, original = self.write_both(Path('style_profiles')/(profile+'.json'),
                    lambda data:data['zh'].__setitem__('question','['))
                self.module.check_shared()
                self.assertTrue(any(profile+'.json' in e and 'zh' in e and 'does not compile' in e for e in self.module.errors), self.module.errors)
                self.restore(paths,original)

    def test_default_limits_reject_invalid_chinese_pattern(self):
        self.write_both(Path('style_limits.json'),lambda data:data['zh'].__setitem__('ordinal','['))
        self.module.check_shared()
        self.assertTrue(any('style_limits.json' in e and 'does not compile' in e for e in self.module.errors))

    def test_missing_common_blocks_are_reported_for_each_profile(self):
        for profile in ('precise','compact','explanatory','generic'):
            for key in ('rhythm','zh'):
                for state in ('missing','null','string'):
                    with self.subTest(profile=profile,key=key,state=state):
                        def change(data):
                            if state == 'missing':data.pop(key)
                            else:data[key] = None if state == 'null' else 'synthetic invalid block'
                        paths, original = self.write_both(Path('style_profiles')/(profile+'.json'),change)
                        self.module.check_shared()
                        self.assertTrue(any(profile+'.json' in e and key+' block missing' in e for e in self.module.errors), self.module.errors)
                        self.restore(paths,original)

    def test_method_name_in_plain_text_is_not_enough(self):
        folder = self.repo/'skills/sci-writing-orchestrator/method-studies'
        study = sorted(folder.glob('[0-9][0-9]-*.md'))[0]
        index = folder/'INDEX.md'
        index.write_text(index.read_text().replace(']('+study.name+')','](../case-studies/DOMAIN_INDEX.md)'))
        self.module.check_method_studies()
        self.assertTrue(any('does not link to '+study.name in e for e in self.module.errors), self.module.errors)

    def test_dangling_numbered_method_link_is_rejected(self):
        index = self.repo/'skills/sci-writing-orchestrator/method-studies/INDEX.md'
        index.write_text(index.read_text()+'\n[Missing fixture](99-missing-fixture.md)\n')
        self.module.check_method_studies()
        self.assertTrue(any('links to missing 99-missing-fixture.md' in e for e in self.module.errors))

    def test_missing_method_index_is_rejected(self):
        (self.repo/'skills/sci-writing-orchestrator/method-studies/INDEX.md').unlink()
        self.module.check_method_studies()
        self.assertTrue(any('INDEX.md is missing' in e for e in self.module.errors))

    def test_removing_checker_call_still_fails_wiring_check(self):
        path = self.repo/'skills/sci-manuscript-build/assets/manuscript_kit/check_manuscript.py'
        text = path.read_text()
        path.write_text(text.replace('    check_line_of_thought(content, floats)\n',''))
        self.module.check_drafting_chain()
        self.assertTrue(any('main does not call' in e for e in self.module.errors))

    def test_cli_exits_nonzero_for_invalid_alternative_profile(self):
        self.write_both(Path('style_profiles/generic.json'),
            lambda data:data['zh']['template'].append({'label':'invalid CLI fixture','pattern':'[','fix':'fixture'}))
        result = subprocess.run([sys.executable,str(self.repo/'tools/validate_skills.py')],capture_output=True,text=True,timeout=60)
        self.assertNotEqual(result.returncode,0)
        self.assertIn('generic.json',result.stdout)
        self.assertIn('does not compile',result.stdout)


if __name__ == '__main__':unittest.main()

"""Local PDF/library regressions. Require optional PyMuPDF and requests; no network calls.
All fixture titles, records and documents are invented test inputs.
"""
import csv
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIT = ROOT / 'skills/sci-literature-evidence/scripts'
AVAILABLE = all(importlib.util.find_spec(m) for m in ('fitz', 'requests'))

@unittest.skipUnless(AVAILABLE, 'Optional PDF/library dependencies unavailable')
class OptionalLibraryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def module(self, name):
        sys.path.insert(0, str(LIT))
        spec = importlib.util.spec_from_file_location(name, LIT / (name + '.py'))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def test_no_doi_source_is_retained_with_stable_id(self):
        file = self.root / 'candidates.csv'
        with file.open('w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=['id','title','year','doi','decision'])
            w.writeheader()
            w.writerow(dict(id='archive-fixture',title='Synthetic archive teaching record',year='2000',doi='',decision='include'))
        lib = self.root / 'library'
        cmd = [sys.executable, str(LIT / 'build_library_tables.py'), 'assign', str(file), '--library', str(lib)]
        self.assertEqual(subprocess.run(cmd,capture_output=True).returncode,0)
        with (lib / 'library_plan.csv').open(encoding='utf-8-sig') as f:
            first = list(csv.DictReader(f))
        self.assertEqual(len(first),1)
        self.assertEqual(first[0]['doi'],'')
        self.assertEqual(first[0]['identity_status'],'pending-manual-check')
        self.assertEqual(subprocess.run(cmd,capture_output=True).returncode,0)
        with (lib / 'library_plan.csv').open(encoding='utf-8-sig') as f:
            self.assertEqual(list(csv.DictReader(f))[0]['id'],first[0]['id'])
        fetch = self.module('fetch_open_access')
        self.assertEqual(len(fetch.load_rows(file)),1)
        self.assertEqual(subprocess.run([sys.executable,str(LIT/'fetch_open_access.py'),str(file),'--out',str(lib)],capture_output=True).returncode,0)
        with (lib/'library_status.csv').open(encoding='utf-8-sig') as f:
            self.assertEqual(list(csv.DictReader(f))[0]['status'],'manual-required')

    def test_single_page_pdf_digest(self):
        import fitz
        pdf = self.root / 'one.pdf'
        doc = fitz.open()
        doc.new_page().insert_text((40,40),'Synthetic one page teaching document')
        doc.save(pdf);doc.close()
        out = self.root/'text'
        result = subprocess.run([sys.executable,str(LIT/'extract_pdf_text.py'),str(pdf),'--out',str(out),'--digest'],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(json.loads((out/'manifest.json').read_text())[0]['pages'],1)
        self.assertEqual(len(list(out.glob('*.digest.md'))),1)

    def test_empty_identifier_and_unicode_title_do_not_false_match(self):
        import fitz
        fetch = self.module('fetch_open_access')
        self.assertEqual(fetch.norm('教育评估'),'教育评估')
        pdf = self.root/'unrelated.pdf'
        doc = fitz.open()
        for _ in range(2):
            doc.new_page().insert_textbox(fitz.Rect(40,40,500,760), 'An unrelated synthetic document. ' * 90, fontsize=9)
        doc.save(pdf);doc.close()
        for title in ('', '教育评估', 'Invented completely different title'):
            self.assertFalse(fetch.validate(pdf, dict(title=title,doi=''))[0])

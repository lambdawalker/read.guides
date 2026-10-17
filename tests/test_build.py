import subprocess
import sys
import tempfile
import shutil
import zipfile
import unittest
from pathlib import Path
import yaml
import pymupdf as fitz

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/build_book.py'
BOOK = ROOT / 'books/01-se-cayo/book.yaml'

class BuildTests(unittest.TestCase):
    def run_build(self, config, output):
        return subprocess.run([sys.executable, str(SCRIPT), str(config), '--output', str(output)], capture_output=True, text=True)

    def test_book_has_cover_twelve_pages_and_accents(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)/'out'
            result = self.run_build(BOOK, out)
            self.assertEqual(result.returncode, 0, result.stderr)
            with fitz.open(out/'01-se-cayo.pdf') as pdf:
                self.assertEqual(len(pdf), 13)
                self.assertIn('El pato caminó.', pdf[1].get_text())
                self.assertIn('El pato se cayó.', pdf[2].get_text())
                self.assertEqual(sum('se cayó.' in p.get_text() for p in pdf), 6)
            with fitz.open(out/'01-se-cayo.pdf') as pdf:
                self.assertTrue(all(p.rect.width > p.rect.height for p in pdf))
                self.assertIn('La llama saltó.', pdf[9].get_text())
                self.assertIn('La llama se cayó.', pdf[10].get_text())
                self.assertIn('El oso bailó.', pdf[11].get_text())
                self.assertIn('El oso se cayó.', pdf[12].get_text())
                self.assertEqual([row[1] for row in pdf.get_toc()], ['Pato', 'Gato', 'Mono', 'Vaca', 'Llama', 'Oso'])
            self.assertEqual(len(list((out/'assets/images').glob('*.png'))), 12)
            self.assertEqual(sorted(p.name for p in out.glob('*.zip')), ['01-se-cayo-assets.zip'])
            self.assertFalse((out/'pages').exists())
            self.assertFalse((out/'illustrations').exists())
            with zipfile.ZipFile(out/'01-se-cayo-assets.zip') as z:
                self.assertIn('assets/book.yaml', z.namelist())
                self.assertIn('assets/images/12-oso.png', z.namelist())

    def test_missing_animal_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp)/'source'
            shutil.copytree(BOOK.parent, source)
            config = source/'book.yaml'
            d = yaml.safe_load(config.read_text(encoding='utf-8'))
            d['pages'] = d['pages'][:8]
            config.write_text(yaml.safe_dump(d), encoding='utf-8')
            result = self.run_build(config, Path(tmp)/'out')
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('two pages', result.stderr)

    def test_missing_image_fails_before_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = yaml.safe_load(BOOK.read_text(encoding='utf-8'))
            d['pages'][0]['image'] = 'missing.png'
            source = Path(tmp)/'source'
            shutil.copytree(BOOK.parent, source)
            config = source/'book.yaml'
            config.write_text(yaml.safe_dump(d), encoding='utf-8')
            out = Path(tmp)/'output'
            result = self.run_build(config, out)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('Missing', result.stderr)
            self.assertFalse(out.exists())

    def test_overflow_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp)/'source'
            shutil.copytree(BOOK.parent, source)
            config = source/'book.yaml'
            d = yaml.safe_load(config.read_text(encoding='utf-8'))
            d['pages'][0]['text'] = 'El pato ' * 40
            config.write_text(yaml.safe_dump(d), encoding='utf-8')
            result = self.run_build(config, Path(tmp)/'out')
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('overflow', result.stderr)

    def test_unowned_output_is_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)/'out'
            (out/'pages').mkdir(parents=True)
            important = out/'pages'/'keep.txt'
            important.write_text('keep')
            result = self.run_build(BOOK, out)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('unowned', result.stderr.lower())
            self.assertEqual(important.read_text(), 'keep')

    def test_source_output_overlap_rejected(self):
        result = self.run_build(BOOK, BOOK.parent)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('overlap', result.stderr.lower())

if __name__ == '__main__':
    unittest.main()

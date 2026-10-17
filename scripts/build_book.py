"""Render a YAML book into a PDF, PNG pages and portable asset archives."""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import sys
import tempfile
import zipfile

import pymupdf as fitz
from PIL import Image
import yaml
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor


def local_file(root: Path, name: str) -> Path:
    if not isinstance(name, str):
        raise ValueError('Asset path must be a string')
    path = (root / name).resolve()
    if not path.is_relative_to(root):
        raise ValueError(f'Asset must stay inside book folder: {name}')
    if not path.is_file():
        raise ValueError(f'Missing asset: {name}')
    return path


def load_book(config: Path) -> dict:
    data = yaml.safe_load(config.read_text(encoding='utf-8'))
    if not isinstance(data, dict) or data.get('schema_version') != 1:
        raise ValueError('Expected schema_version: 1')
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]*', str(data.get('id', ''))):
        raise ValueError('Book id must contain lowercase letters, digits and hyphens')
    if not isinstance(data.get('title'), str) or not data['title'].strip():
        raise ValueError('Book title is required')
    pages = data.get('pages')
    if not isinstance(pages, list) or not pages:
        raise ValueError('Book must have a non-empty pages list')
    for page in ([data['cover']] if data.get('cover') else []) + pages:
        if not isinstance(page, dict) or not isinstance(page.get('text'), str) or not page['text'].strip():
            raise ValueError('Each page requires non-empty text')
        image = local_file(config.parent, page.get('image'))
        with Image.open(image) as im:
            im.verify()
    local_file(config.parent, data.get('font'))
    return data


def number(data: dict, key: str, default: float, low: float, high: float) -> float:
    value = float(data.get(key, default))
    if not math.isfinite(value) or not low <= value <= high:
        raise ValueError(f'{key} must be between {low} and {high}')
    return value


def archive(path: Path, files: list[tuple[Path, str]]) -> None:
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        for source, name in sorted(files, key=lambda item: item[1]):
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, source.read_bytes())


def build(config: Path, output: Path, dpi_override: int | None = None) -> Path:
    config, output = config.resolve(), output.resolve()
    source = config.parent
    if output == source or source.is_relative_to(output) or output.is_relative_to(source):
        raise ValueError('Source and output folders must not overlap')
    if output.exists() and any(output.iterdir()):
        marker = output / '.read-guides-output'
        if not marker.is_file() or marker.is_symlink() or marker.read_text() != 'read.guides v1\n':
            raise ValueError('Refusing to overwrite unowned output folder; choose an empty folder')
        if any(p.is_symlink() for p in output.rglob('*')):
            raise ValueError('Output folder must not contain symlinks')
    if output.is_relative_to(source) or source.is_relative_to(output):
        raise ValueError('Source and output folders must not overlap')
    # Validate all assets and layout before touching output.
    data = load_book(config)
    size = number(data, 'page_size_inches', 8, 3, 16) * 72
    dpi = dpi_override if dpi_override is not None else number(data, 'dpi', 200, 72, 600)
    if not 72 <= dpi <= 600:
        raise ValueError('dpi must be between 72 and 600')
    font_size = number(data, 'font_size_pt', 32, 12, 80)
    baseline = number(data, 'text_baseline', 0.105, 0.05, 0.17) * size
    color = HexColor(data.get('text_color', '#182B36'))
    font_path = local_file(source, data['font'])
    pdfmetrics.registerFont(TTFont('BookFont', str(font_path)))
    entries = ([dict(data['cover'], is_cover=True)] if data.get('cover') else []) + data['pages']
    for page in entries:
        fs = font_size * 1.25 if page.get('is_cover') else font_size
        if '\n' in page['text'] or pdfmetrics.stringWidth(page['text'], 'BookFont', fs) > size * 0.86:
            raise ValueError(f'Text overflow; shorten text or reduce font_size_pt: {page["text"]}')
        if baseline + fs > size * 0.22:
            raise ValueError('Text exceeds reserved bottom 22% of page')
        subtitle = page.get('subtitle')
        if subtitle is not None and baseline - 25 < 12:
            raise ValueError('Cover subtitle would fall below the page; increase text_baseline')
        if subtitle is not None and (not isinstance(subtitle, str) or '\n' in subtitle or pdfmetrics.stringWidth(subtitle, 'BookFont', 12) > size * .86):
            raise ValueError('Cover subtitle overflows')
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='read-guides-', dir=output.parent) as temp:
        staging = Path(temp)
        (staging/'.read-guides-output').write_text('read.guides v1\n')
        pages_dir = staging/'pages'; pages_dir.mkdir()
        art_dir = staging/'illustrations'; art_dir.mkdir()
        pdf_path = staging/f'{data["id"]}.pdf'
        pdf = canvas.Canvas(str(pdf_path), pagesize=(size, size), invariant=1)
        pdf.setTitle(data['title']); pdf.setAuthor('read.guides')
        pdf.setSubject('Seis cuentos de animales para leer juntos')
        for i, page in enumerate(entries):
            pdf.drawImage(str(local_file(source, page['image'])), 0, 0, width=size, height=size)
            pdf.setFillColor(color)
            pdf.setFont('BookFont', font_size * 1.25 if page.get('is_cover') else font_size)
            pdf.drawCentredString(size/2, baseline, page['text'])
            if page.get('is_cover') and page.get('subtitle'):
                pdf.setFont('BookFont', 12)
                pdf.drawCentredString(size/2, baseline - 25, page['subtitle'])
            pdf.showPage()
        pdf.save()
        with fitz.open(pdf_path) as doc:
            for i, page in enumerate(doc):
                page.get_pixmap(dpi=int(dpi)).save(pages_dir/f'{i:02d}.png')
        for i, page in enumerate(data['pages'], 1):
            shutil.copyfile(local_file(source, page['image']), art_dir/f'{i:02d}.png')
        manifest = {'id':data['id'], 'version':str(data.get('version','1.0.0')), 'title':data['title'], 'page_count':len(entries), 'story_pages':len(data['pages']), 'dpi':int(dpi), 'page_size_inches':size/72, 'pages':[{'file':f'pages/{i:02d}.png','text':p['text'],'source':p['image']} for i,p in enumerate(entries)]}
        (staging/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        archive(staging/f'{data["id"]}-pages.zip', [(p, 'pages/'+p.name) for p in pages_dir.glob('*.png')] + [(staging/'manifest.json','manifest.json')])
        archive(staging/f'{data["id"]}-illustrations.zip', [(p,'illustrations/'+p.name) for p in art_dir.glob('*.png')])
        # Portable bundle contains YAML, art, font and its license, plus editorial notes.
        paths = {config, font_path} | {local_file(source,p['image']) for p in entries}
        paths |= set((source/'fonts').glob('*.txt')) | set(source.glob('*.md'))
        archive(staging/f'{data["id"]}-assets.zip', [(p, data['id']+'/'+p.relative_to(source).as_posix()) for p in paths])
        deliverables = sorted(staging.glob('*.zip')) + [pdf_path, staging/'manifest.json']
        (staging/'SHA256SUMS.txt').write_text(''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n' for p in deliverables), encoding='utf-8')
        # Replace only our own generated directories; preserve unrelated user files.
        output.mkdir(parents=True, exist_ok=True)
        for name in ('pages','illustrations'):
            target = output/name
            if target.exists():
                shutil.rmtree(target)
        for p in staging.iterdir():
            target = output/p.name
            if p.is_dir():
                shutil.copytree(p, target)
            else:
                shutil.copyfile(p, target)
    return output/f'{data["id"]}.pdf'


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('config', type=Path)
    parser.add_argument('--output', type=Path, default=Path('dist/01-se-cayo'))
    parser.add_argument('--dpi', type=int, help='PNG resolution; 72–600 (PDF size is unchanged)')
    args = parser.parse_args()
    try:
        result = build(args.config, args.output, args.dpi)
    except (ValueError, OSError, yaml.YAMLError, TypeError, KeyError) as exc:
        print(f'Build failed: {exc}', file=sys.stderr)
        return 1
    print(f'Built {result}')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())

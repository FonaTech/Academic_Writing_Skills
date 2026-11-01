#!/usr/bin/env python3
"""Render Word documents to PDF and page images for a visual check.

Usage
  render_check.py DOC.docx [DOC2.docx ...] [--out render_check/] [--dpi 70] [--per-sheet 8]

Default conversion: LibreOffice headless. --allow-word-app enables Word/docx2pdf fallbacks.
Each PDF is split into page PNGs and tiled into contact sheets
(4 × 2 pages) that an agent or a person can inspect for equation rendering, table layout,
figure placement, captions, orphaned headings and overflowing tables.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from xml.sax.saxutils import escape

APPLESCRIPT = '''on run argv
    set inPath to item 1 of argv
    set outPath to item 2 of argv
    tell application "Microsoft Word"
        open (POSIX file inPath)
        delay 2
        set theDoc to active document
        save as theDoc file name outPath file format format PDF
        close theDoc saving no
    end tell
end run
'''


def via_word(docx: Path, pdf: Path) -> bool:
    if sys.platform != 'darwin' or not Path('/Applications/Microsoft Word.app').exists():
        return False
    script = pdf.parent / '_export_pdf.applescript'
    script.write_text(APPLESCRIPT, encoding='utf-8')
    try:
        subprocess.run(['osascript', str(script), str(docx.resolve()), str(pdf.resolve())],
                       check=True, capture_output=True, timeout=240)
        for _ in range(40):          # Word writes the PDF asynchronously after the script returns
            if pdf.exists() and pdf.stat().st_size > 0:
                time.sleep(0.5)
                return True
            time.sleep(0.5)
        return False
    except Exception:
        return False
    finally:
        script.unlink(missing_ok=True)


def via_soffice(docx: Path, pdf: Path) -> bool:
    exe = shutil.which('soffice') or shutil.which('libreoffice') or \
        ('/Applications/LibreOffice.app/Contents/MacOS/soffice'
         if Path('/Applications/LibreOffice.app/Contents/MacOS/soffice').exists() else None)
    if not exe:
        return False
    try:
        subprocess.run([exe, '--headless', '--convert-to', 'pdf', '--outdir', str(pdf.parent), str(docx)],
                       check=True, capture_output=True, timeout=300)
        produced = pdf.parent / (docx.stem + '.pdf')
        if produced != pdf and produced.exists():
            produced.replace(pdf)
        return pdf.exists()
    except Exception:
        return False


def via_docx2pdf(docx: Path, pdf: Path) -> bool:
    try:
        from docx2pdf import convert
        convert(str(docx), str(pdf))
        return pdf.exists()
    except Exception:
        return False


def to_pdf(docx: Path, out: Path, allow_word=False) -> Path | None:
    pdf = out / (docx.stem + '.pdf')
    pdf.unlink(missing_ok=True)
    for fn in ((via_soffice, via_word, via_docx2pdf) if allow_word else (via_soffice,)):
        if fn(docx, pdf):
            print(f'{docx.name}: PDF via {fn.__name__[4:]}')
            return pdf
    print(f'{docx.name}: no converter available (install LibreOffice or run on macOS with Word)')
    return None

def configure_fonts(out, directories):
    """Expose existing fonts to headless fontconfig without editing system files."""
    dirs = [Path(d).resolve() for d in directories if Path(d).is_dir()]
    if not dirs:
        return
    folder = out.resolve()/'fontconfig'
    folder.mkdir(parents=True, exist_ok=True)
    cache = folder/'cache'
    cache.mkdir(exist_ok=True)
    config = folder/'fonts.conf'
    config.write_text('<?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "fonts.dtd"><fontconfig>'+
        ''.join('<dir>'+escape(str(d))+'</dir>' for d in dirs)+
        '<cachedir>'+escape(str(cache))+'</cachedir></fontconfig>', encoding='utf-8')
    os.environ['FONTCONFIG_FILE'] = str(config)
    print('Headless fonts: '+', '.join(str(d) for d in dirs))


def sheets(pdf: Path, out: Path, dpi: int, per_sheet: int):
    from PIL import Image
    try:
        import fitz
        doc = fitz.open(pdf)
        engine = 'fitz'
    except ImportError:
        import pypdfium2
        doc = pypdfium2.PdfDocument(str(pdf))
        engine = 'pdfium'
    pages = []
    for i, page in enumerate(doc, start=1):
        png = out / f'{pdf.stem}_p{i:03d}.png'
        if engine == 'fitz':
            page.get_pixmap(dpi=dpi).save(str(png))
        else:
            page.render(scale=dpi/72).to_pil().save(png)
        pages.append(png)
    cols = 4
    for s in range(0, len(pages), per_sheet):
        group = [Image.open(p) for p in pages[s:s + per_sheet]]
        w, h = group[0].size
        rows = (len(group) + cols - 1) // cols
        canvas = Image.new('RGB', (w * cols, h * rows), 'white')
        for k, im in enumerate(group):
            canvas.paste(im, ((k % cols) * w, (k // cols) * h))
        name = out / f'{pdf.stem}_sheet{s // per_sheet + 1:02d}.png'
        canvas.save(name)
        print(f'  {name.name}: pages {s + 1}-{s + len(group)}')
    return len(pages)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('docs', nargs='+')
    ap.add_argument('--out', default='render_check')
    ap.add_argument('--dpi', type=int, default=70)
    ap.add_argument('--per-sheet', type=int, default=8)
    ap.add_argument('--font-dir', action='append', default=[], help='existing font directory; repeat as needed')
    ap.add_argument('--allow-word-app', action='store_true', help='allow fallbacks that open Microsoft Word')
    args = ap.parse_args(argv)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    dirs = args.font_dir or (['/System/Library/Fonts','/Library/Fonts'] if sys.platform == 'darwin' else [])
    configure_fonts(out, dirs)
    failed = 0
    for d in args.docs:
        pdf = to_pdf(Path(d), out, args.allow_word_app)
        if pdf:
            n = sheets(pdf, out, args.dpi, args.per_sheet)
            print(f'  {n} pages')
        else:
            failed += 1
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())

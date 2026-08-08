#!/usr/bin/env python3
"""Render guide.html to a print-ready PDF.

The on-screen guide is a dark, single-page app with a sticky sidebar and collapsed rules
blocks — none of which prints well, and the collapsed blocks would silently drop content.
This builds a print variant (light theme, sidebar dropped, every <details> expanded, cover
page + contents, page breaks kept out of diagrams) and drives headless Chrome over it.

    ./make-pdf.py [-o OUTPUT.pdf] [--keep-html]

Requires: google-chrome (or chromium) on PATH.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "guide.html"
DEFAULT_OUT = HERE / "Mayne-SMC-Visual-Guide.pdf"
BROWSERS = ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser")

PRINT_CSS = """
  .printhead{display:none}
  @media print {
    @page { size: A4; margin: 14mm 12mm; }
    nav, .themebtn, #tip { display: none !important; }
    .layout { display: block; max-width: none; }
    main { max-width: none; padding: 0; }
    body { font-size: 10.5pt; }
    h2 { font-size: 15pt; break-after: avoid; break-before: page; }
    #intro h2 { break-before: avoid; }
    h3, h4 { break-after: avoid; }
    .chart, .cap, table, .zt, .card, details { break-inside: avoid; }
    .chart { page-break-inside: avoid; }
    .cap { break-before: avoid; }
    tr, li, p { break-inside: avoid; }
    details > summary { list-style: none; font-weight: 600; }
    a { text-decoration: none; }
    * { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    .printhead{display:block; break-after:page}
    .printhead h1{font-size:24pt; margin:0 0 6px}
    .printhead .sub{color:var(--muted); font-size:11pt; margin:0 0 26px}
    .printhead h3{font-size:13pt; margin:0 0 8px}
    .printhead .toc{columns:2; list-style:none; padding-left:0; font-size:10.5pt; line-height:1.9}
  }
"""


def find_browser() -> str:
    for name in BROWSERS:
        path = shutil.which(name)
        if path:
            return path
    sys.exit("no Chrome/Chromium on PATH — install one or render guide.html by hand (Ctrl+P)")


def build_print_html(html: str) -> str:
    html = html.replace('<html lang="en" data-theme="dark">', '<html lang="en" data-theme="light">')
    html = html.replace("<details>", "<details open>")
    # the toggle would otherwise restore a saved dark theme over the print styling
    html = html.replace('if(saved) root.setAttribute("data-theme",saved);',
                        "/* print build: theme pinned to light */")

    # contents come from the nav, so they can never drift from the actual headings
    sections = re.findall(r'<a href="#[^"]+">([^<]+)</a>', html)
    items = "\n".join("        <li>%s</li>" % s for s in sections)
    cover = (
        '      <div class="printhead">\n'
        "        <h1>Trader Mayne SMC — Visual Guide</h1>\n"
        '        <p class="sub">The Whiteboard Series (episodes 1–17) as one illustrated\n'
        "          reference, with the companion Pine indicator. Every concept is drawn as\n"
        "          schematic candles.</p>\n"
        "        <h3>Contents</h3>\n"
        '        <ol class="toc">\n%s\n        </ol>\n'
        "      </div>\n" % items
    )
    html, n = re.subn(r"(<main[^>]*>\n)", lambda m: m.group(1) + cover, html, count=1)
    if not n:
        sys.exit("could not find <main> to insert the cover page")
    return html.replace("</style>", PRINT_CSS + "</style>")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("-o", "--output", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--keep-html", action="store_true", help="leave the print HTML next to the PDF")
    args = ap.parse_args()

    if not SOURCE.exists():
        sys.exit(f"missing {SOURCE}")
    printable = build_print_html(SOURCE.read_text(encoding="utf-8"))

    with tempfile.TemporaryDirectory() as tmp:
        stage = Path(tmp) / "guide-print.html"
        stage.write_text(printable, encoding="utf-8")
        if args.keep_html:
            (args.output.with_suffix(".print.html")).write_text(printable, encoding="utf-8")
        subprocess.run([
            find_browser(), "--headless", "--disable-gpu", "--no-sandbox",
            "--no-pdf-header-footer", "--virtual-time-budget=15000",
            f"--print-to-pdf={args.output}", stage.as_uri(),
        ], check=True, capture_output=True)

    size = args.output.stat().st_size
    pages = len(re.findall(rb"/Type\s*/Page[^s]", args.output.read_bytes()))
    print(f"{args.output}  —  {pages} pages, {size/1048576:.1f} MB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

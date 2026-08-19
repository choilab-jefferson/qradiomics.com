#!/usr/bin/env python3
"""Render the wiki CV page to the public CV PDF.

    python scripts/cv-to-pdf.py [source.md] [out.pdf]

Defaults: wiki/content-corpus/curriculum-vitae.md -> content/profile/images/wookjin-choi-cv.pdf

The wiki page is the source of truth. Two markers keep private/editorial content out of
the published PDF:

  <!-- wiki-only:start --> ... <!-- wiki-only:end -->   block dropped
  <line> <!-- private -->                               line dropped

Numbered CV lists (publications, abstracts) restart at 1 in each Markdown subsection;
this script renumbers them continuously within "Publications, Peer Reviewed" and
within "Abstracts", the way the CV is meant to read.
"""
import re
import sys
from pathlib import Path

import markdown
from weasyprint import HTML

ROOT = Path(__file__).resolve().parent.parent
SRC = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / "wiki/content-corpus/curriculum-vitae.md"
OUT = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else ROOT / "content/profile/images/wookjin-choi-cv.pdf"

# Sections whose <ol> numbering runs continuously across their subsections.
CONTINUOUS = ("Publications, Peer Reviewed", "Abstracts",
               "Issued Patents and Other Intellectual Property")

CSS = """
@page {
  size: Letter;
  margin: 0.75in 0.75in 0.65in 0.75in;
  @bottom-right { content: counter(page) " | Page"; font: 9pt Georgia, serif; color: #444; }
}
body { font: 10pt/1.35 Georgia, 'Times New Roman', serif; color: #111; }
h1 { font-size: 20pt; margin: 0 0 2pt; letter-spacing: .02em; }
h2 { font-size: 12.5pt; margin: 16pt 0 5pt; padding-bottom: 2pt;
     border-bottom: 1px solid #999; text-transform: uppercase; letter-spacing: .05em;
     break-after: avoid; }
h3 { font-size: 11pt; margin: 10pt 0 3pt; font-style: italic; break-after: avoid; }
h4 { font-size: 10.5pt; margin: 9pt 0 3pt; font-weight: bold; break-after: avoid; }
p { margin: 4pt 0; }
ul, ol { margin: 4pt 0 4pt 0; padding-left: 20pt; }
li { margin: 2pt 0; break-inside: avoid; }
hr { border: 0; border-top: 1px solid #bbb; margin: 12pt 0; }
.contact { font-size: 10pt; color: #333; margin-bottom: 10pt; }
.contact strong { font-size: 11pt; color: #111; }
strong { font-weight: bold; }
"""


def strip_private(text: str) -> str:
    text = re.sub(r"<!-- wiki-only:start -->.*?<!-- wiki-only:end -->\n?", "", text, flags=re.S)
    text = "\n".join(l for l in text.splitlines() if "<!-- private -->" not in l)
    return re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S)  # YAML frontmatter


def renumber(html: str) -> str:
    """Continue <ol> numbering across the subsections of each CONTINUOUS section.

    WeasyPrint ignores the HTML ``start`` attribute, so the offset is applied with
    ``counter-reset: list-item N``.
    """
    out, count, level = [], 0, 0  # level = heading depth that switched numbering on (0 = off)
    for chunk in re.split(r"(<h[1-4][^>]*>.*?</h[1-4]>|<ol>)", html, flags=re.S):
        if chunk.startswith("<h"):
            depth = int(chunk[2])
            heading = re.sub(r"<[^>]+>", "", chunk).strip()
            if any(s.lower() == heading.lower() for s in CONTINUOUS):
                level, count = depth, 0
            elif level and depth <= level:
                level, count = 0, 0
        elif chunk == "<ol>":
            if level and count:
                chunk = f'<ol style="counter-reset: list-item {count};">'
        elif level:
            count += chunk.count("<li>")
        out.append(chunk)
    return "".join(out)


def main() -> None:
    md = strip_private(SRC.read_text())
    body = markdown.markdown(md, extensions=["extra", "sane_lists", "smarty"])
    body = renumber(body)
    # The address/phone/email block right after the title is a plain paragraph.
    body = body.replace("<p><strong>Wookjin Choi, PhD</strong>", '<p class="contact"><strong>Wookjin Choi, PhD</strong>', 1)
    body = body.replace("<p>Office Address:", '<p class="contact">Office Address:', 1)
    html = f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=html, base_url=str(ROOT)).write_pdf(OUT)
    print(f"{SRC} -> {OUT}")


if __name__ == "__main__":
    main()

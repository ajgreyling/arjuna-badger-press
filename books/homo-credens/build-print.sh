#!/bin/sh
# Render the print edition of "Homo Credens" as an A4 PDF for normal printers.
#
# Pipeline: python assembles the book as a SEQUENCE of small HTML fragments
# (title/copyright/TOC, one per chapter, one per full-bleed plate) rather than
# one giant HTML file. Each fragment is printed to its own single-purpose PDF
# by Chrome headless, then all PDFs are concatenated in order with pdfunite.
#
# Why split like this: rendering the whole book as one ~50-100MB HTML file
# triggered a reproducible Chrome headless bug where every full-bleed plate
# page (part frontispieces, standalone art plates, the PD photo gallery)
# rendered at roughly 2/3 scale instead of filling the page — confirmed to be
# specific to large-document paged-media layout, since the EXACT same CSS and
# EXACT same images render correctly as small standalone documents. Splitting
# each plate into its own tiny single-page HTML/PDF sidesteps the bug by
# construction: Chrome never sees a large document while laying out a plate.
set -e
cd "$(dirname "$0")"

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
WORK=$(mktemp -d -t hc-print)
trap 'rm -rf "$WORK"' EXIT

# Print-quality downsized cache (2000px JPEG q85) — separate from the epub's
# 1000px cache since print wants more resolution. Derived/disposable.
mkdir -p art/print-cache

FONT_DIR="$HOME/Library/Fonts"
cp "$FONT_DIR/Atkinson-Hyperlegible-Regular-102.otf" art/print-cache/AtkinsonHyperlegible-Regular.otf
cp "$FONT_DIR/Atkinson-Hyperlegible-Bold-102.otf" art/print-cache/AtkinsonHyperlegible-Bold.otf
cp "$FONT_DIR/Atkinson-Hyperlegible-Italic-102.otf" art/print-cache/AtkinsonHyperlegible-Italic.otf
cp "$FONT_DIR/Atkinson-Hyperlegible-BoldItalic-102.otf" art/print-cache/AtkinsonHyperlegible-BoldItalic.otf

# A4, no bleed — this edition targets a normal office/home printer, not a
# commercial press that trims from an oversized sheet.
BLEED_IN=0
PAGE_W=$(python3 -c "print(round(210 / 25.4, 4))")
PAGE_H=$(python3 -c "print(round(297 / 25.4, 4))")
MARGIN_TOP=0.9; MARGIN_RIGHT=0.85; MARGIN_BOTTOM=0.9; MARGIN_LEFT=0.85
OUT_NAME="Homo Credens (print A4).pdf"

# Shared @font-face + text-page CSS (used by every non-plate fragment).
cat > "$WORK/text.css" <<CSS
@font-face { font-family: "Atkinson Hyperlegible"; src: url("$(pwd)/art/print-cache/AtkinsonHyperlegible-Regular.otf"); font-weight: 400; font-style: normal; }
@font-face { font-family: "Atkinson Hyperlegible"; src: url("$(pwd)/art/print-cache/AtkinsonHyperlegible-Bold.otf"); font-weight: 700; font-style: normal; }
@font-face { font-family: "Atkinson Hyperlegible"; src: url("$(pwd)/art/print-cache/AtkinsonHyperlegible-Italic.otf"); font-weight: 400; font-style: italic; }
@font-face { font-family: "Atkinson Hyperlegible"; src: url("$(pwd)/art/print-cache/AtkinsonHyperlegible-BoldItalic.otf"); font-weight: 700; font-style: italic; }

/* Running head and folio are NOT done via CSS @page counters here: Chrome
   headless does not honor counter-reset: page N as a starting offset for
   the built-in paged-media page counter (confirmed by isolated test -- it
   stays pinned at N on every page of the document instead of incrementing).
   Since this pipeline prints each section as an independent Chrome document,
   that makes continuous numbering via CSS impossible here. Both the running
   head and the folio are burned in by a post-stitch pypdf pass instead (see
   bottom of this script), which also means every page in the final PDF gets
   a consistent header/footer regardless of which of the 48 Chrome jobs it
   came from. */
@page {
  size: ${PAGE_W}in ${PAGE_H}in;
  margin: calc(${MARGIN_TOP}in + ${BLEED_IN}in) calc(${MARGIN_RIGHT}in + ${BLEED_IN}in)
          calc(${MARGIN_BOTTOM}in + ${BLEED_IN}in) calc(${MARGIN_LEFT}in + ${BLEED_IN}in);
}

html { font-size: 12pt; }
body { font-family: "Atkinson Hyperlegible", Georgia, sans-serif; line-height: 1.55;
       color: #111; max-width: none; margin: 0; padding: 0; }
#title-block-header { display: none; }

.copyright-page, .toc-page { font-size: 0.92rem; }
.copyright-page h1, .toc-page h1 { font-size: 1.3rem; }
.copyright-page hr { display: none; }

h1 { page-break-before: always; font-size: 1.6rem; margin-top: 2.2rem; letter-spacing: .02em; }
h1:first-child { page-break-before: avoid; }

.vignette { text-align: center; margin: 0.8rem 0 1.2rem; }
.vignette img { max-width: 55%; }
blockquote { font-style: italic; color: #333; border: none; margin: 1rem 2rem; }
img { max-width: 100%; }
p { orphans: 2; widows: 2; text-align: justify; hyphens: auto; }
CSS

# Standalone single-page CSS for full-bleed plates: page is EXACTLY the
# bleed box, zero margin, image forced to fill it edge to edge. No @page
# margin math at all here, so there's nothing for a large-document bug to
# perturb — this file is only ever a few KB plus one embedded image.
cat > "$WORK/plate.css" <<CSS
@page { size: ${PAGE_W}in ${PAGE_H}in; margin: 0; }
html, body { margin: 0; padding: 0; }
.plate { position: relative; width: ${PAGE_W}in; height: ${PAGE_H}in; overflow: hidden; }
.plate img { width: 100%; height: 100%; object-fit: cover; display: block; }
.plate .cap { position: absolute; bottom: calc(${BLEED_IN}in + 0.25in); left: 0; right: 0;
     text-align: center; font-size: 8.5pt; font-family: "Atkinson Hyperlegible", sans-serif;
     color: #ccc; }
@font-face { font-family: "Atkinson Hyperlegible"; src: url("$(pwd)/art/print-cache/AtkinsonHyperlegible-Regular.otf"); }
CSS

python3 - "$WORK" <<'PY'
import os, re, subprocess, sys

WORK = sys.argv[1]

def cache(src):
    if not os.path.exists(src):
        return None
    key = src.replace("/", "-")
    out = f"art/print-cache/{key}.jpg"
    if out.endswith(".jpg.jpg"):
        out = f"art/print-cache/{key}"
    if not os.path.exists(out) or os.path.getmtime(src) > os.path.getmtime(out):
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "85",
                         "--resampleWidth", "2000", src, "--out", out],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return os.path.abspath(out)

PARTS = {
    1:  ("PART I — THE INVENTION OF THE GODS",  "art/part-1-invention-of-the-gods.png"),
    4:  ("PART II — THE BUREAUCRACY OF HEAVEN", "art/part-2-bureaucracy-of-heaven.png"),
    9:  ("PART III — THE AXIAL GAMBLE",         "art/part-3-the-axial-gamble.png"),
    15: ("PART IV — CONQUERING HEAVENS",        "art/part-4-conquering-heavens.png"),
    20: ("PART V — GOD ON TRIAL",               "art/part-5-god-on-trial.png"),
}

chapters = sorted(f for f in os.listdir("chapters") if re.match(r"ch-\d\d-.*\.md$", f))

def chapter_title(fname):
    text = open(os.path.join("chapters", fname), encoding="utf-8").read()
    m = re.search(r"^#\s+Chapter\s+\d+\s*[—-]\s*(.+)$", text, re.M)
    return m.group(1).strip() if m else fname

# Manifest of (kind, payload) fragments in final book order.
# kind: "text" (markdown, goes through pandoc + text.css) or "plate" (raw
# html snippet, goes through plate.css as its own single page).
manifest = []

cover = cache("art/cover.png")
if cover:
    manifest.append(("plate", (cover, None)))

manifest.append(("text", '<div class="front-matter">\n\n' + open("00-front-matter.md").read() + '\n\n</div>\n'))

copyright_md = (
    '<div class="copyright-page">\n\n'
    "HOMO CREDENS\n===\n\n"
    "*A History of Religion, from the First Graves to 1900*\n\n"
    "*The Illustrated Edition*\n\n"
    "Copyright (c) 2026 Arjuna Badger Press.\n\n"
    "All rights reserved. No part of this publication may be reproduced, "
    "distributed, or transmitted in any form or by any means, including "
    "photocopying, recording, or other electronic or mechanical methods, "
    "without the prior written permission of the publisher, except in the "
    "case of brief quotations embodied in critical reviews and certain "
    "other noncommercial uses permitted by copyright law.\n\n"
    "Scripture quotations are drawn verbatim from public-domain translations; "
    "see Sources & Further Reading for the edition used in each case. "
    "The engraved plates and chapter vignettes are original artwork "
    "commissioned for this edition. Photographic plates are in the public "
    "domain or released under CC0; see Image Credits for sources.\n\n"
    "First edition.\n\n"
    "Published by Arjuna Badger Press.\n\n"
    "ISBN: [to be assigned]\n\n"
    "\n\n</div>\n"
)
manifest.append(("text", copyright_md))

toc = ['<div class="toc-page">\n\n# Contents\n\n']
part_open_at = {n: label for n, (label, _img) in PARTS.items()}
for f in chapters:
    n = int(f[3:5])
    title = chapter_title(f)
    if n in part_open_at:
        toc.append(f"\n**{part_open_at[n]}**\n\n")
    toc.append(f"Chapter {n} — {title}\n\n")
toc.append("\nSources & Further Reading\n\nImage Credits\n\n\n\n</div>\n")
manifest.append(("text", "".join(toc)))

for plate, cap in [("art/endpaper-armillary.png", "The armillary of the heavens"),
                   ("art/symbology.png", "The Signs of the Faiths — the 28 traditions"),
                   ("art/timeline-rivers-of-faith.png", "The Rivers of Faith — five millennia in one delta")]:
    c = cache(plate)
    if c:
        manifest.append(("plate", (c, cap)))

for f in chapters:
    n = int(f[3:5])
    if n in PARTS:
        title, img = PARTS[n]
        c = cache(img)
        if c:
            manifest.append(("plate", (c, None)))
    vin = cache(f"art/ch-{n:02d}-vignette.png")
    body = open(os.path.join("chapters", f)).read()
    if vin:
        body = re.sub(r"^(# [^\n]+\n)", rf'\1\n<div class="vignette">\n\n![]({vin})\n\n</div>\n', body, count=1)
    manifest.append(("text", f'<div class="chapter-body">\n\n{body}\n\n</div>\n'))

if os.path.isdir("art/pd"):
    manifest.append(("text", '<div class="chapter-body">\n\n# Plates — Artifacts, Sites & Places\n\n</div>\n'))
    for part in sorted(os.listdir("art/pd")):
        pdir = os.path.join("art/pd", part)
        if not os.path.isdir(pdir):
            continue
        for img in sorted(os.listdir(pdir)):
            if img.lower().endswith((".jpg", ".jpeg", ".png")):
                name = os.path.splitext(img)[0].replace("-", " ")
                c = cache(os.path.join(pdir, img))
                if c:
                    manifest.append(("plate", (c, name)))

if os.path.exists("backmatter/BIBLIOGRAPHY.md"):
    manifest.append(("text", '<div class="chapter-body">\n\n' + open("backmatter/BIBLIOGRAPHY.md").read() + '\n\n</div>\n'))

credits = []
if os.path.isdir("art/pd"):
    for part in sorted(os.listdir("art/pd")):
        c = os.path.join("art/pd", part, "CREDITS.md")
        if os.path.exists(c):
            credits.append(open(c).read())
if credits:
    manifest.append(("text", '<div class="chapter-body">\n\n# Image Credits\n\nThe engraved plates and vignettes are original artwork made for this edition. The photographic plates are public-domain images via Wikimedia Commons:\n\n</div>\n'))
    for c in credits:
        manifest.append(("text", f'<div class="chapter-body">\n\n{c}\n\n</div>\n'))

# Coalesce consecutive "text" fragments into as few pandoc docs as possible
# (keeps page-count/running-header context correct across chapter breaks)
# while every "plate" fragment stays fully isolated as its own tiny document.
jobs = []  # list of ("text", markdown_str) | ("plate", (img_path, caption))
buf = []
for kind, payload in manifest:
    if kind == "text":
        buf.append(payload)
    else:
        if buf:
            jobs.append(("text", "\n\n".join(buf)))
            buf = []
        jobs.append(("plate", payload))
if buf:
    jobs.append(("text", "\n\n".join(buf)))

manifest_path = os.path.join(WORK, "jobs.json")
import json
job_files = []
first_text_seen = False
for i, (kind, payload) in enumerate(jobs):
    # The FIRST text job is always the coalesced front-matter/copyright/TOC
    # block — no running head or folio. Every plate (including the cover,
    # which may precede it) is unnumbered too. Everything else is a real
    # body page. Tracked by "first text job seen" rather than job index 0,
    # since a cover plate can now occupy index 0 instead of the front matter.
    numbered = False
    if kind == "text":
        if not first_text_seen:
            first_text_seen = True
        else:
            numbered = True
    if kind == "text":
        p = os.path.join(WORK, f"job-{i:04d}.md")
        open(p, "w", encoding="utf-8").write(payload)
        job_files.append({"kind": "text", "path": p, "numbered": numbered})
    else:
        img_path, cap = payload
        p = os.path.join(WORK, f"job-{i:04d}.html")
        cap_html = f'<div class="cap">{cap}</div>' if cap else ""
        open(p, "w", encoding="utf-8").write(
            f'<html><head><link rel="stylesheet" href="{WORK}/plate.css"></head>'
            f'<body><div class="plate"><img src="file://{img_path}">{cap_html}</div></body></html>'
        )
        job_files.append({"kind": "plate", "path": p, "numbered": False})

json.dump(job_files, open(manifest_path, "w"))
print(f"assembled {len(job_files)} print jobs ({sum(1 for j in job_files if j['kind']=='text')} text, {sum(1 for j in job_files if j['kind']=='plate')} plate)")
PY

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Render every job in true manifest order, driven by jobs.json — NOT by
# shelling out to `for job in *.md *.html`, which sorts the .md files and
# .html files as two SEPARATE alphabetic groups instead of interleaving them
# by index. That bug silently moved every plate (part frontispieces,
# standalone plates, the whole PD photo gallery — 41 jobs) to after all the
# text, instead of interleaved through the book as the manifest intends.
python3 - "$WORK" "$CHROME" <<'PY'
import json, os, subprocess, sys

WORK, CHROME = sys.argv[1], sys.argv[2]
jobs = json.load(open(os.path.join(WORK, "jobs.json")))

pdf_parts = []
page_map = []  # per rendered PDF page: True if it should get a running head + folio
for i, job in enumerate(jobs):
    num = f"{i:04d}"
    part_pdf = os.path.join(WORK, f"part-{num}.pdf")
    if job["kind"] == "text":
        html = os.path.join(WORK, f"job-{num}.md.html")
        subprocess.run(["pandoc", job["path"], "-o", html, "--standalone",
                         "--embed-resources", f"--css={WORK}/text.css"], check=True)
        subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                         f"--print-to-pdf={part_pdf}", f"file://{html}"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    else:
        subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                         f"--print-to-pdf={part_pdf}", f"file://{job['path']}"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    n_pages = int(subprocess.run(["pdfinfo", part_pdf], capture_output=True, text=True)
                  .stdout.split("Pages:")[1].split()[0])
    pdf_parts.append(part_pdf)
    page_map.extend([job["numbered"]] * n_pages)

json.dump(page_map, open(os.path.join(WORK, "page_map.json"), "w"))
json.dump(pdf_parts, open(os.path.join(WORK, "pdf_parts.json"), "w"))
print(f"rendered {len(pdf_parts)} job PDFs, {len(page_map)} total pages")
PY

STITCHED="$WORK/stitched.pdf"
pdfunite $(python3 -c "import json; print(' '.join(json.load(open('$WORK/pdf_parts.json'))))") "$STITCHED"

# Burn in the running head + folio on every numbered page, using the same
# venv-installed pypdf used for the rest of this pipeline's post-processing.
PDFVENV="/tmp/pdfvenv/bin/python"
if [ ! -x "$PDFVENV" ]; then
  python3 -m venv /tmp/pdfvenv
  /tmp/pdfvenv/bin/pip install --quiet pypdf reportlab
fi

"$PDFVENV" - "$WORK" "$STITCHED" "$OUT_NAME" <<'PY'
import json, os, sys
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from io import BytesIO

WORK, STITCHED, OUT_NAME = sys.argv[1], sys.argv[2], sys.argv[3]
page_map = json.load(open(os.path.join(WORK, "page_map.json")))

reader = PdfReader(STITCHED)
writer = PdfWriter()

page_w = float(reader.pages[0].mediabox.width)
page_h = float(reader.pages[0].mediabox.height)

folio = 0
for i, page in enumerate(reader.pages):
    numbered = page_map[i] if i < len(page_map) else False
    if numbered:
        folio += 1
        buf = BytesIO()
        c = canvas.Canvas(buf, pagesize=(page_w, page_h))
        c.setFont("Helvetica", 8.5)
        c.setFillGray(0.4)
        c.drawCentredString(page_w / 2, page_h - 0.55 * inch, "HOMO CREDENS")
        c.setFont("Helvetica", 9)
        c.setFillGray(0.27)
        c.drawCentredString(page_w / 2, 0.5 * inch, str(folio))
        c.save()
        buf.seek(0)
        overlay = PdfReader(buf).pages[0]
        page.merge_page(overlay)
    writer.add_page(page)

with open(OUT_NAME, "wb") as f:
    writer.write(f)
print(f"numbered {folio} of {len(reader.pages)} pages")
PY

echo "rendered: $(pwd)/$OUT_NAME ($(du -h "$OUT_NAME" | cut -f1))"

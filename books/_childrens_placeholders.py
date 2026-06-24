#!/usr/bin/env python3
"""Generate matching PLACEHOLDER art + cover.json for the Children's Library folktale books, by
reading each manuscript's actual image markers so filenames always line up. Real ChatGPT art
replaces these file-by-file. Run from the press repo root: python3 books/_childrens_placeholders.py
"""
import json
import os
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent          # books/
MARK = re.compile(r'image="([^"]+)"')
TITLE = re.compile(r'^#\s+(.+)$', re.M)

# id -> (accent hex, cover tagline)
BOOKS = {
    "why-elephant-trunk":     ("#C8865B", "Pull… and pull… and PULL!"),
    "how-zebra-got-stripes":  ("#6B7B8C", "Light and shadow, shadow and light."),
    "how-fire-came":          ("#C2401E", "Carry it gently. Don't let it go."),
    "bird-of-paradise-flower":("#E08A2B", "Still it lifts its face to the sky."),
    "how-king-lion":          ("#A8443C", "Look up, and remember the sky."),
}


def _font(size):
    for p in ("/System/Library/Fonts/Supplemental/Arial.ttf",
              "/System/Library/Fonts/Helvetica.ttc"):
        if Path(p).is_file():
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def panel(w, h, label, scene, accent):
    img = Image.new("RGB", (w, h), (236, 222, 180))
    d = ImageDraw.Draw(img)
    ac = tuple(int(accent.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
    d.rounded_rectangle([w*0.04, h*0.04, w*0.96, h*0.96],
                        radius=int(min(w, h)*0.05), outline=ac, width=max(4, w//220))

    def centre(text, font, y, fill):
        bb = d.textbbox((0, 0), text, font=font)
        d.text(((w-(bb[2]-bb[0]))/2, y), text, font=font, fill=fill)

    centre("PLACEHOLDER", _font(int(h*0.034)), h*0.12, (150, 70, 40))
    centre(label, _font(int(h*0.08)), h*0.38, (40, 46, 70))
    # wrap scene to ~38 chars
    words, line, lines = scene.split(), "", []
    for wd in words:
        if len(line)+len(wd) > 38:
            lines.append(line); line = wd
        else:
            line = (line+" "+wd).strip()
    if line:
        lines.append(line)
    for i, ln in enumerate(lines[:3]):
        centre(ln, _font(int(h*0.042)), h*(0.56+i*0.07), (70, 60, 45))
    # full-colour grain to clear the 500KB cover gate
    noise = Image.frombytes("RGB", (w, h), os.urandom(w*h*3))
    return Image.blend(img, noise, 0.10)


def main():
    for bid, (accent, tagline) in BOOKS.items():
        bdir = ROOT / bid
        mss = (bdir / "build" / "chapters" / "PICTURE_BOOK.md").read_text(encoding="utf-8")
        title_m = TITLE.search(mss)
        title = title_m.group(1).strip() if title_m else bid
        imgs = ROOT / bid / "design" / "images"
        imgs.mkdir(parents=True, exist_ok=True)
        # cover.json
        cj = bdir / "design" / "cover.json"
        cj.write_text(json.dumps({
            "title": title, "eyebrow": "CHILDREN'S LIBRARY · CLASSIC AFRICAN STORIES",
            "tagline": tagline, "author": "ANDRIES J. GREYLING",
            "accent": accent, "prompt_file": "cover-prompt.txt", "numeral": "",
        }), encoding="utf-8")
        # cover
        panel(1600, 2000, title.upper()[:18], tagline, accent).save(bdir / "design" / "cover.png")
        # spreads — read actual filenames from the manuscript
        names = []
        for m in MARK.finditer(mss):
            fn = m.group(1)
            if fn.startswith(("http", "assets/")):
                continue
            names.append(fn)
        for i, fn in enumerate(dict.fromkeys(names), 1):  # de-dup, keep order
            panel(2000, 1333, f"S{i:02d}", title, accent).save(imgs / fn)
        print(f"{bid}: cover + {len(set(names))} spreads")


if __name__ == "__main__":
    main()

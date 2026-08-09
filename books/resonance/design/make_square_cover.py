#!/usr/bin/env python3
"""Square audiobook cover for RESONANCE (Authors Republic / ACX).

Builds a 2400×2400 RGB JPG from design/cover-plate.png with the same Atkinson
lockup as the portrait cover. Filename is alphanumeric-only (AR requirement).

Output:
  design/RESONANCESquareCover.jpg
  design/cover-square.png   (house reference)
  audio/steven-g/RESONANCESquareCover.jpg  (handy for upload)

Usage:
    python3 design/make_square_cover.py
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

HERE = Path(__file__).resolve().parent
BOOK = HERE.parent
REPO = BOOK.parents[1]
_ATK = REPO / "assets" / "fonts"
ATK_REG = str(_ATK / "AtkinsonHyperlegible-Regular.otf")
ATK_BOLD = str(_ATK / "AtkinsonHyperlegible-Bold.otf")
ATK_ITAL = str(_ATK / "AtkinsonHyperlegible-Italic.otf")

SIZE = 2400
SHADOW = (8, 6, 4, 235)
INK = (245, 220, 158, 255)       # honey gold
ACCENT = (229, 181, 103, 255)    # ochre

PLATE = HERE / "cover-plate.png"
OUT_JPG = HERE / "RESONANCESquareCover.jpg"
OUT_PNG = HERE / "cover-square.png"
OUT_UPLOAD = BOOK / "audio" / "steven-g" / "RESONANCESquareCover.jpg"


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def text_width(draw, s, fnt, tracking):
    w = 0
    for ch in s:
        w += draw.textlength(ch, font=fnt) + tracking
    return w - tracking if s else 0


def _place(d, cx, y, s, fnt, tracking, fill, dx=0, dy=0):
    total = text_width(d, s, fnt, tracking)
    x = cx - total / 2
    for ch in s:
        d.text((x + dx, y + dy), ch, font=fnt, fill=fill)
        x += d.textlength(ch, font=fnt) + tracking


def draw_tracked(img, cx, y, s, fnt, tracking, fill, shadow=True, glow=5):
    if shadow:
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        _place(ld, cx, y, s, fnt, tracking, SHADOW, dx=2, dy=3)
        layer = layer.filter(ImageFilter.GaussianBlur(glow))
        img = Image.alpha_composite(img, layer)
        img = Image.alpha_composite(img, layer)
    top = Image.new("RGBA", img.size, (0, 0, 0, 0))
    td = ImageDraw.Draw(top)
    _place(td, cx, y, s, fnt, tracking, fill)
    return Image.alpha_composite(img, top)


def fit_square(plate: Image.Image) -> Image.Image:
    """Cover-fill plate into SIZE×SIZE, centred (keeps the figure + shaft)."""
    art = ImageOps.exif_transpose(plate).convert("RGB")
    aw, ah = art.size
    scale = max(SIZE / aw, SIZE / ah)
    nw, nh = int(aw * scale + 0.5), int(ah * scale + 0.5)
    art = art.resize((nw, nh), Image.Resampling.LANCZOS)
    # Bias crop slightly upward so the light shaft + figure sit in the optical centre
    # under the title block (not dead geometric centre).
    x0 = (nw - SIZE) // 2
    y0 = max(0, (nh - SIZE) // 2 - int(SIZE * 0.04))
    if y0 + SIZE > nh:
        y0 = nh - SIZE
    return art.crop((x0, y0, x0 + SIZE, y0 + SIZE))


def typeset() -> Path:
    if not PLATE.is_file():
        raise SystemExit(f"missing plate: {PLATE}")

    img = fit_square(Image.open(PLATE)).convert("RGBA")
    cx = SIZE / 2

    # Soft scrims for type legibility
    scrim = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrim)
    top_end = int(SIZE * 0.38)
    for y in range(top_end):
        a = int(175 * (1 - y / top_end) ** 1.2)
        sd.line([(0, y), (SIZE, y)], fill=(6, 5, 4, a))
    bot_start = int(SIZE * 0.78)
    for y in range(bot_start, SIZE):
        a = int(185 * ((y - bot_start) / (SIZE - bot_start)) ** 1.15)
        sd.line([(0, y), (SIZE, y)], fill=(6, 5, 4, a))
    img = Image.alpha_composite(img, scrim)

    # Series eyebrow + numeral
    img = draw_tracked(img, cx, int(SIZE * 0.055), "THE AFRICAN GOLD TRILOGY",
                       font(ATK_REG, 42), 10, ACCENT)
    img = draw_tracked(img, cx, int(SIZE * 0.055) + 54, "BOOK ONE",
                       font(ATK_REG, 36), 12, INK)

    rule_y = int(SIZE * 0.055) + 54 + 52
    rd = ImageDraw.Draw(img)
    rd.line([(cx - 180, rule_y), (cx + 180, rule_y)], fill=ACCENT, width=2)

    # Title
    img = draw_tracked(img, cx, int(SIZE * 0.155), "RESONANCE",
                       font(ATK_BOLD, 168), 14, INK, glow=8)

    # Tagline
    img = draw_tracked(img, cx, int(SIZE * 0.155) + 195,
                       "Some minds were not born. They were tuned.",
                       font(ATK_ITAL, 40), 1, ACCENT)

    # Author + press
    img = draw_tracked(img, cx, int(SIZE * 0.88), "ANDRIES J. GREYLING",
                       font(ATK_REG, 56), 9, INK)
    img = draw_tracked(img, cx, int(SIZE * 0.925), "ARJUNA BADGER PRESS",
                       font(ATK_REG, 30), 8, ACCENT, shadow=False)

    out = img.convert("RGB")

    # AR: JPG, RGB, exactly 2400×2400, < 5 MB, alphanumeric filename
    OUT_JPG.parent.mkdir(parents=True, exist_ok=True)
    quality = 90
    out.save(OUT_JPG, "JPEG", quality=quality, subsampling=0, dpi=(72, 72))
    while OUT_JPG.stat().st_size > 5 * 1024 * 1024 and quality > 70:
        quality -= 3
        out.save(OUT_JPG, "JPEG", quality=quality, subsampling=0, dpi=(72, 72))

    out.save(OUT_PNG, "PNG")

    OUT_UPLOAD.parent.mkdir(parents=True, exist_ok=True)
    out.save(OUT_UPLOAD, "JPEG", quality=quality, subsampling=0, dpi=(72, 72))

    print(f"wrote {OUT_JPG}  ({OUT_JPG.stat().st_size / 1024:.0f} KB, q={quality})")
    print(f"wrote {OUT_PNG}")
    print(f"wrote {OUT_UPLOAD}")
    return OUT_JPG


if __name__ == "__main__":
    path = typeset()
    # Verify
    im = Image.open(path)
    print(f"verify: {im.size[0]}x{im.size[1]} {im.mode} {path.name}")
    if im.size != (SIZE, SIZE) or im.mode != "RGB":
        sys.exit("cover failed AR geometry check")

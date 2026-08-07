#!/usr/bin/env python3
"""The African Gold Trilogy — Atkinson lockup on cinematic cover plates.

Expects text-free art at books/<id>/design/cover-plate.png (preferred) or art.png.
Writes design/cover.{png,jpg}, build/export/cover.{png,jpg}, covers/<id>.jpg.

    python3 design/typeset_trilogy_covers.py            # all three
    python3 design/typeset_trilogy_covers.py relic      # one book
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

REPO = Path(__file__).resolve().parent.parent
_ATK = REPO / "assets" / "fonts"
ATK_REG = str(_ATK / "AtkinsonHyperlegible-Regular.otf")
ATK_BOLD = str(_ATK / "AtkinsonHyperlegible-Bold.otf")
ATK_ITAL = str(_ATK / "AtkinsonHyperlegible-Italic.otf")

W, H = 1800, 2700
SHADOW = (8, 6, 4, 235)

BOOKS = {
    "resonance": {
        "numeral": "BOOK ONE",
        "title": "RESONANCE",
        "tagline": "Some minds were not born. They were tuned.",
        "ink": (245, 220, 158, 255),       # honey gold
        "accent": (229, 181, 103, 255),    # ochre
    },
    "revelation": {
        "numeral": "BOOK TWO",
        "title": "REVELATION",
        "tagline": "Every sacred text was edited. She found the edits.",
        "ink": (248, 210, 170, 255),       # warm bone-gold
        "accent": (232, 120, 72, 255),     # forge ember
    },
    "relic": {
        "numeral": "BOOK THREE",
        "title": "RELIC",
        "tagline": "The gold was never the treasure. It was the key.",
        "ink": (252, 230, 170, 255),       # molten bright
        "accent": (240, 196, 96, 255),     # full gold
    },
}


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


def fit_plate(plate: Image.Image) -> Image.Image:
    art = ImageOps.exif_transpose(plate).convert("RGB")
    aw, ah = art.size
    scale = max(W / aw, H / ah)
    nw, nh = int(aw * scale + 0.5), int(ah * scale + 0.5)
    art = art.resize((nw, nh), Image.Resampling.LANCZOS)
    x0 = (nw - W) // 2
    y0 = (nh - H) // 2
    return art.crop((x0, y0, x0 + W, y0 + H))


def find_plate(bid: str) -> Path | None:
    d = REPO / "books" / bid / "design"
    for name in ("cover-plate.png", "cover-plate.jpg", "art.png", "art.jpg"):
        p = d / name
        if p.is_file():
            return p
    return None


def typeset(bid: str) -> None:
    meta = BOOKS[bid]
    plate = find_plate(bid)
    if plate is None:
        print(f"  skip {bid}: no cover-plate.png / art.png")
        return

    img = fit_plate(Image.open(plate)).convert("RGBA")
    cx = W / 2
    ink = meta["ink"]
    accent = meta["accent"]

    # Soft scrims so gold type reads on bright mid-frames.
    scrim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrim)
    top_end = int(H * 0.34)
    for y in range(top_end):
        a = int(165 * (1 - y / top_end) ** 1.25)
        sd.line([(0, y), (W, y)], fill=(6, 5, 4, a))
    bot_start = int(H * 0.82)
    for y in range(bot_start, H):
        a = int(175 * ((y - bot_start) / (H - bot_start)) ** 1.2)
        sd.line([(0, y), (W, y)], fill=(6, 5, 4, a))
    img = Image.alpha_composite(img, scrim)

    # Series eyebrow + numeral
    img = draw_tracked(img, cx, int(H * 0.048), "THE AFRICAN GOLD TRILOGY",
                       font(ATK_REG, 36), 10, accent)
    img = draw_tracked(img, cx, int(H * 0.048) + 48, meta["numeral"],
                       font(ATK_REG, 32), 12, ink)

    rule_y = int(H * 0.048) + 48 + 50
    rd = ImageDraw.Draw(img)
    rd.line([(cx - 160, rule_y), (cx + 160, rule_y)], fill=accent, width=2)

    # Title
    title = meta["title"]
    f_title = font(ATK_BOLD, 150 if len(title) <= 10 else 128)
    track = 14 if len(title) <= 10 else 8
    img = draw_tracked(img, cx, int(H * 0.14), title, f_title, track, ink, glow=7)

    # Tagline
    f_tag = font(ATK_ITAL, 38)
    img = draw_tracked(img, cx, int(H * 0.14) + 175, meta["tagline"], f_tag, 1, accent)

    # Author
    img = draw_tracked(img, cx, int(H * 0.915), "ANDRIES J. GREYLING",
                       font(ATK_REG, 52), 9, ink)
    img = draw_tracked(img, cx, int(H * 0.955), "ARJUNA BADGER PRESS",
                       font(ATK_REG, 28), 8, accent, shadow=False)

    out = img.convert("RGB")
    design = REPO / "books" / bid / "design"
    export = REPO / "books" / bid / "build" / "export"
    thumbs = REPO / "covers"
    export.mkdir(parents=True, exist_ok=True)
    thumbs.mkdir(parents=True, exist_ok=True)

    for p in (design / "cover.png", export / "cover.png"):
        out.save(p, "PNG")
        print(f"wrote {p}  ({p.stat().st_size // 1024} KB)")
    for p in (design / "cover.jpg", export / "cover.jpg"):
        out.save(p, "JPEG", quality=93, subsampling=0)
        print(f"wrote {p}")

    thumb = out.resize((240, 360), Image.Resampling.LANCZOS)
    thumb.save(thumbs / f"{bid}.jpg", "JPEG", quality=88)
    print(f"wrote {thumbs / f'{bid}.jpg'}")


def main() -> None:
    wanted = sys.argv[1:] or list(BOOKS)
    for bid in wanted:
        if bid not in BOOKS:
            raise SystemExit(f"unknown book {bid!r}; choose from {', '.join(BOOKS)}")
        print(f"==== {bid} ====")
        typeset(bid)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Typeset title + author onto Not a Potato cinematic plates (Atkinson Hyperlegible).

Art-only plates live in covers/not-a-potato-ai/<id>.jpg. This script fits each to
1800×2700, adds legibility scrims, lays house Atkinson type, and writes:

  books/<path>/design/cover-plate.png   (fitted art, no type — re-runnable source)
  books/<path>/design/cover.{png,jpg}
  books/<path>/build/export/cover.png

    python3 design/typeset_notapotato_covers.py
    python3 design/typeset_notapotato_covers.py crop-circles voynich-manuscript
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

REPO = Path(__file__).resolve().parent.parent
PLATES = REPO / "covers" / "not-a-potato-ai"
ATK = REPO / "assets" / "fonts"
ATK_REG = str(ATK / "AtkinsonHyperlegible-Regular.otf")
ATK_BOLD = str(ATK / "AtkinsonHyperlegible-Bold.otf")
ATK_ITAL = str(ATK / "AtkinsonHyperlegible-Italic.otf")

W, H = 1800, 2700
INK = (247, 239, 225, 255)
SHADOW = (8, 5, 3, 240)
AUTHOR = "ANDRIES J. GREYLING"
EYEBROW = "NOT A POTATO"

# id → (design root relative to books/, title lines for cover lockup)
BOOKS: list[tuple[str, str, list[str]]] = [
    ("crop-circles", "history-before-time/books/crop-circles", ["THE FIELD", "OF DOORS"]),
    ("gobekli-tepe", "gobekli-tepe", ["THE BELLY", "HILL"]),
    ("voynich-manuscript", "voynich-manuscript", ["THE HAND", "THAT WROTE IT"]),
    ("suppressed-tech", "suppressed-tech", ["THE QUIET", "MEN"]),
    ("anunnaki-mesopotamia", "anunnaki-mesopotamia", ["THE PRINCELY", "OFFSPRING"]),
    ("nazca-lines", "nazca-lines", ["FROM THE", "AIR"]),
    ("atacama-paracas", "atacama-paracas", ["AIMED AT", "THE SEA"]),
    ("nan-madol", "nan-madol", ["THE SPACES", "BETWEEN"]),
    ("newark-earthworks", "newark-earthworks", ["THE", "EIGHTEEN-YEAR", "ALMANAC"]),
    ("serpent-mound", "serpent-mound", ["THE SERPENT'S", "AGE"]),
    ("poverty-point", "poverty-point", ["NINETY", "DAYS"]),
    ("puma-punku", "puma-punku", ["THE UNKNOWN", "CORNER"]),
    ("sajama-lines", "sajama-lines", ["THE LONG", "STRAIGHT"]),
    ("uffington", "uffington", ["THE", "SCOURING"]),
    ("yonaguni", "yonaguni", ["MADE OR", "NOT"]),
]


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def text_width(draw, s, fnt, tracking):
    w = 0
    for ch in s:
        w += draw.textlength(ch, font=fnt) + tracking
    return w - tracking if s else 0


def _place_glyphs(d, cx, y, s, fnt, tracking, fill, dx=0, dy=0):
    total = text_width(d, s, fnt, tracking)
    x = cx - total / 2
    for ch in s:
        d.text((x + dx, y + dy), ch, font=fnt, fill=fill)
        x += d.textlength(ch, font=fnt) + tracking


def draw_tracked(img, cx, y, s, fnt, tracking, fill, shadow=True, glow=5):
    if shadow:
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        _place_glyphs(ld, cx, y, s, fnt, tracking, SHADOW, dx=2, dy=3)
        layer = layer.filter(ImageFilter.GaussianBlur(glow))
        img = Image.alpha_composite(img, layer)
        img = Image.alpha_composite(img, layer)
    top = Image.new("RGBA", img.size, (0, 0, 0, 0))
    td = ImageDraw.Draw(top)
    _place_glyphs(td, cx, y, s, fnt, tracking, fill)
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


def title_size(n_lines: int) -> int:
    if n_lines >= 3:
        return 96
    if n_lines == 2:
        return 118
    return 148


def compose(plate_path: Path, title_lines: list[str]) -> tuple[Image.Image, Image.Image]:
    fitted = fit_plate(Image.open(plate_path))
    img = fitted.convert("RGBA")
    cx = W / 2

    scrim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrim)
    top_end = int(H * 0.38)
    for y in range(top_end):
        a = int(200 * (1 - y / top_end) ** 1.25)
        sd.line([(0, y), (W, y)], fill=(8, 6, 4, a))
    bot_start = int(H * 0.78)
    for y in range(bot_start, H):
        a = int(210 * ((y - bot_start) / (H - bot_start)) ** 1.15)
        sd.line([(0, y), (W, y)], fill=(10, 7, 4, a))
    img = Image.alpha_composite(img, scrim)

    f_eyebrow = font(ATK_REG, 38)
    img = draw_tracked(img, cx, int(H * 0.048), EYEBROW, f_eyebrow, 10, INK)
    rd = ImageDraw.Draw(img)
    rd.line([(cx - 160, int(H * 0.048) + 54), (cx + 160, int(H * 0.048) + 54)], fill=INK, width=2)

    size = title_size(len(title_lines))
    f_title = font(ATK_BOLD, size)
    tracking = 4 if size >= 110 else 2
    line_gap = int(size * 1.12)
    ty = int(H * 0.095)
    for i, line in enumerate(title_lines):
        img = draw_tracked(img, cx, ty + i * line_gap, line, f_title, tracking, INK)

    f_auth = font(ATK_REG, 52)
    img = draw_tracked(img, cx, int(H * 0.925), AUTHOR, f_auth, 8, INK)
    return img.convert("RGB"), fitted


def process(book_id: str, rootrel: str, title_lines: list[str]) -> None:
    src = PLATES / f"{book_id}.jpg"
    if not src.is_file():
        raise SystemExit(f"missing plate: {src}")
    for f in (ATK_REG, ATK_BOLD, ATK_ITAL):
        if not Path(f).is_file():
            raise SystemExit(f"missing Atkinson font: {f}")

    root = REPO / "books" / rootrel
    design = root / "design"
    export = root / "build" / "export"
    design.mkdir(parents=True, exist_ok=True)
    export.mkdir(parents=True, exist_ok=True)

    out, fitted = compose(src, title_lines)
    plate_out = design / "cover-plate.png"
    fitted.save(plate_out, "PNG")
    for dest in (design / "cover.png", export / "cover.png"):
        out.save(dest, "PNG")
    out.save(design / "cover.jpg", "JPEG", quality=92)
    kb = (design / "cover.png").stat().st_size // 1024
    print(f"  [ok] {book_id}: {' / '.join(title_lines)} → {design / 'cover.png'} ({kb} KB)")


def main() -> None:
    want = set(sys.argv[1:])
    for book_id, rootrel, title_lines in BOOKS:
        if want and book_id not in want:
            continue
        process(book_id, rootrel, title_lines)


if __name__ == "__main__":
    main()

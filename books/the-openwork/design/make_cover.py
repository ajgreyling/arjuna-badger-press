#!/usr/bin/env python3
"""Lay the title + author typography onto the clean cover plate for *Lacework*.

Reads design/cover-plate.png (the lace/table plate — text-free), adds soft legibility scrims
and house serif typography, and writes the typeset cover to design/cover.{png,jpg} +
build/export/cover.{png,jpg}. Same house method as *The Dreaming*.

Faithful Modern shelf (no series number): eyebrow = "FAITHFUL MODERN · AFTER SHIRLEY CONRAN";
aged-ivory ink with oxblood-wine and winelands-gold accents to sit with the plate's palette.

    python3 design/make_cover.py
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
BOOK = HERE.parent
PLATE = HERE / "cover-plate.png"
OUT = [


    HERE / "cover.png",
    HERE / "cover.jpg",
    BOOK / "build" / "export" / "cover.png",
    BOOK / "build" / "export" / "cover.jpg",
]

INK = (242, 234, 218, 255)        # aged ivory / antique lace title ink
ACCENT = (196, 154, 74, 255)      # winelands gold for eyebrow + rule
WINE = (146, 46, 52, 255)         # oxblood for the tagline
SHADOW = (28, 12, 14, 215)


def _repo() -> Path:
    p = Path(__file__).resolve()
    for cand in p.parents:
        if (cand / "assets" / "fonts" / "AtkinsonHyperlegible-Bold.otf").is_file():
            return cand
    raise SystemExit("make_cover: cannot find repo assets/fonts/AtkinsonHyperlegible-*.otf")


_REPO = _repo()
_ATK = _REPO / "assets" / "fonts"
ATK_REG = str(_ATK / "AtkinsonHyperlegible-Regular.otf")
ATK_BOLD = str(_ATK / "AtkinsonHyperlegible-Bold.otf")
ATK_ITAL = str(_ATK / "AtkinsonHyperlegible-Italic.otf")
ATK_BI = str(_ATK / "AtkinsonHyperlegible-BoldItalic.otf")

DIDOT = ATK_BOLD
COCHIN = ATK_REG
COPPER = ATK_REG
def font(path: str, size: int, index: int = 0) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size, index=index)


def text_width(draw, s, fnt, tracking):
    w = 0
    for ch in s:
        w += draw.textlength(ch, font=fnt) + tracking
    return w - tracking if s else 0


def draw_tracked(draw, cx, y, s, fnt, tracking, fill, shadow=True):
    total = text_width(draw, s, fnt, tracking)
    x = cx - total / 2
    for ch in s:
        if shadow:
            draw.text((x + 2, y + 3), ch, font=fnt, fill=SHADOW)
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking


def main() -> None:
    img = Image.open(PLATE).convert("RGBA")
    W, H = img.size
    cx = W / 2

    # Legibility scrims — darken the top (eyebrow + title) and the very bottom (author).
    scrim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrim)
    top_end = int(H * 0.42)
    for y in range(top_end):
        a = int(170 * (1 - y / top_end) ** 1.4)
        sd.line([(0, y), (W, y)], fill=(30, 14, 16, a))
    bot_start = int(H * 0.85)
    for y in range(bot_start, H):
        a = int(150 * ((y - bot_start) / (H - bot_start)) ** 1.3)
        sd.line([(0, y), (W, y)], fill=(26, 12, 14, a))
    img = Image.alpha_composite(img, scrim)

    draw = ImageDraw.Draw(img)

    # Eyebrow — the imprint + the homage, no series number.
    f_eyebrow = font(COPPER, 22)
    draw_tracked(draw, cx, int(H * 0.055), "FAITHFUL MODERN · AFTER SHIRLEY CONRAN", f_eyebrow, 6, ACCENT)

    rule_y = int(H * 0.055) + 44
    rw = 150
    draw.line([(cx - rw, rule_y), (cx + rw, rule_y)], fill=ACCENT, width=2)

    # Title.
    f_title = font(DIDOT, 138)
    lines = ["LACEWORK"]
    ty = int(H * 0.19)
    lh = 150
    for i, ln in enumerate(lines):
        draw_tracked(draw, cx, ty + i * lh, ln, f_title, 5, INK)

    # Tagline — the book's line, in oxblood italic.
    f_tag = font(ATK_ITAL, 38)
    draw_tracked(draw, cx, ty + lh + 16, "the pattern is made of what is missing", f_tag, 1, WINE)

    # Author.
    f_auth = font(COCHIN, 46)
    draw_tracked(draw, cx, int(H * 0.93), "ANDRIES J. GREYLING", f_auth, 7, INK)

    out = img.convert("RGB")
    for p in OUT:
        p.parent.mkdir(parents=True, exist_ok=True)
        if p.suffix.lower() == ".jpg":
            out.save(p, "JPEG", quality=92)
        else:
            out.save(p, "PNG")
        print(f"wrote {p}")


if __name__ == "__main__":
    main()

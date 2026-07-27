#!/usr/bin/env python3
"""Lay the title + author typography onto the clean cover plate for *Verdigris*.

Reads design/cover-plate.png (the verdigris-throat plate — text-free), adds soft legibility
scrims and house serif typography, and writes the typeset cover to design/cover.{png,jpg} +
build/export/cover.{png,jpg}. Same house method as *The Dreaming*.

Standalone (no series number): eyebrow = "A STANDALONE NOVEL"; patina-green/copper ink to sit
with the plate's verdigris palette.

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

INK = (231, 238, 230, 255)        # cool bone-green title ink
ACCENT = (188, 122, 74, 255)      # oxidised copper-orange for eyebrow + tagline
SHADOW = (6, 16, 14, 215)

DIDOT = "/System/Library/Fonts/Supplemental/Didot.ttc"
COCHIN = "/System/Library/Fonts/Supplemental/Cochin.ttc"
COPPER = "/System/Library/Fonts/Supplemental/Copperplate.ttc"


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
        sd.line([(0, y), (W, y)], fill=(8, 20, 18, a))
    bot_start = int(H * 0.85)
    for y in range(bot_start, H):
        a = int(150 * ((y - bot_start) / (H - bot_start)) ** 1.3)
        sd.line([(0, y), (W, y)], fill=(6, 16, 14, a))
    img = Image.alpha_composite(img, scrim)

    draw = ImageDraw.Draw(img)

    # Eyebrow — standalone, no series number.
    f_eyebrow = font(COPPER, 30)
    draw_tracked(draw, cx, int(H * 0.055), "A STANDALONE NOVEL", f_eyebrow, 8, ACCENT)

    rule_y = int(H * 0.055) + 48
    rw = 150
    draw.line([(cx - rw, rule_y), (cx + rw, rule_y)], fill=ACCENT, width=2)

    # Title.
    f_title = font(DIDOT, 118)
    lines = ["VERDIGRIS"]
    ty = int(H * 0.135)
    lh = 150
    for i, ln in enumerate(lines):
        draw_tracked(draw, cx, ty + i * lh, ln, f_title, 5, INK)

    # Tagline — the book's line, in copper italic.
    f_tag = font(DIDOT, 38, index=1)
    draw_tracked(draw, cx, ty + len(lines) * lh + 16,
                 "the same green is the cure and the rot", f_tag, 1, ACCENT)

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

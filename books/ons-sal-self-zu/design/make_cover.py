#!/usr/bin/env python3
"""Cover for *Ons Sal Self* (isiZulu) — house colophon treatment (no commissioned art).

    python3 books/ons-sal-self-zu/design/make_cover.py
"""
from __future__ import annotations
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
MARK = REPO / "brand" / "assets" / "badger-bow-imprint.png"
FONTS = REPO / "assets" / "fonts"
OUT = HERE / "cover.png"

W, H = 1600, 2400
INK = (3, 3, 3)
GOLD = (200, 168, 107)
GOLD_DIM = (176, 122, 60)
IVORY = (237, 233, 224)
MUTED = (138, 130, 118)

TITLE = "Ons Sal\nSelf"
SUB = "Indaba ekhulunywayo · isiZulu"
FOOT = "ARJUNA BADGER PRESS"


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONTS / name), size)


def centre(d: ImageDraw.ImageDraw, y: int, text: str, f, fill, tracking: int = 0) -> int:
    if tracking:
        widths = [d.textlength(c, font=f) for c in text]
        total = sum(widths) + tracking * (len(text) - 1)
        x = (W - total) / 2
        for c, cw in zip(text, widths):
            d.text((x, y), c, font=f, fill=fill)
            x += cw + tracking
        return y + f.size
    box = d.textbbox((0, 0), text, font=f)
    d.text(((W - (box[2] - box[0])) / 2 - box[0], y), text, font=f, fill=fill)
    return y + (box[3] - box[1])


def main() -> None:
    canvas = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(canvas)
    d.rectangle([64, 64, W - 65, H - 65], outline=(28, 24, 19), width=3)

    mark = Image.open(MARK).convert("RGBA")
    mw = 1180
    mark = mark.resize((mw, mw), Image.LANCZOS)
    canvas.paste(mark, ((W - mw) // 2, 250), mark)

    y = 1560
    f_title = font("AtkinsonHyperlegible-Bold.otf", 132)
    for line in TITLE.split("\n"):
        y = centre(d, y, line, f_title, IVORY) + 46

    y += 34
    d.line([(W // 2 - 150, y), (W // 2 + 150, y)], fill=GOLD_DIM, width=3)
    y += 58

    y = centre(d, y, SUB, font("AtkinsonHyperlegible-Italic.otf", 42), GOLD) + 10

    centre(d, H - 190, FOOT, font("AtkinsonHyperlegible-Regular.otf", 34), MUTED, tracking=7)

    canvas.save(OUT, "PNG", optimize=True)
    print(f"  [ok] {OUT.relative_to(REPO)}  {W}x{H}")


if __name__ == "__main__":
    main()

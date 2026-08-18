#!/usr/bin/env python3
"""Cover for *The Shape of the One* — house colophon treatment.

No commissioned art: the cover carries the Arjuna Badger imprint mark (the gold
badger-and-bow device) on the mark's own ground, with the title set beneath in
Atkinson Hyperlegible, the house accessibility face.

    python3 books/law-of-one-condensed/design/make_cover.py
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
INK = (3, 3, 3)                 # sampled from the mark's own ground — no seam
GOLD = (200, 168, 107)          # #C8A86B house gold
GOLD_DIM = (176, 122, 60)       # #b07a3c deep gold
IVORY = (237, 233, 224)         # #EDE9E0
MUTED = (138, 130, 118)

TITLE = "The Shape\nof the One"
SUB = "A condensation of the Ra material"
FOOT = "ARJUNA BADGER PRESS"


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONTS / name), size)


def centre(d: ImageDraw.ImageDraw, y: int, text: str, f, fill, tracking: int = 0) -> int:
    """Draw horizontally-centred text (optionally letterspaced); return the y below it."""
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

    # hairline rule inset — a plate edge, not a border
    d.rectangle([64, 64, W - 65, H - 65], outline=(28, 24, 19), width=3)

    # the colophon, centred, upper field
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

    y = centre(d, y, SUB, font("AtkinsonHyperlegible-Italic.otf", 52), GOLD) + 10

    centre(d, H - 190, FOOT, font("AtkinsonHyperlegible-Regular.otf", 34), MUTED, tracking=7)

    canvas.save(OUT, "PNG", optimize=True)
    print(f"  [ok] {OUT.relative_to(REPO)}  {W}x{H}")


if __name__ == "__main__":
    main()

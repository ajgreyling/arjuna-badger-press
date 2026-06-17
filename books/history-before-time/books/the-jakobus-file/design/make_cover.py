#!/usr/bin/env python3
"""Lay the title + author typography onto the clean cover plate for *A Man They All Read Wrong*.

Reads design/cover-plate.png (the rich bush/safari composite — text-free), adds soft legibility
scrims and HBT serif typography, and writes the typeset cover to design/cover.{png,jpg} +
build/export/cover.{png,jpg}. Same house method as *The Silver Thread* / *The Long Dark*.

    python3 design/make_cover.py
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
BOOK = HERE.parent
PLATE = HERE / "cover-plate.png"
OUT = [
    HERE / "cover.png",
    HERE / "cover.jpg",
    BOOK / "build" / "export" / "cover.png",
    BOOK / "build" / "export" / "cover.jpg",
]

INK = (244, 234, 217, 255)
SHADOW = (20, 12, 6, 200)

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

    scrim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrim)
    top_end = int(H * 0.42)
    for y in range(top_end):
        a = int(175 * (1 - y / top_end) ** 1.4)
        sd.line([(0, y), (W, y)], fill=(28, 18, 10, a))
    bot_start = int(H * 0.84)
    for y in range(bot_start, H):
        a = int(155 * ((y - bot_start) / (H - bot_start)) ** 1.3)
        sd.line([(0, y), (W, y)], fill=(22, 13, 7, a))
    img = Image.alpha_composite(img, scrim)

    draw = ImageDraw.Draw(img)

    f_series = font(COCHIN, 33)
    draw_tracked(draw, cx, int(H * 0.048), "HISTORY BEFORE TIME", f_series, 9, INK)

    f_file = font(COPPER, 28)
    draw_tracked(draw, cx, int(H * 0.082), "THE JAKOBUS SWART FILE", f_file, 6, INK)

    rule_y = int(H * 0.082) + 46
    rw = 150
    draw.line([(cx - rw, rule_y), (cx + rw, rule_y)], fill=INK, width=2)

    f_title = font(DIDOT, 118)
    lines = ["A MAN", "THEY ALL", "READ WRONG"]
    ty = int(H * 0.118)
    lh = 128
    for i, ln in enumerate(lines):
        draw_tracked(draw, cx, ty + i * lh, ln, f_title, 4, INK)

    # Subtitle crosses the bright sunset glow behind the figure on this plate, so lay a soft
    # local scrim band under it for legibility before drawing the italic.
    f_sub = font(DIDOT, 36, index=1)
    sub = "assembled, after his death"
    sub_y = ty + 3 * lh + 10
    sub_w = text_width(draw, sub, f_sub, 1)
    band = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(band)
    pad_x, pad_y = 60, 14
    bd.rounded_rectangle(
        [cx - sub_w / 2 - pad_x, sub_y - pad_y, cx + sub_w / 2 + pad_x, sub_y + 48 + pad_y],
        radius=26, fill=(18, 11, 6, 120),
    )
    band = band.filter(ImageFilter.GaussianBlur(18))
    img = Image.alpha_composite(img, band)
    draw = ImageDraw.Draw(img)
    draw_tracked(draw, cx, sub_y, sub, f_sub, 1, INK)

    f_auth = font(COCHIN, 44)
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

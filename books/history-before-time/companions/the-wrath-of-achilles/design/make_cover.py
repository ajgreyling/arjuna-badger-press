#!/usr/bin/env python3
"""Lay the HBT title typography onto the cinematic cover plate for *The Wrath of Achilles*.

Reads design/cover-plate.png (the text-free warrior-before-Troy matte painting from the OpenAI
Images API), adds soft top/bottom legibility scrims and the house serif typography (Didot title /
Cochin eyebrow + author), and writes the typeset cover to design/cover.{png,jpg} + build/export/.
Same house method as The Jakobus File / The Silver Thread. Re-runnable: always works from the plate.

    python3 design/make_cover.py
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
BOOK = HERE.parent
PLATE = HERE / "cover-plate.png"
OUT = [
    HERE / "cover.png", HERE / "cover.jpg",
    BOOK / "build" / "export" / "cover.png", BOOK / "build" / "export" / "cover.jpg",
]

INK = (244, 234, 217, 255)
GOLD = (229, 181, 103, 255)
OCHRE = (200, 168, 107, 255)
DIM = (214, 200, 178, 255)
SHADOW = (16, 10, 5, 220)

DIDOT = "/System/Library/Fonts/Supplemental/Didot.ttc"
COCHIN = "/System/Library/Fonts/Supplemental/Cochin.ttc"


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

    # legibility scrims — the top band is deepened a touch more here because the title is long and
    # the plate's upper sky is already fairly dark (keeps the Didot crisp without greying the art).
    scrim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrim)
    top_end = int(H * 0.44)
    for y in range(top_end):
        a = int(195 * (1 - y / top_end) ** 1.3)
        sd.line([(0, y), (W, y)], fill=(14, 15, 22, a))
    bot_start = int(H * 0.82)
    for y in range(bot_start, H):
        a = int(175 * ((y - bot_start) / (H - bot_start)) ** 1.25)
        sd.line([(0, y), (W, y)], fill=(14, 10, 7, a))
    img = Image.alpha_composite(img, scrim)

    draw = ImageDraw.Draw(img)

    draw_tracked(draw, cx, int(H * 0.050), "HISTORY BEFORE TIME", font(COCHIN, 34), 9, INK)

    tag, f_tag = "COMPANIONS", font(COCHIN, 23)
    draw_tracked(draw, cx, int(H * 0.082), tag, f_tag, 8, OCHRE)
    tw = text_width(draw, tag, f_tag, 8)
    dy = int(H * 0.082) + 14
    for sx in (cx - tw / 2 - 30, cx + tw / 2 + 30):
        draw.ellipse([sx - 3, dy - 3, sx + 3, dy + 3], fill=OCHRE)

    rule_y = int(H * 0.112)
    draw.line([(cx - 140, rule_y), (cx + 140, rule_y)], fill=INK, width=2)

    f_title = font(DIDOT, 116)
    lines = ["THE WRATH", "OF ACHILLES"]
    ty = int(H * 0.132)
    lh = 130
    for i, ln in enumerate(lines):
        draw_tracked(draw, cx, ty + i * lh, ln, f_title, 3, INK)

    f_sub = font(DIDOT, 38, index=1)
    sub = "Homer's Iliad, plainly told"
    sub_y = ty + 2 * lh + 18
    sub_w = text_width(draw, sub, f_sub, 1)
    band = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(band)
    bd.rounded_rectangle(
        [cx - sub_w / 2 - 56, sub_y - 14, cx + sub_w / 2 + 56, sub_y + 52],
        radius=24, fill=(14, 11, 16, 110),
    )
    band = band.filter(ImageFilter.GaussianBlur(18))
    img = Image.alpha_composite(img, band)
    draw = ImageDraw.Draw(img)
    draw_tracked(draw, cx, sub_y, sub, f_sub, 1, DIM)

    draw_tracked(draw, cx, int(H * 0.93), "ANDRIES J. GREYLING", font(COCHIN, 44), 7, INK)

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

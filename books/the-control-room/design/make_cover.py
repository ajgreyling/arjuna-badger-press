#!/usr/bin/env python3
"""Lay title + author typography onto the clean cover plate for *The Control Room*.

    python3 books/the-control-room/design/make_cover.py
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

HERE = Path(__file__).resolve().parent
BOOK = HERE.parent
PLATE = HERE / "cover-plate.png"
OUT_PNG = [HERE / "cover.png", BOOK / "build" / "export" / "cover.png"]
OUT_JPG = HERE / "cover.jpg"

W, H = 1800, 2700
INK = (245, 228, 180, 255)        # warm gold, matches the neural glow
SHADOW = (6, 4, 2, 240)
DIDOT = "/System/Library/Fonts/Supplemental/Didot.ttc"
COCHIN = "/System/Library/Fonts/Supplemental/Cochin.ttc"


def font(path: str, size: int, index: int = 0) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size, index=index)


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


def main() -> None:
    if not PLATE.is_file():
        raise SystemExit(f"missing plate: {PLATE}")

    img = fit_plate(Image.open(PLATE)).convert("RGBA")
    cx = W / 2

    # Room is already dark; light top deepen so gold type punches.
    scrim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrim)
    top_end = int(H * 0.30)
    for y in range(top_end):
        a = int(150 * (1 - y / top_end) ** 1.2)
        sd.line([(0, y), (W, y)], fill=(4, 6, 12, a))
    bot_start = int(H * 0.82)
    for y in range(bot_start, H):
        a = int(180 * ((y - bot_start) / (H - bot_start)) ** 1.15)
        sd.line([(0, y), (W, y)], fill=(4, 6, 12, a))
    img = Image.alpha_composite(img, scrim)

    f_eyebrow = font(COCHIN, 40)
    img = draw_tracked(img, cx, int(H * 0.052), "A RESONANCE NOVELLA", f_eyebrow, 10, INK)

    rule_y = int(H * 0.052) + 58
    rd = ImageDraw.Draw(img)
    rd.line([(cx - 150, rule_y), (cx + 150, rule_y)], fill=INK, width=2)

    ty = int(H * 0.095)
    f_the = font(DIDOT, 96)
    f_title = font(DIDOT, 148)
    img = draw_tracked(img, cx, ty, "THE", f_the, 14, INK)
    img = draw_tracked(img, cx, ty + 115, "CONTROL", f_title, 10, INK)
    img = draw_tracked(img, cx, ty + 115 + 165, "ROOM", f_title, 16, INK)

    sub_y = ty + 115 + 165 + 175
    f_sub = font(DIDOT, 40, index=1)
    img = draw_tracked(img, cx, sub_y, "seven operators · one body", f_sub, 1, INK)

    f_auth = font(COCHIN, 56)
    img = draw_tracked(img, cx, int(H * 0.925), "ANDRIES J. GREYLING", f_auth, 9, INK)

    out = img.convert("RGB")
    for p in OUT_PNG:
        p.parent.mkdir(parents=True, exist_ok=True)
        out.save(p, "PNG")
        print(f"wrote {p}")
    out.save(OUT_JPG, "JPEG", quality=92)
    print(f"wrote {OUT_JPG}")


if __name__ == "__main__":
    main()

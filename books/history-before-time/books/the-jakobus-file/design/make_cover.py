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

INK = (247, 239, 225, 255)
SHADOW = (8, 5, 2, 235)            # near-opaque warm black, for punch over the busy plate

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


def _place_glyphs(d, cx, y, s, fnt, tracking, fill, dx=0, dy=0):
    """Letter-space string s centred on cx, drawn into draw-context d with optional offset."""
    total = text_width(d, s, fnt, tracking)
    x = cx - total / 2
    for ch in s:
        d.text((x + dx, y + dy), ch, font=fnt, fill=fill)
        x += d.textlength(ch, font=fnt) + tracking


def draw_tracked(img, cx, y, s, fnt, tracking, fill, shadow=True, glow=6):
    """Draw letter-spaced text centred on cx at baseline-top y, onto RGBA image `img`.

    A blurred dark copy is laid down first as a soft glow/shadow (so the thin Didot
    strokes hold up over the bright sunburst and busy bush), then the crisp ink on top.
    Returns the composited image.
    """
    if shadow:
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        _place_glyphs(ld, cx, y, s, fnt, tracking, SHADOW, dx=2, dy=3)
        layer = layer.filter(ImageFilter.GaussianBlur(glow))
        # darken twice so the soft halo reads as a real shadow, not a faint smudge
        img = Image.alpha_composite(img, layer)
        img = Image.alpha_composite(img, layer)
    top = Image.new("RGBA", img.size, (0, 0, 0, 0))
    td = ImageDraw.Draw(top)
    _place_glyphs(td, cx, y, s, fnt, tracking, fill)
    return Image.alpha_composite(img, top)


def main() -> None:
    img = Image.open(PLATE).convert("RGBA")
    W, H = img.size
    cx = W / 2

    # Stronger, deeper top scrim: the title stack sits over the brightest part of this
    # plate (the sunburst), so it needs firm darkening to carry the larger type.
    scrim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrim)
    top_end = int(H * 0.56)
    for y in range(top_end):
        a = int(215 * (1 - y / top_end) ** 1.25)
        sd.line([(0, y), (W, y)], fill=(26, 16, 9, a))
    bot_start = int(H * 0.82)
    for y in range(bot_start, H):
        a = int(200 * ((y - bot_start) / (H - bot_start)) ** 1.25)
        sd.line([(0, y), (W, y)], fill=(20, 12, 6, a))
    img = Image.alpha_composite(img, scrim)

    f_series = font(COCHIN, 42)
    img = draw_tracked(img, cx, int(H * 0.046), "HISTORY BEFORE TIME", f_series, 11, INK)

    f_file = font(COPPER, 35)
    img = draw_tracked(img, cx, int(H * 0.080), "THE JAKOBUS SWART FILE", f_file, 7, INK)

    rule_y = int(H * 0.080) + 58
    rw = 185
    rd = ImageDraw.Draw(img)
    rd.line([(cx - rw, rule_y), (cx + rw, rule_y)], fill=INK, width=3)

    f_title = font(DIDOT, 158)
    lines = ["A MAN", "THEY ALL", "READ WRONG"]
    ty = int(H * 0.120)
    lh = 172
    for i, ln in enumerate(lines):
        img = draw_tracked(img, cx, ty + i * lh, ln, f_title, 4, INK)

    # Subtitle crosses the bright sunset glow behind the figure on this plate, so lay a soft
    # local scrim band under it for legibility before drawing the italic.
    f_sub = font(DIDOT, 48, index=1)
    sub = "assembled, after his death"
    sub_y = ty + 3 * lh + 16
    sub_w = text_width(ImageDraw.Draw(img), sub, f_sub, 1)
    band = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(band)
    pad_x, pad_y = 76, 18
    bd.rounded_rectangle(
        [cx - sub_w / 2 - pad_x, sub_y - pad_y, cx + sub_w / 2 + pad_x, sub_y + 62 + pad_y],
        radius=32, fill=(16, 10, 5, 140),
    )
    band = band.filter(ImageFilter.GaussianBlur(22))
    img = Image.alpha_composite(img, band)
    img = draw_tracked(img, cx, sub_y, sub, f_sub, 1, INK)

    f_auth = font(COCHIN, 58)
    img = draw_tracked(img, cx, int(H * 0.925), "ANDRIES J. GREYLING", f_auth, 8, INK)

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

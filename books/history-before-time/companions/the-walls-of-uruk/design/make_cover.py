#!/usr/bin/env python3
"""Compose the typographic cover for *The Walls of Uruk*.

No cinematic plate yet — a designed atmosphere cover in the house manner for an open-draft
companion. A deep clay-and-dusk field carries a quiet figure: stacked courses of brick (the walls
the poem opens and closes on), with the house Didot/Cochin title above.

Re-runnable: always works from nothing but fonts. Writes design/cover.{png,jpg} + build/export/.

    python3 design/make_cover.py
"""
from __future__ import annotations

import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
BOOK = HERE.parent
OUT = [
    HERE / "cover.png", HERE / "cover.jpg",
    BOOK / "build" / "export" / "cover.png", BOOK / "build" / "export" / "cover.jpg",
]

W, H = 1600, 2400

INK = (240, 233, 220, 255)
GOLD = (229, 181, 103, 255)
OCHRE = (200, 168, 107, 255)
DIM = (196, 184, 162, 255)
FAINT = (150, 140, 124, 255)
SHADOW = (10, 8, 6, 220)
BRICK = (168, 110, 72, 255)
MORTAR = (92, 70, 52, 255)


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

DIDOT = ATK_BOLD
COCHIN = ATK_REG


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


def vertical_gradient(top, bot):
    g = Image.new("RGB", (W, H))
    px = g.load()
    for y in range(H):
        t = (y / H) ** 1.15
        r = int(top[0] + (bot[0] - top[0]) * t)
        gg = int(top[1] + (bot[1] - top[1]) * t)
        b = int(top[2] + (bot[2] - top[2]) * t)
        for x in range(W):
            px[x, y] = (r, gg, b)
    return g


def add_grain(img, amount=8):
    random.seed(2100)
    noise = Image.new("L", (W, H))
    np = noise.load()
    for y in range(H):
        for x in range(W):
            np[x, y] = 128 + random.randint(-amount, amount)
    noise = noise.filter(ImageFilter.GaussianBlur(0.45))
    grain = Image.merge("RGB", (noise, noise, noise))
    return Image.blend(img, grain, 0.05)


def draw_walls(draw, cx, top_y, span_w, span_h):
    """Quiet stacked brick courses — the poem's first and last image."""
    courses = 7
    brick_h = span_h / courses
    left = cx - span_w / 2
    for c in range(courses):
        y0 = top_y + c * brick_h
        y1 = y0 + brick_h * 0.82
        offset = (c % 2) * (span_w / 14)
        n = 6
        bw = span_w / n
        for i in range(n + 1):
            x0 = left + offset + i * bw
            x1 = min(left + span_w, x0 + bw * 0.88)
            if x0 >= left + span_w:
                break
            if x1 <= left:
                continue
            x0 = max(left, x0)
            draw.rounded_rectangle(
                [x0, y0, x1, y1],
                radius=6,
                outline=BRICK,
                width=3,
            )
        # mortar line
        draw.line([(left, y1 + 4), (left + span_w, y1 + 4)], fill=MORTAR, width=2)


def main() -> None:
    img = vertical_gradient((22, 18, 16), (48, 32, 22)).convert("RGBA")

    scrim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrim)
    top_end = int(H * 0.42)
    for y in range(top_end):
        a = int(155 * (1 - y / top_end) ** 1.35)
        sd.line([(0, y), (W, y)], fill=(12, 10, 8, a))
    img = Image.alpha_composite(img, scrim)

    draw = ImageDraw.Draw(img)
    cx = W / 2

    draw_tracked(draw, cx, int(H * 0.058), "HISTORY BEFORE TIME", font(COCHIN, 50), 13, INK)
    tag, f_tag = "COMPANIONS", font(COCHIN, 34)
    draw_tracked(draw, cx, int(H * 0.094), tag, f_tag, 11, OCHRE)
    tw = text_width(draw, tag, f_tag, 11)
    dy = int(H * 0.094) + 22
    for sx in (cx - tw / 2 - 44, cx + tw / 2 + 44):
        draw.ellipse([sx - 4, dy - 4, sx + 4, dy + 4], fill=OCHRE)

    rule_y = int(H * 0.128)
    draw.line([(cx - 210, rule_y), (cx + 210, rule_y)], fill=INK, width=3)

    f_title = font(DIDOT, 168)
    lines = ["THE", "WALLS", "OF URUK"]
    ty = int(H * 0.152)
    lh = 184
    for i, ln in enumerate(lines):
        sz = 168 if ln != "OF URUK" else 150
        draw_tracked(draw, cx, ty + i * lh, ln, font(DIDOT, sz), 4, INK)

    f_sub = font(ATK_ITAL, 48)
    sub = "The Epic of Gilgamesh, plainly told"
    sub_y = ty + 3 * lh + 24
    sub_w = text_width(draw, sub, f_sub, 1)
    band = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(band)
    bd.rounded_rectangle(
        [cx - sub_w / 2 - 70, sub_y - 18, cx + sub_w / 2 + 70, sub_y + 70],
        radius=30, fill=(18, 12, 10, 130),
    )
    band = band.filter(ImageFilter.GaussianBlur(22))
    img = Image.alpha_composite(img, band)
    draw = ImageDraw.Draw(img)
    draw_tracked(draw, cx, sub_y, sub, f_sub, 1, DIM)

    fig_top = sub_y + 140
    draw_walls(draw, cx, fig_top, span_w=W * 0.58, span_h=H * 0.18)

    draw_tracked(
        draw, cx, fig_top + H * 0.18 + 36,
        "climb the walls · inspect the brickwork",
        font(COCHIN, 36), 4, FAINT,
    )

    draw_tracked(draw, cx, int(H * 0.92), "ANDRIES J. GREYLING", font(COCHIN, 62), 9, INK)
    draw_tracked(
        draw, cx, int(H * 0.955),
        "A GUEST-AT-THE-FIRE COMPANION · AN OPEN DRAFT",
        font(COCHIN, 27), 5, FAINT,
    )

    img = add_grain(img.convert("RGB"))

    for p in OUT:
        p.parent.mkdir(parents=True, exist_ok=True)
        if p.suffix.lower() == ".jpg":
            img.save(p, "JPEG", quality=92)
        else:
            img.save(p, "PNG")
        print(f"wrote {p}  ({p.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()

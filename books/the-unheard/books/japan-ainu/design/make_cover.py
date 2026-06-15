#!/usr/bin/env python3
"""Cover for *The Way That Was Invented* — The Unheard · Japan.

Visual language: the celebrated postcard peeling away. Indigo Hokkaido dusk, a lacquer-red
cherry-blossom veil cracking to reveal Ainu geometry and the floating stone beneath — the
hands and keels the homogenous myth buried. Procedural, deterministic (fixed seed), 6×9in @ 300dpi.

    python3 design/make_cover.py     # -> design/cover.png + design/cover.jpg

Site generator and EPUB/PDF export pick up design/cover.{png,jpg}.
"""
from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE

W, H = 1800, 2700
SEED = 20266

# The Unheard · Japan — slate-teal series accent on badger-black dusk.
SKY_TOP = (14, 20, 34)
SKY_MID = (32, 48, 62)
HORIZON = (88, 108, 118)
SNOW = (196, 204, 210)
LACQUER = (168, 42, 48)
PETAL = (220, 120, 130)
PETAL_PALE = (240, 190, 196)
STONE = (72, 78, 86)
STONE_LIT = (118, 124, 132)
AINU_INK = (176, 148, 98)
TEAL = (107, 140, 154)
GOLD = (212, 178, 108)
GOLD_BRIGHT = (238, 210, 158)
CREAM = (232, 226, 216)
INK = (196, 188, 178)

F_TITLE = "/System/Library/Fonts/Supplemental/Optima.ttc"
F_SERIES = "/System/Library/Fonts/Supplemental/Copperplate.ttc"
F_TAG_IT = "/System/Library/Fonts/Supplemental/Cochin.ttc"


def font(path: str, size: int, index: int = 0) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size, index=index)


def lerp(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def vgrad(draw, x0, y0, x1, y1, stops):
    span = max(1, y1 - y0)
    for y in range(y0, y1):
        t = (y - y0) / span
        lo, hi = stops[0], stops[-1]
        for i in range(len(stops) - 1):
            if stops[i][0] <= t <= stops[i + 1][0]:
                lo, hi = stops[i], stops[i + 1]
                break
        local = 0.0 if hi[0] == lo[0] else (t - lo[0]) / (hi[0] - lo[0])
        draw.line([(x0, y), (x1, y)], fill=lerp(lo[1], hi[1], local))


def draw_ainu_spiral(draw, cx, cy, scale, color, alpha=180):
    """Stylised Ainu morew (spiral) — geometry beneath the paint-over."""
    pts = []
    turns = 2.4
    steps = 120
    for i in range(steps):
        t = i / steps
        ang = t * turns * 2 * math.pi
        r = scale * (0.08 + 0.92 * t)
        x = cx + r * math.cos(ang)
        y = cy + r * math.sin(ang)
        pts.append((x, y))
    for i in range(len(pts) - 1):
        draw.line([pts[i], pts[i + 1]], fill=color + (alpha,), width=max(2, int(scale * 0.018)))


def draw_floating_stone(draw, cx, base_y, w, h):
    """Ishi-no-Hōden suggestion — a massive levitating block."""
    top = base_y - h
    left = cx - w // 2
    right = cx + w // 2
    shadow = lerp(STONE, (20, 22, 28), 0.65)
    draw.ellipse([cx - int(w * 0.85), base_y + 10, cx + int(w * 0.85), base_y + 70], fill=shadow)
    draw.rectangle([left, top, right, base_y], fill=STONE)
    draw.polygon([(left, top), (right, top), (right - 28, top + 36), (left + 28, top + 36)], fill=STONE_LIT)
    draw.line([(left + 18, top + 50), (left + 18, base_y - 40)], fill=lerp(STONE, (30, 32, 36), 0.5), width=4)
    draw.line([(right - 18, top + 50), (right - 18, base_y - 40)], fill=lerp(STONE, (30, 32, 36), 0.5), width=4)
    band_y = top + int(h * 0.42)
    for i in range(-8, 9):
        x = cx + i * 22
        draw.arc([x - 14, band_y - 8, x + 14, band_y + 8], 200, 340, fill=lerp(STONE_LIT, AINU_INK, 0.35), width=2)


def render_art() -> Image.Image:
    rnd = random.Random(SEED)
    img = Image.new("RGB", (W, H), SKY_TOP)
    d = ImageDraw.Draw(img)

    vgrad(d, 0, 0, W, H, [
        (0.00, SKY_TOP),
        (0.42, SKY_MID),
        (0.72, HORIZON),
        (1.00, lerp(HORIZON, SNOW, 0.55)),
    ])

    # Distant snow ridge
    ridge = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rd = ImageDraw.Draw(ridge)
    pts = [(0, int(H * 0.68))]
    for x in range(0, W + 1, 40):
        y = int(H * 0.68 + 30 * math.sin(x / 180) + rnd.randint(-8, 8))
        pts.append((x, y))
    pts += [(W, H), (0, H)]
    rd.polygon(pts, fill=SNOW + (120,))
    img = Image.alpha_composite(img.convert("RGBA"), ridge).convert("RGB")
    d = ImageDraw.Draw(img)

    # Geometry layer — what the postcard hides
    geom = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(geom)
    cx, cy = W // 2, int(H * 0.58)
    draw_ainu_spiral(gd, cx - 120, cy + 40, 140, AINU_INK, 90)
    draw_ainu_spiral(gd, cx + 130, cy + 20, 110, TEAL, 70)
    for i in range(8):
        ang = i * math.pi / 4
        x1 = cx + 200 * math.cos(ang)
        y1 = cy + 200 * math.sin(ang)
        gd.line([(cx, cy), (x1, y1)], fill=TEAL + (28,), width=1)
    geom = geom.filter(ImageFilter.GaussianBlur(1))
    img = Image.alpha_composite(img.convert("RGBA"), geom).convert("RGB")
    d = ImageDraw.Draw(img)

    # Floating stone — the keel beneath the myth
    stone_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stone_layer)
    draw_floating_stone(sd, W // 2, int(H * 0.64), 460, 300)
    stone_layer = stone_layer.filter(ImageFilter.GaussianBlur(0))
    img = Image.alpha_composite(img.convert("RGBA"), stone_layer).convert("RGB")

    # Lacquer postcard veil — glossy red wash cracking to reveal what lies beneath
    veil = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vd = ImageDraw.Draw(veil)
    vd.rectangle([int(W * 0.06), int(H * 0.36), int(W * 0.94), int(H * 0.80)], fill=LACQUER + (48,))
    # crack lines
    cracks = [
        [(int(W * 0.15), int(H * 0.42)), (int(W * 0.35), int(H * 0.55)), (int(W * 0.28), int(H * 0.72))],
        [(int(W * 0.55), int(H * 0.40)), (int(W * 0.62), int(H * 0.58)), (int(W * 0.48), int(H * 0.74))],
        [(int(W * 0.78), int(H * 0.44)), (int(W * 0.70), int(H * 0.60)), (int(W * 0.82), int(H * 0.70))],
    ]
    for crack in cracks:
        vd.line(crack, fill=(40, 12, 14, 180), width=3)
        vd.line(crack, fill=SNOW + (60,), width=1)
    veil = veil.filter(ImageFilter.GaussianBlur(2))
    img = Image.alpha_composite(img.convert("RGBA"), veil).convert("RGB")

    # Cherry petals — the beloved surface detail
    petals = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pd = ImageDraw.Draw(petals)
    for _ in range(100):
        x = rnd.randint(int(W * 0.05), int(W * 0.95))
        y = rnd.randint(int(H * 0.34), int(H * 0.78))
        rx, ry = rnd.randint(10, 22), rnd.randint(6, 14)
        rot = rnd.uniform(0, math.pi)
        col = rnd.choice([PETAL, PETAL_PALE, LACQUER])
        a = rnd.randint(40, 110)
        # simple ellipse petal
        for k in range(3):
            px = x + k * 4
            py = y + k * 2
            pd.ellipse([px - rx, py - ry, px + rx, py + ry], fill=col + (a,))
    petals = petals.filter(ImageFilter.GaussianBlur(1))
    img = Image.alpha_composite(img.convert("RGBA"), petals).convert("RGB")

    # Top vignette for title
    vig = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vd = ImageDraw.Draw(vig)
    vd.rectangle([0, 0, W, int(H * 0.34)], fill=(0, 0, 0, 110))
    vig = vig.filter(ImageFilter.GaussianBlur(100))
    img = Image.alpha_composite(img.convert("RGBA"), vig).convert("RGB")
    return img


def tracked(draw, xy, text, fnt, fill, tracking=0, center_w=None):
    widths = [draw.textbbox((0, 0), ch, font=fnt)[2] for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = xy[0] - total // 2 if center_w else xy[0]
    y = xy[1]
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + tracking


def lay_type(img: Image.Image) -> Image.Image:
    d = ImageDraw.Draw(img)
    midx = W // 2

    f_series = font(F_SERIES, 48)
    tracked(d, (midx, int(H * 0.085)), "THE UNHEARD", f_series, TEAL, tracking=12, center_w=True)
    f_series2 = font(F_SERIES, 34)
    tracked(d, (midx, int(H * 0.125)), "·  J A P A N  ·", f_series2, TEAL, tracking=8, center_w=True)

    f_the = font(F_TAG_IT, 68)
    d.text((midx, int(H * 0.178)), "The", font=f_the, fill=CREAM, anchor="mm")
    f_title = font(F_TITLE, 132)
    d.text((midx, int(H * 0.228)), "WAY THAT", font=f_title, fill=GOLD_BRIGHT, anchor="mm")
    d.text((midx, int(H * 0.278)), "WAS", font=f_title, fill=GOLD_BRIGHT, anchor="mm")
    d.text((midx, int(H * 0.328)), "INVENTED", font=f_title, fill=GOLD_BRIGHT, anchor="mm")

    rw = int(W * 0.26)
    d.line([(midx - rw, int(H * 0.368)), (midx + rw, int(H * 0.368))], fill=GOLD, width=3)

    f_sub = font(F_TAG_IT, 46)
    d.text((midx, int(H * 0.394)), "Japan — Ainu, burakumin, and the living hands",
           font=f_sub, fill=INK, anchor="mm")
    f_sub2 = font(F_TAG_IT, 38)
    d.text((midx, int(H * 0.422)), "the brochure paints over",
           font=f_sub2, fill=lerp(INK, SKY_TOP, 0.2), anchor="mm")

    f_by = font(F_SERIES, 46)
    tracked(d, (midx, int(H * 0.915)), "ANDRIES J. GREYLING", f_by, GOLD, tracking=10, center_w=True)
    return img


def main():
    img = render_art()
    img = lay_type(img)
    png = OUT / "cover.png"
    jpg = OUT / "cover.jpg"
    img.save(png)
    img.convert("RGB").save(jpg, quality=92)
    print(f"[cover] The Way That Was Invented -> {jpg}  {img.size}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Cover for *A Man They All Read Wrong* — The Jakobus Swart File.

⚠️ SUPERSEDED (2026-06-15): the live cover is now the owner's bespoke POSTER artwork (a finished,
fully-titled illustration installed directly into the cover slots). This procedural generator is
RETIRED so it can't silently overwrite that poster. It is kept for reference only. To deliberately
regenerate the OLD procedural cover, run with the explicit flag:  python3 design/make_cover.py --force

Procedural house cover (Pillow-only, deterministic seed, 6×9in @ 300dpi) — same method as the
HBT Companions. Visual thesis: five offset silhouettes (everyone read a different man), a hollow
centre (the negative space / the man-shaped hole), wraparound shades where the face should be,
and deposition lines radiating outward. No photo plate; no Hollywood bush poster.
"""
from __future__ import annotations

import sys as _sys
if "--force" not in _sys.argv:
    raise SystemExit(
        "make_cover.py is RETIRED — the live cover is the owner's bespoke poster artwork.\n"
        "Re-run with --force only if you intentionally want to regenerate the old procedural cover."
    )

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
BOOK = HERE.parent
OUT_PATHS = [
    HERE / "cover.png",
    HERE / "cover.jpg",
    BOOK / "build" / "export" / "cover.png",
    BOOK / "build" / "export" / "cover.jpg",
]

W, H = 1800, 2700
SEED = 20267

# Brand-adjacent palette — badger-black dusk over Free State veld ochre.
NIGHT = (18, 17, 15)
DUSK = (38, 34, 30)
VELD = (88, 62, 38)
OCHRE = (200, 158, 88)
GOLD = (229, 181, 103)
GOLD_BRIGHT = (245, 220, 158)
CREAM = (236, 230, 220)
INK = (196, 186, 174)
BONE = (189, 182, 166)

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


def tracked(draw, xy, text, fnt, fill, tracking=0, center_w=None):
    widths = [draw.textbbox((0, 0), ch, font=fnt)[2] for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = xy[0] - total // 2 if center_w else xy[0]
    y = xy[1]
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + tracking


def silhouette_polygon(cx, cy, scale=1.0):
    """Plain man — average build, not action-hero. Head + soft shoulders + waistcoat hint."""
    s = scale
    return [
        (cx, cy - 210 * s),
        (cx + 95 * s, cy - 170 * s),
        (cx + 110 * s, cy - 80 * s),
        (cx + 130 * s, cy + 20 * s),
        (cx + 155 * s, cy + 120 * s),
        (cx + 120 * s, cy + 200 * s),
        (cx - 120 * s, cy + 200 * s),
        (cx - 155 * s, cy + 120 * s),
        (cx - 130 * s, cy + 20 * s),
        (cx - 110 * s, cy - 80 * s),
        (cx - 95 * s, cy - 170 * s),
    ]


def draw_shades(draw, cx, cy, scale=1.0, fill=(30, 28, 26), lens=(70, 70, 72)):
    s = scale
    # wraparound band
    draw.rounded_rectangle(
        [cx - 120 * s, cy - 28 * s, cx + 120 * s, cy + 28 * s],
        radius=int(24 * s), fill=fill,
    )
    # lenses — slightly mismatched (one reading saw confidence, one saw coldness)
    draw.ellipse([cx - 98 * s, cy - 18 * s, cx - 28 * s, cy + 18 * s], fill=lens)
    draw.ellipse([cx + 28 * s, cy - 16 * s, cx + 96 * s, cy + 20 * s], fill=lerp(lens, (48, 46, 44), 0.3))
    # faint bridge
    draw.line([(cx - 20 * s, cy), (cx + 20 * s, cy)], fill=lerp(fill, (0, 0, 0), 0.4), width=max(2, int(3 * s)))


def render_art() -> Image.Image:
    rnd = random.Random(SEED)
    img = Image.new("RGB", (W, H), NIGHT)
    d = ImageDraw.Draw(img)

    vgrad(d, 0, 0, W, H, [
        (0.00, NIGHT),
        (0.38, DUSK),
        (0.72, lerp(DUSK, VELD, 0.55)),
        (1.00, lerp(VELD, OCHRE, 0.35)),
    ])

    # Horizon whisper — Free State flatness
    horizon_y = int(H * 0.74)
    d.line([(0, horizon_y), (W, horizon_y)], fill=lerp(VELD, OCHRE, 0.25), width=2)
    for i in range(40):
        x = rnd.randint(0, W)
        h = rnd.randint(4, 22)
        d.line([(x, horizon_y), (x, horizon_y - h)], fill=lerp(VELD, (40, 36, 32), 0.4), width=2)

    cx, cy = W // 2, int(H * 0.58)

    # Deposition lines — testimonies radiating (World War Z / file register)
    dep = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dd = ImageDraw.Draw(dep)
    for i in range(22):
        ang = rnd.uniform(-math.pi * 0.92, -math.pi * 0.08)
        length = rnd.randint(int(W * 0.35), int(W * 0.55))
        x2 = cx + length * math.cos(ang)
        y2 = cy + length * math.sin(ang) * 0.55
        a = rnd.randint(12, 32)
        dd.line([(cx, cy), (x2, y2)], fill=BONE + (a,), width=rnd.choice([1, 1, 2]))
    dep = dep.filter(ImageFilter.GaussianBlur(0))
    img = Image.alpha_composite(img.convert("RGBA"), dep).convert("RGB")

    # Five wrong readings — offset silhouettes, each a different misread
    readings = [
        (cx - 95, cy + 10, 0.92, 52),
        (cx + 110, cy - 15, 0.88, 46),
        (cx - 40, cy + 45, 1.05, 42),
        (cx + 55, cy + 35, 0.96, 48),
        (cx + 5, cy - 55, 0.90, 44),
    ]
    sil_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sil_layer)
    for rx, ry, sc, alpha in readings:
        sd.polygon(silhouette_polygon(rx, ry, sc), fill=(12, 11, 10, alpha))
    sil_layer = sil_layer.filter(ImageFilter.GaussianBlur(2))
    img = Image.alpha_composite(img.convert("RGBA"), sil_layer).convert("RGB")

    # The hollow — warm negative space where he actually was
    hollow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(hollow)
    for r, a in [(420, 16), (320, 28), (220, 42), (140, 58)]:
        hd.ellipse([cx - r, cy - int(r * 1.05), cx + r, cy + int(r * 0.95)], fill=OCHRE + (a,))
    hollow = hollow.filter(ImageFilter.GaussianBlur(55))
    img = Image.alpha_composite(img.convert("RGBA"), hollow).convert("RGB")

    # The one thing everyone saw but misread — shades, centred in the hollow
    shades = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shd = ImageDraw.Draw(shades)
    draw_shades(shd, cx, cy - 20, scale=1.15, fill=(24, 22, 20), lens=(82, 78, 70))
    shades = shades.filter(ImageFilter.GaussianBlur(0))
    img = Image.alpha_composite(img.convert("RGBA"), shades).convert("RGB")
    d = ImageDraw.Draw(img)

    # Pocket stones — boyhood kettie habit, never explained
    stones = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    std = ImageDraw.Draw(stones)
    for sx, sy, col in [
        (cx + 88, cy + 130, (180, 200, 210)),
        (cx + 102, cy + 148, (160, 140, 110)),
        (cx + 74, cy + 142, (120, 130, 150)),
    ]:
        std.ellipse([sx - 10, sy - 8, sx + 10, sy + 8], fill=col + (160,))
    stones = stones.filter(ImageFilter.GaussianBlur(1))
    img = Image.alpha_composite(img.convert("RGBA"), stones).convert("RGB")

    # Top vignette for title
    vig = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vd = ImageDraw.Draw(vig)
    vd.rectangle([0, 0, W, int(H * 0.36)], fill=(0, 0, 0, 100))
    vig = vig.filter(ImageFilter.GaussianBlur(90))
    img = Image.alpha_composite(img.convert("RGBA"), vig).convert("RGB")
    return img


def lay_type(img: Image.Image) -> Image.Image:
    d = ImageDraw.Draw(img)
    midx = W // 2

    f_series = font(F_SERIES, 46)
    tracked(d, (midx, int(H * 0.072)), "HISTORY BEFORE TIME", f_series, GOLD, tracking=12, center_w=True)
    f_file = font(F_SERIES, 32)
    tracked(d, (midx, int(H * 0.108)), "THE JAKOBUS SWART FILE", f_file, BONE, tracking=7, center_w=True)

    rw = int(W * 0.22)
    d.line([(midx - rw, int(H * 0.142)), (midx + rw, int(H * 0.142))], fill=GOLD, width=2)

    f_title = font(F_TITLE, 108)
    lines = ["A MAN", "THEY ALL", "READ WRONG"]
    ty = int(H * 0.162)
    lh = 98
    for i, ln in enumerate(lines):
        d.text((midx, ty + i * lh), ln, font=f_title, fill=GOLD_BRIGHT, anchor="mm")

    f_sub = font(F_TAG_IT, 44)
    d.text((midx, int(H * 0.368)), "assembled, after his death", font=f_sub, fill=INK, anchor="mm")
    f_sub2 = font(F_TAG_IT, 34)
    d.text(
        (midx, int(H * 0.398)),
        "from the people who knew him — and those who only thought they did",
        font=f_sub2,
        fill=lerp(INK, NIGHT, 0.15),
        anchor="mm",
    )

    f_by = font(F_SERIES, 44)
    tracked(d, (midx, int(H * 0.918)), "ANDRIES J. GREYLING", f_by, GOLD, tracking=10, center_w=True)
    return img


def main() -> None:
    img = render_art()
    img = lay_type(img)
    for p in OUT_PATHS:
        p.parent.mkdir(parents=True, exist_ok=True)
        if p.suffix.lower() == ".jpg":
            img.save(p, "JPEG", quality=92)
        else:
            img.save(p, "PNG")
        print(f"wrote {p}")


if __name__ == "__main__":
    main()

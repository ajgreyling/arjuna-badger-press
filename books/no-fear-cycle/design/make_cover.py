#!/usr/bin/env python3
"""Cover art for *Ordinance Pending* — The No-Fear Cycle · Book One.

Composites the selected *Ordinance* illustration into proper 6×9″ @ 300dpi portrait,
re-types with Arjuna Badger Press Atkinson Hyperlegible, boosts contrast for thumbnail
read, and writes design/cover.{jpg,png}.

    python3 design/make_cover.py              # Cover E (enhanced) -> design/cover.*
    python3 design/make_cover.py --variant a  # keep Cover A art only, portrait crop

PDF build (`scripts/build_demo_pdf.sh`) expects design/cover.jpg.
"""
from __future__ import annotations

import argparse
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BRAND = ROOT.parents[2] / "brand"
FONTS = BRAND / "fonts" / "atkinson"
MARK = BRAND / "assets" / "mark-only.png"

W, H = 1800, 2700  # 6×9 @ 300dpi

# Grimdark palette — ridge, orbital fire, Ultramarine blue (no GW logos in typography)
SKY_TOP = (8, 12, 22)
SKY_MID = (18, 28, 48)
FIRE = (255, 120, 40)
FIRE_CORE = (255, 200, 80)
FIRE_TRAIL = (180, 60, 20)
MARINE_BLUE = (28, 48, 88)
CREAM = (238, 232, 218)
BONE = (210, 198, 178)
GOLD = (212, 178, 108)
ORANGE_TITLE = (255, 148, 64)
INK = (160, 168, 178)
BADGER_BLACK = (22, 20, 18)

F_REG = str(FONTS / "Atkinson-Hyperlegible-Regular-102.otf")
F_BOLD = str(FONTS / "Atkinson-Hyperlegible-Bold-102.otf")
F_SERIF = "/System/Library/Fonts/Supplemental/Copperplate.ttc"


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


def draw_orbital_lances(img: Image.Image, rnd: random.Random, count: int = 38) -> Image.Image:
    """Extra lance streaks in the sky band only (above the ridge line)."""
    sky_bottom = int(H * 0.52)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for _ in range(count):
        x0 = rnd.randint(int(W * 0.04), int(W * 0.96))
        y0 = rnd.randint(int(H * 0.14), sky_bottom)
        length = rnd.randint(int(H * 0.06), int(H * 0.16))
        angle = math.radians(rnd.uniform(78, 102))
        x1 = int(x0 + length * math.cos(angle))
        y1 = int(y0 + length * math.sin(angle))
        for width, col, alpha in [
            (12, FIRE_TRAIL, 35),
            (6, FIRE, 80),
            (2, FIRE_CORE, 200),
        ]:
            d.line([(x0, y0), (x1, y1)], fill=col + (alpha,), width=width)
        d.ellipse([x1 - 5, y1 - 5, x1 + 5, y1 + 5], fill=FIRE_CORE + (220,))
    layer = layer.filter(ImageFilter.GaussianBlur(1.0))
    bloom = layer.filter(ImageFilter.GaussianBlur(8))
    out = Image.alpha_composite(img.convert("RGBA"), bloom)
    return Image.alpha_composite(out, layer).convert("RGB")


def composite_source_art(src: Path) -> Image.Image:
    """Crop landscape Ordinance art — strip baked title/author bands, cover-scale portrait."""
    raw = Image.open(src).convert("RGB")
    # Source art has title top ~18% and author bottom ~14%; keep only the illustration band
    crop_box = (
        int(raw.width * 0.04),
        int(raw.height * 0.28),
        int(raw.width * 0.96),
        int(raw.height * 0.84),
    )
    art = raw.crop(crop_box)
    scale = max(W / art.width, H / art.height)
    nw, nh = int(art.width * scale), int(art.height * scale)
    art = art.resize((nw, nh), Image.Resampling.LANCZOS)
    x0 = (W - nw) // 2
    y0 = (H - nh) // 2 + int(H * 0.04)  # slight downward bias for ridge hero
    canvas = Image.new("RGB", (W, H), SKY_TOP)
    vgrad(ImageDraw.Draw(canvas), 0, 0, W, H, [
        (0.0, SKY_TOP), (0.3, SKY_MID), (0.65, (24, 32, 48)), (1.0, (12, 14, 18)),
    ])
    canvas.paste(art, (x0, y0))
    return canvas


def mask_typography_bands(img: Image.Image) -> Image.Image:
    """Scrub remaining baked type from source art; scrims for fresh type."""
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    # Solid top band — kills ghost title letterforms in sky
    d.rectangle([0, 0, W, int(H * 0.22)], fill=BADGER_BLACK + (255,))
    for y in range(int(H * 0.22), int(H * 0.34)):
        t = 1.0 - (y - H * 0.22) / (H * 0.12)
        d.line([(0, y), (W, y)], fill=BADGER_BLACK + (int(255 * t),))
    # Mid-art series line from source (approx y 48–54%)
    mid0, mid1 = int(H * 0.46), int(H * 0.54)
    for y in range(mid0, mid1):
        t = 1 - abs(y - (mid0 + mid1) // 2) / ((mid1 - mid0) // 2)
        d.line([(0, y), (W, y)], fill=BADGER_BLACK + (int(200 * t),))
    for y in range(int(H * 0.88), H):
        t = ((y - H * 0.88) / (H * 0.12)) ** 0.75
        d.line([(0, y), (W, y)], fill=BADGER_BLACK + (int(240 * t),))
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")


def enhance(img: Image.Image) -> Image.Image:
    img = ImageEnhance.Contrast(img).enhance(1.14)
    img = ImageEnhance.Color(img).enhance(1.08)
    vig = Image.new("RGBA", img.size, (0, 0, 0, 0))
    vd = ImageDraw.Draw(vig)
    cx, cy = W // 2, int(H * 0.55)
    for r in range(int(min(W, H) * 0.62), 0, -4):
        t = r / (min(W, H) * 0.62)
        a = int(55 * (1 - t) ** 2)
        vd.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(0, 0, 0, a), width=4)
    return Image.alpha_composite(img.convert("RGBA"), vig).convert("RGB")


def tracked(draw, cx, y, text, fnt, fill, tracking=0):
    widths = [draw.textbbox((0, 0), ch, font=fnt)[2] for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total // 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + tracking


def draw_title_block(img: Image.Image) -> Image.Image:
    d = ImageDraw.Draw(img)
    cx = W // 2

    f_series = font(F_REG, 34)
    tracked(d, cx, int(H * 0.055), "THE NO-FEAR CYCLE", f_series, INK, tracking=10)
    f_book = font(F_BOLD, 30)
    tracked(d, cx, int(H * 0.088), "BOOK ONE", f_book, BONE, tracking=8)

    rw = int(W * 0.18)
    d.line([(cx - rw, int(H * 0.118)), (cx + rw, int(H * 0.118))], fill=FIRE + (200,), width=2)

    f_title = font(F_BOLD, 102)
    tracked(d, cx + 3, int(H * 0.152) + 3, "ORDINANCE", f_title, (0, 0, 0), tracking=6)
    tracked(d, cx, int(H * 0.152), "ORDINANCE", f_title, ORANGE_TITLE, tracking=6)
    f_pending = font(F_BOLD, 92)
    tracked(d, cx + 3, int(H * 0.218) + 3, "PENDING", f_pending, (0, 0, 0), tracking=8)
    tracked(d, cx, int(H * 0.218), "PENDING", f_pending, CREAM, tracking=8)

    f_sub = font(F_REG, 34)
    d.text((cx, int(H * 0.278)), "Metaurus · Titus · the ridge before the lance",
           font=f_sub, fill=INK, anchor="mm")

    f_by = font(F_SERIF, 46, index=0)
    tracked(d, cx, int(H * 0.905), "ANDRIES J. GREYLING", f_by, GOLD, tracking=12)

    f_press = font(F_REG, 26)
    tracked(d, cx, int(H * 0.945), "ARJUNA BADGER PRESS", f_press, INK, tracking=6)

    if MARK.exists():
        mark = Image.open(MARK).convert("RGBA")
        ms = int(W * 0.055)
        mark = mark.resize((ms, ms), Image.Resampling.LANCZOS)
        mx = cx - ms // 2
        my = int(H * 0.968)
        img.paste(mark, (mx, my), mark)

    return img


def render(variant: str = "e", seed: int = 20401) -> Image.Image:
    rnd = random.Random(seed)
    src = HERE / "covers" / "cover-a-ordinance.png"
    if not src.exists():
        src = HERE / "cover.png"
    img = composite_source_art(src)
    img = enhance(img)
    if variant == "e":
        img = draw_orbital_lances(img, rnd, count=28)
        img = enhance(img)
    img = mask_typography_bands(img)
    img = draw_title_block(img)
    return img


def save_cover(img: Image.Image, png: Path, jpg: Path) -> None:
    png.parent.mkdir(parents=True, exist_ok=True)
    img.save(png)
    img.convert("RGB").save(jpg, quality=93, optimize=True)
    print(f"[cover] -> {jpg}  {img.size}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", choices=("a", "e"), default="e",
                    help="e = enhanced Cover E (default); a = portrait crop only")
    args = ap.parse_args()

    img = render(args.variant)
    save_cover(img, HERE / "cover.png", HERE / "cover.jpg")

    covers = HERE / "covers"
    covers.mkdir(exist_ok=True)
    if args.variant == "e":
        save_cover(img, covers / "cover-e-ordinance-enhanced.png",
                   covers / "cover-e-ordinance-enhanced.jpg")
        # Keep Cover A source untouched
        print("[cover] Cover E saved to design/covers/cover-e-ordinance-enhanced.png")


if __name__ == "__main__":
    main()

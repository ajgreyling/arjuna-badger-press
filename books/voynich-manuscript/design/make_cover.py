#!/usr/bin/env python3
"""Cover for *The Unread* — The Why Files · the Voynich Manuscript.

Visual language: a single page of fluent, lawful, unreadable script glowing in a conservator's
raking light against archival dark — the most eloquent silent thing in the world. Procedural
"Voynichese" (deterministic, fixed seed): a constructed glyph-hand that LOOKS like writing and
says nothing, thumb-worn soft at one corner. 6×9in @ 300dpi.

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
ATK_BI = str(_ATK / "AtkinsonHyperlegible-BoldItalic.otf")


W, H = 1800, 2700
SEED = 14041438  # the C-14 interval, 1404–1438

# The Why Files · archival dark with a raking-light warmth; series accent amber-gold.
DARK_TOP = (12, 13, 16)
DARK_MID = (22, 21, 24)
VELLUM = (188, 170, 138)        # the lit calfskin
VELLUM_SHADOW = (120, 104, 80)
VELLUM_WORN = (206, 192, 166)   # the thumb-soft corner, paler
INK = (40, 32, 24)              # iron-gall brown-black
INK_FADED = (92, 74, 54)
RAKE = (236, 206, 150)          # the warm raking light
AMBER = (212, 168, 96)          # series accent
AMBER_BRIGHT = (240, 206, 150)
CREAM = (234, 226, 212)
GREY = (150, 142, 132)

F_TITLE = ATK_BOLD
F_SERIES = ATK_REG
F_TAG_IT = ATK_ITAL
def font(path: str, size: int, index: int = 0) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(path, size, index=index)
    except Exception:
        return ImageFont.load_default()


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vellum_panel(rng):
    """The lit page: a warm parchment rectangle with a raking-light gradient and a worn corner."""
    pw, ph = int(W * 0.74), int(H * 0.52)
    px, py = (W - pw) // 2, int(H * 0.20)
    panel = Image.new("RGB", (pw, ph), VELLUM)
    pd = ImageDraw.Draw(panel)
    # raking light from the upper-left: brighten that way, shadow the lower-right
    for y in range(ph):
        for_band = y / ph
        # cheap horizontal-only gradient per row for speed; add a diagonal feel
        top = lerp(RAKE, VELLUM, min(1.0, for_band * 1.4))
        bot = lerp(VELLUM, VELLUM_SHADOW, for_band)
        col = lerp(top, bot, 0.5)
        pd.line([(0, y), (pw, y)], fill=col)
    # subtle fibre mottling
    for _ in range(2600):
        x = rng.randint(0, pw - 1)
        y = rng.randint(0, ph - 1)
        d = rng.randint(-14, 14)
        base = panel.getpixel((x, y))
        panel.putpixel((x, y), tuple(max(0, min(255, c + d)) for c in base))
    # the thumb-worn lower-outer corner: a soft pale bloom
    corner = Image.new("L", (pw, ph), 0)
    cd = ImageDraw.Draw(corner)
    cx, cy = int(pw * 0.86), int(ph * 0.9)
    cd.ellipse([cx - 240, cy - 200, cx + 260, cy + 220], fill=120)
    corner = corner.filter(ImageFilter.GaussianBlur(90))
    worn = Image.new("RGB", (pw, ph), VELLUM_WORN)
    panel = Image.composite(worn, panel, corner)
    return panel, (px, py, pw, ph)


def glyph(draw, x, y, h, rng, col):
    """One procedural 'Voynichese' character: looks like a real ductus, says nothing.
    Built from a stem + optional bench/gallows loop + tail — fluent, never legible."""
    w = h * rng.uniform(0.42, 0.72)
    lw = max(2, int(h * 0.085))
    kind = rng.random()
    # baseline stem
    if kind < 0.5:
        # 'minim' with a curved foot
        draw.line([(x, y), (x, y - h * 0.7)], fill=col, width=lw)
        draw.arc([x - w * 0.5, y - h * 0.2, x + w * 0.5, y + h * 0.3], 200, 340, fill=col, width=lw)
    elif kind < 0.78:
        # 'gallows' — tall loop (word-initial feel)
        draw.line([(x, y), (x, y - h)], fill=col, width=lw)
        draw.arc([x - w * 0.2, y - h * 1.18, x + w * 1.1, y - h * 0.55], 150, 360, fill=col, width=lw)
    else:
        # 'eva-o/e' — a small bowl
        draw.ellipse([x - w * 0.45, y - h * 0.62, x + w * 0.45, y - h * 0.05], outline=col, width=lw)
    # occasional connecting tail (the smooth ductus)
    if rng.random() < 0.55:
        draw.arc([x + w * 0.2, y - h * 0.3, x + w * 1.2, y + h * 0.25], 180, 320, fill=col, width=lw)
    return w


def write_unreadable(panel_draw, pw, ph, rng):
    """Fill the page with fluent lines of glyphs that obey rules and mean nothing."""
    margin_x = int(pw * 0.12)
    margin_top = int(ph * 0.13)
    line_h = int(ph * 0.052)
    y = margin_top + line_h
    line_no = 0
    while y < ph - int(ph * 0.12):
        x = margin_x
        # a faint star-marker on some lines (the 'recipe' paragraphs)
        if rng.random() < 0.22:
            sx = margin_x - int(pw * 0.055)
            panel_draw.line([(sx - 8, y - line_h * 0.4), (sx + 8, y - line_h * 0.4)], fill=INK_FADED, width=3)
            panel_draw.line([(sx, y - line_h * 0.4 - 8), (sx, y - line_h * 0.4 + 8)], fill=INK_FADED, width=3)
        right = pw - margin_x
        # words: 2–6 glyphs, with the Voynich 'stacking' (repeat a word now and then)
        while x < right - 40:
            wlen = rng.randint(2, 6)
            word_seed = rng.randint(0, 9999)
            reps = 1
            if rng.random() < 0.08:
                reps = rng.randint(2, 4)  # the famous same-word-repeats
            for _ in range(reps):
                wr = random.Random(word_seed)
                gx = x
                gh = line_h * rng.uniform(0.74, 0.92)
                col = INK if rng.random() < 0.85 else INK_FADED
                for _ in range(wlen):
                    gw = glyph(panel_draw, gx, y, gh, wr, col)
                    gx += gw + gh * 0.16
                    if gx > right - 30:
                        break
                x = gx + gh * 0.5  # word space
                if x > right - 40:
                    break
        y += line_h
        line_no += 1


def main():
    rng = random.Random(SEED)
    img = Image.new("RGB", (W, H), DARK_TOP)
    d = ImageDraw.Draw(img)
    # archival dark vertical gradient
    for y in range(H):
        d.line([(0, y), (W, y)], fill=lerp(DARK_TOP, DARK_MID, y / H))

    # the lit page
    panel, (px, py, pw, ph) = vellum_panel(rng)
    pdraw = ImageDraw.Draw(panel)
    write_unreadable(pdraw, pw, ph, rng)
    # soft inner shadow so the page sits in the dark
    panel = panel.filter(ImageFilter.GaussianBlur(0.4))
    # drop shadow
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rectangle([px - 18, py - 14, px + pw + 26, py + ph + 34], fill=(0, 0, 0, 170))
    shadow = shadow.filter(ImageFilter.GaussianBlur(40))
    img.paste(Image.alpha_composite(img.convert("RGBA"), shadow).convert("RGB"), (0, 0))
    img.paste(panel, (px, py))

    # a warm raking-light wash across the upper-left of the whole cover
    glow = Image.new("L", (W, H), 0)
    gd = ImageDraw.Draw(glow)
    gd.ellipse([-W * 0.3, -H * 0.2, W * 0.7, H * 0.5], fill=70)
    glow = glow.filter(ImageFilter.GaussianBlur(220))
    warm = Image.new("RGB", (W, H), RAKE)
    img = Image.composite(warm, img, glow)

    d = ImageDraw.Draw(img)

    # ── series line (top) ──
    fser = font(F_SERIES, 44)
    series = "THE WHY FILES"
    sb = d.textbbox((0, 0), series, font=fser)
    d.text(((W - (sb[2] - sb[0])) // 2, int(H * 0.072)), series, font=fser, fill=AMBER)
    sub = font(F_SERIES, 30)
    subt = "THE VOYNICH MANUSCRIPT"
    ub = d.textbbox((0, 0), subt, font=sub)
    d.text(((W - (ub[2] - ub[0])) // 2, int(H * 0.072) + 60), subt, font=sub, fill=GREY)

    # ── title (lower third, over the dark) ──
    ftitle = font(F_TITLE, 230, index=0)
    title = "The Unread"
    tb = d.textbbox((0, 0), title, font=ftitle)
    tx = (W - (tb[2] - tb[0])) // 2
    ty = int(H * 0.775)
    # a soft plate behind the title so it reads over any glyphs that bleed near it
    plate = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ppd = ImageDraw.Draw(plate)
    ppd.rectangle([0, ty - 40, W, ty + (tb[3] - tb[1]) + 70], fill=(12, 12, 15, 205))
    plate = plate.filter(ImageFilter.GaussianBlur(30))
    img = Image.alpha_composite(img.convert("RGBA"), plate).convert("RGB")
    d = ImageDraw.Draw(img)
    d.text((tx, ty), title, font=ftitle, fill=CREAM)

    # ── tagline ──
    ftag = font(ATK_ITAL, 46)
    tag = "A real book. A real hand. An unread page."
    gb = d.textbbox((0, 0), tag, font=ftag)
    d.text(((W - (gb[2] - gb[0])) // 2, ty + (tb[3] - tb[1]) + 96), tag, font=ftag, fill=AMBER_BRIGHT)

    # ── author (foot) ──
    fauth = font(F_SERIES, 40)
    auth = "ANDRIES J. GREYLING"
    ab = d.textbbox((0, 0), auth, font=fauth)
    d.text(((W - (ab[2] - ab[0])) // 2, int(H * 0.945)), auth, font=fauth, fill=GREY)

    img.save(OUT / "cover.png")
    img.convert("RGB").save(OUT / "cover.jpg", quality=90)
    print(f"[cover] wrote {OUT/'cover.png'} and cover.jpg  ({W}x{H})")


if __name__ == "__main__":
    main()

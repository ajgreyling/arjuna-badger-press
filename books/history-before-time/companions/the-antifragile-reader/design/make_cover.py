#!/usr/bin/env python3
"""Compose the typographic cover for *The Antifragile Reader*.

No cinematic plate — this is a designed *typography-and-diagram* cover in the house manner, fitting an
open-draft companion. A dark field carries a single quiet figure: three lines for Taleb's three states
of the world — the fragile line that breaks under stress, the robust line that holds flat, and the
antifragile line that rises *because of* the stress — and the house Didot/Cochin title above it.

Re-runnable: always works from nothing but fonts. Writes design/cover.{png,jpg} + build/export/.

    python3 design/make_cover.py
"""
from __future__ import annotations

import math
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

# the three states, by colour
C_FRAGILE = (196, 92, 78, 255)    # terracotta — the line that breaks
C_ROBUST = (150, 140, 124, 255)   # stone — the line that holds flat
C_ANTI = (229, 181, 103, 255)     # gold — the line that gains from disorder


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
    """A deep, slightly warm night field — not flat black, so the file carries real tonal data."""
    g = Image.new("RGB", (W, H))
    px = g.load()
    for y in range(H):
        t = y / H
        # ease toward the warmer floor
        t2 = t ** 1.2
        r = int(top[0] + (bot[0] - top[0]) * t2)
        gg = int(top[1] + (bot[1] - top[1]) * t2)
        b = int(top[2] + (bot[2] - top[2]) * t2)
        for x in range(W):
            px[x, y] = (r, gg, b)
    return g


def add_grain(img, amount=7):
    """Subtle film grain so the cover is a real composed image (and comfortably > 500 KB as PNG)."""
    import random
    random.seed(1838)  # fixed seed — re-runnable, deterministic
    noise = Image.new("L", (W, H))
    np = noise.load()
    for y in range(H):
        for x in range(W):
            np[x, y] = 128 + random.randint(-amount, amount)
    noise = noise.filter(ImageFilter.GaussianBlur(0.4))
    grain = Image.merge("RGB", (noise, noise, noise))
    return Image.blend(img, grain, 0.045)


def three_state_figure(draw, cx, top_y, span_w, span_h):
    """Three small panels, side by side: fragile (snaps), robust (flat), antifragile (rises).

    Each panel shares the same x-domain (rising 'stress'); the y-response is the whole argument.
    Separate panels keep the three responses legible instead of letting the curves collide.
    """
    gap = span_w * 0.085
    pw = (span_w - 2 * gap) / 3            # panel width
    ph = span_h
    panels_x0 = cx - span_w / 2
    n = 120

    def panel(idx, colour, fn, break_at=None):
        px0 = panels_x0 + idx * (pw + gap)
        base = top_y + ph
        # faint frame floor for each panel
        draw.line([(px0, base + 1), (px0 + pw, base + 1)], fill=(64, 58, 50, 255), width=2)
        cut = int((break_at if break_at else 1.0) * n)
        pts = []
        for i in range(cut + 1):
            t = i / n
            x = px0 + t * pw
            y = base - fn(t) * ph
            pts.append((x, y))
        if len(pts) >= 2:
            draw.line(pts, fill=colour, width=8, joint="curve")
        if break_at is not None:
            # a clean snap: the line stops, a small gap, then a short stub drops away
            bx, by = pts[-1]
            draw.ellipse([bx - 6, by - 6, bx + 6, by + 6], fill=colour)  # the break point
            sx = bx + pw * 0.10
            sy = by + ph * 0.42
            draw.line([(sx, sy), (px0 + pw, sy + ph * 0.10)], fill=colour, width=8, joint="curve")

    # fragile: rises then snaps partway — terracotta
    panel(0, C_FRAGILE, lambda t: 0.20 + 0.95 * t, break_at=0.60)
    # robust: holds flat — survives, gains nothing — stone
    panel(1, C_ROBUST, lambda t: 0.46)
    # antifragile: convex — rises faster as stress grows — gold
    panel(2, C_ANTI, lambda t: 0.12 + 0.86 * (t ** 1.9))


def main() -> None:
    img = vertical_gradient((16, 17, 24), (28, 20, 14)).convert("RGBA")

    # soft top vignette to seat the title
    scrim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrim)
    top_end = int(H * 0.40)
    for y in range(top_end):
        a = int(150 * (1 - y / top_end) ** 1.4)
        sd.line([(0, y), (W, y)], fill=(8, 9, 14, a))
    img = Image.alpha_composite(img, scrim)

    draw = ImageDraw.Draw(img)
    cx = W / 2

    # eyebrow
    draw_tracked(draw, cx, int(H * 0.058), "HISTORY BEFORE TIME", font(COCHIN, 50), 13, INK)
    tag, f_tag = "COMPANIONS", font(COCHIN, 34)
    draw_tracked(draw, cx, int(H * 0.094), tag, f_tag, 11, OCHRE)
    tw = text_width(draw, tag, f_tag, 11)
    dy = int(H * 0.094) + 22
    for sx in (cx - tw / 2 - 44, cx + tw / 2 + 44):
        draw.ellipse([sx - 4, dy - 4, sx + 4, dy + 4], fill=OCHRE)

    rule_y = int(H * 0.128)
    draw.line([(cx - 210, rule_y), (cx + 210, rule_y)], fill=INK, width=3)

    # title
    f_title = font(DIDOT, 168)
    lines = ["THE", "ANTIFRAGILE", "READER"]
    ty = int(H * 0.152)
    lh = 184
    for i, ln in enumerate(lines):
        sz = 168 if ln != "ANTIFRAGILE" else 150  # fit the long word
        draw_tracked(draw, cx, ty + i * lh, ln, font(DIDOT, sz), 4, INK)

    # subtitle in a soft glass band
    f_sub = font(ATK_ITAL, 52)
    sub = "Nassim Taleb's Incerto, plainly told"
    sub_y = ty + 3 * lh + 30
    sub_w = text_width(draw, sub, f_sub, 1)
    band = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(band)
    bd.rounded_rectangle(
        [cx - sub_w / 2 - 70, sub_y - 18, cx + sub_w / 2 + 70, sub_y + 70],
        radius=30, fill=(14, 11, 16, 120),
    )
    band = band.filter(ImageFilter.GaussianBlur(22))
    img = Image.alpha_composite(img, band)
    draw = ImageDraw.Draw(img)
    draw_tracked(draw, cx, sub_y, sub, f_sub, 1, DIM)

    # the three-state figure, the cover's quiet argument
    fig_top = sub_y + 150
    three_state_figure(draw, cx, fig_top, span_w=W * 0.62, span_h=H * 0.165)

    # a one-line gloss under the figure
    draw_tracked(draw, cx, fig_top + H * 0.165 + 40,
                 "fragile breaks · robust holds · antifragile gains",
                 font(COCHIN, 38), 4, FAINT)

    # author
    draw_tracked(draw, cx, int(H * 0.92), "ANDRIES J. GREYLING", font(COCHIN, 62), 9, INK)
    draw_tracked(draw, cx, int(H * 0.955), "A GUEST-AT-THE-FIRE COMPANION · AN OPEN DRAFT",
                 font(COCHIN, 27), 5, FAINT)

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

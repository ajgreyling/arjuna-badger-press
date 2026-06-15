#!/usr/bin/env python3
"""House-style "coming soon" covers for the *Not a Potato* shelf.

Procedural (Pillow-only, deterministic, 1800×2700 @ 300dpi) — the same house method as the other
covers. Visual thesis of the line: the official story played dead straight, with **one hole in it**.
So each cover is a dense field of neat "official-record" rule-lines in bone, with a single gold gap
where one line refuses to close — the unresolved residue. Badger-Black field, gold serif title,
"NOT A POTATO" eyebrow, "COMING SOON" footer. No EPUB/PDF; this is the placeholder cover.

    python3 design/make_notapotato_covers.py
      -> books/_comingsoon/<id>/design/cover.{png,jpg} + covers/<id>.jpg
"""
from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO = Path(__file__).resolve().parent.parent
W, H = 1800, 2700

# House palette (brand/BRAND.md)
BADGER_BLACK = (22, 21, 19)
NIGHT        = (16, 15, 14)
BONE         = (237, 233, 224)
BONE_DIM     = (120, 116, 108)
GOLD         = (213, 168, 96)
GOLD_BRIGHT  = (240, 214, 150)
VELD_OCHRE   = (176, 122, 60)

F_TITLE  = "/System/Library/Fonts/Supplemental/Optima.ttc"        # idx 1 = Bold
F_SERIES = "/System/Library/Fonts/Supplemental/Copperplate.ttc"   # idx 2 = Bold
F_TAG    = "/System/Library/Fonts/Supplemental/Cochin.ttc"        # idx 2 = Italic

BOOKS = [
    # id, title, the gold-gap "residue" caption
    ("crop-circles",       ["The Field", "of Doors"],        "the one that won't close"),
    ("gobekli-tepe",       ["The Belly", "Hill"],            "older than the plough"),
    ("voynich-manuscript", ["The Hand", "That Wrote It"],    "a language no one reads"),
    ("suppressed-tech",    ["The Quiet", "Men"],             "the thing we couldn't keep"),
]


def font(path, size, index=0):
    return ImageFont.truetype(path, size, index=index)


def lerp(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def vgrad(d, x0, y0, x1, y1, stops):
    span = max(1, y1 - y0)
    for y in range(y0, y1):
        t = (y - y0) / span
        lo, hi = stops[0], stops[-1]
        for i in range(len(stops) - 1):
            if stops[i][0] <= t <= stops[i + 1][0]:
                lo, hi = stops[i], stops[i + 1]
                break
        loc = 0.0 if hi[0] == lo[0] else (t - lo[0]) / (hi[0] - lo[0])
        d.line([(x0, y), (x1, y)], fill=lerp(lo[1], hi[1], loc))


def tracked(d, xy, text, fnt, fill, tracking=0, center=False):
    widths = [d.textbbox((0, 0), c, font=fnt)[2] for c in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = xy[0] - total // 2 if center else xy[0]
    y = xy[1]
    for c, w in zip(text, widths):
        d.text((x, y), c, font=fnt, fill=fill)
        x += w + tracking


def render(book) -> Image.Image:
    bid, title_lines, residue = book
    rnd = random.Random(sum(ord(c) for c in bid))
    img = Image.new("RGB", (W, H), BADGER_BLACK)
    d = ImageDraw.Draw(img)
    vgrad(d, 0, 0, W, H, [(0.0, NIGHT), (0.4, BADGER_BLACK), (1.0, lerp(BADGER_BLACK, VELD_OCHRE, 0.10))])

    # The "official record" — a dense field of neat bone rule-lines in the middle band.
    top, bot = int(H * 0.30), int(H * 0.66)
    n = 26
    gap_line = rnd.randint(int(n * 0.40), int(n * 0.62))   # which line carries the hole
    left, right = int(W * 0.16), int(W * 0.84)
    for i in range(n):
        y = top + int((bot - top) * i / (n - 1))
        if i == gap_line:
            # the one line that won't close: a gold segment, then a GAP, then nothing
            seg = int((right - left) * rnd.uniform(0.34, 0.5))
            d.line([(left, y), (left + seg, y)], fill=GOLD_BRIGHT, width=5)
            # a faint gold glow around the break
            glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            gd = ImageDraw.Draw(glow)
            gd.ellipse([left + seg - 60, y - 60, left + seg + 60, y + 60], fill=GOLD + (60,))
            glow = glow.filter(ImageFilter.GaussianBlur(30))
            img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
            d = ImageDraw.Draw(img)
            d.line([(left, y), (left + seg, y)], fill=GOLD_BRIGHT, width=5)
        else:
            # an ordinary "settled" line — bone, slightly varied length, dim
            w = int((right - left) * rnd.uniform(0.82, 1.0))
            a = rnd.randint(38, 70)
            d.line([(left, y), (left + w, y)], fill=lerp(BADGER_BLACK, BONE, a / 255), width=2)

    # eyebrow
    tracked(d, (W // 2, int(H * 0.085)), "NOT A POTATO", font(F_SERIES, 44, 2), GOLD, tracking=14, center=True)
    rw = int(W * 0.14)
    d.line([(W // 2 - rw, int(H * 0.125)), (W // 2 + rw, int(H * 0.125))], fill=GOLD, width=2)

    # title (Optima Bold, gold-bright, lower band)
    ft = font(F_TITLE, 150, 1)
    ty = int(H * 0.72)
    for ln in title_lines:
        d.text((W // 2 + 3, ty + 3), ln, font=ft, fill=lerp(VELD_OCHRE, BADGER_BLACK, 0.5), anchor="mm")
        d.text((W // 2, ty), ln, font=ft, fill=GOLD_BRIGHT, anchor="mm")
        ty += 150

    # residue caption (the wink) — Cochin italic
    d.text((W // 2, int(H * 0.835)), residue, font=font(F_TAG, 46, 2), fill=BONE, anchor="mm")

    # coming soon + press
    tracked(d, (W // 2, int(H * 0.90)), "COMING SOON", font(F_SERIES, 34, 2), BONE_DIM, tracking=12, center=True)
    tracked(d, (W // 2, int(H * 0.945)), "ARJUNA BADGER PRESS", font(F_SERIES, 26, 2), BONE_DIM, tracking=8, center=True)
    return img


def main():
    for book in BOOKS:
        bid = book[0]
        img = render(book)
        outs = [
            REPO / "books" / "_comingsoon" / bid / "design" / "cover.png",
            REPO / "books" / "_comingsoon" / bid / "design" / "cover.jpg",
            REPO / "covers" / f"{bid}.jpg",
        ]
        for p in outs:
            p.parent.mkdir(parents=True, exist_ok=True)
            img.save(p, "JPEG", quality=90) if p.suffix == ".jpg" else img.save(p, "PNG")
        print(f"  wrote cover for {bid}")
    print("\nNot a Potato — coming-soon covers rendered (4).")


if __name__ == "__main__":
    main()

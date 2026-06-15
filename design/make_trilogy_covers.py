#!/usr/bin/env python3
"""The African Gold Trilogy — house-style cover SET (RESONANCE · REVELATION · RELIC).

One generator, three covers, deliberately a *set*. Arjuna Badger Press house method:
Pillow-only, deterministic seed, 1800×2700 (6×9in @ 300dpi), brand palette, procedural art +
typographic layer — the same technique as design/.../make_cover.py (the Jakobus File / Companions).

The "set" signal (identical on all three):
  • Badger-Black field; identical layout grid.
  • The signature device — the bone DORSAL STRIPE that resolves into a LOOSED-ARROW arrowhead —
    runs edge-to-edge at the same y on every cover (the "line of flight").
  • Series eyebrow "THE AFRICAN GOLD TRILOGY" + the book numeral, same place, same faces.
  • Title in Optima Bold seated on the arrow-line; Cochin-italic tagline; Copperplate author;
    a thin Press rule + "ARJUNA BADGER PRESS" at the foot.
  • A faint honeycomb-hex resonance wash (the engine is a resonance key).

The per-book signal (so they're three individuals, in order):
  • An accent TEMPERATURE that progresses with the story —
        RESONANCE  cool dawn ochre  (the minds first tuned)
        REVELATION the hot charge   (Sting-Red — the edit found, the loosed arrow)
        RELIC      full molten gold (the key found; the warmest)
  • The arrow STRIKES a resonance node; rings ring outward — denser book to book (1→2→3 rings).

    python3 design/make_trilogy_covers.py     # -> books/<id>/design/cover.{png,jpg}
                                              #  + books/<id>/build/export/cover.{png,jpg}
                                              #  + covers/<id>.jpg   (the catalog thumbnail)
"""
from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO = Path(__file__).resolve().parent.parent
W, H = 1800, 2700

# ── House palette (brand/BRAND.md) ────────────────────────────────────────────────────────────
BADGER_BLACK = (22, 21, 19)     # #161513 — home; the field
NIGHT        = (16, 15, 14)     # a hair deeper, for the top vignette
BONE         = (237, 233, 224)  # #EDE9E0 — the dorsal stripe / arrow-line / primary light text
BONE_DIM     = (150, 146, 138)
VELD_OCHRE   = (176, 122, 60)   # #B07A3C — the accent spark
STING_RED    = (194, 64, 30)    # #C2401E — the one hot charge / the loosed arrow
GOLD         = (213, 168, 96)
GOLD_BRIGHT  = (240, 214, 150)

# ── House faces (same as the shipped house covers) ────────────────────────────────────────────
F_TITLE  = "/System/Library/Fonts/Supplemental/Optima.ttc"        # idx 1 = Bold
F_SERIES = "/System/Library/Fonts/Supplemental/Copperplate.ttc"   # idx 2 = Bold (engraved eyebrow)
F_TAG    = "/System/Library/Fonts/Supplemental/Cochin.ttc"        # idx 2 = Italic (tagline)
F_NUM    = "/System/Library/Fonts/Supplemental/Futura.ttc"        # idx 4 = Condensed ExtraBold


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


def tracked(draw, xy, text, fnt, fill, tracking=0, center_w=False):
    widths = [draw.textbbox((0, 0), ch, font=fnt)[2] for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = xy[0] - total // 2 if center_w else xy[0]
    y = xy[1]
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + tracking


# ── The three books (order is the trilogy order) ──────────────────────────────────────────────
BOOKS = [
    {
        "id": "resonance",
        "numeral": "BOOK ONE",
        "title": "RESONANCE",
        "tagline": "Some minds were not born. They were tuned.",
        "accent": VELD_OCHRE,        # cool dawn spark
        "accent_bright": GOLD,
        "rings": 1,                  # the first node struck
        "warm": 0.30,                # field warmth 0..1 (rises across the set)
        "seed": 1011,
    },
    {
        "id": "revelation",
        "numeral": "BOOK TWO",
        "title": "REVELATION",
        "tagline": "Every sacred text was edited. She found the edits.",
        "accent": STING_RED,         # the hot charge — the loosed arrow
        "accent_bright": (224, 104, 64),
        "rings": 2,
        "warm": 0.46,
        "seed": 2022,
    },
    {
        "id": "relic",
        "numeral": "BOOK THREE",
        "title": "RELIC",
        "tagline": "The gold was never the treasure. It was the key.",
        "accent": GOLD,              # full molten gold — the key found
        "accent_bright": GOLD_BRIGHT,
        "rings": 3,
        "warm": 0.62,
        "seed": 3033,
    },
]

# Shared geometry — IDENTICAL on all three (this is what makes it read as a set).
ARROW_Y   = int(H * 0.605)   # the dorsal stripe / arrow-line height
NODE_X    = int(W * 0.50)    # where the arrow strikes the resonance node
EYEBROW_Y = int(H * 0.072)
NUM_Y     = int(H * 0.112)
TITLE_Y   = int(H * 0.548)   # the big title seats just ABOVE the arrow-line (on the line of flight)
TAG_Y     = int(H * 0.652)   # tagline sits just BELOW the arrow-line
AUTHOR_Y  = int(H * 0.905)
PRESS_Y   = int(H * 0.945)


def hex_wash(book) -> Image.Image:
    """Faint honeycomb (the resonance/engine motif) — subtle, behind everything."""
    rnd = random.Random(book["seed"] + 7)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    r = 70
    dx = int(r * 1.5)
    dy = int(r * math.sqrt(3))
    col = lerp(BADGER_BLACK, book["accent"], 0.5)
    for row, gy in enumerate(range(-dy, H + dy, dy // 1)):
        for gx in range(-dx, W + dx, dx * 1):
            ox = (dx // 1) if (row % 2) else 0
            cx, cy = gx + ox, gy
            pts = [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
                   for a in range(0, 360, 60)]
            a = rnd.randint(4, 12)
            d.line(pts + [pts[0]], fill=col + (a,), width=1)
    return layer.filter(ImageFilter.GaussianBlur(0.6))


def render_field(book) -> Image.Image:
    """Badger-Black field with a faint warm ground rising from the foot (warmth grows per book)."""
    img = Image.new("RGB", (W, H), BADGER_BLACK)
    d = ImageDraw.Draw(img)
    warm_ground = lerp(BADGER_BLACK, book["accent"], 0.18 * book["warm"] / 0.62)
    vgrad(d, 0, 0, W, H, [
        (0.00, NIGHT),
        (0.34, BADGER_BLACK),
        (0.62, BADGER_BLACK),
        (1.00, warm_ground),
    ])
    img = Image.alpha_composite(img.convert("RGBA"), hex_wash(book)).convert("RGB")
    return img


def resonance_rings(book) -> Image.Image:
    """Concentric rings ringing out from the struck node — symmetric (centred on the node),
    one more ring per book (1→2→3). Every cover gets ONE bright leading ring so book one reads
    as designed, not empty; the extra rings (book 2, 3) fade outward."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    n = book["rings"]
    step = 215
    for k in range(n):
        rr = 175 + k * step
        # the innermost ring is the brightest; outer rings dim with distance
        head_a = 150 if k == 0 else max(28, 150 - k * 60)
        col = book["accent_bright"] if k == 0 else book["accent"]
        # a crisp leading ring + two soft echoes just outside it (concentric, both sides — symmetric)
        d.ellipse([NODE_X - rr, ARROW_Y - rr, NODE_X + rr, ARROW_Y + rr],
                  outline=col + (head_a,), width=3)
        d.ellipse([NODE_X - rr - 26, ARROW_Y - rr - 26, NODE_X + rr + 26, ARROW_Y + rr + 26],
                  outline=col + (max(14, head_a // 3),), width=2)
        d.ellipse([NODE_X - rr - 60, ARROW_Y - rr - 60, NODE_X + rr + 60, ARROW_Y + rr + 60],
                  outline=col + (max(8, head_a // 6),), width=1)
    return layer.filter(ImageFilter.GaussianBlur(1.4))


def arrow_line(img: Image.Image, book) -> Image.Image:
    """The signature device: the bone dorsal stripe → loosed-arrow arrowhead, edge to edge.

    The stripe enters from the left as a clean bone line, passes THROUGH the struck node
    (a small filled gold key-node), and resolves on the right into a slim arrowhead.
    """
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    y = ARROW_Y

    # soft underglow in the book's accent (the line is 'hot' where it has been struck)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.line([(60, y), (W - 60, y)], fill=book["accent"] + (90,), width=18)
    glow = glow.filter(ImageFilter.GaussianBlur(22))
    layer = Image.alpha_composite(layer, glow)
    d = ImageDraw.Draw(layer)

    x_left = 70
    head_tip = W - 70
    head_back = head_tip - 150
    head_half = 46

    # the bone stripe (slight taper toward the head — a line of flight, not a ruler)
    d.line([(x_left, y), (head_back, y)], fill=BONE, width=12)
    d.line([(x_left, y), (head_back, y)], fill=GOLD_BRIGHT + (60,), width=4)

    # the arrowhead (bone, gold-lit edge)
    d.polygon([(head_back - 6, y - head_half), (head_tip, y), (head_back - 6, y + head_half)],
              fill=BONE)
    d.line([(head_back - 6, y - head_half), (head_tip, y)], fill=GOLD_BRIGHT, width=3)
    d.line([(head_tip, y), (head_back - 6, y + head_half)], fill=lerp(BONE, BADGER_BLACK, 0.25), width=3)
    # fletching notches at the nock (left end)
    for off in (0, 16, 32):
        d.line([(x_left + off, y - 26), (x_left + off + 30, y)], fill=BONE_DIM, width=3)
        d.line([(x_left + off, y + 26), (x_left + off + 30, y)], fill=BONE_DIM, width=3)

    # the struck node — a filled gold 'key' bead where rings originate
    nr = 26
    d.ellipse([NODE_X - nr, y - nr, NODE_X + nr, y + nr], fill=book["accent_bright"])
    d.ellipse([NODE_X - nr, y - nr, NODE_X + nr, y + nr], outline=GOLD_BRIGHT, width=3)
    d.ellipse([NODE_X - 9, y - 9, NODE_X + 9, y + 9], fill=lerp(book["accent_bright"], (255, 255, 255), 0.4))

    out = Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")
    return out


def top_vignette(img: Image.Image) -> Image.Image:
    vig = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vd = ImageDraw.Draw(vig)
    vd.rectangle([0, 0, W, int(H * 0.30)], fill=(0, 0, 0, 90))
    vd.rectangle([0, int(H * 0.82), W, H], fill=(0, 0, 0, 70))
    vig = vig.filter(ImageFilter.GaussianBlur(80))
    return Image.alpha_composite(img.convert("RGBA"), vig).convert("RGB")


def lay_type(img: Image.Image, book) -> Image.Image:
    d = ImageDraw.Draw(img)
    midx = W // 2

    # series eyebrow + numeral (identical placement/faces on all three = the set's masthead)
    tracked(d, (midx, EYEBROW_Y), "THE AFRICAN GOLD TRILOGY",
            font(F_SERIES, 44), GOLD, tracking=12, center_w=True)
    tracked(d, (midx, NUM_Y), book["numeral"],
            font(F_NUM, 34, index=4), BONE_DIM, tracking=18, center_w=True)
    rw = int(W * 0.16)
    d.line([(midx - rw, int(H * 0.146)), (midx + rw, int(H * 0.146))], fill=GOLD, width=2)

    # big title — Optima Bold, gold-bright, seated above the arrow-line
    title = book["title"]
    size = 196 if len(title) <= 6 else (150 if len(title) <= 9 else 132)
    ft = font(F_TITLE, size, index=1)
    d.text((midx, TITLE_Y), title, font=ft, fill=GOLD_BRIGHT, anchor="mm")
    # faint accent shadow for depth
    d.text((midx + 3, TITLE_Y + 3), title, font=ft, fill=lerp(book["accent"], BADGER_BLACK, 0.5),
           anchor="mm")
    d.text((midx, TITLE_Y), title, font=ft, fill=GOLD_BRIGHT, anchor="mm")

    # tagline — Cochin italic, bone, just under the arrow-line
    d.text((midx, TAG_Y), book["tagline"], font=font(F_TAG, 50, index=2), fill=BONE, anchor="mm")

    # author + Press rule at the foot
    tracked(d, (midx, AUTHOR_Y), "ANDRIES J. GREYLING",
            font(F_SERIES, 46, index=2), GOLD, tracking=10, center_w=True)
    prw = int(W * 0.11)
    d.line([(midx - prw, int(H * 0.936)), (midx + prw, int(H * 0.936))], fill=BONE_DIM, width=1)
    tracked(d, (midx, PRESS_Y), "ARJUNA BADGER PRESS",
            font(F_SERIES, 26, index=2), BONE_DIM, tracking=8, center_w=True)
    return img


def render_one(book) -> Image.Image:
    img = render_field(book)
    img = Image.alpha_composite(img.convert("RGBA"), resonance_rings(book)).convert("RGB")
    img = arrow_line(img, book)
    img = top_vignette(img)
    img = lay_type(img, book)
    return img


def out_paths(book) -> list[Path]:
    bid = book["id"]
    bookdir = REPO / "books" / bid
    return [
        bookdir / "design" / "cover.png",
        bookdir / "design" / "cover.jpg",
        bookdir / "build" / "export" / "cover.png",
        bookdir / "build" / "export" / "cover.jpg",
        REPO / "covers" / f"{bid}.jpg",
    ]


def main() -> None:
    for book in BOOKS:
        img = render_one(book)
        for p in out_paths(book):
            p.parent.mkdir(parents=True, exist_ok=True)
            if p.suffix.lower() == ".jpg":
                img.save(p, "JPEG", quality=92)
            else:
                img.save(p, "PNG")
            print(f"wrote {p}")
    print("\nThe African Gold Trilogy — cover set rendered (3 books).")


if __name__ == "__main__":
    main()

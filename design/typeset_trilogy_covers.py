#!/usr/bin/env python3
"""The African Gold Trilogy — typeset the HOUSE NOVEL lockup onto generated cover art.

Pairs with design/TRILOGY_COVER_ART_PROMPTS.md. You generate the cinematic art (book1-africa tier);
this script drops the exact House lockup on top — the SAME typographic system the HBT novels use
(Copperplate gold eyebrow + gold rule, Optima-Bold gold-bright stacked title, Cochin-italic tagline,
Copperplate gold author, ARJUNA BADGER PRESS) — and exports the cover + catalog thumbnail.

Per book it expects the art at:   books/<id>/design/art.png   (or art.jpg)
Outputs (same paths as the rest of the catalog):
    books/<id>/design/cover.{png,jpg}
    books/<id>/build/export/cover.{png,jpg}
    covers/<id>.jpg

    python3 design/typeset_trilogy_covers.py            # all three (skips any with no art yet)
    python3 design/typeset_trilogy_covers.py relic      # just one

If a book has no art.png yet, it is SKIPPED with a note (so you can typeset as art arrives).
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

REPO = Path(__file__).resolve().parent.parent
W, H = 1800, 2700

# ── House palette (matches the HBT novel covers) ──────────────────────────────────────────────
GOLD        = (229, 181, 103)
GOLD_BRIGHT = (245, 220, 158)
CREAM       = (236, 230, 220)
BONE_DIM    = (196, 188, 172)
SHADOW      = (10, 10, 12)

# ── House faces (identical to books/.../the-jakobus-file/design/make_cover.py) ────────────────
F_TITLE  = "/System/Library/Fonts/Supplemental/Optima.ttc"        # idx 1 = Bold
F_SERIES = "/System/Library/Fonts/Supplemental/Copperplate.ttc"   # idx 2 = Bold (engraved eyebrow)
F_TAG    = "/System/Library/Fonts/Supplemental/Cochin.ttc"        # idx 2 = Italic (tagline)

BOOKS = {
    "resonance": {
        "numeral": "BOOK ONE",
        "title": ["RESONANCE"],
        "tagline": "Some minds were not born. They were tuned.",
    },
    "revelation": {
        "numeral": "BOOK TWO",
        "title": ["REVELATION"],
        "tagline": "Every sacred text was edited. She found the edits.",
    },
    "relic": {
        "numeral": "BOOK THREE",
        "title": ["RELIC"],
        "tagline": "The gold was never the treasure. It was the key.",
    },
}


def font(path: str, size: int, index: int = 0) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size, index=index)


def tracked(draw, xy, text, fnt, fill, tracking=0, center_w=False):
    widths = [draw.textbbox((0, 0), ch, font=fnt)[2] for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = xy[0] - total // 2 if center_w else xy[0]
    y = xy[1]
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + tracking


def find_art(bid: str) -> Path | None:
    d = REPO / "books" / bid / "design"
    for name in ("art.png", "art.jpg", "art.jpeg"):
        p = d / name
        if p.exists():
            return p
    return None


def fit_cover(art: Image.Image) -> Image.Image:
    """Cover-crop the art to exactly W×H (no distortion)."""
    art = ImageOps.exif_transpose(art).convert("RGB")
    aw, ah = art.size
    scale = max(W / aw, H / ah)
    nw, nh = int(aw * scale + 0.5), int(ah * scale + 0.5)
    art = art.resize((nw, nh), Image.LANCZOS)
    x0 = (nw - W) // 2
    y0 = (nh - H) // 2
    return art.crop((x0, y0, x0 + W, y0 + H))


def darken_bands(img: Image.Image) -> Image.Image:
    """Deepen the TOP (for the eyebrow) and BOTTOM (for the title block + author) so gold type
    always reads, whatever the art does there. A soft gradient scrim, house-consistent."""
    scrim = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(scrim)
    # top band
    top_h = int(H * 0.20)
    for y in range(top_h):
        a = int(150 * (1 - y / top_h) ** 1.4)
        d.line([(0, y), (W, y)], fill=a)
    # bottom band (stronger — the title lives here)
    bot_start = int(H * 0.52)
    for y in range(bot_start, H):
        t = (y - bot_start) / (H - bot_start)
        a = int(205 * (t ** 1.25))
        d.line([(0, y), (W, y)], fill=a)
    scrim = scrim.filter(ImageFilter.GaussianBlur(8))
    black = Image.new("RGB", (W, H), SHADOW)
    return Image.composite(black, img, scrim)


def shadowed_text(d, xy, text, fnt, fill, anchor="mm", shadow=SHADOW, off=3):
    d.text((xy[0] + off, xy[1] + off), text, font=fnt, fill=shadow, anchor=anchor)
    d.text(xy, text, font=fnt, fill=fill, anchor=anchor)


def lay_type(img: Image.Image, book) -> Image.Image:
    d = ImageDraw.Draw(img)
    midx = W // 2

    # ── series eyebrow + numeral (top) ──────────────────────────────────────────────────────────
    tracked(d, (midx - _tw(d, "THE AFRICAN GOLD TRILOGY", font(F_SERIES, 46), 12) // 2,
                int(H * 0.066)),
            "THE AFRICAN GOLD TRILOGY", font(F_SERIES, 46), GOLD, tracking=12)
    tracked(d, (midx - _tw(d, book["numeral"], font(F_SERIES, 32), 8) // 2, int(H * 0.103)),
            book["numeral"], font(F_SERIES, 32), CREAM, tracking=8)
    rw = int(W * 0.17)
    d.line([(midx - rw, int(H * 0.138)), (midx + rw, int(H * 0.138))], fill=GOLD, width=2)

    # ── title block (bottom third), Optima Bold gold-bright, stacked ────────────────────────────
    lines = book["title"]
    longest = max(lines, key=len)
    size = 224 if len(longest) <= 6 else (176 if len(longest) <= 9 else 150)
    ft = font(F_TITLE, size, index=1)
    # vertical anchor: title sits low, above the author
    block_h = len(lines) * int(size * 1.0)
    ty = int(H * 0.80) - block_h
    for ln in lines:
        shadowed_text(d, (midx, ty), ln, ft, GOLD_BRIGHT, anchor="mm", off=4)
        ty += int(size * 1.0)

    # short gold rule + tagline under the title
    trw = int(W * 0.20)
    ry = int(H * 0.815)
    d.line([(midx - trw, ry), (midx + trw, ry)], fill=GOLD, width=2)
    shadowed_text(d, (midx, int(H * 0.842)), book["tagline"], font(F_TAG, 50, index=2),
                  CREAM, anchor="mm", off=2)

    # ── author + Press (foot) ───────────────────────────────────────────────────────────────────
    tracked(d, (midx - _tw(d, "ANDRIES J. GREYLING", font(F_SERIES, 46), 10) // 2, int(H * 0.918)),
            "ANDRIES J. GREYLING", font(F_SERIES, 46), GOLD, tracking=10)
    tracked(d, (midx - _tw(d, "ARJUNA BADGER PRESS", font(F_SERIES, 26), 8) // 2, int(H * 0.950)),
            "ARJUNA BADGER PRESS", font(F_SERIES, 26), BONE_DIM, tracking=8)
    return img


def _tw(d, text, fnt, tracking) -> int:
    widths = [d.textbbox((0, 0), ch, font=fnt)[2] for ch in text]
    return sum(widths) + tracking * (len(text) - 1)


def out_paths(bid: str) -> list[Path]:
    bd = REPO / "books" / bid
    return [
        bd / "design" / "cover.png",
        bd / "design" / "cover.jpg",
        bd / "build" / "export" / "cover.png",
        bd / "build" / "export" / "cover.jpg",
        REPO / "covers" / f"{bid}.jpg",
    ]


def typeset_one(bid: str) -> bool:
    art_path = find_art(bid)
    if art_path is None:
        print(f"  SKIP {bid}: no art yet (drop it at books/{bid}/design/art.png — see "
              f"design/TRILOGY_COVER_ART_PROMPTS.md)")
        return False
    img = fit_cover(Image.open(art_path))
    img = darken_bands(img)
    img = lay_type(img, BOOKS[bid])
    for p in out_paths(bid):
        p.parent.mkdir(parents=True, exist_ok=True)
        img.save(p, "JPEG", quality=92) if p.suffix.lower() == ".jpg" else img.save(p, "PNG")
    print(f"  OK   {bid}: typeset from {art_path.name} -> cover.{{png,jpg}} + covers/{bid}.jpg")
    return True


def main() -> None:
    which = [a for a in sys.argv[1:] if a in BOOKS] or list(BOOKS)
    print("Typesetting the African Gold Trilogy (house novel lockup):")
    done = sum(typeset_one(b) for b in which)
    if not done:
        print("\nNo art found yet. Generate the 3 images (design/TRILOGY_COVER_ART_PROMPTS.md), "
              "save each as books/<id>/design/art.png, then re-run.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Lay the title + author typography onto the clean cover plate for *The Metal Man*.

Reads design/cover-plate.png (the bending-teaspoon / Tel Aviv garden plate — text-free),
upscales to house size, adds legibility scrims and house serif type, and writes the typeset
cover to design/cover.{png,jpg} + build/export/cover.{png,jpg}. Same house method as
Henry Sugar / The Jakobus File.

Eyebrow = "A GOSPEL-BIOGRAPHY"; Bone-white title ink against the warm amber plate; Veld Ochre
accent (the metal's memory, the honey-badger nerve).

    python3 design/make_cover.py
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
BOOK = HERE.parent
PLATE = HERE / "cover-plate.png"
W, H = 1800, 2700
OUT = [
    HERE / "cover.png",
    HERE / "cover.jpg",
    BOOK / "build" / "export" / "cover.png",
    BOOK / "build" / "export" / "cover.jpg",
]

INK = (237, 233, 224, 255)        # Bone Stripe — title ink
GOLD = (200, 168, 107, 255)       # Veld Dust — eyebrow / tagline accent
SHADOW = (12, 10, 6, 210)


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
COPPER = ATK_REG


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


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


def main() -> None:
    plate = Image.open(PLATE).convert("RGBA")
    # Upscale/center-crop the plate to house 1800x2700 (6x9in @ 300dpi).
    src_ratio = plate.width / plate.height
    dst_ratio = W / H
    if src_ratio > dst_ratio:
        new_h = H
        new_w = int(H * src_ratio)
    else:
        new_w = W
        new_h = int(W / src_ratio)
    plate = plate.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - W) // 2
    top = (new_h - H) // 2
    img = plate.crop((left, top, left + W, top + H))

    W_, H_ = img.size
    cx = W_ / 2

    scrim = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrim)
    top_end = int(H_ * 0.40)
    for y in range(top_end):
        a = int(170 * (1 - y / top_end) ** 1.4)
        sd.line([(0, y), (W_, y)], fill=(10, 8, 6, a))
    bot_start = int(H_ * 0.84)
    for y in range(bot_start, H_):
        a = int(160 * ((y - bot_start) / (H_ - bot_start)) ** 1.3)
        sd.line([(0, y), (W_, y)], fill=(8, 6, 4, a))
    img = Image.alpha_composite(img, scrim)

    draw = ImageDraw.Draw(img)

    f_eyebrow = font(COPPER, 30)
    draw_tracked(draw, cx, int(H_ * 0.058), "A GOSPEL-BIOGRAPHY", f_eyebrow, 7, GOLD)

    rule_y = int(H_ * 0.058) + 48
    rw = 150
    draw.line([(cx - rw, rule_y), (cx + rw, rule_y)], fill=GOLD, width=2)

    f_title = font(DIDOT, 138)
    lines = ["THE", "METAL", "MAN"]
    ty = int(H_ * 0.115)
    lh = 150
    for i, ln in enumerate(lines):
        draw_tracked(draw, cx, ty + i * lh, ln, f_title, 6, INK)

    f_tag = font(ATK_ITAL, 38)
    draw_tracked(draw, cx, ty + 3 * lh + 14, "the spoon was the smallest thing he was ever asked to bend",
                 f_tag, 1, GOLD)

    f_auth = font(COPPER, 46)
    draw_tracked(draw, cx, int(H_ * 0.93), "ANDRIES J. GREYLING", f_auth, 7, INK)

    out = img.convert("RGB")
    for p in OUT:
        p.parent.mkdir(parents=True, exist_ok=True)
        if p.suffix.lower() == ".jpg":
            out.save(p, "JPEG", quality=92)
        else:
            out.save(p, "PNG")
        print(f"wrote {p} ({p.stat().st_size} bytes)")


if __name__ == "__main__":
    main()

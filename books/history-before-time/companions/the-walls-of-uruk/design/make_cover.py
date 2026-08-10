#!/usr/bin/env python3
"""Lay the HBT title typography onto the cinematic cover plate for *The Walls of Uruk*.

Reads design/cover-plate.png (the text-free king-on-the-rampart matte painting), adds soft
top/bottom legibility scrims and the house typography (title / eyebrow + author), and writes
the typeset cover to design/cover.{png,jpg} + build/export/. Same house method as
The Wrath of Achilles / The Jakobus File. Re-runnable: always works from the plate.

    python3 design/make_cover.py
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
BOOK = HERE.parent
PLATE = HERE / "cover-plate.png"
OUT = [
    HERE / "cover.png", HERE / "cover.jpg",
    BOOK / "build" / "export" / "cover.png", BOOK / "build" / "export" / "cover.jpg",
]

W, H = 1600, 2400

INK = (244, 236, 221, 255)
OCHRE = (222, 178, 116, 255)
DIM = (218, 204, 182, 255)
SHADOW = (14, 9, 5, 220)


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


def main() -> None:
    img = Image.open(PLATE).convert("RGBA").resize((W, H), Image.LANCZOS)
    cx = W / 2

    # legibility scrims — the plate's sky is a bright dawn gradient, so the top band is deeper
    # than the Achilles cover's; the bottom band stays light to keep the king and brick readable.
    scrim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrim)
    top_end = int(H * 0.40)
    for y in range(top_end):
        a = int(200 * (1 - y / top_end) ** 1.25)
        sd.line([(0, y), (W, y)], fill=(20, 14, 26, a))
    bot_start = int(H * 0.86)
    for y in range(bot_start, H):
        a = int(165 * ((y - bot_start) / (H - bot_start)) ** 1.25)
        sd.line([(0, y), (W, y)], fill=(16, 10, 7, a))
    img = Image.alpha_composite(img, scrim)

    draw = ImageDraw.Draw(img)

    draw_tracked(draw, cx, int(H * 0.050), "HISTORY BEFORE TIME", font(COCHIN, 50), 13, INK)

    tag, f_tag = "COMPANIONS", font(COCHIN, 34)
    draw_tracked(draw, cx, int(H * 0.086), tag, f_tag, 11, OCHRE)
    tw = text_width(draw, tag, f_tag, 11)
    dy = int(H * 0.086) + 22
    for sx in (cx - tw / 2 - 44, cx + tw / 2 + 44):
        draw.ellipse([sx - 4, dy - 4, sx + 4, dy + 4], fill=OCHRE)

    rule_y = int(H * 0.120)
    draw.line([(cx - 210, rule_y), (cx + 210, rule_y)], fill=INK, width=3)

    lines = [("THE WALLS", 158), ("OF URUK", 158)]
    ty = int(H * 0.142)
    lh = 176
    for i, (ln, sz) in enumerate(lines):
        draw_tracked(draw, cx, ty + i * lh, ln, font(DIDOT, sz), 4, INK)

    f_sub = font(ATK_ITAL, 52)
    sub = "The Epic of Gilgamesh, plainly told"
    sub_y = ty + 2 * lh + 30
    sub_w = text_width(draw, sub, f_sub, 1)
    band = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(band)
    bd.rounded_rectangle(
        [cx - sub_w / 2 - 70, sub_y - 18, cx + sub_w / 2 + 70, sub_y + 74],
        radius=30, fill=(18, 12, 16, 120),
    )
    band = band.filter(ImageFilter.GaussianBlur(22))
    img = Image.alpha_composite(img, band)
    draw = ImageDraw.Draw(img)
    draw_tracked(draw, cx, sub_y, sub, f_sub, 1, DIM)

    draw_tracked(draw, cx, int(H * 0.936), "ANDRIES J. GREYLING", font(COCHIN, 60), 9, INK)

    out = img.convert("RGB")
    for p in OUT:
        p.parent.mkdir(parents=True, exist_ok=True)
        if p.suffix.lower() == ".jpg":
            out.save(p, "JPEG", quality=92)
        else:
            out.save(p, "PNG")
        print(f"wrote {p}  ({p.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()

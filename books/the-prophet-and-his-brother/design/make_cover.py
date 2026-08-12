#!/usr/bin/env python3
"""Typeset *The Prophet and his Brother* cover from design/cover-plate.png.

Eyebrow + title + author on river/Mutatus plate. Writes design/cover.{png,jpg}
and build/export/cover.{png,jpg}.

    python3 design/make_cover.py
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
BOOK = HERE.parent
PLATE = HERE / "cover-plate.png"
OUT = [
    HERE / "cover.png",
    HERE / "cover.jpg",
    BOOK / "build" / "export" / "cover.png",
    BOOK / "build" / "export" / "cover.jpg",
]

# Bone title on dark dawn scrim; river-amber accent
INK = (236, 232, 220, 255)
ACCENT = (196, 148, 74, 255)
SHADOW = (8, 14, 12, 220)


def _repo() -> Path:
    p = Path(__file__).resolve()
    for cand in p.parents:
        if (cand / "assets" / "fonts" / "AtkinsonHyperlegible-Bold.otf").is_file():
            return cand
    raise SystemExit("make_cover: cannot find repo assets/fonts/")


_ATK = _repo() / "assets" / "fonts"
ATK_REG = str(_ATK / "AtkinsonHyperlegible-Regular.otf")
ATK_BOLD = str(_ATK / "AtkinsonHyperlegible-Bold.otf")
ATK_ITAL = str(_ATK / "AtkinsonHyperlegible-Italic.otf")


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
    img = Image.open(PLATE).convert("RGBA")
    W, H = img.size
    cx = W / 2

    # Heavy top scrim kills any residual plate text; bottom for author.
    scrim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrim)
    top_end = int(H * 0.48)
    for y in range(top_end):
        a = int(200 * (1 - y / top_end) ** 1.25)
        sd.line([(0, y), (W, y)], fill=(6, 14, 12, a))
    bot_start = int(H * 0.86)
    for y in range(bot_start, H):
        a = int(170 * ((y - bot_start) / max(1, H - bot_start)) ** 1.2)
        sd.line([(0, y), (W, y)], fill=(4, 10, 8, a))
    img = Image.alpha_composite(img, scrim)
    draw = ImageDraw.Draw(img)

    f_eyebrow = font(ATK_REG, 28)
    draw_tracked(draw, cx, int(H * 0.05), "AFRICAN GOLD · COMPANION 3.5", f_eyebrow, 5, ACCENT)

    rule_y = int(H * 0.05) + 44
    draw.line([(cx - 140, rule_y), (cx + 140, rule_y)], fill=ACCENT, width=2)

    f_title = font(ATK_BOLD, 72)
    lines = ["THE PROPHET", "AND HIS", "BROTHER"]
    ty = int(H * 0.12)
    lh = 86
    for i, ln in enumerate(lines):
        draw_tracked(draw, cx, ty + i * lh, ln, f_title, 4, INK)

    f_tag = font(ATK_ITAL, 30)
    draw_tracked(
        draw,
        cx,
        ty + len(lines) * lh + 18,
        "custody of meaning after the meters agree",
        f_tag,
        1,
        ACCENT,
    )

    f_auth = font(ATK_REG, 40)
    draw_tracked(draw, cx, int(H * 0.925), "ANDRIES J. GREYLING", f_auth, 6, INK)

    out = img.convert("RGB")
    for p in OUT:
        p.parent.mkdir(parents=True, exist_ok=True)
        if p.suffix.lower() == ".jpg":
            out.save(p, "JPEG", quality=92)
        else:
            out.save(p, "PNG")
        print(f"wrote {p}")


if __name__ == "__main__":
    main()

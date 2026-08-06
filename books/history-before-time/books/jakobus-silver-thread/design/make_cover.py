#!/usr/bin/env python3
"""Lay the title + author typography onto the clean cover plate for *The Silver Thread*.

Reads design/cover-plate.png (the text-free image), adds soft legibility scrims and elegant
serif typography, and writes the typeset cover to design/cover.png + build/export/cover.png.
Re-runnable: always works from the plate, never from an already-typeset file.
"""
from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
PLATE = HERE / "cover-plate.png"
OUT = [HERE / "cover.png", HERE.parent / "build" / "export" / "cover.png"]

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


INK = (244, 234, 217, 255)        # warm off-white
SHADOW = (20, 12, 6, 200)         # warm near-black

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
    """Draw letter-spaced text centred on cx at baseline-top y."""
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

    # --- legibility scrims (subtle; preserve the photo) ---
    scrim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrim)
    top_end = int(H * 0.40)
    for y in range(top_end):
        a = int(165 * (1 - y / top_end) ** 1.4)
        sd.line([(0, y), (W, y)], fill=(28, 18, 10, a))
    bot_start = int(H * 0.84)
    for y in range(bot_start, H):
        a = int(150 * ((y - bot_start) / (H - bot_start)) ** 1.3)
        sd.line([(0, y), (W, y)], fill=(22, 13, 7, a))
    img = Image.alpha_composite(img, scrim)

    draw = ImageDraw.Draw(img)

    # --- series line ---
    f_series = font(COCHIN, 33)
    draw_tracked(draw, cx, int(H * 0.052), "HISTORY BEFORE TIME", f_series, 9, INK)

    # thin rule under the series line
    rule_y = int(H * 0.052) + 52
    rw = 150
    draw.line([(cx - rw, rule_y), (cx + rw, rule_y)], fill=INK, width=2)

    # --- title, stacked ---
    f_title = font(DIDOT, 132)
    lines = ["THE", "SILVER", "THREAD"]
    ty = int(H * 0.105)
    lh = 142
    for i, ln in enumerate(lines):
        draw_tracked(draw, cx, ty + i * lh, ln, f_title, 6, INK)

    # --- subtitle ---
    f_sub = font(ATK_ITAL, 40)  # italic face
    draw_tracked(draw, cx, ty + 3 * lh + 14, "the Jakobus origin", f_sub, 2, INK)

    # --- author at the foot ---
    f_auth = font(COCHIN, 44)
    draw_tracked(draw, cx, int(H * 0.93), "ANDRIES J. GREYLING", f_auth, 7, INK)

    out = img.convert("RGB")
    for p in OUT:
        p.parent.mkdir(parents=True, exist_ok=True)
        out.save(p, "PNG")
        print(f"wrote {p}")


if __name__ == "__main__":
    main()

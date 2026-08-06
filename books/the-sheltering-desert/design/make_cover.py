#!/usr/bin/env python3
"""Lay the title + author typography onto the clean cover plate for *The Indifferent Desert*.

Reads design/cover-plate.png (the text-free Namib image, portrait 2:3), adds soft legibility
scrims and elegant serif typography in the house style, and writes the typeset cover to
design/cover.png + design/cover.jpg + build/export/cover.png.
Re-runnable: always works from the plate, never from an already-typeset file.
"""
from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = Path(__file__).resolve().parent
PLATE = HERE / "cover-plate.png"
OUT_PNG = [HERE / "cover.png", HERE.parent / "build" / "export" / "cover.png"]
OUT_JPG = HERE / "cover.jpg"

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


INK = (247, 239, 225, 255)        # warm off-white
SHADOW = (10, 6, 3, 235)          # warm near-black, near-opaque for punch

DIDOT = ATK_BOLD
COCHIN = ATK_REG
def font(path: str, size: int, index: int = 0) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size, index=index)


def text_width(draw, s, fnt, tracking):
    w = 0
    for ch in s:
        w += draw.textlength(ch, font=fnt) + tracking
    return w - tracking if s else 0


def _place_glyphs(d, cx, y, s, fnt, tracking, fill, dx=0, dy=0):
    """Letter-space string s centred on cx, drawn into draw-context d with optional offset."""
    total = text_width(d, s, fnt, tracking)
    x = cx - total / 2
    for ch in s:
        d.text((x + dx, y + dy), ch, font=fnt, fill=fill)
        x += d.textlength(ch, font=fnt) + tracking


def draw_tracked(img, cx, y, s, fnt, tracking, fill, shadow=True, glow=6):
    """Draw letter-spaced text centred on cx at baseline-top y, onto RGBA image `img`.

    A blurred dark copy is laid down first as a soft glow/shadow (so the thin Didot
    strokes hold up over the bright sky and busy rock), then the crisp ink on top.
    Returns the composited image.
    """
    if shadow:
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        _place_glyphs(ld, cx, y, s, fnt, tracking, SHADOW, dx=2, dy=3)
        layer = layer.filter(ImageFilter.GaussianBlur(glow))
        # darken twice so the soft halo reads as a real shadow, not a faint smudge
        img = Image.alpha_composite(img, layer)
        img = Image.alpha_composite(img, layer)
    top = Image.new("RGBA", img.size, (0, 0, 0, 0))
    td = ImageDraw.Draw(top)
    _place_glyphs(td, cx, y, s, fnt, tracking, fill)
    return Image.alpha_composite(img, top)


def main() -> None:
    img = Image.open(PLATE).convert("RGBA")
    W, H = img.size
    cx = W / 2

    # --- legibility scrims. The title sits in the upper sky, so darken the top band
    #     firmly; a stronger foot scrim seats the author over the busy rock. Deeper and
    #     reaching a little further down than before, to carry the larger type. ---
    scrim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrim)
    top_end = int(H * 0.62)
    for y in range(top_end):
        a = int(205 * (1 - y / top_end) ** 1.35)
        sd.line([(0, y), (W, y)], fill=(12, 20, 36, a))   # cool, matches the sky
    bot_start = int(H * 0.82)
    for y in range(bot_start, H):
        a = int(205 * ((y - bot_start) / (H - bot_start)) ** 1.25)
        sd.line([(0, y), (W, y)], fill=(18, 11, 6, a))
    img = Image.alpha_composite(img, scrim)

    # --- eyebrow ---
    f_eyebrow = font(COCHIN, 44)
    img = draw_tracked(img, cx, int(H * 0.058), "A TRUE STORY", f_eyebrow, 13, INK)

    rule_y = int(H * 0.058) + 70
    rw = 165
    rd = ImageDraw.Draw(img)
    rd.line([(cx - rw, rule_y), (cx + rw, rule_y)], fill=INK, width=3)

    # --- title, stacked (THE / INDIFFERENT / DESERT) ---
    ty = int(H * 0.105)
    f_the = font(DIDOT, 118)
    img = draw_tracked(img, cx, ty, "THE", f_the, 14, INK)
    f_title = font(DIDOT, 168)
    img = draw_tracked(img, cx, ty + 146, "INDIFFERENT", f_title, 4, INK)
    img = draw_tracked(img, cx, ty + 146 + 190, "DESERT", f_title, 13, INK)

    # --- subtitle: the evocative line, then the two real men it is about ---
    sub_y = ty + 146 + 190 + 210
    f_sub = font(ATK_ITAL, 54)  # italic face
    img = draw_tracked(img, cx, sub_y, "the Namib, and the war they hid from", f_sub, 1, INK)
    f_names = font(COCHIN, 48)
    img = draw_tracked(img, cx, sub_y + 88, "HENNO MARTIN  &  HERMANN KORN", f_names, 7, INK)

    # --- author at the foot ---
    f_auth = font(COCHIN, 60)
    img = draw_tracked(img, cx, int(H * 0.925), "ANDRIES J. GREYLING", f_auth, 9, INK)

    out = img.convert("RGB")
    for p in OUT_PNG:
        p.parent.mkdir(parents=True, exist_ok=True)
        out.save(p, "PNG")
        print(f"wrote {p}")
    out.save(OUT_JPG, "JPEG", quality=90)
    print(f"wrote {OUT_JPG}")


if __name__ == "__main__":
    main()

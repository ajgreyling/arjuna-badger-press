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

INK = (244, 234, 217, 255)        # warm off-white
SHADOW = (16, 10, 5, 205)         # warm near-black

DIDOT = "/System/Library/Fonts/Supplemental/Didot.ttc"
COCHIN = "/System/Library/Fonts/Supplemental/Cochin.ttc"


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

    # --- legibility scrims (subtle; preserve the photo). The title sits in the upper sky,
    #     so darken the top band more; a light foot scrim seats the author over the rock. ---
    scrim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrim)
    top_end = int(H * 0.52)
    for y in range(top_end):
        a = int(150 * (1 - y / top_end) ** 1.5)
        sd.line([(0, y), (W, y)], fill=(14, 22, 38, a))   # cool, matches the sky
    bot_start = int(H * 0.86)
    for y in range(bot_start, H):
        a = int(160 * ((y - bot_start) / (H - bot_start)) ** 1.3)
        sd.line([(0, y), (W, y)], fill=(20, 12, 7, a))
    img = Image.alpha_composite(img, scrim)

    draw = ImageDraw.Draw(img)

    # --- eyebrow ---
    f_eyebrow = font(COCHIN, 34)
    draw_tracked(draw, cx, int(H * 0.060), "A TRUE STORY", f_eyebrow, 10, INK)

    rule_y = int(H * 0.060) + 54
    rw = 130
    draw.line([(cx - rw, rule_y), (cx + rw, rule_y)], fill=INK, width=2)

    # --- title, stacked (THE / INDIFFERENT / DESERT) ---
    ty = int(H * 0.100)
    f_the = font(DIDOT, 88)
    draw_tracked(draw, cx, ty, "THE", f_the, 10, INK)
    f_title = font(DIDOT, 118)
    draw_tracked(draw, cx, ty + 108, "INDIFFERENT", f_title, 3, INK)
    draw_tracked(draw, cx, ty + 108 + 134, "DESERT", f_title, 9, INK)

    # --- subtitle (short, dignified; the full true-story line lives on the card/title page) ---
    f_sub = font(DIDOT, 42, index=1)  # italic face
    draw_tracked(draw, cx, ty + 108 + 134 + 150,
                 "two men, the Namib, and the war they hid from", f_sub, 1, INK)

    # --- author at the foot ---
    f_auth = font(COCHIN, 46)
    draw_tracked(draw, cx, int(H * 0.93), "ANDRIES J. GREYLING", f_auth, 8, INK)

    out = img.convert("RGB")
    for p in OUT_PNG:
        p.parent.mkdir(parents=True, exist_ok=True)
        out.save(p, "PNG")
        print(f"wrote {p}")
    out.save(OUT_JPG, "JPEG", quality=90)
    print(f"wrote {OUT_JPG}")


if __name__ == "__main__":
    main()

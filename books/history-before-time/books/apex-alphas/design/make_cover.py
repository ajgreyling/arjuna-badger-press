#!/usr/bin/env python3
"""Typeset *Apex Alphas* — bold sans, not HBT house Didot/gold.

Digital-only cover: keeps landscape plate (full motley crew — ballerina, throne, etc.).
Portrait plates still supported if width < height.

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

INK = (28, 32, 42, 255)
ORANGE = (255, 98, 28, 255)
DIM = (72, 76, 86, 255)
SHADOW = (255, 255, 255, 120)

HELV = "/System/Library/Fonts/Helvetica.ttc"
HELV_NEUE = "/System/Library/Fonts/HelveticaNeue.ttc"
IMPACT = "/System/Library/Fonts/Supplemental/Impact.ttf"


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
            draw.text((x + 3, y + 4), ch, font=fnt, fill=SHADOW)
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking


def sky_scrim(W: int, H: int, *, top_frac: float, bot_frac: float) -> Image.Image:
    scrim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrim)
    top_end = int(H * top_frac)
    for y in range(top_end):
        a = int(175 * (1 - y / top_end) ** 1.05)
        sd.line([(0, y), (W, y)], fill=(248, 246, 242, a))
    bot_start = int(H * (1 - bot_frac))
    for y in range(bot_start, H):
        a = int(160 * ((y - bot_start) / (H - bot_start)) ** 1.1)
        sd.line([(0, y), (W, y)], fill=(248, 246, 242, a))
    return scrim


def typeset_landscape(img: Image.Image) -> Image.Image:
    W, H = img.size
    cx = W / 2
    scale = W / 2400
    img = Image.alpha_composite(img, sky_scrim(W, H, top_frac=0.28, bot_frac=0.10))
    draw = ImageDraw.Draw(img)

    f_eyebrow = font(HELV_NEUE, int(26 * scale), index=1)
    draw_tracked(draw, cx, int(H * 0.04), "A NOVEL", f_eyebrow, 12, DIM, shadow=False)

    rule_y = int(H * 0.075)
    draw.line([(cx - int(W * 0.12), rule_y), (cx + int(W * 0.12), rule_y)], fill=ORANGE, width=max(3, int(4 * scale)))

    f_title = font(IMPACT, int(112 * scale))
    draw_tracked(draw, cx, int(H * 0.09), "APEX ALPHAS", f_title, 8, INK, shadow=True)

    f_tag = font(HELV_NEUE, int(32 * scale), index=1)
    draw_tracked(draw, cx, int(H * 0.20), "Every mastery is the same climb.", f_tag, 2, DIM, shadow=False)

    f_auth = font(HELV, int(30 * scale))
    draw_tracked(draw, cx, int(H * 0.93), "ANDRIES J. GREYLING", f_auth, 8, INK, shadow=False)

    f_press = font(HELV_NEUE, int(20 * scale), index=1)
    draw_tracked(draw, cx, int(H * 0.965), "ARJUNA BADGER PRESS", f_press, 10, DIM, shadow=False)
    return img


def typeset_portrait(img: Image.Image) -> Image.Image:
    W, H = img.size
    cx = W / 2
    img = Image.alpha_composite(img, sky_scrim(W, H, top_frac=0.36, bot_frac=0.10))
    draw = ImageDraw.Draw(img)

    f_eyebrow = font(HELV_NEUE, 28, index=1)
    draw_tracked(draw, cx, int(H * 0.055), "A NOVEL", f_eyebrow, 14, DIM, shadow=False)

    rule_y = int(H * 0.085)
    rw = int(W * 0.18)
    draw.line([(cx - rw, rule_y), (cx + rw, rule_y)], fill=ORANGE, width=4)

    f_title = font(IMPACT, 148)
    draw_tracked(draw, cx, int(H * 0.10), "APEX", f_title, 6, INK, shadow=True)
    draw_tracked(draw, cx, int(H * 0.22), "ALPHAS", f_title, 6, INK, shadow=True)

    f_tag = font(HELV_NEUE, 36, index=1)
    draw_tracked(draw, cx, int(H * 0.345), "Every mastery is the same climb.", f_tag, 2, DIM, shadow=False)

    f_auth = font(HELV, 34)
    draw_tracked(draw, cx, int(H * 0.945), "ANDRIES J. GREYLING", f_auth, 8, INK, shadow=False)

    f_press = font(HELV_NEUE, 22, index=1)
    draw_tracked(draw, cx, int(H * 0.975), "ARJUNA BADGER PRESS", f_press, 10, DIM, shadow=False)
    return img


def main() -> None:
    if not PLATE.is_file():
        raise SystemExit(f"missing {PLATE}")

    img = Image.open(PLATE).convert("RGBA")
    W, H = img.size
    if W >= H:
        img = typeset_landscape(img)
        print(f"[cover] landscape {W}×{H}")
    else:
        img = typeset_portrait(img)
        print(f"[cover] portrait {W}×{H}")

    out = img.convert("RGB")
    for p in OUT:
        p.parent.mkdir(parents=True, exist_ok=True)
        if p.suffix.lower() == ".jpg":
            out.save(p, "JPEG", quality=94, subsampling=0)
        else:
            out.save(p, "PNG")
        print(f"wrote {p}")


if __name__ == "__main__":
    main()

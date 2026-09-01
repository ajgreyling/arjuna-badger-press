#!/usr/bin/env python3
"""Lay title + author typography onto the clean cover plate for *The Man Who Drew the Universe*.

    python3 books/richard-feynman/design/make_cover.py
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

HERE = Path(__file__).resolve().parent
BOOK = HERE.parent
PLATE = HERE / "cover-plate.png"
OUT_PNG = [HERE / "cover.png", BOOK / "build" / "export" / "cover.png"]
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


W, H = 1800, 2700
INK = (247, 218, 149, 255)       # chalk-amber
SHADOW = (10, 8, 4, 235)


def font(path: str, size: int, index: int = 0) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size, index=index)


def text_width(draw, s, fnt, tracking):
    w = 0
    for ch in s:
        w += draw.textlength(ch, font=fnt) + tracking
    return w - tracking if s else 0


def _place_glyphs(d, cx, y, s, fnt, tracking, fill, dx=0, dy=0):
    total = text_width(d, s, fnt, tracking)
    x = cx - total / 2
    for ch in s:
        d.text((x + dx, y + dy), ch, font=fnt, fill=fill)
        x += d.textlength(ch, font=fnt) + tracking


def draw_tracked(img, cx, y, s, fnt, tracking, fill, shadow=True, glow=5):
    if shadow:
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        _place_glyphs(ld, cx, y, s, fnt, tracking, SHADOW, dx=2, dy=3)
        layer = layer.filter(ImageFilter.GaussianBlur(glow))
        img = Image.alpha_composite(img, layer)
        img = Image.alpha_composite(img, layer)
    top = Image.new("RGBA", img.size, (0, 0, 0, 0))
    td = ImageDraw.Draw(top)
    _place_glyphs(td, cx, y, s, fnt, tracking, fill)
    return Image.alpha_composite(img, top)


def fit_plate(plate: Image.Image) -> Image.Image:
    art = ImageOps.exif_transpose(plate).convert("RGB")
    aw, ah = art.size
    scale = max(W / aw, H / ah)
    nw, nh = int(aw * scale + 0.5), int(ah * scale + 0.5)
    art = art.resize((nw, nh), Image.Resampling.LANCZOS)
    x0 = (nw - W) // 2
    y0 = (nh - H) // 2
    return art.crop((x0, y0, x0 + W, y0 + H))


def main() -> None:
    if not PLATE.is_file():
        raise SystemExit(f"missing plate: {PLATE}")

    img = fit_plate(Image.open(PLATE)).convert("RGBA")
    cx = W / 2

    # Darken edges so amber type holds over the lit chalkboard/starfield.
    scrim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrim)
    top_end = int(H * 0.28)
    for y in range(top_end):
        a = int(170 * (1 - y / top_end) ** 1.25)
        sd.line([(0, y), (W, y)], fill=(8, 6, 4, a))
    bot_start = int(H * 0.76)
    for y in range(bot_start, H):
        a = int(205 * ((y - bot_start) / (H - bot_start)) ** 1.15)
        sd.line([(0, y), (W, y)], fill=(6, 5, 3, a))
    img = Image.alpha_composite(img, scrim)

    f_eyebrow = font(ATK_REG, 36)
    img = draw_tracked(img, cx, int(H * 0.048), "A LIFE IN CURIOSITY AND PHYSICS", f_eyebrow, 7, INK)

    rule_y = int(H * 0.048) + 54
    rd = ImageDraw.Draw(img)
    rd.line([(cx - 170, rule_y), (cx + 170, rule_y)], fill=INK, width=2)

    f_title = font(ATK_BOLD, 108)
    ty = int(H * 0.85)
    img = draw_tracked(img, cx, ty, "THE MAN WHO DREW", f_title, 6, INK)
    img = draw_tracked(img, cx, ty + 130, "THE UNIVERSE", f_title, 6, INK)

    f_auth = font(ATK_REG, 54)
    img = draw_tracked(img, cx, int(H * 0.945), "ANDRIES J. GREYLING", f_auth, 9, INK)

    out = img.convert("RGB")
    for p in OUT_PNG:
        p.parent.mkdir(parents=True, exist_ok=True)
        out.save(p, "PNG")
        print(f"wrote {p}")
    out.save(OUT_JPG, "JPEG", quality=92)
    print(f"wrote {OUT_JPG}")


if __name__ == "__main__":
    main()

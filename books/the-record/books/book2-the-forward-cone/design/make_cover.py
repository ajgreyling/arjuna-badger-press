#!/usr/bin/env python3
"""Compose the final cover for ONE RECORD, Book II: *The Forward Cone*."""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps


HERE = Path(__file__).resolve().parent
BOOK = HERE.parent
PLATE = HERE / "cover-plate.png"
OUT_PNG = (HERE / "cover.png", BOOK / "build" / "export" / "cover.png")
OUT_JPG = HERE / "cover.jpg"


def repo_root() -> Path:
    for candidate in Path(__file__).resolve().parents:
        if (candidate / "assets" / "fonts" / "AtkinsonHyperlegible-Bold.otf").is_file():
            return candidate
    raise SystemExit("make_cover: cannot find the repository font assets")


REPO = repo_root()
sys.path.insert(0, str(REPO))
from brand.cover_imprint import apply_imprint  # noqa: E402

FONTS = REPO / "assets" / "fonts"
ATK_REG = str(FONTS / "AtkinsonHyperlegible-Regular.otf")
ATK_BOLD = str(FONTS / "AtkinsonHyperlegible-Bold.otf")

W, H = 1800, 2700
INK = (234, 214, 166, 255)
SHADOW = (2, 5, 8, 245)


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def text_width(draw: ImageDraw.ImageDraw, text: str, face: ImageFont.FreeTypeFont, tracking: int) -> float:
    return sum(draw.textlength(ch, font=face) + tracking for ch in text) - (tracking if text else 0)


def place_glyphs(
    draw: ImageDraw.ImageDraw,
    cx: float,
    y: int,
    text: str,
    face: ImageFont.FreeTypeFont,
    tracking: int,
    fill: tuple[int, int, int, int],
    *,
    dx: int = 0,
    dy: int = 0,
) -> None:
    x = cx - text_width(draw, text, face, tracking) / 2
    for ch in text:
        draw.text((x + dx, y + dy), ch, font=face, fill=fill)
        x += draw.textlength(ch, font=face) + tracking


def draw_tracked(
    image: Image.Image,
    cx: float,
    y: int,
    text: str,
    face: ImageFont.FreeTypeFont,
    tracking: int,
    fill: tuple[int, int, int, int],
    *,
    glow: int = 6,
) -> Image.Image:
    shadow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    place_glyphs(ImageDraw.Draw(shadow), cx, y, text, face, tracking, SHADOW, dx=3, dy=4)
    shadow = shadow.filter(ImageFilter.GaussianBlur(glow))
    image = Image.alpha_composite(image, shadow)
    image = Image.alpha_composite(image, shadow)

    top = Image.new("RGBA", image.size, (0, 0, 0, 0))
    place_glyphs(ImageDraw.Draw(top), cx, y, text, face, tracking, fill)
    return Image.alpha_composite(image, top)


def fit_plate(plate: Image.Image) -> Image.Image:
    art = ImageOps.exif_transpose(plate).convert("RGB")
    scale = max(W / art.width, H / art.height)
    width, height = round(art.width * scale), round(art.height * scale)
    art = art.resize((width, height), Image.Resampling.LANCZOS)
    left, top = (width - W) // 2, (height - H) // 2
    return art.crop((left, top, left + W, top + H))


def main() -> None:
    if not PLATE.is_file():
        raise SystemExit(f"missing plate: {PLATE}")

    image = fit_plate(Image.open(PLATE)).convert("RGBA")
    cx = W / 2

    # Keep the plotting instrument legible while reserving quiet bands for exact typography.
    scrim = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(scrim)
    top_end = int(H * 0.27)
    for y in range(top_end):
        alpha = int(174 * (1 - y / top_end) ** 1.1)
        draw.line(((0, y), (W, y)), fill=(2, 7, 11, alpha))
    bottom_start = int(H * 0.85)
    for y in range(bottom_start, H):
        alpha = int(182 * ((y - bottom_start) / (H - bottom_start)) ** 1.1)
        draw.line(((0, y), (W, y)), fill=(2, 7, 11, alpha))
    image = Image.alpha_composite(image, scrim)

    eyebrow = font(ATK_REG, 42)
    image = draw_tracked(image, cx, 122, "ONE RECORD · BOOK II", eyebrow, 10, INK)
    rule = ImageDraw.Draw(image)
    rule.line(((cx - 175, 190), (cx + 175, 190)), fill=INK, width=2)

    title = font(ATK_BOLD, 124)
    image = draw_tracked(image, cx, 232, "THE FORWARD CONE", title, 7, INK, glow=8)

    author = font(ATK_REG, 55)
    image = draw_tracked(image, cx, 2482, "ANDRIES J. GREYLING", author, 9, INK)

    image = apply_imprint(image, anchor="tr", variant="gold", opacity=0.88)
    output = image.convert("RGB")
    for path in OUT_PNG:
        path.parent.mkdir(parents=True, exist_ok=True)
        output.save(path, "PNG", dpi=(300, 300))
        print(f"wrote {path}")
    output.save(OUT_JPG, "JPEG", quality=92, dpi=(300, 300))
    print(f"wrote {OUT_JPG}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Facebook cover: collage of the 7 History Before Time covers with Engineer of the Gods full-frame.

The seven full HBT novels (Calendar of Stone, Temple in the Rock ×2, Shore That Remembers,
Engineer of the Gods, Songlines of Stone) fanned across the right side of the banner, with
Engineer of the Gods rendered at a larger scale as the hero. Warm near-black house ground.

Writes the exact 851x315 cover plus a 2x master.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent
BRAND = HERE.parent
BOOKS = BRAND.parent / "books" / "history-before-time" / "books"

W, H = 851, 315
SCALE = 2
BG = (22, 21, 19)

# The six non-hero covers: Calendar of Stone, Temple in the Rock (India ×2), Shore That Remembers,
# Songlines of Stone. Ordered left to right in the fan (smallest to largest).
COVERS = [
    "book1-africa",           # Calendar of Stone
    "book2-india",            # Temple in the Rock
    "book3-india-deccan",     # Temple in the Rock (Deccan)
    "book4-india-tamil",      # Shore That Remembers
    "australia-outback",      # Songlines of Stone
]

# The hero: Engineer of the Gods (book5-egypt), rendered larger/fuller
HERO = BOOKS / "book5-egypt" / "design" / "cover.png"

out = HERE / "facebook-cover.png"
out_2x = HERE / "facebook-cover@2x.png"


def _cover_shadowed(path: Path, target_h: int) -> Image.Image:
    """Load a cover, scale to target height, add a soft drop shadow + thin gold edge."""
    img = Image.open(path).convert("RGB")
    cw, ch = img.size
    scale = target_h / ch
    img = img.resize((int(cw * scale), target_h), Image.LANCZOS)
    cw, ch = img.size
    # Thin gold keyline.
    GOLD = (229, 181, 103)
    edge = Image.new("RGB", (cw, ch), GOLD)
    border = max(2, int(target_h * 0.006))
    inner = img.crop((0, 0, cw, ch)).resize((cw - 2 * border, ch - 2 * border), Image.LANCZOS)
    edge.paste(inner, (border, border))
    img = edge
    # Compose onto a transparent tile with a drop shadow.
    pad = int(target_h * 0.12)
    tile = Image.new("RGBA", (cw + pad * 2, ch + pad * 2), (0, 0, 0, 0))
    shadow = Image.new("RGBA", tile.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rectangle([pad, pad + int(pad * 0.4), pad + cw, pad + ch + int(pad * 0.4)],
                 fill=(0, 0, 0, 170))
    shadow = shadow.filter(ImageFilter.GaussianBlur(pad * 0.5))
    tile.alpha_composite(shadow)
    tile.alpha_composite(Image.merge("RGBA", (*img.split(), Image.new("L", img.size, 255))), (pad, pad))
    return tile


def main():
    sw, sh = W * SCALE, H * SCALE
    canvas = Image.new("RGB", (sw, sh), BG)

    # Subtle vignette (warm center, darker edges).
    vig = Image.new("L", (sw, sh), 0)
    vd = ImageDraw.Draw(vig)
    vd.ellipse([-sw * 0.2, -sh * 0.6, sw * 1.2, sh * 1.6], fill=60)
    vig = vig.filter(ImageFilter.GaussianBlur(sw * 0.12))
    warm = Image.new("RGB", (sw, sh), (38, 33, 24))
    canvas = Image.composite(warm, canvas, vig)

    # ── The supporting 5 covers: densely packed on the left ──
    cover_h = int(sh * 0.82)
    overlap = int(cover_h * 0.65)            # aggressive overlap
    tiles = [_cover_shadowed(BOOKS / c / "design" / "cover.png", cover_h) for c in COVERS]
    step = [t.width - overlap for t in tiles]
    total_w = sum(step[:-1]) + tiles[-1].width
    x = int(-tiles[0].width * 0.15)          # start slightly off-left for drama
    y = (sh - tiles[0].height) // 2
    for i, t in enumerate(tiles):
        canvas.paste(t, (x, y), t)
        x += step[i] if i < len(tiles) - 1 else 0

    # ── The hero: Engineer of the Gods, pasted LAST so it's on top ──
    hero_h = int(sh * 0.92)
    hero = _cover_shadowed(HERO, hero_h)
    hero_x = int(sw * 0.52)                  # right side, positioned to overlap slightly but stay visible
    hero_y = (sh - hero.height) // 2
    canvas.paste(hero, (hero_x, hero_y), hero)

    canvas.save(out_2x)
    canvas.resize((W, H), Image.LANCZOS).save(out, optimize=True)
    print(f"wrote {out.name} ({out.stat().st_size // 1024} KB) and {out_2x.name}")


if __name__ == "__main__":
    main()

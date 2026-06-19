#!/usr/bin/env python3
"""Compose the Facebook cover: a collage of the History Before Time covers + house typography.

Same house language as the LinkedIn banner (warm near-black ground #161513, gold eyebrow, the
crest) but the scene is the seven full HISTORY BEFORE TIME novel covers, fanned across the right as
a cinematic shelf, with the series title + press wordmark on the left.

Facebook's cover crops differently per device. We compose on the recommended 851x315 upload size
and keep all type inside a centre-safe band (~640px wide) so nothing important is cropped on mobile.
Writes the exact 851x315 cover plus a 2x master.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = Path(__file__).resolve().parent
BRAND = HERE.parent
ASSETS = BRAND / "assets"
BOOKS = BRAND.parent / "books" / "history-before-time" / "books"

W, H = 851, 315
SCALE = 2
BG = (22, 21, 19)            # #161513 warm near-black
GOLD = (229, 181, 103)       # #E5B567
BONE = (237, 233, 224)       # #EDE9E0
MUT = (138, 132, 120)        # #8a8478

# The seven full HISTORY BEFORE TIME novels (registry HBT order, novellas excluded), by cover folder.
COVERS = [
    "book1-africa", "book2-india", "book3-india-deccan",
    "book4-india-tamil", "book5-egypt", "australia-outback", "project-stargate",
]

out = HERE / "facebook-cover.png"
out_2x = HERE / "facebook-cover@2x.png"


def _font(names, size):
    for n in names:
        try:
            return ImageFont.truetype(n, size)
        except Exception:
            continue
    return ImageFont.load_default()


def _try_fonts(size, *, bold=False):
    # Prefer the house faces; fall back to common macOS fonts so the script runs anywhere.
    if bold:
        return _font([
            "/System/Library/Fonts/Supplemental/Futura.ttc",
            "/System/Library/Fonts/HelveticaNeue.ttc",
            "/Library/Fonts/Arial Bold.ttf",
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        ], size)
    return _font([
        "/System/Library/Fonts/Supplemental/Futura.ttc",
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ], size)


def _serif(size):
    return _font([
        "/System/Library/Fonts/Supplemental/Cochin.ttc",
        "/System/Library/Fonts/Supplemental/Georgia.ttf",
        "/System/Library/Fonts/Times.ttc",
    ], size)


def _tracked(draw, xy, text, font, fill, tracking):
    """Draw letter-spaced text (Pillow has no native tracking)."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + tracking
    return x


def _cover_shadowed(path: Path, target_h: int) -> Image.Image:
    """Load a cover, scale to target height, add a soft drop shadow + thin gold edge."""
    img = Image.open(path).convert("RGB")
    cw, ch = img.size
    scale = target_h / ch
    img = img.resize((int(cw * scale), target_h), Image.LANCZOS)
    cw, ch = img.size
    # Thin gold keyline.
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

    # Subtle vignette so the centre reads warmer than the edges (matches the brand banners).
    vig = Image.new("L", (sw, sh), 0)
    vd = ImageDraw.Draw(vig)
    vd.ellipse([-sw * 0.2, -sh * 0.6, sw * 1.2, sh * 1.6], fill=60)
    vig = vig.filter(ImageFilter.GaussianBlur(sw * 0.12))
    warm = Image.new("RGB", (sw, sh), (38, 33, 24))
    canvas = Image.composite(warm, canvas, vig)

    # ── The collage: seven covers fanned across the right, with top/bottom breathing room ──
    cover_h = int(sh * 0.74)             # leaves margin top & bottom (covers + their shadow tile)
    overlap = int(cover_h * 0.52)        # tighter step so all 7 fit; each still clearly reads
    tiles = [_cover_shadowed(BOOKS / c / "design" / "cover.png", cover_h) for c in COVERS]
    step = [t.width - overlap for t in tiles]
    total_w = sum(step[:-1]) + tiles[-1].width
    # The fan occupies the right ~62%; keep the last cover fully inside the right edge.
    right_pad = int(tiles[-1].width * 0.10)
    x = sw - total_w - right_pad
    y = (sh - tiles[0].height) // 2
    for i, t in enumerate(tiles):
        canvas.paste(t, (x, y), t)
        x += step[i] if i < len(tiles) - 1 else 0

    # ── Left-side gradient scrim so the type stays legible over any cover bleed ──
    scrim = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrim)
    scrim_w = int(sw * 0.52)
    for i in range(scrim_w):
        a = int(235 * (1 - i / scrim_w) ** 1.4)
        sd.line([(i, 0), (i, sh)], fill=(22, 21, 19, a))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), scrim).convert("RGB")

    # ── House typography (left, inside the mobile-safe band) ──
    d = ImageDraw.Draw(canvas)
    lx = int(54 * SCALE)
    eyebrow = _try_fonts(int(15 * SCALE), bold=True)
    title = _try_fonts(int(40 * SCALE), bold=True)
    sub = _try_fonts(int(17 * SCALE))
    tagline = _serif(int(17 * SCALE))

    _tracked(d, (lx, int(70 * SCALE)), "ARJUNA BADGER PRESS", eyebrow, GOLD, int(4 * SCALE))
    d.text((lx, int(96 * SCALE)), "History Before Time", font=title, fill=BONE)
    # gold rule
    d.rectangle([lx, int(152 * SCALE), lx + int(60 * SCALE), int(155 * SCALE)], fill=GOLD)
    d.text((lx, int(166 * SCALE)), "A novelised ancient-mysteries saga.", font=sub, fill=BONE)
    d.text((lx, int(192 * SCALE)), "Seven books. Grounded in the evidence.", font=sub, fill=MUT)
    _tracked(d, (lx, int(232 * SCALE)), "arjunabadger.press", tagline, MUT, int(1 * SCALE))

    # Save 2x master + the exact Facebook size.
    canvas.save(out_2x)
    canvas.resize((W, H), Image.LANCZOS).save(out, optimize=True)
    print(f"wrote {out.name} ({out.stat().st_size // 1024} KB) and {out_2x.name}")


if __name__ == "__main__":
    main()

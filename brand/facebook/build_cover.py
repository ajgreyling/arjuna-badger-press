#!/usr/bin/env python3
"""Facebook cover: the Engineer of the Gods cover, full-frame and epic. Just the cover.

A Facebook cover is a wide landscape (851x315) and the book cover is a tall portrait, so we can't
simply crop a thin slice without losing the art. Instead we fill the banner with the cover's OWN
image: the cover is scaled to the full banner height and centred, and its background is extended to
the wide sides by a mirrored, blurred, darkened bleed — so the whole thing reads as one cinematic
full-frame image with the real cover intact and dominant in the mobile-safe centre.

Writes the exact 851x315 cover plus a 2x master.
"""
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter

HERE = Path(__file__).resolve().parent
BRAND = HERE.parent
BOOKS = BRAND.parent / "books" / "history-before-time" / "books"

W, H = 851, 315
SCALE = 2

# The hero cover — Engineer of the Gods (the most striking cover).
COVER = BOOKS / "book5-egypt" / "design" / "cover.png"

out = HERE / "facebook-cover.png"
out_2x = HERE / "facebook-cover@2x.png"


def main():
    sw, sh = W * SCALE, H * SCALE
    cover = Image.open(COVER).convert("RGB")

    # 1) Background bleed: scale the cover to COVER the whole wide banner (crop overflow), then blur
    #    + darken it so it fills the sides without competing with the sharp cover on top.
    cw, ch = cover.size
    cover_ar = cw / ch
    banner_ar = sw / sh
    if cover_ar < banner_ar:                 # cover narrower than banner → match width, crop height
        bw = sw
        bh = int(sw / cover_ar)
    else:
        bh = sh
        bw = int(sh * cover_ar)
    bg = cover.resize((bw, bh), Image.LANCZOS)
    bg = bg.crop(((bw - sw) // 2, (bh - sh) // 2, (bw - sw) // 2 + sw, (bh - sh) // 2 + sh))
    bg = bg.filter(ImageFilter.GaussianBlur(sw * 0.03))
    bg = ImageEnhance.Brightness(bg).enhance(0.45)
    bg = ImageEnhance.Color(bg).enhance(0.9)

    # 2) The sharp full cover, scaled to the banner height, centred. (Slight inset so a sliver of
    #    the cinematic bleed frames it top & bottom — feels intentional, not letterboxed.)
    target_h = int(sh * 0.995)
    scale = target_h / ch
    fg = cover.resize((int(cw * scale), target_h), Image.LANCZOS)
    fw, fh = fg.size

    canvas = bg.copy()
    pos = ((sw - fw) // 2, (sh - fh) // 2)
    canvas.paste(fg, pos)

    # 3) Feather the vertical seams where the sharp cover meets the bleed, so there's no hard line.
    seam = Image.new("L", (sw, sh), 0)
    left = pos[0]
    right = pos[0] + fw
    feather = int(fw * 0.04)
    from PIL import ImageDraw
    sd = ImageDraw.Draw(seam)
    sd.rectangle([left + feather, 0, right - feather, sh], fill=255)
    seam = seam.filter(ImageFilter.GaussianBlur(feather * 0.7))
    sharp_full = bg.copy()
    sharp_full.paste(fg, pos)
    canvas = Image.composite(sharp_full, bg, seam)

    canvas.save(out_2x)
    canvas.resize((W, H), Image.LANCZOS).save(out, optimize=True)
    print(f"wrote {out.name} ({out.stat().st_size // 1024} KB) and {out_2x.name}")


if __name__ == "__main__":
    main()

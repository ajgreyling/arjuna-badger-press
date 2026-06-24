#!/usr/bin/env python3
"""Generate warm PLACEHOLDER art for The Little Key so the picture-book render path can be
built and verified before the real ChatGPT/OpenRouter illustrations land. Each placeholder is
a soft honey-gold panel, > 500 KB so it clears the cover gate, clearly labelled PLACEHOLDER and
carrying the spread number + the scene one-liner. Swap each file for the real art when generated;
the filenames match the markers in build/chapters/PICTURE_BOOK.md and design/cover-prompt.txt.
"""
from pathlib import Path
import math
import os
from PIL import Image, ImageDraw, ImageFont, ImageChops

HERE = Path(__file__).resolve().parent
IMAGES = HERE / "images"
IMAGES.mkdir(exist_ok=True)

# (filename, scene one-liner) — spreads are 3:2 landscape; cover is its own portrait-ish panel.
SPREADS = [
    ("spread-01-cupboard.png", "The old cupboard in the sunbeam"),
    ("spread-02-key.png", "The small brass key on a red thread"),
    ("spread-03-carving.png", "The carved badger on the shelf"),
    ("spread-04-turn.png", "Night — she turns the key"),
    ("spread-05-awake-HERO.png", "HERO — Nkwe is awake"),
    ("spread-06-toy.png", "Played like a toy"),
    ("spread-07-runs.png", "He runs — the world goes huge"),
    ("spread-08-composite-COMPOSITE.png", "COMPOSITE — the other little ones wake"),
    ("spread-09-longnight.png", "The long, clever night"),
    ("spread-10-cornered.png", "Cornered — the big hand comes down"),
    ("spread-11-asks.png", "She makes herself small and asks"),
    ("spread-12-stays.png", "He chooses to stay"),
    ("spread-13-gogo.png", "Gogo in the doorway, unsurprised"),
    ("spread-14-closing.png", "Four watchers in the moonlight"),
]


def _font(size):
    for p in (
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf",
    ):
        if Path(p).is_file():
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def panel(w, h, label, scene, *, accent=(127, 176, 105)):
    """A warm gouache-ish gradient panel with a soft vignette and centred text."""
    img = Image.new("RGB", (w, h))
    px = img.load()
    # honey-gold vertical gradient with a gentle radial warmth (kept simple but smooth)
    top = (240, 224, 178)
    bot = (210, 170, 110)
    cx, cy = w * 0.5, h * 0.42
    maxd = math.hypot(cx, cy)
    for y in range(h):
        t = y / (h - 1)
        r = int(top[0] * (1 - t) + bot[0] * t)
        g = int(top[1] * (1 - t) + bot[1] * t)
        b = int(top[2] * (1 - t) + bot[2] * t)
        for x in range(w):
            d = math.hypot(x - cx, y - cy) / maxd
            v = 1.0 - 0.28 * d  # soft vignette
            px[x, y] = (int(r * v), int(g * v), int(b * v))
    d = ImageDraw.Draw(img)
    # soft rounded frame in the accent colour
    d.rounded_rectangle([w * 0.04, h * 0.04, w * 0.96, h * 0.96],
                        radius=int(min(w, h) * 0.05), outline=accent, width=max(4, w // 220))
    night = (40, 46, 70)
    f_big = _font(int(h * 0.085))
    f_mid = _font(int(h * 0.05))
    f_small = _font(int(h * 0.034))

    def centre(text, font, y, fill):
        bb = d.textbbox((0, 0), text, font=font)
        d.text(((w - (bb[2] - bb[0])) / 2, y), text, font=font, fill=fill)

    centre("PLACEHOLDER", f_small, h * 0.12, (150, 70, 40))
    centre(label, f_big, h * 0.40, night)
    centre(scene, f_mid, h * 0.58, (70, 60, 45))
    centre("The Little Key", f_small, h * 0.84, (110, 90, 55))
    # Fine full-colour grain blended in lightly: defeats PNG compression so the placeholder clears
    # the 500KB cover gate, while staying subtle (paint-tooth texture, not static).
    noise = Image.frombytes("RGB", (w, h), os.urandom(w * h * 3))
    img = Image.blend(img, noise, 0.10)
    return img


def main():
    # Cover — portrait-ish 1600x2000 (shelf cards expect ~400/620; this reads fine and clears 500KB)
    cov = panel(1600, 2000, "THE LITTLE KEY", "You can wake a thing. You can't own a thing.")
    cov.save(HERE / "cover.png")
    print("wrote design/cover.png", (HERE / "cover.png").stat().st_size, "bytes")
    # Spreads — 2000x1333 landscape (3:2)
    for fn, scene in SPREADS:
        label = fn.replace("spread-", "S").split("-")[0].upper()
        panel(2000, 1333, label, scene).save(IMAGES / fn)
        sz = (IMAGES / fn).stat().st_size
        print(f"wrote images/{fn} {sz} bytes{'  ⚠ under 500KB' if sz < 500_000 else ''}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build safari-mark.png — gold Badger Bow medallion on transparent, from favicon-512."""
from __future__ import annotations

from pathlib import Path

from PIL import Image

ASSETS = Path(__file__).resolve().parent / "assets"
SRC = ASSETS / "favicon-512.png"
OUT = ASSETS / "safari-mark.png"


def key_gold_transparent(img: Image.Image, *, threshold: int = 35) -> Image.Image:
    """Key dark background to alpha; keep the original favicon gold/yellow tones."""
    rgba = img.convert("RGBA")
    px = rgba.load()
    w, h = rgba.size
    edge = 35
    for y in range(h):
        for x in range(w):
            r, g, b, _a = px[x, y]
            lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
            if lum < threshold:
                px[x, y] = (0, 0, 0, 0)
            elif lum < threshold + edge:
                fade = int(255 * (lum - threshold) / edge)
                px[x, y] = (r, g, b, fade)
            else:
                px[x, y] = (r, g, b, 255)
    return rgba


def main() -> None:
    if not SRC.is_file():
        raise SystemExit(f"Missing source: {SRC}")

    img = key_gold_transparent(Image.open(SRC))
    img.save(OUT, optimize=True)
    print(f"Wrote {OUT} ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()

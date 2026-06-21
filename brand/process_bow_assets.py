#!/usr/bin/env python3
"""Process Badger Bow master + stamp downloads into brand/assets."""
from __future__ import annotations

from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"

MASTER_SRC = Path("/Users/ajgreyling/Downloads/ChatGPT Image Jun 20, 2026, 11_32_03 AM.png")
STAMP_SRC = Path("/Users/ajgreyling/Downloads/ChatGPT Image Jun 20, 2026, 11_33_52 AM.png")


def key_to_alpha(img: Image.Image, *, mode: str, threshold: int = 40) -> Image.Image:
    """mode='black' keys dark pixels transparent; mode='white' keys light pixels transparent."""
    rgba = img.convert("RGBA")
    px = rgba.load()
    w, h = rgba.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
            if mode == "black" and lum < threshold:
                px[x, y] = (r, g, b, 0)
            elif mode == "white" and lum > 255 - threshold:
                px[x, y] = (r, g, b, 0)
            else:
                # soften edges
                if mode == "black" and lum < threshold + 30:
                    fade = int(255 * (lum - threshold) / 30)
                    px[x, y] = (r, g, b, max(0, min(255, fade)))
                elif mode == "white" and lum > 255 - threshold - 30:
                    fade = int(255 * (255 - threshold - lum) / -30)
                    px[x, y] = (r, g, b, max(0, min(255, fade)))
    return rgba


def main():
    ASSETS.mkdir(parents=True, exist_ok=True)
    if not MASTER_SRC.exists():
        raise SystemExit(f"Missing master: {MASTER_SRC}")
    if not STAMP_SRC.exists():
        raise SystemExit(f"Missing stamp: {STAMP_SRC}")

    master = Image.open(MASTER_SRC)
    stamp = Image.open(STAMP_SRC)

    master.save(ASSETS / "badger-bow-master.png")
    stamp.save(ASSETS / "badger-bow-stamp-light.png")

    key_to_alpha(master, mode="black").save(ASSETS / "badger-bow-imprint.png")
    key_to_alpha(stamp, mode="white").save(ASSETS / "badger-bow-stamp.png")

    # Nav / favicon source — simple black bow on transparent
    mark = key_to_alpha(stamp, mode="white")
    mark.save(ASSETS / "mark-only.png")

    print("Wrote brand/assets:")
    for name in (
        "badger-bow-master.png",
        "badger-bow-stamp-light.png",
        "badger-bow-imprint.png",
        "badger-bow-stamp.png",
        "mark-only.png",
    ):
        p = ASSETS / name
        print(f"  {name} ({p.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()

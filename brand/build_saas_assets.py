#!/usr/bin/env python3
"""Build Studio (SaaS) logo variants — violet on indigo-black, from press gold crest art.

Outputs:
  mark-saas.png          Badger Bow medallion, violet on transparent (nav · footer · Auth0)
  logo-saas.png          Full crest + scenery on --saas-bg (#0E0B14)
  favicon-saas-32.png    Tab icon derived from mark-saas
  favicon-saas-180.png   Apple touch icon

Run from repo root or brand/:
  python3 brand/build_saas_assets.py
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"

# Studio tokens (saas/web/static/tokens.css)
SAAS_BG = (14, 11, 20)  # #0E0B14
VIOLET_DEEP = (124, 92, 255)  # #7C5CFF
VIOLET = (167, 139, 250)  # #A78BFA
VIOLET_BRIGHT = (196, 181, 253)  # #C4B5FD
GOLD_HINT = (229, 181, 103)  # #E5B567 — press bridge in mid-tones

SRC_MARK = ASSETS / "badger-bow-imprint.png"
SRC_CREST = ASSETS / "logo-master.png"

OUT_NAMES = (
    "mark-saas.png",
    "logo-saas.png",
    "favicon-saas-32.png",
    "favicon-saas-180.png",
)

PLATFORM_BRAND = HERE.parent.parent / "arjuna-badger-platform" / "saas" / "web" / "public" / "assets" / "brand"


def _lerp(a: tuple[int, ...], b: tuple[int, ...], t: float) -> tuple[int, int, int]:
    t = max(0.0, min(1.0, t))
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _luma(r: int, g: int, b: int) -> float:
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def recolor_studio_pixel(
    r: int,
    g: int,
    b: int,
    a: int,
    *,
    bg_mode: str,
    bg_threshold: float = 24.0,
) -> tuple[int, int, int, int]:
    """Map press gold-on-black art to Studio violet palette."""
    if a < 4:
        return (0, 0, 0, 0)

    lum = _luma(r, g, b)

    if lum < bg_threshold:
        if bg_mode == "transparent":
            edge = max(0.0, min(1.0, (lum - 2.0) / max(1.0, bg_threshold - 2.0)))
            out_a = int(a * edge * 0.85)
            if out_a < 6:
                return (0, 0, 0, 0)
            # Anti-aliased fringe only — keep transparent, not a tinted fill
            return (0, 0, 0, out_a)
        return (*SAAS_BG, 255)

    span = 210.0 - bg_threshold
    t = max(0.0, min(1.0, (lum - bg_threshold) / span))

    if t < 0.42:
        rgb = _lerp(VIOLET_DEEP, VIOLET, t / 0.42)
    elif t < 0.68:
        u = (t - 0.42) / 0.26
        base = _lerp(VIOLET, GOLD_HINT, u * 0.28)
        rgb = _lerp(base, VIOLET_BRIGHT, u * 0.22)
    else:
        rgb = _lerp(GOLD_HINT, VIOLET_BRIGHT, (t - 0.68) / 0.32)

    return (*rgb, a)


def recolor_image(img: Image.Image, *, bg_mode: str) -> Image.Image:
    rgba = img.convert("RGBA")
    px = rgba.load()
    w, h = rgba.size
    for y in range(h):
        for x in range(w):
            px[x, y] = recolor_studio_pixel(*px[x, y], bg_mode=bg_mode)
    return rgba


def build_mark() -> Image.Image:
    if not SRC_MARK.is_file():
        raise FileNotFoundError(SRC_MARK)
    return recolor_image(Image.open(SRC_MARK), bg_mode="transparent")


def build_crest() -> Image.Image:
    if not SRC_CREST.is_file():
        raise FileNotFoundError(SRC_CREST)
    return recolor_image(Image.open(SRC_CREST), bg_mode="solid")


def write_favicons(mark: Image.Image, out_dir: Path) -> None:
    mark_rgb = mark.convert("RGBA")
    for size, name in ((32, "favicon-saas-32.png"), (180, "favicon-saas-180.png")):
        icon = mark_rgb.resize((size, size), Image.Resampling.LANCZOS)
        icon.save(out_dir / name, optimize=True)


def sync_outputs(out_dir: Path) -> None:
    if PLATFORM_BRAND.is_dir() and out_dir.resolve() != PLATFORM_BRAND.resolve():
        PLATFORM_BRAND.mkdir(parents=True, exist_ok=True)
        for name in OUT_NAMES:
            src = out_dir / name
            if src.is_file():
                shutil.copy2(src, PLATFORM_BRAND / name)
        print(f"Synced -> {PLATFORM_BRAND}")


def main() -> int:
    out_dir = ASSETS
    out_dir.mkdir(parents=True, exist_ok=True)

    mark = build_mark()
    crest = build_crest()

    mark_path = out_dir / "mark-saas.png"
    crest_path = out_dir / "logo-saas.png"
    mark.save(mark_path, optimize=True)
    crest.save(crest_path, optimize=True)
    write_favicons(mark, out_dir)

    print("Wrote Studio brand assets:")
    for name in OUT_NAMES:
        p = out_dir / name
        kb = p.stat().st_size // 1024 if p.is_file() else 0
        print(f"  {name} ({kb} KB)")

    sync_outputs(out_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())

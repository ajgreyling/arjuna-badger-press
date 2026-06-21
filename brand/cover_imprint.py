#!/usr/bin/env python3
"""Apply the Badger Bow colophon to book covers without obscuring art or type.

Uses:
  badger-bow-imprint.png  — gold mark, black keyed transparent (dark / busy covers)
  badger-bow-stamp.png    — black mark, white keyed transparent (light corners)

Default placement: bottom-right colophon (~4.5% of cover width, 3% inset).
Picks corner + variant from local luminance; skips corners that overlap high-contrast type bands.

    python3 brand/cover_imprint.py path/to/cover.png
    python3 brand/cover_imprint.py --all   # every design/cover.png under books/
"""
from __future__ import annotations

import argparse
import statistics
import sys
from pathlib import Path

from PIL import Image, ImageFilter, ImageStat

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
IMPRINT_GOLD = ASSETS / "badger-bow-imprint.png"
IMPRINT_STAMP = ASSETS / "badger-bow-stamp.png"

# Avoid the lower title band (typical 6×9 layout) and top series line.
SAFE_EXCLUDE = (
    (0.0, 0.62, 1.0, 1.0),   # lower 38% — title / author
    (0.0, 0.0, 1.0, 0.11),   # top 11% — series eyebrow
)

CORNER_ANCHORS = ("br", "bl", "tr", "tl")  # try bottom-right first (publisher colophon)
SIZE_FRAC = 0.045
MARGIN_FRAC = 0.03
LIGHT_LUMA = 165


def _luma(rgb: tuple[int, ...]) -> float:
    r, g, b = rgb[:3]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _region_stats(img: Image.Image, box: tuple[int, int, int, int]) -> tuple[float, float]:
    crop = img.crop(box).convert("RGB")
    stat = ImageStat.Stat(crop)
    mean = _luma(tuple(int(x) for x in stat.mean))
    # variance proxy — busy regions get higher spread
    spread = max(stat.stddev) if stat.stddev else 0.0
    return mean, spread


def _overlaps_excluded(x0: int, y0: int, x1: int, y1: int, w: int, h: int) -> bool:
    fx0, fy0, fx1, fy1 = x0 / w, y0 / h, x1 / w, y1 / h
    for ex0, ey0, ex1, ey1 in SAFE_EXCLUDE:
        if fx0 < ex1 and fx1 > ex0 and fy0 < ey1 and fy1 > ey0:
            return True
    return False


def _box_for_anchor(anchor: str, w: int, h: int, side: int, margin: int) -> tuple[int, int]:
    if anchor == "br":
        return w - margin - side, h - margin - side
    if anchor == "bl":
        return margin, h - margin - side
    if anchor == "tr":
        return w - margin - side, margin
    return margin, margin


def _pick_placement(img: Image.Image, side: int, margin: int) -> tuple[str, str]:
    """Return (anchor, variant) where variant is 'gold' or 'stamp'."""
    w, h = img.size
    best: tuple[float, str, str] | None = None
    for anchor in CORNER_ANCHORS:
        x, y = _box_for_anchor(anchor, w, h, side, margin)
        if _overlaps_excluded(x, y, x + side, y + side, w, h):
            continue
        mean, spread = _region_stats(img, (x, y, x + side, y + side))
        variant = "stamp" if mean > LIGHT_LUMA else "gold"
        # prefer dark quiet corners for gold; light quiet for stamp; penalise busy
        score = abs(mean - (210 if variant == "stamp" else 45)) + spread * 2
        if anchor == "br":
            score -= 8  # slight preference for classic colophon corner
        if best is None or score < best[0]:
            best = (score, anchor, variant)
    if best:
        return best[1], best[2]
    return "br", "gold"


def _load_mark(variant: str) -> Image.Image:
    path = IMPRINT_STAMP if variant == "stamp" else IMPRINT_GOLD
    if not path.exists():
        raise FileNotFoundError(f"Missing imprint asset: {path}")
    return Image.open(path).convert("RGBA")


def apply_imprint(
    cover: Image.Image,
    *,
    anchor: str | None = None,
    variant: str | None = None,
    opacity: float = 0.92,
) -> Image.Image:
    """Return a new RGBA/RGB image with the Badger Bow colophon composited."""
    base = cover.convert("RGBA")
    w, h = base.size
    side = max(24, int(min(w, h) * SIZE_FRAC))
    margin = max(12, int(min(w, h) * MARGIN_FRAC))

    if anchor is None or variant is None:
        auto_anchor, auto_variant = _pick_placement(base, side, margin)
        anchor = anchor or auto_anchor
        variant = variant or auto_variant

    mark = _load_mark(variant)
    mark = mark.resize((side, side), Image.Resampling.LANCZOS)

    # soft shadow for legibility on busy art
    shadow = Image.new("RGBA", (side + 8, side + 8), (0, 0, 0, 0))
    sh = Image.new("RGBA", mark.size, (0, 0, 0, 110))
    shadow.paste(sh, (4, 4), sh)
    shadow = shadow.filter(ImageFilter.GaussianBlur(3))

    x, y = _box_for_anchor(anchor, w, h, side, margin)
    out = base.copy()
    out.alpha_composite(shadow, (x - 2, y - 2))

    if opacity < 1.0:
        alpha = mark.split()[3]
        alpha = alpha.point(lambda a: int(a * opacity))
        mark.putalpha(alpha)
    out.alpha_composite(mark, (x, y))
    return out


def imprint_file(path: Path, *, dry_run: bool = False) -> bool:
    if not path.exists():
        print(f"  [skip] missing {path}")
        return False
    img = Image.open(path)
    w, h = img.size
    side = max(24, int(min(w, h) * SIZE_FRAC))
    margin = max(12, int(min(w, h) * MARGIN_FRAC))

    if dry_run:
        anchor, variant = _pick_placement(img.convert("RGBA"), side, margin)
        print(f"  [dry] {path} -> {anchor}/{variant}")
        return True

    result = apply_imprint(img)
    mode = "RGBA" if path.suffix.lower() == ".png" else "RGB"
    out = result.convert(mode)
    if path.suffix.lower() in (".jpg", ".jpeg"):
        out.save(path, quality=92, dpi=img.info.get("dpi", (300, 300)))
    else:
        out.save(path, dpi=img.info.get("dpi", (300, 300)))
    print(f"  [ok] {path}")
    return True


def iter_covers(root: Path):
    for rel in (
        "design/cover.png",
        "design/cover.jpg",
        "build/export/cover.png",
        "build/export/cover.jpg",
    ):
        yield from sorted(root.rglob(rel))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Apply Badger Bow cover colophon")
    parser.add_argument("paths", nargs="*", help="Cover image(s)")
    parser.add_argument("--all", action="store_true", help="Stamp every books/**/design/cover.*")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    repo = HERE.parent
    targets: list[Path] = [Path(p) for p in args.paths]
    if args.all:
        targets = list(iter_covers(repo / "books"))
        # platform mirror
        plat = repo.parent / "arjuna-badger-platform" / "books"
        if plat.is_dir():
            targets.extend(iter_covers(plat))

    if not targets:
        parser.print_help()
        return 1

    n = sum(imprint_file(t, dry_run=args.dry_run) for t in targets)
    print(f"Done — {n} cover(s) processed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

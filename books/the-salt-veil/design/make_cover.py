#!/usr/bin/env python3
"""Book 1 *The Salt Veil* — HBT typography on cinematic plate (see ~/Desktop/salt-veil-covers/).

    python3 design/make_cover.py   # reads design/cover-plate.png -> cover.{png,jpg}
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

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
ATK_BI = str(_ATK / "AtkinsonHyperlegible-BoldItalic.otf")

DESKTOP = Path.home() / "Desktop" / "salt-veil-covers" / "make_cover_book1_hbt.py"

if DESKTOP.is_file():
    # Delegate to the canonical Desktop generator (same plate + type stack).
    import runpy
    sys.argv[0] = str(DESKTOP)
    runpy.run_path(str(DESKTOP), run_name="__main__")
    # Copy outputs into this design/ dir.
    src = DESKTOP.parent
    for name in ("the-salt-veil_cover.png", "the-salt-veil_cover.jpg"):
        data = (src / name).read_bytes()
        (HERE / name.replace("the-salt-veil_", "cover.")).write_bytes(data)
    exp = HERE.parent / "build" / "export"
    exp.mkdir(parents=True, exist_ok=True)
    for ext in ("png", "jpg"):
        (exp / f"cover.{ext}").write_bytes((HERE / f"cover.{ext}").read_bytes())
    print(f"synced -> {HERE} and {exp}")
else:
    raise SystemExit(f"Missing {DESKTOP} — run from Desktop salt-veil-covers bundle.")

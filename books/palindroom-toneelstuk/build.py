#!/usr/bin/env python3
"""Render *Palindroom Toneelstuk* — Afrikaans stage adaptation of Palindrome.

Source of truth: build/BOOK.md (authored play). Same cover plate as Palindrome
(design/cover.png, copied from books/palindrome/design/).

  python3 books/palindroom-toneelstuk/build.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUILD = HERE / "build"
TITLE = "Palindroom Toneelstuk"
AUTHOR = "Andries J. Greyling"


def render() -> None:
    repo = HERE.parent.parent
    gate = repo / "tools" / "render_book.sh"
    book_md = BUILD / "BOOK.md"
    out_base = BUILD / "export" / TITLE
    if not book_md.exists():
        sys.exit(f"  [render] missing {book_md}")
    if not gate.exists():
        sys.exit(f"  [render] missing gate {gate}")
    cover = HERE / "design" / "cover.png"
    out_base.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["bash", str(gate), str(book_md), str(out_base), TITLE, AUTHOR]
    if cover.is_file():
        cmd.append(str(cover))
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    render()

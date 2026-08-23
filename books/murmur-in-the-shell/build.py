#!/usr/bin/env python3
"""Assemble and render *Murmur in the Shell*.

Canonical prose lives in manuscript/ch-*.md. Derived BOOK.md and exports stay under build/.
Run after every completed chapter so the current EPUB is always readable.
"""

from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
MANUSCRIPT = ROOT / "manuscript"
BOOK = ROOT / "build" / "BOOK.md"
OUT = ROOT / "build" / "export" / "Murmur in the Shell"


def assemble() -> list[Path]:
    chapters = sorted(MANUSCRIPT.glob("ch-*.md"))
    if not chapters:
        raise SystemExit("No completed chapter files found")
    frontmatter = """---
lang: en-ZA
publisher: House of Greyling
title: Murmur in the Shell
author: Andries J. Greyling
---

"""
    BOOK.parent.mkdir(parents=True, exist_ok=True)
    BOOK.write_text(
        frontmatter
        + "\n\n".join(path.read_text(encoding="utf-8").rstrip() for path in chapters)
        + "\n",
        encoding="utf-8",
    )
    print(f"assembled {len(chapters)} chapter(s) -> {BOOK}")
    return chapters


def render() -> None:
    subprocess.run(
        [
            str(REPO / "tools" / "render_book.sh"),
            str(BOOK),
            str(OUT),
            "Murmur in the Shell",
            "Andries J. Greyling",
        ],
        check=True,
    )


if __name__ == "__main__":
    assemble()
    render()


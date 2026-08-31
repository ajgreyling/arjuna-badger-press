#!/usr/bin/env python3
"""Assemble and render *Ethics and Metaphysics for Everyone*.

Canonical prose lives in manuscript/. Derived BOOK.md and exports stay under build/.
Run after every completed chapter so the current EPUB is always readable (goal: chapter
at a time, EPUB after every finished chapter).
"""

from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
MANUSCRIPT = ROOT / "manuscript"
BOOK = ROOT / "build" / "BOOK.md"
OUT = ROOT / "build" / "export" / "Ethics and Metaphysics for Everyone"

TITLE = "Ethics and Metaphysics for Everyone"
AUTHOR = "Andries J. Greyling"


def assemble() -> list[Path]:
    chapters = sorted(MANUSCRIPT.glob("ch-*.md"))
    if not chapters:
        raise SystemExit("No completed chapter files found")

    frontmatter = f"""---
lang: en-ZA
publisher: House of Greyling
title: {TITLE}
author: {AUTHOR}
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
            TITLE,
            AUTHOR,
        ],
        check=True,
    )


if __name__ == "__main__":
    assemble()
    render()

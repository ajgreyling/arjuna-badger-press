#!/usr/bin/env python3
"""Assemble and render *TAME*.

Canonical prose lives in manuscript/. Derived BOOK.md and exports stay under build/.
Run after every completed chapter so the current EPUB is always readable.

Matter order is fixed by CANON_LOCKS L-19 and is not negotiable:

    FOREWORD.md   the machine's, signed, already written
    ch-*.md       the novel
    AFTERWORD.md  the author's own voice — the machine may edit, never draft
    COLOPHON.md   required in every edition and format by L-16

The afterword and colophon are included when present and warned about when absent.
The build never invents either one.
"""

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
MANUSCRIPT = ROOT / "manuscript"
BOOK = ROOT / "build" / "BOOK.md"
OUT = ROOT / "build" / "export" / "TAME"

TITLE = "TAME"
AUTHOR = "Andries J. Greyling"


def assemble() -> list[Path]:
    chapters = sorted(MANUSCRIPT.glob("ch-*.md"))
    if not chapters:
        raise SystemExit("No completed chapter files found")

    parts: list[Path] = []
    foreword = MANUSCRIPT / "FOREWORD.md"
    if foreword.exists():
        parts.append(foreword)
    else:
        print("  [L-19] WARNING: FOREWORD.md missing — the machine's disclosure is binding matter")

    parts.extend(chapters)

    for name, lock in (("AFTERWORD.md", "L-19"), ("COLOPHON.md", "L-16")):
        path = MANUSCRIPT / name
        if path.exists():
            parts.append(path)
        else:
            print(f"  [{lock}] not yet written: {name} — required before any edition ships")

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
        + "\n\n".join(path.read_text(encoding="utf-8").rstrip() for path in parts)
        + "\n",
        encoding="utf-8",
    )
    print(f"assembled {len(chapters)} chapter(s), {len(parts)} part(s) -> {BOOK}")
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

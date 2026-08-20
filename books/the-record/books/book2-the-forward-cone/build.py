#!/usr/bin/env python3
"""Assemble and render ONE RECORD, Book II: The Forward Cone.

Chapter Markdown is canonical prose. build/BOOK.md and build/export are derived local artifacts.
"""

from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parent
CHAPTERS = ROOT / "build" / "chapters"
BOOK = ROOT / "build" / "BOOK.md"
OUT = ROOT / "build" / "export" / "The Forward Cone"


def assemble() -> None:
    chapter_files = sorted(CHAPTERS.glob("ch-*.md"))
    if not chapter_files:
        raise SystemExit("No chapter files found")

    # Title/author are supplied explicitly by render_book.sh. Keeping them in this YAML as well
    # makes Pandoc emit a plain title page before the full-bleed PDF cover.
    frontmatter = """---
lang: en-ZA
publisher: House of Greyling
---

"""
    BOOK.parent.mkdir(parents=True, exist_ok=True)
    BOOK.write_text(
        frontmatter
        + "\n\n".join(path.read_text(encoding="utf-8").rstrip() for path in chapter_files)
        + "\n",
        encoding="utf-8",
    )
    print(f"assembled {len(chapter_files)} chapter(s) -> {BOOK}")


def render() -> None:
    subprocess.run(
        [
            str(ROOT.parents[3] / "tools" / "render_book.sh"),
            str(BOOK),
            str(OUT),
            "The Forward Cone",
            "Andries J. Greyling",
        ],
        check=True,
    )


if __name__ == "__main__":
    assemble()
    render()

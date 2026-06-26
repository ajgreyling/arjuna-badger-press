#!/usr/bin/env python3
"""Merge *The Antifragile Reader* book/*.md -> build/BOOK.md.

  python3 build.py           # merge only
  python3 build.py --render  # merge + EPUB/PDF via tools/render_book.sh
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BOOK = HERE / "book"
BUILD = HERE / "build"
EXPORT = BUILD / "export"
TITLE = "The Antifragile Reader"
AUTHOR = "Andries J. Greyling"
COVER = HERE / "design" / "cover.png"

_YAML = re.compile(r"^---\s*\n.*?\n(?:---|\.\.\.)\s*\n", re.DOTALL)


def _strip_yaml(text: str) -> str:
    return _YAML.sub("", text, count=1).lstrip()


def _ordered_sections() -> list[Path]:
    front = BOOK / "_front.md"
    essays = sorted(BOOK.glob("[0-9][0-9]-*.md"), key=lambda p: p.name)
    out: list[Path] = []
    if front.exists():
        out.append(front)
    out.extend(essays)
    return out


def merge() -> Path:
    sections = _ordered_sections()
    if len(sections) < 2:
        sys.exit("  [skip] no essays in book/")

    title_block = f"""# {TITLE}

*Nassim Taleb's* Incerto*, plainly told — a companion for every reader*

{AUTHOR}

*House of Greyling · History Before Time · Companions*

---

"""
    parts = [title_block]
    for p in sections:
        text = _strip_yaml(p.read_text(encoding="utf-8")).rstrip()
        parts.append(text)

    book = "\n\n".join(parts) + "\n"
    BUILD.mkdir(parents=True, exist_ok=True)
    out = BUILD / "BOOK.md"
    out.write_text(book, encoding="utf-8")
    words = len(book.split())
    print(f"  [ok] BOOK.md ({len(sections)} sections, ~{words:,} words)")
    return out


def render(book_md: Path) -> None:
    repo = HERE.parents[3]
    gate = repo / "tools" / "render_book.sh"
    if not gate.is_file():
        sys.exit(f"  [fail] render gate missing: {gate}")
    EXPORT.mkdir(parents=True, exist_ok=True)
    out_base = str(EXPORT / TITLE)
    cmd = ["bash", str(gate), str(book_md), out_base, TITLE, AUTHOR]
    if COVER.is_file():
        cmd.append(str(COVER))
    subprocess.run(cmd, check=True)


def main() -> None:
    book_md = merge()
    if "--render" in sys.argv:
        render(book_md)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Assemble the tracked Markdown manuscript from its source parts."""

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "build"
CHAPTER_NAME = re.compile(r"^ch-?(\d+)(?:-[^.]+)?\.md$")


def chapter_sort_key(path: Path) -> tuple[int, str]:
    match = CHAPTER_NAME.fullmatch(path.name)
    if match is None:
        raise ValueError(f"Unsupported chapter filename: {path.name}")
    return int(match.group(1)), path.name


def assemble() -> Path:
    chapters = sorted((BUILD / "chapters").glob("ch*.md"), key=chapter_sort_key)
    parts = [(BUILD / "PREFACE.md").read_text(encoding="utf-8").rstrip()]
    parts.extend(chapter.read_text(encoding="utf-8").rstrip() for chapter in chapters)
    parts.append((BUILD / "ACKNOWLEDGEMENTS.md").read_text(encoding="utf-8").rstrip())
    manuscript = parts[0] + "\n\n---\n\n" + "\n\n".join(parts[1:]) + "\n"
    output = BUILD / "BOOK.md"
    output.write_text(manuscript, encoding="utf-8")
    print(f"assembled {len(chapters)} chapter/backmatter files -> {output}")
    return output


if __name__ == "__main__":
    assemble()

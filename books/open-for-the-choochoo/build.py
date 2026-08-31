#!/usr/bin/env python3
"""Assemble, render, validate and log *Open for the choochoo*.

Canonical prose lives in manuscript/ch-*.md. Derived BOOK.md, EPUB and PDF stay under build/.

Run this after every completed chapter. A chapter does not count as finished until:

1. chapter numbering is contiguous from 1;
2. the full manuscript is assembled;
3. the house render gate succeeds;
4. the EPUB passes ZIP/container checks;
5. every completed chapter heading appears in the EPUB; and
6. the successful snapshot is recorded in EPUB_BUILD_LEDGER.md.

The same current EPUB is replaced on each run. The append-only ledger proves that a valid cumulative
EPUB existed after each chapter without keeping thirty-two heavy binary snapshots in git.
"""

from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from html import unescape
from pathlib import Path
import re
import subprocess
import unicodedata
import zipfile


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
MANUSCRIPT = ROOT / "manuscript"
AUTHOR_NOTE = MANUSCRIPT / "FRONT_MATTER.md"
BOOK = ROOT / "build" / "BOOK.md"
OUT = ROOT / "build" / "export" / "Open for the choochoo"
EPUB = OUT.with_suffix(".epub")
LEDGER = ROOT / "EPUB_BUILD_LEDGER.md"

TITLE = "Open for the choochoo"
AUTHOR = "Andries J. Greyling"
CHAPTER_FILE = re.compile(r"ch-(\d{2})\.md$")
HEADING = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
WORDS = re.compile(r"\b[\w’'-]+\b", re.UNICODE)


def completed_chapters() -> list[Path]:
    chapters: list[tuple[int, Path]] = []
    for path in MANUSCRIPT.glob("ch-*.md"):
        match = CHAPTER_FILE.fullmatch(path.name)
        if match:
            chapters.append((int(match.group(1)), path))
    chapters.sort()
    if not chapters:
        raise SystemExit("No completed chapter files found")
    numbers = [number for number, _ in chapters]
    expected = list(range(1, len(chapters) + 1))
    if numbers != expected:
        raise SystemExit(f"Chapter sequence must be contiguous: found {numbers}, expected {expected}")
    return [path for _, path in chapters]


def heading(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = HEADING.search(text)
    if not match:
        raise SystemExit(f"Missing Markdown H1 chapter heading: {path}")
    return match.group(1).strip()


def assemble(chapters: list[Path]) -> str:
    if not AUTHOR_NOTE.is_file():
        raise SystemExit(f"Required authorship disclosure is missing: {AUTHOR_NOTE}")
    frontmatter = f"""---
lang: en-ZA
publisher: House of Greyling
title: {TITLE}
author: {AUTHOR}
---

"""
    parts = [AUTHOR_NOTE.read_text(encoding="utf-8").rstrip()]
    parts.extend(path.read_text(encoding="utf-8").rstrip() for path in chapters)
    source = frontmatter + "\n\n".join(parts) + "\n"
    BOOK.parent.mkdir(parents=True, exist_ok=True)
    BOOK.write_text(source, encoding="utf-8")
    print(f"assembled {len(chapters)} chapter(s) -> {BOOK}")
    return source


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


def epub_text(epub: Path) -> str:
    if not epub.is_file() or epub.stat().st_size < 1024:
        raise SystemExit(f"EPUB missing or implausibly small: {epub}")
    with zipfile.ZipFile(epub) as archive:
        bad_member = archive.testzip()
        if bad_member:
            raise SystemExit(f"EPUB ZIP integrity failure at {bad_member}")
        names = set(archive.namelist())
        for required in ("mimetype", "META-INF/container.xml"):
            if required not in names:
                raise SystemExit(f"EPUB missing required member: {required}")
        if archive.read("mimetype") != b"application/epub+zip":
            raise SystemExit("EPUB mimetype member is invalid")
        documents: list[str] = []
        for name in sorted(names):
            if name.lower().endswith((".xhtml", ".html", ".htm")):
                documents.append(archive.read(name).decode("utf-8", errors="replace"))
    plain = re.sub(r"<[^>]+>", " ", "\n".join(documents))
    return re.sub(r"\s+", " ", unescape(plain)).strip()


def validate(epub: Path, chapters: list[Path]) -> None:
    def normalise(value: str) -> str:
        value = unicodedata.normalize("NFKC", value)
        return value.translate(
            str.maketrans(
                {
                    "’": "'",
                    "‘": "'",
                    "“": '"',
                    "”": '"',
                    "–": "-",
                    "—": "-",
                    "\u00a0": " ",
                }
            )
        )

    rendered = normalise(epub_text(epub))
    note_heading = normalise(heading(AUTHOR_NOTE))
    if note_heading not in rendered:
        raise SystemExit(f"EPUB does not contain required authorship disclosure heading: {note_heading}")
    missing = [heading(path) for path in chapters if normalise(heading(path)) not in rendered]
    if missing:
        raise SystemExit(f"EPUB does not contain completed chapter heading(s): {missing}")
    print(f"validated EPUB container and {len(chapters)} chapter heading(s) -> {epub}")


def digest(data: bytes) -> str:
    return sha256(data).hexdigest()


def word_count(text: str) -> int:
    body = re.sub(r"^---.*?---\s*", "", text, count=1, flags=re.DOTALL)
    return len(WORDS.findall(body))


def ensure_ledger() -> None:
    if LEDGER.exists():
        return
    LEDGER.write_text(
        "# EPUB build ledger — Open for the choochoo\n\n"
        "> Append-only evidence. Each row is written only after the cumulative manuscript has passed\n"
        "> the house render gate, EPUB integrity checks and completed-heading checks. The EPUB itself\n"
        "> is a regenerable heavy build artifact and is ignored by git.\n\n"
        "| Build | Through chapter | Latest heading | Chapter words | Total words | Source SHA-256 | EPUB SHA-256 | Built UTC |\n"
        "|---:|---:|---|---:|---:|---|---|---|\n",
        encoding="utf-8",
    )


def log_success(chapters: list[Path], source: str) -> None:
    ensure_ledger()
    latest = chapters[-1]
    latest_heading = heading(latest).replace("|", "\\|")
    source_hash = digest(source.encode("utf-8"))
    epub_hash = digest(EPUB.read_bytes())
    existing = LEDGER.read_text(encoding="utf-8")
    unique_marker = f"{len(chapters)}:{source_hash}:{epub_hash}"
    if f"<!-- {unique_marker} -->" in existing:
        print(f"snapshot already logged through chapter {len(chapters)}")
        return
    build_number = existing.count("<!-- build:") + 1
    chapter_words = word_count(latest.read_text(encoding="utf-8"))
    total_words = word_count(source)
    built = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    row = (
        f"| {build_number} | {len(chapters)} | {latest_heading} | {chapter_words} | {total_words} | "
        f"`{source_hash}` | `{epub_hash}` | {built} |\n"
        f"<!-- build:{build_number} {unique_marker} -->\n"
    )
    with LEDGER.open("a", encoding="utf-8") as handle:
        handle.write(row)
    print(f"logged successful cumulative EPUB build {build_number} through chapter {len(chapters)}")


def main() -> None:
    chapters = completed_chapters()
    source = assemble(chapters)
    render()
    validate(EPUB, chapters)
    log_success(chapters, source)


if __name__ == "__main__":
    main()

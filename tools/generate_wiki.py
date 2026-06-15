#!/usr/bin/env python3
"""Generate docs/wiki/{book-id}.md from design/IMAGE_COMPENDIUM.md sources.

Run from the arjuna-badger-press repo root:

    python3 tools/generate_wiki.py

Hand-authored wiki pages (resonance, revelation, relic, …) are skipped when they
contain ``<!-- hand-authored -->`` in the first ten lines.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
WIKI = REPO / "docs" / "wiki"
BOOKS = REPO / "books"

# book id, title, subtitle, root relative to books/, read path (GitHub-relative)
CATALOG = [
    ("book1-africa", "The Calendar of Stone", "History Before Time · I",
     "history-before-time/books/book1-africa",
     "books/history-before-time/books/book1-africa/build/BOOK.md"),
    ("book2-india", "The Indian One", "History Before Time · II",
     "history-before-time/books/book2-india",
     "books/history-before-time/books/book2-india/build/BOOK.md"),
    ("book3-india-deccan", "The Temple in the Rock — Deccan", "History Before Time · III",
     "history-before-time/books/book3-india-deccan",
     "books/history-before-time/books/book3-india-deccan/build/BOOK.md"),
    ("book4-india-tamil", "The Shore That Remembers", "History Before Time · IV",
     "history-before-time/books/book4-india-tamil",
     "books/history-before-time/books/book4-india-tamil/build/BOOK.md"),
    ("book5-egypt", "The Engineer of the Gods", "History Before Time · V",
     "history-before-time/books/book5-egypt",
     "books/history-before-time/books/book5-egypt/build/BOOK.md"),
    ("australia-outback", "The Songlines of Stone", "History Before Time · VI",
     "history-before-time/books/australia-outback",
     "books/history-before-time/books/australia-outback/build/BOOK.md"),
    ("project-stargate", "The Men Who Opened the Door", "History Before Time · VII",
     "history-before-time/books/project-stargate",
     "books/history-before-time/books/project-stargate/build/BOOK.md"),
    ("jakobus-silver-thread", "The Silver Thread", "A Jakobus Swart story",
     "history-before-time/books/jakobus-silver-thread",
     "books/history-before-time/books/jakobus-silver-thread/build/BOOK.md"),
    ("jakobus-the-recitation", "The Recitation", "A Jakobus Swart story",
     "history-before-time/books/jakobus-the-recitation",
     "books/history-before-time/books/jakobus-the-recitation/build/BOOK.md"),
    ("crop-circles", "The Field of Doors", "Not a Potato",
     "history-before-time/books/crop-circles",
     "books/history-before-time/books/crop-circles/build/BOOK.md"),
    ("unheard-japan", "The Way That Was Invented", "The Unheard · Japan",
     "the-unheard/books/japan-ainu",
     "books/the-unheard/books/japan-ainu/build/BOOK.md"),
    ("unheard-mongolia", "The Felt and the Sky", "The Unheard · Mongolia",
     "the-unheard/books/mongolia-steppe",
     "books/the-unheard/books/mongolia-steppe/build/BOOK.md"),
    ("sheltering-desert", "The Indifferent Desert", "A standalone novel · true story",
     "the-sheltering-desert",
     "books/the-sheltering-desert/build/BOOK.md"),
]


def is_hand_authored(path: Path) -> bool:
    if not path.is_file():
        return False
    head = path.read_text(encoding="utf-8", errors="ignore").splitlines()[:10]
    return any("<!-- hand-authored -->" in line for line in head)


def img_prefix(rootrel: str) -> str:
    return f"../../books/{rootrel}/design/images/"


def transform_compendium(text: str, rootrel: str) -> str:
    """Strip production metadata; fix image paths for docs/wiki/."""
    out: list[str] = []
    skip_block = False
    prefix = img_prefix(rootrel)

    for raw in text.splitlines():
        line = raw.rstrip()
        s = line.strip()

        if s.startswith("# Image Compendium"):
            continue
        if s.startswith("> Freely-licensed") or s.startswith("> Every image") or s.startswith("> The **credit"):
            continue
        if s.startswith("> Files live alongside"):
            continue
        if s.startswith("- **File:**") or s.startswith("- **Source:**") or s.startswith("- **Licence:"):
            skip_block = True
            continue
        if skip_block:
            if s.startswith("- **Credit line"):
                m = re.search(r"\*\*Credit line.*?:\*\*\s*(.+)$", s)
                if m:
                    out.append(f"*{m.group(1).strip()}*")
                skip_block = False
            continue

        if "design/images/" in line:
            line = line.replace("design/images/", prefix)
        out.append(line)

    # collapse triple blank lines
    body = re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip()
    return body


def render_wiki(book_id: str, title: str, subtitle: str, rootrel: str, read_path: str, body: str) -> str:
    return f"""# {title} — real places & people

> {subtitle} · A photo wiki for travellers and curious readers.
> The novel is fiction; these grounds are real — go stand in them.
> **[Read the book](../../{read_path})** · [All place wikis](README.md)

{body}

---

*All photographs are freely licensed (public domain / CC) via [Wikimedia Commons](https://commons.wikimedia.org/).
See each caption for author and licence.*
"""


def main() -> None:
    WIKI.mkdir(parents=True, exist_ok=True)
    n = 0
    for book_id, title, subtitle, rootrel, read_path in CATALOG:
        out_path = WIKI / f"{book_id}.md"
        if is_hand_authored(out_path):
            print(f"[skip] hand-authored {out_path.name}")
            continue
        comp = BOOKS / rootrel / "design" / "IMAGE_COMPENDIUM.md"
        if not comp.is_file():
            print(f"[skip] no compendium for {book_id}")
            continue
        body = transform_compendium(comp.read_text(encoding="utf-8", errors="ignore"), rootrel)
        out_path.write_text(render_wiki(book_id, title, subtitle, rootrel, read_path, body), encoding="utf-8")
        print(f"[ok] {out_path.name}")
        n += 1
    print(f"generated {n} wiki pages -> {WIKI}")


if __name__ == "__main__":
    main()

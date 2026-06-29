#!/usr/bin/env python3
"""Self-contained merge + render for the standalone chamber-piece novella *PALINDROME*.

Total firewall: depends on NOTHING in History Before Time or the trilogy. Mirrors the proven
standalone pattern (books/the-loneliest/build.py): [canon/DEDICATION_BOOK.md if present] +
[canon/READER_NOTE.md if present] + ch-*.md -> build/BOOK.md, then render through the binding
RENDER GATE (tools/render_book.sh): Atkinson body embedded, cover, colophon, PDF + EPUB.

PALINDROME is a STANDALONE — it is OUT of scope for the (now-retired) standing library dedication
(that is dedicated to History Before Time + the Jakobus stories only). It carries only its own
dedication; there is no library inscription to suppress, but the opt-out marker is honoured anyway
for symmetry with the-loneliest.

  python3 books/palindrome/build.py            # merge + render (epub + pdf via gate)
  python3 books/palindrome/build.py --merge    # merge only (BOOK.md + novelcrafter)

BOOK.md / BOOK.novelcrafter.md / the .epub / .pdf are DERIVED, local-only build artifacts.
Commit only chapters/ + canon/.
"""
from __future__ import annotations

import re
import sys
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent          # books/palindrome
BUILD = HERE / "build"
CH = BUILD / "chapters"
CANON = HERE / "canon"
TITLE = "Palindrome"
AUTHOR = "Andries J. Greyling"


def _chapters() -> list[Path]:
    return sorted(CH.glob("ch-*.md")) if CH.exists() else []


_HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)


def _clean(txt: str) -> str:
    """Strip authoring HTML comments so they never reach the rendered book."""
    return _HTML_COMMENT.sub("", txt).strip()


def _strip_h1(txt: str) -> str:
    if txt.startswith("#"):
        return txt.split("\n", 1)[1].strip() if "\n" in txt else ""
    return txt


def _section(path: Path) -> str:
    """Read a canon front/back-matter file, cleaned, keeping its own leading '# ' heading so the
    EPUB splitter gives it its own section. Empty string if absent."""
    if not path.exists():
        return ""
    return _clean(path.read_text(encoding="utf-8"))


def _dedication_page() -> str:
    """PALINDROME's own dedication only. (Standalone: the standing dedication is retired.)
    Honours a leading <!-- NO_LIBRARY_DEDICATION --> marker for symmetry, though it is moot here."""
    own_raw = _section(CANON / "DEDICATION_BOOK.md")
    if not own_raw:
        return ""
    own = own_raw if own_raw.startswith("# ") else "# Dedication\n\n" + own_raw
    return own.strip()


def merge() -> Path:
    files = _chapters()
    if not files:
        sys.exit("  [skip] no chapters/")
    parts: list[str] = []
    # Front matter, in order: dedication, then the reader's note (the author's-note front matter).
    ded = _dedication_page()
    if ded:
        parts.append(ded + "\n")
    note = _section(CANON / "READER_NOTE.md")
    if note:
        parts.append((note if note.startswith("# ") else "# A Note\n\n" + note) + "\n")
    nch = 0
    nc_parts: list[str] = []
    for f in files:
        body = f.read_text(encoding="utf-8").rstrip()
        parts.append(body + "\n")
        nc_parts.append(body + "\n")
        nch += 1
    # Back matter: the reader's glossary, if present.
    glos = _section(CANON / "READER_GLOSSARY.md")
    if glos:
        parts.append((glos if glos.startswith("# ") else "# A Reader's Glossary\n\n" + glos) + "\n")
    BUILD.mkdir(parents=True, exist_ok=True)
    book = "\n\n".join(parts) + "\n"
    (BUILD / "BOOK.md").write_text(book, encoding="utf-8")
    nc_header = "<!-- Untitled — import title set in the novelcrafter dialog -->\n\n\n"
    (BUILD / "BOOK.novelcrafter.md").write_text(nc_header + "\n\n".join(nc_parts) + "\n", encoding="utf-8")
    words = len(book.split())
    print(f"  [ok] BOOK.md + novelcrafter ({nch} chapters, ~{words} words)")
    return BUILD / "BOOK.md"


def _split_sections(md: str) -> list[tuple[str, list[str]]]:
    out: list[tuple[str, list[str]]] = []
    cur_title: str | None = None
    cur: list[str] = []
    for ln in md.splitlines():
        m = re.match(r"^# (?!#)(.+)$", ln)
        if m:
            if cur_title is not None or cur:
                out.append((cur_title or "Front Matter", cur))
            cur_title = m.group(1).strip()
            cur = [ln]
        else:
            cur.append(ln)
    if cur_title is not None or cur:
        out.append((cur_title or "Front Matter", cur))
    return out


def epub() -> None:
    """Legacy stdlib-only EPUB (no cover/PDF) — fallback if the render gate is unavailable."""
    try:
        import markdown  # noqa
        from ebooklib import epub as _epub  # noqa
    except Exception as e:  # pragma: no cover
        sys.exit(f"  [epub] need markdown + ebooklib in the venv ({e}); run with ../../.venv/bin/python3")
    src = BUILD / "BOOK.md"
    md = src.read_text(encoding="utf-8")
    sections = _split_sections(md)
    book = _epub.EpubBook()
    book.set_identifier(f"urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, 'standalone/palindrome')}")
    book.set_title(TITLE)
    book.set_language("en")
    book.add_author(AUTHOR)
    book.add_metadata("DC", "publisher", "Arjuna Badger Press")
    md_exts = ["extra", "smarty", "sane_lists"]
    chapters = []
    for i, (title, body_lines) in enumerate(sections):
        import markdown as _m
        html = _m.markdown("\n".join(body_lines), extensions=md_exts)
        c = _epub.EpubHtml(title=title, file_name=f"sec_{i:02d}.xhtml", lang="en")
        c.content = f"<html><body>{html}</body></html>"
        book.add_item(c)
        chapters.append(c)
    book.toc = tuple(chapters)
    book.add_item(_epub.EpubNcx())
    book.add_item(_epub.EpubNav())
    book.spine = ["nav", *chapters]
    out_dir = BUILD / "export"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{TITLE}.epub"
    _epub.write_epub(str(out), book)
    print(f"  [ok] {out}  ({len(sections)} sections)")


def render_via_gate() -> None:
    """Render EPUB + PDF through the binding RENDER GATE (tools/render_book.sh): Atkinson body
    embedded, cover, colophon (ABP mark + Klaus crest). The gate is the single sanctioned render
    path (see tools/RENDER_GATE.md); the ebooklib epub() above is kept only as a stdlib fallback."""
    import subprocess
    repo = HERE.parent.parent                         # repo root
    gate = repo / "tools" / "render_book.sh"
    book_md = BUILD / "BOOK.md"
    out_base = BUILD / "export" / TITLE
    if not gate.exists():
        print(f"  [warn] render gate not found at {gate}; falling back to ebooklib epub()")
        epub()
        return
    out_base.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["bash", str(gate), str(book_md), str(out_base), TITLE, AUTHOR],
        check=True,
    )


if __name__ == "__main__":
    merge()
    if "--merge" not in sys.argv:
        if "--ebooklib" in sys.argv:
            epub()                # legacy stdlib-only EPUB (no cover/PDF)
        else:
            render_via_gate()     # default: full gate render (cover + colophon + PDF)

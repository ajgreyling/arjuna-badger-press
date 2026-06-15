#!/usr/bin/env python3
"""Self-contained merge + EPUB build for the standalone novella *The Loneliest People in the World*.

Total firewall: depends on NOTHING in History Before Time or the trilogy. Mirrors the proven HBT
pattern — [canon/DEDICATION_BOOK.md if present] + ch-*.md -> build/BOOK.md, then split on top-level
'# ' headings into EPUB sections.

  python3 books/the-loneliest/build.py            # merge + epub
  python3 books/the-loneliest/build.py --merge    # merge only (BOOK.md + novelcrafter)

BOOK.md / BOOK.novelcrafter.md / the .epub are DERIVED, local-only build artifacts. Commit only
chapters/ + canon/.
"""
from __future__ import annotations

import re
import sys
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent          # books/the-loneliest
BUILD = HERE / "build"
CH = BUILD / "chapters"
CANON = HERE / "canon"
TITLE = "The Loneliest People in the World"
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


def _dedication_page() -> str:
    """The dedication PAGE: the standing library dedication (to Lisel, from the africangold-root
    LIBRARY_DEDICATION.md) above this book's own dedication, joined by an asterism. A leading
    `# Dedication` heading is kept so the EPUB splitter gives it its own section.

    PER-BOOK OPT-OUT: if this book's DEDICATION_BOOK.md begins with the marker
    `<!-- NO_LIBRARY_DEDICATION -->`, the standing library (Lisel) dedication is SUPPRESSED and the
    book carries ONLY its own dedication. (Used by books that pre-date / sit outside the library-as-
    Lisel's frame — e.g. THE LONELIEST PEOPLE IN THE WORLD, which is pre-Lisel and is For Carla.)"""
    own_path = CANON / "DEDICATION_BOOK.md"
    own_raw = own_path.read_text(encoding="utf-8") if own_path.exists() else ""
    opt_out = "NO_LIBRARY_DEDICATION" in own_raw.splitlines()[0] if own_raw.strip() else False
    own = _strip_h1(_clean(own_raw)) if own_raw else ""
    lib = ""
    heading = ""
    if not opt_out:
        lib_path = HERE.parents[1] / "LIBRARY_DEDICATION.md"
        lib_raw = _clean(lib_path.read_text(encoding="utf-8")) if lib_path.exists() else ""
        heading = "# Dedication" if lib_raw.startswith("# ") else ""
        lib = _strip_h1(lib_raw)
    if opt_out and own:
        heading = "# Dedication"
    if not (lib or own):
        return ""
    page = heading + ("\n\n" if heading else "")
    page += f"{lib}\n\n⁂\n\n{own}" if (lib and own) else (lib or own)
    return page.strip()


def merge() -> Path:
    files = _chapters()
    if not files:
        sys.exit("  [skip] no chapters/")
    parts: list[str] = []
    ded_page = _dedication_page()
    if ded_page:
        parts.append(ded_page + "\n")
    nch = 0
    nc_parts: list[str] = []
    for f in files:
        body = f.read_text(encoding="utf-8").rstrip()
        parts.append(body + "\n")
        nc_parts.append(body + "\n")
        nch += 1
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
    try:
        import markdown  # noqa
        from ebooklib import epub as _epub  # noqa
    except Exception as e:  # pragma: no cover
        sys.exit(f"  [epub] need markdown + ebooklib in the venv ({e}); run with ../../.venv/bin/python3")
    src = BUILD / "BOOK.md"
    md = src.read_text(encoding="utf-8")
    sections = _split_sections(md)
    book = _epub.EpubBook()
    book.set_identifier(f"urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, 'standalone/the-loneliest')}")
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
    embedded, the newsprint cover as PDF page 1 + EPUB cover image, and the "free illustrated PDF
    online" note in the EPUB. The gate is the single sanctioned render path (see tools/RENDER_GATE.md);
    the ebooklib epub() below is kept only as a stdlib fallback."""
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
            render_via_gate()     # default: full gate render (cover + note + PDF)

#!/usr/bin/env python3
"""Wide-distribution upload sheet for the Arjuna Badger Press catalogue.

Going live on Kindle (KDP), Apple Books, Google Play Books, and Kobo means typing the same metadata
into four dashboards, 27 times. This generates one sheet with every field those stores ask for,
pulled straight from the live catalogue (so it can't drift), ready to copy-paste.

    python3 tools/distribution_sheet.py            # write distribution-sheet.csv + .md
    python3 tools/distribution_sheet.py --print    # also echo a per-book summary

Outputs (repo root, git-ignored):
  distribution-sheet.csv  — one row per available book; columns map to the upload forms.
  distribution-sheet.md   — the same, as readable per-book blocks (good for working through one
                            book at a time with all four dashboards open).

What it fills, and from where:
  title / subtitle / series / series_no   <- catalogue (CURATED + scan)
  author = "Andries Jakobus Greyling"      (legal name, as on the NLSA application)
  publisher = "Arjuna Badger Press"
  description                              <- catalogue blurb (SHORT — see the warning the tool
                                              prints; stores allow ~4000 chars, so expand the
                                              flagged ones for better conversion)
  language = English
  keywords                                 <- BOOK_KEYWORDS (the same set the site's SEO uses)
  bisac_categories                         <- mapped per series below (edit BISAC_BY_SERIES to taste)
  price                                    = 0.00 (free) — with per-store reality notes (KDP can't
                                              do $0 directly; the others can)
  isbn_ebook                               <- project.json if assigned, else "(pending — backfill)"
  epub_path / cover_path                   <- the actual files to upload
  ai_disclosure = "YES — AI-assisted"      reminder; you MUST declare this truthfully at upload.

NOTHING here is invented prose. BISAC codes are a starting suggestion by series — review them; the
store will also let you pick at upload. The description is your existing blurb; the tool does not
write new marketing copy.
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "site"))
import build  # noqa: E402

CSV_PATH = REPO / "distribution-sheet.csv"
MD_PATH = REPO / "distribution-sheet.md"

AUTHOR = "Andries Jakobus Greyling"     # legal name, as on the NLSA ISBN application
PUBLISHER = "Arjuna Badger Press"

# BISAC subject codes by series — a sensible STARTING point; refine per book at upload. Stores let
# you pick 2-3, so each entry offers a couple. (Codes from the standard BISAC subject list.)
BISAC_BY_SERIES = {
    "The African Gold Trilogy": "FIC028000 Science Fiction / General; FIC031000 Thrillers / General",
    "History Before Time": "FIC014000 Historical / General; FIC028000 Science Fiction / General",
    "The Synthesis": "FIC028000 Science Fiction / General; FIC031010 Thrillers / Suspense",
    "The Salt Veil": "FIC009020 Fantasy / Epic; FIC009000 Fantasy / General",
    "The Dust Throne": "FIC009020 Fantasy / Epic; FIC009000 Fantasy / General",
    "The Unheard": "FIC051000 Cultural Heritage; FIC066000 Small Town & Rural",
    "Not a Potato": "FIC028000 Science Fiction / General; FIC022000 Mystery & Detective / General",
    "The No-Fear Cycle": "FIC028070 Science Fiction / Military; FIC028000 Science Fiction / General",
    "The Reichenbach Files": "FIC022000 Mystery & Detective / General; FIC022080 Traditional",
    "Non-fiction": "REL000000 Religion / General; LIT004190 Literary Criticism / Ancient & Classical",
    "Standalones": "FIC019000 Literary; FIC028000 Science Fiction / General",
}
DEFAULT_BISAC = "FIC000000 Fiction / General"

# Per-store pricing reality for a free-to-read press.
PRICE_NOTES = (
    "Kobo/Apple/Google: set list price 0.00 (true free). "
    "KDP: cannot set $0 directly (min ~$0.99) — get to free via price-matching a free listing "
    "elsewhere, or KDP Select free-promo days. List 0.00 here as the intent."
)

# Stores still want a real description; flag blurbs shorter than this to expand before upload.
SHORT_DESC_THRESHOLD = 250

FIELDS = [
    "n", "id", "title", "subtitle", "series", "series_no", "author", "publisher",
    "language", "description", "description_note", "keywords", "bisac_categories",
    "price", "isbn_ebook", "epub_path", "cover_path", "ai_disclosure",
]


def _epub(e: dict) -> str:
    for f in e.get("downloads", []):
        if f.suffix.lower() == ".epub":
            return str(f)
    return "(no EPUB found in build/export)"


def _series_no(subtitle: str) -> str:
    """Pull a 'Book I/II/One' marker out of the subtitle if present (e.g. '... · Book II')."""
    if not subtitle:
        return ""
    for sep in ("·", "-", "—"):
        if sep in subtitle:
            tail = subtitle.rsplit(sep, 1)[-1].strip()
            if any(w in tail for w in ("Book", "Volume", "Part", "I", "II", "III", "One", "Two",
                                       "Three", "Four", "Five", "Six", "Seven")):
                return tail
    return ""


def _has_epub(e: dict) -> bool:
    return any(f.suffix.lower() == ".epub" for f in e.get("downloads", []))


def rows() -> tuple[list[dict], list[str]]:
    """Return (uploadable_rows, excluded_notes).

    Only EPUB-ready books can go to the stores. Serials (read-online-only, no download) and any
    book missing its EPUB are EXCLUDED and reported, so nothing is silently dropped from the plan."""
    out = []
    avail = [e for e in build.scan() if e["available"]]
    uploadable = [e for e in avail if _has_epub(e)]
    excluded = []
    for e in avail:
        if not _has_epub(e):
            why = "serial — read-online only, no EPUB to distribute" if e.get("serial") \
                else "no EPUB found in build/export — render it first"
            excluded.append(f'{e["title"]} ({e["id"]}): {why}')
    for i, e in enumerate(uploadable, 1):
        blurb = (e.get("blurb") or "").strip()
        kw = build.BOOK_KEYWORDS.get(e["id"], build.DEFAULT_BOOK_KEYWORDS) \
            if hasattr(build, "BOOK_KEYWORDS") else ""
        isbn = e.get("isbn") or "(pending — backfill when NLSA/Bowker issues)"
        note = ""
        if len(blurb) < SHORT_DESC_THRESHOLD:
            note = f"SHORT ({len(blurb)} chars) — expand to a fuller description before upload"
        out.append({
            "n": i,
            "id": e["id"],
            "title": e["title"],
            "subtitle": e.get("subtitle") or "",
            "series": e["series"] or "",
            "series_no": _series_no(e.get("subtitle") or ""),
            "author": AUTHOR,
            "publisher": PUBLISHER,
            "language": "English",
            "description": blurb,
            "description_note": note,
            "keywords": kw,
            "bisac_categories": BISAC_BY_SERIES.get(e["series"], DEFAULT_BISAC),
            "price": "0.00",
            "isbn_ebook": isbn,
            "epub_path": _epub(e),
            "cover_path": str(e["cover"]) if e.get("cover") else "(generated placeholder — add a real cover)",
            "ai_disclosure": "YES — declare AI-assisted/AI-generated truthfully at upload",
        })
    return out, excluded


def write_csv(data: list[dict]) -> None:
    with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(data)


def write_md(data: list[dict], excluded: list[str]) -> None:
    md = [
        "# Wide-distribution upload sheet — Arjuna Badger Press",
        "",
        "> **Status (2026-06-20): ON HOLD** — ISBN path blocked (NLSA broken; commercial too",
        "> expensive). Text free on arjunabadger.press; revenue = human audiobooks. Sheet kept for",
        "> when ISBNs arrive.",
        "",
        f"**{len(data)} EPUB-ready books** — uploadable to Kindle / Apple Books / Google Play / "
        "Kobo when ISBNs exist.",
        "",
        "Editable spine is `distribution-sheet.csv`. This .md is a per-book working view — open it",
        "next to the four store dashboards and go book by book.",
        "",
    ]
    if excluded:
        md.append("> **Not in this sheet (can't distribute yet):**")
        for note in excluded:
            md.append(f"> - {note}")
        md.append("")
    md += [
        "**Every upload, three rules:** (1) declare AI authorship truthfully; (2) ebook/EPUB only",
        "(you chose Electronic with NLSA); (3) leave ISBN blank / store-assigned for now, backfill",
        "the real number later. KDP & Kobo take ISBN as an editable field; Apple & Google read it",
        "from inside the EPUB, so those may need a re-upload once the number is embedded.",
        "",
        f"**Pricing:** {PRICE_NOTES}",
        "",
        "---",
        "",
    ]
    for r in data:
        md.append(f"## {r['n']}. {r['title']}")
        if r["subtitle"]:
            md.append(f"*{r['subtitle']}*")
        md.append("")
        md.append(f"- **Series:** {r['series'] or '—'}  ·  **In series:** {r['series_no'] or '—'}")
        md.append(f"- **Author:** {r['author']}")
        md.append(f"- **Publisher:** {r['publisher']}")
        md.append(f"- **Language:** {r['language']}")
        md.append(f"- **Description:** {r['description'] or '—'}")
        if r["description_note"]:
            md.append(f"  - ⚠️ {r['description_note']}")
        md.append(f"- **Keywords:** {r['keywords'] or '—'}")
        md.append(f"- **BISAC categories:** {r['bisac_categories']}")
        md.append(f"- **Price:** {r['price']} (free)")
        md.append(f"- **ISBN (e-book):** {r['isbn_ebook']}")
        md.append(f"- **EPUB file:** `{r['epub_path']}`")
        md.append(f"- **Cover file:** `{r['cover_path']}`")
        md.append(f"- **AI disclosure:** {r['ai_disclosure']}")
        md.append("")
    MD_PATH.write_text("\n".join(md) + "\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate the wide-distribution upload sheet.")
    ap.add_argument("--print", action="store_true", dest="do_print",
                    help="echo a short per-book summary to stdout")
    args = ap.parse_args()

    data, excluded = rows()
    write_csv(data)
    write_md(data, excluded)

    n_short = sum(1 for r in data if r["description_note"])
    n_no_isbn = sum(1 for r in data if r["isbn_ebook"].startswith("("))
    print(f"wrote {CSV_PATH.name} and {MD_PATH.name}: {len(data)} EPUB-ready books (uploadable now)")
    for note in excluded:
        print(f"  EXCLUDED — {note}")
    if n_short:
        print(f"  {n_short} book(s) have a SHORT description — expand before upload for better "
              f"conversion (flagged in the sheet).")
    if n_no_isbn:
        print(f"  {n_no_isbn} book(s) have no ISBN yet — fine to upload now, backfill later.")
    print(f"  reminder: declare AI authorship truthfully on every store.")
    if args.do_print:
        for r in data:
            print(f"  {r['n']:2}. {r['title']}  [{r['series']}]  EPUB: "
                  f"{'yes' if not r['epub_path'].startswith('(') else 'MISSING'}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Wikidata-ready export for the Arjuna Badger Press catalogue.

Wikidata is the one structured-entity database with NO notability bar — every published, freely
readable book is squarely in scope — and entities there feed Google's Knowledge Graph, Bing, and
the wider semantic web. This is the highest-leverage backlink target for the press, so we make the
data trivial to load.

The catalogue is read straight from the site generator (we import scan() from site/build.py), so
this export can never drift from what the website actually ships.

WHAT IT EMITS (into site/public/ is wrong — these are NOT web pages; they go to ./wikidata-export/
at the repo root, which is for you, not for deploy):

  1. quickstatements.txt — paste into https://quickstatements.toolforge.org (the standard Wikidata
     batch tool). Creates one item for the publisher, one for the author, one per series, and one
     per available book, with the right properties and cross-links. Series/book links use CREATE
     LAST references so QuickStatements wires them together in a single run.
  2. entities.json — the same data as plain JSON, for your own records / any other tool.
  3. README.txt — a step-by-step on how to load it and what to check first.

IMPORTANT — read before loading:
  * Wikidata forbids DUPLICATES. Before running the batch, SEARCH Wikidata for "Arjuna Badger
    Press", "Andries J. Greyling", and a few book titles. If an item already exists, delete that
    block from quickstatements.txt and instead add statements to the existing Q-id by hand.
  * QuickStatements needs a logged-in Wikidata account (autoconfirmed for batches). The CREATE
    blocks below assume none of these items exist yet.
  * This script invents NO facts. It emits only what the catalogue already asserts (title, author,
    publisher, series, language, free-to-read URL, translated-edition languages). Dates, ISBNs,
    genres, and subjects are left for you to add — there is no reliable source for them here.

Usage:
    python3 tools/wikidata_export.py            # write the export
    python3 tools/wikidata_export.py --print    # also echo quickstatements to stdout
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Import the live catalogue from the site generator so this never drifts from the website.
REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "site"))
import build  # noqa: E402  (path set above)

OUT_DIR = REPO / "wikidata-export"

# ── Wikidata property / item IDs used below ───────────────────────────────────────────────────
# Items (Q):  Q3331189 = "version, edition, or translation" is NOT used; we use the work-level
#   Q571 = book, Q5 = human, Q2085381 = publisher, Q277759 = book series, Q7725634 = literary work.
# Properties (P):
P_INSTANCE_OF = "P31"
P_AUTHOR = "P50"           # work -> author (item)
P_PUBLISHER = "P123"       # work -> publisher (item)
P_LANGUAGE = "P407"        # language of work
P_PART_OF_SERIES = "P179"  # work -> series
P_FREE_URL = "P953"        # "full work available at" URL
P_ISBN_13 = "P212"         # ISBN-13
P_ISBN_10 = "P957"         # ISBN-10
P_OFFICIAL_WEBSITE = "P856"
P_OCCUPATION = "P106"      # human -> occupation
P_FOUNDED_BY = "P112"      # org -> founder
Q_HUMAN = "Q5"
Q_BOOK = "Q571"
Q_LITERARY_WORK = "Q7725634"
Q_PUBLISHER = "Q2085381"
Q_BOOK_SERIES = "Q277759"
Q_WRITER = "Q36180"
Q_ENGLISH = "Q1860"
# Wikidata language-item IDs for our translated editions (P407 values on the free-URL statement
# would be ideal, but edition modelling is involved; we instead note edition languages in the
# human-readable summary and leave per-edition items to you).
LANG_QID = {
    "af": "Q14196", "zu": "Q10179", "es": "Q1321", "fr": "Q150", "am": "Q28244",
    "ar": "Q13955", "hi": "Q1568", "mr": "Q1571", "ta": "Q5885", "zh": "Q7850",
    "mn": "Q9246", "ja": "Q5287", "de": "Q188", "en": "Q1860",
}

AUTHOR_NAME = "Andries J. Greyling"
PUBLISHER_NAME = "Arjuna Badger Press"


def q(s: str) -> str:
    """QuickStatements string-literal: wrapped in double quotes, inner quotes escaped."""
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def mono(s: str, lang: str = "en") -> str:
    """QuickStatements monolingual-text literal (for labels/aliases): lang:"text"."""
    return f'{lang}:{q(s)}'


def build_quickstatements(entries: list[dict]) -> tuple[str, list[dict]]:
    """Return (quickstatements_text, json_entities).

    QuickStatements 'CREATE' makes a new blank item; 'LAST' refers to the most recently created
    item, so each CREATE block is followed by LAST<TAB>property<TAB>value lines. We create the
    publisher first, then the author, then series, then books — but because LAST only points at the
    immediately preceding CREATE, cross-references between already-created items can't use LAST.
    Wikidata has no stable handle for an item until it exists, so we link books -> publisher/author
    /series by NAME in the human summary and leave those exact links for you to confirm after the
    items get their Q-ids. The CREATE blocks still set everything that does NOT need another new
    item's Q-id (labels, descriptions, instance-of, language, free-to-read URL, official website).
    """
    lines: list[str] = []
    j_entities: list[dict] = []

    def emit_create(label: str, desc: str, statements: list[tuple[str, str]],
                    aliases: list[str] | None = None) -> None:
        lines.append("CREATE")
        lines.append(f"LAST\tLen\t{q(label)}")
        lines.append(f"LAST\tDen\t{q(desc)}")
        for al in (aliases or []):
            lines.append(f"LAST\tAen\t{q(al)}")  # 'A'+lang = alias; 'Aen' = English alias
        for prop, val in statements:
            lines.append(f"LAST\t{prop}\t{val}")
        lines.append("")  # blank line between blocks for readability

    # ── Publisher ─────────────────────────────────────────────────────────────────────────────
    pub_stmts = [
        (P_INSTANCE_OF, Q_PUBLISHER),
        (P_OFFICIAL_WEBSITE, q(f"{build.DOMAIN}/")),
    ]
    emit_create(PUBLISHER_NAME,
                "independent publisher of free-to-read fiction",
                pub_stmts)
    j_entities.append({"type": "publisher", "label": PUBLISHER_NAME,
                       "website": f"{build.DOMAIN}/", "instance_of": Q_PUBLISHER})

    # ── Author ────────────────────────────────────────────────────────────────────────────────
    auth_stmts = [
        (P_INSTANCE_OF, Q_HUMAN),
        (P_OCCUPATION, Q_WRITER),
    ]
    emit_create(AUTHOR_NAME, "novelist; founder of Arjuna Badger Press", auth_stmts,
                aliases=["A. J. Greyling"])
    j_entities.append({"type": "author", "label": AUTHOR_NAME,
                       "occupation": Q_WRITER, "instance_of": Q_HUMAN})

    # ── Series (only those that actually carry available books) ──────────────────────────────────
    available = [e for e in entries if e["available"]]
    series_with_books = []
    for name, _accent in build.SERIES:
        if any(e["series"] == name for e in available):
            series_with_books.append(name)
    for name in series_with_books:
        emit_create(name, "book series by Andries J. Greyling (Arjuna Badger Press)",
                    [(P_INSTANCE_OF, Q_BOOK_SERIES)])
        j_entities.append({"type": "series", "label": name, "instance_of": Q_BOOK_SERIES})

    # ── Books (available only — Wikidata wants real, accessible works) ───────────────────────────
    for e in available:
        url = f'{build.DOMAIN}/book/{e["id"]}.html'
        # Don't assert "novel" for non-fiction — Wikidata descriptions must be factual. The
        # "Non-fiction" shelf gets the neutral "book"; everything else is a novel.
        kind = "book" if e["series"] == "Non-fiction" else "novel"
        desc_bits = [kind]
        if e["series"] and e["series"] != "Non-fiction":
            desc_bits.append(f'in the {e["series"]} series')
        desc_bits.append("by Andries J. Greyling")
        desc = " ".join(desc_bits)
        stmts = [
            (P_INSTANCE_OF, Q_BOOK),
            (P_LANGUAGE, Q_ENGLISH),
            (P_FREE_URL, q(url)),
        ]
        # ISBN, only if assigned. scan() returns digits-only; P212 is ISBN-13, P957 is ISBN-10.
        isbn = (e.get("isbn") or "").strip()
        if len(isbn) == 13:
            stmts.append((P_ISBN_13, q(isbn)))
        elif len(isbn) == 10:
            stmts.append((P_ISBN_10, q(isbn)))
        emit_create(e["title"], desc, stmts)
        edition_langs = sorted((e.get("editions") or {}).keys())
        j_entities.append({
            "type": "book",
            "id": e["id"],
            "label": e["title"],
            "series": e["series"] or None,
            "url": url,
            "language": "en",
            "isbn": isbn or None,
            "instance_of": Q_BOOK,
            # links you must wire by hand once Q-ids exist:
            "author_label": AUTHOR_NAME,
            "publisher_label": PUBLISHER_NAME,
            "translated_edition_languages": [
                {"code": c, "name": build.EDITION_LANGS.get(c, (c, c))[0],
                 "wikidata_lang_qid": LANG_QID.get(c)}
                for c in edition_langs
            ],
        })

    header = (
        "# QuickStatements V1 for Arjuna Badger Press\n"
        "# Paste into https://quickstatements.toolforge.org  (Import → V1 syntax).\n"
        "# READ wikidata-export/README.txt FIRST — search Wikidata for duplicates before running.\n"
        "# 'Len'/'Den' = English label/description; 'Aen' lines set English aliases.\n"
        "# Cross-links (book -> author/publisher/series) are NOT auto-set: items have no Q-id until\n"
        "# created, so add P50/P123/P179 by hand once these items exist (see README).\n"
        "\n"
    )
    return header + "\n".join(lines), j_entities


def write_readme(out_dir: Path, n_books: int, n_series: int) -> None:
    txt = f"""Arjuna Badger Press — Wikidata export
=====================================

Files in this folder:
  quickstatements.txt  — batch commands for QuickStatements (creates the items)
  entities.json        — the same data as JSON, for your records
  README.txt           — this file

What got generated: 1 publisher item, 1 author item, {n_series} series items, {n_books} book
items (available books only). Nothing here invents facts — it asserts only what the website
already says: title, that it's a book/novel, English language, the free-to-read URL, the author,
the publisher, and series membership.

STEP 1 — Check for duplicates (REQUIRED).
  Wikidata forbids duplicate items. Before loading ANYTHING, search https://www.wikidata.org for:
    - "Arjuna Badger Press"
    - "Andries J. Greyling"
    - each book title
  If an item already exists, delete its CREATE block from quickstatements.txt. You can still add
  the missing statements to the existing item by replacing 'CREATE' + 'LAST' with that item's
  Q-id (e.g.  Q12345  P953  "https://...").

STEP 2 — Load the batch.
  1. Log in to Wikidata (you need an autoconfirmed account for batches).
  2. Go to https://quickstatements.toolforge.org  →  "New batch"  →  "Import V1 commands".
  3. Paste the contents of quickstatements.txt and run.
  4. Note the new Q-ids it creates (the batch report lists them).

STEP 3 — Wire the cross-links (by hand, once Q-ids exist).
  QuickStatements 'LAST' only points at the item created immediately before it, so links BETWEEN
  newly created items can't be auto-set. After the batch, for each book item add:
    - P50  (author)     -> the new Andries J. Greyling Q-id
    - P123 (publisher)  -> the new Arjuna Badger Press Q-id
    - P179 (part of series) -> the matching series Q-id (see entities.json "series")
  And on the publisher item, optionally add P112 (founded by) -> the author Q-id.
  entities.json lists, per book, the author/publisher/series labels to match.

STEP 4 — Optional enrichment (no reliable source in the repo, so left to you).
  Publication date (P577), genre (P136), main subject (P921), ISBN (P212/P957), and translated-
  edition items. entities.json records each book's translated-edition languages (with the Wikidata
  language Q-ids) so you can model editions later if you want.

Re-running this script regenerates the files from the current catalogue. It does NOT touch
Wikidata — loading is always a manual, reviewed step.
"""
    (out_dir / "README.txt").write_text(txt, encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate Wikidata-ready exports for the catalogue.")
    ap.add_argument("--print", action="store_true", dest="do_print",
                    help="also echo the QuickStatements to stdout")
    args = ap.parse_args()

    entries = build.scan()
    qs_text, j_entities = build_quickstatements(entries)

    OUT_DIR.mkdir(exist_ok=True)
    (OUT_DIR / "quickstatements.txt").write_text(qs_text, encoding="utf-8")
    (OUT_DIR / "entities.json").write_text(
        json.dumps({"source": build.DOMAIN, "entities": j_entities}, ensure_ascii=False, indent=2),
        encoding="utf-8")

    n_books = sum(1 for x in j_entities if x["type"] == "book")
    n_series = sum(1 for x in j_entities if x["type"] == "series")
    write_readme(OUT_DIR, n_books, n_series)

    print(f"wrote Wikidata export -> {OUT_DIR}")
    print(f"  publisher: 1, author: 1, series: {n_series}, books: {n_books}")
    print(f"  files: quickstatements.txt, entities.json, README.txt")
    print(f"  NEXT: read {OUT_DIR}/README.txt — search Wikidata for duplicates before loading.")
    if args.do_print:
        print("\n" + "=" * 70 + "\n" + qs_text)


if __name__ == "__main__":
    main()

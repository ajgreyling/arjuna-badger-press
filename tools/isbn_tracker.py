#!/usr/bin/env python3
"""ISBN allocation tracker for the Arjuna Badger Press catalogue.

Going wide (Kindle, Apple Books, Google Play, Kobo) means every title needs its own ISBN, and
ISBNs are per-FORMAT: the EPUB and a sold PDF are different numbers; Kindle uses a free ASIN and
needs none. Across the whole catalogue that's a few dozen numbers to assign without losing track —
which one went to which book, which are still free in the block. This tool is the ledger.

It reads the live catalogue from the site generator (so the book list can't drift) and supports a
round-trip so you never hand-edit dozens of project.json files:

    python3 tools/isbn_tracker.py export      # write isbn-tracker.csv (+ .md view) from project.json
    python3 tools/isbn_tracker.py import       # read isbn-tracker.csv back INTO each project.json
    python3 tools/isbn_tracker.py import --dry  # show what import WOULD change, write nothing
    python3 tools/isbn_tracker.py status        # quick summary: assigned vs unassigned

Workflow:
  1. `export` — generates isbn-tracker.csv, one row per book, pre-filled with any ISBNs already in
     project.json. Columns: id, title, series, available, asin, isbn_ebook, isbn_paperback,
     isbn_hardcover, notes.
  2. When your ISBN block arrives, open the CSV in any spreadsheet and paste numbers into the
     isbn_* columns (and the ASIN once Kindle assigns it). Hyphens are fine; they're normalised.
  3. `import` — writes those numbers back into each book's project.json `isbn` block. Then rebuild
     the site (python3 site/build.py) and the numbers flow to the page, JSON-LD, and Wikidata
     export. `import --dry` first if you want to see the diff.

The CSV is the editable source of truth between block-arrival and import. It lives at the repo root
(./isbn-tracker.csv) and, like the other generated artifacts, is git-ignored.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "site"))
import build  # noqa: E402

CSV_PATH = REPO / "isbn-tracker.csv"
MD_PATH = REPO / "isbn-tracker.md"

FIELDS = ["id", "title", "series", "available", "asin",
          "isbn_ebook", "isbn_paperback", "isbn_hardcover", "notes"]
_CLEAN = re.compile(r"[^0-9Xx]")


def _proj_path(entry: dict) -> Path:
    return entry["root"] / "project.json"


def _load_proj(entry: dict) -> dict:
    p = _proj_path(entry)
    if not p.is_file():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return {}


def _norm_isbn(raw: str) -> str:
    """Digits-only (hyphens/spaces stripped), upper-cased. Blank/placeholder -> ''."""
    cleaned = _CLEAN.sub("", (raw or "")).upper()
    if len(cleaned) == 13 and cleaned.isdigit():
        return cleaned
    if len(cleaned) == 10 and cleaned[:9].isdigit() and cleaned[9] in "0123456789X":
        return cleaned
    return ""


def cmd_export() -> None:
    entries = build.scan()
    rows = []
    for e in entries:
        proj = _load_proj(e)
        isbn = proj.get("isbn") or {}
        rows.append({
            "id": e["id"],
            "title": e["title"],
            "series": e["series"] or "",
            "available": "yes" if e["available"] else "no",
            "asin": (proj.get("asin") or ""),
            "isbn_ebook": (isbn.get("ebook") or ""),
            "isbn_paperback": (isbn.get("paperback") or ""),
            "isbn_hardcover": (isbn.get("hardcover") or ""),
            "notes": "",
        })
    rows.sort(key=lambda r: (r["available"] != "yes", r["series"], r["title"]))

    with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)

    # Markdown view — read-only, for a glance; the CSV is the editable one.
    md = ["# ISBN allocation — Arjuna Badger Press",
          "",
          "Editable source is `isbn-tracker.csv` (this .md is a generated view). "
          "Fill the CSV, then `python3 tools/isbn_tracker.py import`.",
          "",
          "| Book | Series | Available | e-book ISBN | paperback | hardcover | ASIN |",
          "|------|--------|-----------|-------------|-----------|-----------|------|"]
    for r in rows:
        md.append(f"| {r['title']} | {r['series']} | {r['available']} | "
                  f"{r['isbn_ebook'] or '—'} | {r['isbn_paperback'] or '—'} | "
                  f"{r['isbn_hardcover'] or '—'} | {r['asin'] or '—'} |")
    MD_PATH.write_text("\n".join(md) + "\n", encoding="utf-8")

    n_avail = sum(1 for r in rows if r["available"] == "yes")
    print(f"wrote {CSV_PATH.name} and {MD_PATH.name}: {len(rows)} books ({n_avail} available)")
    print(f"  edit {CSV_PATH.name} (isbn_* / asin columns), then: "
          f"python3 tools/isbn_tracker.py import")


def cmd_import(dry: bool) -> None:
    if not CSV_PATH.is_file():
        sys.exit(f"no {CSV_PATH.name} — run `export` first, fill it in, then import.")
    by_id = {e["id"]: e for e in build.scan()}
    with CSV_PATH.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    changes, skipped, missing = [], 0, []
    for r in rows:
        cid = (r.get("id") or "").strip()
        e = by_id.get(cid)
        if not e:
            missing.append(cid)
            continue
        p = _proj_path(e)
        if not p.is_file():
            # No project.json to write into — flag it; we don't fabricate one silently.
            if any(_norm_isbn(r.get(k, "")) or (r.get("asin") or "").strip()
                   for k in ("isbn_ebook", "isbn_paperback", "isbn_hardcover")):
                missing.append(f"{cid} (no project.json)")
            continue
        proj = _load_proj(e)
        isbn_block = dict(proj.get("isbn") or {})
        before = (isbn_block.get("ebook", ""), isbn_block.get("paperback", ""),
                  isbn_block.get("hardcover", ""), proj.get("asin", ""))

        new_ebook = _norm_isbn(r.get("isbn_ebook", "")) or isbn_block.get("ebook", "")
        new_paper = _norm_isbn(r.get("isbn_paperback", "")) or isbn_block.get("paperback", "")
        new_hard = _norm_isbn(r.get("isbn_hardcover", "")) or isbn_block.get("hardcover", "")
        new_asin = (r.get("asin") or "").strip() or proj.get("asin", "")
        after = (new_ebook, new_paper, new_hard, new_asin)

        if after == before:
            skipped += 1
            continue

        if not dry:
            isbn_block["ebook"] = new_ebook
            isbn_block["paperback"] = new_paper
            isbn_block["hardcover"] = new_hard
            proj["isbn"] = isbn_block
            if new_asin:
                proj["asin"] = new_asin
            p.write_text(json.dumps(proj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        changes.append((cid, before, after))

    verb = "WOULD change" if dry else "changed"
    print(f"{verb} {len(changes)} book(s); {skipped} unchanged.")
    for cid, before, after in changes:
        print(f"  {cid}: ebook {before[0]!r}->{after[0]!r}  "
              f"paper {before[1]!r}->{after[1]!r}  hard {before[2]!r}->{after[2]!r}  "
              f"asin {before[3]!r}->{after[3]!r}")
    if missing:
        print(f"  WARNING — rows with no matching/writable book: {', '.join(missing)}")
    if not dry and changes:
        print("  NEXT: python3 site/build.py  (flows ISBNs to pages, JSON-LD, Wikidata export)")


def cmd_status() -> None:
    entries = build.scan()
    avail = [e for e in entries if e["available"]]
    with_ebook = [e for e in avail if e.get("isbn")]
    print(f"catalogue: {len(entries)} books, {len(avail)} available")
    print(f"e-book ISBN assigned: {len(with_ebook)}/{len(avail)} available books")
    missing = [e["title"] for e in avail if not e.get("isbn")]
    if missing:
        print(f"  still unassigned ({len(missing)}): "
              f"{', '.join(missing[:12])}{'…' if len(missing) > 12 else ''}")
    else:
        print("  every available book has an e-book ISBN.")


def main() -> None:
    ap = argparse.ArgumentParser(description="ISBN allocation tracker (round-trips project.json).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("export", help="write isbn-tracker.csv (+ .md) from project.json")
    imp = sub.add_parser("import", help="write isbn-tracker.csv back into project.json files")
    imp.add_argument("--dry", action="store_true", help="show changes without writing")
    sub.add_parser("status", help="summary of assigned vs unassigned ISBNs")
    args = ap.parse_args()

    if args.cmd == "export":
        cmd_export()
    elif args.cmd == "import":
        cmd_import(args.dry)
    elif args.cmd == "status":
        cmd_status()


if __name__ == "__main__":
    main()

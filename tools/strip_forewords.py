#!/usr/bin/env python3
"""Strip the AI-generated vanity FOREWORD from book manuscripts.

Every vanity foreword has the same fingerprint:
    # Foreword
    ### *by <pseudonym>* †          (an anagram/fake byline; the † footnotes the joke)
    ...prose...
    ---                              (optional trailing rule)
    # <next H1>                      ← the foreword ends here (first chapter / next section)

We excise from the top-level `# Foreword` heading up to (but NOT including) the next
top-level `# ` heading. We DELIBERATELY do not touch:
  - `## Image Compendium — Foreword` (an image-appendix section, not the vanity piece),
  - any `# Dedication` / copyright / real author matter above it,
  - the first chapter below it.

Safety: only a heading that is EXACTLY `# Foreword` (H1) qualifies. A `## `/`### ` foreword,
or one whose body does NOT carry the tell-tale `### *by ... †` byline, is reported and SKIPPED
unless --force is given, so we never silently cut something unexpected.

Usage:
    tools/strip_forewords.py            # DRY RUN — show what would be removed
    tools/strip_forewords.py --apply    # actually rewrite the files
"""
from __future__ import annotations
import argparse, re, sys
from pathlib import Path

H1 = re.compile(r"^# (?!Foreword\b).+", )           # any H1 that's NOT the foreword
FOREWORD_H1 = re.compile(r"^# Foreword\s*$")
BYLINE = re.compile(r"^#{2,3} \*by .+\*")            # "### *by <name>*" (the vanity tell)


def find_books() -> list[Path]:
    base = Path("books")
    return sorted(p for p in base.rglob("BOOK.md") if "/_comingsoon/" not in p.as_posix())


def excise(lines: list[str]) -> tuple[list[str], dict] | None:
    """Return (new_lines, info) if a vanity foreword was found & removed, else None."""
    start = None
    for i, ln in enumerate(lines):
        if FOREWORD_H1.match(ln):
            start = i
            break
    if start is None:
        return None
    # find the end: the next H1 heading after the foreword
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if H1.match(lines[j]):
            end = j
            break
    block = lines[start:end]
    has_byline = any(BYLINE.match(b) for b in block)
    info = {
        "start": start + 1, "end": end,            # 1-based, end exclusive
        "removed_lines": end - start,
        "has_byline": has_byline,
        "byline": next((b.strip() for b in block if BYLINE.match(b)), None),
        "preview_head": block[0].strip(),
        "next_heading": lines[end].strip() if end < len(lines) else "(EOF)",
    }
    # Trim a leading blank line left behind so we don't accrue blank gaps.
    new = lines[:start] + lines[end:]
    while start < len(new) and new[start].strip() == "" and (start == 0 or new[start-1].strip() == ""):
        del new[start]
    return new, info


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write changes (default: dry run)")
    ap.add_argument("--force", action="store_true", help="strip even without the *by ...* byline")
    a = ap.parse_args()

    touched, skipped = 0, []
    for book in find_books():
        lines = book.read_text(encoding="utf-8").splitlines(keepends=True)
        res = excise(lines)
        if res is None:
            continue
        new, info = res
        rel = book.as_posix().replace("books/", "")
        if not info["has_byline"] and not a.force:
            skipped.append((rel, info))
            print(f"  SKIP  {rel}: '# Foreword' found but no '*by ...*' byline "
                  f"(lines {info['start']}-{info['end']}). Use --force if intended.")
            continue
        print(f"  {'STRIP' if a.apply else 'would strip'}  {rel}: "
              f"lines {info['start']}–{info['end']} ({info['removed_lines']} lines), "
              f"byline={info['byline']!r} → next: {info['next_heading']!r}")
        if a.apply:
            book.write_text("".join(new), encoding="utf-8")
            touched += 1

    print()
    if a.apply:
        print(f"Applied: stripped foreword from {touched} book(s). Skipped {len(skipped)}.")
    else:
        print("DRY RUN — no files changed. Re-run with --apply to strip.")


if __name__ == "__main__":
    main()

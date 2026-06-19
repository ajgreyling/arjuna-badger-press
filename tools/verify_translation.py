#!/usr/bin/env python3
"""Arjuna Badger Press — translation preserve-list verifier.

A structural safety net that does NOT trust the translator's self-report. For each
translated edition (build/BOOK.<code>.md), it checks that the deliberately-untranslated
tokens which appear in the SOURCE also appear in the TRANSLATION, verbatim.

We only assert on the highest-stakes class — `in_language_terms` (the isiZulu phrases
that must survive into every edition) — plus a sampled check on invented_entities and
multi-word proper names. Single-word common-ish names are skipped (a name like "Mother"
or "Priya" can legitimately be absent from / inflected in a given edition); the point is
to catch a translator who dissolved 'Umuntu ngumuntu ngabantu' or renamed 'Guardian',
not to demand every name appear identically.

Usage:
    tools/verify_translation.py books/resonance              # all declared codes
    tools/verify_translation.py books/resonance --code af    # one edition
Exit code is non-zero if any required token present in the source is missing from a
translation.
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def check_edition(source: str, translated: str, preserve: dict) -> list[str]:
    pv = preserve["preserve_verbatim_all_languages"]
    problems: list[str] = []

    # 1) in_language_terms — every such token in source MUST be in translation.
    for lang, terms in pv.get("in_language_terms", {}).items():
        for t in terms:
            if t in source and t not in translated:
                problems.append(f"[in_language:{lang}] '{t}' is in source but MISSING from translation")

    # 2) invented entities — check the distinctive core (before any '(' qualifier).
    for ent in pv.get("invented_entities", []):
        core = ent.split("(")[0].strip()
        if len(core) >= 4 and core in source and core not in translated:
            problems.append(f"[invented] '{core}' is in source but MISSING from translation")

    # 3) multi-word proper names (distinctive) — single-word names are too noisy to assert.
    for nm in pv.get("proper_names", []):
        if len(nm.split()) >= 2 and "/" not in nm and nm in source and nm not in translated:
            problems.append(f"[name] '{nm}' is in source but MISSING from translation")

    return problems


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("book_dir", type=Path)
    ap.add_argument("--code", help="check only this language code")
    a = ap.parse_args()

    book = a.book_dir
    manifest = load(book / "LANGUAGES.json")
    preserve = load(book / manifest["glossary_preserve"])
    source = (book / manifest["source"]).read_text(encoding="utf-8")

    codes = [a.code] if a.code else [t["code"] for t in manifest["targets"]]
    any_fail = False
    for code in codes:
        ed = book / "build" / f"BOOK.{code}.md"
        if not ed.is_file():
            print(f"  {code}: NOT BUILT ({ed.name} missing) — skipping")
            continue
        problems = check_edition(source, ed.read_text(encoding="utf-8"), preserve)
        if problems:
            any_fail = True
            print(f"  {code}: ✗ {len(problems)} preserve violation(s)")
            for p in problems[:20]:
                print(f"      {p}")
        else:
            print(f"  {code}: ✓ all required source tokens preserved")
    sys.exit(1 if any_fail else 0)


if __name__ == "__main__":
    main()

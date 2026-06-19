#!/usr/bin/env python3
"""Arjuna Badger Press — glossary / do-not-translate extractor.

Reads a book's canon/ and produces a preserve-list the translator MUST honour:
terms that stay verbatim in EVERY language edition (including the culture-specific
ones). This is what keeps a translation faithful to the press's rule that language
is content, not decoration.

Three classes of preserved token, drawn straight from canon so the list is auditable:

  1. in-language terms  — words tagged `*(real — <lang>)*` or `*(real — <lang> proverb)*`
                          in READER_GLOSSARY.md. e.g. isiZulu "Ngiyabonga", "Yebo",
                          "Umuntu ngumuntu ngabantu". These appear untranslated ON
                          PURPOSE and must survive into the Afrikaans, Spanish, etc.
                          editions exactly as written.
  2. invented entities  — `*(in the novel)*` glossary terms + the canon NAMES.md proper
                          nouns (SAGE, the Court, Guardian, IAOC, ATLAS, WOLF, character
                          names, place names). Constant across all languages.
  3. proper names       — bold proper nouns harvested from NAMES.md.

Usage:
    tools/extract_glossary.py <book-dir>            # prints JSON to stdout
    tools/extract_glossary.py <book-dir> -o out.json

<book-dir> is e.g. books/resonance (the dir containing canon/).
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

# `**Term** *(real — isiZulu)*`  or  `**Term** *(real — isiZulu proverb)*`
RE_IN_LANG = re.compile(
    r"\*\*(?P<term>[^*]+?)\*\*\s*\*\(real\s*[—–-]\s*(?P<lang>[A-Za-z][A-Za-z ]*?)(?:\s+proverb)?\)\*"
)
# `**Term** *(in the novel)*`
RE_INVENTED = re.compile(r"\*\*(?P<term>[^*]+?)\*\*\s*\*\(in the novel\)\*")
# any bold proper noun: starts with a capital, looks like a name not a sentence
RE_BOLD = re.compile(r"\*\*(?P<term>[A-Z][A-Za-z0-9'’.\-/ ]{1,40}?)\*\*")

# A tag counts as a real human language ONLY if it's in this allow-list. Everything
# else tagged `*(real — X)*` is a category (food, history, geography…). We split those
# into two fates:
#   - CULTURAL_TAGS  → kept verbatim too (flavour words: biltong, veld, stoep, rooibos),
#                      but filed as cultural_terms, NOT mislabelled as a language.
#   - anything else  → ignored for the preserve-list (history/tech/institutions are
#                      concepts, not tokens to freeze).
# Matching is substring-insensitive so "south african word"/"south african food" hit.
LANGUAGE_TAGS = {"isizulu", "zulu", "afrikaans", "xhosa", "sesotho", "setswana",
                 "arabic", "swahili", "amharic", "tamil", "marathi", "hindi",
                 "mongolian", "mandarin", "japanese", "spanish", "french"}
CULTURAL_TAG_HINTS = ("word", "food", "drink", "dish")  # SA "word"/"food"/"drink" → flavour


def _classify_tag(lang: str) -> str:
    """Return 'language', 'cultural', or 'ignore' for a `*(real — <lang>)*` tag."""
    l = lang.lower()
    if l in LANGUAGE_TAGS or any(t == l for t in LANGUAGE_TAGS):
        return "language"
    if any(h in l for h in CULTURAL_TAG_HINTS):
        return "cultural"
    return "ignore"

# Bold harvest noise — section labels / role words in NAMES.md tables that aren't names.
NAME_STOPWORDS = {
    "protagonist", "mentor", "scientist", "confidant", "collaborator", "father",
    "mother", "ceo", "union rep", "hardware vp", "judge", "male names",
}


def _clean(t: str) -> str:
    return re.sub(r"\s+", " ", t).strip()


def _looks_like_sentence(t: str) -> bool:
    """Heuristic: a bold span that's instructional prose, not a proper noun.

    NAMES.md tables carry bold imperatives like 'Name meanings matter' and
    'Honor apartheid legacy in casting'. A real name is short and mostly
    capitalised; a sentence has lowercase content words and/or >3 tokens.
    """
    words = t.split()
    if len(words) > 3:
        return True
    # any non-first word lowercase → reads as a phrase ("Name meanings matter")
    return any(w[:1].islower() for w in words[1:])


def extract(book_dir: Path) -> dict:
    canon = book_dir / "canon"
    if not canon.is_dir():
        sys.exit(f"extract_glossary: no canon/ under {book_dir}")

    in_language: dict[str, set[str]] = {}   # lang -> {terms}
    cultural: set[str] = set()              # flavour words (veld, biltong…)
    invented: set[str] = set()
    names: set[str] = set()

    glossary = canon / "READER_GLOSSARY.md"
    if glossary.is_file():
        text = glossary.read_text(encoding="utf-8")
        for m in RE_IN_LANG.finditer(text):
            lang = _clean(m["lang"])
            term = _clean(m["term"])
            kind = _classify_tag(lang)
            if kind == "language":
                in_language.setdefault(lang.lower(), set()).add(term)
            elif kind == "cultural":
                cultural.add(term)
            # else: ignore (history/tech/institutions/etc.)
        for m in RE_INVENTED.finditer(text):
            invented.add(_clean(m["term"]))

    names_md = canon / "NAMES.md"
    if names_md.is_file():
        for m in RE_BOLD.finditer(names_md.read_text(encoding="utf-8")):
            term = _clean(m["term"])
            if term.lower() in NAME_STOPWORDS:
                continue
            if _looks_like_sentence(term):      # instructional prose, not a name
                continue
            names.add(term)

    # Invented entities also show up as bold names; fold them in for safety.
    names |= invented

    return {
        "book": book_dir.name,
        "preserve_verbatim_all_languages": {
            "in_language_terms": {k: sorted(v) for k, v in sorted(in_language.items())},
            "cultural_terms": sorted(cultural),
            "invented_entities": sorted(invented),
            "proper_names": sorted(names),
        },
        "note": (
            "Every token above MUST appear UNCHANGED in every translated edition. "
            "in_language_terms are deliberately-untranslated source words (keep verbatim); "
            "invented_entities and proper_names are story-constant nouns. "
            "Do NOT add footnotes or inline glosses the source doesn't have."
        ),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("book_dir", type=Path)
    ap.add_argument("-o", "--out", type=Path)
    a = ap.parse_args()
    data = extract(a.book_dir)
    out = json.dumps(data, ensure_ascii=False, indent=2)
    if a.out:
        a.out.write_text(out + "\n", encoding="utf-8")
        print(f"wrote {a.out}")
    else:
        print(out)


if __name__ == "__main__":
    main()

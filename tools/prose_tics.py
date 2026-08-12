#!/usr/bin/env python3
"""Blind machine-tell + duplication scanner for a book's chapters.

Free and local — no API calls. Counts the tells named in the de-LLM contract
(books/resonance/canon/STYLE_GUIDE.md, "MACHINE-TELL TABOOS") and finds repeated
prose, so the metered rewrite pass only spends tokens where the text needs it.

Duplication has two kinds and they are NOT the same problem:
  * MOTIF  — a deliberate refrain (a slogan, a stated goal, a repeated image).
             Load these from a protect-list; they are the book's spine.
  * DRIFT  — the same sentence re-emitted across chapters because the drafting
             model re-anchored on the story bible. This is what we cut.

Usage:
    python3 tools/prose_tics.py books/the-prophet-and-his-brother [--protect FILE]
"""

from __future__ import annotations

import argparse
import collections
import json
import pathlib
import re
import sys

# The named tells, as regexes. Source: the de-LLM contract, tells 1-12.
TELLS = {
    "almost_emotion": r"\balmost\s+(?:[a-z]+ed|[a-z]+ing|gentle|kind|tender|soft|warm|human)\b",
    "reframe_not_x_but_y": r"\b(?:not|wasn't|isn't|wasn’t|isn’t)\s+[^.,;]{2,40},?\s+but\s+",
    "em_dash": r"—",
    "em_dash_spaced": r"\s—\s",
    "something_placeholder": r"\bsomething\s+(?:in|about|moved|shifted|eased|loosened|tightened|passed)\b",
    "the_way": r"\bthe way\b",
    "not_a_x_fragment": r"(?m)^\s*Not a [a-z]+\.",
    "which_translation": r"\bwhich,? from [A-Z][a-z]+,? meant\b",
    "hedges": r"\b(?:seemed to|appeared to|perhaps|somewhat|sort of|kind of)\b",
    "weasel": r"\b(?:obviously|clearly|literally|actually|basically)\b",
    "very_really": r"\b(?:very|really)\s+[a-z]+",
    "wordy_connective": r"\b(?:the fact that|in order to|in terms of|due to the fact)\b",
}

# Advisory target bands, per 1000 words. Over the ceiling = go look.
BANDS = {
    "almost_emotion": 0.05,
    "reframe_not_x_but_y": 0.15,
    "em_dash": 4.0,
    "em_dash_spaced": 0.0,
    "something_placeholder": 0.15,
    "the_way": 0.60,
    "not_a_x_fragment": 0.05,
    "which_translation": 0.05,
    "hedges": 0.50,
    "weasel": 0.30,
    "very_really": 0.40,
    "wordy_connective": 0.10,
}

MIN_SENTENCE_WORDS = 6
NGRAM = 7
NGRAM_MIN_HITS = 3


def strip_markup(text: str) -> str:
    text = re.sub(r"(?m)^#.*$", "", text)          # headings
    text = re.sub(r"(?m)^\s*[-*]{3,}\s*$", "", text)  # rules
    return text


def sentences(text: str) -> list[str]:
    out = []
    for raw in re.split(r"(?<=[.!?])[\s”\"']+", strip_markup(text)):
        s = " ".join(raw.split())
        if len(s.split()) >= MIN_SENTENCE_WORDS:
            out.append(s)
    return out


def normalise(s: str) -> str:
    # Collapse whitespace too: punctuation becomes a space, so "cunt. be" and
    # "cunt be" must land on the same string or a protected motif reads as drift.
    return " ".join(re.sub(r"[^a-z0-9 ]", " ", s.lower()).split())


def words(text: str) -> list[str]:
    return normalise(strip_markup(text)).split()


def load_protect(path: pathlib.Path | None) -> list[str]:
    if not path or not path.exists():
        return []
    return [normalise(l) for l in path.read_text().splitlines()
            if l.strip() and not l.startswith("#")]


def is_protected(phrase: str, protect: list[str]) -> bool:
    return any(p and p in phrase for p in protect)


def scan(book: pathlib.Path, protect: list[str]) -> dict:
    chapters = sorted((book / "build" / "chapters").glob("*.md"))
    if not chapters:
        sys.exit(f"no chapters under {book}/build/chapters")

    per_chapter, sent_index, gram_index = [], collections.defaultdict(list), collections.defaultdict(set)
    gram_counts = collections.Counter()

    for path in chapters:
        text = path.read_text()
        wc = len(words(text))
        counts = {name: len(re.findall(rx, text, flags=re.I))
                  for name, rx in TELLS.items()}
        flags = [n for n, c in counts.items()
                 if wc and (c / wc * 1000) > BANDS.get(n, 999)]
        per_chapter.append({
            "chapter": path.name, "words": wc, "counts": counts,
            "per_1k": {n: round(c / wc * 1000, 2) if wc else 0 for n, c in counts.items()},
            "over_band": flags,
        })
        for s in sentences(text):
            sent_index[normalise(s)].append((path.name, s))
        w = words(text)
        for i in range(max(0, len(w) - NGRAM)):
            g = " ".join(w[i:i + NGRAM])
            gram_counts[g] += 1
            gram_index[g].add(path.name)

    dup_sentences = [
        {"hits": len(v), "chapters": sorted({c for c, _ in v}), "text": v[0][1],
         "protected": is_protected(k, protect)}
        for k, v in sent_index.items() if len(v) > 1
    ]
    dup_sentences.sort(key=lambda d: -d["hits"])

    dup_grams = [
        {"hits": n, "chapters": len(gram_index[g]), "text": g,
         "protected": is_protected(g, protect)}
        for g, n in gram_counts.items() if n >= NGRAM_MIN_HITS
    ]
    dup_grams.sort(key=lambda d: -d["hits"])

    total_words = sum(c["words"] for c in per_chapter)
    lengths = [c["words"] for c in per_chapter if c["words"] > 1000]
    spread = (max(lengths) - min(lengths)) / (sum(lengths) / len(lengths)) if lengths else 0

    return {
        "book": book.name,
        "chapters": len(chapters),
        "total_words": total_words,
        "length_spread": round(spread, 3),
        "per_chapter": per_chapter,
        "duplicate_sentences": dup_sentences,
        "duplicate_ngrams": dup_grams,
    }


def report(r: dict) -> None:
    print(f"{r['book']}: {r['chapters']} chapters, {r['total_words']:,} words")
    print(f"length spread (max-min)/mean = {r['length_spread']}  "
          f"({'EVEN — structural tell' if r['length_spread'] < 0.25 else 'varied'})\n")

    print("per-chapter tells over band:")
    for c in r["per_chapter"]:
        if c["over_band"]:
            detail = ", ".join(f"{n}={c['counts'][n]}({c['per_1k'][n]}/1k)" for n in c["over_band"])
            print(f"  {c['chapter']:<12} {detail}")

    drift = [d for d in r["duplicate_sentences"] if not d["protected"]]
    motif = [d for d in r["duplicate_sentences"] if d["protected"]]
    print(f"\nduplicate sentences: {len(drift)} DRIFT (cut) / {len(motif)} motif (keep)")
    for d in drift[:20]:
        print(f"  x{d['hits']} {','.join(d['chapters'])}: {d['text'][:100]}")

    gdrift = [d for d in r["duplicate_ngrams"] if not d["protected"]]
    print(f"\nrepeated {NGRAM}-grams (3+): {len(gdrift)} drift / "
          f"{len(r['duplicate_ngrams']) - len(gdrift)} motif")
    for d in gdrift[:15]:
        print(f"  x{d['hits']} ({d['chapters']} ch) {d['text']}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("book", type=pathlib.Path)
    ap.add_argument("--protect", type=pathlib.Path,
                    help="file of deliberate motifs, one per line, never flagged as drift")
    ap.add_argument("--json", type=pathlib.Path, help="write the full scan here")
    args = ap.parse_args()

    result = scan(args.book, load_protect(args.protect))
    report(result)
    if args.json:
        args.json.write_text(json.dumps(result, indent=2))
        print(f"\nwrote {args.json}")


if __name__ == "__main__":
    main()

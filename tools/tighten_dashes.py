#!/usr/bin/env python3
"""Set em-dashes tight, per the de-LLM contract. Free, local, deterministic.

The contract (books/resonance/canon/STYLE_GUIDE.md, tell #3) requires em-dashes
set TIGHT — `word—word` — never spaced. That is typography, not judgment, so it
belongs in a deterministic pass rather than in metered model calls.

Only touches spacing around an existing em-dash. Never adds, removes, or converts
a dash; the decision about HOW MANY dashes survive is the model's, made earlier.

PROTECTED MOTIFS ARE EXEMPT. A refrain is quoted verbatim, and its spacing is part
of the quotation. The first version of this script had no protect list — being
"just typography" felt like reason enough to skip it — and it silently rewrote all
22 instances of "Don't be a cunt — be kind." to "cunt—be kind" across the book.
A deterministic pass needs the same guard as a model call; arguably more, because
nobody thinks to check it.

Usage:
    python3 tools/tighten_dashes.py books/<book>/build/chapters --dry-run
    python3 tools/tighten_dashes.py books/<book>/build/chapters \\
        --protect books/<book>/canon/MOTIFS_PROTECTED.txt
"""

from __future__ import annotations

import argparse
import pathlib
import re

# Spaced em-dash between two word characters. Deliberately narrow: it will not
# touch a dash at the start of a line (dialogue dash) or around markdown syntax.
SPACED = re.compile(r"(?<=[\w\)\]\"'’”])[ \t]*—[ \t]*(?=[\w\(\[\"'‘“])")


def motif_patterns(path: pathlib.Path | None) -> list[re.Pattern]:
    """Build loose matchers for each protected motif.

    A motif is stored in plain text ("don't be a cunt. be kind.") but appears in
    the prose with different punctuation ("Don't be a cunt — be kind."). So match
    on the word sequence and let any punctuation, dash or spacing sit between.
    """
    if not path or not path.exists():
        return []
    pats = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        words = re.findall(r"[A-Za-z0-9]+", line)
        if len(words) < 2:
            continue
        pats.append(re.compile(r"[\s\W]{0,4}".join(re.escape(w) for w in words),
                               re.IGNORECASE))
    return pats


def protect_spans(text: str, pats: list[re.Pattern]) -> list[tuple[int, int]]:
    return [m.span() for p in pats for m in p.finditer(text)]


def tighten(text: str, pats: list[re.Pattern]) -> tuple[str, int, int]:
    spans = protect_spans(text, pats)
    skipped = 0

    def repl(m: re.Match) -> str:
        nonlocal skipped
        if any(s <= m.start() and m.end() <= e for s, e in spans):
            skipped += 1
            return m.group(0)          # inside a refrain — leave it exactly as written
        return "—"

    out, n = SPACED.subn(repl, text)
    return out, n - skipped, skipped


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("chapters", type=pathlib.Path)
    ap.add_argument("--protect", type=pathlib.Path,
                    help="motif file whose lines must keep their exact spacing")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    pats = motif_patterns(args.protect)

    files = sorted(args.chapters.glob("*.md"))
    if not files:
        raise SystemExit(f"no .md under {args.chapters}")

    total_fixed = total_skipped = 0
    for path in files:
        text = path.read_text()
        fixed, n, skipped = tighten(text, pats)
        total_fixed += n
        total_skipped += skipped
        if n or skipped:
            note = f", {skipped} left inside protected motifs" if skipped else ""
            print(f"  {path.name}: {n} tightened{note}")
            if not args.dry_run and fixed != text:
                path.write_text(fixed)

    verb = "would tighten" if args.dry_run else "tightened"
    print(f"\n{verb} {total_fixed} spaced em-dashes across {len(files)} files; "
          f"{total_skipped} left untouched inside protected motifs")


if __name__ == "__main__":
    main()
